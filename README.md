# Issue Tracker

### What it does

* Read through daily log of items and backlog review items to generate a review items sheet
* Write review items sheet to Google spreadsheet, pick todo items for today from review items
* Pick a quote from my bank of quotes, concatenate with todo items for today and send a daily reminder email

### Why issue tracker

* Accomodate personalized and evolving data model and prioritization
* Integrate with configuration-driven Ebbinghaus memory curve

### How to use

* Install dependencies
```
pip3 install --upgrade --user google-api-python-client oauth2client
```
* Create src/conf.json looking like this
```
{
    "quote-url": "https://xxx",
    "email-user": "xxx@xxx.com",
    "email-pwd": "xxx",
    "email-recipient": "yyy@yyy.com",
    "email-sender": "zzz"
}
```
* [Set up Google oauth2 client secret](https://developers.google.com/api-client-library/python/guide/aaa_oauth) (expects src/client/credentials.json to bootstrap, and keeps src/client/token.json for authentication)
* Example crontab -e setup
```
0 20 * * * /home/zhehao/issue-tracker/src/main.py
```

### Dependencies

* Google spreadsheet Python API
* oauth2client
* smtplib
