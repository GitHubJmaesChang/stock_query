#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import requests
from io import StringIO
import time

# "http://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID=1101&SYEAR=2018&SSEASON=2&REPORT_ID=C"
web_url     = "http://mops.twse.com.tw/server-java/t164sb01?step=1&"
company_url = "CO_ID="
year_url = "&SYEAR="
q_url = "&SSEASON="
report_url = "&REPORT_ID=C"

headers = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'	
}


def fetch_entire_finacialStatement(year, section, company_id):
    url = web_url + company_url + str(company_id) + year_url+ str(year)+ q_url+str(section) + report_url
    print url
    
    r = requests.get(url, headers=headers)
    r.encoding = 'big5'
    html_df = pd.read_html(StringIO(r.text))
    
    table1 = html_df[1]
    table2 = html_df[2]
    table3 = html_df[3]

    print table1.iloc[3][0:table1.shape[1]]   
    print table2.columns
    print table3.columns

    

if __name__ == '__main__':
   fetch_entire_finacialStatement("2018","2" ,"1101")
     
