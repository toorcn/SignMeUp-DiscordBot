from __future__ import print_function

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os.path
from dotenv import load_dotenv

import globalVar

load_dotenv()

SPREADSHEET_ID = os.getenv('SPREAD_ID')

def batch_update_values(spreadsheet_id, range_name, value_input_option, values):
    creds = globalVar.creds
    # pylint: disable=maybe-no-member
    try:
        service = build('sheets', 'v4', credentials=creds)
        data = [
            {
                'range': range_name,
                'values': values
            },
        ]
        body = {
            'valueInputOption': value_input_option,
            'data': data
        }
        result = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
        print(f"{(result.get('totalUpdatedCells'))} cells updated. in {range_name}.")
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

def setRow(sheet_id, entry_value, entry_row):
    batch_update_values(SPREADSHEET_ID, f'{sheet_id}!A{entry_row}:D{entry_row}', "USER_ENTERED", [entry_value])

def run(sheet_id, entry_value):
    # Pass: spreadsheet_id, range_name value_input_option and _values)
    end_var = 1
    if sheet_id == globalVar.DEF_id:
        end_var = globalVar.current_row_num_DEF
        globalVar.current_row_num_DEF += 1
    elif sheet_id == globalVar.IGN_id:
        end_var = globalVar.current_row_num_IGN
        globalVar.current_row_num_IGN += 1
    batch_update_values(SPREADSHEET_ID, f'{sheet_id}!A{end_var}:D{end_var}', "USER_ENTERED", [entry_value])
