# -*- coding: utf-8 -*-
"""
Created on Wed May 22 18:15:39 2024

@author: ashwe
"""

from logger import *
from tradebot import *

bot_mode = "LIVE"


# Example tasks/functions
def trading_strategy1():
    lg.info("trading_strategy1 is running")
    # running for test ##
    # ticker = "INFY"
    # obj = market_data()
    # data = obj.get_current_price(ticker)
    # print(data)
    # infy_data = obj.get_hist_data("INFY", 5, "ONE_DAY")
    # lg.info(infy_data)
    # end test ###

    x = input("TRADE BUY/SELL\n")

    if x.lower() == "buy":
        return "BUY"
    elif x.lower() == "sell":
        return "SELL"
    else:
        return "NA"


def main():
    # initialize the logger (imported from logger)
    initialize_logger()

    ticker = "SBIN-EQ"
    bot = TradeBot()
    lg.info("TradeBot obj created successfully")

    # bot.add_strat("TEST STRATEGY", 1, trading_strategy1)
    lg.info("Added Trading strategy")

    # bot.run_strat(ticker)
    lg.info("Trading bot done ...")


if __name__ == "__main__":
    main()