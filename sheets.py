import gspread
from oauth2client.service_account import ServiceAccountCredentials

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