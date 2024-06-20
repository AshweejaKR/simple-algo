# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 21:44:09 2024

@author: ashwe
"""

class TradeBot:
    def __init__(self):
        print("TradeBot __init__")
        self.strategy = None
        self.interval = 1
    
    def __del__(self):
        print("TradeBot __del__")
        
    def add_strategy(self, strategy):
        self.strategy = strategy
        self.interval = strategy.interval
        print("added strategy: {} with interval: {} ".format(self.strategy.name, self.interval))
    
    def run(self):
        if self.strategy is not None:
            print("running strategy: {}".format(self.strategy.name))
        else:
            print("NOT VALID")
