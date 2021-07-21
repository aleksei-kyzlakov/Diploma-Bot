import settings
import requests
 
access_key = settings.FIXERIO_KEY
symbols = {'USD','GBP','CNY','JPY','RUB'}
sym_param = ','.join(symbols)

query = requests.get("http://data.fixer.io/api/latest",
						params={"access_key":access_key, "symbols":sym_param})
rates = query.json()
if rates["success"]:
    data = rates["rates"]
    print(data)
else:
    print("unsuccess")