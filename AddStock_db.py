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
    init_db_utf8.InitDB()
    add_db_record.ConnectDB("10.34.0.100", "stock")



# insert base_financail report into data base :

def database_InsertCompany(name_id, name):
    add_db_record.InsertCompany((name_id), (name) )

def database_InsertFinancialStatement(stockID, asset, equity, date):
    add_db_record.InsertFinancialStatement((stockID), asset, equity, date)

def database_InsertIncomeStatement(stockid, oprevenu, opprofit, netincome, \
			nonoprevenueexpense, revenuebeforetax, date):
    
    add_db_record.InsertIncomeStatement((stockid), oprevenu, opprofit, netincome, \
			nonoprevenueexpense, revenuebeforetax, date)
        
def database_InsertCalStatement(stockid, eps, netaps, roe, roa, date):
    add_db_record.InsertCalStatement((stockid), eps, netaps, roe, roa, date)
    

def insertFinancailSeate_to_database(file_name, date):
    intial_db()
    
    if((0) == check_file_exist(file_name)):
        print(("insertFinancailSeate_to_database : No such file name : "), file_name)
        return (0)
    
    table = pd.read_csv(file_name)


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


def test_verify_financaStatement():
    target_file = File_Path + "basic_report106_s1.csv"
    print target_file
    insertFinancailSeate_to_database(target_file, "2017-05-15")
    
    target_file = File_Path + "basic_report106_s2.csv"
    print target_file
    insertFinancailSeate_to_database(target_file, "2017-08-14")

    target_file = File_Path + "basic_report106_s3.csv"
    print target_file
    insertFinancailSeate_to_database(target_file, "2017-10-31")

    target_file = File_Path + "basic_report106_s4.csv"
    print target_file
    insertFinancailSeate_to_database(target_file, "2018-03-31")

    target_file = File_Path + "basic_report107_s1.csv"
    print target_file
    insertFinancailSeate_to_database(target_file, "2018-05-15")

    target_file = File_Path + "basic_report107_s2.csv"
    print target_file
    insertFinancailSeate_to_database(target_file, "2018-08-14")
    print "process done"

def insertMonthlyRevenueDB(file_name, date):

    intial_db()
    
    if((0) == check_file_exist(file_name)):
        print(("insertMonthlyRevenueDB : No such file name : "), file_name)
        return (0)
    
    table = pd.read_csv(file_name)

    for idx in range(0, table.shape[0]):
        database_InsertCompany(str(table.iloc[idx]['公司代號']), str(table.iloc[idx]['公司名稱']))
        add_db_record.InsertMonthlyRevenue(str(table.iloc[idx]['公司代號']), str(int(table.iloc[idx]['當月營收'])), \
                                           str(int(table.iloc[idx]['上月營收'])), str(int(table.iloc[idx]['去年當月營收'])), \
                                           str(table.iloc[idx]['上月比較增減(%)']), str(table.iloc[idx]['去年同月增減(%)']), \
                                           str(table.iloc[idx]['當月累計營收']), str(table.iloc[idx]['去年累計營收']), \
                                           str(table.iloc[idx]['前期比較增減(%)']),date)


def inserFoundationExchangeDB(file_name, date):

    intial_db()    
    if((0) == check_file_exist(file_name)):
        print(("inserFoundationExchangeDB : No such file name : "), file_name)
        return (0)
    
    table = pd.read_csv(file_name)

    #Foreign_Investor_buy,Foreign_Investor_sell,Investment_Trust_buy,Investment_Trust_sell,Dealer_buy,Dealer_sell,Total
    for idx in range(0, table.shape[0]):
        database_InsertCompany(str(table.iloc[idx]['ID']), str(table.iloc[idx]['Name']))
        add_db_record.InsertFoundationExchange(str(table.iloc[idx]['ID']), str(int(table.iloc[idx]['Foreign_Investor_buy'])), \
                                               str(int(table.iloc[idx]['Foreign_Investor_sell'])), str(int(table.iloc[idx]['Investment_Trust_buy'])), \
                                               str(table.iloc[idx]['Investment_Trust_sell']), str(table.iloc[idx]['Dealer_buy']), \
                                               str(table.iloc[idx]['Dealer_sell']), str(table.iloc[idx]['Total']),date)


def insertInsertStockExchangeDB(file_name, date):

    intial_db()
    
    if((0) == check_file_exist(file_name)):
        print(("insertInsertStockExchangeDB : No such file name : "), file_name)
        return (0)
    
    table = pd.read_csv(file_name)

    #ID,Name,Volume,StrPrice,highPrice,lowPrice,EndPrice
    for idx in range(0, table.shape[0]):
        database_InsertCompany(str(table.iloc[idx]['ID']), str(table.iloc[idx]['Name']))
        add_db_record.InsertStockExchange(str(table.iloc[idx]['ID']), str(int(table.iloc[idx]['Volume'])), \
                                          str((table.iloc[idx]['StrPrice'])), str((table.iloc[idx]['highPrice'])), \
                                          str(table.iloc[idx]['lowPrice']), str(table.iloc[idx]['EndPrice']) ,date)
        

def insertInsertMarginTradeDB(file_name, date):

    intial_db()
    
    if((0) == check_file_exist(file_name)):
        print(("insertInsertMarginTradeDB : No such file name : "), file_name)
        return (0)
    
    table = pd.read_csv(file_name)
    #,ID,Name,MarginTradebuy,MarginTradeSell,MarginTradeRemine,ShortSellBuy,ShortSellSell,ShortSellRemine
    for idx in range(0, table.shape[0]):
        database_InsertCompany(str(table.iloc[idx]['ID']), str(table.iloc[idx]['Name']))
        add_db_record.InsertMarginTrade(str(table.iloc[idx]['ID']), str(int(table.iloc[idx]['MarginTradeBuy'])), \
                                               str(int(table.iloc[idx]['MarginTradeSell'])), str(int(table.iloc[idx]['MarginTradeRemain'])), \
                                               str(table.iloc[idx]['ShortSellBuy']), str(table.iloc[idx]['ShortSellSell']) ,str(table.iloc[idx]['ShortSellRemain']),date)
        
if __name__ == '__main__':
    #insertMonthlyRevenueDB("D:/Stock/finacial/2018_9_MonthlyRevenue.csv", "2018-09-01")
    #inserFoundationExchangeDB("D:/Stock/finacial/20181105_FoundationExchange.csv", "2018-11-05")
    #insertInsertStockExchangeDB("D:/Stock/finacial/20181105_stockExchange.csv", "2018-11-05")
    insertInsertMarginTradeDB("D:/Stock/finacial/20181105_MarginTrade.csv", "2018-11-05")

