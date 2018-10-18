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
url="http://www.twse.com.tw/exchangeReport/MI_MARGN?response=html&date="
stock_type = "&selectType="
headers = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'	
}


def margin_purchase_and_short_sale_query(date , mode):
    target_url = url + str(date) + stock_type + str(mode)
    print target_url
    html_report = requests.get(target_url, headers=headers)
    DataFrame_form = pd.read_html(html_report.text.encode('utf8'))
    return pd.concat(DataFrame_form)

def margin_transaction(date, mode):
    #水泥
    type_1_DataFrame = margin_purchase_and_short_sale_query(date , mode)
    return type_1_DataFrame

def daily_margin_transaction(stock_num, stock_name,
                             margin_buy, margin_sell, margin_remain,
                             short_sale_buy, short_sale_sell, short_sale_remain,
                             pd_data):
    print pd_data
    for idx in range(0, pd_data.shape[0]):
        stock_num.append(pd_data.iloc[idx, 0])
        stock_name.append(pd_data.iloc[idx, 1])
        margin_buy.append(pd_data.iloc[idx, 2])
        margin_sell.append(pd_data.iloc[idx, 3])
        margin_remain.append(pd_data.iloc[idx, 6])
        short_sale_buy.append(pd_data.iloc[idx, 8])
        short_sale_sell.append(pd_data.iloc[idx, 9])
        short_sale_remain.append(pd_data.iloc[idx, 12])

    time.sleep(10)


