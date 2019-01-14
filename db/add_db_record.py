#!/usr/bin/python
# -*- coding: utf_8 -*-

import mysql.connector as mcon
from mysql.connector import errorcode
import datetime
from datetime import date, timedelta
import socket
import warnings
#from enum import Enum

#ERR = Enum(Empty = -1, Network = -2, Dup = -3)


def dbgPrint(s):
	ts = str(datetime.datetime.now())
	print("\n[" + ts + "]:" + str(s) + "\n")

def isfloat(d):
	try:
		num = float(d)
	except ValueError:
		return False
	return True

# Must provide a database name and a host, either "localhost" or an IP address
def ConnectDB(host_addr, dbname, dbpasswrod):
	global cursor
	global db

	if (host_addr.strip() == "" or dbname.strip()) =="":
		dbgPrint("Must have a host and database to connect")
		return(-1)

	# check for a valid IP address
	if not (host_addr == "localhost"):
		try:
			socket.inet_aton(host_addr)
		except socket.error:
			dbgPrint("Invalid IP address")
			return(-1)
	try:
		db = mcon.connect(host=host_addr,		# the host
			user="root",	# username
			passwd=dbpasswrod,
			database=dbname,
			charset='utf8',
			use_unicode=True)

		cursor = db.cursor()

		return(db)

	except mysql.connector.Error as err:
		dbgPrint("Connect to DB Error [" + str(err.errno) + "] " + str(err))
		return(-1)



# Function to validate a date in the formate of yyyy-mm-dd
def valid_date(strDate):
	try:
		datetime.datetime.strptime(strDate, '%Y-%m-%d')
	except ValueError:
		raise ValueError("valid_date: Incorrect DATE format, should be YYYY-MM-DD")


# Function to get the latest date of a given table
def getLatestDate(table):
	if(table.strip() == ""):
		return(-1)

	try:
		cursor.execute("SELECT max(Date) FROM " + table)
		row = cursor.fetchall()
		if(cursor.rowcount <= 0):
			dbgPrint("getLatestDate (ERROR): Cannot get last record")
			return(-1)

		return(row[0][0])

	except Exception as e:
		dbgPrint("getLatestDate (ERROR): Exception")
		print(e)
		raise Exception

def check_record(sID, date, category, table):
	try:
		if(date.strip() == ""):
			cursor.execute( \
			"SELECT COUNT(1) FROM " + table + " WHERE StockID = %s limit 1", (sID,))
		else:
			if(category.strip() == ""):
				cursor.execute( \
				"SELECT COUNT(1) FROM " + table + " WHERE CoId = %s and Date = %s limit 1", (sID, date))
			else:
				 cursor.execute( \
                 "SELECT COUNT(1) FROM " + table + " WHERE CoId = %s and Date = %s and Category = %s limit 1", (sID, date, category))

		res = cursor.fetchone()
		if res[0] > 0:
			dbgPrint("cehck_record: Error: Record already exist")
			return(-1)

	except mcon.Error as err:
		 dbgPrint("cehck_record: DB Error, table[" + table + "] err [" + str(err) + "] ")
		 return(-1)

	dbgPrint("check_record Completed: table [" + table + "] [" + str(sID) + "]")
	return(0)


def InsertCompany(stockID, name):
	if (stockID.strip()=="" or name.strip()==""):
		dbgPrint("InsertCompany: Parameters cannot be empty")
		return(-1)

	# Get CoId
	cursor.execute("SELECT CoId FROM Company WHERE StockID = %s", (stockID,))
	row = cursor.fetchall()
		
	# only insert if the company does not exists
	if(cursor.rowcount > 0):
		dbgPrint("InsertCompany: Error: Company already exists" + str(cursor.rowcount))
		return(-1)
				
	try:
		if(check_record(stockID, "", "", "Company") != 0):
			dbgPrint("InsertCompany: Error: Record already exist, please make sure no duplicates")
			return(-1)

		add_fs = ("INSERT INTO Company (StockID, CompanyName) " \
			  "VALUES (%(_stockid)s, %(_name)s)")

		data_fs = { 
			'_stockid': int(stockID),
			'_name': name,
			}

		cursor.execute(add_fs, data_fs)
		db.commit()
		
	except mcon.Error as err:
		dbgPrint("InsertCompany: Insert Error  [" + str(err) + "] ")
		return(-1)

	dbgPrint("InsertCompany: Insert Completed: " + str(data_fs))
	return(0)

