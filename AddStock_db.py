#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import pandas as pd
import time


from db import init_db_utf8
from db import add_db_record

comp_id   = 'comp_id.csv'
File_Path = "D:/Stock/finacial/"


def check_file_exist(filename):
	if(os.path.isfile(filename)):
		return (1)
	else:
		return (0)


# crate database : 
def intial_db():
	init_db_utf8.InitDB("localhost", "root", "1234")
	add_db_record.ConnectDB("localhost", "stock", "1234")

# insert base_financail report into data base :

def database_InsertCompany(name_id, name):
	print("company ID = " + name_id + " name = " + name)
	add_db_record.InsertCompany((name_id), (name) )

def database_InsertFinancialStatement(stockID, asset, equity, date):
	add_db_record.InsertFinancialStatement((stockID), asset, equity, date)

def database_InsertIncomeStatement(stockid, oprevenu, opprofit, netincome, \
			nonoprevenueexpense, revenuebeforetax, date):

	add_db_record.InsertIncomeStatement((stockid), oprevenu, opprofit, netincome, \
			nonoprevenueexpense, revenuebeforetax, date)

def database_InsertCalStatement(stockid, eps, netaps, roe, roa, date):
	add_db_record.InsertCalStatement((stockid), eps, netaps, roe, roa, date)


# Function to return non float string.
# Numbers are read from CSV files as floating numbers.
# For empty data, -1 is used, and it is read as -1.0. This function
# is to transform -1.0 to int -1 for inserting into the database.
def fstr(x):
	try:
		if(x is None):
			x = 0

		i = (str(x)[-2:] == '.0' and str(x)[:-2] or str(x))
	
		print("fstr (DEBUG): Input[" + str(x) + "] Output[" + i + "]")
		
		return(i)
	except Exception as e:
		print("fstr (ERROR): Exception")
		print(e)
		return("0")


def insertFinancailSeate_to_database(path, date, quarterly):

	sdate = date.split("-")
	year = sdate[0]
	month = sdate[1]
	day = sdate[2]
	
	file_name = str(year) + "_"+ str(quarterly) + "_financialStatement.csv"
	
	intial_db()

	print("Process file: [" + file_name + "]")

	if((0) == check_file_exist(path + file_name)):
		print(("insertFinancailSeate_to_database : No such file name : "), file_name)
		return (0)

	table = pd.read_csv(path + file_name)
	for idx in range(0, table.shape[0]):
		database_InsertCompany(str(table.iloc[idx]['Name']), str(table.iloc[idx]['ID']))

		database_InsertFinancialStatement(str(table.iloc[idx]['公司代號']),str(table.iloc[idx]['資產總計']), \
								  str(table.iloc[idx]['權益總計']),date)

		database_InsertIncomeStatement(str(table.iloc[idx]['公司代號']), str(table.iloc[idx]['營業收入']), \
								str(table.iloc[idx]['營業利益(損失)']), str(table.iloc[idx]['本期淨利(淨損)']), \
								str(table.iloc[idx]['營業外收入及支出']), str(table.iloc[idx]['稅前淨利(淨損)']), \
								date)
		
		database_InsertCalStatement(str(table.iloc[idx]['公司代號']),str(table.iloc[idx]['基本每股盈餘(元)']), \
								str(table.iloc[idx]['每股參考淨值']),str(table.iloc[idx]['ROE']), \
								str(table.iloc[idx]['ROA']), date)



