#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#
# 融資融卷 (Margin Trading and Short Selling)
#
# [margin_buy 融資買入] [margin_sell 融資賣出] [margin_remain 融資餘額]
# [short_sale_buy 融卷買入] [short_sale_sell 融卷賣出] [short_sale_remain 融卷餘額]

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

from dateutil import parser
from db import add_db_record
import datetime



# Function to plot 6 graphs, 
# margin_buy, margin_sell, margin_remain, 
# short_sale_buy, short_sale_sell, short_sale_remain
# stockid: stock number in string
# sdate: start date of data to see
# edate: end date of data to see
# stick: type of plot, by "day", "month" or "year"
def main(stockid, sdate, edate, stick):

	# Make DB access to retrive data
	# Table StockExchang has following colums in roder:
	# 2@margin_buy, 3@margin_sell, 4@margin_remain,
	# 5@short_sale_buy, 6@short_sale_sell, 7@short_sale_remain
	# 8@TotalVolume, 9@ChargeOff, 10@Category, 11@Date
	#
	db = add_db_record.ConnectDB("localhost", "stock", "ftdi1234")
	cursor = db.cursor()
	
	cursor.execute( \
			"SELECT * FROM `MarginTrading` WHERE CoId = (SELECT CoId from Company WHERE StockID = %s) \
				AND Date BETWEEN %s AND %s ORDER BY Date ASC", (stockid, sdate, edate,))
	data = cursor.fetchall()
	if(cursor.rowcount <= 0):
		print("StockExchange_plot: Error: No DATA " + str(cursor.rowcount))
		return(-1)


	print(data)

	df = pd.DataFrame(index=pd.date_range(sdate, edate))

	#df['Date'] = [mdates.date2num(parser.parse(str(t))) for t in df['Date']]
	df['Date'] = df.index.tolist()
	df['Date'] = pd.to_datetime(df['Date'])
	df["Date"] = df["Date"].apply(mdates.date2num)

	df['Margin Buy'] = [0] * df.shape[0]
	df['Margin Sell'] = [0] * df.shape[0]
	df['Margin Balance'] = [0] * df.shape[0]
	df['Stock Short Buy'] = [0] * df.shape[0]
	df['Stock Short Sell'] = [0] * df.shape[0]
	df['Stock Short Balance'] = [0] * df.shape[0]

	# Date is the index, using date to copy values
	for row in data:
		df.loc[row[11], 'Margin Buy'] = row[2]
		df.loc[row[11], 'Margin Sell'] = row[3]
		df.loc[row[11], 'Margin Balance'] =  row[4]
		df.loc[row[11], 'Stock Short Buy'] = row[5]
		df.loc[row[11], 'Stock Short Sell'] = row[6]
		df.loc[row[11], 'Stock Short Balance'] = row[7]

	plot_df = df[['Date', 'Margin Buy', 'Margin Sell', 'Margin Balance',
				'Stock Short Buy', 'Stock Short Sell', 'Stock Short Balance']].copy()

	# 券資比 = (融券餘額 / 融資餘額) * 100%
	plot_df['Balance Ratio'] = (plot_df['Stock Short Balance']/plot_df['Margin Balance']) * 100

	# Fill 0 instead of NaN
	plot_df['Balance Ratio'].fillna(value=0, inplace=True) 

	#print(df.groupby(df.index.strftime("%m%d")).sum())

	# Group by Year and Month
	# print(df.groupby(df.index.strftime("%y%m")).sum())

	# Group by the numeric day of the year 
	# print(df.groupby(df.index.strftime("%j")).mean())
	# print(df.groupby(df.index.strftime("%m%d")).mean())

	cursor.execute("SELECT CompanyName FROM Company WHERE StockID = %s", (stockid,))
	row = cursor.fetchall()
	if(cursor.rowcount <= 0):
		print("StockExchange_plot: Error: Cannot find Company Name " + str(cursor.rowcount))
		figTitle = u'股票交易資訊' + "    STOCK: [" + stockid + "]"
	else:
		figTitle = u'股票交易資訊' + "    " + row[0][0] + ": [" + stockid + "]"

	
	# Construct all the plots
	ax = []
	fig, ax = plt.subplots(4, 1, sharex=True, gridspec_kw={'height_ratios': [1,1,1,1]}, figsize = (12,10))
	#fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6, 1, sharex=True, gridspec_kw={'height_ratios': [1,1,1,1,1,1]}, figsize = (12,10))
	fig.autofmt_xdate(rotation=60)
	
	# Tick on mondays every week, if monthly, then use "mdates.MonthLocator()"
	ax[0].xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=MO))
	ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
	ax[0].xaxis.set_minor_locator(mdates.DayLocator())

	for ap in ax:
		ap.set_ylabel('Volume', size=10)
		ap.xaxis.grid(False)

	# Setup font manager to display Chinese characters
	fontP = FontProperties(fname="/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc")

	ax[0].plot(plot_df["Date"], plot_df["Margin Buy"], color = 'b', label = "Margin Buy(" + u'融資買入' + ")")
	ax[0].plot(plot_df["Date"], plot_df["Margin Sell"], color = 'm', label = "Margin Sell(" + u'融資賣出)' + ")")
	ax[2].plot(plot_df["Date"], plot_df["Margin Balance"], color = 'r', label = "Margin Balance(" + u'融資餘額)' + ")")
	ax[1].plot(plot_df["Date"], plot_df["Stock Short Buy"], color = 'k', label = "Stock Short Buy(" + u'融卷買入)' + ")")
	ax[1].plot(plot_df["Date"], plot_df["Stock Short Sell"], color = 'y', label = "Stock Short Sell(" + u'融卷賣出)' + ")")
	ax[2].plot(plot_df["Date"], plot_df["Stock Short Balance"], color = 'g', label = "Stock Short Balance(" + u'融卷餘額)' + ")")
	ax[3].plot(plot_df["Date"], plot_df["Balance Ratio"], color = 'b', label = "Stock Short Balance(" + u'券資比)' + ")")


	# Show legend, only be done after above "label" is configured
	for ap in ax:
		ap.legend(loc='best', fancybox=True, framealpha=1, shadow=True, borderpad=1, prop=fontP)

	fig.suptitle(figTitle, fontproperties=fontP)
	plt.axis('tight')
	plt.show()



if __name__ == '__main__':
	main("1316", "2018-11-01", "2018-12-11", "year")

