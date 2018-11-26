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

stock_dict = {
	1:'水泥', 2:'食品', 3:'塑膠', 4:'纖維', 5:'電機',
	6:'電器電纜', 7:'化學生技醫療', 8:'玻璃陶瓷', 9:'造紙工業', 10:'鋼鐵工業',
	11:'橡膠', 12:'汽車', 13:'電子工業', 14:'建材', 15:'航運',
	16:'觀光', 17:'金融', 18:'貿易百貨', 20:'其他', 21:'化學工業',
	22:'生技醫療', 23:'油電燃氣', 24:'半導體', 25:'電腦周邊設備', 26:'光電',
	27:'通信網路', 28:'電子零組件', 29:'電子通路', 30:'資訊服務', 31:'其他電子',
}


def margin_purchase_and_short_sale_query(date , mode):
    tout = 10
    htmltout = 2
    
    headers = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'    }
    
    target_url = url + str(date) + stock_type + str(mode)
    print target_url
    
    while True :
        try:
            htmltout = (htmltout + 3)%30
            html_report = requests.get(target_url, headers=headers, timeout=htmltout)
        except requests.exceptions.Timeout:
            print "invest_table_by_type: (Error) HTML request time out"
            time.sleep(tout)
            tout = tout + 3
            if(tout > 40):
                print("invest_table_by_type: (Error) quit trying time out")
                raise
            continue

        except requests.exceptions.TooManyRedirects:
            print ("invest_table_by_type: (Error) HTML request URL error ")
            time.sleep(tout)
            tout = tout + 3
            if(tout > 50):
                print("invest_table_by_type: (Error) quit trying URL error")
                raise
            continue

        except requests.exceptions.RequestException as e:
            print (e)
            time.sleep(tout)
            tout = tout + 3
            if(tout > 50):
                print("invest_table_by_type: (Error) quit trying exception")
                raise
            continue
        break

    try: 
        DataFrame_form = pd.read_html(html_report.text.encode('utf8'))
    except Exception as e:
    	print(e)
    	raise

    return pd.concat(DataFrame_form)

def margin_transaction(date, mode):
    DataFrame = margin_purchase_and_short_sale_query(date , mode)
    return DataFrame

def daily_margin_transaction(stock_num, stock_name,
                             margin_buy, margin_sell, margin_remain,
                             short_sale_buy, short_sale_sell, short_sale_remain,
                             totalvolune, chargeoff, pd_data):

    mutil_coumns = pd.IndexSlice
    
    #print pd_data.columns
    #print pd_data.loc[mutil_coumns[0], mutil_coumns[:, :, u'股票代號']][0]
    #print pd_data.loc[mutil_coumns[0], mutil_coumns[:, :, u'賣出']][0]
    #print pd_data.loc[mutil_coumns[0], mutil_coumns[:, :, u'賣出']][1]
    #print pd_data.loc[mutil_coumns[0], mutil_coumns[:, :, u'今日餘額']][0]
    #print pd_data.loc[mutil_coumns[0], mutil_coumns[:, :, u'今日餘額']][1]
    #print pd_data.loc[mutil_coumns[0], mutil_coumns[:, :, u'買進']][0]
    #print pd_data.loc[mutil_coumns[0], mutil_coumns[:, :, u'買進']][1]
    #return

    for idx in range(0, pd_data.shape[0]):
        stock_num.append(pd_data.loc[mutil_coumns[idx], mutil_coumns[:, :, u'股票代號']][0])
        stock_name.append(pd_data.loc[mutil_coumns[idx], mutil_coumns[:, :, u'股票名稱']][0])
        margin_buy.append(pd_data.loc[mutil_coumns[idx], mutil_coumns[:, :, u'買進']][0])
        margin_sell.append(pd_data.loc[mutil_coumns[idx], mutil_coumns[:, :, u'賣出']][0])
        margin_remain.append(pd_data.loc[mutil_coumns[idx], mutil_coumns[:, :, u'今日餘額']][0])
        short_sale_buy.append(pd_data.loc[mutil_coumns[idx], mutil_coumns[:, :, u'買進']][1])
        short_sale_sell.append(pd_data.loc[mutil_coumns[idx], mutil_coumns[:, :, u'賣出']][1])
        short_sale_remain.append(pd_data.loc[mutil_coumns[idx], mutil_coumns[:, :, u'今日餘額']][1])
        totalvolune.append(pd_data.loc[mutil_coumns[idx], mutil_coumns[:, :, u'限額']][1])
        chargeoff.append(pd_data.loc[mutil_coumns[idx], mutil_coumns[:, :, u'資券互抵']][0])

    time.sleep(10)


def daily_information(FilePath, sdate):
    date = sdate.replace("-", "")
    
    stock_num=[]
    stock_name=[]
    margin_buy=[]
    margin_sell=[]
    margin_remain=[]
    short_sale_buy=[]
    short_sale_sell=[]
    short_sale_remain=[]
    totalvolume=[]
    chargeoff=[]

    print("daily_Margin_trade_info: " + str(sdate))
    for k in stock_dict:
        try:
            daily_margin_transaction(stock_num, stock_name,
                                     margin_buy, margin_sell, margin_remain,
                                     short_sale_buy, short_sale_sell, short_sale_remain,
                                     totalvolume, chargeoff, margin_transaction(date, str(k).zfill(2)))
        except Exception as e:
            print(e)
            print(str(k).zfill(2) + ": (Error) Continue to next category")
            time.sleep(10)

    
    row_form1  = pd.DataFrame({ u'ID'     : stock_num})
    row_form2  = pd.DataFrame({ u'Name'   : stock_name})
    row_form3  = pd.DataFrame({ u'MarginTradeBuy'    : margin_buy})
    row_form4  = pd.DataFrame({ u'MarginTradeSell'   : margin_sell})
    row_form5  = pd.DataFrame({ u'MarginTradeRemain' : margin_remain})
    row_form6  = pd.DataFrame({ u'ShortSellBuy'      : short_sale_buy})
    row_form7  = pd.DataFrame({ u'ShortSellSell'     : short_sale_sell})
    row_form8  = pd.DataFrame({ u'ShortSellRemain'   : short_sale_remain})
    row_form9  = pd.DataFrame({ u'TotalVolume'       : totalvolume})
    row_form10 = pd.DataFrame({ u'ChargeOff'         : chargeoff})
    
    form1 = pd.concat([row_form1[u'ID'],
                       row_form2[u'Name'],
                       row_form3[u'MarginTradeBuy'],
                       row_form4[u'MarginTradeSell'],
                       row_form5[u'MarginTradeRemain'],
                       row_form6[u'ShortSellBuy'],
                       row_form7[u'ShortSellSell'],
                       row_form8[u'ShortSellRemain'],
                       row_form9[u'TotalVolume'],
                       row_form10[u'ChargeOff'],],
                       axis =1)
    
    #micolumns  = pd.MultiIndex.from_tuples([(date,'ID'), (date,'Name'),
    #                                        (date,'margin_buy'),(date,'margin_sell'),(date,'margin_remain'),
    #                                        (date,'short_sale_buy'),(date,'short_sale_sell'),(date,'short_sale_remain')],
    #                                         names = ['date', 'margin trade and short sale'])
    
    #form1.columns = micolumns
    #print form1
    #print pd_form
    form1.to_csv(FilePath + date +"_MarginTrade.csv", index = False, encoding = "utf-8")
    return


if  __name__ == '__main__':
    daily_information(Savefiledir , "2018-11-05")
    print "query all stock info sdone"
