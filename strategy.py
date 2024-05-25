# -*- coding: utf-8 -*-
"""
Created on Sat May 25 23:55:36 2024

@author: ashwe
"""

class Strategy:
    def __init__(self, name, interval=1):
        self.name = name
        self.interval = interval
        print("Strategy obj created with name: {} ...".format(self.name))
    
    def init(self):
        print("Initialize strategy for trade for Strat: {} ...".format(self.name))

        self.prev_high = 200.00
        self.prev_low = 100.00

        print("prev high: {}, prev low: {}".format(self.prev_high, self.prev_low))

    def run(self):
        print("running strategy: {} ... ".format(self.name))

        cur_price = float(input("Enter LTP for Test:\n"))

        if self.prev_low > cur_price:
            return "BUY"
        
        elif self.prev_high < cur_price:
            return "SELL"
        
        else:
            return "NA"
