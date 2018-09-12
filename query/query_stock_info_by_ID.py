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

# example_1_day :http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date=201807031&stockNo=1101
# example_2_year  :http://www.twse.com.tw/exchangeReport/FMSRFK?response=html&date=20180806&stockNo=1101 
url="http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date="
stock ="&stockNo="
headers = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'	
}

last_year_month_days=[]
this_year_month_days=[]

def calender_days(year):
    int_year = int(year)
    print int_year
    last_year_month_days.append(int_year-1)
    this_year_month_days.append(int_year)    
    for month in range(1,12):
        last_year_month_days.append(calendar.monthrange(int_year-1, month)[1])
        this_year_month_days.append(calendar.monthrange(int_year, month)[1])

    print last_year_month_days
    print this_year_month_days

    
def query_stock_value_by_continue_days_and_save_csv(file_path, stock_number):

    #日期 :
    exchange_date =[]
    #成交股數 :
    total_stock_volumn_day =[]
    #成交金額 :
    total_cost_day =[]
    #開盤價   :
    start_price_day =[]
    #最高價   :
    max_price_day =[]
    #最低價   :
    min_price_day =[]
    #收盤價   :
    end_price_day =[]
    #漲跌價差 :
    diff_day =[]
    #成交比數 :
    total_volume_day =[]

    
    now = datetime.datetime.now()
    start_date = now - datetime.timedelta(days = 180)
    if(start_date.year == now.year):
        table = this_year_month_days
    else:
        table = last_year_month_days

    # to prepare the trading data for six months     
    for idx in range(start_date.month, now.month):
        if idx<10:
            idx_mon = '0'
        idx_mon += str(idx)
        query_date = str(this_year_month_days[0])+ idx_mon + str(table[idx])
        print query_date
        query_addr = url + query_date + stock+ stock_number
        print query_addr
        r = requests.get(query_addr,headers=headers)
        time.sleep(5)
        df = pd.read_html(r.text)
        df = pd.concat(df)
        for item in range(0, df.shape[0]):            
            exchange_date.append(df[df.columns[0][0]][df.columns[0][1]][item])
            total_stock_volumn_day.append(df[df.columns[1][0]][df.columns[1][1]][item])
            total_cost_day.append(df[df.columns[2][0]][df.columns[2][1]][item])
            start_price_day.append(df[df.columns[3][0]][df.columns[3][1]][item])
            max_price_day.append(df[df.columns[4][0]][df.columns[4][1]][item])
            min_price_day.append(df[df.columns[5][0]][df.columns[5][1]][item])
            end_price_day.append(df[df.columns[6][0]][df.columns[6][1]][item])
            diff_day.append(df[df.columns[7][0]][df.columns[7][1]][item])
            total_volume_day.append(df[df.columns[8][0]][df.columns[8][1]][item])

    #to capture the trading data for this month 
    current_date = '{:%Y%m%d}'.format(now)        
    query_addr = url + current_date + stock+ stock_number
    time.sleep(5)
    r = requests.get(query_addr, headers=headers)
    df = pd.read_html(r.text)
    df = pd.concat(df)
    for item in range(0, df.shape[0]):
        exchange_date.append(df[df.columns[0][0]][df.columns[0][1]][item])
        total_stock_volumn_day.append(df[df.columns[1][0]][df.columns[1][1]][item])
        total_cost_day.append(df[df.columns[2][0]][df.columns[2][1]][item])
        start_price_day.append(df[df.columns[3][0]][df.columns[3][1]][item])
        max_price_day.append(df[df.columns[4][0]][df.columns[4][1]][item])
        min_price_day.append(df[df.columns[5][0]][df.columns[5][1]][item])
        end_price_day.append(df[df.columns[6][0]][df.columns[6][1]][item])
        diff_day.append(df[df.columns[7][0]][df.columns[7][1]][item])
        total_volume_day.append(df[df.columns[8][0]][df.columns[8][1]][item])


    row_form1 = pd.DataFrame({ u' date '         : exchange_date})
    row_form2 = pd.DataFrame({ u' stock_volumn ' : total_stock_volumn_day})
    row_form3 = pd.DataFrame({ u' total_cost '   : total_cost_day})
    row_form4 = pd.DataFrame({ u' start_price '  : start_price_day})
    row_form5 = pd.DataFrame({ u' max_price '    : max_price_day})
    row_form6 = pd.DataFrame({ u' min_price '    : min_price_day})
    row_form7 = pd.DataFrame({ u' end_price '    : end_price_day})
    row_form8 = pd.DataFrame({ u' diff '         : diff_day})
    row_form9 = pd.DataFrame({ u' trade_volume ' : total_volume_day})
    
    Total_info = pd.concat([row_form1[u' date '],row_form2[u' stock_volumn '],row_form3[u' total_cost '],row_form4[u' start_price '],
                           row_form5[u' max_price '],row_form6[u' min_price '],row_form7[u' end_price '], row_form8[u' diff '],
                           row_form9[u' trade_volume ']], axis=1)

    file_name = file_path+stock_number +'.csv'
    Total_info.to_csv(file_name, encoding = "utf-8")

def stock_query(stock, path):
    if not os.path.isdir(path):
       os.makedirs(path)
    calender_days(datetime.datetime.now().year)
    query_stock_value_by_continue_days_and_save_csv(path, stock)
    
if __name__ == '__main__':
    stock_query('1101', Savefiledir)
