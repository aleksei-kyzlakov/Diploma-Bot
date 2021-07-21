from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import settings

symbols = {'BTC','ETH','BNB','ADA','HEX','XRP'}
sym_param = ','.join(symbols)

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
parameters = {
  'symbol':sym_param,
  'convert':'EUR'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': settings.CRYPTO_KEY
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  for s in symbols:
      name = data['data'][s]['name']
      symbol = data['data'][s]['symbol']
      price = data['data'][s]['quote']['EUR']['price']
      print(f"{name} {symbol} {price}")

except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)
  