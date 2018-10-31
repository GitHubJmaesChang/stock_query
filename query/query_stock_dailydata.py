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
from collections import OrderedDict


Savefiledir = 'D:/Stock/finacial/'
url="http://www.tse.com.tw/exchangeReport/MI_INDEX?response=html&date="
stock_type = "&type="

def stock_query_html_table_by_type(date , mode):
    target_url = url + str(date) + stock_type + str(mode)
    print target_url
    html_report = requests.get(target_url)
    DataFrame_form = pd.read_html(html_report.text.encode('utf8'))
    return pd.concat(DataFrame_form)

def daily_query_stock_exchange_information(date, mode):
    #水泥
    type_1_DataFrame = stock_query_html_table_by_type(date , mode)
    print type_1_DataFrame.loc[0][0:]
    return type_1_DataFrame

def merge_data(stock_num, stock_name, excahnge_volume, s_price, high_price, low_price, e_price, pd_data):
    print pd_data
    for idx in range(0, pd_data.shape[0]):
        stock_num.append(pd_data.iloc[idx, 0])
        stock_name.append(pd_data.iloc[idx, 1])
        excahnge_volume.append(pd_data.iloc[idx, 3])
        s_price.append(pd_data.iloc[idx, 5])
        high_price.append(pd_data.iloc[idx, 6])
        low_price.append(pd_data.iloc[idx, 7])
        e_price.append(pd_data.iloc[idx, 8])

    time.sleep(5)


