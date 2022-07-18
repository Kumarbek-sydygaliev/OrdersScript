import gspread
from oauth2client.service_account import ServiceAccountCredentials

import requests, xmltodict


# Доступ к таблице через Google API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive.file',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)


def get_sheet():
    client = gspread.authorize(credentials)
    sheet = client.open("Копия test").sheet1
    data = sheet.get_all_records()
    return data

def exchange(price_usd: int):
    x = requests.get('https://www.cbr.ru/scripts/XML_daily_eng.asp')
    x = xmltodict.parse(x.text)
    x = int(x['ValCurs']['Valute'][10]['Value'][:2])
    return price_usd * x