import settings
import requests
 
access_key = settings.STOCKS_KEY
symbols = {'BAC','AAPL','AMC','SPY','VERB'}
sym_param = ','.join(symbols)

for s in symbols:
    query = requests.get(f"https://cloud.iexapis.com/stable/stock/{s}/quote",
					 params={"token":access_key, "filter":"symbol,companyName,latestPrice"})
    stocks = query.json()
    print(stocks)

