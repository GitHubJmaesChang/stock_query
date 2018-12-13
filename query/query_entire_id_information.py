#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import requests
from io import StringIO
import time
import cell_items_name  
from rand_proxy import htmlRequest
from query_company_id import query_public_trade_TWSE_ID
from query_company_id import query_public_trade_TPEX_ID


# "http://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID=1101&SYEAR=2018&SSEASON=2&REPORT_ID=C"
web_url     = "http://mops.twse.com.tw/server-java/t164sb01?step=1&"
company_url = "CO_ID="
year_url = "&SYEAR="
q_url = "&SSEASON="
report_url_modeA = "&REPORT_ID=A"
report_url_modeC = "&REPORT_ID=C"

headers ={
	    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'	
          }

def fill_table(idxID, balance_sheet_fetch, cash_flow_sheet_fetch, income_statement_sheet_fetch):
    
    #balance_sheet_fetch = {}
    search_start = 0
    for idx, members in cell_items_name.balance_sheet.iteritems():
        for cell in members :
                balance_sheet_fetch.update({cell : 0})


    #cash_flow_sheet_fetch = {}
    search_start = 0
    for idx, members in cell_items_name.cash_flow_sheet.iteritems():
        for cell in members :
            cash_flow_sheet_fetch.update({cell : 0})
                
    #income_statement_sheet_fetch = {}
    search_start = 0
    for idx, members in cell_items_name.income_statement_sheet.iteritems():
        for cell in members :
            income_statement_sheet_fetch.update({cell : 0})
    
    pd0 =  pd.DataFrame({"ID" : str(idxID)}, index=[0])
    pd1 =  pd.DataFrame(data=balance_sheet_fetch, index=[0])
    pd2 =  pd.DataFrame(data=cash_flow_sheet_fetch, index=[0])
    pd3 =  pd.DataFrame(data=income_statement_sheet_fetch, index=[0])
    
    #母公司淨利比例
    pd4 =  pd.DataFrame({"母公司淨利比例" : float(0.0)}, index=[0])
    #業外占營收比例
    pd5 =  pd.DataFrame({"業外占營收比例" : float(0.0)}, index=[0])
    #存貨周轉率
    pd6 =  pd.DataFrame({"存貨周轉率" : float(0.0)}, index=[0])
    #毛利率
    pd7 =  pd.DataFrame({"毛利率" : float(0.0)}, index=[0])
    #營業利益
    pd8 =  pd.DataFrame({"營業利益" : float(0.0)}, index=[0])    
    #original Roe
    pd9 =  pd.DataFrame({"ROE_Org" : float(0.0)}, index=[0])
    #total income Roe
    pd10 =  pd.DataFrame({"ROE" : float(0.0)}, index=[0])
    #total Roa
    pd11 =  pd.DataFrame({"ROA" : float(0.0)},index=[0])
    frame_table = pd.concat([pd0, pd1, pd2, pd3, pd4, pd5, pd6, pd7, pd8, pd9, pd10, pd11], axis=1, sort=False)
    return frame_table

