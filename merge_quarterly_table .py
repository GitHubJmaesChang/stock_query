#!/usr/bin/python
# -*- coding: utf-8 -*-
# merge basic_report to Q1~Q4

import os
import requests
import pandas as pd
import numpy
import csv, codecs, urllib, datetime, time, pdb
import copy

File_Location = 'D:/Stock/finacial/'
Table_name    = "basic_report"

NO_UPDATE = 0
Q1_TABLE = 1
Q2_TABLE = 2
Q3_TABLE = 3
Q4_TABLE = 4

def check_report(FileName, FilePath):
    open_status = 0
    File_idx = FilePath + FileName + ".csv"
    print ("open file path at \\", File_idx)
    try:
        f = open(File_idx, 'r')
        open_status = 1
    except ValueError:
        print("No such file at" , File_idx)
    return open_status


def insert_row(idx, df, df_insert):
    dfA = df.iloc[:idx, ]
    dfB = df.iloc[idx:, ]
    df = dfA.append(df_insert).append(dfB).reset_index(drop = True)
    return df

# in order to reduce the trace resource, we mask the max search length = 10
def get_data_from_table_list(stock_numbs_table, Qx_target_table, column_idx):
    current_search_pos = 0
    searched = 0
    row=[]
    for idx in range(0, len(stock_numbs_table)):
        for chk in range(current_search_pos, current_search_pos + 20 ):
            if(stock_numbs_table[idx] == Qx_target_table.loc[current_search_pos][1]):
                row.append(Qx_target_table.loc[current_search_pos][column_idx])
                current_search_pos+=1
                searched =1
                break
            else:
                searched =0
        if(searched ==0):
            row.append(0)
    return row

def update_list(cmp1, cmp2):
    for idx in range(0, len(cmp1)):
        if(cmp1[idx] == 0 and (cmp2[idx])):
            cmp1[idx] = cmp2[idx]

def add_data_to_list(stock_numb_table, Qx_table, column):
    row = [ 0 for x in range(len(stock_numb_table))]
    checked =0
    for idx in range(0, len(stock_numb_table)):
        for chk in range(checked, checked+10):
            if(stock_numb_table[idx] == Qx_table.loc[chk][1]):
                row[idx] = (Qx_table.loc[chk][column])
                checked+=1
                break

    return row
    

def merge_table(year, FilePath):
    table_numbs =0
    if year>=1000:
        year -= 1911

    FileName =  Table_name + str(year) + "_s"
    