def InsertCalStatement(stockID, eps, netaps, roe, roa, date):
	if (stockID.strip() == "" or date.strip() == ""):
		dbgPrint("InsertCalStatement: StockID and Date cannot be empty")
		return(-1)

	if ((stockID.lstrip('-+').isdigit() == False) and (not isfloat(stockID))):
		dbgPrint("InsertCalStatement: stockID must be a digit")
		return(-1)
	else:
		# Convert stockID from float to in then string
		stockID = str(int(float(stockID)))

	if (not eps.strip() == "") and (not isfloat(eps)):
		dbgPrint("CalIncomeStatement: Earning Per Share must be digits")
		return(-1)

	if (not netaps.strip() == "") and (not isfloat(netaps)):
		dbgPrint("InsertCalStatement: Net Asset Per Share must be digits")
		return(-1)

	if (not roe.strip() == "") and (not isfloat(roe)):
		dbgPrint("InsertCalStatement: Net Asset Per Share must be digits")
		return(-1)

	if (not roa.strip() == "") and (not isfloat(roa)):
		dbgPrint("InsertCalStatement: Net Asset Per Share must be digits")
		return(-1)

	try:
		valid_date(date)

		# Get CoId
		cursor.execute("SELECT CoId FROM Company WHERE StockID=%s", (stockID,))
		row = cursor.fetchall()
		if(cursor.rowcount <= 0):
			dbgPrint("CalStatement: Error: Cannot locate Company ID" + str(cursor.rowcount))
			return(-1)

		if(check_record(str(row[0][0]), date, "", "CalStatement") != 0):
			dbgPrint("InsertCalStatement: Error: Record already exist, please make sure no duplicates")
			return(-1)


		add_is = ("INSERT INTO CalStatement " \
			"(CoId, EarningPerShare, NetAssetPerShare, ROE, ROA, Date) " \
			"VALUES (%(_coid)s, %(_earningpershare)s, %(_netassetpershare)s, %(_roe)s, \
			%(_roa)s, %(_date)s)")

		data_is = {
				'_coid': int(row[0][0]),
				'_earningpershare': float(eps),
				'_netassetpershare': float(netaps),
				'_roe': float(roe),
				'_roa': float(roa),
				'_date': date,
				}
	
		cursor.execute(add_is, data_is)
		db.commit()
		
	except mcon.Error as err:
		 dbgPrint("InsertCalStatement: DB Error [" + str(err) + "] ")
		 return(-1)


	dbgPrint("InsertcalStatement: Insert Complete " + str(data_is))
	return(0)


def InsertIncomeStatement(stockID, oprevenu, opprofit, netincome, \
							nonoprevenueexpense, revenuebeforetax, date):
	if (stockID.strip() == "" or date.strip() == ""):
		dbgPrint("InsertIncomeStatement: StockID and Date cannot be empty")
		return(-1)

	#if not (stockID.lstrip('-+').isdigit()):
	#	dbgPrint("InsertIncomeStatement: StockID must be a digit")
	#	return(-1)
	if ((stockID.lstrip('-+').isdigit() == False) and (not isfloat(stockID))):
		dbgPrint("InsertCalStatement: stockID must be a digit")
		return(-1)
	else:
		# Convert stockID from float to in then string
		stockID = str(int(float(stockID)))

	if (not oprevenu.strip() == "") and (not oprevenu.lstrip('-+').isdigit()):
		dbgPrint("InsertIncomeStatement: Operational Revenue must be digits")
		return(-1)

	if (not opprofit.strip() == "") and (not opprofit.lstrip('-+').isdigit()):
		 dbgPrint("InsertIncomeStatement: Operational Profit must be digits")
		 return(-1)

	if (not netincome.strip() == "") and (not netincome.lstrip('-+').isdigit()):
		 dbgPrint("InsertIncomeStatement: Non-Operational Revenue must be digits")
		 return(-1)

	if (not nonoprevenueexpense.strip() == "") and (not nonoprevenueexpense.lstrip('-+').isdigit()):
		 dbgPrint("InsertIncomeStatement: Non-Operational Revenue and Expense must be digits")
		 return(-1)

	if (not revenuebeforetax.strip() == "") and (not revenuebeforetax.lstrip('-+').isdigit()):
		 dbgPrint("InsertIncomeStatement: Revenue Before Tax must be digits")
		 return(-1)


	try:
		valid_date(date)

		# Get CoId
		cursor.execute("SELECT CoId FROM Company WHERE StockID = %s", (stockID,))
		row = cursor.fetchall()
		if(cursor.rowcount <= 0):
						 dbgPrint("IncomeStatement Error: Cannot locate Company ID" + str(cursor.rowcount))
						 return(-1)
		
		if(check_record(str(row[0][0]), date, "", "IncomeStatement") != 0):
			dbgPrint("InsertIncomeStatement: Error: Record already exist, please make sure no duplicates")
			return(-1)

		add_is = ("INSERT INTO IncomeStatement " \
			"(CoId, OpRevenue, OpProfit, NetIncome, NonOpRevenueExpense, RevenueBeforeTax, Date) " \
			"VALUES (%(_coid)s, %(_oprevenue)s, %(_opprofit)s, %(_netincome)s, \
			%(_nonoprevenueexpense)s, %(_revenuebeforetax)s, %(_date)s)")

		data_is = {
			'_coid': int(row[0][0]),
			'_oprevenue': int(oprevenu),
			'_opprofit': int(opprofit),
			'_netincome': int(netincome),
			'_nonoprevenueexpense': int(nonoprevenueexpense),
			'_revenuebeforetax': int(revenuebeforetax),
			'_date': date,
			}

		cursor.execute(add_is, data_is)
		db.commit()


	except mcon.Error as err:
		 dbgPrint("InsertIncomeStatement: Connect to DB Error [" + str(err) + "] ")
		 return(-1)


	dbgPrint("InsertIncomeStatement: Insert Complete " + str(data_is))
	return(0)


