# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 18:20:19 2024

@author: ashwe
"""
from tradebot import *
from strategy import *

def main():
    print("running the main ...")
    
    obj = TradeBot()
    strat = Strategy("TEST")
    
    obj.add_strategy(strat)
    obj.run()

if __name__ == '__main__':
    main()
