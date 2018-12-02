#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import requests
from io import StringIO
import time
import cell_items_name  
#from rand_proxy import htmlRequest


# "http://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID=1101&SYEAR=2018&SSEASON=2&REPORT_ID=C"
web_url     = "http://mops.twse.com.tw/server-java/t164sb01?step=1&"
company_url = "CO_ID="
year_url = "&SYEAR="
q_url = "&SSEASON="
report_url = "&REPORT_ID=C"

headers ={
	    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'	
          }


def fetch_entire_finacialStatement(year, section, company_id,
                                   balance_sheet_fetch,
                                   cash_flow_sheet_fetch,
                                   income_statement_sheet_fetch):
    
    target_url = web_url + company_url + str(company_id) + year_url+ str(year)+ q_url+str(section) + report_url
    """
    try:
        html_report = htmlRequest(target_url, "get", "")
        DataFrame_form = pd.read_html(html_report.text.encode('utf8'))
    except Exception as e:
        print(e)
        raise Exception
    """

    r = requests.get(target_url, headers=headers)
    r.encoding = 'big5'
    DataFrame_form = pd.read_html(StringIO(r.text))
    
    balance_sheet_table = DataFrame_form[1]
    cash_flow_sheet_table = DataFrame_form[2]
    income_statement_sheet_table = DataFrame_form[3]

    
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

    print balance_sheet_fetch
    pd0 =  pd.DataFrame({"ID" : str(company_id)}, index=[0])
    pd1 =  pd.DataFrame(data=balance_sheet_fetch, index=[0])
    pd2 =  pd.DataFrame(data=cash_flow_sheet_fetch, index=[0])
    pd3 =  pd.DataFrame(data=income_statement_sheet_fetch, index=[0])

    frame_table = pd.concat([pd0, pd1, pd2, pd3], axis=1, sort=False)
    return frame_table
                
"""
    for idx, members in cell_items_name.balance_sheet.iteritems():
        for cell in members :
            print balance_sheet_table[cell]
"""
    

if __name__ == '__main__':
    
    balance_sheet_fetch = {}
    cash_flow_sheet_fetch = {}
    income_statement_sheet_fetch = {}
    pd1 = fetch_entire_finacialStatement("2018","3" ,"1101", balance_sheet_fetch, cash_flow_sheet_fetch, income_statement_sheet_fetch)
    time.sleep(11)
    pd2 = fetch_entire_finacialStatement("2018","3" ,"6605", balance_sheet_fetch, cash_flow_sheet_fetch, income_statement_sheet_fetch)
    time.sleep(11)
    pd3 = fetch_entire_finacialStatement("2018","3" ,"2352", balance_sheet_fetch, cash_flow_sheet_fetch, income_statement_sheet_fetch)
    time.sleep(11)
    pd4 = fetch_entire_finacialStatement("2018","3" ,"9945", balance_sheet_fetch, cash_flow_sheet_fetch, income_statement_sheet_fetch)
    time.sleep(11)
    pd5 = fetch_entire_finacialStatement("2018","3" ,"3045", balance_sheet_fetch, cash_flow_sheet_fetch, income_statement_sheet_fetch)
    
    pd1 = pd1.append(pd2)
    pd1 = pd1.append(pd3)
    pd1 = pd1.append(pd4)
    pd1 = pd1.append(pd5)
    pd1.to_csv("D:/Stock/finacial/test.csv",  index = False, encoding = "utf-8")
