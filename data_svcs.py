# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 21:43:22 2024

@author: ashwe
"""

from broker import *
from utils import *

class Market_data:
    def __init__(self):
        self.obj = AngelOneClient()

    def __del__(self):
        print("Market_data __del__")
        
    def get_current_price(self, ticker, exchange='NSE'):
        data = self.obj.get_ltp(ticker, exchange)
        ltp = float(data['data']['ltp'])
        return ltp
    
    def hist_data_daily(self, tickers, duration, exchange="NSE"):
        data = self.obj.get_hist_data(ticker, duration, exchange)
