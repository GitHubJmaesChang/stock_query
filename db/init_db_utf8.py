#!/usr/bin/python
# -*- coding: utf_8 -*-

import MySQLdb as MS
import datetime
import warnings


def dbgPrint(s):
	ts = str(datetime.datetime.now())
	print("[" + ts + "]:" + str(s))

def InitDB():
	db = MS.connect(host="localhost",  # the host
		user="root",       # username
		passwd="1234",
		charset='utf8',
		use_unicode=True)

	cursor = db.cursor()

	dbgPrint(db)

	# create db
	try:
		dbgPrint("Create database stock")
		sql = 'CREATE DATABASE IF NOT EXISTS stock'

		# We don't care if the db already exists and this was a no-op
		warnings.filterwarnings('ignore', category=MS.Warning)
		cursor.execute(sql)
		warnings.resetwarnings()

		# switch to the newly created database
		cursor.execute("USE stock")

	except MS.Error as e:
		dbgPrint("Error: unable to create database [" + str(e) + "]")
		db.close()
		return(-1)
	except MS.Warning as wrn:
		dbgPrint("Warning: create database [" + str(wrn) + "]")
		db.close()
		return(-1)


	# create tables
	print("Create Tables")
	res = CreatFinancialTable(db)
	db.close()
	if res < 0:
		return(-1)

	return(0)