def fetch_entire_finacialStatement(year,
                                   section,
                                   company_id,
                                   report_url_mode, 
                                   balance_sheet_fetch,
                                   cash_flow_sheet_fetch,
                                   income_statement_sheet_fetch):

    print report_url_mode
    target_url = web_url + company_url + str(company_id) + year_url+ str(year)+ q_url+str(section) + report_url_mode
    print target_url
    try:
        html_report = htmlRequest(target_url, "get", "")
        html_report.encoding = 'big5'
        DataFrame_form = pd.read_html(StringIO(html_report.text))
        print "DataFrame create success"
    except Exception as e:
        print "exception happened"
        print(e)

    #print DataFrame_form
    #r = requests.get(target_url, headers=headers)
    #r.encoding = 'big5'
    #DataFrame_form = pd.read_html(StringIO(r.text))

    if(len(DataFrame_form) < 2):
        print "hteml file not exist"
        print DataFrame_form
        raise 


    print "fetch data start"
    
    balance_sheet_table = DataFrame_form[1]
    cash_flow_sheet_table = DataFrame_form[2]
    income_statement_sheet_table = DataFrame_form[3]

    print "fetch balance_sheet_fetch start"
    #balance_sheet_fetch = {}
    search_start = 0
    for idx, members in cell_items_name.balance_sheet.iteritems():
        for cell in members :
            for row_item in range (search_start, balance_sheet_table.shape[0]):
                if balance_sheet_table.loc[row_item][0] == cell:
                    balance_sheet_fetch.update({cell : balance_sheet_table.loc[row_item][1]})
                    search_start = row_item
                    break
                if(row_item == (balance_sheet_table.shape[0]-1)):
                    balance_sheet_fetch.update({cell : 0})

    print "fetch cash_flow_sheet_fetch start"
    #cash_flow_sheet_fetch = {}
    search_start = 0
    for idx, members in cell_items_name.cash_flow_sheet.iteritems():
        for cell in members :
            for row_item in range (search_start, cash_flow_sheet_table.shape[0]):
                if cash_flow_sheet_table.loc[row_item][0] == cell:
                    cash_flow_sheet_fetch.update({cell : cash_flow_sheet_table.loc[row_item][1]})
                    search_start = row_item
                    break
                if(row_item == (cash_flow_sheet_table.shape[0]-1)):
                    cash_flow_sheet_fetch.update({cell : 0})

    print "fetch cash_flow_sheet_fetch start"
    #income_statement_sheet_fetch = {}
    search_start = 0
    for idx, members in cell_items_name.income_statement_sheet.iteritems():
        for cell in members :
            for row_item in range (search_start, income_statement_sheet_table.shape[0]):
                if income_statement_sheet_table.loc[row_item][0] == cell:
                    income_statement_sheet_fetch.update({cell: income_statement_sheet_table.loc[row_item][1]})
                    search_start = row_item
                    break
                if(row_item == (income_statement_sheet_table.shape[0]-1)):
                    income_statement_sheet_fetch.update({cell : 0})

    pd0 =  pd.DataFrame({"ID" : str(company_id)}, index=[0])
    pd1 =  pd.DataFrame(data=balance_sheet_fetch, index=[0])
    pd2 =  pd.DataFrame(data=cash_flow_sheet_fetch, index=[0])
    pd3 =  pd.DataFrame(data=income_statement_sheet_fetch, index=[0])
    
    #母公司淨利比例
    data1 = float(cash_flow_sheet_fetch[u'營業利益（損失）']) + float(cash_flow_sheet_fetch[u'營業外收入及支出合計'])
    data2 = float(cash_flow_sheet_fetch[u'母公司業主（淨利／損）'])
    if(data1 ==0):
        print "exception error happened"
        temp = 0.0
    else :
        temp = float(data2 / data1)
        
    print ("母公司淨利比例 : " + str(temp) )
    pd4 =  pd.DataFrame({"母公司淨利比例" : temp }, index=[0])

    #業外占營收比例
    data1 = float(cash_flow_sheet_fetch[u'營業利益（損失）']) + float(cash_flow_sheet_fetch[u'營業外收入及支出合計'])
    data2 = float(cash_flow_sheet_fetch[u'營業外收入及支出合計'])

    if(data1 ==0):
        print "exception error happened"
        temp = 0.0
    else :
        temp = float(data2 / data1)
        
    print ("業外占營收比例 : " + str(temp) )
    pd5 =  pd.DataFrame({"業外占營收比例" : temp },index=[0])

    
    #存貨周轉率
    data1 = float(balance_sheet_fetch[u'存貨'])
    data2 = float(cash_flow_sheet_fetch[u'營業成本合計'])

    if(data1 ==0):
        print "exception error happened"
        temp = 0.0
    else :
        temp = float(data2 / data1)

    print ("存貨周轉率 : " + str(temp) )
    pd6 =  pd.DataFrame({"存貨周轉率" : temp }, index=[0])
    
    #毛利率
    data1 = float(cash_flow_sheet_fetch[u'營業收入合計'])
    data2 = float(cash_flow_sheet_fetch[u'營業毛利（毛損）淨額'])

    if(data1 ==0):
        print "exception error happened"
        temp = 0.0
    else :
        temp = float(data2 / data1)
        
    print ("存貨周轉率 : " + str(temp) )
    pd7 =  pd.DataFrame({"毛利率" : temp }, index=[0])
    
    #營業利益
    data1 = float(cash_flow_sheet_fetch[u'營業收入合計'])
    data2 = float(cash_flow_sheet_fetch[u'營業利益（損失）'])
    if(data1 ==0):
        print "exception error happened"
        temp = 0.0
    else :
        temp = float(data2 / data1)
        
    print ("營業利益 : " + str(temp) )
    pd8 =  pd.DataFrame({"營業利益" : temp }, index=[0])
    
    #original Roe
    data1 = float(balance_sheet_fetch[u'權益總額'])
    data2 = float(cash_flow_sheet_fetch[u'本期淨利（淨損）'] )- float(cash_flow_sheet_fetch[u'營業外收入及支出合計'])

    if(data1 ==0):
        print "exception error happened"
        temp = 0.0
    else :
        temp = float(data2 / data1)

    if(data2>0.0):
        print ("ROE_Org : " + str(temp) )
    else:
        print ("ROE_Org : -" + str(abs(temp)) )
     
    pd9 =  pd.DataFrame({"ROE_Org" : temp }, index=[0])
    
    #total income Roe
    data1 = float(balance_sheet_fetch[u'權益總額'])
    data2 = float(cash_flow_sheet_fetch[u'本期淨利（淨損）'])

    if(data1 ==0):
        print "exception error happened"
        temp = 0.0
    else :
        temp = float(data2 / data1)

    print ("ROE : " + str(temp) )
    pd10 =  pd.DataFrame({"ROE" : temp }, index=[0])
    
    #total Roa
    data1 = float(balance_sheet_fetch[u'負債及權益總計'])
    data2 = float(cash_flow_sheet_fetch[u'本期淨利（淨損）'])

    if(data1 ==0):
        print "exception error happened"
        temp = 0.0
    else :
        temp = float(data2 / data1)

    print ("ROA : " + str(temp) )
    pd11 =  pd.DataFrame({"ROA" : temp }, index=[0])
    
    frame_table = pd.concat([pd0, pd1, pd2, pd3, pd4, pd5, pd6, pd7, pd8, pd9, pd10, pd11], axis=1, sort=False)
    return frame_table
                