def daily_information(FilePath, date):
    stock_num=[]
    stock_name=[]
    exchange_volume=[]
    start_price=[]
    high_price=[]
    low_price=[]
    end_price=[]
    
    #水泥
    merge_data(stock_num, stock_name, exchange_volume, start_price, high_price, low_price, end_price,
               daily_query_stock_exchange_information(date, "01"))
    #食品
    merge_data(stock_num, stock_name, exchange_volume, start_price, high_price, low_price, end_price,
               daily_query_stock_exchange_information(date, "02"))
    #塑膠
    merge_data(stock_num, stock_name, exchange_volume, start_price, high_price, low_price, end_price,
               daily_query_stock_exchange_information(date, "03"))
    #纖維
    merge_data(stock_num, stock_name, exchange_volume, start_price, high_price, low_price, end_price,
               daily_query_stock_exchange_information(date, "04"))
    #電機
    merge_data(stock_num, stock_name, exchange_volume, start_price, high_price, low_price, end_price,
               daily_query_stock_exchange_information(date, "05"))
    #電器電纜
    merge_data(stock_num, stock_name, exchange_volume, start_price, high_price, low_price, end_price,
               daily_query_stock_exchange_information(date, "06"))
    #化學生技醫療
    merge_data(stock_num, stock_name, exchange_volume, start_price, high_price, low_price, end_price,
               daily_query_stock_exchange_information(date, "07"))
    #化學工業
    merge_data(stock_num, stock_name, exchange_volume, start_price, high_price, low_price, end_price,
               daily_query_stock_exchange_information(date, "21"))
    #生技醫療
    merge_data(stock_num, stock_name, exchange_volume, start_price, high_price, low_price, end_price,
               daily_query_stock_exchange_information(date, "22"))
    #玻璃陶瓷
    merge_data(stock_num, stock_name, exchange_volume, start_price, high_price, low_price, end_price,
               daily_query_stock_exchange_information(date, "08"))
    #造紙工業
    merge_data(stock_num, stock_name, exchange_volume, start_price, high_price, low_price, end_price,
               daily_query_stock_exchange_information(date, "09"))
    #鋼鐵工業
    merge_data(stock_num, stock_name, exchange_volume, start_price, high_price, low_price, end_price,
               daily_query_stock_exchange_information(date, "10"))
    #橡膠
    merge_data(stock_num, stock_name, exchange_volume, start_price, high_price, low_price, end_price,
               daily_query_stock_exchange_information(date, "11"))
    #汽車
    merge_data(stock_num, stock_name, exchange_volume, start_price, high_price, low_price, end_price,
               daily_query_stock_exchange_information(date, "12"))
    #電子工業
    merge_data(stock_num, stock_name, exchange_volume, start_price, high_price, low_price, end_price,
               daily_query_stock_exchange_information(date, "13"))
    #半導體
    merge_data(stock_num, stock_name, exchange_volume, start_price, high_price, low_price, end_price,
               daily_query_stock_exchange_information(date, "24"))
    #電腦周邊設備
    merge_data(stock_num, stock_name, exchange_volume, start_price, high_price, low_price, end_price,
               daily_query_stock_exchange_information(date, "25"))
    #光電
    merge_data(stock_num, stock_name, exchange_volume, start_price, high_price, low_price, end_price,
               daily_query_stock_exchange_information(date, "26"))
    #通信網路
    merge_data(stock_num, stock_name, exchange_volume, start_price, high_price, low_price, end_price,
               daily_query_stock_exchange_information(date, "27"))
    #電子零組件
    merge_data(stock_num, stock_name, exchange_volume, start_price, high_price, low_price, end_price,
               daily_query_stock_exchange_information(date, "28"))
    #電子通路
    merge_data(stock_num, stock_name, exchange_volume, start_price, high_price, low_price, end_price,
               daily_query_stock_exchange_information(date, "29"))
    #資訊服務
    merge_data(stock_num, stock_name, exchange_volume, start_price, high_price, low_price, end_price,
               daily_query_stock_exchange_information(date, "30"))
    #其他電子
    merge_data(stock_num, stock_name, exchange_volume, start_price, high_price, low_price, end_price,
               daily_query_stock_exchange_information(date, "31"))
    #建材
    merge_data(stock_num, stock_name, exchange_volume, start_price, high_price, low_price, end_price,
               daily_query_stock_exchange_information(date, "14"))
    #航運
    merge_data(stock_num, stock_name, exchange_volume, start_price, high_price, low_price, end_price,
               daily_query_stock_exchange_information(date, "15"))
    #觀光
    merge_data(stock_num, stock_name, exchange_volume, start_price, high_price, low_price, end_price,
               daily_query_stock_exchange_information(date, "16"))
    #金融
    merge_data(stock_num, stock_name, exchange_volume, start_price, high_price, low_price, end_price,
               daily_query_stock_exchange_information(date, "17"))
    #貿易百貨
    merge_data(stock_num, stock_name, exchange_volume, start_price, high_price, low_price, end_price,
               daily_query_stock_exchange_information(date, "18"))
    #油電燃氣
    merge_data(stock_num, stock_name, exchange_volume, start_price, high_price, low_price, end_price,
               daily_query_stock_exchange_information(date, "23"))
    #其他
    merge_data(stock_num, stock_name, exchange_volume, start_price, high_price, low_price, end_price,
               daily_query_stock_exchange_information(date, "20"))

    row_form1 = pd.DataFrame({ u' ID'     : stock_num})
    row_form2 = pd.DataFrame({ u' Name'   : stock_name})
    row_form3 = pd.DataFrame({ u' Volume' : exchange_volume})
    row_form4 = pd.DataFrame({ u' StrPrice'   : start_price})
    row_form5 = pd.DataFrame({ u' highPrice'   : high_price})
    row_form6 = pd.DataFrame({ u' lowPrice'   : low_price})
    row_form7 = pd.DataFrame({ u' EndPrice'   : end_price})
    
    form1 = pd.concat([row_form1[u' ID'],
                       row_form2[u' Name'],
                       row_form3[u' Volume'],
                       row_form4[u' StrPrice'],
                       row_form5[u' highPrice'],
                       row_form6[u' lowPrice'],
                       row_form7[u' EndPrice']], axis =1)

    micolumns  = pd.MultiIndex.from_tuples([(date,'ID'), (date,'Name'),(date,'Volume'),(date,'StrPrice'),(date,'highPrice'),(date,'lowPrice'),(date,'EndPrice')], names = ['date', 'stock info'])
    
    form1.columns = micolumns
    print form1
    #print pd_form
    form1.to_csv(FilePath + date +".csv", index = False, encoding = "utf-8")
    return 


if  __name__ == '__main__':
    daily_information(Savefiledir , "20181031")
    print "query 1101 data done"
