#!/usr/bin/python
# -*- coding: utf_8 -*-

from datetime import date, timedelta
import datetime
import calendar
import sys
import requests
import pandas as pd
from collections import defaultdict
from query import rand_proxy


AllYear = defaultdict(list)

def removeYear(text):
	if(isinstance(text, float)):
		return("")
	# remove year information
	start = text.find(u'\u65e5') # search for first "ri"
	end = text.find(u'\u5e74')   # search for fist "nian"

	# "nian" not found
	if(end == -1):
		print("Year char Not found")
		return(text)
	else:
		if(start > end): # indicates that there is no "ri" before
			text = text[(end + 1):]
		else:
			text = text[:start] + text[(end + 1):]


	print("removeYear: Start: [" + str(start) + "] End: [" + str(end) + "]")

	result = removeYear(text)
	return(result)

def removeBracket(text):
        if(isinstance(text, float)):
                return("")
        
	start = text.find("(") 
        end = text.find(")")  

        if((end == -1) and (start == -1)):
                print("Parenthesis Not found")
                return(text)
	elif((end == -1) or (start == -1) or (start > end)):
		print("Incorrect parenthesis")
		return(text)
        else:
		print("Remove ()")
		text = text[:start] + text[(end+1):]


	result = removeBracket(text)
	return(result)

def checkTradeDate(text, date, ischeck):
	dlist = []
	res = text.split(u'\u65e5')
	res = filter(None, res)
	for x in res:
		tmp = x.replace(u'\u6708', "")
		tmp = tmp.replace(" ", "")
		tmp = str(tmp)
		dlist.append(tmp)
		if((tmp == date) and (ischeck == True)):
			return(dlist, False)

	return(dlist, True)

def isTradeDate(date, fullcheck):

	print("verify date: " + date)

	if(fullcheck == True):
		# check if date format is correct
		if(not validDate(date)):
			return(-1)
		# check if it is a weekend
		if(isWeekend(date)):
			return(-1)

	# extract year and date to check if it is a trading date
	sdate = date.split("-")
        year = sdate[0]
       	month = sdate[1].lstrip('0')
        day = sdate[2].lstrip('0')

	tw_year = int(year) - 1911
	tw_date = month + day


	# only accept tw years from 91 to 107
	if((tw_year < 91) or (tw_year > 107)):
		print("Error: year is out of range")
		return(-1)


	print(tw_year)
	print(tw_date)

	header={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gekko) Chrom/67.0.3396.87 Safari/537.36'}
	payload = {'queryYear': tw_year, 'submitBtn': '%E6%9F%A5%E8%A9%A2'}
	url = "http://www.twse.com.tw/zh/holidaySchedule/holidaySchedule"
	#resp = requests.post('http://www.twse.com.tw/zh/holidaySchedule/holidaySchedule', headers=header, data=payload)
	resp = rand_proxy.htmlRequest(url, "post", payload)
	table = pd.read_html(resp.text, header=0)[0]
	offDate = []
	for i in xrange(len(table)):
		date = table.iloc[i][1]

		noBrkt = removeBracket(date)
		noYear = removeYear(noBrkt)

		listDate, isTrade = checkTradeDate(noYear, tw_date, fullcheck)
		offDate.extend(listDate)
		if((isTrade == False) and (fullcheck == True)):
			print("NOT A TRADE DATE")
			print(offDate)
			return(0)
	

	if(fullcheck == False):
		AllYear[int(year)] = offDate

	print(offDate)
	return(1)


def buildTradeDate():
	today = datetime.datetime.today().strftime('%Y-%m-%d')
	sdate = today.split("-")
	year = sdate[0]
	startYear = int(sdate[0]) - 5

	for i in range(startYear, int(year) + 1):
		print("build year: " + str(i))
		res = isTradeDate(str(i) + "-1-1", False)
		if(res != 1):
			print("ERROR buildTradeDate year: [" + str(i) + "]")

	print(AllYear)

def checkStoreYear(date):
	sdate = date.split("-")
	year = sdate[0]
	md = str(int(sdate[1])) + str(int(sdate[2]))

	key = int(year)
	if key in AllYear:
		if md in AllYear[key]:
			return(0)
		else:
			return(1)
	else:
		return(-1)


def isWeekend(date):
	sdate = date.split("-")
	year = sdate[0]
	month = sdate[1]
	day = sdate[2]

	# Input: year, month, day, Output: the day of the week (0 is Monday)
	weekday = calendar.weekday(int(year), int(month), int(day))
	if((weekday == 6) or (weekday == 7)):
		return(True)
	else:
		return(False)

def validDate(strDate):
         try:
                 datetime.datetime.strptime(strDate, '%Y-%m-%d')
		 return(True)
         except ValueError:
                 print("valid_date: Incorrect DATE format, should be YYYY-MM-DD")
		 return(False)


if __name__ == '__main__':
	buildTradeDate()
	#isTradeDate("2018-3-01")
	#isWeekend(str(sys.argv[1]))

