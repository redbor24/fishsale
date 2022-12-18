# Telegram-bot "Магазин"
Telegram-bot предоставляет покупателю интерфейс для заказа товаров в онлайн-магазине.

## Цели проекта
Код реализует учебный проект [Devman](https://dvmn.org) - 
[Урок 5. Продаём рыбу в Telegram](https://dvmn.org/modules/chat-bots/lesson/fish-shop/)
в курсе по Python и веб-разработке.

# Установка и запуск

## Установка
- Скачайте код проекта
```commandline
git clone https://github.com/redbor24/fishsale.git
```
- Перейдите в папку проекта
```commandline
cd fishsale
```
- Установите зависимости
```
pip install -r requirements.txt
```

## Создайте файл `.env`
Создайте аккаунт на [redis.com](http://redis.com) и впишите сюда хост, порт и пароль для созданной БД.
  - `REDIS_HOST=<имя хоста>`
  - `REDIS_PORT=<порт для подключения>`
  - `REDIS_PASSWORD=<пароль>`

[Получите](https://t.me/botfather) Телеграм-токен
  - `TG_TOKEN=` токен для работы с Telegram-API

Получите у куратора курса доступ к [Moltin](https://euwest.cm.elasticpath.com/), зарегистрируйтесь там
и со страницы **Application keys** возьмите: 
  - `SHOP_CLIENT_ID=`**Client ID** с вкладки **Application Keys**
  - `SHOP_SECRET_KEY=`**Client Secret** с вкладки **Legacy Key**

## Запуск 
```
python tgbot.py
```

## Тестовый бот 
Ознакомиться с работой бота можно [здесь](https://t.me/fishsale_bot) 