# API to insert into Financial Statement Table
# stockID, asset and equity must be numbers
# date must be in the format of yyyy-mm-dd
# all parameters must be provided
def InsertFinancialStatement(stockID, asset, equity, date):
	if (stockID.strip()=="" or asset.strip()=="" or equity.strip()=="" or date.strip()==""):
		dbgPrint("InsertFinancialStatement: Parameters cannot be empty")
		return(-1)

	if ((stockID.lstrip('-+').isdigit() == False) and (not isfloat(stockID))):
		dbgPrint("InsertCalStatement: stockID must be a digit")
		return(-1)
	else:
		# Convert stockID from float to in then string
		stockID = str(int(float(stockID)))

	if not (asset.isdigit and equity.isdigit):
		dbgPrint("InsertFinancialStatement: stockID, asset and equity must be numbers")
		return(-1)

	try:
		valid_date(date)

		# Get CoId
		cursor.execute("SELECT CoId FROM Company WHERE StockID=%s", (stockID,))
		row = cursor.fetchall()
		if(cursor.rowcount <= 0):
			dbgPrint("InsertFinancialStatement: Error: Cannot locate Company ID" + str(cursor.rowcount))
			return(-1)
			   
		if(check_record(str(row[0][0]), date, "", "FinancialStatement") != 0):
			dbgPrint("InsertFinancialStatement: Error: Record already exist, please make sure no duplicates")
			return(-1)

		add_fs = ("INSERT INTO FinancialStatement " \
			"(CoId, TotalAsset, TotalEquity, Date) " \
			"VALUES (%(_coid)s, %(_asset)s, %(_equity)s, %(_date)s)")

		data_fs = {
						'_coid': int(row[0][0]),
			'_asset': int(asset),
			'_equity': int(equity),
			'_date': date,}

		cursor.execute(add_fs, data_fs)
		db.commit()

	except mcon.Error as err:
		dbgPrint("InsertFinancialStatement: Connect to DB Error [" + str(err) + "] ")
		return(-1)

	dbgPrint("InsertFinancialStatement: Insert Completed: " + str(data_fs))
	return(0)


def InsertStockExchange(stockID, ExchangeVolume, StartPrice, HighPrice, LowPrice, EndPrice, Category,  date):
	if (stockID.strip()=="" or \
			ExchangeVolume.strip()=="" or StartPrice.strip()=="" or \
			HighPrice.strip()=="" or LowPrice.strip()=="" or		\
			EndPrice.strip()=="" or date.strip()==""):
		dbgPrint("InsertStockExchange: Parameters cannot be empty")
		return(-1)

	if ((stockID.lstrip('-+').isdigit() == False) and (not isfloat(stockID))):
		dbgPrint("InsertCalStatement: stockID must be a digit")
		return(-1)
	else:
		# Convert stockID from float to in then string
		stockID = str(int(float(stockID)))


	try:
		valid_date(date)
		
		# Get CoId
		cursor.execute("SELECT CoId FROM Company WHERE StockID=%s", (stockID,))
		row = cursor.fetchall()
		if(cursor.rowcount <= 0):
			dbgPrint("InsertStockExchange: Error: Cannot locate Company ID"  +str(stockID) +":"+ str(cursor.rowcount))
			return(-1)

		if(check_record(str(row[0][0]), date, Category, "StockExchange") != 0):
			dbgPrint("InsertStockExchange: Error: Record already exist, please make sure no duplicates")
			return(-1)

		add_fs = ("INSERT INTO StockExchange " \
					  "(CoId, ExchangeVolume, StartPrice, HighPrice, LowPrice, EndPrice, Category, Date) " \
				  "VALUES (%(_coid)s, %(_exchangevolume)s, %(_startprice)s, %(_highprice)s, \
					  %(_lowprice)s, %(_endprice)s, %(_category)s, %(_date)s)")

		data_fs = {
			'_coid': int(row[0][0]),
			'_exchangevolume': int(ExchangeVolume),
			'_startprice': float(StartPrice),
			'_highprice': float(HighPrice),
			'_lowprice': float(LowPrice),
			'_endprice': float(EndPrice),
			'_category': int(Category),
			'_date': date,}

		cursor.execute(add_fs, data_fs)
		db.commit()

	except mcon.Error as err:
		dbgPrint("InsertStockExchange: Connect to DB Error [" + str(err) + "] ")
		return(-1)

	dbgPrint("InsertStockExchange: Insert Completed: " + str(data_fs))
	return(0)

