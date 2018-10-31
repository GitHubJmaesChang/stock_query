#!/usr/bin/python
# -*- coding: utf_8 -*-

import mysql.connector as mcon
from mysql.connector import errorcode
import datetime
from datetime import date, timedelta
import socket
import warnings



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
def ConnectDB(host_addr, dbname):
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
			passwd="1234",
			database=dbname,
			charset='utf8',
			use_unicode=True)

		cursor = db.cursor()

	except mysql.connector.Error as err:
		dbgPrint("Connect to DB Error [" + str(err.errno) + "] " + str(err))
		return(-1)



# functino to validate a date in the formate of yyyy-mm-dd
def valid_date(strDate):
	try:
		datetime.datetime.strptime(strDate, '%Y-%m-%d')
	except ValueError:
		raise ValueError("valid_date: Incorrect DATE format, should be YYYY-MM-DD")


def check_record(sID, date, table):
	try:
		if(date.strip() == ""):
			cursor.execute( \
				"SELECT COUNT(1) FROM " + table + " WHERE StockID = %s limit 1", (sID,))
		else:
			cursor.execute( \
				"SELECT COUNT(1) FROM " + table + " WHERE StockID = %s and Date = %s limit 1", \
				(sID, date))

		res = cursor.fetchone()
		if res[0] > 0:
			dbgPrint("cehck_record: Error: Record already exist")
			return(-1)

	except mcon.Error as err:
		 dbgPrint("cehck_record: DB Error [" + str(err) + "] ")
		 return(-1)

	dbgPrint("check_record Completed: table [" + table + "] StockID[" + str(sID) + "]")
	return(0)


def InsertCalStatement(stockid, eps, netaps, roe, roa, date):
        if (stockid.strip() == "" or date.strip() == ""):
                dbgPrint("InsertCalStatement: StockID and Date cannot be empty")
                return(-1)

        if not (stockid.isdigit()):
                dbgPrint("InsertCalStatement: StockID must be a digit")
                return(-1)
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
                if(check_record(stockid, date, "CalStatement") != 0):
                        dbgPrint("InsertCalStatement: Error: Record already exist, please make sure no duplicates")
                        return(-1)

		# Get CoId
                cursor.execute("SELECT CoId FROM Company WHERE StockID=%s", (stockid,))
                row = cursor.fetchall()

                print("#######get CoID########")
                print(row)

                if(cursor.rowcount <= 0):
                        dbgPrint("CalStatement: Error: Cannot locate Company ID" + str(cursor.rowcount))
                        return(-1)

                add_is = ("INSERT INTO CalStatement " \
                        "(CoId, StockID, EarningPerShare, NetAssetPerShare, ROE, ROA, Date) " \
                        "VALUES (%(_coid)s, %(_stockid)s, %(_earningpershare)s, %(_netassetpershare)s, %(_roe)s, \
                        %(_roa)s, %(_date)s)")

                data_is = {
                        '_coid': int(row[0][0]),
                        '_stockid': int(stockid),
                        '_earningpershare': float(eps),
                        '_netassetpershare': float(netaps),
                        '_roe': float(roe),
                        '_roa': float(roa),
                        '_date': date,
                        }

                cursor.execute(add_is, data_is)
                db.commit()

        except mcon.Error as err:
                 dbgPrint("InsertCalStatement: Connect to DB Error [" + str(err) + "] ")
                 return(-1)


        dbgPrint("InsertcalStatement: Insert Complete " + str(data_is))
        return(0)


def InsertIncomeStatement(stockid, oprevenu, opprofit, netincome, \
			nonoprevenueexpense, revenuebeforetax, date):
	if (stockid.strip() == "" or date.strip() == ""):
		dbgPrint("InsertIncomeStatement: StockID and Date cannot be empty")
		return(-1)

	if not (stockid.isdigit()):
		dbgPrint("InsertIncomeStatement: StockID must be a digit")
		return(-1)

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
		if(check_record(stockid, date, "IncomeStatement") != 0):
			 dbgPrint("InsertIncomeStatement: Error: Record already exist, please make sure no duplicates")
			 return(-1)

		# Get CoId
		cursor.execute("SELECT CoId FROM Company WHERE StockID = %s", (stockid,))
		row = cursor.fetchall()
		#if(cursor.rowcount > 1): # this is to be enabled later
		#dbgPrint("IncomeStatement: Error: Too many FinID" + str(cursor.rowcount))
		#return(-1)

		if(cursor.rowcount <= 0):
			dbgPrint("IncomeStatement: Error: Cannot locate Company ID" + str(cursor.rowcount))
			return(-1)

		add_is = ("INSERT INTO IncomeStatement " \
			"(CoId, StockID, OpRevenue, OpProfit, NetIncome, NonOpRevenueExpense, RevenueBeforeTax, Date) " \
			"VALUES (%(_coid)s, %(_stockid)s, %(_oprevenue)s, %(_opprofit)s, %(_netincome)s, \
			%(_nonoprevenueexpense)s, %(_revenuebeforetax)s, %(_date)s)")

		data_is = {
			'_coid': int(row[0][0]),
			'_stockid': int(stockid),
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


def InsertCompany(stockID, name):
	if (stockID.strip()=="" or name.strip()==""):
		dbgPrint("InsertCompany: Parameters cannot be empty")
		return(-1)

	if not (stockID.isdigit()):
		dbgPrint("InsertCompany: stockID must be numbers")
		return(-1)

	try:
		if(check_record(stockID, "", "Company") != 0):
			dbgPrint("InsertCompany: Error: Record already exist, please make sure no duplicates")
			return(-1)
		print("########check_record########")

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


# API to insert into Financial Statement Table
# stockID, asset and equity must be numbers
# date must be in the format of yyyy-mm-dd
# all parameters must be provided
def InsertFinancialStatement(stockID, asset, equity, date):
	if (stockID.strip()=="" or asset.strip()=="" or equity.strip()=="" or date.strip()==""):
		dbgPrint("InsertFinancialStatement: Parameters cannot be empty")
		return(-1)

	if not (stockID.isdigit() and asset.isdigit and equity.isdigit):
		dbgPrint("InsertFinancialStatement: stockID, asset and equity must be numbers")
		return(-1)

	try:
		valid_date(date)
		if(check_record(stockID, date, "FinancialStatement") != 0):
			dbgPrint("InsertFinancialStatement: Error: Record already exist, please make sure no duplicates")
			return(-1)

		add_fs = ("INSERT INTO FinancialStatement " \
			"(StockID, TotalAsset, TotalEquity, Date) " \
			"VALUES (%(_stockid)s, %(_asset)s, %(_equity)s, %(_date)s)")

		data_fs = {
			'_stockid': int(stockID),
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


if	__name__ == '__main__':
	ConnectDB("localhost", "stock")
	InsertCompany("2075", "abc")
	#InsertFinancialStatement("2075", "abc", "1234567890", "1234567890", "2018-09-27")
	#InsertIncomeStatement("2075","3333333333","4444444444","5555555555","6666666666","7777777777","2018-09-27")
	#InsertCalStatement("2075", "55555", "666666", "77777", "88888", "2018-09-27")
	InsertCompany("7777", "Test Company Name")
