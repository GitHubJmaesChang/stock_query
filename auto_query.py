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
from db import add_db_record
import datetime
import calendar
import sys
import glob
import os

from QueryStock_Infor import data_query_financialStatementByQuarterTPEX
from QueryStock_Infor import data_query_financialStatementByQuarterTWSE


Monthly_Query_date =[ "01-20", "02-20", "03-20", "04-20", "05-20", "06-20", "07-20", "08-20", "09-20", "10-20", "11-20", "12-20"]

Quanter_report_date = { "05-17", "08-17", "11-17", "04-02"}

query_dict = {
		'FoundationExchange': data_query_institutional_investors_info,
		'MarginTrade': data_query_margin_and_short_trade,
		'StockExchange': data_query_stock_dailydata
			 }
query_monthly = {'MonthlyRevenue': data_query_month_income}

table_dict = {
		'FoundationExchange': "FoundationExchange",
		'MarginTrade':	"MarginTrading",
		'StockExchange': "StockExchange" 
		 }

buildOffDateTable = False

daily_job = [
        "/home/thomaschen/tmp/stock_query/CrawlerData/FoundationExchange/", \
        "/home/thomaschen/tmp/stock_query/CrawlerData/StockExchange/", \
        "/home/thomaschen/tmp/stock_query/CrawlerData/MarginTrade/" \
	    ]

def daterange(start_date, end_date):
	for n in range(int ((end_date - start_date).days)):
		yield start_date + timedelta(n)



# Functino to verify if a given path is valid.
# That is, it needs to have folder names as listed in query_dict.
def hasFunction(path):
	for fn in query_dict:
		if((str(fn) in path) == True):
			print("hasFunction: found corresponding function [" + str(fn) + "]")
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
	print("do_Crawl: Start calling crawler:: " + str(path))
	print("do_Crawl: Date Range:: START(" + str(startDate) + ") END(" + str(endDate) + ")")
	
	if(buildOffDateTable == False):
		print("do_Crawl: buildOffDateTable")
		buildTradeDate("2014", datetime.datetime.now().year)
		buildOffDateTable = True
	
	# Check function key
	fn = hasFunction(path)
	if(fn == 1):
		print("do_Crawl (ERROR): No function key found")
		return(-1)

	print("do_Crawl: Start looping through the dates")

	for single_date in daterange(startDate, endDate):
		try:
			sdate = single_date.strftime("%Y-%m-%d")
			print("Start processing date: [" + str(sdate) + "]")
			res = checkStoreYear(sdate)
			if(res == 1):
				print("Date: [" + str(sdate) + "] is valide")
				query_dict[fn](path, sdate)
			else:
				print("auto_query result: [0]:off [-1]:error : (" + str(res) + ")")
		except Exception as e:
			# No return or raise, need to loop through all dates
			print(e)



