# Back-end script to update stock information in the database
# We will store records in the database in UTC time
# This script runs every 5 minutes

# The script takes 3 command line arguments:
    # user, password, database


#-----------------------------------------------------------------------------------------------------


import pandas as pd
import requests as web
import datetime as dt
import mysql.connector as sql
import re
import math
import sys


#-----------------------------------------------------------------------------------------------------


def is_na(s: str):
    return re.compile('N/A').search(s) != None


def convert_suffixed_number(suffixed_number: str):
    suffix = re.compile('.\Z').search(suffixed_number).group().lower()
    number = float(re.sub('.\Z', '', suffixed_number))
    if suffix == 't':
        converted = number * math.pow(10, 12)
    elif suffix == 'b':
        converted = number * math.pow(10, 9)
    elif suffix == 'm':
        converted = number * math.pow(10, 6)
    else:
        converted = float(number)
    return converted


def current_stock_information(symbol: str):
    stock_info = dict()
    
    html = web.get('https://finance.yahoo.com/quote/' + symbol + '?p=' + symbol).content
    dfs = pd.read_html(html)
    df0 = dfs[0]
    df1 = dfs[1]

    df = pd.read_html(web.get('https://money.cnn.com/quote/quote.html?symb=' + symbol).content)[0]

    price = df[0]
    change = df[1]

    bid = df0[1][2]
    if is_na(bid):
        bid_value = None
        bid_amount = None
    else:
        bid_value = float(re.sub(',', '', re.sub('\s*x\s*\d*\s*\Z', '', bid)))
        bid_amount = int(re.sub('\A\s*(\d*,)*\d*\.\d*\s*x\s*', '', bid))

    ask = df0[1][3]
    if is_na(ask):
        ask_value = None
        ask_amount = None
    else:
        ask_value = float(re.sub(',', '', re.sub('\s*x\s*\d*\s*\Z', '', ask)))
        ask_amount = int(re.sub('\A\s*(\d*,)*\d*\.\d*\s*x\s*', '', ask))
        
    todays_range = df0[1][4]
    if is_na(todays_range):
        low = None
        high = None
    else:
        low = float(re.sub(',', '', re.sub('\s*-\s*(\d*,)*\d*\.\d*\s*\Z', '', todays_range)))
        high = re.sub(',', '', re.sub('\A\s*(\d*,)*\d*\.\d*\s*-\s*', '', todays_range))    

    div_and_yield = df1[1][5]
    if is_na(div_and_yield):
        dividend = None
        stock_yield = None
    else:
        dividend = float(re.sub('\s*\(\d*\.\d*%\)\s*\Z', '', div_and_yield))
        stock_yield = float(re.sub('%\)\s*\Z', '', re.sub('\A\s*\d*\.\d*\s*\(', '', div_and_yield)))
    
    market_cap = df1[1][0]
    if is_na(market_cap):
        market_cap = None
    else:
        market_cap = convert_suffixed_number(market_cap)

    beta = df1[1][1]
    if is_na(beta):
        beta = None
    else:
        float(beta)

    pe_ratio = df1[1][2]
    if is_na(pe_ratio):
        pe_ratio = None
    else:
        float(pe_ratio)

    eps = df1[1][3]
    if is_na(eps):
        eps = None
    else:
        float(eps)

    price = float(re.sub('(\A0\s*)|,', '', re.compile('\A0\s*(\d*,)*\d*\.\d*').search(str(price)).group()))

    change = re.sub('\A0\s*', '', re.compile('\A0\s*(\+|-)(\d*,)*\d*\.\d*\s*/\s*(\+|-)(\d*,)*\d*\.\d*%').search(str(change)).group())
    total_change = float(re.sub('(\s*/\s*(\+|-)(\d*,)*\d*\.\d*%\Z)|,', '', change))
    percent_change = float(re.sub('(\A(\+|-)(\d*,)*\d*\.\d*\s*/\s*)|%|,', '', change))
    
    stock_info['current_price'] = price
    stock_info['price_change'] = total_change
    stock_info['percent_change'] = percent_change
    stock_info['bid_value'] = bid_value
    stock_info['bid_amount'] = bid_amount
    stock_info['ask_value'] = ask_value
    stock_info['ask_amount'] = ask_amount
    stock_info['market_cap'] = market_cap
    stock_info['pe_ratio'] = pe_ratio
    stock_info['eps'] = eps
    stock_info['dividend'] = dividend
    stock_info['yield'] = stock_yield
    stock_info['beta'] = beta
    
    return stock_info


#--------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    args = sys.argv
    user = args[1]
    passwd = args[2]
    database = args[3]
    
    current_time = dt.datetime.now(tz=dt.timezone.utc)
    current_minute = current_time.minute
    minute_delta = current_minute % 5
    current_time_rounded = dt.datetime(
        current_time.year,
        current_time.month,
        current_time.day,
        current_time.hour,
        current_minute - minute_delta,
        0,
        0
    )
    print(current_time_rounded)

    mydb = sql.connect(
        host='localhost',
        user=user,
        passwd=passwd,
        database=database
    )
    cursor = mydb.cursor()
    symbols = list()
    cursor.execute('SELECT stocks.symbol FROM stocks')
    for (symbol) in cursor:
        symbols.append(symbol[0])
    print(symbols)

    stocks_query = 'UPDATE stocks SET current_price = %s, price_change = %s, percent_change = %s, bid_value = %s, bid_amount = %s, ask_value = %s, ask_amount = %s, market_cap = %s, pe_ratio = %s, eps = %s, dividend = %s, yield = %s, beta = %s WHERE symbol = %s'
    stock_tracker_query = 'INSERT INTO stock_tracker (symbol, market_time, price) VALUES (%s, %s, %s)'
    print(stock_tracker_query)
    for symbol in symbols:
        info = current_stock_information(symbol)
        stocks_val = (info['current_price'], info['price_change'], info['percent_change'], info['bid_value'], info['bid_amount'], info['ask_value'], info['ask_amount'], info['market_cap'], info['pe_ratio'], info['eps'], info['dividend'], info['yield'], info['beta'], symbol)
        stock_tracker_val = (symbol, current_time_rounded, info['current_price'])
        print(stock_tracker_val)
        cursor.execute(stocks_query, stocks_val)
        cursor.execute(stock_tracker_query, stock_tracker_val)

    mydb.commit()  
    cursor.close()
    mydb.close()