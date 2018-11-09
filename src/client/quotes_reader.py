#!/usr/bin/env python3

import urllib.request
import re

class QuotesReader():
    def __init__(self, url):
        self.url = url
        return

    def read_quotes(self):
        resp = urllib.request.urlopen(self.url)
        content = str(resp.read().strip())
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
    qr = QuotesReader('https://raw.githubusercontent.com/zhehaowang/zhehao.me/master/quotes.md')
    result = qr.readQuotes()
    print(result)