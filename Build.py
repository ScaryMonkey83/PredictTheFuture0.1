from Database.SearchFile import *
from Database.StockData import *
from Database.BuildTable import *
from Database.DatabaseConncetion import *

import os
import glob

import mysql.connector

from pytrends.request import TrendReq as req
import numpy as np

from datetime import datetime
import threading
import multiprocessing as multi


def _per_thread(start_date, dates, tickers, connection):
    data = StockData(connection, dates)
    data.insert_SP(start_date, tickers)

def _per_core(start_date, dates, num_threads, tickers):
    if num_threads == 1:
        pool = PoolConn('NaN', 1)
        pool.get_connection()

        stock = StockData(pool.connections[0], dates)
        stock.insert_SP(start_date, tickers)

        pool.close_connection(pool.connections[0])

# TODO: this else is broken because the stock data is not created in its own thread.
# TODO: figure out how to create subdirectories
    else:
        ticker_split_n2 = np.array_split(tickers, num_threads)
        pool = PoolConn('NaN', num_threads)

        for ii in range(num_threads):
            pool.get_connection()

        threads = []
        for ii in range(num_threads):
            args = (start_date, dates, ticker_split_n2[ii], pool.connections[ii])
            threads.append(threading.Thread(target=_per_thread, args=args))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        for connection in pool.connections:
            pool.close_connection(connection)

def populate_stocks(main_debug, dates, tickers):
    num_processes = 3

    tickers_lists = np.array_split(tickers, num_processes)

    proc = []
    for i in range(num_processes):
        args = (datetime(2014, 1, 1), dates, 2, tickers_lists[i])
        proc.append(multi.Process(target=_per_core, args=args))

    for process in proc:
        process.start()

    for process in proc:
        process.join()

def _login_to_google_(main_debug):
    with open(main_debug, 'a+') as debug:
        debug.write('\nLogging into Google...')
    # Login to google
    login = req()

    # SearchFile object
    search = SearchFile(login, main_debug)
    return search

def Build():

    # files = glob.glob('Debug/*')
    # for f in files:
    #     try:
    #         os.remove(f)
    #     except PermissionError:
    #         g = glob.glob(f)
    #         for ff in g:
    #             os.remove(ff)


    # Creates and 'primes' the debug test file
    main_debug = 'Debug/main.txt'
    f = open(main_debug, "a+")
    f.writelines(['\n\n', str(datetime.now())])
    f.close()

    # logs into google and creates a searchfile object
    search = _login_to_google_(main_debug)
    # logs into database and creates a connection object
    c = PoolConn(main_debug, 1)
    c.get_connection()
    connection = c.connections[0]
    # builds table based on search information
    search_data_populate = BuildTable(connection, main_debug)

    # gets search keywords and stores them in search_keywords
    connection.cursor.execute('SELECT * FROM searches')
    search_keywords = connection.cursor.fetchall()

    # read and refine data to be inserted into database
    search.read_database(search_keywords)
    search.refine_dict()
    # builds date vector
    search.get_dates()

    #
    # DEBUG DEBUG DEBUG
    #
    connection.cursor.execute("TRUNCATE TABLE search_results")
    connection.cursor.execute("TRUNCATE TABLE stock_data")
    connection.database.commit()
    #
    # DEBUG DEBUG DEBUG
    #

    # inserts the dates into search database
    search_data_populate.insert_dates(search.dates)
    connection.database.commit()
    # inserts the search data per date into the database
    search_data_populate.insert_searches(search.trends, search.keywords, search.dates)
    connection.database.commit()

    s = StockData(connection, search.dates)
    s.insert_dates()
    tickers = s.tickers
    del s
    connection.database.commit()


    c.close_connection(connection)
    del c

    time = datetime.now()
    populate_stocks(main_debug, search.dates, tickers)
    print(str(datetime.now() - time))