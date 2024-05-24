# -*- coding: utf-8 -*-
"""
Created on Wed May 22 18:18:04 2024

@author: ashwe
"""

from tradebot import *
import config

def get_hist_data(smart_obj, ticker, duration, interval, exchange="NSE"):
    params = {
        "exchange" : exchange,
        "symboltoken" : token_lookup(ticker),
        "interval" : interval,
        "fromdate" : (dt.date.today() - dt.timedelta(duration)).strftime('%Y-%m-%d %H:%M'),
        "todate" : dt.date.today().strftime('%Y-%m-%d %H:%M')
    }
    hist_data = smart_obj.getCandleData(params)
    df_data = pd.DataFrame(hist_data["data"],
                           columns=["date", "open", "high", "low", "close", "volume"])
    df_data.set_index("date", inplace=True)
    df_data.index = pd.to_datetime(df_data.index)
    df_data.index = df_data.index.tz_localize(None)
    return df_data


def get_current_price(smart_obj, ticker, exchange='NSE'):
    global ltp_g
    data = "NO DATA RECEIVED"
    try:
        data = smart_obj.ltpData(exchange=exchange, tradingsymbol=ticker, symboltoken=token_lookup(ticker))
        if(data['status'] and (data['message'] == 'SUCCESS')):
            ltp = float(data['data']['ltp'])
            ltp_g = ltp
        else:
            template = "An ERROR occurred. error message : {0!r}"
            message = template.format(data['message'])
            lg.error(message)
    except Exception as err:
        template = "An exception of type {0} occurred. error message:{1!r}"
        message = template.format(type(err).__name__, err.args)
        lg.error(message)
        lg.error("DATA RECEIVED: {}".format(data))
        ltp = ltp_g
    # For test/debug only
    if config.bot_mode == 2:
        print("Actual LTP: ", ltp)
        ltp = float(input("Enter modified LTP\n"))
    ####################
    return ltp
