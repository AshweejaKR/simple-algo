# -*- coding: utf-8 -*-
"""
Created on Thu May 23 19:26:16 2024

@author: ashwe
"""

from logger import *

waitTime = dt.time(8, 59)
startTime = dt.time(9, 15)
endTime = dt.time(15, 15)
sleepTime = 5
bot_mode = 0

def initialize_bot():
    global bot_mode, waitTime, startTime, endTime, sleepTime
    config_path = './config/'
    config_file = config_path + "config.txt"
    if bot_mode:
        if bot_mode == 404:
            bot_mode = 0
        try:
            with open(config_file, "w") as f:
                f.write(str(bot_mode))
                f.flush()
                f.close()
        except Exception as err:
            lg.error(err)
    else:
        try:
            with open(config_file) as f:
                bot_mode = int(f.read())
        except Exception as err:
            lg.error(err)
    lg.info('Initialized BOT Successfull ... ')
    if bot_mode == 1:
        print("DEBUG ON")
        waitTime = dt.time(0, 1)
        startTime = dt.time(0, 5)
        endTime = dt.time(23, 55)
        sleepTime = 1
    elif bot_mode == 2:
        print("TEST/DEBUG ON")
        waitTime = dt.time(0, 1)
        startTime = dt.time(0, 5)
        endTime = dt.time(23, 55)
        sleepTime = 1
    else:
        print("DEBUG OFF")