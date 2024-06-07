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
        self.entryprice = 0.0
        self.takeProfit = 0.2
        self.stoploss = 0.1
        self.isEntered = False
        lg.info("Strategy obj created with name: {} ...".format(self.name))
    
    def set_takeprofit(self, takeProfit):
        self.takeProfit = takeProfit / 100.00

    def set_stoploss(self, stoploss):
        self.stoploss = stoploss / 100.00

    def init(self, ticker):
        self.ticker = ticker
        lg.info("Initialize strategy for trade for Strat: {} ...".format(self.name))

        stock_data = get_hist_data(self.botobj.smartApi, self.ticker, 4, "ONE_DAY")
        lg.info(stock_data)
        self.prev_high = max(stock_data.iloc[-1]['high'], stock_data.iloc[-2]['high'])
        self.prev_low = min(stock_data.iloc[-1]['low'], stock_data.iloc[-2]['low'])
        self.prev_high = 100.00
        # simple trading strategy to test bot working
        # get current price
        ltp = 0.0
        while ltp <= 1.0:
            ltp = get_current_price(self.botobj.smartApi, self.ticker)
        lg.info("prev high: {}, prev low: {}, LTP: {}".format(self.prev_high, self.prev_low, ltp))

    def run(self):
        self.cur_price = get_current_price(self.botobj.smartApi, self.ticker)

        stoploss = self.entryprice - (self.entryprice * self.stoploss)
        takeprofit = self.entryprice + (self.entryprice * self.takeProfit)
            
        lg.info("self.prev_high: {}, current price: {}".format(self.prev_high, self.cur_price))
        lg.info('SL %.2f <-- %.2f --> %.2f TP' % (stoploss, self.cur_price, takeprofit))
        # if self.prev_low > cur_price:
        if((self.cur_price < self.buy_p * self.prev_high) and (not self.isEntered)):
            self.entryprice = self.cur_price
            self.isEntered = True
            return "BUY"
        
        # elif self.prev_high < cur_price:
        elif(((self.cur_price > takeprofit) or (self.cur_price < stoploss)) and (self.isEntered)):
            self.isEntered = False
            return "SELL"
        
        else:
            return "NA"
