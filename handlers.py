from api_requests import request_all
from datetime import datetime

from db import (db, get_or_create_user, set_recent_rates,
                default_currency_db, get_recent_rates,
                sub_currency_db, sub_crypto_db, sub_stocks_db)

from utils import main_keyboard, sub_keyboard

import settings

def greeting(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    update.message.reply_text(f"Привет {user['first_name']}!", reply_markup=main_keyboard())
    

def default_currency_handler(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    update.message.reply_text(f'''Ваша валюта по умолчанию {user['default_currency']}. 
    Выберите валюту по умолчанию. 
    Курсы валют будут отображаться относительно выбранной.''', reply_markup=sub_keyboard(0,0))


def default_currency_reply(update, context):
    update.callback_query.answer()
    callback_type, symbol = update.callback_query.data.split("|")
    user = get_or_create_user(db, update.effective_user, update.effective_chat.id)
    default_currency_db(db, user, symbol)
    update.callback_query.message.edit_text(f"Выбрана валюта по умолчанию {symbol}", reply_markup=None)


def list_currency(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    rates = get_recent_rates(db)
    msg = f"Курсы валют на {rates['datetime']} в {user['default_currency']}:\n\n"
    rates = rates['currency']
    for i in settings.CURRENCY_SYMBOLS:
        msg += f"{i}: {rates[i]/rates[user['default_currency']]}" + "\n"
    msg += "\nВыберите валюту, чтобы подписаться на рассылку"
    try:
        msg += f"\nВаши подписки: {user['sub_currency']}"
    except:
        pass
    update.message.reply_text(msg, reply_markup=sub_keyboard(0,1))


def list_crypto(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    rates = get_recent_rates(db)
    msg = f"Курсы криптовалют на {rates['datetime']} в {user['default_currency']}:\n\n"
    for i in settings.CRYPTO_SYMBOLS:
        msg += f"{i}: {rates['crypto'][i]*rates['currency'][user['default_currency']]}" + "\n"
    msg += "\nВыберите криптовалюту, чтобы подписаться на рассылку"
    try:
        msg += f"\nВаши подписки: {user['sub_crypto']}"
    except:
        pass
    update.message.reply_text(msg, reply_markup=sub_keyboard(1,2))


def list_stocks(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    rates = get_recent_rates(db)
    msg = f"Курсы акций на {rates['datetime']} в {user['default_currency']}:\n\n"
    for i in settings.STOCKS_SYMBOLS:
        msg += f"{i}: {rates['stocks'][i]*rates['currency'][user['default_currency']]}" + "\n"
    msg += "\nВыберите компании, чтобы подписаться на рассылку"
    try:
        msg += f"\nВаши подписки: {user['sub_stocks']}"
    except:
        pass
    update.message.reply_text(msg, reply_markup=sub_keyboard(2,3))


def sub_currency(update, context):
    update.callback_query.answer()
    callback_type, symbol = update.callback_query.data.split("|")
    user = get_or_create_user(db, update.effective_user, update.effective_chat.id)
    if sub_currency_db(db, user, symbol):
        user = get_or_create_user(db, update.effective_user, update.effective_chat.id)
        msg = f"Вы подписались на рассылку курса {symbol}"
    else:
        user = get_or_create_user(db, update.effective_user, update.effective_chat.id)
        msg = f"Вы отписались от рассылки курса {symbol}"
    try:
        msg += f"\nВаши подписки: {user['sub_currency']}"
    except:
        pass
    update.callback_query.message.edit_text(msg, reply_markup=sub_keyboard(0,1))


def sub_crypto(update, context):
    update.callback_query.answer()
    callback_type, symbol = update.callback_query.data.split("|")
    user = get_or_create_user(db, update.effective_user, update.effective_chat.id)
    if sub_crypto_db(db, user, symbol):
        user = get_or_create_user(db, update.effective_user, update.effective_chat.id)
        msg = f"Вы подписались на рассылку курса {symbol}"
    else:
        user = get_or_create_user(db, update.effective_user, update.effective_chat.id)
        msg = f"Вы отписались от рассылки курса {symbol}"
    try:
        msg += f"\nВаши подписки: {user['sub_crypto']}"
    except:
        pass
    update.callback_query.message.edit_text(msg, reply_markup=sub_keyboard(1,2))


def sub_stocks(update, context):
    update.callback_query.answer()
    callback_type, symbol = update.callback_query.data.split("|")
    user = get_or_create_user(db, update.effective_user, update.effective_chat.id)
    if sub_stocks_db(db, user, symbol):
        user = get_or_create_user(db, update.effective_user, update.effective_chat.id)
        msg = f"Вы подписались на рассылку курса {symbol}"
    else:
        user = get_or_create_user(db, update.effective_user, update.effective_chat.id)
        msg = f"Вы отписались от рассылки курса {symbol}"
    try:
        msg += f"\nВаши подписки: {user['sub_stocks']}"
    except:
        pass
    update.callback_query.message.edit_text(msg, reply_markup=sub_keyboard(2,3))


def populate_DB(update, context):
    set_recent_rates(db, request_all())


def echo(update, context):
    text = update.message.text
    update.message.reply_text('Echo: '+text)