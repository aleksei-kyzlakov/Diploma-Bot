from api_requests import request_all

from db import (db, get_or_create_user, subscribe_user, set_recent_rates,
                unsubscribe_user, default_currency_db, get_recent_rates)

from utils import main_keyboard, sub_keyboard

from telegram import ForceReply

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
    response = f"Курсы валют на {rates['datetime']} в {user['default_currency']}:\n"
    rates = rates['currency']
    for i in settings.CURRENCY_SYMBOLS:
        response += f"{i}: {rates[i]/rates[user['default_currency']]}" + "\n"
    response += "\nВыберите валюту, чтобы подписаться на рассылку"
    update.message.reply_text(response, reply_markup=sub_keyboard(0,1))


def list_crypto(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    rates = get_recent_rates(db)
    response = f"Курсы криптовалют на {rates['datetime']} в {user['default_currency']}:\n"
    for i in settings.CRYPTO_SYMBOLS:
        response += f"{i}: {rates['crypto'][i]*rates['currency'][user['default_currency']]}" + "\n"
        #response += '\n'
    update.message.reply_text(response, reply_markup=sub_keyboard(1,2))


def list_stocks(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    rates = get_recent_rates(db)
    response = f"Курсы акций на {rates['datetime']} в {user['default_currency']}:\n"
    for i in settings.STOCKS_SYMBOLS:
        response += f"{i}: {rates['stocks'][i]*rates['currency'][user['default_currency']]}" + "\n"
        #response += '\n'
    update.message.reply_text(response, reply_markup=sub_keyboard(2,3))


def subscribe(update, context):
    pass


def populate_DB(update, context):
    set_recent_rates(db, request_all())


def echo(update, context):
    text = update.message.text
    update.message.reply_text('Echo: '+text)