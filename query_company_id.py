# -*- coding: cp950 -*-

#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pandas as pd
import time
import requests
from lxml import etree
from collections import namedtuple

#from query import query_company_data
#from query import query_stock_date

comp_id   = 'comp_id.csv'
File_Path = 'D:/Stock/finacial/'

headers_info ={
	    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'	
          }

ROW = namedtuple('Row', ['type', 'code', 'name', 'ISIN', 'start',
                         'market', 'group', 'CFI'])

def make_row_tuple(typ, row):
    code = row[1].split()[0]
    name = row[1].split()[1]
    return ROW(typ, code, name, *row[2: -1])

def fetch_data(url, cmp_id, cmp_name):
    r = requests.get(url)
    root = etree.HTML(r.text)
    trs = root.xpath('//tr')[1:]
    result = []
    typ = ''
    for tr in trs:
        tr = list(map(lambda x: x.text, tr.iter()))
        if len(tr) == 4:
            # This is type
            typ = tr[2].strip(' ')
        else:
            # This is the row data
            idx = make_row_tuple(typ, tr)
            if(idx[7] ==u'ESVUFR'):
                cmp_id.append(idx[1])
                cmp_name.append(idx[2])

def query_public_trade_company_ID():
    url = "http://isin.twse.com.tw/isin/C_public.jsp?strMode=2"
    name =[]
    com_id=[]
    fetch_data(url, com_id, name)
    row_form1 = pd.DataFrame({ u' ID '     : com_id})
    row_form2 = pd.DataFrame({ u' Name '   : name})
    form1 = pd.concat([row_form1[u' ID '],
                       row_form2[u' Name '],], axis =1)
    
    form1.to_csv(File_Path + comp_id, encoding = "utf-8")
    
if __name__ == '__main__':
    query_public_trade_company_ID()
    print "process done"
