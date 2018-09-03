#!/usr/bin/env python3

from __future__ import print_function

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

class GSheetClient():
    def __init__(self, token_file_name = 'token.json', cred_file_name = 'credentials.json'):
        self.service = self.create_service(token_file_name, cred_file_name)
        return

    def create_service(self, token_file_name, cred_file_name):
        # If modifying these scopes, delete the file token.json.
        scopes = 'https://www.googleapis.com/auth/spreadsheets'

        store = file.Storage(token_file_name)
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(cred_file_name, scopes)
            creds = tools.run_flow(flow, store)
        return build('sheets', 'v4', http = creds.authorize(Http()))

    def read(self, sheet_id, range_id):
        if not self.service:
            raise RuntimeError('GSheet service not set up, check oauth step')

        result = self.service.spreadsheets().values().get(spreadsheetId = sheet_id,
                                                          range = range_id).execute()
        values = result.get('values', [])
        return values

        # if not values:
        #     print('No data found.')
        # else:
        #     for row in values:
        #         # Print columns A and E, which correspond to indices 0 and 4.
        #         print('%s, %s' % (row[0], row[1]))

    def write(self, sheet_id, range_id, values):
        body = {
            'values': values
        }
        result = self.service.spreadsheets().values().update(
            spreadsheetId = sheet_id,
            range = range_id,
            valueInputOption = "USER_ENTERED",
            body = body).execute()
        return result.get('updatedCells')

if __name__ == "__main__":
    client = GSheetClient()
    values = client.read('1hloMXB_eL1f_OWpZR3qDSwc51AJQjLslr_yNR0u7n8c', 'review_backlog!A1:ZZ')
    values.append(['Test', 'Test'])
    client.write('1hloMXB_eL1f_OWpZR3qDSwc51AJQjLslr_yNR0u7n8c', 'review_backlog!A1:ZZ', values)