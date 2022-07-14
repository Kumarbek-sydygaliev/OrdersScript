import requests, xmltodict, json

# Курс доллара к рублю
x = requests.get('https://www.cbr.ru/scripts/XML_daily_eng.asp')
x = xmltodict.parse(x.text)
x = int(x['ValCurs']['Valute'][10]['Value'][:2])

def exchange(price_usd: int):
    return price_usd * x