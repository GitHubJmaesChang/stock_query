#!/usr/bin/python
# -*- coding: utf-8 -*-
# merge basic_report to Q1~Q4

import os
import requests
import pandas as pd
import numpy
import csv, codecs, urllib, datetime, time, pdb
import copy

File_Location = 'D://Stock/finacial/'
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
        for chk in range(current_search_pos, current_search_pos + 10 ):
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

def merge_table(year, FilePath):
    table_numbs =0
    if year>=1000:
        year -= 1911

    FileName =  Table_name + str(year) + "_s"
    
# to check how many file in the folder "D://Stock/finacial/"
    for file in os.listdir(FilePath):
        if file.endswith(".csv"):
            table_numbs +=1
            File_idx = FilePath + FileName + str(table_numbs)+".csv"
            print File_idx
            if(os.path.join(FilePath, file) != File_idx):
                table_numbs -=1
                break

    print table_numbs
    if(table_numbs ==1):
        print ("only one table, can't be merge")

    max_length =[0,0];
    if(table_numbs >=2):
        Q1_table = pd.read_csv(FilePath + FileName + str(1) + ".csv")
        max_length[0]= 1
        max_length[1]= Q1_table.shape[0]
        Q2_table = pd.read_csv(FilePath + FileName + str(2) + ".csv")
        if(max_length>Q2_table.shape[0]):
            max_length[0]= 2
            max_length[1]= Q2_table.shape[0]        
        print "create two table"
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
    if(table_numbs==2):
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
    if(table_numbs ==3):
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
    if(table_numbs==4):
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

    stock_numbs = sorted(stock_numbs)
    print "add company name"
    company_name =[]
    company_name_temp =[]
    company_name = list(get_data_from_table_list(stock_numbs, Q1_table, Q1_table.columns[2]))
    if(table_numbs >= 2):
        company_name_temp = list(get_data_from_table_list(stock_numbs, Q2_table, Q2_table.columns[2]))
        update_list(company_name, company_name_temp)
    if(table_numbs >= 3):
        company_name_temp = list(get_data_from_table_list(stock_numbs, Q3_table, Q3_table.columns[2]))
        update_list(company_name, company_name_temp)
    if(table_numbs >= 4):
        company_name_temp = list(get_data_from_table_list(stock_numbs, Q4_table, Q4_table.columns[2]))
        update_list(company_name, company_name_temp)

    sotck_id_form = pd.DataFrame({ Q1_table.columns[1] : stock_numbs})
    name_form = pd.DataFrame({ Q1_table.columns[2] : company_name})
    df = pd.concat( [ sotck_id_form[Q1_table.columns[1] ],
                      name_form[Q1_table.columns[2]]], axis =1)

    df.to_csv( FilePath + "test" + str(1) + ".csv", encoding = "utf-8") 
    return 
    
    for idx in range(0, max_length[1]):
        if(table_numbs<=2):
            if(Q1_table.loc[idx][1] != Q2_table.loc[idx][1] ) :
                #Step 1 : check who's data has lost
                for c in range(idx ,Q2_table.shape[0]):
                    if(Q1_table.loc[idx][1] == Q2_table.loc[c][1]) :
                       lost_data_target_is_numb = Q1_TABLE
                       break
                    else:
                        lost_data_target_is_numb = Q2_TABLE
                if(lost_data_target_is_numb ==Q1_TABLE):
                    Q1_table = insert_row(idx, Q1_table, Q2_table.loc[idx])
                    print "Q1_table drop"
                if(lost_data_target_is_numb ==Q2_TABLE):
                    Q2_table = insert_row(idx, Q2_table, Q1_table.loc[idx])
                    print "Q2_table drop"
                if(Q1_table.columns[0] == "Unnamed: 0"):
                    Q1_table = Q1_table.drop([Q1_table.columns[0]], axis =1)

                if(Q2_table.columns[0] == "Unnamed: 0"):
                    Q2_table = Q2_table.drop([Q2_table.columns[0]], axis =1)
                print ("lost item at Q")+str(lost_data_target_is_numb) + ", position is " + str(idx)
     
if __name__ == '__main__':
    merge_table(2018, File_Location)
    