def insertCompanyFinancialStatement(path, date, quarterly, stock_type):

        sdate = date.split("-")
        year = sdate[0]
        month = sdate[1]
        day = sdate[2]

        file_name = str(year) + "_"+ str(quarterly)

        if(stock_type == "TWSE"):
                file_name +=  "_TWSE_financialStatement.csv"
        else:
                file_name +=  "_TPEX_financialStatement.csv"


        intial_db()

        print("Process file: [" +path + file_name + "]")

        if((0) == check_file_exist(path + file_name)):
                print(("insertFinancailSeate_to_database : No such file name : "), file_name)
                return (0)

        table = pd.read_csv(path + file_name)

        balance_sheet = ["0"]*64 
        Income_sheet  = ["0"]*64 
        Cash_sheet    = ["0"]*64
        valueable_sheet   = ["0.0"]*64

        for idx in range(0, table.shape[0]):
                database_InsertCompany(str(table.iloc[idx]['ID']), str(table.iloc[idx]['Name']) )
                
                balance_sheet[0] = str(table.iloc[idx]['現金及約當現金'])
                balance_sheet[1] = str(table.iloc[idx]['應收票據淨額'])
                balance_sheet[2] = str(table.iloc[idx]['應收帳款淨額'])
                balance_sheet[3] = str(table.iloc[idx]['應收帳款－關係人淨額'])
                balance_sheet[4] = str(table.iloc[idx]['其他應收款'])
                balance_sheet[5] = str(table.iloc[idx]['其他應收款－關係人'])
                balance_sheet[6] = str(table.iloc[idx]['存貨'])
                balance_sheet[7] = str(table.iloc[idx]['預付款項'])
                balance_sheet[8] = str(table.iloc[idx]['流動資產合計'])
                balance_sheet[9] = str(table.iloc[idx]['非流動資產合計'])
                balance_sheet[10] = str(table.iloc[idx]['資產總計'])
                balance_sheet[11] = str(table.iloc[idx]['短期借款'])
                balance_sheet[12] = str(table.iloc[idx]['應付帳款'])
                balance_sheet[13] = str(table.iloc[idx]['應付帳款－關係人'])
                balance_sheet[14] = str(table.iloc[idx]['其他應付款'])
                balance_sheet[15] = str(table.iloc[idx]['流動負債合計'])
                balance_sheet[16] = str(table.iloc[idx]['長期借款'])
                balance_sheet[17] = str(table.iloc[idx]['非流動負債合計'])
                balance_sheet[18] = str(table.iloc[idx]['負債總計'])
                balance_sheet[19] = str(table.iloc[idx]['普通股股本'])
                balance_sheet[20] = str(table.iloc[idx]['權益總額'])
                balance_sheet[21] = str(table.iloc[idx]['負債及權益總計'])
                print (balance_sheet)
                print (str(table.iloc[idx]['ID']))
                add_db_record.InsertBalanceSheet(str(table.iloc[idx]['ID']), balance_sheet, date)

                Income_sheet[0] = str(table.iloc[idx]['營業收入合計'])
                Income_sheet[1] = str(table.iloc[idx]['營業成本合計'])
                Income_sheet[2] = str(table.iloc[idx]['營業毛利（毛損）淨額'])
                Income_sheet[3] = str(table.iloc[idx]['推銷費用'])
                Income_sheet[4] = str(table.iloc[idx]['管理費用'])
                Income_sheet[5] = str(table.iloc[idx]['研究發展費用'])
                Income_sheet[6] = str(table.iloc[idx]['其他費用'])
                Income_sheet[7] = str(table.iloc[idx]['營業費用合計'])
                Income_sheet[8] = str(table.iloc[idx]['營業利益（損失）'])
                Income_sheet[9] = str(table.iloc[idx]['營業外收入及支出合計'])
                Income_sheet[10] = str(table.iloc[idx]['繼續營業單位稅前淨利（淨損）'])
                Income_sheet[11] = str(table.iloc[idx]['本期淨利（淨損）'])
                Income_sheet[12] = str(table.iloc[idx]['母公司業主（淨利／損）'])

                add_db_record.InsertIncomeStatementSheet(str(table.iloc[idx]['ID']), Income_sheet, date)

                Cash_sheet[0] = str(table.iloc[idx]['營業活動之淨現金流入（流出）'])
                Cash_sheet[1] = str(table.iloc[idx]['投資活動之淨現金流入（流出）'])
                Cash_sheet[2] = str(table.iloc[idx]['籌資活動之淨現金流入（流出）'])
                Cash_sheet[3] = str(table.iloc[idx]['匯率變動對現金及約當現金之影響'])
                Cash_sheet[4] = str(table.iloc[idx]['本期現金及約當現金增加（減少）數'])
                Cash_sheet[5] = str(table.iloc[idx]['期初現金及約當現金餘額'])
                Cash_sheet[6] = str(table.iloc[idx]['期末現金及約當現金餘額'])

                add_db_record.InsertCashStatementSheet(str(table.iloc[idx]['ID']), Cash_sheet, date)

                valueable_sheet[0] = fstr(table.iloc[idx]['母公司淨利比例'])
                valueable_sheet[1] = fstr(table.iloc[idx]['業外占營收比例'])
                valueable_sheet[2] = fstr(table.iloc[idx]['存貨周轉率'])
                valueable_sheet[3] = fstr(table.iloc[idx]['毛利率'])
                valueable_sheet[4] = fstr(table.iloc[idx]['營業利益'])
                valueable_sheet[5] = fstr(table.iloc[idx]['淨利率'])
                valueable_sheet[6] = fstr(table.iloc[idx]['ROE_Org'])
                valueable_sheet[7] = fstr(table.iloc[idx]['ROE'])
                valueable_sheet[8] = fstr(table.iloc[idx]['ROE'])
                valueable_sheet[9] = fstr(table.iloc[idx]['基本每股盈餘合計'])

                add_db_record.InsertCompanyEstimateSheet(str(table.iloc[idx]['ID']), valueable_sheet, date)
	
                
	
        
