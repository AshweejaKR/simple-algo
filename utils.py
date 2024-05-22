# -*- coding: utf-8 -*-
"""
Created on Wed May 22 18:16:33 2024

@author: ashwe
"""

import datetime as dt
import time
import pytz
import sys

waitTime = dt.time(8, 59)
startTime = dt.time(18, 00)
endTime = dt.time(23, 55)
sleepTime = 2

def wait_till_market_open():
    global endTime, waitTime, startTime
    while True:
        cur_time = dt.datetime.now(pytz.timezone("Asia/Kolkata")).time()
        if cur_time > endTime or cur_time < waitTime:
            print('Market is closed. \n')
            sys.exit()

        if cur_time > startTime:
            break

        print("Market is NOT opened waiting ... !")
        time.sleep(sleepTime)

    print("Market is Opened ...")


def is_market_open(mode='None'):
    global endTime, waitTime, startTime
    cur_time = dt.datetime.now(pytz.timezone("Asia/Kolkata")).time()
    if startTime <= cur_time <= endTime:
        return True
    else:
        return False