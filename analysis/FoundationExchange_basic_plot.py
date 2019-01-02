#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# 外資買入/ 賣出, 投信買入/賣出, 自然人買入/賣出
# ForeignInvestBuy/Sell， InvestmentTrustBuy/Sell， DealerBuy/Sell
#

import sys
sys.path.insert(0, '/home/thomaschen/tmp/stock_query')

import numpy as np
import matplotlib
#matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import datetime
import mpld3
import pandas as pd


from scipy.interpolate import spline
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter
from matplotlib.font_manager import *
from dateutil import parser
from db import add_db_record




def main(stockid, sdate, edate, opt):
	global cursor
	foreign_buy = []
	foreign_sell = []
	trust_buy = []
	trust_sell = []
	dealer_buy = []
	dealer_sell = []
	idate = []


	try:
		db = add_db_record.ConnectDB("localhost", "stock", "ftdi1234")
		cursor = db.cursor()

		# DB Columns are:
		# 0@FexId (table's unique id), 1@CoId (company id) 2@Foreign_Investor_buy, 
		# 3@Foreign_Investor_sell, 4@Investment_Trust_buy, 5@Investment_Trust_sell, 
		# 6@Dealer_buy, 7@Dealer_sell, 8@Total, 9@Category, 10@Date
		cursor.execute( \
			"SELECT * FROM FoundationExchange WHERE CoId = (SELECT CoId from Company WHERE StockID = %s) AND \
				Date BETWEEN %s AND %s ORDER BY Date ASC", (stockid, sdate, edate,))
		data = cursor.fetchall()
		if(cursor.rowcount <= 0):
			print("StockExchange_plot: Error: No DATA " + str(cursor.rowcount))
			return(-1)


		for row in data:
			print(row)
			foreign_buy.append(row[2])
			foreign_sell.append(row[3])
			trust_buy.append(row[4])
			trust_sell.append(row[5])
			dealer_buy.append(row[6])
			dealer_sell.append(row[7])
			idate.append(parser.parse(row[10]))

		dates = [mdates.date2num(t) for t in idate]

		cursor.execute("SELECT CompanyName FROM Company WHERE StockID = %s", (stockid,))
		row = cursor.fetchall()
		if(cursor.rowcount <= 0):
			print("StockExchange_plot: Error: Cannot find Company Name " + str(cursor.rowcount))
			figTitle = u'股票交易資訊' + "	  STOCK: [" + stockid + "]"
		else:
			figTitle = u'股票交易資訊' + "	  " + row[0][0] + ": [" + stockid + "]"

		#fig, ax1 = plt.subplots(1, 1, sharex=True, gridspec_kw={'height_ratios': [1]}, figsize = (12,8))
		#fig, ax1 = plt.subplots(1, 1, sharex=True, figsize = (12,8))
		fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, gridspec_kw={'height_ratios': [1,1,1]}, figsize = (12,10))
		fontP = FontProperties(fname="/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc")
		fig.suptitle(figTitle, fontproperties=fontP)
		
		date_format = '%Y-%m-%d'
		start = datetime.datetime.strptime(sdate, date_format)
		end = datetime.datetime.strptime(edate, date_format)
		tdelta = end - start
		print(tdelta.days)

		# Configure x-ticks according to number of days
		ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
		ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
		ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
		if(tdelta.days > 547):
			ax1.xaxis.set_major_locator(mdates.MonthLocator())
			ax1.xaxis.set_minor_locator(MonthLocator(bymonthday=1, interval=3))
			ax2.xaxis.set_major_locator(mdates.MonthLocator())
			ax2.xaxis.set_minor_locator(MonthLocator(bymonthday=1, interval=3))
			ax3.xaxis.set_major_locator(mdates.MonthLocator())
			ax3.xaxis.set_minor_locator(MonthLocator(bymonthday=1, interval=3))
		elif(182 < tdelta.days < 547):
			ax1.xaxis.set_major_locator(mdates.MonthLocator())
			ax1.xaxis.set_minor_locator(MonthLocator(bymonthday=1, interval=1))
			ax2.xaxis.set_major_locator(mdates.MonthLocator())
			ax2.xaxis.set_minor_locator(MonthLocator(bymonthday=1, interval=1))
			ax3.xaxis.set_major_locator(mdates.MonthLocator())
			ax3.xaxis.set_minor_locator(MonthLocator(bymonthday=1, interval=1))
		else:
			ax1.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=MO))
			ax1.xaxis.set_minor_locator(mdates.DayLocator())
			ax2.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=MO))
			ax2.xaxis.set_minor_locator(mdates.DayLocator())
			ax3.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=MO))
			ax3.xaxis.set_minor_locator(mdates.DayLocator())


		# Plot on left Y axis
		#ax1.set_ylabel("Number of Shares")
		#ax2.set_ylabel("Number of Shares")
		#ax3.set_ylabel("Number of Shares")
		
		volume_dict = {
						'foreign_buy': foreign_buy,
						'foreign_sell': foreign_sell,
						'trust_buy': trust_buy,
						'trust_sell': trust_sell,
						'dealer_buy': dealer_buy,
						'dealer_sell': dealer_sell
					}

		volume_scale_dict = {
								'foreign_buy': None,
								'foreign_sell': None,
								'trust_buy': None,
								'trust_sell': None,
								'dealer_buy': None,
								'dealer_sell': None
							}

		#for k in volume_dict:
		#	if(max(volume_dict[k]) > 1000000):
		#		volume_scale_dict[k] = 'M'
		#		volume_dict[k][:] = [x/1000000 for x in volume_dict[k]]
		#	elif(max(volume_dict[k]) > 1000):
		#		volume_scale_dict[k] = 'K'
		#		volume_dict[k][:] = [x/1000 for x in volume_dict[k]]
			
		foreign_buy_scale = None
		#if(max(foreign_buy) > 1000000):
		#	foreign_buy_scale = 'M'
		#	foreign_buy[:] = [x/1000000 for x in foreign_buy]
		#elif(max(foreign_buy) > 1000):
		#	foreign_buy_scale = 'K'
		#	foreign_buy[:] = [x/1000 for x in foreign_buy]

		ax1_volume_title = 'Number of Shares (%s)' % volume_scale_dict['foreign_buy']
		ax1.set_ylabel(ax1_volume_title)
		ax2.set_ylabel('Number of Shares (%s)' % volume_scale_dict['trust_buy'])
		ax3.set_ylabel('Number of Shares (%s)' % volume_scale_dict['dealer_buy'])

		# trying to smooth out the curve here, but not much differences
		#y_sm = np.array(foreign_buy)
		#x_sm = np.array(dates)
		#x_smooth = np.linspace(x_sm.min(), x_sm.max(), 800)
		#y_smooth = spline(dates, foreign_buy, x_smooth)
		#ax1.plot(x_smooth, y_smooth, 'red', linewidth=1)

		#ax1.bar(dates, foreign_buy, 0.5, label="Foreign Buy", color='r')
		#ax1.bar(dates, foreign_sell, 0.5, label="Foreign Sell", color='b')
		
		# using rolloing to se the trends
		#rforeign_buy = pd.DataFrame({'Foreigh Buy':foreign_buy})
		#rforeign_buy = rforeign_buy.rolling(8).mean()
		ax1.plot_date(dates, foreign_buy, '-', label="Foreign Buy", color='r')
		ax1.plot_date(dates, foreign_sell, '-', label="Foreign Sell", color='b')
		#ax1.plot_date(dates, rforeign_buy, '-', label="Foreign Sell", color='b')


		ax2.plot_date(dates, trust_buy, '-', label="Investor Buy", color='y')
		ax2.plot_date(dates, trust_sell, '-', label="Investor Sell", color='m')

		ax3.plot_date(dates, dealer_buy, '-', label="Dealer Buy", color='g')
		ax3.plot_date(dates, dealer_sell, '-', label="Dealer Sell", color='k')

		#Format the x-axis for dates (label formatting, rotation)
		fig.autofmt_xdate(rotation=60)
		#fig.tight_layout()

		# Show grids and legends
		ax1.grid(True)
		ax1.legend(loc='best', framealpha=0.5)
		ax2.grid(True)
		ax2.legend(loc='best', framealpha=0.5)
		ax3.grid(True)
		ax3.legend(loc='best', framealpha=0.5)


		plt.show()
		#plt.savefig("/var/www/script/figure.png")
		#res = mpld3.save_html(fig)
		#mpld3.display(fig)
		#jf = open("/var/www/script/foundation.js", "w")
		#res = mpld3.fig_to_html(fig, "fig.hmtl")
		#print(res)
		#jf.write(res)
		#jf.close()
		#mpld3.show()

		#return(res)

	except Exception as e:
		print(e)
		raise Exception


if __name__ == '__main__':
	#main("1301")
	main("1301", "2016-11-01", "2017-12-11", "year")

