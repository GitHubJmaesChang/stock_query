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
                passwd="ftdi1234",
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

                print("Create FinancialStatment Table")
                # Table: FinancialStatment
                # 公司代號, 公司名稱,資產總額/總計, 權益總額/總計
                # colums are created in the order as listed above.
                cursor.execute("create table IF NOT EXISTS FinancialStatement( \
                                FinId INT AUTO_INCREMENT, \
                                StockID INT NOT NULL, \
                                CompanyName varchar(100), \
                                TotalAsset BIGINT, \
                                TotalEquity BIGINT, \
                                Date varchar(20), \
                                PRIMARY KEY (FinId) \
                                ) DEFAULT CHARSET=utf8 ENGINE=INNODB \
                        ")

                print("Create IncomeStatment Table")
                # Table: IncomeStatment
                # 營業收入, 營業利益, 營業外收入及支出, 稅前淨利
                cursor.execute("create table IF NOT EXISTS IncomeStatement( \
                                InId INT AUTO_INCREMENT PRIMARY KEY, \
                                FinId INT, \
                                StockID INT NOT NULL, \
                                OpRevenue BIGINT, \
                                OpProfit BIGINT, \
                                NetIncome BIGINT, \
                                NonOpRevenueExpense BIGINT, \
                                RevenueBeforeTax BIGINT, \
                                Date varchar(20), \
                                FOREIGN KEY (FinId) REFERENCES FinancialStatement(FinId) \
                                ) DEFAULT CHARSET=utf8 ENGINE=INNODB \
                        ")

                print("Create CalStatment Table")
                # Table: CalStatment (Calculated Statment)
                # 基本每股盈餘, 每股參考淨值, ROE, ROA
                cursor.execute("create table IF NOT EXISTS CalStatement( \
                                CalId INT AUTO_INCREMENT PRIMARY KEY, \
                                FinId INT, \
                                StockID INT NOT NULL, \
                                EarningPerShare BIGINT, \
                                NetAssetPerShare BIGINT, \
                                ROE BIGINT, \
                                ROA BIGINT, \
                                Date varchar(20), \
                                FOREIGN KEY (FinId) REFERENCES FinancialStatement(FinId) \
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
