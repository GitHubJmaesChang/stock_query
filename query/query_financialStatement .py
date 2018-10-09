#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import requests
import pandas as pd
import numpy as np
import csv, codecs, urllib, datetime, time, pdb
Savefiledir   = 'D://Stock/finacial/'
income_sheet  = "income_0"
blance_sheet  = "blance_0"
benefit_sheet = "benefit"
target_sheet  = "basic_report"
company_id_list =[]
headers = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'	
          }
def csv_create(path, target, year, season):
    filename = path + target + str(year) +'_s'+ str(season) + '.csv'
    print filename
    return filename
def statement_comprehensive_income_to_csv(year, season, url, path):
    if year>=1000:
       year -= 1911
		
    r = requests.post(url, {
        'encodeURIComponent':1,
        'step':1,
        'firstin':1,
        'off':1,
        'TYPEK':'sii',
        'year':str(year),
        'season':str(season),
    }, headers=headers)
	
    r.encoding = 'utf8'
    source_1 = pd.read_html(r.text)[3]
    fileoption  = codecs.open(csv_create(path, income_sheet, year, season),'wb')
    writer = csv.writer(fileoption, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    for idx in range(0, source_1.index.shape[0]):
        writer.writerow([source_1[0][idx].encode('utf8'),source_1[1][idx].encode('utf8'),source_1[2][idx].encode('utf8'),
                         source_1[3][idx].encode('utf8'),source_1[4][idx].encode('utf8'),source_1[5][idx].encode('utf8'),
                         source_1[6][idx].encode('utf8'),source_1[7][idx].encode('utf8'),source_1[8][idx].encode('utf8'),
                         source_1[9][idx].encode('utf8'),source_1[10][idx].encode('utf8'),source_1[11][idx].encode('utf8'),
                         source_1[12][idx].encode('utf8'),source_1[13][idx].encode('utf8'),source_1[14][idx].encode('utf8'),
                         source_1[15][idx].encode('utf8'),source_1[16][idx].encode('utf8'),source_1[17][idx].encode('utf8'),
                         source_1[18][idx].encode('utf8'),source_1[19][idx].encode('utf8'),source_1[20][idx].encode('utf8'),
                         source_1[21][idx].encode('utf8'),source_1[22][idx].encode('utf8'),source_1[23][idx].encode('utf8'),
                         source_1[24][idx].encode('utf8'),source_1[25][idx].encode('utf8'),source_1[26][idx].encode('utf8'),
                         source_1[27][idx].encode('utf8'),source_1[28][idx].encode('utf8'),source_1[29][idx].encode('utf8')
                         ])
    
    fileoption.close()
    return source_1
   
def blance_sheet_to_csv(year, season, url, path):
    if year>=1000:
       year -= 1911
		
    r = requests.post(url, {
        'encodeURIComponent':1,
        'step':1,
        'firstin':1,
        'off':1,
        'TYPEK':'sii',
        'year':str(year),
        'season':str(season),
    }, headers=headers)
	
    r.encoding = 'utf8'
    source_1 = pd.read_html(r.text)[3]
    fileoption  = codecs.open(csv_create(path, blance_sheet, year, season),'wb')
    writer = csv.writer(fileoption, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    for idx in range(0, source_1.index.shape[0]):
        writer.writerow([source_1[0][idx].encode('utf8'),source_1[1][idx].encode('utf8'),source_1[2][idx].encode('utf8'),
                         source_1[3][idx].encode('utf8'),source_1[4][idx].encode('utf8'),source_1[5][idx].encode('utf8'),
                         source_1[6][idx].encode('utf8'),source_1[7][idx].encode('utf8'),source_1[8][idx].encode('utf8'),
                         source_1[9][idx].encode('utf8'),source_1[10][idx].encode('utf8'),source_1[11][idx].encode('utf8'),
                         source_1[12][idx].encode('utf8'),source_1[13][idx].encode('utf8'),source_1[14][idx].encode('utf8'),
                         source_1[15][idx].encode('utf8'),source_1[16][idx].encode('utf8'),source_1[17][idx].encode('utf8'),
                         source_1[18][idx].encode('utf8'),source_1[19][idx].encode('utf8'),source_1[20][idx].encode('utf8'),
                         source_1[21][idx].encode('utf8')
                         ])
    
    fileoption.close()
    return source_1
def finacial_statement_to_csv(year, season, url, path):
    if year>=1000:
       year -= 1911
		
    r = requests.post(url, {
        'encodeURIComponent':1,
        'step':1,
        'firstin':1,
        'off':1,
        'TYPEK':'sii',
        'year':str(year),
        'season':str(season),
    })
	
    r.encoding = 'utf8'
    # to Bank table for general company
    source = pd.read_html(r.text)[0]
    # drop '公司代號'
    for idx in range(1, source.index.shape[0]):
        if idx>=source.index.shape[0]:
            break
        if not source[0][idx]:
                pass
        else:
            if (source[0][idx]== u'公司代號'):
                    source = source.drop(source.index[idx])
                    source = source.reset_index(drop=True)
     
    fileoption  = codecs.open(csv_create(path, benefit_sheet, year, season),'wb')
    writer = csv.writer(fileoption, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    for idx in range(0, source.index.shape[0]):
        writer.writerow([source[0][idx].encode('utf8'),
                         source[1][idx].encode('utf8'),
                         source[2][idx].encode('utf8'),
                         source[3][idx].encode('utf8'),
                         source[4][idx].encode('utf8'),
                         source[5][idx].encode('utf8'),
                         source[6][idx].encode('utf8')])
    
    fileoption.close()

def Stock_query_data(year, season, query_table, path):
    url=''
    if query_table == '綜合損益彙總表':	
        url = 'http://mops.twse.com.tw/mops/web/ajax_t163sb04'
        statement_comprehensive_income_to_csv(year, season, url, path)
    elif query_table == '資產負債彙總表':
        url = 'http://mops.twse.com.tw/mops/web/ajax_t163sb05'
        blance_sheet_to_csv(year, season, url, path)
    elif query_table == '營益分析彙總表':
        url = 'http://mops.twse.com.tw/mops/web/ajax_t163sb06'
        finacial_statement_to_csv(year, season, url, path)
    else:
        print('type does not match')
def query_stock_sheet(year, season, path):
    income = Stock_query_data(year, season,'綜合損益彙總表', path)
    print "incom sheet done"
    balance = Stock_query_data(year, season,'資產負債彙總表', path)
    print "blance sheet done"
    Stock_query_data(year, season,'營益分析彙總表', path)
    print "benefit sheet done"

def Stock_roe_roa_eps_prepare(year, season, path):
    if year>=1000:
       year -= 1911
    inclome_file = path + income_sheet + str(year) +"_s"+ str(season)+".csv"
    income_data = pd.read_csv(inclome_file)
    balance_file = path + blance_sheet + str(year) +"_s"+ str(season)+".csv"
    balance_data = pd.read_csv(balance_file) 
    roe =[]

    equity_str = 0
    cmp_value_str =0

    if(year>106):
        equity_str = u'權益總計'.encode('utf-8')
        cmp_value_str = u'資產總計'.encode('utf-8')
    else:
        equity_str = u'權益總額'.encode('utf-8')
        cmp_value_str = u'資產總額'.encode('utf-8')
        
    for idx in range(0, income_data.shape[0]):
        roe.append(float(income_data[u'本期淨利（淨損）'.encode('utf-8')][idx])/
                   float(balance_data[equity_str][idx]))
    roe_form = pd.DataFrame({ u' ROE ' : roe})
        
    roa =[]
    for idx in range(0, income_data.shape[0]):
        roa.append(float(income_data[u'本期淨利（淨損）'.encode('utf-8')][idx])/
                   float(balance_data[equity_str][idx]))

    roa_form = pd.DataFrame({ u' ROA ' : roa})
    #update company id to global list "company_id_list"
    new_form = pd.concat([balance_data[u'公司代號'.encode('utf-8')],
               balance_data[u'公司名稱'.encode('utf-8')],
               balance_data[cmp_value_str],
               balance_data[equity_str],
               income_data[u'營業收入'.encode('utf-8')],
               income_data[u'營業利益（損失）'.encode('utf-8')],
               income_data[u'營業外收入及支出'.encode('utf-8')],
               income_data[u'稅前淨利（淨損）'.encode('utf-8')],
               income_data[u'本期淨利（淨損）'.encode('utf-8')],
               income_data[u'基本每股盈餘（元）'.encode('utf-8')],
               balance_data[u'每股參考淨值'.encode('utf-8')],
               roe_form[u' ROE '.encode('utf-8')],
               roa_form[u' ROA '.encode('utf-8')]],
               axis=1)
   
    save_merge_file = path + target_sheet + str(year) +"_s"+str(season)+".csv"
    new_form.to_csv (save_merge_file, encoding = "utf-8")
    #id_data = pd.concat([balance_data[u'公司代號'.encode('utf-8')]],axis=1)
    #id_data.to_csv( path + "comp_id"+".csv", encoding = "utf-8")
    return new_form
                         
def update_company_state(year, season, filePath):
   if not os.path.isdir(filePath):
       os.makedirs(filePath)
   query_stock_sheet(year, season, filePath)
   #Stock_roe_roa_eps_prepare(year, season, filePath)
   
if __name__ == '__main__':
   update_company_state(2017, 4, Savefiledir)
