#!/usr/bin/env python3

import urllib.request
import re

class QuotesReader():
    def __init__(self):
        return

    def readQuotes(self, url):
        resp = urllib.request.urlopen(url)
        content = str(resp.read())
        result = content.split(r'\n\n')
        quotes = []
        for item in result:
            quote = item.split(r'-- ')
            quotes.append({
                'content': quote[0],
                'author': quote[1]
            })
        return quotes

if __name__ == "__main__":
    qr = QuotesReader()
    result = qr.readQuotes('https://raw.githubusercontent.com/zhehaowang/zhehao.me/master/quotes.md')
    print(result)