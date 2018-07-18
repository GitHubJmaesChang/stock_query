# -*- coding: utf-8 -*-
#
# -*- coding: utf-8 -*-
# TWSE equities = 上市證券
# TPEx equities = 上櫃證券
#

import csv
import os
from collections import namedtuple


ROW = namedtuple('StockCodeInfo', ['type', 'code', 'name', 'ISIN', 'start',
                                   'market', 'group', 'CFI'])
PACKAGE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
TPEX_EQUITIES_CSV_PATH = os.path.join(PACKAGE_DIRECTORY, 'codes', 'tpex_equities.csv')
TWSE_EQUITIES_CSV_PATH = os.path.join(PACKAGE_DIRECTORY, 'codes', 'twse_equities_edit.csv')

codes = {}
tpex = {}
twse = {}
company_id=[]

def read_csv(path, types):
    global codes, twse, tpex, company_id
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        csvfile.readline()
        for row in reader:
            row = ROW(*(item.strip() for item in row))
            codes[row.code] = row
            company_id.append(row.code)
            if types == 'tpex':
                tpex[row.code] = row
            else:
                twse[row.code] = row

print  "current path : "+TPEX_EQUITIES_CSV_PATH
print  "current path :" +TWSE_EQUITIES_CSV_PATH
#read_csv(TPEX_EQUITIES_CSV_PATH, 'tpex')
read_csv(TWSE_EQUITIES_CSV_PATH, 'twse')