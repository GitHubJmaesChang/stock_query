#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import pandas as pd
import time

from query import query_company_id
from query import query_financialStatement
from query import query_institutional_investors_info
from query import query_margin_and_short_trade
from query import query_month_income
from query import query_stock_dailydata
from query import query_stock_info_by_ID

from db import init_db_utf8
from db import add_db_record

TRUE  = 1
FALSE = 0

comp_id   = 'comp_id.csv'
File_Path = "D:/Stock/finacial/"


def check_file_exist(filename):
    if(os.path.isfile(filename)):
        return TRUE
    else:
        return FALSE


# crate database : 
def intial_db():
    init_db_utf8.InitDB()
    add_db_record.ConnectDB("localhost", "stock")

# update company ID
def data_query_company_id():
    query_company_id.query_public_trade_company_ID()

# 
def data_query_financialStatement(path, year,season):
    query_financialStatement.update_company_state(year, season, path)

def data_query_financialStatement_to_db(path, year,season):
    query_financialStatement.Stock_roe_roa_eps_prepare(year, season, path)

def data_query_institutional_investors_info(path, date):
    query_institutional_investors_info.daily_institutional_info(File_Path , "20181001")
    
def data_query_margin_and_short_trade(path, date):
    query_margin_and_short_trade.daily_information(File_Path , "20181002")
    
def data_query_month_income(path, date):
    query_month_income.monthly_report(File_Path, 2018, 8)
    
def data_query_stock_dailydata(path, date):
    query_stock_dailydata.daily_information(File_Path , "20181001")
    
def data_query_stock_info_by_ID(path, Stock_id):
    query_stock_info_by_ID.stock_query(Stock_id, path)


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
    

def insert_date_into_database(file_name, date):
    intial_db()
    
    if(FALSE == check_file_exist(file_name)):
        return FALSE
    
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


if __name__ == '__main__':
    target_file = File_Path + "basic_report106_s1.csv"
    print target_file
    insert_date_into_database(target_file, "2017-05-15")
    
    target_file = File_Path + "basic_report106_s2.csv"
    print target_file
    insert_date_into_database(target_file, "2017-08-14")

    target_file = File_Path + "basic_report106_s3.csv"
    print target_file
    insert_date_into_database(target_file, "2017-10-31")

    target_file = File_Path + "basic_report106_s4.csv"
    print target_file
    insert_date_into_database(target_file, "2018-03-31")

    target_file = File_Path + "basic_report107_s1.csv"
    print target_file
    insert_date_into_database(target_file, "2018-05-15")

    target_file = File_Path + "basic_report107_s2.csv"
    print target_file
    insert_date_into_database(target_file, "2018-08-14")
    print "process done"
