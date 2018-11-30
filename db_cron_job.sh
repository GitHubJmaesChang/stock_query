#!/bin/bash
# db_cron_job.sh

DATE=`date +%Y-%m-%d`
logfilename="/home/thomaschen/tmp/stock_query/log/$DATE.db_cron_job.log"
echo "Start processing FoundationExchange"  |& tee -a $logfilename
date '+%Y-%m-%d %H:%M:%S' |& tee -a $logfilename
python /home/thomaschen/tmp/stock_query/new_file_notify.py /home/thomaschen/tmp/stock_query/CrawlerData/ |& tee -a $logfilename
echo "Processing..." |& tee -a $logfilename
wait
date '+%Y-%m-%d %H:%M:%S'  |& tee -a $logfilename
echo "Completed db cron job" |& tee -a $logfilename