def insertMonthlyRevenueDB(path, date):

	sdate = date.split("-")
	year = sdate[0]
	month = sdate[1]
	day = sdate[2]

	file_name = str(year) + "_" + str(month) + "_MonthlyRevenue.csv"

	intial_db()
	
	if((0) == check_file_exist(path + file_name)):
		print(("insertMonthlyRevenueDB : No such file name : "), file_name)
		return (0)
	
	table = pd.read_csv(path + file_name)
	table.fillna(value=0, inplace=True)

	for idx in range(0, table.shape[0]):
		database_InsertCompany(fstr(table.iloc[idx]['公司代號']), fstr(table.iloc[idx]['公司名稱']))
		add_db_record.InsertMonthlyRevenue(fstr(table.iloc[idx]['公司代號']), fstr(table.iloc[idx]['當月營收']), \
			fstr(table.iloc[idx]['上月營收']), fstr(table.iloc[idx]['去年當月營收']), \
			fstr(table.iloc[idx]['上月比較增減(%)']), fstr(table.iloc[idx]['去年同月增減(%)']), \
			fstr(table.iloc[idx]['當月累計營收']), fstr(table.iloc[idx]['去年累計營收']), \
			fstr(table.iloc[idx]['前期比較增減(%)']), date)

		#add_db_record.InsertMonthlyRevenue(str(table.iloc[idx]['公司代號']), str(int(table.iloc[idx]['當月營收'])), \
		#						str(int(table.iloc[idx]['上月營收'])), str(int(table.iloc[idx]['去年當月營收'])), \
		#						str(table.iloc[idx]['上月比較增減(%)']), str(table.iloc[idx]['去年同月增減(%)']), \
		#						str(table.iloc[idx]['當月累計營收']), str(table.iloc[idx]['去年累計營收']), \
		#						str(table.iloc[idx]['前期比較增減(%)']),date)


