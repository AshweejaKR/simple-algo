# -*- coding: utf-8 -*-
"""
Created on Wed May 22 18:15:39 2024

@author: ashwe
"""

from tradebot import *
from market_data import *
from strategy import Strategy
import config

def main():
    # *************** FOR DEBUG ONLY ***************
    if(len(sys.argv) > 1):
        if("debug".lower() == sys.argv[1].lower()):
            config.bot_mode = 1
        elif("test".lower() == sys.argv[1].lower()):
            config.bot_mode = 2
        elif("edit".lower() == sys.argv[1].lower()):
            config.bot_mode = 3
        else:
            config.bot_mode = 404
    # **********************************************

    # initialize the logger (imported from logger)
    initialize_logger()

    # initialize bot
    initialize_bot()
    lg.info('Trading Bot running ... ! \n')

    bot = TradeBot()
    lg.info("TradeBot obj created successfully")

    st1_obj = Strategy("TEST STRATEGY")
    bot.add_strat_obj(st1_obj)
    lg.info("Added Trading strategy obj")

    ticker = "NIFTYBEES-EQ"
    bot.run_strat(ticker)

    del bot
    lg.info("Trading bot done ...")


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        lg.error("EXCEPTION IN MAIN")
        template = "An exception of type {0} occurred. error message:{1!r}"
        message = template.format(type(err).__name__, err.args)
        lg.error("{}".format(message))
        del bot
        