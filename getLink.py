import requests
import gspread
import urllib.parse
import pickle
import pprint


def getLink(cellNumber):
    try:
        spreadsheetId = "1vnJX2rVhxHyvWecD7hgi1naDUD4nfbgg3-_B1u39J8A"  # Please set the Spreadsheet ID.
        cellRange = "1 курс (копия)!T11:T62"

        with open('token_sheets_v4.pickle', 'rb') as token:
            credentials = pickle.load(token)

        client = gspread.authorize(credentials)  # I think that this is also used in your script for using gsperad.

        # 1. Retrieve the access token.
        access_token = client.auth.token

        # 2. Request to the method of spreadsheets.get in Sheets API using `requests` module.
        fields = "sheets(data(rowData(values(hyperlink))))"  # formattedValue or hyperlink
        url = "https://sheets.googleapis.com/v4/spreadsheets/" + spreadsheetId + "?ranges=" + urllib.parse.quote(
            cellRange) + "&fields=" + urllib.parse.quote(fields)
        res = requests.get(url, headers={"Authorization": "Bearer " + access_token})

        # 3. Retrieve the hyperlink.
        obj = res.json()
        link = obj["sheets"][0]['data'][0]['rowData'][cellNumber]['values'][0]['hyperlink']
        # link = obj["sheets"][0]['data'][0]['rowData']
        return ' ' + link
    except Exception as e:
        return e

def getValue(cellNumber): # alternative method to read spreadsheet
    spreadsheetId = "1vnJX2rVhxHyvWecD7hgi1naDUD4nfbgg3-_B1u39J8A"  # Please set the Spreadsheet ID.
    cellRange = "1 курс (копия)!T11:T100"

    with open('token_sheets_v4.pickle', 'rb') as token:
        credentials = pickle.load(token)

    client = gspread.authorize(credentials)  # I think that this is also used in your script for using gsperad.

    # 1. Retrieve the access token.
    access_token = client.auth.token

    # 2. Request to the method of spreadsheets.get in Sheets API using `requests` module.
    fields = "sheets(data(rowData(values(formattedValue))))"  # formattedValue or hyperlink
    url = "https://sheets.googleapis.com/v4/spreadsheets/" + spreadsheetId + "?ranges=" + urllib.parse.quote(
        cellRange) + "&fields=" + urllib.parse.quote(fields)
    res = requests.get(url, headers={"Authorization": "Bearer " + access_token})

    # 3. Retrieve the hyperlink.
    obj = res.json()
    # print(obj)
    # link = obj["sheets"][0]['data'][0]['rowData'][0]['values'][0]['hyperlink']
    # link = obj["sheets"][0]['data'][0]['rowData'][cellNumber]['values'][0]['hyperlink']
    value = obj["sheets"][0]['data'][0]['rowData']
    return value

# debug
# print(getLink(69))
# print(getValue(1448))