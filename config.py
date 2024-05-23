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

    if bot_mode == 404 or bot_mode == 3:
        if bot_mode == 3:
            key_file = config_path + "key.txt"
            os.remove(key_file)
        bot_mode = 0
    if bot_mode:
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
        cur_time = dt.datetime.now(pytz.timezone("Asia/Kolkata")).time()
        x = input("delay wait?")
        d_ = 0
        if "y" in x:
            d_ = 1
        waitTime = dt.time(cur_time.hour, (cur_time.minute + d_))
        startTime = dt.time(cur_time.hour, (cur_time.minute + 1))
        endTime = dt.time(cur_time.hour, (cur_time.minute + 4))
        sleepTime = 1
    else:
        print("DEBUG OFF")
