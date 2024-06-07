# -*- coding: utf-8 -*-
"""
Created on Wed May 22 18:16:33 2024

@author: ashwe
"""

import time
import pytz
import json
import os.path

import datetime as dt
from config import *
import config

def wait_till_market_open():
    while True:
        cur_time = dt.datetime.now(pytz.timezone("Asia/Kolkata")).time()
        if cur_time > config.endTime or cur_time < config.waitTime:
            lg.info('Market is closed. \n')
            return

        if cur_time > config.startTime:
            break

        lg.info("Market is NOT opened waiting ... !")
        time.sleep(config.sleepTime)

    lg.info("Market is Opened ...")


def is_market_open(mode='None'):
    cur_time = dt.datetime.now(pytz.timezone("Asia/Kolkata")).time()
    if config.startTime <= cur_time <= config.endTime:
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
    config_path = './config/'
    key_file = config_path + "key.txt"
    try:
        key_secret = open(key_file, "r").read().split()
    except FileNotFoundError:
        key_secret = []
        api_key = input("Enter API Key\n")
        api_secret = input("Enter API Secret\n")
        client_id = input("Enter Client ID/Username\n")
        passwd = input("Enter password/PIN\n")
        totp_str = input("Enter TOTP string\n")
        key_secret.append(api_key)
        key_secret.append(api_secret)
        key_secret.append(client_id)
        key_secret.append(passwd)
        key_secret.append(totp_str)

        try:
            with open(key_file, "w") as f:
                for key in key_secret:
                    f.write(f'{key}\n')
        except Exception as err:
            template = "An exception of type {0} occurred. error message:{1!r}"
            message = template.format(type(err).__name__, err.args)
            lg.error("ERROR: {}".format(message))
    return key_secret

def save_positions(ticker, quantity, order_type, entryprice):
    pos_path = './data/'
    try:
        os.mkdir(pos_path)
    except Exception as err:
        template = "An exception of type {0} occurred. error message:{1!r}"
        message = template.format(type(err).__name__, err.args)
        lg.error("ERROR: {}".format(message))
    pos_file_name = ticker + "_trade_data.json"
    currentpos_path = pos_path + pos_file_name

    data = {
        "ticker" : ticker,
        "quantity" : quantity,
        "order_type" : order_type,
        "entryprice" : entryprice,
    }

    write_to_json(data, currentpos_path)

def load_positions(ticker):
    pos_path = './data/'
    pos_file_name = ticker + "_trade_data.json"
    currentpos_path = pos_path + pos_file_name
    data = None
    
    if os.path.exists(currentpos_path):
        data = read_from_json(currentpos_path)

    return data

def remove_positions(ticker):
    pos_path = './data/'
    pos_file_name = ticker + "_trade_data.json"
    currentpos_path = pos_path + pos_file_name
    os.remove(currentpos_path)
