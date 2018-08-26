#!/usr/bin/env python3

import smtplib

class Emailer():
    def __init__(self, user, pwd):
        self.server = smtplib.SMTP("smtp.gmail.com", 587)
        self.server.ehlo()
        self.server.starttls()
        self.server.login(user, pwd)

    def send(self, sender, recipient, message):
        try:
            self.server.sendmail(sender, recipient, message)
        except Exception as e:
            print(e + " : failed to send mail")
        return

    def close(self):
        self.server.close()

if __name__ == "__main__":
    with open('email.conf', 'r') as email_conf:
        contents = email_conf.readlines()
        em = Emailer(contents[0], contents[1])
        em.send('Issue Tracker', ['wangzhehao410305@gmail.com'], 'Test Email')
