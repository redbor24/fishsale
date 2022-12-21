import logging

from email_validate import validate
from environs import Env
from redis import Redis
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (CallbackQueryHandler, CommandHandler, Filters,
                          MessageHandler, Updater)

from functools import partial

from shop_moltin import MoltinShop

_database = None

KG_1 = '1 кг'
KG_3 = '3 кг'
KG_5 = '5 кг'
KG_15 = '15 кг'
BACK_BTN_NAME = 'Назад'

CART_BTN_NAME = 'Корзина'

START = 'START'
HANDLE_DESCRIPTION = 'HANDLE_DESCRIPTION'
HANDLE_MENU = 'HANDLE_MENU'
HANDLE_CART = 'HANDLE_CART'
PAY_CART = 'PAY_CART'
WAITING_EMAIL = 'WAITING_EMAIL'
TO_BACK = 'BACK'

weights_keyboard_template = [KG_1, KG_3, KG_5, KG_15]

logger = logging.getLogger('tgbot')


def get_weights_kbd(product_id, back_button=False, back_state=''):
    weights_part = []
    for elem in weights_keyboard_template:
        callback_value = f'{product_id}#{elem.replace(" кг", "")}'
        weights_part.append(InlineKeyboardButton(elem, callback_data=callback_value))

    weights_keyboard = [weights_part]

    if back_button:
        weights_keyboard.append([InlineKeyboardButton(BACK_BTN_NAME, callback_data=back_state)])

    return weights_keyboard


def get_back_kbd(state):
    return [InlineKeyboardButton(BACK_BTN_NAME, callback_data=state)]


def get_products_kbd(shop, with_back_button=False):
    keyboard = []
    for product in shop.get_products():
        keyboard.append(
            [
                InlineKeyboardButton(
                    f"{product['attributes']['name']} ({product['id']})",
                    callback_data=product['id']
                )
            ]
        )

    keyboard.append([InlineKeyboardButton(CART_BTN_NAME, callback_data=HANDLE_CART)])

    if with_back_button:
        keyboard.append([InlineKeyboardButton(BACK_BTN_NAME, callback_data=TO_BACK)])

    return keyboard


def start(update, _, shop):
    update.effective_message.reply_text(
        text='Выберите продукт:',
        reply_markup=InlineKeyboardMarkup(get_products_kbd(shop)))

    return HANDLE_MENU


def handle_menu(update, context, shop):
    """
    Из списка продуктов.
    Показ информации по продукту.
    """
    query = update.callback_query
    query.answer()
    if query.data == HANDLE_CART:
        return handle_cart(update, context, shop)

    product_id = query.data
    message_id = update.effective_message.message_id
    chat_id = update.effective_message.chat_id

    product_details = shop.get_product_details(product_id)
    product_photo_url = shop.get_product_image(product_id)

    caption = f"Название: {product_details['name']}\n" \
              f"Описание: {product_details['description']}\n" \
              f"Цена: {product_details['price']} {product_details['currency']} за кг.\n" \
              f"Доступно для заказа: {product_details['available']} кг.\n"
    kbd = InlineKeyboardMarkup(get_weights_kbd(product_id, True, START))

    if product_photo_url:
        context.bot.send_photo(chat_id=chat_id, caption=caption, photo=product_photo_url, reply_markup=kbd)
    else:
        context.bot.send_message(chat_id=chat_id, text=caption, reply_markup=kbd)

    context.bot.delete_message(chat_id=chat_id, message_id=message_id)

    return HANDLE_DESCRIPTION


def handle_description(update, _, shop):
    """
    Из продукта.
    Показ детальной информации о продукте.
    Выбор веса продукта для добавления в корзину.
    Назад.
    """
    query = update.callback_query
    query.answer()

    product_id, quantity = query.data.split('#')
    chat_id = update.effective_message.chat_id
    db_identifier = f'{chat_id}_cart_id'

    db_value = _database.get(db_identifier)
    cart_id = None
    if db_value:
        cart_id = db_value.decode('utf-8')

    if not cart_id:
        cart_id = shop.create_cart(chat_id)
        _database.set(db_identifier, cart_id)

    cart = shop.add_product_to_cart(cart_id, product_id, quantity)
    if cart['result']:
        query.message.reply_text(
            text='Товар добавлен в корзину',
            reply_markup=InlineKeyboardMarkup([get_back_kbd(START)])
        )
        return HANDLE_DESCRIPTION
    else:
        query.message.reply_text(
            text=f"Ошибка!\n{cart['message']}",
            reply_markup=InlineKeyboardMarkup([get_back_kbd(product_id)])
        )
        return HANDLE_MENU


