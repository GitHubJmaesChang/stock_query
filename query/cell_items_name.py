#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

fundation_table_request= {
   '2013' : [u'證券代號', u'證券名稱', u'外資買進股數', u'外資賣出股數', u'投信買進股數', u'投信賣出股數', u'自營商買進股數', u'自營商賣出股數', u'三大法人買賣超股數' ] ,
   '2014' : [u'證券代號', u'證券名稱', u'外資買進股數', u'外資賣出股數', u'投信買進股數', u'投信賣出股數', u'自營商買進股數', u'自營商賣出股數', u'三大法人買賣超股數' ] ,
   '2015' : [u'證券代號', u'證券名稱', u'外資買進股數', u'外資賣出股數', u'投信買進股數', u'投信賣出股數', u'自營商買進股數(自行買賣)', u'自營商賣出股數(自行買賣)', u'三大法人買賣超股數' ] ,
   '2016' : [u'證券代號', u'證券名稱', u'外資買進股數', u'外資賣出股數', u'投信買進股數', u'投信賣出股數', u'自營商買進股數(自行買賣)', u'自營商賣出股數(自行買賣)', u'三大法人買賣超股數' ] ,
   '2017' : [u'證券代號', u'證券名稱', u'外資買進股數', u'外資賣出股數', u'投信買進股數', u'投信賣出股數', u'自營商買進股數(自行買賣)', u'自營商賣出股數(自行買賣)', u'三大法人買賣超股數' ] ,
   '2018' : [u'證券代號', u'證券名稱', u'外陸資買進股數(不含外資自營商)', u'外陸資賣出股數(不含外資自營商)',\
             u'投信買進股數', u'投信賣出股數', u'自營商買進股數(自行買賣)', u'自營商賣出股數(自行買賣)', u'三大法人買賣超股數'] ,}


balance_sheet = {
   1 : [u'現金及約當現金'],
   2 : [u'應收票據淨額', u'應收帳款淨額', u'應收帳款－關係人淨額', u'其他應收款', u'其他應收款－關係人'], 
   3 : [u'存貨'],
   4 : [u'預付款項'],
   5 : [u'流動資產合計'],
   6 : [u'非流動資產合計'],
   7 : [u'資產總計'],
   8 : [u'短期借款', u'應付帳款', u'應付帳款－關係人', u'其他應付款'],
   9 : [u'流動負債合計'],
   10 : [u'長期借款'],
   11 : [u'非流動負債合計'],
   12 : [u'負債總計'],
   13 : [u'普通股股本'],
   14 : [u'權益總額'],
   15 : [u'負債及權益總計'],
   }

cash_flow_sheet={
   1 : [u'營業收入合計'],
   2 : [u'營業成本合計'], 
   3 : [u'營業毛利（毛損）淨額'], 
   4 : [u'推銷費用', u'管理費用', u'研究發展費用', u'其他費用', u'營業費用合計'],
   5 : [u'營業利益（損失）'],
   6 : [u'營業外收入及支出合計'],
   7 : [u'繼續營業單位稅前淨利（淨損）'],
   8 : [u'本期淨利（淨損）'],
   9 : [u'母公司業主（淨利／損）'],
   10 : [u'基本每股盈餘合計'],
   }

income_statement_sheet={
   1 : [u'營業活動之淨現金流入（流出）'],
   2 : [u'投資活動之淨現金流入（流出）'], 
   3 : [u'籌資活動之淨現金流入（流出）'], 
   4 : [u'匯率變動對現金及約當現金之影響'],
   5 : [u'本期現金及約當現金增加（減少）數'],
   6 : [u'期初現金及約當現金餘額'],
   7 : [u'期末現金及約當現金餘額'],
   8 : [u'資產負債表帳列之現金及約當現金'],
   }



def information():
   print (fundation_table_request["2013"][0])

if  __name__ == '__main__':
   #information()
   print (balance_sheet)
