# -*- coding: utf-8 -*-
"""
Created on Wed May 22 18:16:04 2024

@author: ashwe
"""

from SmartApi import SmartConnect
from pyotp import TOTP
import pandas as pd
import time
import urllib

from logger import *
from utils import *
import config


global instrument_list
ltp_g = 0

def token_lookup(ticker, exchange="NSE"):
    global instrument_list
    for instrument in instrument_list:
        if instrument["symbol"] == ticker and instrument["exch_seg"] == exchange and instrument["symbol"].split('-')[
            -1] == "EQ":
            lg.debug('token: {} for {}'.format(instrument["token"], ticker))
            return instrument["token"]


def symbol_lookup(token, exchange="NSE"):
    global instrument_list
    for instrument in instrument_list:
        if instrument["token"] == token and instrument["exch_seg"] == exchange and instrument["symbol"].split('-')[
            -1] == "EQ":
            return instrument["symbol"]


def config_bot():
    global instrument_list
    filename = "instrument_list_file.json"
    instrument_list = read_from_json(filename)

    if instrument_list is None:
        instrument_url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
        response = urllib.request.urlopen(instrument_url)
        instrument_list = json.loads(response.read())

        write_to_json(instrument_list, filename)


class TradeBot:
    def __init__(self):
        self.name = "TradeBot"
        self.smartApi = None
        self.client_id = None
        self.interval = 1
        self._args = None
        self.stop_event = None
        self.trade = "NA"
        self.isOpen = False
        self.no_of_exec = 0
        self.long_only = True

        config_bot()
        self.login()

    def __del__(self):
        self.logout()

    def add_strat_obj(self, str_obj):
        self.str_obj = str_obj
        self.interval = str_obj.interval
        self.name = str_obj.name
        lg.info("added strat: {} with interval: {} ".format(self.name, self.interval))

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
        data = None
        try:
            data = self.smartApi.terminateSession(self.client_id)
            if data['status'] and data['message'] == 'SUCCESS':
                lg.info('Logout success ... !')
            else:
                lg.error('Logout failed ... !')
        except Exception as err:
            template = "An exception of type {0} occurred. error message:{1!r}"
            message = template.format(type(err).__name__, err.args)
            lg.error("{}".format(message))
            lg.error('Logout failed ... !')

    def run_strat(self, ticker):
        wait_till_market_open()
        self.str_obj.init(ticker)
        data = load_positions(ticker)
        lg.info(data)
        if data is not None:
            try:
                if ticker == data['ticker']:
                    self.str_obj.quantity = data['quantity']
                    self.trade = data['order_type']
                    self.str_obj.entryprice = data['entryprice']
                    self.isOpen = True
                    self.str_obj.isEntered = True
            except Exception as err:
                template = "An exception of type {0} occurred. error message:{1!r}"
                message = template.format(type(err).__name__, err.args)
                lg.error("ERROR: {}".format(message))

        try:
            while is_market_open():
                lg.info("running {} for {} ...".format(self.name, ticker))
                tr = self.str_obj.run()
                # print("RETURN : ", tr)
                # lg.info("SL: {} <---> CP: {} <---> TP: {} \n".format(bp, ltp, sp))

                # To make trade only long
                if self.long_only:
                    if self.trade == "NA" and tr == "SELL":
                        tr = "NA"

                if tr == "BUY" and self.trade != 'BUY':
                    if self.isOpen:
                        buy_sell = "BUY"
                        quantity = self.str_obj.quantity
                        orderid = self.place_order(ticker, quantity, buy_sell)
                        count = 0
                        while self.get_oder_status(orderid) == 'open':
                            lg.info('Buy order is in open, waiting ... %d ' % count)
                            count = count + 1
                            time.sleep(sleepTime)
                        status = self.get_oder_status(orderid)
                        lg.info("current status: {} for orderid: {} for order {}".format(status, orderid, buy_sell))
                        cur_price = 0.0
                        if status == 'complete':
                            lg.info('Submitting {} Order for {}, Qty = {} at price: {}'.format(buy_sell,
                                                                                               ticker,
                                                                                               quantity,
                                                                                               cur_price))
                            self.trade = 'NA'
                            self.isOpen = False
                            lg.info("exiting short Trade ...")
                            remove_positions(ticker)
                            self.no_of_exec = self.no_of_exec + 1
                        else:
                            lg.error('Buy order NOT submitted, aborting trade!')
                    else:
                        buy_sell = "BUY"
                        quantity = self.str_obj.quantity
                        orderid = self.place_order(ticker, quantity, buy_sell)
                        count = 0
                        while self.get_oder_status(orderid) == 'open':
                            lg.info('Buy order is in open, waiting ... %d ' % count)
                            count = count + 1
                            time.sleep(sleepTime)
                        status = self.get_oder_status(orderid)
                        lg.info("current status: {} for orderid: {} for order {}".format(status, orderid, buy_sell))
                        cur_price = self.str_obj.cur_price
                        self.str_obj.entryprice = cur_price
                        if status == 'complete':
                            lg.info('Submitting {} Order for {}, Qty = {} at price: {}'.format(buy_sell,
                                                                                               ticker,
                                                                                               quantity,
                                                                                               self.str_obj.entryprice))
                            self.trade = "BUY"
                            self.isOpen = True
                            save_positions(ticker, quantity, buy_sell, self.str_obj.entryprice)
                            lg.info("entering Long Trade ...")
                        else:
                            lg.error('Buy order NOT submitted, aborting trade!')

                elif tr == "SELL" and self.trade != 'SELL':
                    if self.isOpen:
                        buy_sell = "SELL"
                        quantity = self.str_obj.quantity
                        orderid = self.place_order(ticker, quantity, buy_sell)
                        count = 0
                        while self.get_oder_status(orderid) == 'open':
                            lg.info('Buy order is in open, waiting ... %d ' % count)
                            count = count + 1
                            time.sleep(sleepTime)
                        status = self.get_oder_status(orderid)
                        lg.info("current status: {} for orderid: {} for order {}".format(status, orderid, buy_sell))
                        cur_price = 0.0
                        if status == 'complete':
                            lg.info('Submitting {} Order for {}, Qty = {} at price: {}'.format(buy_sell,
                                                                                               ticker,
                                                                                               quantity,
                                                                                               cur_price))
                            self.trade = 'NA'
                            self.isOpen = False
                            lg.info("exiting Long Trade ...")
                            remove_positions(ticker)
                            self.no_of_exec = self.no_of_exec + 1
                        else:
                            lg.error('Sell order NOT submitted, aborting trade!')
                    else:
                        buy_sell = "SELL"
                        quantity = self.str_obj.quantity
                        orderid = self.place_order(ticker, quantity, buy_sell)
                        count = 0
                        while self.get_oder_status(orderid) == 'open':
                            lg.info('Buy order is in open, waiting ... %d ' % count)
                            count = count + 1
                            time.sleep(sleepTime)
                        status = self.get_oder_status(orderid)
                        lg.info("current status: {} for orderid: {} for order {}".format(status, orderid, buy_sell))
                        cur_price = 0.0
                        self.str_obj.entryprice = cur_price
                        if status == 'complete':
                            lg.info('Submitting {} Order for {}, Qty = {} at price: {}'.format(buy_sell,
                                                                                               ticker,
                                                                                               quantity,
                                                                                               self.str_obj.entryprice))
                            self.trade = "SELL"
                            self.isOpen = True
                            save_positions(ticker, quantity, buy_sell, self.str_obj.entryprice)
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

            lg.debug("params: {} for order: {}".format(params, buy_sell))
            if config.bot_mode == 2:
                orderid = "DUMMY ORDER ID FOR TEST"
            else:
                orderid = self.smartApi.placeOrder(params)
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
        if config.bot_mode == 2:
            order_history_response = {'status': True, 'message': 'SUCCESS', 'errorcode': '', 'data': []}
        else:
            order_history_response = self.smartApi.orderBook()
            lg.info(order_history_response)
        try:
            for i in order_history_response['data']:
                if i['orderid'] == orderid:
                    lg.debug(str(i))
                    status = i['status']  # complete/rejected/open/cancelled
                    break
        except Exception as err:
            template = "An exception of type {0} occurred. error message:{1!r}"
            message = template.format(type(err).__name__, err.args)
            lg.error(message)
            send_to_telegram(message)
        # For test/debug only
        if config.bot_mode == 2:
            lg.info("Actual status: ".format(status))
            status = "complete"#input("updated oder status?? (complete/rejected/open/cancelled) \n")
        ####################
        return status
