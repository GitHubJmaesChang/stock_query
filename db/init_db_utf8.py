#!/usr/bin/python
# -*- coding: utf_8 -*-

import MySQLdb as MS
import datetime
import warnings


def dbgPrint(s):
	ts = str(datetime.datetime.now())
	print("[" + ts + "]:" + str(s))

def InitDB( dbhost, dbuser,dbpassword):
	db = MS.connect(host=dbhost,  # the host
		user=dbuser,       # username
		passwd=dbpassword,
		charset='utf8mb4',
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
	if (res == (-1)):
		return(-1)

	return(0)


def CreatFinancialTable(db):

	try:
		cursor = db.cursor()

		print("Create Company Table")
		# Table: Company 
		# 公司代號, 公司名稱
		# colums are created in the order as listed above.
		cursor.execute("create table IF NOT EXISTS Company( \
				CoId INT AUTO_INCREMENT PRIMARY KEY, \
				StockID INT NOT NULL, \
				CompanyName varchar(100) \
				) DEFAULT CHARSET=utf8 ENGINE=INNODB \
			") 

		print("Create Company Group Table")
		# Table: Company 
		# 公司代號, 產業別
		# colums are created in the order as listed above.
		cursor.execute("create table IF NOT EXISTS CompanyGroup( \
			FinId INT AUTO_INCREMENT PRIMARY KEY, \
			CoId INT NOT NULL,\
			CompanyGroup varchar(20), \
			FOREIGN KEY (CoId) REFERENCES Company(CoId) \
			) DEFAULT CHARSET=utf8 ENGINE=INNODB \
			")

		print("Create BalanceStatementSheet Table")
                #現金及約當現金 : Cash_and_cash_equivalents 
                #應收票據淨額 : Notes_receivable_net
                #應收帳款淨額 : Accounts_receivable_net 
                #應收帳款－關係人淨額 : Accounts_receivable_related_net
                #其他應收款 : Others_accounts_receivable
                #其他應收款－關係人 : Others_accounts_receivable_related
                #存貨 :Inventories 
                #預付款項 : Prepayments 
                #流動資產合計 TotalCurrentAssets
                #非流動資產合計 TotalNonCurrentAssets
                #資產總計 TotalAssets
                #短期借款 Short_term_debt 
                #應付帳款 Accounts_payable
                #應付帳款－關係人 Accounts_payable_related
                #其他應付款 Other_Accounts_payable
                #流動負債合計 TotalCurrentDebt
                #長期借款  long_term_debt_payable
                #非流動負債合計 TotalNonCurrentDebt
                #負債總計 TotalLiabilities
                #普通股股本 capital_common_stock
                #權益總計 Total_equity
                #負債及權益總計 Total_liabilities_and_equity
		# colums are created in the order as listed above.
		
		cursor.execute("create table IF NOT EXISTS BalanceStatementSheet( \
			FinId INT AUTO_INCREMENT PRIMARY KEY, \
			CoId INT NOT NULL, \
			CashAndCashEquivalents BIGINT, \
			NotesReceivableNet BIGINT, \
			AccountsReceivableNet BIGINT, \
			AccountsReceivableRelatedNet BIGINT, \
			OthersAccountsReceivable BIGINT, \
			OthersAccountsReceivableRelated BIGINT, \
			Inventories BIGINT, \
			Prepayments BIGINT, \
			TotalCurrentAssets BIGINT, \
			TotalNonCurrentAssets BIGINT, \
			TotalAssets BIGINT, \
			ShortTermDebt BIGINT, \
			AccountsPayable BIGINT, \
			AccountsPayableRelated BIGINT, \
			OtherAccountsPayable BIGINT, \
			TotalCurrentDebt BIGINT, \
			LongTermDebtPayable BIGINT, \
			TotalNonCurrentDebt BIGINT, \
			TotalLiabilities BIGINT, \
			CapitalCommonStock BIGINT, \
			TotalEquity BIGINT, \
			TotalLiabilitiesAndEquity BIGINT, \
			Date varchar(20), \
			FOREIGN KEY (CoId) REFERENCES Company(CoId) \
			) DEFAULT CHARSET=utf8 ENGINE=INNODB \
			")

		print("Create IncomeStatementSheet Table")
                
                #營業收入合計 GrossSales
                #營業成本合計 CostOfGoodsSold
                #營業毛利（毛損）淨額 GrossProfitNet
                #推銷費用 CostPromotion
                #管理費用 CostADM
                #研究發展費用 CostExpenseRD
                #其他費用 CostOther
                #營業費用合計 TotalCostOfExpenses
                #營業利益（損失） OperateIncome
                #營業外收入及支出合計 TotalNonOpIncome
                #繼續營業單位稅前淨利（淨損） PreTaxIncome
                #本期淨利（淨損）PureIncome
                #母公司業主（淨利／損） CNIS (Consolidated Net Income Attributed to Stockholders of the Company)

		cursor.execute("create table IF NOT EXISTS IncomeStatementSheet( \
			FinId INT AUTO_INCREMENT PRIMARY KEY, \
			CoId INT NOT NULL, \
			GrossSales BIGINT, \
			CostOfGoodsSold BIGINT, \
			GrossProfitNet BIGINT, \
			CostPromotion BIGINT, \
			CostADM BIGINT, \
			CostExpenseRD BIGINT, \
			CostOther BIGINT, \
			TotalCostOfExpenses BIGINT, \
			OperateIncome BIGINT, \
			TotalNonOpIncome BIGINT, \
			PreTaxIncome BIGINT, \
			PureIncome BIGINT, \
			CNIS BIGINT, \
			Date varchar(20), \
			FOREIGN KEY (CoId) REFERENCES Company(CoId) \
			) DEFAULT CHARSET=utf8 ENGINE=INNODB \
			")
		print("Create CashStatementSheet Table")
                
                #營業活動之淨現金流入（流出）OperatingCashFlows
                #投資活動之淨現金流入（流出）InvestCashProvided
                #籌資活動之淨現金流入（流出）FinanceCashFlows
                #匯率變動對現金及約當現金之影響  ExchangeRateChangeOnCash
                #本期現金及約當現金增加（減少）數 CashNetIncrease
                #期初現金及約當現金餘額 StartCashOfYear
                #期末現金及約當現金餘額 EndCashOfYear

		cursor.execute("create table IF NOT EXISTS CashStatementSheet( \
			FinId INT AUTO_INCREMENT PRIMARY KEY, \
			CoId INT NOT NULL, \
			OperatingCashFlows BIGINT, \
			InvestCashProvided BIGINT, \
			FinanceCashFlows BIGINT, \
			ExchangeRateChangeOnCash BIGINT, \
			CashNetIncrease BIGINT, \
			StartCashOfYear BIGINT, \
			EndCashOfYear BIGINT, \
			Date varchar(20), \
			FOREIGN KEY (CoId) REFERENCES Company(CoId) \
			) DEFAULT CHARSET=utf8 ENGINE=INNODB \
			")

		print("Create CompanyEstimateSheet Table")
                #母公司淨利比例 OriginalIncomeRate
                #業外占營收比例 OutIncomeRate
                #存貨周轉率 InventoryTurnoverRate
                #毛利率 GrossMarginRate
                #營業利益 OrgProfitRate
                #淨利率 PurIncomeRate
                #ROE_Org
                #ROE
                #ROE
		#EPS
		cursor.execute("create table IF NOT EXISTS CompanyEstimateSheet( \
			FinId INT AUTO_INCREMENT PRIMARY KEY, \
			CoId INT NOT NULL, \
			OriginalIncomeRate DOUBLE, \
			OutIncomeRate DOUBLE, \
			InventoryTurnoverRate DOUBLE, \
			GrossMarginRate DOUBLE, \
			OrgProfitRate DOUBLE, \
			PurIncomeRate DOUBLE, \
			ROE_Org DOUBLE, \
			ROE DOUBLE, \
			ROA DOUBLE, \
			EPS DOUBLE, \
			Date varchar(20), \
			FOREIGN KEY (CoId) REFERENCES Company(CoId) \
			) DEFAULT CHARSET=utf8 ENGINE=INNODB \
			")             

		print("Create FinancialStatement Table")
		# Table: FinancialStatement
		# 資產總額/總計, 權益總額/總計
		# colums are created in the order as listed above.
		cursor.execute("create table IF NOT EXISTS FinancialStatement( \
			FinId INT AUTO_INCREMENT PRIMARY KEY, \
			CoId INT NOT NULL, \
			TotalAsset BIGINT, \
			TotalEquity BIGINT, \
			Date varchar(20), \
			FOREIGN KEY (CoId) REFERENCES Company(CoId) \
			) DEFAULT CHARSET=utf8 ENGINE=INNODB \
			")


		print("Create IncomeStatment Table")
		# Table: IncomeStatment
		# 營業收入,營業利益(損失), 本期淨利(淨損), 營業外收入及支出, 稅前淨利(淨損)
		cursor.execute("create table IF NOT EXISTS IncomeStatement( \
			InId INT AUTO_INCREMENT PRIMARY KEY, \
			CoId INT NOT NULL, \
			OpRevenue BIGINT, \
			OpProfit BIGINT, \
			NetIncome BIGINT, \
			NonOpRevenueExpense BIGINT, \
			RevenueBeforeTax BIGINT, \
			Date varchar(20), \
			FOREIGN KEY (CoId) REFERENCES Company(CoId) \
			) DEFAULT CHARSET=utf8 ENGINE=INNODB \
			")

		print("Create CalStatment Table")
		# Table: CalStatment (Calculated Statment)
		# 基本每股盈餘, 每股參考淨值, ROE, ROA
		cursor.execute("create table IF NOT EXISTS CalStatement( \
			CalId INT AUTO_INCREMENT PRIMARY KEY, \
			CoId INT NOT NULL, \
			EarningPerShare DOUBLE, \
			NetAssetPerShare DOUBLE, \
			ROE DOUBLE, \
			ROA DOUBLE, \
			Date varchar(20), \
			FOREIGN KEY (CoId) REFERENCES Company(CoId) \
			) DEFAULT CHARSET=utf8 ENGINE=INNODB \
			")


		print("Create Stock excahnge Table")
		# Table: CalStatment (Calculated Statment)
		# 成交量, 開盤價格, 盤中最高價, 盤中最低價, 收盤價, 日期
		cursor.execute("create table IF NOT EXISTS StockExchange( \
			ExcId INT AUTO_INCREMENT PRIMARY KEY, \
			CoId INT NOT NULL, \
			ExchangeVolume BIGINT, \
			StartPrice DOUBLE, \
			HighPrice DOUBLE, \
			LowPrice DOUBLE, \
			EndPrice DOUBLE, \
			Category INT, \
			Date varchar(20), \
			FOREIGN KEY (CoId) REFERENCES Company(CoId) \
			) DEFAULT CHARSET=utf8 ENGINE=INNODB \
			")

		print("Create foundation excahnge Table")
		# Table: FoundationExchange
		# 外資買入, 外資賣出, 投信商買入, 投信商賣出, 自營商買入, 自營商賣出, 當日總量, 日期    
		cursor.execute("create table IF NOT EXISTS FoundationExchange( \
			FexId INT AUTO_INCREMENT PRIMARY KEY, \
			CoId INT NOT NULL, \
			ForeignInvestorBuy BIGINT, \
			ForeignInvestorSell BIGINT, \
			InvestmentTrustBuy BIGINT, \
			InvestmentTrustSell BIGINT, \
			DealerBuy BIGINT, \
			DealerSell BIGINT, \
			TotalVolume BIGINT, \
			Category INT, \
			Date varchar(20), \
			FOREIGN KEY (CoId) REFERENCES Company(CoId) \
			) DEFAULT CHARSET=utf8 ENGINE=INNODB \
			")

		print("Create Month FoundationExchange Table")
		# Table: MonthRevenue
		#當月營收,上月營收,去年當月營收,上月比較增減(%),去年同月增減(%),當月累計營收,去年累計營收,前期比較增減(%)

		cursor.execute("create table IF NOT EXISTS MonthlyRevenue( \
                        MReId INT AUTO_INCREMENT PRIMARY KEY, \
			CoId INT NOT NULL, \
			MonthlyRevenue BIGINT, \
			LastMonthlyRevenue BIGINT, \
			LastYearMonthlyRevenue BIGINT, \
			MonthlyIncreaseRevenue DOUBLE, \
			LastYearMonthlyIncreaseRevenue DOUBLE, \
			CumulativeRevenue BIGINT, \
			LastYearCumulativeRevenue BIGINT, \
			CompareCumulativeRevenue DOUBLE, \
			Date varchar(20), \
			FOREIGN KEY (CoId) REFERENCES Company(CoId) \
			) DEFAULT CHARSET=utf8 ENGINE=INNODB \
			")

		print("Create Month MarginTrading Table")
                #融資買入, 融資賣出, 融資餘額, 融卷買入, 融卷賣出, 融卷餘額,
		cursor.execute("create table IF NOT EXISTS MarginTrading( \
                        MrevId INT AUTO_INCREMENT PRIMARY KEY, \
			CoId INT NOT NULL, \
			MarginBuy BIGINT, \
			MarginSell BIGINT, \
			MarginRemine BIGINT, \
			ShortSellBuy BIGINT, \
			ShortSellSell BIGINT, \
			ShortSellRemine BIGINT, \
			TotalVolume BIGINT, \
			ChargeOff BIGINT, \
			Category INT, \
			Date varchar(20), \
			FOREIGN KEY (CoId) REFERENCES Company(CoId) \
			) DEFAULT CHARSET=utf8 ENGINE=INNODB \
			")


	except MS.Error as e:
		dbgPrint("Error: unable to create tables [" + str(e) + "]")
		return(-1)
	except MS.Warning as wrn:
		dbgPrint("Warning: create tables [" + str(wrn) + "]")
		return(-1)

if  __name__ == '__main__':
        InitDB("localhost" , "root", "1234")
