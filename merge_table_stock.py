#!/usr/bin/python
# -*- coding: utf-8 -*-
# merge basic_report to Q1~Q4

import os
import requests
import pandas as pd
import numpy as np
import csv, codecs, urllib, datetime, time, pdb

File_Location = 'D://Stock/finacial/'
Table_name    = "basic_report"

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
    df = df.drop([df.columns[0]], axis =1)
    return df

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
    
    for idx in range(0, max_length[1]):
        if(table_numbs<=2):
            if(Q1_table[u'公司代號'.encode('utf-8')][idx] != Q2_table[u'公司代號'.encode('utf-8')][idx] ) :
                print Q1_table[u'公司代號'.encode('utf-8')][idx]
                print Q2_table[u'公司代號'.encode('utf-8')][idx]
                #Step 1 : check who's data has lost
                for c in range(idx ,Q2_table.shape[0]):
                    if(Q1_table[u'公司代號'.encode('utf-8')][idx] == Q2_table[u'公司代號'.encode('utf-8')][c]) :
                       lost_data_target_is_numb = Q1_TABLE
                       break
                    else:
                        lost_data_target_is_numb = Q2_TABLE
                if(lost_data_target_is_numb ==Q1_TABLE):
                    Q1_table = insert_row(idx, Q1_table, Q2_table.loc[idx][2:])
                    print Q1_table
                    print Q2_table
                    print "Q1_table drop"
                if(lost_data_target_is_numb ==Q2_TABLE):
                    Q2_table = insert_row(idx, Q2_table, Q1_table.loc[idx][2:])
                    print "Q2_table drop"
                print ("lost item at Q")+str(lost_data_target_is_numb) + ", position is " + str(idx)
                break;

    Q1_table.to_csv(FilePath + FileName + str(1) + "1.csv", encoding = "utf-8")
    Q2_table.to_csv(FilePath + FileName + str(2) + "2.csv", encoding = "utf-8")
     
if __name__ == '__main__':
    merge_table(2018, File_Location)
    