def InsertFoundationExchange(stockID, ForeignInvestorBuy, ForeignInvestorSell, \
							 InvestmentTrustBuy, InvestmentTrustSell, \
							 DealerBuy, DealerSell, TotalVolume, Category, date):

	if (stockID.strip()=="" or \
			ForeignInvestorBuy.strip()=="" or ForeignInvestorSell.strip()=="" or \
			InvestmentTrustBuy.strip()=="" or InvestmentTrustSell.strip()=="" or \
			DealerBuy.strip()=="" or DealerSell.strip()=="" or \
			TotalVolume.strip()=="" or Category.strip()=="" or date.strip()==""):
		dbgPrint("InsertFoundationExchange: Parameters cannot be empty")
		return(-1)

	try:
		valid_date(date)

		# Get CoId
		cursor.execute("SELECT CoId FROM Company WHERE StockID=%s", (stockID,))
		row = cursor.fetchall()
		if(cursor.rowcount <= 0):
			dbgPrint("InsertFoundationExchange: Error: Cannot locate Company ID"  + str(stockID) +":"+ str(cursor.rowcount))
			return(-1)

		# check for duplicate, i.e. same coID, same date and same category
		if(check_record(str(row[0][0]), date, Category, "FoundationExchange") != 0):
			dbgPrint("InsertFoundationExchange (Error): Record already exist:: coID[" + str(row[0][0]) + "] date[" + str(date) + "] Category[" + str(Category) + "]")
			return(-1)

		add_fs = ("INSERT INTO FoundationExchange (CoId, ForeignInvestorBuy, ForeignInvestorSell, " \
				"InvestmentTrustBuy, InvestmentTrustSell, DealerBuy, DealerSell, TotalVolume, Category, date) " \
			"VALUES (%(_coid)s, %(_foreigninvestorbuy)s, %(_foreigninvestorsell)s, %(_investmenttrustbuy)s, %(_investmenttrustsell)s, " \
				"%(_dealerbuy)s, %(_dealersell)s, %(_totalvolume)s, %(_category)s, %(_date)s)")

		data_fs = {
			'_coid'				   : int(row[0][0]),
			'_foreigninvestorbuy'  : int(ForeignInvestorBuy),
			'_foreigninvestorsell' : int(ForeignInvestorSell),
			'_investmenttrustbuy'  : int(InvestmentTrustBuy),
			'_investmenttrustsell' : int(InvestmentTrustSell),
			'_dealerbuy'		   : int(DealerBuy),
			'_dealersell'		   : int(DealerSell),
			'_totalvolume'		   : int(TotalVolume),
			'_category'		   : int(Category),
			'_date': date,}

		cursor.execute(add_fs, data_fs)
		db.commit()

	except mcon.Error as err:
		dbgPrint("FoundationExchange: DB Error [" + str(err) + "] ")
		return(-1)
	except Exception as e:
		dbgPrint("FoundationExchange (ERROR): Exception")
		dbgPrint(e)
		raise Exception

	dbgPrint("FoundationExchange: Insert Completed: " + str(data_fs))
	return(0)

