#!/bin/bash
# crawler_cron_job.sh

DATE=`date +%Y-%m-%d`
logfilename="/home/thomaschen/tmp/stock_query/log/$DATE.FoundationExchange.log"
echo "Start processing FoundationExchange"  |& tee -a $logfilename
date '+%Y-%m-%d %H:%M:%S' |& tee -a $logfilename
python /home/thomaschen/tmp/stock_query/auto_query.py /home/thomaschen/tmp/stock_query/CrawlerData/FoundationExchange/ |& tee -a $logfilename
echo "Processing..." |& tee -a $logfilename
wait
date '+%Y-%m-%d %H:%M:%S'  |& tee -a $logfilename

DATE=`date +%Y-%m-%d`
logfilename="/home/thomaschen/tmp/stock_query/log/$DATE.StockExchange.log"
echo "Start processing StockExchange"  |& tee -a $logfilename
date '+%Y-%m-%d %H:%M:%S' |& tee -a $logfilename
python /home/thomaschen/tmp/stock_query/auto_query.py /home/thomaschen/tmp/stock_query/CrawlerData/StockExchange/ |& tee -a $logfilename
echo "Processing..." |& tee -a $logfilename
wait
date '+%Y-%m-%d %H:%M:%S' |& tee -a $logfilename

DATE=`date +%Y-%m-%d`
logfilename="/home/thomaschen/tmp/stock_query/log/$DATE.MarginTrade.log"
echo "Start processing MarginTrade" |& tee -a $logfilename
date '+%Y-%m-%d %H:%M:%S' |& tee -a $logfilename
python /home/thomaschen/tmp/stock_query/auto_query.py /home/thomaschen/tmp/stock_query/CrawlerData/MarginTrade/ |& tee $logfilename
echo "Processing..." |& tee -a $logfilename
wait
date '+%Y-%m-%d %H:%M:%S' |& tee -a $logfilename
echo "Completed crawling" |& tee -a $logfilename
