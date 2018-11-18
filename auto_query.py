#!/usr/bin/python
# -*- coding: utf_8 -*-

from datetime import date, timedelta
from QueryStock_Infor import checkQueryCommand
from QueryStock_Infor import data_query_institutional_investors_info
from publicholiday import buildTradeDate
from publicholiday import checkStoreYear
import datetime
import calendar
import sys



def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def auto_query():
	start_date = date(datetime.datetime.today().year - 5, 1, 1)
	#end_date = date(2014, 1, 1)
	end_date = datetime.datetime.today().date()
	directory = "./CrawlerData/"

	buildTradeDate()

	print("complete building years")

	checkStoreYear("2018-1-1")

	for single_date in daterange(start_date, end_date):
		sdate = single_date.strftime("%Y-%m-%d")
		print(sdate)
		res = checkStoreYear(sdate)
		if(res == 1):
		#if(checkQueryCommand(directory, sdate) == 1)
			#sdate = sdate.replace("-", "")
			print(sdate)
			data_query_institutional_investors_info(directory, sdate)
		else:
			print("auto_query result: 0:off -1:error " + str(res))

if __name__ == '__main__':
	auto_query()		


