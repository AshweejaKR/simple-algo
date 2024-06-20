# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 21:42:59 2024

@author: ashwe
"""
import time

from broker import *
from utils import *

class Orders:
    def __init__(self):
        self.obj = AngelOneClient()

    def __del__(self):
        print("Orders __del__")

    def __place_order(self, ticker, quantity, buy_sell, exchange = 'NSE'):
        orderid = None

        try:
            params = {
                "variety" : "NORMAL",
                "tradingsymbol" : "{}".format(ticker),
                "symboltoken" : token_lookup(ticker, self.obj.instrument_list),
                "transactiontype" : buy_sell,
                "exchange" : exchange,
                "ordertype" : "MARKET",
                "producttype" : "DELIVERY",
                "duration" : "DAY",
                "quantity" : quantity
            }

            orderid = self.obj.placeOrder(params)
            print(orderid)
        except Exception as err:
            print(err)

        return orderid

    def __wait_till_order_fill(self, orderid):
        count = 0
        while self.get_oder_status(orderid) == 'open':
            print('Buy order is in open, waiting ... %d ' % count)
            count = count + 1
            time.sleep(1)

    def place_buy_order(self, ticker, quantity, exchange = 'NSE'):
        buy_sell = "BUY"
        orderid = self.__place_order(ticker, quantity, buy_sell)
        self.__wait_till_order_fill(orderid)
        return orderid

    def place_sell_order(self, ticker, quantity, exchange = 'NSE'):
        buy_sell = "SELL"
        orderid = self.__place_order(ticker, quantity, buy_sell)
        self.__wait_till_order_fill(orderid)
        return orderid

    def get_oder_status(self, orderid):
        order_history_response = self.obj.orderBook()
        status = "NA"

        try:
            for i in order_history_response['data']:
                if i['orderid'] == orderid:
                    status = i['status']  # complete/rejected/open/cancelled
                    break
        except Exception as err:
            print(err)

        return status
