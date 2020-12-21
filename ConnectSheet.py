import os
import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
import datetime


# -- Google library --

def Create_Service(client_secret_file, api_name, api_version, *scopes):
    print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    # print(pickle_file)

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None


def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt


# -- Google library --


CLIENT_SECRET_FILE = 'secret.json'
API_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
counter = 0


class ConnectSheet:

    def __init__(self):
        pass


    def createCopy():
        source_spreadsheet_id = '1bM8GZfbp3UnvdOAIDhHzAOBK6-HTBIeVMueyy5ZrnxE'
        target_spreadsheet_id = '1vnJX2rVhxHyvWecD7hgi1naDUD4nfbgg3-_B1u39J8A'
        worksheet_id = '541466792'

        service.spreadsheets().sheets().copyTo(
            spreadsheetId=source_spreadsheet_id,
            sheetId=worksheet_id,
            body={'destinationSpreadsheetId': target_spreadsheet_id}
        ).execute()

    def readCol(self):
        """
        This method reads spreadsheet in range from A11 to A62
        it returns list of list. How to access:
        foo = readCol()['values']
        text = foo[var1][var2], var1 - column, var2 - row

        var1: 0 - день недели/группа
              1 - время
              19 - 118 группа
        """

        spreadsheet_id = '1vnJX2rVhxHyvWecD7hgi1naDUD4nfbgg3-_B1u39J8A'

        response = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            majorDimension='COLUMNS',
            range='1 курс (копия)!A11:T100'
        ).execute()

        return response