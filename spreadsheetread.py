from __future__ import print_function

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os.path
from dotenv import load_dotenv

import globalVar

load_dotenv()

SPREADSHEET_ID = os.getenv('SPREAD_ID')

def get_values(spreadsheet_id, range_name):
    creds = globalVar.creds
    # pylint: disable=maybe-no-member
    try:
        service = build('sheets', 'v4', credentials=creds)

        result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        rows = result.get('values', [])
        # print(f"{len(rows)} rows retrieved")
        globalVar.row_data = rows
        # return result
        return rows
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

def run(sheet_id, sheet_range):
    # Pass: spreadsheet_id, and range_name
    return get_values(SPREADSHEET_ID, f"{sheet_id}!" + sheet_range)