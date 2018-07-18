# -*- coding: utf-8 -*-
#
# Usage: Download all stock code info from TWSE
#
# TWSE equities = 上市證券
# TPEx equities = 上櫃證券
#

import csv
from collections import namedtuple

import requests
from lxml import etree

TARGET_ID = "http://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID="
YEAR = "&SYEAR="
SECTION = "&SSEASON="
REPORT_ID = "&REPORT_ID=C"

def fetch_fincail_report(id, year, section):
    tarurl = TARGET_ID + id + YEAR + year + SECTION + section + REPORT_ID
    print tarurl