def CreatFinancialTable(db):

	try:
		cursor = db.cursor()

		print("Create Company Table")
		# Table: Company 
		# 公司代號, 公司名稱
		# colums are created in the order as listed above.
		cursor.execute("create table IF NOT EXISTS Company( \
				CoId INT AUTO_INCREMENT PRIMARY KEY, \
				StockID INT NOT NULL, \
				CompanyName varchar(100) \
				) DEFAULT CHARSET=utf8 ENGINE=INNODB \
			") 


		print("Create FinancialStatement Table")
		# Table: FinancialStatement
		# 資產總額/總計, 權益總額/總計
		# colums are created in the order as listed above.
		cursor.execute("create table IF NOT EXISTS FinancialStatement( \
			FinId INT AUTO_INCREMENT PRIMARY KEY, \
			CoId INT NOT NULL, \
			TotalAsset BIGINT, \
			TotalEquity BIGINT, \
			Date varchar(20), \
			FOREIGN KEY (CoId) REFERENCES Company(CoId) \
			) DEFAULT CHARSET=utf8 ENGINE=INNODB \
			")


		print("Create IncomeStatment Table")
		# Table: IncomeStatment
		# 營業收入,營業利益(損失), 本期淨利(淨損), 營業外收入及支出, 稅前淨利(淨損)
		cursor.execute("create table IF NOT EXISTS IncomeStatement( \
			InId INT AUTO_INCREMENT PRIMARY KEY, \
			CoId INT NOT NULL, \
			OpRevenue BIGINT, \
			OpProfit BIGINT, \
			NetIncome BIGINT, \
			NonOpRevenueExpense BIGINT, \
			RevenueBeforeTax BIGINT, \
			Date varchar(20), \
			FOREIGN KEY (CoId) REFERENCES Company(CoId) \
			) DEFAULT CHARSET=utf8 ENGINE=INNODB \
			")

		print("Create CalStatment Table")
		# Table: CalStatment (Calculated Statment)
		# 基本每股盈餘, 每股參考淨值, ROE, ROA
		cursor.execute("create table IF NOT EXISTS CalStatement( \
			CalId INT AUTO_INCREMENT PRIMARY KEY, \
			CoId INT NOT NULL, \
			EarningPerShare DOUBLE, \
			NetAssetPerShare DOUBLE, \
			ROE DOUBLE, \
			ROA DOUBLE, \
			Date varchar(20), \
			FOREIGN KEY (CoId) REFERENCES Company(CoId) \
			) DEFAULT CHARSET=utf8 ENGINE=INNODB \
			")


		print("Create Stock excahnge Table")
		# Table: CalStatment (Calculated Statment)
		# 成交量, 開盤價格, 盤中最高價, 盤中最低價, 收盤價, 日期
		cursor.execute("create table IF NOT EXISTS StockExchange( \
			ExcId INT AUTO_INCREMENT PRIMARY KEY, \
			CoId INT NOT NULL, \
			ExchangeVolume BIGINT, \
			StartPrice DOUBLE, \
			HighPrice DOUBLE, \
			LowPrice DOUBLE, \
			EndPrice DOUBLE, \
			Date varchar(20), \
			FOREIGN KEY (CoId) REFERENCES Company(CoId) \
			) DEFAULT CHARSET=utf8 ENGINE=INNODB \
			")

		print("Create foundation excahnge Table")
		# Table: FoundationExchange
		# 外資買入, 外資賣出, 投信商買入, 投信商賣出, 自營商買入, 自營商賣出, 當日總量, 日期    
		cursor.execute("create table IF NOT EXISTS FoundationExchange( \
			FexId INT AUTO_INCREMENT PRIMARY KEY, \
			CoId INT NOT NULL, \
			ForeignInvestorBuy BIGINT, \
			ForeignInvestorSell BIGINT, \
			InvestmentTrustBuy BIGINT, \
			InvestmentTrustSell BIGINT, \
			DealerBuy BIGINT, \
			DealerSell BIGINT, \
			TotalVolume BIGINT, \
			Date varchar(20), \
			FOREIGN KEY (CoId) REFERENCES Company(CoId) \
			) DEFAULT CHARSET=utf8 ENGINE=INNODB \
			")

		print("Create Month FoundationExchange Table")
		# Table: MonthRevenue
		#當月營收,上月營收,去年當月營收,上月比較增減(%),去年同月增減(%),當月累計營收,去年累計營收,前期比較增減(%)

		cursor.execute("create table IF NOT EXISTS MonthlyRevenue( \
                        MReId INT AUTO_INCREMENT PRIMARY KEY, \
			CoId INT NOT NULL, \
			MonthlyRevenue BIGINT, \
			LastMonthlyRevenue BIGINT, \
			LastYearMonthlyRevenue BIGINT, \
			MonthlyIncreaseRevenue DOUBLE, \
			LastYearMonthlyIncreaseRevenue DOUBLE, \
			CumulativeRevenue BIGINT, \
			LastYearCumulativeRevenue BIGINT, \
			CompareCumulativeRevenue DOUBLE, \
			Date varchar(20), \
			FOREIGN KEY (CoId) REFERENCES Company(CoId) \
			) DEFAULT CHARSET=utf8 ENGINE=INNODB \
			")

		print("Create Month MarginTrading Table")
                #融資買入, 融資賣出, 融資餘額, 融卷買入, 融卷賣出, 融卷餘額,
		cursor.execute("create table IF NOT EXISTS MarginTrading( \
                        MrevId INT AUTO_INCREMENT PRIMARY KEY, \
			CoId INT NOT NULL, \
			MarginBuy BIGINT, \
			MarginSell BIGINT, \
			MarginRemine BIGINT, \
			ShortSellBuy DOUBLE, \
			ShortSellSell DOUBLE, \
			ShortSellRemine BIGINT, \
			TotalVolume DOUBLE, \
			ChargeOff BIGINT, \
			Date varchar(20), \
			FOREIGN KEY (CoId) REFERENCES Company(CoId) \
			) DEFAULT CHARSET=utf8 ENGINE=INNODB \
			")


	except MS.Error as e:
		dbgPrint("Error: unable to create tables [" + str(e) + "]")
		return(-1)
	except MS.Warning as wrn:
		dbgPrint("Warning: create tables [" + str(wrn) + "]")
		return(-1)

if  __name__ == '__main__':
        InitDB()
