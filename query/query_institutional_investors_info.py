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
import cell_items_name

Savefiledir = 'D:/Stock/finacial/'
url="http://www.twse.com.tw/fund/T86?response=html&date="
stock_type = "&selectType="


def invest_table_by_type(date , mode):

    headers = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'    }
    
    target_url = url + str(date) + stock_type + str(mode)
    print target_url
    
    while True :
        try:
            html_report = requests.get(target_url, headers=headers, timeout=5)
        except requests.exceptions.Timeout:
            print "request time out"
            time.sleep(10)
            continue
        except requests.exceptions.TooManyRedirects:
            print ("request url error ")
            time.sleep(10)
            continue
        except requests.exceptions.RequestException as e:
            print (e)
            time.sleep(10)
            continue
        break

    
    DataFrame_form = pd.read_html(html_report.text.encode('utf8'))
    return pd.concat(DataFrame_form)

def daily_invest_information(date, mode):
    #水泥
    type_1_DataFrame = invest_table_by_type(date , mode)
    return type_1_DataFrame

def merge_invest_data(stock_num, name,
               Foreign_Investor_buy, Foreign_Investor_sell,
               Investment_Trust_buy,Investment_Trust_sell,
               Dealer_buy, Dealer_sell,
               Total,
               pd_data):

    print query_year
    mutil_coumns = pd.IndexSlice
    stock_id = cell_items_name.fundation_table_request[query_year][0]
    stock_name = cell_items_name.fundation_table_request[query_year][1] 
    stock_infom1 = cell_items_name.fundation_table_request[query_year][2] 
    stock_infom2 = cell_items_name.fundation_table_request[query_year][3] 
    stock_infom3 = cell_items_name.fundation_table_request[query_year][4] 
    stock_infom4 = cell_items_name.fundation_table_request[query_year][5] 
    stock_infom5 = cell_items_name.fundation_table_request[query_year][6]
    stock_infom6 = cell_items_name.fundation_table_request[query_year][7] 
    stock_infom7 = cell_items_name.fundation_table_request[query_year][8] 
    
    #print pd_data.loc[mutil_coumns[0], mutil_coumns[:, u'證券名稱']][0]
    
    for idx in range(0, pd_data.shape[0]):
        stock_num.append(pd_data.loc[mutil_coumns[idx], mutil_coumns[:, stock_id ]][0])
        name.append(pd_data.loc[mutil_coumns[idx], mutil_coumns[:, stock_name ] ][0])
        Foreign_Investor_buy.append(pd_data.loc[mutil_coumns[idx], mutil_coumns[:, stock_infom1 ]][0])
        Foreign_Investor_sell.append(pd_data.loc[mutil_coumns[idx], mutil_coumns[:, stock_infom2 ]][0])
        Investment_Trust_buy.append(pd_data.loc[mutil_coumns[idx], mutil_coumns[:, stock_infom3 ]][0])
        Investment_Trust_sell.append(pd_data.loc[mutil_coumns[idx], mutil_coumns[:, stock_infom4 ]][0])
        Dealer_buy.append(pd_data.loc[mutil_coumns[idx], mutil_coumns[:, stock_infom5 ]][0])
        Dealer_sell.append(pd_data.loc[mutil_coumns[idx], mutil_coumns[:, stock_infom6 ]][0])
        Total.append(pd_data.loc[mutil_coumns[idx], mutil_coumns[:, stock_infom7 ]][0])

    time.sleep(11)


