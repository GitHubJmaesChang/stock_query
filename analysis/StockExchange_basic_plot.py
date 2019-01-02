#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '/home/thomaschen/tmp/stock_query')

import numpy as np
import pandas as pd
import matplotlib
#matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
from matplotlib.font_manager import *
from mpl_finance import candlestick_ohlc

from dateutil import parser
from db import add_db_record
import datetime



# Function to plot Candle Stick OHLC (Open, High, Low, Closing price)
# stockid: stock number in string
# sdate: start date of data to see
# edate: end date of data to see
# stick: type of plot, by "day", "month" or "year"
def main(stockid, sdate, edate, opt):

	# Make DB access to retrive data
	# Table StockExchang has following colums in roder:
	# 0@ExcId, 1@CoId, 2@ExchangVolume, 3@StartPrice
	# 4@HighPrice, 5@LowPrice, 6@EndPrice, 7@Category, 8@Date
	db = add_db_record.ConnectDB("localhost", "stock", "ftdi1234")
	cursor = db.cursor()
	
	cursor.execute( \
			"SELECT * FROM `StockExchange` WHERE CoId = (SELECT CoId from Company WHERE StockID = %s) \
				AND Date BETWEEN %s AND %s ORDER BY Date ASC", (stockid, sdate, edate,))
	data = cursor.fetchall()
	if(cursor.rowcount <= 0):
		print("StockExchange_plot: Error: No DATA " + str(cursor.rowcount))
		return(-1)


	# d = pandas.date_range(start='1/1/1980', end='11/1/1990', freq='MS')	 
	# freq: [M] month end frequency, [MS] month start frequency
	#		[A, Y] year end frequency, [AS, YS] year start frequency
	ohlc = pd.DataFrame(index=pd.date_range(sdate, edate))

	#ohlc['Date'] = [mdates.date2num(parser.parse(str(t))) for t in ohlc['Date']]
	ohlc['Date'] = ohlc.index.tolist()
	ohlc['Date'] = pd.to_datetime(ohlc['Date'])
	ohlc["Date"] = ohlc["Date"].apply(mdates.date2num)

	ohlc['Open Price'] = [0] * ohlc.shape[0]
	ohlc['Close Price'] = [0] * ohlc.shape[0]
	ohlc['High Price'] = [0] * ohlc.shape[0]
	ohlc['Low Price'] = [0] * ohlc.shape[0]
	ohlc['Volume'] = [0] * ohlc.shape[0]

	# Date is the index, using date to copy values
	for row in data:
		ohlc.loc[row[8], 'Open Price'] = row[3]
		ohlc.loc[row[8], 'Close Price'] = row[6]
		ohlc.loc[row[8], 'High Price'] =  row[4]
		ohlc.loc[row[8], 'Low Price'] = row[5]
		ohlc.loc[row[8], 'Volume'] = row[2]

	print(ohlc)

	df = ohlc[['Date', 'Open Price', 'High Price', 'Low Price','Close Price']].copy()
	df_bar = ohlc[['Volume']].copy()

	#print(df.groupby(df.index.strftime("%m%d")).sum())

	# Group by Year and Month
	# print(df.groupby(df.index.strftime("%y%m")).sum())

	# Group by the numeric day of the year 
	# print(df.groupby(df.index.strftime("%j")).mean())
	# print(df.groupby(df.index.strftime("%m%d")).mean())
	
	#f1, ax = plt.subplots(figsize = (10,5))
	#fig = plt.figure()
	#ax = fig.add_subplot(1,1,1)
	fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [3,1]})
	fig.autofmt_xdate(rotation=60)
	ax1.set_ylabel('Price', size=10)
	
	# Tick on mondays every week, if monthly, then use "mdates.MonthLocator()"
	ax1.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=MO))
	ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
	ax1.xaxis.set_minor_locator(mdates.DayLocator())

	cursor.execute("SELECT CompanyName FROM Company WHERE StockID = %s", (stockid,))
	row = cursor.fetchall()
	if(cursor.rowcount <= 0):
		print("StockExchange_plot: Error: Cannot find Company Name " + str(cursor.rowcount))
		figTitle = u'股票交易資訊' + "    STOCK: [" + stockid + "]"
	else:
		figTitle = u'股票交易資訊' + "    " + row[0][0] + ": [" + stockid + "]"


	fontP = FontProperties(fname="/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc")
	fig.suptitle(figTitle, fontproperties=fontP)

	#print(df.values)
	candlestick_ohlc(ax1, df.values, width=.6, colorup='red', colordown='green')

	# Followiong is to draw using DataFrame 
	#candlestick_ohlc(ax, list(zip(ohlc["Date"].tolist(), ohlc["Open Price"].tolist(), ohlc["High Price"].tolist(),
	#				   ohlc["Low Price"].tolist(), ohlc["Close Price"].tolist())),width=.6, colorup='green', colordown='red' )


	# Create SMA: Simple Moving Average
	#df["SMA200"] = df["Close Price"].rolling(20).mean()

	#print(df["SMA200"])
	#ax1.plot(ohlc["Date"], df["SMA200"], color = 'blue', label = 'SMA200')

	# Plot volume
	# Set M/K for the volume
	ax2.set_ylabel('Volume', size=10)
	volume = df_bar['Volume']
	volume_scale = None
	scaled_volume = volume
	if volume.max() > 1000000:
		volume_scale = 'M'
		scaled_volume = volume/1000000
	elif volume.max() > 1000:
		volume_scale = 'K'
		scaled_volume = volume/1000
	
	# Set color according to candlestick: colorup='red', colordown='green'
	color_data = []
	for vopen, vclose in zip(df["Open Price"], df["Close Price"]):
		if(vopen > vclose):
			color_data.append('g')
		else:
			color_data.append('r')
	
	# do plot
	ax2.bar(df['Date'], scaled_volume, color=color_data, width=.6, align='center')
	if volume_scale:
		volume_title = 'Volume (%s)' % volume_scale
	
	#ax2.set_title("Volume")
	ax2.xaxis.grid(False)

	plt.show()



if __name__ == '__main__':
	main("1316", "2018-11-01", "2018-12-11", "year")

