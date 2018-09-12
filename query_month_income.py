#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import requests
from io import StringIO
import time

Savefiledir = 'D:/Stock/finacial/'


def monthly_report(path, year, month):
    
    # 假如是西元，轉成民國
    if year > 1990:
        year -= 1911
    
    url = 'http://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(year)+'_'+str(month)+'_0.html'
    
    if year <= 98:
        url = 'http://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(year)+'_'+str(month)+'.html'
    
    # 偽瀏覽器
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    
    # 下載該年月的網站，並用pandas轉換成 dataframe
    r = requests.get(url, headers=headers)
    r.encoding = 'big5'
    html_df = pd.read_html(StringIO(r.text))
    
    # 處理一下資料
    if html_df[0].shape[0] > 500:
        df = html_df[0].copy()
    else:
        df = pd.concat([df for df in html_df if df.shape[1] <= 11])
    df = df[list(range(0,10))]
    column_index = df.index[(df[0] == u'公司代號')][0]
    df.columns = df.iloc[column_index]
    df[u'當月營收'] = pd.to_numeric(df[u'當月營收'], 'coerce')
    df = df[~df[u'當月營收'].isnull()]
    df = df[df[u'公司代號'] != u'合計'].reset_index(drop=True)
    
    # 偽停頓
    time.sleep(5)
    df.to_csv(path + str(year) + str(month) + "income.csv", encoding = "utf-8")
    return df


if  __name__ == '__main__':
    print (monthly_report(Savefiledir, 2018, 8))
    print "query all stock info sdone"
