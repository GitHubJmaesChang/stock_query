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
    init_db_utf8.InitDB("localhost", "root", "ftdi1234")
    add_db_record.ConnectDB("localhost", "stock", "ftdi1234")



# insert base_financail report into data base :

def database_InsertCompany(name_id, name):
    print("company ID = " + name_id + "name = " + name)
    add_db_record.InsertCompany((name_id), (name) )

def database_InsertFinancialStatement(stockID, asset, equity, date):
    add_db_record.InsertFinancialStatement((stockID), asset, equity, date)

def database_InsertIncomeStatement(stockid, oprevenu, opprofit, netincome, \
			nonoprevenueexpense, revenuebeforetax, date):
    
    add_db_record.InsertIncomeStatement((stockid), oprevenu, opprofit, netincome, \
			nonoprevenueexpense, revenuebeforetax, date)
        
def database_InsertCalStatement(stockid, eps, netaps, roe, roa, date):
    add_db_record.InsertCalStatement((stockid), eps, netaps, roe, roa, date)
    

def insertFinancailSeate_to_database(path, date, quarterly):

    sdate = date.split("-")
    year = sdate[0]
    month = sdate[1]
    day = sdate[2]
	
    file_name = str(year) + "_"+ str(quarterly) + "_financialStatement.csv"
    
    intial_db()
    
    if((0) == check_file_exist(path + file_name)):
        print(("insertFinancailSeate_to_database : No such file name : "), file_name)
        return (0)
    
    table = pd.read_csv(path + file_name)


    for idx in range(0, table.shape[0]):
        database_InsertCompany(str(table.iloc[idx]['公司代號']), str(table.iloc[idx]['公司名稱']))

        database_InsertFinancialStatement(str(table.iloc[idx]['公司代號']),str(table.iloc[idx]['資產總計']), \
                                          str(table.iloc[idx]['權益總計']),date)
        
        database_InsertIncomeStatement(str(table.iloc[idx]['公司代號']), str(table.iloc[idx]['營業收入']), \
                                       str(table.iloc[idx]['營業利益(損失)']), str(table.iloc[idx]['本期淨利(淨損)']), \
                                       str(table.iloc[idx]['營業外收入及支出']), str(table.iloc[idx]['稅前淨利(淨損)']), \
                                       date)
        
        database_InsertCalStatement(str(table.iloc[idx]['公司代號']),str(table.iloc[idx]['基本每股盈餘(元)']), \
                                    str(table.iloc[idx]['每股參考淨值']),str(table.iloc[idx]['ROE']), \
                                    str(table.iloc[idx]['ROA']), date)


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

    for idx in range(0, table.shape[0]):
        database_InsertCompany(str(table.iloc[idx]['公司代號']), str(table.iloc[idx]['公司名稱']))
        add_db_record.InsertMonthlyRevenue(str(table.iloc[idx]['公司代號']), str(int(table.iloc[idx]['當月營收'])), \
                                           str(int(table.iloc[idx]['上月營收'])), str(int(table.iloc[idx]['去年當月營收'])), \
                                           str(table.iloc[idx]['上月比較增減(%)']), str(table.iloc[idx]['去年同月增減(%)']), \
                                           str(table.iloc[idx]['當月累計營收']), str(table.iloc[idx]['去年累計營收']), \
                                           str(table.iloc[idx]['前期比較增減(%)']),date)


def inserFoundationExchangeDB(path, date):

    current_date = date.replace("-", "")
    file_name = current_date + "_FoundationExchange.csv"
    
    intial_db()    
    if((0) == check_file_exist(path + file_name)):
        print(("inserFoundationExchangeDB : No such file name : "), file_name)
        return (0)
    
    table = pd.read_csv(path + file_name)

    #Foreign_Investor_buy,Foreign_Investor_sell,Investment_Trust_buy,Investment_Trust_sell,Dealer_buy,Dealer_sell,Total
    for idx in range(0, table.shape[0]):
        database_InsertCompany(str(table.iloc[idx]['ID']), str(table.iloc[idx]['Name']))
        add_db_record.InsertFoundationExchange(str(table.iloc[idx]['ID']), str(int(table.iloc[idx]['Foreign_Investor_buy'])), \
                                               str(int(table.iloc[idx]['Foreign_Investor_sell'])), str(int(table.iloc[idx]['Investment_Trust_buy'])), \
                                               str(table.iloc[idx]['Investment_Trust_sell']), str(table.iloc[idx]['Dealer_buy']), \
                                               str(table.iloc[idx]['Dealer_sell']), str(table.iloc[idx]['Total']),date)


def insertInsertStockExchangeDB(path, date):

    current_date = date.replace("-", "")
    file_name = current_date + "_stockExchange.csv"
    
    intial_db()
    
    if((0) == check_file_exist(path + file_name)):
        print(("insertInsertStockExchangeDB : No such file name : "), file_name)
        return (0)
    
    table = pd.read_csv(path + file_name)

    #ID,Name,Volume,StrPrice,highPrice,lowPrice,EndPrice
    for idx in range(0, table.shape[0]):
        database_InsertCompany(str(table.iloc[idx]['ID']), str(table.iloc[idx]['Name']))
        add_db_record.InsertStockExchange(str(table.iloc[idx]['ID']), str(int(table.iloc[idx]['Volume'])), \
                                          str((table.iloc[idx]['StrPrice'])), str((table.iloc[idx]['highPrice'])), \
                                          str(table.iloc[idx]['lowPrice']), str(table.iloc[idx]['EndPrice']) ,date)
        

def insertInsertMarginTradeDB(path, date):

    current_date = date.replace("-", "")
    file_name = current_date + "_MarginTrade.csv"
    
    intial_db()
    
    if((0) == check_file_exist(path + file_name)):
        print(("insertInsertMarginTradeDB : No such file name : "), file_name)
        return (0)
    
    table = pd.read_csv(path + file_name)
    #,ID,Name,MarginTradebuy,MarginTradeSell,MarginTradeRemine,ShortSellBuy,ShortSellSell,ShortSellRemine
    for idx in range(0, table.shape[0]):
        database_InsertCompany(str(table.iloc[idx]['ID']), str(table.iloc[idx]['Name']))
        add_db_record.InsertMarginTrade(str(table.iloc[idx]['ID']), str(int(table.iloc[idx]['MarginTradeBuy'])), \
                                               str(int(table.iloc[idx]['MarginTradeSell'])), str(int(table.iloc[idx]['MarginTradeRemain'])), \
                                               str(table.iloc[idx]['ShortSellBuy']), str(table.iloc[idx]['ShortSellSell']) ,
                                               str(table.iloc[idx]['TotalVolume']), str(table.iloc[idx]['ChargeOff']), str(table.iloc[idx]['ShortSellRemain']),date)


def test_verify_financaStatement():
    insertFinancailSeate_to_database("./", "1","2017-05-15")
    print "process done"

        
if __name__ == '__main__':
    #insertMonthlyRevenueDB("./", "2018-09-01")
    #print("**********2018_9_MonthRevenue insert done***************")
    inserFoundationExchangeDB("./", "2018-11-05")
    print("**********20181105_FoundationExchange insert done***************")
    insertInsertStockExchangeDB("./", "2018-11-05")
    print("**********20181105_stockExchange insert done***************")
    insertInsertMarginTradeDB("./", "2018-11-05")
    print("**********20181105_MarginTrade insert done***************")