def InsertMonthlyRevenue(stockID, MonthlyRevenue, LastMonthlyRevenue, LastYearMonthlyRevenue,\
		 MonthlyIncreaseRevenue, LastYearMonthlyIncreaseRevenue, \
		 CumulativeRevenue, LastYearCumulativeRevenue, CompareCumulativeRevenue,date):
		
	if (stockID.strip()=="" or \
			MonthlyRevenue.strip()=="" or LastMonthlyRevenue.strip()=="" or \
			LastYearMonthlyRevenue.strip()=="" or MonthlyIncreaseRevenue.strip()=="" or \
			LastYearMonthlyIncreaseRevenue.strip()=="" or CumulativeRevenue.strip()=="" or \
			LastYearCumulativeRevenue.strip()=="" or CompareCumulativeRevenue.strip()=="" or \
			date.strip()==""):
		dbgPrint("InsertMonthlyRevenue: Parameters cannot be empty")
		return(-1)

	try:
		valid_date(date)

		# Get CoId
		cursor.execute("SELECT CoId FROM Company WHERE StockID=%s", (stockID,))
		row = cursor.fetchall()
		if(cursor.rowcount <= 0):
			dbgPrint("InsertMonthlyRevenue: Error: Cannot locate Company ID"  +str(stockID) +":"+ str(cursor.rowcount))
			return(-1)

		if(check_record(str(row[0][0]), date, "", "MonthlyRevenue") != 0):
			dbgPrint("InsertMonthlyRevenue: Error: Record already exist, please make sure no duplicates")
			return(-1)

		print("insert db")
		add_fs = ("INSERT INTO MonthlyRevenue (CoId, MonthlyRevenue, LastMonthlyRevenue, LastYearMonthlyRevenue, MonthlyIncreaseRevenue, " \
				"LastYearMonthlyIncreaseRevenue, CumulativeRevenue, LastYearCumulativeRevenue, CompareCumulativeRevenue, date) " \
			"VALUES (%(_coid)s, %(_monthlyrevenue)s, %(_lastmonthlyrevenue)s, %(_lastyearmonthlyrevenue)s, %(_monthlyincreaserevenue)s, " \
				"%(_lastyearmonthlyincreaserevenue)s, %(_cumulativerevenue)s, %(_lastyearcumulativerevenue)s, %(_comparecumulativerevenue)s, %(_date)s)" )

		data_fs = {
			'_coid'				   : int(row[0][0]),
			'_monthlyrevenue'	   : int(MonthlyRevenue),
			'_lastmonthlyrevenue'  : int(LastMonthlyRevenue),
			'_lastyearmonthlyrevenue'  : int(LastYearMonthlyRevenue),
			'_monthlyincreaserevenue'  : float(MonthlyIncreaseRevenue),
			'_lastyearmonthlyincreaserevenue': float(LastYearMonthlyIncreaseRevenue),
			'_cumulativerevenue'		  : int(CumulativeRevenue),
			'_lastyearcumulativerevenue'  : int(LastYearCumulativeRevenue),
			'_comparecumulativerevenue'   : float(CompareCumulativeRevenue),
			'_date': date,}

		cursor.execute(add_fs, data_fs)
		db.commit()

	except mcon.Error as err:
		dbgPrint("InsertMonthlyRevenue: Connect to DB Error [" + str(err) + "] ")
		return(-1)

	dbgPrint("InsertMonthlyRevenue: Insert Completed: " + str(data_fs))
	return(0)

def InsertMarginTrade(stockID, MarginBuy, MarginSell, MarginRemine, ShortSellBuy, \
		ShortSellSell, ShortSellRemine, TotalVolume, ChargeOff, Category, date):
	if (stockID.strip()==""   or \
			MarginBuy.strip()=="" or MarginSell.strip()==""		  or \
			MarginRemine.strip()==""  or ShortSellBuy.strip()=="" or \
			ShortSellSell.strip()=="" or ShortSellRemine.strip()=="" or \
			TotalVolume.strip()==""   or ChargeOff.strip()==""	  or date.strip()==""):
		dbgPrint("InsertMarginTrade: Parameters cannot be empty")
		return(-1)

	try:
		valid_date(date)

		# Get CoId
		cursor.execute("SELECT CoId FROM Company WHERE StockID=%s", (stockID,))
		row = cursor.fetchall()
		if(cursor.rowcount <= 0):
			dbgPrint("InsertMarginTrade: Error: Cannot locate Company ID" +str(stockID) +":"+ str(cursor.rowcount))
			return(-1)

		if(check_record(str(row[0][0]), date, Category, "MarginTrading") != 0):
			dbgPrint("InsertMarginTrade: Error: Record already exist, please make sure no duplicates")
			return(-1) 

		add_fs = ("INSERT INTO MarginTrading (CoId, MarginBuy, MarginSell, MarginRemine, ShortSellBuy, " \
				"ShortSellSell, ShortSellRemine, TotalVolume, ChargeOff, Category, date) " \
			"VALUES (%(_coid)s, %(_marginbuy)s, %(_marginsell)s, %(_marginremine)s, %(_shortsellbuy)s, " \
				"%(_shortsellsell)s, %(_shortsellremine)s, %(_totalvolume)s, %(_chargeoff)s, %(_category)s, %(_date)s)")

		data_fs = {
			'_coid'		  : int(row[0][0]),
			'_marginbuy'  : int(MarginBuy),
			'_marginsell' : int(MarginSell),
			'_marginremine'  : int(MarginRemine),
			'_shortsellbuy'  : int(ShortSellBuy),
			'_shortsellsell'  : int(ShortSellSell),
			'_shortsellremine' : int(ShortSellRemine),
			'_totalvolume' : int(TotalVolume),
			'_chargeoff' : int(ChargeOff),
			'_category' : int(Category),
			'_date': date,}

		cursor.execute(add_fs, data_fs)
		db.commit()

	except mcon.Error as err:
		dbgPrint("InsertMarginTrade: Insert Error [" + str(err) + "] ")
		return(-1)

	dbgPrint("InsertMarginTrade: Insert Completed: " + str(data_fs))
	return(0)


