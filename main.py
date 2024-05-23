# -*- coding: utf-8 -*-
"""
Created on Wed May 22 18:15:39 2024

@author: ashwe
"""

from tradebot import *
from market_data import *
import config

bot = None
ticker = "NIFTYBEES-EQ"

mid_price = 0.0

# Example tasks/functions
def trading_strategy1():
    global bot, ticker, mid_price
    sp = mid_price * 1.001
    bp = mid_price * 0.999
    lg.info("trading_strategy1 is running")

    # simple trading strategy to test bot working
    # get current price
    ltp = 0.0
    while ltp <= 1.0:
        ltp = get_current_price(bot.smartApi, ticker)
    
    lg.info("\n")
    lg.info("---------------------------------------")
    lg.info("Current Price of {} : {}".format(ticker, ltp))
    lg.info("BP: {} <---> CP: {} <---> SP: {} \n".format(bp, ltp, sp))

    # buy when price drop 0.2%
    if ltp < bp:
        return "BUY"
    
    # sell when price goes above 0.2%
    elif ltp > sp:
        return "SELL"
    
    # do nothing if price in between
    else:
        return "NA"

    # **** For Test/Debug purpose **** 
    # x = input("ENTER BUY/SELL/NA\n")
    # if x == "BUY":
    #     return "BUY"
    
    # elif x == "SELL":
    #     return "SELL"
    
    # else:
    #     return "NA"
    # ********************************


def main():
    global bot, ticker, mid_price
    if(len(sys.argv) > 1):
        if("debug".lower() == sys.argv[1].lower()):
            config.bot_mode = 1
        elif("test".lower() == sys.argv[1].lower()):
            config.bot_mode = 2
        elif("edit".lower() == sys.argv[1].lower()):
            config.bot_mode = 3
        else:
            config.bot_mode = 404

    # initialize the logger (imported from logger)
    initialize_logger()

    # initialize bot
    initialize_bot()
    lg.info('Trading Bot running ... ! \n')

    bot = TradeBot()
    lg.info("TradeBot obj created successfully")

    # getting price of stock
    mid_price = get_current_price(bot.smartApi, ticker)
    lg.info("Current Price of {} : {}".format(ticker, mid_price))

    bot.add_strat(name="TEST STRATEGY", interval=5, function=trading_strategy1)
    lg.info("Added Trading strategy")

    bot.run_strat(ticker)

    del bot
    lg.info("Trading bot done ...")


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        lg.error("Exception IN MAIN")
        template = "An exception of type {0} occurred. error message:{1!r}"
        message = template.format(type(err).__name__, err.args)
        lg.error("ERROR: {}".format(message))
        del bot
        