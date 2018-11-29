#!/usr/bin/python
# -*- coding: utf_8 -*-

from datetime import date, timedelta
from QueryStock_Infor import checkQueryCommand
from QueryStock_Infor import data_query_institutional_investors_info
from QueryStock_Infor import data_query_margin_and_short_trade
from QueryStock_Infor import data_query_stock_dailydata
from QueryStock_Infor import data_query_month_income
from publicholiday import buildTradeDate
from publicholiday import checkStoreYear
from db imoprt add_db_record
import datetime
import calendar
import sys
import glob
import os


query_dict = {
		'FoundationExchange': data_query_institutional_investors_info,
		'MarginTrade': data_query_margin_and_short_trade,
		'StockExchange': data_query_stock_dailydata
		#'MonthlyRevenue': data_query_month_income
             }

table_dict = {
		'FoundationExchange': "FinancialExchange",
		'MarginTrade':  "MarginTrading",
		'StockExchange': "StockExchange" 
	     }

buildOffDateTable = False

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)



# Functino to verify if a given path is valid.
# That is, it needs to have folder names as listed in query_dict.
def hasFunction(path):
    for fn in query_dict:
        if((str(fn) in path) == True):
	    return(fn)

    return(-1)

# Function to crawl data by a provided date
def single_query(path, date):
    global query_dict

    fn = hasFunction(path)
    if(fn != -1):
        query_dict[fn](path, date)
    else:
        print("single_query (ERROR): function [" + str(fn) + "] not in dict")

# Function to run corresponding data crawling function with 
# the given date range and path.
def do_Crawl(startDate, endDate, path):
    global buildOffDateTable

    print("Start calling crawler: " + str(fn))

    if(buildOffDateTable == False):
        buildTradeDate()
	buildOffDateTable = True
    
    for single_date in daterange(startDate, endDate):
        try:
            sdate = single_date.strftime("%Y-%m-%d")
            print("Start processing date: [" + str(sdate) + "]")
            res = checkStoreYear(sdate)
            fn = hasFunction(path)	# Get function key
            if((res == 1) and (fn != -1)):
                print("Date: [" + str(sdate) + "] is valide")
                query_dict[fn](path, sdate)
            else:
                print("auto_query result: [0]:off [-1]:error : (" + str(res) + ")")
	except Exception as e:
	    print(e)
       

# Function to continue crawling from where stopped.
# That is, the next date of the last saved file to current execution date.
# If the directory is empty, the DB record will be checked
def auto_query_cnt(path):
    # search for the last saved file
    fileList = glob.glob(os.path.join(path, "*.csv")) 
    
    if(fileList != False):
        latest_file = max(fileList, key=os.path.getctime)
        print(latest_file)

        # Gets the date from the file and start from the next till current date.
	# The file's name is YYYYMMDD_[File Name].csv
        fdate = latest_file.split("_")[0]
        startDate = date(int(fdate[:4]), int(fdate[4:6]), int(fdate[6:8]) + 1)
        endDate = datetime.datetime.today().date()
    	do_Crawl(startDate, endDate, path)
    else:
        print("Directory is empty:" + path)
	print("Start checking latest record in DB")

	# This is to check if the table name exists before connecting to the DB
	fn = hasFunction(path)
	if(fn == -1):
	    print("auto_query result (ERROR): No matching function for the table")
	    return(-1)
	try:
            add_db_record.ConnectDB("localhost", "stock", "ftdi1234")
            table_date = add_db_record.getLatestDate(table_dict[fn])

	    # Check if record exists
            if(table_date == -1):
	        print("auto_query result (ERROR): no records found")
	        return(-1)

	    # The date stored in the DB has the format of YYYY-MM-DD
	    tdate = table_date.split("-")
            startDate = date(int(tdate[0]), int(tdate[1]), int(tdate[2]) + 1 )
            endDate = datetime.datetime.today().date()
	    do_Crawl(startDate, endDate, path)

    except Exception as e:
            print("auto_query result (ERROR): Exception")
	    print(e)
	    return(-1)



# Function to crawl data of a date range.
# The date range is previous 5 years from current execution date
def auto_query():
	start_date = date(datetime.datetime.today().year - 5, 1, 1)
	#end_date = date(2014, 1, 1)
	end_date = datetime.datetime.today().date()
	directory = "/home/thomaschen/tmp/stock_query/CrawlerData/FoundationExchange/"

	buildTradeDate()

	print("complete building years")

	for single_date in daterange(start_date, end_date):
		sdate = single_date.strftime("%Y-%m-%d")
		print("Start processing date: [" + str(sdate) + "]")
		res = checkStoreYear(sdate)
		if(res == 1):
		#if(checkQueryCommand(directory, sdate) == 1)
			#sdate = sdate.replace("-", "")
			print("Date: [" + str(sdate) + "] is valide")
			data_query_institutional_investors_info(directory, sdate)
		else:
			print("auto_query result: [0]:off [-1]:error : (" + str(res) + ")")

if __name__ == '__main__':
	auto_query()		


