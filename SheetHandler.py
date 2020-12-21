import gspread
from ConnectSheet import ConnectSheet
from oauth2client.service_account import ServiceAccountCredentials


class SheetHandler:
    def __init__(self):
        workingSpreadsheetId = '1vnJX2rVhxHyvWecD7hgi1naDUD4nfbgg3-_B1u39J8A'

        self.gc = gspread.service_account(filename='credentials.json')
        self.sh = self.gc.open_by_key(workingSpreadsheetId)
        self.worksheet = self.sh.get_worksheet(1)

    def deleteWorksheet(self):
        try:
            self.sh.del_worksheet(self.worksheet)
        except:
            return False
        return True

    def copySheet(self):
        ConnectSheet.createCopy()

    def maintain(self):
        pass
        # scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        # credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        # gc = gspread.authorize(credentials)
        #
        # spreadsheet_id = '1sN4war5N8FGEkomKv0Vo-lwLmREsEmXt'
        # sheet = gc.open_by_key(response[spreadsheet_id]).Sheet1
        # sheet_id = 0
        #
        # copy_sheet_to_another_spreadsheet_request_body = {
        #     "destinationSpreadsheetId": "1vnJX2rVhxHyvWecD7hgi1naDUD4nfbgg3-_B1u39J8A"
        # }
        #
        # request = service.spreadsheets().sheets().copyTo(spreadsheetId=spreadsheet_id, sheetId=sheet_id,
        #                                                  body=copy_sheet_to_another_spreadsheet_request_body)
        # response = request.execute()