# Function to be called by the directory monitoring daemon.
# When a file with the name format of "YYYYMMDD_FoundationExchange.csv", 
# it is picked up and inserts its content into the DB
def inserFoundationExchangeDB(pathname):
	file_name = os.path.basename(pathname)

	print("Function: inserFoundationExchangeDB")

	# split the file name and file extension
	fname, fext = os.path.splitext(file_name)
	fdate = fname.split("_")[0]

	# create a date with format YYYY-MM-DD
	sdate = fdate[:4] + "-" + fdate[4:6] + "-" + fdate[6:8] 
	
	intial_db()    
	if((0) == check_file_exist(pathname)):
		print(("inserFoundationExchangeDB : No such file : "), pathname)
		return (-1)
	
	try:
		print("inserFoundationExchangeDB: Process file[" + pathname + "]")
		table = pd.read_csv(pathname)
		table.fillna(value=0, inplace=True)

		# DB Columns are: 
		# Foreign_Investor_buy,Foreign_Investor_sell,Investment_Trust_buy,
		# Investment_Trust_sell,Dealer_buy,Dealer_sell,Total, Category, Date
		for idx in range(0, table.shape[0]):
			database_InsertCompany(fstr(table.iloc[idx]['ID']), fstr(table.iloc[idx]['Name']))
			#add_db_record.InsertFoundationExchange(fstr(table.iloc[idx]['ID']), fstr(table.iloc[idx]['Foreign_Investor_buy']), \
			#	 fstr(table.iloc[idx]['Foreign_Investor_sell']), fstr(table.iloc[idx]['Investment_Trust_buy']), \
			#	 fstr(table.iloc[idx]['Investment_Trust_sell']), fstr(table.iloc[idx]['Dealer_buy']), \
			#	 fstr(table.iloc[idx]['Dealer_sell']), fstr(table.iloc[idx]['Total']), \
			#	 fstr(table.iloc[idx]['Category']), sdate)
			add_db_record.InsertFoundationExchange(fstr(table.iloc[idx]['ID']), fstr(int(table.iloc[idx]['Foreign_Investor_buy'])), \
				fstr(int(table.iloc[idx]['Foreign_Investor_sell'])), fstr(int(table.iloc[idx]['Investment_Trust_buy'])), \
				fstr(table.iloc[idx]['Investment_Trust_sell']), fstr(table.iloc[idx]['Dealer_buy']), \
				fstr(table.iloc[idx]['Dealer_sell']), fstr(table.iloc[idx]['Total']), \
				fstr(int(table.iloc[idx]['Category'])), sdate)
	except Exception as e:
		print(e)
		print(table.iloc[idx])
		raise Exception



def insertInsertStockExchangeDB(pathname):
	file_name = os.path.basename(pathname)

	print("Function: insertInsertStockExchangeDB")

	# Split the file name and file extension
	fname, fext = os.path.splitext(file_name)
	fdate = fname.split("_")[0]

	# Create a date with format YYYY-MM-DD
	sdate = fdate[:4] + "-" + fdate[4:6] + "-" + fdate[6:8]

	intial_db()
	if((0) == check_file_exist(pathname)):
		print(("insertInsertStockExchangeDB : No such file name : "), pathname)
		return (-1)

	try:
		print("insertInsertStockExchangeDB: Process file[" + pathname + "]")
		table = pd.read_csv(pathname)
		table.fillna(value=0, inplace=True)

		# DB Columns are: ID, Name, Volume, StrPrice, highPrice, lowPrice, EndPrice, Category, Date
		for idx in range(0, table.shape[0]):
			database_InsertCompany(fstr(table.iloc[idx]['ID']), fstr(table.iloc[idx]['Name']))
			add_db_record.InsertStockExchange(fstr(table.iloc[idx]['ID']), fstr(table.iloc[idx]['Volume']), \
				fstr((table.iloc[idx]['StrPrice'])), fstr((table.iloc[idx]['highPrice'])), \
				fstr(table.iloc[idx]['lowPrice']), fstr(table.iloc[idx]['EndPrice']), fstr(table.iloc[idx]['Category']), sdate)

			#add_db_record.InsertStockExchange(fstr(table.iloc[idx]['ID']), fstr(int(table.iloc[idx]['Volume'])), \
			#	fstr((table.iloc[idx]['StrPrice'])), fstr((table.iloc[idx]['highPrice'])), \
			#	fstr(table.iloc[idx]['lowPrice']), fstr(table.iloc[idx]['EndPrice']), fstr(int(table.iloc[idx]['Category'])), sdate)
	except Exception as e:
		print(e)
	raise Exception

