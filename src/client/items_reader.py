#!/usr/bin/env python3

# TODO: fix this path issue
from .gsheet_client import GSheetClient
import datetime

SPREADSHEET_ID     = '1hloMXB_eL1f_OWpZR3qDSwc51AJQjLslr_yNR0u7n8c'
DAILY_SHEET_RANGE  = 'daily!A1:ZZ'
REVIEW_SHEET_RANGE = 'review_backlog!A1:ZZ'
ITEMS_SHEET_RANGE  = 'items_backlog!A1:ZZ'
CONF_SHEET_RANGE   = 'configuration!A1:ZZ'
LAWS_SHEET_RANGE   = 'laws!A1:ZZ'

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

    def deserialize_review_events(self, content):
        contents = content.split(';')
        if len(contents) != 3:
            raise ValueError("unexpected row size, " + str(content))
        event = {
            'time': datetime.datetime.strptime(contents[0].strip(), '%m/%d/%y'),
            'status': contents[1].strip().lower(),
            'reschedule_cnt': int(contents[2].strip())
        }
        return event

    def read_review_backlog(self):
        rows = self.client.read(SPREADSHEET_ID, REVIEW_SHEET_RANGE)
        reviews = dict()
        cnt = 0
        for row in rows:
            cnt += 1
            if cnt == 1:
                continue
            if row[0] in reviews:
                raise ValueError("duplicated dates")
            events = []
            for i in range(1, len(row)):
                events.append(self.deserialize_review_events(row[i]))
            reviews[row[0]] = events
        return reviews

    def read_items_backlog(self):
        return

    def read_laws(self):
        rows = self.client.read(SPREADSHEET_ID, LAWS_SHEET_RANGE)
        laws = []
        cnt = 0
        for row in rows:
            cnt += 1
            if cnt == 1:
                continue
            print(row)
            laws.append({
                'law': row[0],
                'description': row[1],
                'start_date': datetime.datetime.strptime(row[2], '%m/%d/%y').date(),
                'end_date': datetime.datetime.strptime(row[3], '%m/%d/%y').date()
            })
        return laws

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

    def write_review_backlog(self, values):
        return self.client.write(SPREADSHEET_ID, REVIEW_SHEET_RANGE, values)

if __name__ == "__main__":
    ir = ItemsReader(GSheetClient())
    print(ir.read_daily())
