# -*- coding: utf-8 -*-
"""
Created on Sat May 25 23:55:36 2024

@author: ashwe
"""
from market_data import *

class Strategy:
    def __init__(self, name, obj, interval=1):
        self.name = name
        self.botobj = obj
        self.interval = interval
        print("Strategy obj created with name: {} ...".format(self.name))
    
    def init(self, ticker):
        self.ticker = ticker
        print("Initialize strategy for trade for Strat: {} ...".format(self.name))

        stock_data = get_hist_data(self.botobj.smartApi, self.ticker, 4, "ONE_DAY")
        print(stock_data)
        self.prev_high = max(stock_data.iloc[-1]['high'], stock_data.iloc[-2]['high'])
        self.prev_low = min(stock_data.iloc[-1]['low'], stock_data.iloc[-2]['low'])

        # simple trading strategy to test bot working
        # get current price
        ltp = 0.0
        while ltp <= 1.0:
            ltp = get_current_price(self.botobj.smartApi, self.ticker)
        print("prev high: {}, prev low: {}, LTP: {}".format(self.prev_high, self.prev_low, ltp))

    def run(self):
        print("running strategy: {} ... ".format(self.name))

        cur_price = get_current_price(self.botobj.smartApi, self.ticker)

        if self.prev_low > cur_price:
            return "BUY"
        
        elif self.prev_high < cur_price:
            return "SELL"
        
        else:
            return "NA"
