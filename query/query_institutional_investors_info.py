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
from rand_proxy import htmlRequest

Savefiledir = './'
url="http://www.twse.com.tw/fund/T86?response=html&date="
stock_type = "&selectType="
stock_dict = {
	1:'水泥', 2:'食品', 3:'塑膠', 4:'纖維', 5:'電機',
	6:'電器電纜', 7:'化學生技醫療', 8:'玻璃陶瓷', 9:'造紙工業', 10:'鋼鐵工業',
	11:'橡膠', 12:'汽車', 13:'電子工業', 14:'建材', 15:'航運',
	16:'觀光', 17:'金融', 18:'貿易百貨', 20:'其他', 21:'化學工業',
	22:'生技醫療', 23:'油電燃氣', 24:'半導體', 25:'電腦周邊設備', 26:'光電',
	27:'通信網路', 28:'電子零組件', 29:'電子通路', 30:'資訊服務', 31:'其他電子',
}

def invest_table_by_type(date , mode):
    
    target_url = url + str(date) + stock_type + str(mode)
    print(target_url)
    
    try:
    	# htmlRequest parameters: url, restful, payload
        html_report = htmlRequest(target_url, "get", "")
        DataFrame_form = pd.read_html(html_report.text.encode('utf8'))
    except Exception as e:
    	print(e)
    	raise Exception

    return pd.concat(DataFrame_form)

def daily_invest_information(date, mode):
    try:
        type_1_DataFrame = invest_table_by_type(date , mode)
    except Exception as e:
    	raise Exception

    return type_1_DataFrame


def merge_invest_data(stock_num, name,
               Foreign_Investor_buy, Foreign_Investor_sell,
               Investment_Trust_buy,Investment_Trust_sell,
               Dealer_buy, Dealer_sell,
               Total, Category, currentCat,
               pd_data):

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
	Category.append(currentCat)

    time.sleep(11)


def daily_institutional_info(FilePath, sdate):
    date = sdate.replace("-", "")
    global query_year
    query_year = str(sdate.split("-")[0])
    stock_num=[]
    stock_name=[]
    Foreign_Investor_buy=[]
    Foreign_Investor_sell=[]
    Investment_Trust_buy=[]
    Investment_Trust_sell=[]
    Dealer_buy=[]
    Dealer_sell=[]
    Total=[]
    Category=[]


    print("daily_institutional_info: " + str(sdate))

    for k in stock_dict:
        try:
            merge_invest_data(stock_num, stock_name,
                              Foreign_Investor_buy, Foreign_Investor_sell,
                              Investment_Trust_buy,Investment_Trust_sell,
                              Dealer_buy, Dealer_sell,
                              Total,
	   		      Category,
	   		      str(k).zfill(2),
                              daily_invest_information(date, str(k).zfill(2)))
        except Exception as e:
            print(e)
            print("daily_institutional_info [" + str(k).zfill(2) + "]: (Error) Continue to next category")
            time.sleep(10)
	    # Append empty record
            stock_num.append('NA')
            stock_name.append('NA')
            Foreign_Investor_buy.append(-1)
            Foreign_Investor_sell.append(-1)
            Investment_Trust_buy.append(-1)
            Investment_Trust_sell.append(-1)
            Dealer_buy.append(-1)
            Dealer_sell.append(-1)
            Total.append(-1)
            Category.append(str(k).zfill(2))



    row_form1 = pd.DataFrame({ u'ID'     : stock_num})
    row_form2 = pd.DataFrame({ u'Name'   : stock_name})
    row_form3 = pd.DataFrame({ u'Foreign_Investor_buy' : Foreign_Investor_buy})
    row_form4 = pd.DataFrame({ u'Foreign_Investor_sell'   : Foreign_Investor_sell})
    row_form5 = pd.DataFrame({ u'Investment_Trust_buy'   : Investment_Trust_buy})
    row_form6 = pd.DataFrame({ u'Investment_Trust_sell' : Investment_Trust_sell})
    row_form7 = pd.DataFrame({ u'Dealer_buy'   : Dealer_buy})
    row_form8 = pd.DataFrame({ u'Dealer_sell'   : Dealer_sell})
    row_form9 = pd.DataFrame({ u'Total'   : Total})
    row_form10 = pd.DataFrame({ u'Category'   : Category})

    form1 = pd.concat([row_form1[u'ID'],
                       row_form2[u'Name'],
                       row_form3[u'Foreign_Investor_buy'],
                       row_form4[u'Foreign_Investor_sell'],
                       row_form5[u'Investment_Trust_buy'],
                       row_form6[u'Investment_Trust_sell'],
                       row_form7[u'Dealer_buy'],
                       row_form8[u'Dealer_sell'],
                       row_form9[u'Total'],
		       row_form10[u'Category']],
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
    daily_institutional_info(Savefiledir , "2013-01-05")
    print "query all stock info sdone"
