from telegram import (ReplyKeyboardMarkup, KeyboardButton, 
                      InlineKeyboardButton, InlineKeyboardMarkup)


def main_keyboard():
    return ReplyKeyboardMarkup([[KeyboardButton('Валюта по умолчанию'), 
                                KeyboardButton('Курсы валют')], 
                                [KeyboardButton('Курсы крипто'),
                                KeyboardButton('Курсы акций')],
                                [KeyboardButton('заполнить базу')]], 
                                resize_keyboard=True)


def sub_keyboard(keyset,option):
    symbols = [['USD','GBP','CNY','JPY','RUB','EUR'],
              ['BTC','ETH','BNB','ADA','HEX','XRP'],
              ['BAC','AAPL','AMC','SPY','VERB']]
    options = ['default|', 'sub_cur|', 'sub_crypto|', 'sub_stock|']
    inline_keys = [[]]
    for i in range(len(symbols[keyset])):
        inline_keys[0].append(InlineKeyboardButton(symbols[keyset][i], 
                            callback_data=options[option]+symbols[keyset][i]))
    return InlineKeyboardMarkup(inline_keys)