"""
    for idx, members in cell_items_name.balance_sheet.iteritems():
        for cell in members :
            print balance_sheet_table[cell]
"""

def financialStatement_prepare(year, section, fetch_table_type):

    id_table = []
    if(fetch_table_type == "TWSE"):
        id_table = query_public_trade_TWSE_ID()
    else:
        id_table = query_public_trade_TPEX_ID()

    print id_table

    if(len(id_table) ==0):
        return
    
    balance_sheet_fetch = {}
    cash_flow_sheet_fetch = {}
    income_statement_sheet_fetch = {}

    pd1 = fill_table("99999", balance_sheet_fetch, cash_flow_sheet_fetch, income_statement_sheet_fetch)
    #fetch_entire_finacialStatement("2018","3" ,"1108", balance_sheet_fetch, cash_flow_sheet_fetch, income_statement_sheet_fetch)

    url_type1 ="&REPORT_ID=C"
    url_type2 ="&REPORT_ID=A"
    url = url_type1
    idx = 0
    retry_idx = 0
    
    while True:
        print "start process"
        # fill the ID table to "0"
        if(retry_idx >= 10): #retry times
            pdx = fill_table(str(id_table[idx]), balance_sheet_fetch, cash_flow_sheet_fetch, income_statement_sheet_fetch)
            pd1 = pd1.append(pdx)
            idx = idx + 1
            retry_idx = 0
        try :
            print "access data from proxy server"                
            pdx = fetch_entire_finacialStatement(year, section ,str(id_table[idx]),url,
                                                 balance_sheet_fetch, cash_flow_sheet_fetch, income_statement_sheet_fetch)
        except Exception as e:
            print "retry"
            if(url == url_type1):
                url = url_type2
            else:
                url = url_type1

            retry_idx = retry_idx +1
            time.sleep(10)
            continue
        # update table
        pd1 = pd1.append(pdx)
        #clean retry
        retry_idx = 0
        print ("The ID : " + str(idx) + " done")
        idx = idx + 1
        if(idx >= len(id_table)):
            break

    PATH_FILE = ""
    if(fetch_table_type == "TWSE"):
        PATH_FILE = "D:/Stock/finacial/TWSE_financialStatement.csv"
    else:
        PATH_FILE = "D:/Stock/finacial/TPEX_financialStatement.csv"
    
    pd1.to_csv(PATH_FILE, index = False, encoding = "utf-8")
    return pd1


if __name__ == '__main__':
    financialStatement_prepare("2018", "3", "TPEX")
