import requests


r = requests.get("http://data.fixer.io/api/latest",
                access_key = "47fde738bd8af6ed0e4188103f4dbafd",
                base = "RUB",
                symbol = "GBP,JPY,EUR,USD,CAD")
print 