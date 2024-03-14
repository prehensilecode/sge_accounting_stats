#!/usr/bin/env python3
import sys
import os
import datetime
import time

starttime = 1609412491
foo = datetime.datetime.fromtimestamp(starttime)
print(foo)

starttime = 1710291103
foo = datetime.datetime.fromtimestamp(starttime)
print(foo)

timestamp = time.mktime(time.strptime('2023-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'))
print(timestamp)

timestamp = time.mktime(time.strptime('2024-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'))
print(timestamp)
