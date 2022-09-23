from __future__ import print_function

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os.path
from dotenv import load_dotenv

import globalVar

load_dotenv()

SPREADSHEET_ID = os.getenv('SPREAD_ID')
# get current highest entry and +1
cell_entry = "A1:C2"
entry_value = [
                ['F', 'B'],
                ['C', 'D']
            ]

def batch_update_values(spreadsheet_id, range_name, value_input_option, values):
    creds = globalVar.creds
    # pylint: disable=maybe-no-member
    try:
        service = build('sheets', 'v4', credentials=creds)

        # values = [
        #     [
        #         # Cell values ...
        #     ],
        #     # Additional rows
        # ]
        data = [
            {
                'range': range_name,
                'values': values
            },
            # Additional ranges to update ...
        ]
        body = {
            'valueInputOption': value_input_option,
            'data': data
        }
        result = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
        print(f"{(result.get('totalUpdatedCells'))} cells updated.")
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

def run():
    # Pass: spreadsheet_id, range_name value_input_option and _values)
    batch_update_values(SPREADSHEET_ID, cell_entry, "USER_ENTERED", entry_value)