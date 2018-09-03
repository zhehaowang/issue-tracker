#!/usr/bin/env python3

from client.quotes_reader import QuotesReader
from client.items_reader  import ItemsReader
from client.gsheet_client import GSheetClient
from notify.emailer       import Emailer
from conf_reader          import ConfReader
from review               import Review

import random
from datetime    import date
from collections import OrderedDict

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
    
    # read content
    conf_reader = ConfReader('conf.json')
    
    quote_reader = QuotesReader(conf_reader['quote-url'])
    quote = select_quote(quote_reader)
    quote_str = "Quote of the day: " + "\n" + quote['content'] + "\n" + quote["author"]

    items_reader = ItemsReader(GSheetClient('client/token.json', 'client/credentials.json'))    
    daily = items_reader.read_daily()
    confs = items_reader.read_conf()

    review_items = items_reader.read_review_backlog()
    review = Review()

    # fill unscheduled reviews, merge, get todo list
    review.fill_review_dates(confs, review_items)
    review.merge_review_items(daily, confs, review_items)
    todo_list = review.reschedule_and_generate_todo(confs, review_items)
    
    # write review schedules back to sheet
    items_reader.write_review_backlog(review.to_table(review_items))

    # send email
    greetings_str = "Hi,\n"
    close_str     = "Thanks,\nBot\n\nP.S. remember to update your progress here:\nhttps://docs.google.com/spreadsheets/d/1hloMXB_eL1f_OWpZR3qDSwc51AJQjLslr_yNR0u7n8c/edit"

    todo_list_str = "\n".join(todo_list)
    todo_list_str = "Consider reviewing the following today:\n" + todo_list_str

    today_str = date.today().strftime("%B %d %Y")
    msg = 'Subject: {}\n\n{}\n{}\n\n{}\n\n{}'.format('Issues for ' + today_str, greetings_str, todo_list_str, quote_str, close_str)

    print(msg)

    emailer = Emailer(conf_reader['email-user'], conf_reader['email-pwd'])
    # send_email(emailer, conf_reader['email-sender'], [conf_reader['email-recipient']], msg)

