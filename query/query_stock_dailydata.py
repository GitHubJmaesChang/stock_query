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
from rand_proxy import htmlRequest


Savefiledir = './'
url="http://www.tse.com.tw/exchangeReport/MI_INDEX?response=html&date="
stock_type = "&type="

stock_dict = {
	1:'水泥', 2:'食品', 3:'塑膠', 4:'纖維', 5:'電機',
	6:'電器電纜', 7:'化學生技醫療', 8:'玻璃陶瓷', 9:'造紙工業', 10:'鋼鐵工業',
	11:'橡膠', 12:'汽車', 13:'電子工業', 14:'建材', 15:'航運',
	16:'觀光', 17:'金融', 18:'貿易百貨', 20:'其他', 21:'化學工業',
	22:'生技醫療', 23:'油電燃氣', 24:'半導體', 25:'電腦周邊設備', 26:'光電',
	27:'通信網路', 28:'電子零組件', 29:'電子通路', 30:'資訊服務', 31:'其他電子',
}


def stock_query_html_table_by_type(date , mode):
    target_url = url + str(date) + stock_type + str(mode)
    print target_url
    
    try:
        #html_report = requests.get(target_url, headers=headers, timeout=htmltout)
        html_report = htmlRequest(target_url, "get", "")
        DataFrame_form = pd.read_html(html_report.text.encode('utf8'))
    except Exception as e:
    	print(e)
    	raise Exception

    return pd.concat(DataFrame_form)


def daily_query_stock_exchange_information(date, mode):
    try:
        type_1_DataFrame = stock_query_html_table_by_type(date , mode)
    except Exception as e:
    	print(e)
	raise Exception

    return(type_1_DataFrame)

def merge_data(stock_num, stock_name, excahnge_volume, s_price, high_price, low_price, e_price, category, currentCat, pd_data):
    #print pd_data

    # initail columns index
    mutil_coumns = pd.IndexSlice
    
    for idx in range(0, pd_data.shape[0]):
        stock_num.append(pd_data.loc[mutil_coumns[idx], mutil_coumns[:, :, u'證券代號']][0])
        stock_name.append(pd_data.loc[mutil_coumns[idx], mutil_coumns[:, :, u'證券名稱']][0])
        excahnge_volume.append(pd_data.loc[mutil_coumns[idx], mutil_coumns[:, :, u'成交股數']][0])
        s_price.append(pd_data.loc[mutil_coumns[idx], mutil_coumns[:, :, u'開盤價']][0])
        high_price.append(pd_data.loc[mutil_coumns[idx], mutil_coumns[:, :, u'最高價']][0])
        low_price.append(pd_data.loc[mutil_coumns[idx], mutil_coumns[:, :, u'最低價']][0])
        e_price.append(pd_data.loc[mutil_coumns[idx], mutil_coumns[:, :, u'收盤價']][0])
	Category.append(currentCat)


    time.sleep(5)


def daily_information(FilePath, sdate):
    date = sdate.replace("-", "")
    stock_num=[]
    stock_name=[]
    exchange_volume=[]
    start_price=[]
    high_price=[]
    low_price=[]
    end_price=[]
    category=[]

    print("daily_Stock_exchange_info: " + str(sdate))
    for k in stock_dict:
        try:
            merge_data(stock_num, stock_name, exchange_volume, start_price, high_price, low_price, end_price,
               category, str(k).zfill(2), daily_query_stock_exchange_information(date, str(k).zfill(2)))

        except Exception as e:
            print(e)
            print(str(k).zfill(2) + ": (Error) Continue to next category")
            time.sleep(10)
	    # Append empty record
	    stock_num.append(-1)
	    stock_name.append('NA')
	    exchange_volume.append(-1)
	    start_price.append(-1)
	    high_price.append(-1)
	    low_price.append(-1)
	    end_price.append(-1)
	    category.append(str(k).zfill(2))



    row_form1 = pd.DataFrame({ u'ID'     : stock_num})
    row_form2 = pd.DataFrame({ u'Name'   : stock_name})
    row_form3 = pd.DataFrame({ u'Volume' : exchange_volume})
    row_form4 = pd.DataFrame({ u'StrPrice'   : start_price})
    row_form5 = pd.DataFrame({ u'highPrice'   : high_price})
    row_form6 = pd.DataFrame({ u'lowPrice'   : low_price})
    row_form7 = pd.DataFrame({ u'EndPrice'   : end_price})
    row_form8 = pd.DataFrame({ u'Category'   : category})


    form1 = pd.concat([row_form1[u'ID'],
                       row_form2[u'Name'],
                       row_form3[u'Volume'],
                       row_form4[u'StrPrice'],
                       row_form5[u'highPrice'],
                       row_form6[u'lowPrice'],
                       row_form7[u'EndPrice'],
		       row_form8[u'Category']], axis =1)

    #replace the "--" to "0"
    form1[u'Volume'].replace('--', '0', inplace=True)
    form1[u'StrPrice'].replace('--', '0.0', inplace=True)
    form1[u'highPrice'].replace('--', '0.0', inplace=True)
    form1[u'lowPrice'].replace('--', '0.0', inplace=True)
    form1[u'EndPrice'].replace('--', '0.0', inplace=True)
    

    #micolumns  = pd.MultiIndex.from_tuples([(date,'ID'), (date,'Name'),
    #                                         (date,'Volume'),(date,'StrPrice'),
    #                                         (date,'highPrice'),(date,'lowPrice'),
    #                                         (date,'EndPrice')], names = ['date', 'stock info'])  
    #form1.columns = micolumns
    #print form1
    #print pd_form
    form1.to_csv(FilePath + date +"_stockExchange.csv", index = False, encoding = "utf-8")
    return 


if  __name__ == '__main__':
    daily_information(Savefiledir , "2013-02-05")
    print "query stock data done"


