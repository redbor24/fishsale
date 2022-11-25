"""
Работает с этими модулями:

python-telegram-bot==13.14
redis==3.2.1
"""
import logging

from redis import Redis
from environs import Env
from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (CallbackQueryHandler, CommandHandler, Filters,
                          MessageHandler, Updater)

from shop_moltin import get_products

_database = None
shop_client_id = None
_glb_counter = 0

kg_1 = '1 кг'
kg_3 = '3 кг'
kg_5 = '5 кг'

product_keyboard = [
        [InlineKeyboardButton(kg_1, callback_data=kg_1),
         InlineKeyboardButton(kg_3, callback_data=kg_3),
         InlineKeyboardButton(kg_5, callback_data=kg_5)],
        [InlineKeyboardButton('Назад', callback_data='BACK')]
    ]


def start(update, _):
    global shop_client_id

    products = get_products(shop_client_id)
    keyboard = []
    for product in products:
        name = product['attributes']['name']
        product_id = product['id']
        keyboard.append([InlineKeyboardButton(name, callback_data=product_id)])

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Выберите:', reply_markup=reply_markup)
    return 'HANDLE_MENU'


def handle_menu(update, context):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(
        text=f"Selected option: {query.data}",
        reply_markup=InlineKeyboardMarkup(product_keyboard)
    )
    return 'HANDLE_DESCRIPTION'


def handle_description(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text=f"Selected option: {query.data}",
    )
    # return 'START'
    return 'HANDLE_MENU'


def echo(update, context):
    """
    Хэндлер для состояния ECHO.

    Бот отвечает пользователю тем же, что пользователь ему написал.
    Оставляет пользователя в состоянии ECHO.
    """
    users_reply = update.message.text
    update.message.reply_text(users_reply)
    return 'ECHO'


def handle_users_reply(update, context):
    global _glb_counter
    _glb_counter += 1
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

    db = get_database_connection()

    if update.message:
        user_reply = update.message.text
        chat_id = update.message.chat_id
    elif update.callback_query:
        user_reply = update.callback_query.data
        chat_id = update.callback_query.message.chat_id
    else:
        return

    if user_reply == '/start':
        user_state = 'START'
    else:
        user_state = db.get(chat_id).decode("utf-8")

    states_functions = {
        'START': start,
        'ECHO': echo,
        'HANDLE_MENU': handle_menu,
        'HANDLE_DESCRIPTION': handle_description
    }
    state_handler = states_functions[user_state]

    # Если вы вдруг не заметите, что python-telegram-bot перехватывает ошибки.
    # Оставляю этот try...except, чтобы код не падал молча.
    # Этот фрагмент можно переписать.
    try:
        next_state = state_handler(update, context)
        db.set(chat_id, next_state)
    except Exception as err:
        print(err)


def get_database_connection():
    """
    Возвращает конекшн с базой данных Redis, либо создаёт новый, если он ещё не создан.
    """
    global _database
    if _database is None:
        redis_host = env('REDIS_HOST')
        redis_port = env('REDIS_PORT')
        redis_password = env('REDIS_PASSWORD')
        _database = Redis(host=redis_host, port=redis_port, password=redis_password)
    return _database


if __name__ == '__main__':
    env = Env()
    env.read_env()
    tg_token = env('TG_TOKEN')
    shop_client_id = env('SHOP_CLIENT_ID')

    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CallbackQueryHandler(handle_users_reply))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_users_reply))
    dispatcher.add_handler(CommandHandler('start', handle_users_reply))
    updater.start_polling()
