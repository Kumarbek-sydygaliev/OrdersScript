import requests

# Курс доллара к рублю
api_key = '34l5AQ1nejfv2JAEnNqCQTxIYfoZpZ6I'

x = requests.get(f'https://api.apilayer.com/fixer/latest?apikey={api_key}&base=USD&symbols=RUB')
x = x.json()

def exchange(price_usd: int):
    price_rub = price_usd * x['rates']['RUB']
    return price_rub