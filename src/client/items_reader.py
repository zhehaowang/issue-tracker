#!/usr/bin/env python3

# TODO: fix this path issue
from .gsheet_client import GSheetClient
import datetime

SPREADSHEET_ID     = '1hloMXB_eL1f_OWpZR3qDSwc51AJQjLslr_yNR0u7n8c'
DAILY_SHEET_RANGE  = 'daily!A1:ZZ'
REVIEW_SHEET_RANGE = 'review_backlog!A1:ZZ'
ITEMS_SHEET_RANGE  = 'items_backlog!A1:ZZ'
CONF_SHEET_RANGE   = 'configuration!A1:ZZ'

# Data model dependent reader class
class ItemsReader():
    def __init__(self, client):
        self.client = client
        return

    def read_daily(self):
        rows = self.client.read(SPREADSHEET_ID, DAILY_SHEET_RANGE)
        daily = dict()
        cnt = 0
        for row in rows:
            cnt += 1
            if cnt == 1:
                continue
            if row[0] in daily:
                raise ValueError("duplicated dates")
            daily[row[0]] = {
                'date': datetime.datetime.strptime(row[0], '%m/%d/%y').date(),
                'work': row[1] if len(row) > 1 else '',
                'activities': row[2] if len(row) > 2 else '',
                'item': row[3] if len(row) > 3 else ''
            }
        return daily

    def read_review_backlog(self):
        return

    def read_items_backlog(self):
        return

    def read_conf(self):
        rows = self.client.read(SPREADSHEET_ID, CONF_SHEET_RANGE)
        confs = dict()
        cnt = 0
        for row in rows:
            cnt += 1
            if cnt == 1:
                continue
            if row[0] in confs:
                raise ValueError("duplicated key")
            confs[row[0]] = row[1]
        return confs

if __name__ == "__main__":
    ir = ItemsReader(GSheetClient())
    print(ir.read_daily())