def daily_information(FilePath, date):
    stock_num=[]
    stock_name=[]
    margin_buy=[]
    margin_sell=[]
    margin_remain=[]
    short_sale_buy=[]
    short_sale_sell=[]
    short_sale_remain=[]
    
    #水泥
    daily_margin_transaction(stock_num, stock_name,
                             margin_buy, margin_sell, margin_remain,
                             short_sale_buy, short_sale_sell, short_sale_remain,
                             margin_transaction(date, "01"))
    #食品
    daily_margin_transaction(stock_num, stock_name,
                             margin_buy, margin_sell, margin_remain,
                             short_sale_buy, short_sale_sell, short_sale_remain,
                             margin_transaction(date, "02"))
    #塑膠
    daily_margin_transaction(stock_num, stock_name,
                             margin_buy, margin_sell, margin_remain,
                             short_sale_buy, short_sale_sell, short_sale_remain,
                             margin_transaction(date, "03"))
    #纖維
    daily_margin_transaction(stock_num, stock_name,
                             margin_buy, margin_sell, margin_remain,
                             short_sale_buy, short_sale_sell, short_sale_remain,
                             margin_transaction(date, "04"))
    #電機
    daily_margin_transaction(stock_num, stock_name,
                             margin_buy, margin_sell, margin_remain,
                             short_sale_buy, short_sale_sell, short_sale_remain,
                             margin_transaction(date, "05"))
    #電器電纜
    daily_margin_transaction(stock_num, stock_name,
                             margin_buy, margin_sell, margin_remain,
                             short_sale_buy, short_sale_sell, short_sale_remain,
                             margin_transaction(date, "06"))
    #化學生技醫療
    daily_margin_transaction(stock_num, stock_name,
                             margin_buy, margin_sell, margin_remain,
                             short_sale_buy, short_sale_sell, short_sale_remain,
                             margin_transaction(date, "07"))
    #化學工業
    daily_margin_transaction(stock_num, stock_name,
                             margin_buy, margin_sell, margin_remain,
                             short_sale_buy, short_sale_sell, short_sale_remain,
                             margin_transaction(date, "21"))
    #生技醫療
    daily_margin_transaction(stock_num, stock_name,
                             margin_buy, margin_sell, margin_remain,
                             short_sale_buy, short_sale_sell, short_sale_remain,
                             margin_transaction(date, "22"))
    #玻璃陶瓷
    daily_margin_transaction(stock_num, stock_name,
                             margin_buy, margin_sell, margin_remain,
                             short_sale_buy, short_sale_sell, short_sale_remain,
                             margin_transaction(date, "08"))
    #造紙工業
    daily_margin_transaction(stock_num, stock_name,
                             margin_buy, margin_sell, margin_remain,
                             short_sale_buy, short_sale_sell, short_sale_remain,
                             margin_transaction(date, "09"))
    #鋼鐵工業
    daily_margin_transaction(stock_num, stock_name,
                             margin_buy, margin_sell, margin_remain,
                             short_sale_buy, short_sale_sell, short_sale_remain,
                             margin_transaction(date, "10"))
    #橡膠
    daily_margin_transaction(stock_num, stock_name,
                             margin_buy, margin_sell, margin_remain,
                             short_sale_buy, short_sale_sell, short_sale_remain,
                             margin_transaction(date, "11"))
    #汽車
    daily_margin_transaction(stock_num, stock_name,
                             margin_buy, margin_sell, margin_remain,
                             short_sale_buy, short_sale_sell, short_sale_remain,
                             margin_transaction(date, "12"))
    #電子工業
    daily_margin_transaction(stock_num, stock_name,
                             margin_buy, margin_sell, margin_remain,
                             short_sale_buy, short_sale_sell, short_sale_remain,
                             margin_transaction(date, "13"))
    #半導體
    daily_margin_transaction(stock_num, stock_name,
                             margin_buy, margin_sell, margin_remain,
                             short_sale_buy, short_sale_sell, short_sale_remain,
                             margin_transaction(date, "24"))
    #電腦周邊設備
    daily_margin_transaction(stock_num, stock_name,
                             margin_buy, margin_sell, margin_remain,
                             short_sale_buy, short_sale_sell, short_sale_remain,
                             margin_transaction(date, "25"))
    #光電
    daily_margin_transaction(stock_num, stock_name,
                             margin_buy, margin_sell, margin_remain,
                             short_sale_buy, short_sale_sell, short_sale_remain,
                             margin_transaction(date, "26"))
    #通信網路
    daily_margin_transaction(stock_num, stock_name,
                             margin_buy, margin_sell, margin_remain,
                             short_sale_buy, short_sale_sell, short_sale_remain,
                             margin_transaction(date, "27"))
    #電子零組件
    daily_margin_transaction(stock_num, stock_name,
                             margin_buy, margin_sell, margin_remain,
                             short_sale_buy, short_sale_sell, short_sale_remain,
                             margin_transaction(date, "28"))
    #電子通路
    daily_margin_transaction(stock_num, stock_name,
                             margin_buy, margin_sell, margin_remain,
                             short_sale_buy, short_sale_sell, short_sale_remain,
                             margin_transaction(date, "29"))
    #資訊服務
    daily_margin_transaction(stock_num, stock_name,
                             margin_buy, margin_sell, margin_remain,
                             short_sale_buy, short_sale_sell, short_sale_remain,
                             margin_transaction(date, "30"))
    #其他電子
    daily_margin_transaction(stock_num, stock_name,
                             margin_buy, margin_sell, margin_remain,
                             short_sale_buy, short_sale_sell, short_sale_remain,
                             margin_transaction(date, "31"))
    #建材
    daily_margin_transaction(stock_num, stock_name,
                             margin_buy, margin_sell, margin_remain,
                             short_sale_buy, short_sale_sell, short_sale_remain,
                             margin_transaction(date, "14"))
    #航運
    daily_margin_transaction(stock_num, stock_name,
                             margin_buy, margin_sell, margin_remain,
                             short_sale_buy, short_sale_sell, short_sale_remain,
                             margin_transaction(date, "15"))
    #觀光
    daily_margin_transaction(stock_num, stock_name,
                             margin_buy, margin_sell, margin_remain,
                             short_sale_buy, short_sale_sell, short_sale_remain,
                             margin_transaction(date, "16"))
    #金融
    daily_margin_transaction(stock_num, stock_name,
                             margin_buy, margin_sell, margin_remain,
                             short_sale_buy, short_sale_sell, short_sale_remain,
                             margin_transaction(date, "17"))
    #貿易百貨
    daily_margin_transaction(stock_num, stock_name,
                             margin_buy, margin_sell, margin_remain,
                             short_sale_buy, short_sale_sell, short_sale_remain,
                             margin_transaction(date, "18"))
    #油電燃氣
    daily_margin_transaction(stock_num, stock_name,
                             margin_buy, margin_sell, margin_remain,
                             short_sale_buy, short_sale_sell, short_sale_remain,
                             margin_transaction(date, "23"))
    #其他
    daily_margin_transaction(stock_num, stock_name,
                             margin_buy, margin_sell, margin_remain,
                             short_sale_buy, short_sale_sell, short_sale_remain,
                             margin_transaction(date, "20"))
    
    row_form1 = pd.DataFrame({ u' ID '     : stock_num})
    row_form2 = pd.DataFrame({ u' Name '   : stock_name})
    row_form3 = pd.DataFrame({ u' margin_buy '    : margin_buy})
    row_form4 = pd.DataFrame({ u' margin_sell '   : margin_sell})
    row_form5 = pd.DataFrame({ u' margin_remain ' : margin_remain})
    row_form6 = pd.DataFrame({ u' short_sale_buy '      : short_sale_buy})
    row_form7 = pd.DataFrame({ u' short_sale_sell '     : short_sale_sell})
    row_form8 = pd.DataFrame({ u' short_sale_remain '   : short_sale_remain})
    
    form1 = pd.concat([row_form1[u' ID '],
                       row_form2[u' Name '],
                       row_form3[u' margin_buy '],
                       row_form4[u' margin_sell '],
                       row_form5[u' margin_remain '],
                       row_form6[u' short_sale_buy '],
                       row_form7[u' short_sale_sell '],
                       row_form8[u' short_sale_remain ']],
                       axis =1)

    micolumns  = pd.MultiIndex.from_tuples([(date,'ID'), (date,'Name'),
                                            (date,'margin_buy'),(date,'margin_sell'),(date,'margin_remain'),
                                            (date,'short_sale_buy'),(date,'short_sale_sell'),(date,'short_sale_remain')],
                                             names = ['date', 'margin trade and short sale'])
    
    form1.columns = micolumns
    print form1
    #print pd_form
    form1.to_csv(FilePath + date +"margin_trade.csv", index = False, encoding = "utf-8")
    return 


if  __name__ == '__main__':
    daily_information(Savefiledir , "20180911")
    print "query all stock info sdone"
