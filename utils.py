from telegram import (ReplyKeyboardMarkup, KeyboardButton, 
                      InlineKeyboardButton, InlineKeyboardMarkup)


def main_keyboard():
    return ReplyKeyboardMarkup([[KeyboardButton('Валюта по умолчанию'), 
                                KeyboardButton('Курсы валют')], 
                                [KeyboardButton('Курсы крипто'),
                                KeyboardButton('Курсы акций')],
                                [KeyboardButton('DEMO заполнить базу')]], 
                                resize_keyboard=True)


def sub_keyboard(keyset, option):
    symbols = [['USD','GBP','CNY','JPY','RUB','EUR'],
              ['BTC','ETH','BNB','ADA','HEX','XRP'],
              ['BAC','AAPL','AMC','SPY','VERB']]
    options = ['default|', 'sub_cur|', 'sub_crypto|', 'sub_stocks|']
    buttons = []
    chosen_option = options[option]
    for symbol in symbols[keyset]:
        key = symbol
        callback_data = f'{chosen_option}{key}'
        button = InlineKeyboardButton(key, callback_data=callback_data)
        buttons.append(button)
    return InlineKeyboardMarkup([buttons])