def daily_institutional_info(FilePath, sdate):
    date = sdate.replace("-", "")
    global query_year
    query_year = str(sdate.split("-")[0])
    print query_year
    #print cell_items_name.fundation_table_request[query_year][0]
    #return
    stock_num=[]
    stock_name=[]
    Foreign_Investor_buy=[]
    Foreign_Investor_sell=[]
    Investment_Trust_buy=[]
    Investment_Trust_sell=[]
    Dealer_buy=[]
    Dealer_sell=[]
    Total=[]
    
    #水泥
    merge_invest_data(stock_num, stock_name,
               Foreign_Investor_buy, Foreign_Investor_sell,
               Investment_Trust_buy,Investment_Trust_sell,
               Dealer_buy, Dealer_sell,
               Total,
               daily_invest_information(date, "01"))

    #食品
    merge_invest_data(stock_num, stock_name,
               Foreign_Investor_buy, Foreign_Investor_sell,
               Investment_Trust_buy,Investment_Trust_sell,
               Dealer_buy, Dealer_sell,
               Total,
               daily_invest_information(date, "02"))
    #塑膠
    merge_invest_data(stock_num, stock_name,
               Foreign_Investor_buy, Foreign_Investor_sell,
               Investment_Trust_buy,Investment_Trust_sell,
               Dealer_buy, Dealer_sell,
               Total,
               daily_invest_information(date, "03"))
    #纖維
    merge_invest_data(stock_num, stock_name,
               Foreign_Investor_buy, Foreign_Investor_sell,
               Investment_Trust_buy,Investment_Trust_sell,
               Dealer_buy, Dealer_sell,
               Total,
               daily_invest_information(date, "04"))
    #電機
    merge_invest_data(stock_num, stock_name,
               Foreign_Investor_buy, Foreign_Investor_sell,
               Investment_Trust_buy,Investment_Trust_sell,
               Dealer_buy, Dealer_sell,
               Total,
               daily_invest_information(date, "05"))
    #電器電纜
    merge_invest_data(stock_num, stock_name,
               Foreign_Investor_buy, Foreign_Investor_sell,
               Investment_Trust_buy,Investment_Trust_sell,
               Dealer_buy, Dealer_sell,
               Total,
               daily_invest_information(date, "06"))
    #化學生技醫療
    merge_invest_data(stock_num, stock_name,
               Foreign_Investor_buy, Foreign_Investor_sell,
               Investment_Trust_buy,Investment_Trust_sell,
               Dealer_buy, Dealer_sell,
               Total,
               daily_invest_information(date, "07"))
    #化學工業
    merge_invest_data(stock_num, stock_name,
               Foreign_Investor_buy, Foreign_Investor_sell,
               Investment_Trust_buy,Investment_Trust_sell,
               Dealer_buy, Dealer_sell,
               Total,
               daily_invest_information(date, "21"))
    #生技醫療
    merge_invest_data(stock_num, stock_name,
               Foreign_Investor_buy, Foreign_Investor_sell,
               Investment_Trust_buy,Investment_Trust_sell,
               Dealer_buy, Dealer_sell,
               Total,
               daily_invest_information(date, "22"))
    #玻璃陶瓷
    merge_invest_data(stock_num, stock_name,
               Foreign_Investor_buy, Foreign_Investor_sell,
               Investment_Trust_buy,Investment_Trust_sell,
               Dealer_buy, Dealer_sell,
               Total,
               daily_invest_information(date, "08"))
    #造紙工業
    merge_invest_data(stock_num, stock_name,
               Foreign_Investor_buy, Foreign_Investor_sell,
               Investment_Trust_buy,Investment_Trust_sell,
               Dealer_buy, Dealer_sell,
               Total,
               daily_invest_information(date, "09"))
    #鋼鐵工業
    merge_invest_data(stock_num, stock_name,
               Foreign_Investor_buy, Foreign_Investor_sell,
               Investment_Trust_buy,Investment_Trust_sell,
               Dealer_buy, Dealer_sell,
               Total,
               daily_invest_information(date, "10"))
    #橡膠
    merge_invest_data(stock_num, stock_name,
               Foreign_Investor_buy, Foreign_Investor_sell,
               Investment_Trust_buy,Investment_Trust_sell,
               Dealer_buy, Dealer_sell,
               Total,
               daily_invest_information(date, "11"))
    #汽車
    merge_invest_data(stock_num, stock_name,
               Foreign_Investor_buy, Foreign_Investor_sell,
               Investment_Trust_buy,Investment_Trust_sell,
               Dealer_buy, Dealer_sell,
               Total,
               daily_invest_information(date, "12"))
    #電子工業
    merge_invest_data(stock_num, stock_name,
               Foreign_Investor_buy, Foreign_Investor_sell,
               Investment_Trust_buy,Investment_Trust_sell,
               Dealer_buy, Dealer_sell,
               Total,
               daily_invest_information(date, "13"))
    #半導體
    merge_invest_data(stock_num, stock_name,
               Foreign_Investor_buy, Foreign_Investor_sell,
               Investment_Trust_buy,Investment_Trust_sell,
               Dealer_buy, Dealer_sell,
               Total,
               daily_invest_information(date, "24"))
    #電腦周邊設備
    merge_invest_data(stock_num, stock_name,
               Foreign_Investor_buy, Foreign_Investor_sell,
               Investment_Trust_buy,Investment_Trust_sell,
               Dealer_buy, Dealer_sell,
               Total,
               daily_invest_information(date, "25"))
    #光電
    merge_invest_data(stock_num, stock_name,
               Foreign_Investor_buy, Foreign_Investor_sell,
               Investment_Trust_buy,Investment_Trust_sell,
               Dealer_buy, Dealer_sell,
               Total,
               daily_invest_information(date, "26"))
    #通信網路
    merge_invest_data(stock_num, stock_name,
               Foreign_Investor_buy, Foreign_Investor_sell,
               Investment_Trust_buy,Investment_Trust_sell,
               Dealer_buy, Dealer_sell,
               Total,
               daily_invest_information(date, "27"))
    #電子零組件
    merge_invest_data(stock_num, stock_name,
               Foreign_Investor_buy, Foreign_Investor_sell,
               Investment_Trust_buy,Investment_Trust_sell,
               Dealer_buy, Dealer_sell,
               Total,
               daily_invest_information(date, "28"))
    #電子通路
    merge_invest_data(stock_num, stock_name,
               Foreign_Investor_buy, Foreign_Investor_sell,
               Investment_Trust_buy,Investment_Trust_sell,
               Dealer_buy, Dealer_sell,
               Total,
               daily_invest_information(date, "29"))
    #資訊服務
    merge_invest_data(stock_num, stock_name,
               Foreign_Investor_buy, Foreign_Investor_sell,
               Investment_Trust_buy,Investment_Trust_sell,
               Dealer_buy, Dealer_sell,
               Total,
               daily_invest_information(date, "30"))
    #其他電子
    merge_invest_data(stock_num, stock_name,
               Foreign_Investor_buy, Foreign_Investor_sell,
               Investment_Trust_buy,Investment_Trust_sell,
               Dealer_buy, Dealer_sell,
               Total,
               daily_invest_information(date, "31"))
    #建材
    merge_invest_data(stock_num, stock_name,
               Foreign_Investor_buy, Foreign_Investor_sell,
               Investment_Trust_buy,Investment_Trust_sell,
               Dealer_buy, Dealer_sell,
               Total,
               daily_invest_information(date, "14"))
    #航運
    merge_invest_data(stock_num, stock_name,
               Foreign_Investor_buy, Foreign_Investor_sell,
               Investment_Trust_buy,Investment_Trust_sell,
               Dealer_buy, Dealer_sell,
               Total,
               daily_invest_information(date, "15"))
    #觀光
    merge_invest_data(stock_num, stock_name,
               Foreign_Investor_buy, Foreign_Investor_sell,
               Investment_Trust_buy,Investment_Trust_sell,
               Dealer_buy, Dealer_sell,
               Total,
               daily_invest_information(date, "16"))
    #金融
    merge_invest_data(stock_num, stock_name,
               Foreign_Investor_buy, Foreign_Investor_sell,
               Investment_Trust_buy,Investment_Trust_sell,
               Dealer_buy, Dealer_sell,
               Total,
               daily_invest_information(date, "17"))
    #貿易百貨
    merge_invest_data(stock_num, stock_name,
               Foreign_Investor_buy, Foreign_Investor_sell,
               Investment_Trust_buy,Investment_Trust_sell,
               Dealer_buy, Dealer_sell,
               Total,
               daily_invest_information(date, "18"))
    #油電燃氣
    merge_invest_data(stock_num, stock_name,
               Foreign_Investor_buy, Foreign_Investor_sell,
               Investment_Trust_buy,Investment_Trust_sell,
               Dealer_buy, Dealer_sell,
               Total,
               daily_invest_information(date, "23"))
    #其他
    merge_invest_data(stock_num, stock_name,
               Foreign_Investor_buy, Foreign_Investor_sell,
               Investment_Trust_buy,Investment_Trust_sell,
               Dealer_buy, Dealer_sell,
               Total,
               daily_invest_information(date, "20"))
    

    row_form1 = pd.DataFrame({ u'ID'     : stock_num})
    row_form2 = pd.DataFrame({ u'Name'   : stock_name})
    row_form3 = pd.DataFrame({ u'Foreign_Investor_buy' : Foreign_Investor_buy})
    row_form4 = pd.DataFrame({ u'Foreign_Investor_sell'   : Foreign_Investor_sell})
    row_form5 = pd.DataFrame({ u'Investment_Trust_buy'   : Investment_Trust_buy})
    row_form6 = pd.DataFrame({ u'Investment_Trust_sell' : Investment_Trust_sell})
    row_form7 = pd.DataFrame({ u'Dealer_buy'   : Dealer_buy})
    row_form8 = pd.DataFrame({ u'Dealer_sell'   : Dealer_sell})
    row_form9 = pd.DataFrame({ u'Total'   : Total})
    
    form1 = pd.concat([row_form1[u'ID'],
                       row_form2[u'Name'],
                       row_form3[u'Foreign_Investor_buy'],
                       row_form4[u'Foreign_Investor_sell'],
                       row_form5[u'Investment_Trust_buy'],
                       row_form6[u'Investment_Trust_sell'],
                       row_form7[u'Dealer_buy'],
                       row_form8[u'Dealer_sell'],
                       row_form9[u'Total']],
                       axis =1)

    #micolumns  = pd.MultiIndex.from_tuples([(date,'ID'), (date,'Name'),
    #                                        (date,'Foreign_Investor_buy'),(date,'Foreign_Investor_sell'),
    #                                        (date,'Investment_Trust_buy'),(date,'Investment_Trust_sell'),
    #                                        (date,'Dealer_buy'),(date,'Dealer_sell'),(date,'Total')],
    #                                       names = ['date', 'Institutional investors'])
    #form1.columns = micolumns
    #print form1
    #print pd_form
    form1.to_csv(FilePath + date +"_FoundationExchange.csv",  index = False, encoding = "utf-8")
    return 


if  __name__ == '__main__':
    daily_institutional_info(Savefiledir , "2017-11-16")
    print "query all stock info sdone"
