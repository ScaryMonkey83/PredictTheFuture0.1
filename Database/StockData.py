import pandas_datareader as web
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

import numpy as np
import os

import multiprocessing
import threading
import warnings

# allows a default value to be assigned to the insert_SP function
__ticker_length__ = 0


def _build_list_(soup):
    table = soup.find('table', {'class': 'wikitable sortable'})
    links = table.find_all('a', {'class' : 'external text'})

    new = []

    for link in links:
        if link.text != 'reports':
            str_ = str(link.text)
            str_ = str_.replace(".", "-")

            new = np.append(new, str_)
    return new, new.size

def _find_opt_value_(date, list):
    try_back = 1
    try_forward = 0
    count = 0
    final_date_forward = None
    final_date_back = None
    while final_date_back is None:
        try:
            final_date_back = list[date - timedelta(days=try_back)]
            final_date_forward = list[date + timedelta(days=try_forward)]
        except:
            if count % 2 == 0:
                try_forward += 1
            else:
                try_back += 1
            count += 1

        if (count > 1000):
            raise Exception("RUNAWAY LOOP ERROR")

    return (final_date_forward + final_date_back) / 2


class StockData(object):

    def __init__(self, dbConn, dates=None):
        s = "Debug/{}/{}".format(str(multiprocessing.current_process()), str(threading.current_thread())) + "_.txt"
        s = s.replace(' ', '_').replace('<', '_').replace('>', '_').replace('(', '_').replace(')', '_').replace(',', '_')
        try:
            self.debug = open(s, 'a+')
        except:
            dir = 'Debug/{}'.format(str(multiprocessing.current_process()))
            dir = dir.replace(' ', '_').replace('<', '_').replace('>', '_').replace('(', '_').replace(')', '_').replace(',', '_')
            os.mkdir(dir)
            self.debug = open(s, 'a+')

        self.debug.writelines(['\n', str(datetime.now())])
        self.debug.write('  Retrieving wiki data...')

        # Gets wikipedia URL for S&P 500 list
        wikiURL = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies').text
        soup = BeautifulSoup(wikiURL, 'lxml')
        # List of tickers for S&P 500
        self.tickers, self.__ticker_length__ = _build_list_(soup)
        self.sql_cursor = dbConn.cursor
        self.database = dbConn.database
        self.dates = dates

        self.__moves__ = 0

    def insert_dates(self):
        self.debug.write('\n  Inserting dates...')
        for date in self.dates:
            self.sql_cursor.callproc('insert_date_sp', [date])

    def insert_SP(self, start_date, tickers, scrape_loc='yahoo'):
        self.debug.write('\n  Inserting SP stock data into database...')
        for ticker in tickers:
            self.debug.write('\n  ' + ticker)

            try:
                self.sql_cursor.callproc('add_stock_column', [str(ticker)])
            except:
                pass
                self.debug.write('\n  ' + str(ticker) + ' already has a column in stock_data')

            d = None
            delta = 1
            try:
                d = web.DataReader(ticker, scrape_loc, start_date)
            except:
                while d is None:
                    try:
                        d = web.DataReader(ticker, scrape_loc, start_date + timedelta(days=delta * 7))
                    except:
                        delta += 1
                        if delta > 52 * 5:
                            warnings.warn("RUNAWAY LOOP")

            for date in reversed(self.dates):
                try:
                    args = [str(ticker), float(round(d['Close'][date], 2)), date]

                except:
                    self.__moves__ += 1
                    try:
                        if date.weekday() > 4:

                            try:
                                args = [str(ticker), float(round(d['Close'][date - timedelta(days=2)], 2)), date]
                            except:
                                self.__moves__ += 2
                                value = _find_opt_value_(date, d['Close'])
                                args = [str(ticker), float(round(value)), date]

                        else:
                            self.__moves__ += 2
                            value = _find_opt_value_(date, d['Close'])
                            args = [str(ticker), float(round(value)), date]

                    except:
                        self.debug.write("""THERE IS SOMETHING SERIOUSLY WRONG WITH THE DATE AND
                                        YAHOO IS BEING A TOTAL WHORE AND YOU REALLY NEED TO
                                         PAY SOMEONE WHO KNOWS WHAT THEY ARE DOING TO GIVE YOU
                                         STABLE NUMBERS""")
                        continue


                try : self.sql_cursor.callproc('add_data_point_stock', args)
                except :
                    if (date > datetime.today() - timedelta(weeks=8)):
                        continue
                    else:
                        break


            self.debug.write('\n         ' + str(ticker) + ' success')
            self.database.commit()
        self.debug.close()