def InsertBalanceSheet(stockID, dataGroup, date):
        if (stockID.strip() == "" or date.strip() == ""):
                dbgPrint("InsertIncomeStatement: StockID and Date cannot be empty")
                return(-1)
    
        #if not (stockID.lstrip('-+').isdigit()):
        #	dbgPrint("InsertIncomeStatement: StockID must be a digit")
        #	return(-1)

        if ((stockID.lstrip('-+').isdigit() == False) and (not isfloat(stockID))):
                dbgPrint("InsertCalStatement: stockID must be a digit")
                return(-1)
        else:
                # Convert stockID from float to in then string
                stockID = str(int(float(stockID)))
		
        for idx in range(1, dataGroup.len()):
                if(not dataGroup[idx].strip() == "") and (not dataGroup[idx].lstrip('-+').isdigit()):
                        dbgPrint("dataGroup[" + idx +"]" + "=" + dataGroup[idx])
                        return(-1)
        try:
                valid_date(date)
                # Get CoId
                cursor.execute("SELECT CoId FROM Company WHERE StockID = %s", (stockID,))
                row = cursor.fetchall()

                if(cursor.rowcount <= 0):
                        dbgPrint("BalanceStatementSheet Error: Cannot locate Company ID" + str(cursor.rowcount))
                        return(-1)

                if(check_record(str(row[0][0]), date, "", "BalanceStatementSheet") != 0):
                        dbgPrint("BalanceStatementSheet: Error: Record already exist, please make sure no duplicates")
                        return(-1)

                add_is = ("INSERT INTO BalanceStatementSheet " \
			  "(CoId, \
                            CashAndCashEquivalents, \
			    NotesReceivableNet, \
			    AccountsReceivableNet, \
			    AccountsReceivableRelatedNet, \
			    OthersAccountsReceivable, \
			    OthersAccountsReceivableRelated, \
			    Inventories, \
			    Prepayments, \
			    TotalCurrentAssets, \
			    TotalNonCurrentAssets, \
			    TotalAssets, \
			    ShortTermDebt, \
			    AccountsPayable, \
			    AccountsPayableRelated, \
			    OtherAccountsPayable, \
			    TotalCurrentDebt, \
			    LongTermDebtPayable, \
			    TotalNonCurrentDebt, \
			    TotalLiabilities, \
			    CapitalCommonStock, \
			    TotalEquity, \
			    TotalLiabilitiesAndEquity, \
			    Date) " \
			   "VALUES (%(_coid)s, %(_data[0])s, %(_data[1])s, %(_data[2])s, %(_data[3])s, %(_data[4])s, %(_data[5])s, \
			   %(_data[6])s, %(_data[7])s, %(_data[8])s, %(_data[9])s, %(_data[10])s, %(_data[11])s, %(_data[12])s, \
			   %(_data[13])s, %(_data[14])s, %(_data[15])s, %(_data[16])s, %(_data[17])s, %(_data[18])s, %(_data[19])s, \
			   %(_data[20])s, %(_data[21])s, %(_date)s)")

                data_is = {
			'_coid': int(row[0][0]),
			'_data[0]': int(dataGroup[0]),
                        '_data[1]': int(dataGroup[1]),
                        '_data[2]': int(dataGroup[2]),
                        '_data[3]': int(dataGroup[3]),
                        '_data[4]': int(dataGroup[4]),
                        '_data[5]': int(dataGroup[5]),
                        '_data[6]': int(dataGroup[6]),
                        '_data[7]': int(dataGroup[7]),
                        '_data[8]': int(dataGroup[8]),
                        '_data[9]': int(dataGroup[9]),
                        '_data[10]': int(dataGroup[10]),
                        '_data[11]': int(dataGroup[11]),
                        '_data[12]': int(dataGroup[12]),
                        '_data[13]': int(dataGroup[13]),
                        '_data[14]': int(dataGroup[14]),
                        '_data[15]': int(dataGroup[15]),
                        '_data[16]': int(dataGroup[16]),
                        '_data[17]': int(dataGroup[17]),
                        '_data[18]': int(dataGroup[18]),
                        '_data[19]': int(dataGroup[19]),
                        '_data[20]': int(dataGroup[20]),
                        '_data[21]': int(dataGroup[21]),
			'_date': date,
			}
                cursor.execute(add_is, data_is)
                db.commit()
        except mcon.Error as err:
                dbgPrint("BalanceStatementSheet: Connect to DB Error [" + str(err) + "] ")
                return(-1)

        dbgPrint("BalanceStatementSheet: Insert Complete " + str(data_is))
        return(0)

