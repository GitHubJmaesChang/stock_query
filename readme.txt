python stock project 
1. query_financialStatement.py : to query financail statement for Quartely, and geneate a Q information, 
                                 the columns of table are : 
								 [公司代號, 公司名稱,資產總額/總計, 權益總額 / 總計, 營業收入, 營業利益,營業外收入及支出,
								  稅前淨利, 基本每股盈餘, 每股參考淨值, ROE, ROA]

2. merge_quartely_table.py : to merge the Quartely 1 ~4 into year report, the table sheet as the  query_financialStatement.py 

3. query_institutional_investors_info :三大法人買賣超表, table[ ID, Name, Foreign_investor_buy, Foreign_Investor_sell,
                                                                Investment_Trust_buy, Investment_Trust_sell,
																Dealer_buy, Dealer_sell, total]

4. query_margin_and_short_trade.py : 融資卷表 , table [ID, Name, 
                                                       margin_buy, margin_sell, margin_remain,
													   short_sale_buy, short_sale_sell, short_sale_remain,]
5. query_stock_dailydata.py : 日成交表, table[ID, Name, volume , StrP, EndP]