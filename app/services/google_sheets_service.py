import asyncio
from typing import List, Any
from google.oauth2 import service_account
from googleapiclient.discovery import build

from app.services.config import load_config


config = load_config()

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = config.spreadsheet_id
CREDENTIALS_FILE = config.credentials_file


async def write_to_google_sheets(data: List[List[Any]], sheet_name: str):
    """
    Асинхронно записывает данные в Google Sheets.

    Параметры:
        data (List[List[Any]]): Двумерный список с данными для записи.
        sheet_name (str): Название листа, в который будут записаны данные.

    Возвращает:
        bool: True, если данные успешно записаны, иначе False.

    Исключения:
        Exception: Если произошла ошибка при записи данных.
    """
    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: _write_to_sheets_sync(data, sheet_name))
        return True
    except Exception as e:
        return False


def _write_to_sheets_sync(data: List[List[Any]], sheet_name: str):
    """
    Синхронно записывает данные в Google Sheets.

    Параметры:
        data (List[List[Any]]): Двумерный список с данными для записи.
        sheet_name (str): Название листа, в который будут записаны данные.

    Действия:
        - Авторизуется в Google Sheets API.
        - Проверяет существование листа, создает его при необходимости.
        - Очищает содержимое листа.
        - Записывает новые данные в лист.

    Исключения:
        Exception: Если произошла ошибка при взаимодействии с Google Sheets API.
    """
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES)

    service = build('sheets', 'v4', credentials=creds)
    sheets = service.spreadsheets()

    sheet_metadata = sheets.get(spreadsheetId=SPREADSHEET_ID).execute()
    sheets_list = sheet_metadata.get('sheets', '')
    sheet_exists = False

    for sheet in sheets_list:
        if sheet['properties']['title'] == sheet_name:
            sheet_exists = True
            break

    if not sheet_exists:
        request_body = {
            'requests': [{
                'addSheet': {
                    'properties': {
                        'title': sheet_name
                    }
                }
            }]
        }
        sheets.batchUpdate(spreadsheetId=SPREADSHEET_ID, body=request_body).execute()

    range_name = f'{sheet_name}!A1:ZZ'
    sheets.values().clear(spreadsheetId=SPREADSHEET_ID, range=range_name).execute()

    body = {
        'values': data
    }
    sheets.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f'{sheet_name}!A1',
        valueInputOption='RAW',
        body=body
    ).execute()