def InsertIncomeStatementSheet(stockID, dataGroup, date):
        if (stockID.strip() == "" or date.strip() == ""):
                dbgPrint("IncomeStatementSheet: StockID and Date cannot be empty")
                return(-1)
    
        #if not (stockID.lstrip('-+').isdigit()):
        #	dbgPrint("InsertIncomeStatement: StockID must be a digit")
        #	return(-1)

        if ((stockID.lstrip('-+').isdigit() == False) and (not isfloat(stockID))):
                dbgPrint("IncomeStatementSheet: stockID must be a digit")
                return(-1)
        else:
                # Convert stockID from float to in then string
                stockID = str(int(float(stockID)))
		
        for idx in range(1, dataGroup.len()):
                if(not dataGroup[idx].strip() == "") and (not dataGroup[idx].lstrip('-+').isdigit()):
                        dbgPrint("dataGroup[" + idx +"]" + "=" + dataGroup[idx])
                        return(-1)
        try:
                valid_date(date)
                # Get CoId
                cursor.execute("SELECT CoId FROM Company WHERE StockID = %s", (stockID,))
                row = cursor.fetchall()

                if(cursor.rowcount <= 0):
                        dbgPrint("IncomeStatementSheet Error: Cannot locate Company ID" + str(cursor.rowcount))
                        return(-1)

                if(check_record(str(row[0][0]), date, "", "IncomeStatementSheet") != 0):
                        dbgPrint("IncomeStatementSheet: Error: Record already exist, please make sure no duplicates")
                        return(-1)


                add_is = ("INSERT INTO IncomeStatementSheet " \
                          "(CoId, \
			    GrossSales, \
			    CostOfGoodsSold, \
			    GrossProfitNet, \
			    CostPromotion, \
			    CostADM, \
			    CostExpenseRD, \
			    CostOther, \
			    TotalCostOfExpenses, \
			    OperateIncome, \
			    TotalNonOpIncome, \
			    PreTaxIncome, \
			    PureIncome, \
			    CNIS, \
			    Date) " \
			   "VALUES (%(_coid)s, %(_data[0])s, %(_data[1])s, %(_data[2])s, %(_data[3])s, %(_data[4])s, %(_data[5])s, \
			   %(_data[6])s, %(_data[7])s, %(_data[8])s, %(_data[9])s, %(_data[10])s, %(_data[11])s, %(_data[12])s, %(_date)s)")

                data_is = {
			'_coid': int(row[0][0]),
			'_data[0]': int(dataGroup[0]),
                        '_data[1]': int(dataGroup[1]),
                        '_data[2]': int(dataGroup[2]),
                        '_data[3]': int(dataGroup[3]),
                        '_data[4]': int(dataGroup[4]),
                        '_data[5]': int(dataGroup[5]),
                        '_data[6]': int(dataGroup[6]),
                        '_data[7]': int(dataGroup[7]),
                        '_data[8]': int(dataGroup[8]),
                        '_data[9]': int(dataGroup[9]),
                        '_data[10]': int(dataGroup[10]),
                        '_data[11]': int(dataGroup[11]),
                        '_data[12]': int(dataGroup[12]),
			'_date': date,}
                 
                cursor.execute(add_is, data_is)
                db.commit()

        except mcon.Error as err:
                dbgPrint("IncomeStatementSheet: Connect to DB Error [" + str(err) + "] ")
                return(-1)

        dbgPrint("IncomeStatementSheet: Insert Complete " + str(data_is))
        return(0) 

def InsertCashStatementSheet(stockID, dataGroup, date):
        if (stockID.strip() == "" or date.strip() == ""):
                dbgPrint("CashStatementSheet: StockID and Date cannot be empty")
                return(-1)
    
        #if not (stockID.lstrip('-+').isdigit()):
        #	dbgPrint("InsertIncomeStatement: StockID must be a digit")
        #	return(-1)

        if ((stockID.lstrip('-+').isdigit() == False) and (not isfloat(stockID))):
                dbgPrint("CashStatementSheet: stockID must be a digit")
                return(-1)
        else:
                # Convert stockID from float to in then string
                stockID = str(int(float(stockID)))
		
        for idx in range(1, dataGroup.len()):
                if(not dataGroup[idx].strip() == "") and (not dataGroup[idx].lstrip('-+').isdigit()):
                        dbgPrint("dataGroup[" + idx +"]" + "=" + dataGroup[idx])
                        return(-1)
        try:
                valid_date(date)
                # Get CoId
                cursor.execute("SELECT CoId FROM Company WHERE StockID = %s", (stockID,))
                row = cursor.fetchall()

                if(cursor.rowcount <= 0):
                        dbgPrint("CashStatementSheet Error: Cannot locate Company ID" + str(cursor.rowcount))
                        return(-1)

                if(check_record(str(row[0][0]), date, "", "CashStatementSheet") != 0):
                        dbgPrint("CashStatementSheet: Error: Record already exist, please make sure no duplicates")
                        return(-1)

                add_is = ("INSERT INTO CashStatementSheet " \
			  "(CoId, \
			    OperatingCashFlows, \
			    InvestCashProvided, \
			    FinanceCashFlows, \
			    ExchangeRateChangeOnCash, \
			    CashNetIncrease, \
			    StartCashOfYear, \
			    EndCashOfYear, \
			    Date) " \
			   "VALUES (%(_coid)s, %(_data[0])s, %(_data[1])s, %(_data[2])s, %(_data[3])s, %(_data[4])s, %(_data[5])s,  %(_data[6])s, %(_date)s)")

                data_is = {
			'_coid': int(row[0][0]),
			'_data[0]': int(dataGroup[0]),
                        '_data[1]': int(dataGroup[1]),
                        '_data[2]': int(dataGroup[2]),
                        '_data[3]': int(dataGroup[3]),
                        '_data[4]': int(dataGroup[4]),
                        '_data[5]': int(dataGroup[5]),
                        '_data[6]': int(dataGroup[6]),
			'_date': date,
			}
                cursor.execute(add_is, data_is)
                db.commit()

        except mcon.Error as err:
                dbgPrint("CashStatementSheet: Connect to DB Error [" + str(err) + "] ")
                return(-1)
        dbgPrint("CashStatementSheet: Insert Complete " + str(data_is))
        return (0)


