#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, errno
import sys
import pandas as pd
import time

from query import query_company_id
from query import query_financialStatement
from query import query_institutional_investors_info
from query import query_margin_and_short_trade
from query import query_month_income
from query import query_stock_dailydata
from query import query_stock_info_by_ID
from query import query_entire_id_information
from query import cell_items_name
from publicholiday import validDate
from publicholiday import isTradeDate

def check_file_exist(filename):
    if(os.path.isfile(filename)):
        return TRUE
    else:
        return FALSE


# update company ID
def data_query_company_id():
    query_company_id.query_public_trade_company_ID()

# to query financial report
# parameter ->path = "to save the csv file"
#           ->year = "2018"
#           ->season = "1" //Q1
def data_query_financialStatement(path, year,season):
    query_financialStatement.update_company_state(year, season, path)

# to query institutional_investors report
# parameter ->path = "to save the csv file"
#           ->date = "20181031"
def data_query_institutional_investors_info(path, date):
    query_institutional_investors_info.daily_institutional_info(path , date)

# to query query_margin_and_short_trade report
# parameter ->path = "to save the csv file"
#           ->date = "20181031"
def data_query_margin_and_short_trade(path, date):
    query_margin_and_short_trade.daily_information(path , date)

# to query monthly Revenue report
# parameter ->path = "to save the csv file"
#           ->date = "2018"
#           ->month = "8"
def data_query_month_income(path, year, month):
    query_month_income.monthly_report(path, year, month)

# to query syock exchange report
# parameter ->path = "to save the csv file"
#           ->date = "20181031"
def data_query_stock_dailydata(path, date):
    query_stock_dailydata.daily_information(path , date)
    
# to query entire TPEX financail Statement report
# parameter ->path = "to save the csv file"
#           ->year = "2018"
#           ->Quarter = "2"
def data_query_financialStatementByQuarterTPEX(path, year, quarter):
    query_entire_id_information.financialStatement_prepare(path, year, quarter, "TPEX")

# to query entire TWSE financail Statement report
# parameter ->path = "to save the csv file"
#           ->year = "2018"
#           ->Quarter = "2"
def data_query_financialStatementByQuarterTWSE(path, year, quarter):
    query_entire_id_information.financialStatement_prepare(path, year, quarter, "TWSE")

def data_query_stock_info_by_ID(path, Stock_id):
    query_stock_info_by_ID.stock_query(Stock_id, path)


def checkQueryCommandInput(argv):
	directory = str(argv[1])
	date = str(argv[2])

	# not enough or too many argument(s)
	if(len(sys.argv) <= 1) or (len(sys.argv) > 3):
		return(False)
	
	return(checkQueryCommand(directory, date))

def checkQueryCommand(directory, date):
	if(date.isdigit == False):
		return(-1)

	if not os.path.exists(directory):
		try:
			os.makedirs(directory)
		except OSError as err:
			print("Create directory error: [" + str(err) + "] ")
			return(-1)
	
	print("Path: [" + directory + "]  Date: [" + date + "]")

	if(validDate(date) == False):
		return(-1)

	if(isTradeDate(date, True) == False):
		print("QueryStock_infor: [" + str(date)  + "] not a trade date")
		return(0)

	return(1)


if __name__ == '__main__':
	#if(checkQueryCommandInput(sys.argv) == True):
	#	data_query_institutional_investors_info(argv[1], argv[2])
    data_query_institutional_investors_info("D:/Stock/finacial/", "20181105")
    #time.sleep(60)
    #data_query_margin_and_short_trade("D:/Stock/finacial/", "20181105")
    #time.sleep(70)
    #data_query_stock_dailydata("D:/Stock/finacial/", "20181105")
    #time.sleep(80)
    #data_query_month_income("D:/Stock/finacial/", "2018", "09")


