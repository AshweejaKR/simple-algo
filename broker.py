# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 18:29:19 2024

@author: ashwe
"""

from SmartApi import SmartConnect
from pyotp import TOTP

from config import *

class AngelOneClient:
    _instance = None

    def __init__(self):
        if not self.__class__._instance:
            self.__class__._instance = SmartConnect(API_KEY)
            totp = TOTP(TOTP_TOKEN).now()
            data = self.__class__._instance.generateSession(CLIENT_ID, PASSWORD, totp)
            self.refreshToken = data['data']['refreshToken']
            self.instrument_list = load_instrument_list()
            if data['status'] and data['message'] == 'SUCCESS':
                print('Login success ... !')
                self.obj = "CREATED OBJ FOR USE"

        else:
            print("NOT")

    def __del__(self):
        if self.__class__._instance:
            data = self.__class__._instance.terminateSession(CLIENT_ID)
            if data['status'] and data['message'] == 'SUCCESS':
                print('Logout success ... !')
            self.__class__._instance = None

    def get_user_data(self):
        res = self.__class__._instance.getProfile(self.refreshToken)
        print(res)
        return res

    def get_margin(self):
        res = self.__class__._instance.rmsLimit()
        print(res)
        margin = res['data']['net']
        return margin
    
    def placeOrder(self, params):
        orderid = self.__class__._instance.placeOrder(params)
        return orderid

    def orderBook(self):
        order_history_response = self.__class__._instance.orderBook()
        return order_history_response
    
    def get_hist(self, ticker, interval, fromdate, todate, exchange="NSE"):
        params = {
            "exchange" : exchange,
            "symboltoken" : token_lookup(ticker, self.instrument_list),
            "interval" : interval,
            "fromdate" : fromdate,
            "todate" : todate
                    }
        hist_data = self.__class__._instance.getCandleData(params)
        return hist_data

    # def get_hist_data(self, ticker, duration, interval="ONE_DAY", exchange="NSE"):
    #     params = {
    #         "exchange" : exchange,
    #         "symboltoken" : token_lookup(ticker, self.instrument_list),
    #         "interval" : interval,
    #         "fromdate" : (dt.date.today() - dt.timedelta(duration)).strftime('%Y-%m-%d %H:%M'),
    #         "todate" : dt.date.today().strftime('%Y-%m-%d %H:%M')
    #             }
    #     hist_data = self.__class__._instance.getCandleData(params)
    #     return hist_data

    # def get_hist_data_intraday(self, ticker, datestamp, interval='FIVE_MINUTE', exchange="NSE"):
    #     params = {
    #         "exchange" : exchange,
    #         "symboltoken" : token_lookup(ticker, self.instrument_list),
    #         "interval" : interval,
    #          "fromdate": datestamp.strftime("%Y-%m-%d")+ " 09:15",
    #          "todate": datestamp.strftime("%Y-%m-%d") + " 15:30" 
    #             }
    #     hist_data = self.__class__._instance.getCandleData(params)
    #     return hist_data

    def get_ltp(self, ticker, exchange):
        data = self.__class__._instance.ltpData(exchange=exchange, tradingsymbol=ticker, symboltoken=token_lookup(ticker, self.instrument_list))
        return data