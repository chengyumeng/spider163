#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
import datetime


def send_email(host,port, subject, user, content):

    illegal = ["\n", "\r"]
    for ill in illegal:
        subject = subject.replace(ill, ' ')

    headers = {
        'Content-Type': 'text/html; charset=utf-8',
        'Content-Disposition': 'inline',
        'Content-Transfer-Encoding': '8bit',
        'Subject': subject,
        'From': "chengyumeng@github.com",
        'To': user,
        'Date': datetime.datetime.now().strftime('%a, %d %b %Y  %H:%M:%S %Z'),
        'X-Mailer': 'ChengYumeng',
    }

    msg = ''
    for key, value in headers.items():
        msg += "%s: %s\n" % (key, value)

    # add contents
    msg += "\n%s\n" % content

    s = smtplib.SMTP(host, port)

    print ("sending %s to %s" % (subject,headers['To']))
    s.sendmail( headers['From'], headers['To'], msg.encode("utf8"))
    s.quit()