def handle_cart(update, context, shop):
    """
    Из списка продуктов.
    Просмотр корзины.
    """
    query = update.callback_query

    if query.data == START:
        return START

    elif query.data == HANDLE_CART:
        chat_id = update.effective_message.chat_id

        db_value = _database.get(f'{chat_id}_cart_id')
        cart_buttons = []
        if db_value:
            cart_id = db_value.decode('utf-8')
            cart = shop.get_cart(cart_id)
            cart_description = ''
            buttons = []

            for position in cart['products']:
                cart_description += f"{position['name']}, {position['quantity']} кг, " \
                                    f"{position['cost']} {position['currency']}\n"
                buttons.append(
                    InlineKeyboardButton(
                        f'Удалить из корзины {position["name"]}',
                        callback_data=position['cart_item_id'])
                )
            cart_description += f'Итого: {cart["summa"]}'

            cart_buttons.append(buttons)
            cart_buttons.append([InlineKeyboardButton('Оплатить', callback_data=PAY_CART)])
        else:
            cart_description = 'Ваша корзина пуста'

        cart_buttons.append(get_back_kbd(START))
        query.message.reply_text(
            text=cart_description,
            reply_markup=InlineKeyboardMarkup(cart_buttons)
        )
        return HANDLE_CART

    elif query.data == PAY_CART:
        query.message.reply_text(
            text='Для создания заказа напишите email'
        )
        return WAITING_EMAIL

    else:
        chat_id = update.effective_message.chat_id

        db_identifier = f'{chat_id}_cart_id'
        db_value = _database.get(db_identifier)
        if db_value:
            cart_id = db_value.decode('utf-8')

        shop.del_product_from_cart(cart_id, query.data)
        cart = shop.get_cart(cart_id)
        if not cart["summa"]:
            _database.delete(db_identifier)

        update.callback_query.data = HANDLE_CART
        handle_cart(update, context, shop)
        return HANDLE_CART


def waiting_email(update, context, shop):
    user_email = update.message.text
    chat_id = update.effective_message.chat_id

    if not validate(
            email_address=user_email,
            check_format=True,
            check_dns=False,
            check_smtp=False,
            check_blacklist=False
    ):
        context.bot.send_message(
            chat_id=chat_id,
            text='Введён некорректный email',
            reply_markup=InlineKeyboardMarkup([get_back_kbd(TO_BACK)])
        )
    else:
        customer = shop.find_customer_by_email(user_email)
        if not customer:
            shop.save_customer(user_email, user_email)
        context.bot.send_message(
            chat_id=chat_id,
            text=f'Ваш email {user_email} сохранён. Наши менеджеры свяжутся с вами в ближайшее время.',
            reply_markup=InlineKeyboardMarkup([get_back_kbd(TO_BACK)])
        )
        db_identifier = f'{chat_id}_cart_id'
        cart_id = _database.get(db_identifier).decode('utf-8')
        shop.delete_cart(cart_id)
        _database.delete(db_identifier)

    return START


def handle_users_reply(update, context, shop=None):
    """
    Функция, которая запускается при любом сообщении от пользователя и решает как его обработать.

    Эта функция запускается в ответ на эти действия пользователя:
        * Нажатие на inline-кнопку в боте
        * Отправка сообщения боту
        * Отправка команды боту
    Она получает стейт пользователя из базы данных и запускает соответствующую функцию-обработчик (хэндлер).
    Функция-обработчик возвращает следующее состояние, которое записывается в базу данных.
    Если пользователь только начал пользоваться ботом, Telegram форсит его написать "/start",
    поэтому по этой фразе выставляется стартовое состояние.
    Если пользователь захочет начать общение с ботом заново, он также может воспользоваться этой командой.
    """
    global _database
    if _database is None:
        redis_host = env('REDIS_HOST')
        redis_port = env('REDIS_PORT')
        redis_password = env('REDIS_PASSWORD')
        _database = Redis(host=redis_host, port=redis_port, password=redis_password)

    if update.message:
        user_reply = update.message.text
        chat_id = update.message.chat_id
    elif update.callback_query:
        user_reply = update.callback_query.data
        chat_id = update.callback_query.message.chat_id
    else:
        return

    if user_reply in ('/start', START):
        user_state = START
    else:
        user_state = _database.get(chat_id).decode('utf-8')

    states_functions = {
        START: start,
        HANDLE_MENU: handle_menu,
        HANDLE_DESCRIPTION: handle_description,
        HANDLE_CART: handle_cart,
        WAITING_EMAIL: waiting_email
    }
    state_handler = states_functions[user_state]

    try:
        next_state = state_handler(update, context, shop)
        _database.set(chat_id, next_state)
    except Exception as err:
        logger.error(err)
        context.bot.send_message(
            chat_id=chat_id,
            text=f'Произошла ошибка при выполнении действия. Действие не выполнено. Обратитесь к разработчику.'
        )
        start(update, context, shop)
        _database.set(chat_id, HANDLE_MENU)


def main():
    logging.basicConfig(
        format='%(asctime)s %(name)s:%(levelname)s:%(message)s',
        level=logging.INFO
    )

    env = Env()
    env.read_env()
    tg_token = env('TG_TOKEN')
    shop_client_id = env('SHOP_CLIENT_ID')
    shop_secret_key = env('SHOP_SECRET_KEY')

    moltin_shop = MoltinShop(shop_client_id, shop_secret_key)

    main_handler = partial(handle_users_reply, shop=moltin_shop)

    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CallbackQueryHandler(main_handler))
    dispatcher.add_handler(MessageHandler(Filters.text, main_handler))
    dispatcher.add_handler(CommandHandler('start', main_handler))
    updater.start_polling()


if __name__ == '__main__':
    main()
