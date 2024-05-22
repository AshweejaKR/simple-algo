# -*- coding: utf-8 -*-
"""
Created on Wed May 22 18:16:04 2024

@author: ashwe
"""

from SmartApi import SmartConnect
from pyotp import TOTP
import urllib
import json
import pandas as pd
import datetime as dt

global instrument_list


def token_lookup(ticker, exchange="NSE"):
    global instrument_list
    for instrument in instrument_list:
        if instrument["name"] == ticker and instrument["exch_seg"] == exchange and instrument["symbol"].split('-')[
            -1] == "EQ":
            return instrument["token"]


def symbol_lookup(token, exchange="NSE"):
    global instrument_list
    for instrument in instrument_list:
        if instrument["token"] == token and instrument["exch_seg"] == exchange and instrument["symbol"].split('-')[
            -1] == "EQ":
            return instrument["name"]


def get_keys():
    # just for testing
    key_secret = open("D:\\GitHub\\key.txt", "r").read().split()
    return key_secret


def config():
    global instrument_list
    instrument_url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
    response = urllib.request.urlopen(instrument_url)
    instrument_list = json.loads(response.read())


def sample_strategy():
    pass

class TradeBot:
    def __init__(self):
        self.smartApi = None
        self.client_id = None
        self.interval = 0
        self.function = sample_strategy
        config()
        self.login()

    def __del__(self):
        self.logout()

    def add_strat(self, name, interval, function):
        pass

    def run(self):
        pass

    def login(self):
        keys = get_keys()
        api_key = keys[0]
        self.client_id = keys[2]
        passwd = keys[3]
        totp_str = keys[4]

        self.smartApi = SmartConnect(api_key)
        try:
            totp = TOTP(totp_str).now()
        except Exception as err:
            print("Invalid Token: The provided token is not valid.")
            raise err

        data = self.smartApi.generateSession(self.client_id, passwd, totp)

        try:
            if data['status'] and data['message'] == 'SUCCESS':
                print('Login success ... !')
            else:
                print('Login failed ... !')
        except Exception as err:
            template = "An exception of type {0} occurred. error message:{1!r}"
            message = template.format(type(err).__name__, err.args)
            print("ERROR: {}".format(message))

    def logout(self):
        try:
            data = self.smartApi.terminateSession(self.client_id)
            if data['status'] and data['message'] == 'SUCCESS':
                print('Logout success ... !')
            else:
                print('Logout failed ... !')
        except Exception as err:
            template = "An exception of type {0} occurred. error message:{1!r}"
            message = template.format(type(err).__name__, err.args)
            print("ERROR: {}".format(message))
            print('Logout failed ... !')

    def run_bot(self):
        print("running the bot ...")

    def place_order(self, symbol, price, quantity, order_type):
        # Place order using SmartAPI
        pass

    def get_hist_data(self, ticker, duration, interval, exchange="NSE"):
        params = {
            "exchange" : exchange,
            "symboltoken" : token_lookup(ticker),
            "interval" : interval,
            "fromdate" : (dt.date.today() - dt.timedelta(duration)).strftime('%Y-%m-%d %H:%M'),
            "todate" : dt.date.today().strftime('%Y-%m-%d %H:%M')
        }
        hist_data = self.smartApi.getCandleData(params)
        df_data = pd.DataFrame(hist_data["data"],
                               columns=["date", "open", "high", "low", "close", "volume"])
        df_data.set_index("date", inplace=True)
        df_data.index = pd.to_datetime(df_data.index)
        df_data.index = df_data.index.tz_localize(None)
        return df_data

    def get_current_price(self, ticker, exchange='NSE'):
        data = self.smartApi.ltpData(exchange=exchange, tradingsymbol=ticker, symboltoken=token_lookup(ticker))
        print(data)
