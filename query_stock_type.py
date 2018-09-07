#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import requests
import pandas as pd
import numpy as np
import csv
import datetime
import time
import pdb
import codecs
import calendar


Savefiledir = 'D://Stock/stock_trade//'
url="http://www.tse.com.tw/exchangeReport/MI_INDEX?response=html&date="
stock_type = "&type="

def stock_query_html_table_by_type(date , mode):
    target_url = url + str(date) + stock_type + str(mode)
    print target_url
    html_report = requests.get(target_url)
    DataFrame_form = pd.read_html(html_report.text)
    return pd.concat(DataFrame_form)

def daily_query_stock_exchange_information(date, mode):
    #水泥
    type_1_DataFrame = stock_query_html_table_by_type(date , mode)
    print type_1_DataFrame
    return
    

if  __name__ == '__main__':
    #水泥
    daily_query_stock_exchange_information("20180906", "01")
    #食品
    daily_query_stock_exchange_information("20180906", "02")
    time.sleep(5)
    #塑膠
    daily_query_stock_exchange_information("20180906", "03")
    time.sleep(5)
    #纖維
    daily_query_stock_exchange_information("20180906", "04")
    time.sleep(5)
    #電機
    daily_query_stock_exchange_information("20180906", "05")
    time.sleep(5)
    #電器電纜
    daily_query_stock_exchange_information("20180906", "06")
    time.sleep(5)
    #化學生技醫療
    daily_query_stock_exchange_information("20180906", "07")
    time.sleep(5)
    #化學工業
    daily_query_stock_exchange_information("20180906", "21")
    time.sleep(5)
    #生技醫療
    daily_query_stock_exchange_information("20180906", "22")
    time.sleep(5)
    #玻璃陶瓷
    daily_query_stock_exchange_information("20180906", "08")
    time.sleep(5)
    #造紙工業
    daily_query_stock_exchange_information("20180906", "09")
    time.sleep(5)
    #鋼鐵工業
    daily_query_stock_exchange_information("20180906", "10")
    time.sleep(5)
    #橡膠
    daily_query_stock_exchange_information("20180906", "11")
    time.sleep(5)
    #汽車
    daily_query_stock_exchange_information("20180906", "12")
    time.sleep(5)
    #電子工業
    daily_query_stock_exchange_information("20180906", "13")
    time.sleep(5)
    #半導體
    daily_query_stock_exchange_information("20180906", "24")
    time.sleep(5)
    #電腦週邊設備
    daily_query_stock_exchange_information("20180906", "25")
    time.sleep(5)
    #光電
    daily_query_stock_exchange_information("20180906", "26")
    time.sleep(5)
    #通信網路
    daily_query_stock_exchange_information("20180906", "27")
    time.sleep(5)
    #電子零組件
    daily_query_stock_exchange_information("20180906", "28")
    time.sleep(5)
    #電子通路
    daily_query_stock_exchange_information("20180906", "29")
    time.sleep(5)
    #資訊服務
    daily_query_stock_exchange_information("20180906", "30")
    time.sleep(5)
    #其他電子
    daily_query_stock_exchange_information("20180906", "31")
    time.sleep(5)
    #建材
    daily_query_stock_exchange_information("20180906", "14")
    time.sleep(5)
    #航運
    daily_query_stock_exchange_information("20180906", "15")
    time.sleep(5)
    #觀光
    daily_query_stock_exchange_information("20180906", "16")
    time.sleep(5)
    #金融
    daily_query_stock_exchange_information("20180906", "17")
    time.sleep(5)
    #貿易百貨
    daily_query_stock_exchange_information("20180906", "18")
    time.sleep(5)
    #油電然氣
    daily_query_stock_exchange_information("20180906", "23")
    time.sleep(5)
    #其他
    daily_query_stock_exchange_information("20180906", "20")    
    print "query 1101 data done"
