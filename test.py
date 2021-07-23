from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta
from db import db, get_recent_rates, get_or_create_user

symbols = [['USD','GBP','CNY','JPY','RUB','EUR'],
          ['BTC','ETH','BNB','ADA','HEX','XRP'],
          ['BAC','AAPL','AMC','SPY','VERB']]

inline_keys = [[]]

for i in range(len(symbols[0])):
    inline_keys[0].append(symbols[0][i])

print(inline_keys)

a = {'sub':'aa'}
a = a['sub'].split('|')
a.remove('aa')
if a:
    print('|'.join(a))
else:
    print(None)

a = None
if not a:
    print('empty')
else:
    print('full')