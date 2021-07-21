from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


symbols = [['USD','GBP','CNY','JPY','RUB','EUR'],
          ['BTC','ETH','BNB','ADA','HEX','XRP'],
          ['BAC','AAPL','AMC','SPY','VERB']]

inline_keys = []

for i in range(len(symbols[0])):
    inline_keys.append([symbols[0][i]])

print(inline_keys)


options = ['Валюта по умолчанию|',
               'Подписка на валюту|',
               'Подписка на крипто|',
               'Подписка на акции|']

print(options[0]+"!!")               
