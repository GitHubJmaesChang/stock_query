# -*- coding: utf-8 -*-
#
# Usage: Download all stock code info from TWSE
#
# TWSE equities = 上市證券
# TPEx equities = 上櫃證券
#

import datetime
from collections import namedtuple

try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError

import requests
import code_csv
from codes import fincial_report_parser
	
	
	
if __name__ == '__main__':
     for ID in code_csv.company_id :
	      fincial_report_parser.fetch_fincail_report(ID, "2018", "1")

		  




