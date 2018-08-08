
#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pandas as pd
import time

from query import query_company_data
from query import query_stock_date

comp_id   = 'comp_id.csv'
File_Path = 'D://Stock/stock_trade//'

if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    #query_company_data.update_company_state(2018,1, path + "//fincial_report//")

    company_id = pd.read_csv(path + "/fincial_report/" + comp_id)
    
    for idx in range(0, company_id.shape[0]):
        query_stock_date.stock_query( str(company_id.iloc[idx][1]), path + "//stock_report//")
        time.sleep(5)
    
    print "process done"