def insertInsertMarginTradeDB(pathname):
	file_name = os.path.basename(pathname)

	print("Function: insertInsertMarginTradeDB")

	# Split the file name and file extension
	fname, fext = os.path.splitext(file_name)
	fdate = fname.split("_")[0]

	# Create a date with format YYYY-MM-DD
	sdate = fdate[:4] + "-" + fdate[4:6] + "-" + fdate[6:8]
	
	intial_db()
	if((0) == check_file_exist(pathname)):
		print(("insertInsertMarginTradeDB : No such file name : "), pathname)
		return (0)

	try:
		table = pd.read_csv(pathname)
		table.fillna(value=0, inplace=True)

		# DB Columns are: ID, Name, MarginTradebuy, MarginTradeSell, MarginTradeRemine, 
		# ShortSellBuy, ShortSellSell, ShortSellRemine, Category, Date
		for idx in range(0, table.shape[0]):
			database_InsertCompany(fstr(table.iloc[idx]['ID']), fstr(table.iloc[idx]['Name']))
			add_db_record.InsertMarginTrade(str(table.iloc[idx]['ID']), fstr(int(table.iloc[idx]['MarginTradeBuy'])), \
				fstr(table.iloc[idx]['MarginTradeSell']), fstr(table.iloc[idx]['MarginTradeRemain']), \
				fstr(table.iloc[idx]['ShortSellBuy']), fstr(table.iloc[idx]['ShortSellSell']), \
				fstr(table.iloc[idx]['TotalVolume']), fstr(table.iloc[idx]['ChargeOff']), \
				fstr(table.iloc[idx]['ShortSellRemain']), fstr(table.iloc[idx]['Category']), sdate)

			#add_db_record.InsertMarginTrade(str(table.iloc[idx]['ID']), fstr(int(table.iloc[idx]['MarginTradeBuy'])), \
			#	fstr(int(table.iloc[idx]['MarginTradeSell'])), fstr(int(table.iloc[idx]['MarginTradeRemain'])), \
			#	fstr(table.iloc[idx]['ShortSellBuy']), fstr(table.iloc[idx]['ShortSellSell']), \
			#	fstr(table.iloc[idx]['TotalVolume']), fstr(table.iloc[idx]['ChargeOff']), \
			#	fstr(table.iloc[idx]['ShortSellRemain']), fstr(int(table.iloc[idx]['Category'])), sdate)
	except Exception as e:
		print(e)
		raise Exception

def test_verify_financaStatement():
	insertFinancailSeate_to_database("./", "1","2017-05-15")
	print ("process done")

		
if __name__ == '__main__':
	#insertMonthlyRevenueDB("./", "2018-09-01")
	#print("**********2018_9_MonthRevenue insert done***************")
	#inserFoundationExchangeDB("/home/thomaschen/tmp/test_run/CrawlerData/FoundationExchange/20130721_FoundationExchange.csv")
	#inserFoundationExchangeDB("/home/thomaschen/tmp/test_run/CrawlerData/FoundationExchange/20130115_FoundationExchange.csv")
	#print("**********20181105_FoundationExchange insert done***************")
	#insertInsertStockExchangeDB("./", "2018-11-05")
	#print("**********20181105_stockExchange insert done***************")
	#insertInsertMarginTradeDB("./", "2018-11-05")
	#print("**********20181105_MarginTrade insert done***************")
	insertCompanyFinancialStatement("D:/Stock/finacial/", "2018-11-15", "3", "TWSE")

