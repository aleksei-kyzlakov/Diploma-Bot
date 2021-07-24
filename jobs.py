from api_requests import request_all

from db import db, set_recent_rates, get_recent_rates, get_sub

from telegram.error import BadRequest

def hourly_db_repopulation(context):
    set_recent_rates(db, request_all())

def sub_announce(context):
    rates = get_recent_rates(db)
    msg = ''
    for user in get_sub(db, 'sub_currency'):
        msg += f"Вы подписаны на рассылку {user['sub_currency']}\n\n"
        for sub in user['sub_currency'].split('|'):
            msg += f"{sub}: {rates['currency'][sub]/rates['currency'][user['default_currency']]}" + "\n"
        msg += '\n'
    for user in get_sub(db, 'sub_crypto'):
        msg += f"Вы подписаны на рассылку {user['sub_crypto']}\n\n"
        for sub in user['sub_crypto'].split('|'):
            msg += f"{sub}: {rates['crypto'][sub]*rates['currency'][user['default_currency']]}" + "\n"
        msg += '\n'
    for user in get_sub(db, 'sub_stocks'):
        msg += f"Вы подписаны на рассылку {user['sub_stocks']}\n\n"
        for sub in user['sub_stocks'].split('|'):
            msg += f"{sub}: {rates['stocks'][sub]*rates['currency'][user['default_currency']]}" + "\n"
    try:
        context.bot.send_message(chat_id=user['chat_id'], text=msg)
    except BadRequest:
        print(f"Chat {user['chat_id']} not found")
