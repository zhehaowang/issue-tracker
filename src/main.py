#!/usr/bin/env python3

from client.quotes_reader import QuotesReader
from client.items_reader  import ItemsReader
from client.gsheet_client import GSheetClient
from notify.emailer       import Emailer
from conf_reader          import ConfReader

import random
import datetime

def select_quote(quote_reader):
    result = quote_reader.read_quotes()
    return random.choice(result)

def send_email(emailer, sender, receiver, msg):
    emailer.send(sender, receiver, msg)
    return

if __name__ == "__main__":
    # What it does:
    # 1. Read through review items, see which ones we need to review today,
    # 2. Suggest some items from backlogged to work on today / tonight,
    # 3. Send myself a random quote from my gh,
    # 4. Append to gsheet log of anything I could be interested in later, e.g. unaccounted for time.
    
    conf_reader = ConfReader('conf.json')
    
    quote_reader = QuotesReader(conf_reader['quote-url'])
    quote = select_quote(quote_reader)
    quote_str = "Quote of the day: " + "\n" + quote['content'] + "\n" + quote["author"]

    # items_reader = ItemsReader(GSheetClient())
    # print(ir.read_daily())

    today_str = datetime.date.today().strftime("%B %d %Y")
    msg = 'Subject: {}\n\n{}'.format('Issues for ' + today_str, quote_str)

    emailer = Emailer(conf_reader['email-user'], conf_reader['email-pwd'])
    send_email(emailer, conf_reader['email-sender'], [conf_reader['email-recipient']], msg)


