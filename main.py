# -*- coding: utf-8 -*-
"""
Created on Wed May 22 18:15:39 2024

@author: ashwe
"""

from logger import *
from tradebot import *

bot_mode = "LIVE"
bot = None
ticker = "MIRZAINT"

mid_price = 0.0

# Example tasks/functions
def trading_strategy1():
    global bot, ticker, mid_price
    sp = mid_price * 1.002
    bp = mid_price * 0.998
    lg.info("trading_strategy1 is running")

    # simple trading strategy to test bot working
    # get current price
    ltp = 0.0
    while ltp <= 1.0:
        ltp = bot.get_current_price(ticker)
    
    lg.info("\n")
    lg.info("---------------------------------------")
    lg.info("Current Price of {} : {}".format(ticker, ltp))
    lg.info("Mid Price of {} : {}".format(ticker, mid_price))
    lg.info("Buy Price of {} : {}".format(ticker, bp))
    lg.info("Sell Price of {} : {}".format(ticker, sp))
    lg.info("---------------------------------------\n")

    # buy when price drop 0.2%
    if ltp < bp:
        return "BUY"
    
    # sell when price goes above 0.2%
    elif ltp > sp:
        return "SELL"
    
    # do nothing if price in between
    else:
        return "NA"


def main():
    global bot, ticker, mid_price
    # initialize the logger (imported from logger)
    initialize_logger()

    bot = TradeBot()
    lg.info("TradeBot obj created successfully")

    # getting price of stock
    mid_price = bot.get_current_price(ticker)
    lg.info("Current Price of {} : {}".format(ticker, mid_price))

    bot.add_strat("TEST STRATEGY", 5, trading_strategy1)
    lg.info("Added Trading strategy")

    bot.run_strat(ticker)
    lg.info("Trading bot done ...")


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        lg.error("Exception IN MAIN")
        template = "An exception of type {0} occurred. error message:{1!r}"
        message = template.format(type(err).__name__, err.args)
        lg.error("ERROR: {}".format(message))
        