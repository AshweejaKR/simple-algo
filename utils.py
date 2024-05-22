# -*- coding: utf-8 -*-
"""
Created on Wed May 22 18:16:33 2024

@author: ashwe
"""

import datetime as dt
import time
import pytz
import sys
import json
import urllib

from logger import *

waitTime = dt.time(8, 59)
startTime = dt.time(18, 00)
endTime = dt.time(23, 55)
sleepTime = 2

def wait_till_market_open():
    global endTime, waitTime, startTime
    while True:
        cur_time = dt.datetime.now(pytz.timezone("Asia/Kolkata")).time()
        if cur_time > endTime or cur_time < waitTime:
            lg.info('Market is closed. \n')
            sys.exit()

        if cur_time > startTime:
            break

        lg.info("Market is NOT opened waiting ... !")
        time.sleep(sleepTime)

    lg.info("Market is Opened ...")


def is_market_open(mode='None'):
    global endTime, waitTime, startTime
    cur_time = dt.datetime.now(pytz.timezone("Asia/Kolkata")).time()
    if startTime <= cur_time <= endTime:
        return True
    else:
        return False


def write_to_json(data, filename):
    try:
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
    except Exception as err:
        template = "An exception of type {0} occurred. error message:{1!r}"
        message = template.format(type(err).__name__, err.args)
        lg.error("ERROR: {}".format(message))


# Function to read data from a JSON file
def read_from_json(filename):
    data = None
    try:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
    except Exception as err:
        template = "An exception of type {0} occurred. error message:{1!r}"
        message = template.format(type(err).__name__, err.args)
        lg.error("ERROR: {}".format(message))
    return data


def get_keys():
    # just for testing
    key_secret = open("D:\\GitHub\\key.txt", "r").read().split()
    return key_secret


def sample_strategy():
    return "NA"
