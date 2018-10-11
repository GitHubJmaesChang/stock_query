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

def insert_date_into_database(file_name):
    intial_db()
    if(FALSE == check_file_exist(file_name)):
        return FALSE

    pd_form = pd.read_csv(file_name)
    return pd_form

    

if __name__ == '__main__':
    #path = os.path.dirname(os.path.abspath(__file__))
    #query_company_data.update_company_state(2018,1, path + "//fincial_report//")
    #company_id = pd.read_csv(path + "/fincial_report/" + comp_id)
    
    #for idx in range(0, company_id.shape[0]):
    #    query_stock_date.stock_query( str(company_id.iloc[idx][1]), path + "//stock_report//")
    #    time.sleep(5)

    target_file = File_Path + "basic_report107_s1.csv"
    print "save data to DB = " + (insert_date_into_database(target_file))
    
    print "process done"