def InsertCompanyEstimateSheet(stockID, dataGroup, date):
        if (stockID.strip() == "" or date.strip() == ""):
                dbgPrint("CompanyEstimateSheet: StockID and Date cannot be empty")
                return(-1)
    
        #if not (stockID.lstrip('-+').isdigit()):
        #	dbgPrint("InsertIncomeStatement: StockID must be a digit")
        #	return(-1)

        if ((stockID.lstrip('-+').isdigit() == False) and (not isfloat(stockID))):
                dbgPrint("CompanyEstimateSheet: stockID must be a digit")
                return(-1)
        else:
                # Convert stockID from float to in then string
                stockID = str(int(float(stockID)))
		
        for idx in range(1, dataGroup.len()):
                if(not dataGroup[idx].strip() == ""):
                        dbgPrint("dataGroup[" + idx +"]" + "=" + dataGroup[idx])
                        return(-1)
        try:
                valid_date(date)
                # Get CoId
                cursor.execute("SELECT CoId FROM Company WHERE StockID = %s", (stockID,))
                row = cursor.fetchall()

                if(cursor.rowcount <= 0):
                        dbgPrint("CompanyEstimateSheet Error: Cannot locate Company ID" + str(cursor.rowcount))
                        return(-1)

                if(check_record(str(row[0][0]), date, "", "CompanyEstimateSheet") != 0):
                        dbgPrint("CompanyEstimateSheet: Error: Record already exist, please make sure no duplicates")
                        return(-1)
                
                add_is = ("INSERT INTO CompanyEstimateSheet " \
			  "(CoId, \
			    OriginalIncomeRate, \
			    OutIncomeRate, \
			    InventoryTurnoverRate, \
			    GrossMarginRate, \
			    OrgProfitRate, \
			    PurIncomeRate, \
			    ROE_Org, \
			    ROE, \
			    ROA, \
			    EPS, \
			    Date) " \
			   "VALUES (%(_coid)s, %(_data[0])s, %(_data[1])s, %(_data[2])s, %(_data[3])s, %(_data[4])s, %(_data[5])s, \
                                    %(_data[6])s, %(_data[7])s, %(_data[8])s, %(_data[9])s, %(_date)s)")
                
                data_is = {
			'_coid': int(row[0][0]),
			'_data[0]': float(dataGroup[0]),
                        '_data[1]': float(dataGroup[1]),
                        '_data[2]': float(dataGroup[2]),
                        '_data[3]': float(dataGroup[3]),
                        '_data[4]': float(dataGroup[4]),
                        '_data[5]': float(dataGroup[5]),
                        '_data[6]': float(dataGroup[6]),
                        '_data[7]': float(dataGroup[7]),
                        '_data[8]': float(dataGroup[8]),
                        '_data[9]': float(dataGroup[9]),
			'_date': date,
			}
                
                cursor.execute(add_is, data_is) 
                db.commit()

        except mcon.Error as err:
                dbgPrint("CompanyEstimateSheet: Connect to DB Error [" + str(err) + "] ")
                return(-1)
        
        dbgPrint("CompanyEstimateSheet: Insert Complete " + str(data_is))
        return(0)
        

if	__name__ == '__main__':
	ConnectDB("localhost", "stock", "ftdi1234")
	InsertCompany("2075", "abc")
	#InsertFinancialStatement("2075", "abc", "1234567890", "1234567890", "2018-09-27")
	#InsertIncomeStatement("2075","3333333333","4444444444","5555555555","6666666666","7777777777","2018-09-27")
	#InsertCalStatement("2075", "55555", "666666", "77777", "88888", "2018-09-27")
	#InsertCompany("7777", "Test Company Name")
