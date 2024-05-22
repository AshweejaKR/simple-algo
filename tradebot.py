# -*- coding: utf-8 -*-
"""
Created on Wed May 22 18:16:04 2024

@author: ashwe
"""

from SmartApi import SmartConnect
from pyotp import TOTP
import pandas as pd
import time

from logger import *
from utils import *


global instrument_list

def token_lookup(ticker, exchange="NSE"):
    global instrument_list
    for instrument in instrument_list:
        if instrument["name"] == ticker and instrument["exch_seg"] == exchange and instrument["symbol"].split('-')[
            -1] == "EQ":
            return instrument["token"]


def symbol_lookup(token, exchange="NSE"):
    global instrument_list
    for instrument in instrument_list:
        if instrument["token"] == token and instrument["exch_seg"] == exchange and instrument["symbol"].split('-')[
            -1] == "EQ":
            return instrument["name"]


def config():
    global instrument_list
    instrument_url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
    response = urllib.request.urlopen(instrument_url)
    instrument_list = json.loads(response.read())


class TradeBot:
    def __init__(self):
        self.name = "TradeBot"
        self.smartApi = None
        self.client_id = None
        self.interval = 1
        self.function = sample_strategy
        self.stop_event = None
        self.trade = "NA"
        self.isOpen = False
        self.no_of_exec = 0

        config()
        self.login()

    def __del__(self):
        self.logout()

    def add_strat(self, name, interval, function):
        self.name = name
        self.interval = interval
        self.function = function

    def login(self):
        keys = get_keys()
        api_key = keys[0]
        self.client_id = keys[2]
        passwd = keys[3]
        totp_str = keys[4]

        self.smartApi = SmartConnect(api_key)
        try:
            totp = TOTP(totp_str).now()
        except Exception as err:
            lg.error("Invalid Token: The provided token is not valid.")
            template = "An exception of type {0} occurred. error message:{1!r}"
            message = template.format(type(err).__name__, err.args)
            lg.error("ERROR: {}".format(message))
            raise err

        data = self.smartApi.generateSession(self.client_id, passwd, totp)

        try:
            if data['status'] and data['message'] == 'SUCCESS':
                lg.info('Login success ... !')
            else:
                lg.error('Login failed ... !')
        except Exception as err:
            template = "An exception of type {0} occurred. error message:{1!r}"
            message = template.format(type(err).__name__, err.args)
            lg.error("ERROR: {}".format(message))

    def logout(self):
        try:
            data = self.smartApi.terminateSession(self.client_id)
            if data['status'] and data['message'] == 'SUCCESS':
                lg.info('Logout success ... !')
            else:
                lg.error('Logout failed ... !')
        except Exception as err:
            template = "An exception of type {0} occurred. error message:{1!r}"
            message = template.format(type(err).__name__, err.args)
            lg.error("ERROR: {}".format(message))
            lg.error('Logout failed ... !')

    def run_strat(self, ticker):
        try:
            while True:
                lg.info("running {} for {}...".format(self.name, ticker))
                r = self.function()
                print("RETURN : ", r)

                if r == "BUY" and self.trade != 'BUY':
                    if self.isOpen:
                        buy_sell = "BUY"
                        quantity = 1
                        orderid = self.place_order(ticker, quantity, buy_sell)
                        count = 0
                        while self.get_oder_status(orderid) == 'open':
                            lg.info('Buy order is in open, waiting ... %d ' % count)
                            count = count + 1
                            time.sleep(sleepTime)
                        status = self.get_oder_status(orderid)
                        cur_price = 0.0
                        if status == 'completed':
                            lg.info('Submitting {} Order for {}, Qty = {} at price: {}'.format(buy_sell,
                                                                                               ticker,
                                                                                               quantity,
                                                                                               cur_price))
                            self.trade = 'NA'
                            self.isOpen = False
                            lg.info("exiting short Trade ...")
                            self.no_of_exec = self.no_of_exec + 1
                        else:
                            lg.error('Sell order NOT submitted, aborting trade!')
                    else:
                        buy_sell = "BUY"
                        quantity = 1
                        orderid = self.place_order(ticker, quantity, buy_sell)
                        count = 0
                        while self.get_oder_status(orderid) == 'open':
                            lg.info('Buy order is in open, waiting ... %d ' % count)
                            count = count + 1
                            time.sleep(sleepTime)
                        status = self.get_oder_status(orderid)
                        cur_price = 0.0
                        if status == 'completed':
                            lg.info('Submitting {} Order for {}, Qty = {} at price: {}'.format(buy_sell,
                                                                                               ticker,
                                                                                               quantity,
                                                                                               cur_price))
                            self.trade = "BUY"
                            self.isOpen = True
                            lg.info("entering Long Trade ...")
                        else:
                            lg.error('Sell order NOT submitted, aborting trade!')

                elif r == "SELL" and self.trade != 'SELL':
                    if self.isOpen:
                        buy_sell = "SELL"
                        quantity = 1
                        orderid = self.place_order(ticker, quantity, buy_sell)
                        count = 0
                        while self.get_oder_status(orderid) == 'open':
                            lg.info('Buy order is in open, waiting ... %d ' % count)
                            count = count + 1
                            time.sleep(sleepTime)
                        status = self.get_oder_status(orderid)
                        cur_price = 0.0
                        if status == 'completed':
                            lg.info('Submitting {} Order for {}, Qty = {} at price: {}'.format(buy_sell,
                                                                                               ticker,
                                                                                               quantity,
                                                                                               cur_price))
                            self.trade = 'NA'
                            self.isOpen = False
                            lg.info("exiting Long Trade ...")
                            self.no_of_exec = self.no_of_exec + 1
                        else:
                            lg.error('Sell order NOT submitted, aborting trade!')
                    else:
                        buy_sell = "SELL"
                        quantity = 1
                        orderid = self.place_order(ticker, quantity, buy_sell)
                        count = 0
                        while self.get_oder_status(orderid) == 'open':
                            lg.info('Buy order is in open, waiting ... %d ' % count)
                            count = count + 1
                            time.sleep(sleepTime)
                        status = self.get_oder_status(orderid)
                        cur_price = 0.0
                        if status == 'completed':
                            lg.info('Submitting {} Order for {}, Qty = {} at price: {}'.format(buy_sell,
                                                                                               ticker,
                                                                                               quantity,
                                                                                               cur_price))
                            self.trade = "SELL"
                            self.isOpen = True
                            lg.info("entering short Trade ...")
                        else:
                            lg.error('Sell order NOT submitted, aborting trade!')

                time.sleep(self.interval)
        except KeyboardInterrupt:
            lg.info("bot stop request by user")
        except Exception as err:
            template = "An exception of type {0} occurred. error message:{1!r}"
            message = template.format(type(err).__name__, err.args)
            lg.error("ERROR: {}".format(message))

    def place_order(self, ticker, quantity, buy_sell, exchange = 'NSE'):
        lg.info('Submitting %s Order for %s, Qty = %d ' % (buy_sell, ticker, quantity))
        orderid = None

        try:
            params = {
                "variety" : "NORMAL",
                "tradingsymbol" : "{}".format(ticker),
                "symboltoken" : token_lookup(ticker),
                "transactiontype" : buy_sell,
                "exchange" : exchange,
                "ordertype" : "MARKET",
                "producttype" : "DELIVERY",
                "duration" : "DAY",
                "quantity" : quantity
            }

            lg.debug('params: %s ' % params)
            orderid = self.smartApi.placeOrder(params)
            lg.debug('orderID: %s ' % orderid)
        except Exception as err:
            template = "An exception of type {0} occurred. error message:{1!r}"
            message = template.format(type(err).__name__, err.args)
            lg.error(message)
            send_to_telegram(message)
            lg.error('%s order NOT submitted!' % buy_sell)
            send_to_telegram('{} order NOT submitted!'.format(buy_sell))
            self.logout()
            sys.exit()
        return orderid

    def get_oder_status(self, orderid):
        status = 'NA'
        time.sleep(sleepTime)
        order_history_response = self.smartApi.orderBook()
        try:
            for i in order_history_response['data']:
                if i['orderid'] == orderid:
                    lg.debug(str(i))
                    status = i['status']  # completed/rejected/open/cancelled
                    break
        except Exception as err:
            template = "An exception of type {0} occurred. error message:{1!r}"
            message = template.format(type(err).__name__, err.args)
            lg.error(message)
            send_to_telegram(message)
        # for testing only
        lg.info("current status: {} for orderid: {} ".format(status, orderid))
        # status = input("updated oder status?? (completed/rejected/open/cancelled) \n")
        return status

    def get_hist_data(self, ticker, duration, interval, exchange="NSE"):
        params = {
            "exchange" : exchange,
            "symboltoken" : token_lookup(ticker),
            "interval" : interval,
            "fromdate" : (dt.date.today() - dt.timedelta(duration)).strftime('%Y-%m-%d %H:%M'),
            "todate" : dt.date.today().strftime('%Y-%m-%d %H:%M')
        }
        hist_data = self.smartApi.getCandleData(params)
        df_data = pd.DataFrame(hist_data["data"],
                               columns=["date", "open", "high", "low", "close", "volume"])
        df_data.set_index("date", inplace=True)
        df_data.index = pd.to_datetime(df_data.index)
        df_data.index = df_data.index.tz_localize(None)
        return df_data

    def get_current_price(self, ticker, exchange='NSE'):
        data = self.smartApi.ltpData(exchange=exchange, tradingsymbol=ticker, symboltoken=token_lookup(ticker))
        print(data)