# Function to continue crawling from where stopped.
# That is, the next date of the last saved file to current execution date.
# If the directory is empty, the DB record will be checked. If the DB
# is empty, then an initialization process is triggered to get data from
# 5 years ago starting from the date of the execution of this script
def auto_query_cnt(path):
	isFolderChecked = False
	isDBChecked = False

	# search for the last saved file
	fileList = glob.glob(os.path.join(path, "*.csv")) 
	if(len(fileList) > 0):
		print("auto_query_cnt: Directory is NOT empty")
		isFolderChecked = True
		latest_file = max(fileList, key=os.path.getctime)
		print(latest_file)
		
		# Extract file name from full path string
		file_name = os.path.basename(latest_file)
		fname, fext = os.path.splitext(file_name)

		# Gets the date from the file and start from the next till current date.
		# The file's name is YYYYMMDD_[File Name].csv
		fdate = fname.split("_")[0]
		startDate = date(int(fdate[:4]), int(fdate[4:6]), int(fdate[6:8]) + 1)
		endDate = datetime.datetime.today().date()
		do_Crawl(startDate, endDate, path)
	else:
		print("auto_query_cnt: Directory is empty::" + path)

		print("auto_query_cnt: Start checking latest record in DB")
		# This is to check if the table name exists before connecting to the DB
		fn = hasFunction(path)
		if(fn == -1):
			print("auto_query result (ERROR): No matching function for the table")
		else:
			try:
				add_db_record.ConnectDB("localhost", "stock", "ftdi1234")
				table_date = add_db_record.getLatestDate(table_dict[fn])

				print("auto_query_cnt: found table dates are::")
				print(table_date)
				# Check if record exists
				if(table_date is None):
					print("auto_query result (ERROR): no records found")
				else:
					isDBChecked = True
					# The date stored in the DB has the format of YYYY-MM-DD
					tdate = table_date.split("-")
					startDate = date(int(tdate[0]), int(tdate[1]), int(tdate[2]) + 1 )
					endDate = datetime.datetime.today().date()
					do_Crawl(startDate, endDate, path)

			except Exception as e:
				print("auto_query result (ERROR): Exception")
				print(e)

	
	print("auto_query_cnt: Check if to run init process")
	# If folder is empty and DB is also empty, then run the init
	# process, that is date range is 5 years before current executing date
	# till now
	if((isFolderChecked == False) and (isDBChecked == False)):
		start_date = date(datetime.datetime.today().year - 5, 1, 1)
		end_date = datetime.datetime.today().date()

		print("auto_query_cnt: Start running init process")
		do_Crawl(start_date, end_date, path)
	else:
		print("auto_query result: Not running init process")



# Function to crawl data of a date range.
# The date range is previous 5 years from current execution date
def auto_query():
	start_date = date(datetime.datetime.today().year - 5, 1, 1)
	#end_date = date(2014, 1, 1)
	end_date = datetime.datetime.today().date()
	#directory = "/home/thomaschen/tmp/stock_query/CrawlerData/FoundationExchange/"
	directory = "/home/thomaschen/tmp/stock_query/CrawlerData/StockExchange/"

	buildTradeDate("2014", datetime.datetime.now().year)

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

def query_specify_report_by_date(sYear, edYear, path):
        start_date = date(int(sYear), 1, 1)
        end_date = datetime.datetime.today().date()
        
        print("start Year " + str(sYear) )
        print("end Year " + str(edYear) )
        
        directory = path
        buildTradeDate(str(sYear), datetime.datetime.now().year)
        
        print("*******sstart to fetch*********")
        for IdxYear in range(int(sYear), int(edYear)):
                for single_date in daterange(start_date, end_date):
                        sdate = single_date.strftime("%m-%d")
                        for t_date in Monthly_Query_date:
                                print("current date is " + str(t_date) + "sdate is " + str(single_date))
                                if(t_date == sdate):
                                        print("fetch the monthly data")
                                        print(str(int(single_date.strftime("%m"))))
                                        data_query_month_income(directory, IdxYear, int(single_date.strftime("%m")))
                        for t_date in Quanter_report_date:
                                print(t_date)
                                if(t_date == sdate):
                                        print("fetch the Qulter data")
                                        data_query_financialStatementByQuarterTPEX(directory, IdxYear, str(single_date.strftime("%m")))
                                        data_query_financialStatementByQuarterTWSE(directory, IdxYear, str(single_date.strftime("%m")))
                                
                

def test_main():
	for p in daily_job:
		print(p)
		auto_query_cnt(p)

# The subdirectory must contain either one of the following keywords:
# "FoundationExchange", "MarginTrade", "StockExchange". The python scripts, uses these
# keywords to point to corresponding functions for data crawling
def main(path):
	print(path)
	auto_query_cnt(path)

if __name__ == '__main__':
	#auto_query()		
	#test_main()
        query_specify_report_by_date("2016", datetime.datetime.now().year, "D:/Stock/data_folder/")
	#main(str(sys.argv[1]))


