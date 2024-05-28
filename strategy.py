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
        self.quantity = 4
        self.buy_p = 0.995
        self.sell_p = 1.01
        self.takeProfit = 9999.9999
        self.stoploss = 0.001
        self.isEnter = True
        print("Strategy obj created with name: {} ...".format(self.name))
    
    def set_takeprofit(self, entryPrice):
        self.takeProfit = (self.sell_p * entryPrice)

    def set_stoploss(self, entryPrice):
        self.stoploss = 0.5 * entryPrice

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

        lg.info("self.prev_low: {}, current price: {}".format(self.prev_low, cur_price))
        lg.info('SL %.2f <-- %.2f --> %.2f TP' % (self.stoploss, cur_price, self.takeProfit))
        # if self.prev_low > cur_price:
        if(cur_price <= self.buy_p * self.prev_low) and self.isEnter:
            self.set_takeprofit(cur_price)
            self.set_stoploss(cur_price)
            self.isEnter = False
            return "BUY"
        
        # elif self.prev_high < cur_price:
        elif((cur_price > self.takeProfit) or (cur_price < self.stoploss)):
            self.isEnter = True
            return "SELL"
        
        else:
            return "NA"