# to check how many file in the folder "D://Stock/finacial/"
    table_numbs =0
    for file in os.listdir(FilePath):
        if file.endswith(".csv"):
            File_idx = FilePath + FileName + str(table_numbs+1)+".csv"
            if(os.path.join(FilePath, file) == File_idx):
                table_numbs +=1

    print table_numbs
    if(table_numbs <=1):
        print ("only one table, can't be merge")
        return

    max_length =[0,0];
    if(table_numbs >=2):
        Q1_table = pd.read_csv(FilePath + FileName + str(1) + ".csv")
        max_length[0]= 1
        max_length[1]= Q1_table.shape[0]
        Q2_table = pd.read_csv(FilePath + FileName + str(2) + ".csv")
        if(max_length>Q2_table.shape[0]):
            max_length[0]= 2
            max_length[1]= Q2_table.shape[0]
        print ("max- length at Q", max_length[0],"L=", max_length[1])

    if(table_numbs >=3):
        Q3_table = pd.read_csv(FilePath + FileName + str(3) + ".csv")
        if(max_length>Q3_table.shape[0]):
            max_length[0]= 3
            max_length[1]= Q3_table.shape[0]


    if(table_numbs >=4):
        Q4_table = pd.read_csv(FilePath + FileName + str(4) + ".csv")
        if(max_length>Q4_table.shape[0]):
            max_length[0]= 4
            max_length[1]= Q4_table.shape[0]

    # be used to check which table lost items
    lost_data_target_is_numb =0
    update_table = 0
   
    stock_numbs=[]
  #add Q1 company id at first
    for idx in range(0, Q1_table.shape[0]):
        stock_numbs.append(Q1_table.loc[idx][1])

  # Q2 table vs Q1 list
    print "check Q2 table"
    numbs_idx =0
    if(table_numbs>=2):
        for idx in range(0, Q2_table.shape[0]):
            if(stock_numbs[numbs_idx] != Q2_table.loc[idx][1]):
                update_table = Q1_TABLE
                for ch in range(numbs_idx, len(stock_numbs)):
                    if(Q2_table.loc[idx][1] == stock_numbs[ch]):
                        update_table = NO_UPDATE
                        #update the index to correct position
                        numbs_idx = ch
                        break
                if(update_table == Q1_TABLE):
                    stock_numbs.insert(numbs_idx, Q2_table.loc[idx][1])

    print "check Q2 table done"
   # Q3 table vs Q1 list
    numbs_idx =0
    if(table_numbs >=3):
        for idx in range(0, Q3_table.shape[0]):
            if(stock_numbs[numbs_idx] != Q3_table.loc[idx][1]):
                update_table = Q3_TABLE
                for ch in range(numbs_idx, len(stock_numbs)):
                    if(Q3_table.loc[idx][1] == stock_numbs[ch]):
                        update_table = NO_UPDATE
                        #update the index to correct position
                        numbs_idx = ch
                        break
                if(update_table == Q3_TABLE):
                    stock_numbs.insert(numbs_idx, Q3_table.loc[idx][1])


   # Q4 table vs Q1 list
    numbs_idx =0
    if(table_numbs>=4):
        for idx in range(0, Q4_table.shape[0]):
            if(stock_numbs[numbs_idx] != Q4_table.loc[idx][1]):
                update_table = Q4_TABLE
                for ch in range(numbs_idx, len(stock_numbs)):
                    if(Q4_table.loc[idx][1] == stock_numbs[ch]):
                        update_table = NO_UPDATE
                        #update the index to correct position
                        numbs_idx = ch
                        break
                if(update_table == Q4_TABLE):
                    stock_numbs.insert(numbs_idx, Q4_table.loc[idx][1])

    
    check_repeat = []
    [check_repeat.append(x) for x in stock_numbs if x not in check_repeat]
    stock_numbs = check_repeat
    
    stock_numbs = sorted(stock_numbs)
    print "add company name"
    company_name =[]
    company_name_temp =[]
    company_name = list(get_data_from_table_list(stock_numbs, Q1_table, Q1_table.columns[2]))
    if(table_numbs >= 2):
        print "add Q2 "
        company_name_temp = list(get_data_from_table_list(stock_numbs, Q2_table, Q2_table.columns[2]))
        update_list(company_name, company_name_temp)
    if(table_numbs >= 3):
        print "add Q3 "
        company_name_temp = list(get_data_from_table_list(stock_numbs, Q3_table, Q3_table.columns[2]))
        update_list(company_name, company_name_temp)
    if(table_numbs >= 4):
        print "add Q4 "
        company_name_temp = list(get_data_from_table_list(stock_numbs, Q4_table, Q4_table.columns[2]))
        update_list(company_name, company_name_temp)



    #prepare other data
    sotck_info_Q1 = [[0 for x in range(len(stock_numbs))] for y in range(len(Q1_table.columns)-2)]
    sotck_info_Q2 = [[0 for x in range(len(stock_numbs))] for y in range(len(Q1_table.columns)-2)]
    sotck_info_Q3 = [[0 for x in range(len(stock_numbs))] for y in range(len(Q1_table.columns)-2)]
    sotck_info_Q4 = [[0 for x in range(len(stock_numbs))] for y in range(len(Q1_table.columns)-2)]
   
    print "start merge data, total columns", len(Q1_table.columns), "items = ",Q1_table.columns 
    #capture data from column index 3
    for idx in range(0, (len(Q1_table.columns)-3)):
        print "to merge index at ", idx+3
        if(table_numbs>=2):
           sotck_info_Q1[idx] = list(add_data_to_list(stock_numbs, Q1_table, idx+3))
           sotck_info_Q2[idx] = list(add_data_to_list(stock_numbs, Q2_table, idx+3))
        if(table_numbs>=3):
           sotck_info_Q3[idx] = list(add_data_to_list(stock_numbs, Q3_table, idx+3))
        if(table_numbs>=4):
           sotck_info_Q4[idx] = list(add_data_to_list(stock_numbs, Q4_table, idx+3))
           
    data_Q ={}
    columns_list =[]
    data_Q.update({Q1_table.columns[1]: stock_numbs})
    columns_list.append(Q1_table.columns[1])
    data_Q.update({Q1_table.columns[2]: company_name})
    columns_list.append(Q1_table.columns[2])
    # total 14 items
    for column_idx in range(0, len(Q1_table.columns)-3):
        columns_list.append("Q1 "+ Q1_table.columns[column_idx+3])
        columns_list.append("Q2 "+ Q1_table.columns[column_idx+3])
        columns_list.append("Q3 "+ Q1_table.columns[column_idx+3])
        columns_list.append("Q4 "+ Q1_table.columns[column_idx+3])
        data_Q.update({"Q1 "+ Q1_table.columns[column_idx+3]: sotck_info_Q1[column_idx]})
        data_Q.update({"Q2 "+ Q1_table.columns[column_idx+3]: sotck_info_Q2[column_idx]})
        data_Q.update({"Q3 "+ Q1_table.columns[column_idx+3]: sotck_info_Q3[column_idx]})
        data_Q.update({"Q4 "+ Q1_table.columns[column_idx+3]: sotck_info_Q4[column_idx]})
       
    #prepare stock number and stock name
    data_form     = pd.DataFrame(data_Q, columns = columns_list)
    data_form.to_csv( FilePath + "Q1_Q4_"+str(year)+ ".csv", encoding = "utf-8")
    
    return 
     
if __name__ == '__main__':
    merge_table(2018, File_Location)
