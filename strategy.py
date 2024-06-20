# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 21:44:59 2024

@author: ashwe
"""

class Strategy:
    def __init__(self, name, interval=1):
        print("Strategy __init__")
        self.name = name
        self.interval = interval
    
    def __del__(self):
        print("Strategy __del__")
    
    def init(self, ticker):
        print("init strategy: {}".format(self.name))
    
    def run(self):
        print("running strategy: {}".format(self.name))
