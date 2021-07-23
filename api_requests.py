from datetime import datetime
import json
import requests
import settings


def crypto(symbols):
    sym_param = ','.join(symbols)
    query = requests.get(
        'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest',
        params={
            'symbol':sym_param,
            'convert':'EUR'},
        headers={
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': settings.CRYPTO_KEY})
    data = query.json() #.loads(response.text)
    result = {}
    for s in symbols:
        price = data['data'][s]['quote']['EUR']['price']
        result[s] = price
    return {'crypto':result}


def stocks(symbols):
    result = {}
    for s in symbols:
        query = requests.get(
            f"https://cloud.iexapis.com/stable/stock/{s}/quote",
		    params={"token":settings.STOCKS_KEY,
            "filter":"symbol,companyName,latestPrice"})
        data = query.json()
        result[s] = data['latestPrice']
    return {'stocks':result}

 
def currency(symbols):
    sym_param = ','.join(symbols)
    query = requests.get(
                "http://data.fixer.io/api/latest",
				params={"access_key":settings.FIXERIO_KEY, 
                "symbols":sym_param})
    data = query.json()
    result = {}
    for s in symbols:
        result[s] = data['rates'][s]
    return {'currency':result}

def request_all():
    result = {}
    result['datetime'] = str(datetime.now())
    result.update(currency(settings.CURRENCY_SYMBOLS))
    result.update(crypto(settings.CRYPTO_SYMBOLS))
    result.update(stocks(settings.STOCKS_SYMBOLS))
    return result
