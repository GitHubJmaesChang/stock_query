import os
import sys
import shutil
import pyinotify
from AddStock_db import inserFoundationExchangeDB
from AddStock_db import insertInsertStockExchangeDB
from AddStock_db import insertInsertMarginTradeDB
from auto_query import hasFunction

class FileEventHandler(pyinotify.ProcessEvent):
	insert_db_dict = {
					 'FoundationExchange': inserFoundationExchangeDB,
					 'StockExchange': insertInsertStockExchangeDB, 
					 'MarginTrade': insertInsertMarginTradeDB
					 }

	def process_IN_CLOSE_NOWRITE(self, event):
		print "CLOSE_NOWRITE event:", event.pathname

	# The event used to trigger actual DB insert
	def process_IN_CLOSE_WRITE(self, event):
		print "CLOSE_WRITE event:", event.pathname
		try:
			FileEventHandler.process_event(self, event.pathname)
			print("Processed Event: FileEventHandler.process_event")
		except Exception as e:
			print(e)

	def process_IN_CREATE(self, event):
		print "CREATE event:", event.pathname

	# Function to run corresponding DB insert fucntion and move processed
	# file to another folder.
	def process_event(self, evtPath):
		fn = hasFunction(evtPath)
		if(fn != -1):
			print("Process with function: " + str(fn))
			try:
				#FileEventHandler.insert_db_dict[fn](event.pathname)

				# After insert, move processed file to another folder
				dstpath = evtPath.replace("CrawlerData", "CrawlerData_Inserted")
				#shutil.move(evtPath, dstpath)
				print("File moved from: [" + evtPath + "] to (" + dstpath + ")")
			except Exception as e:
				print(e)
		else:
			print("Error: function key not found")

def absoluteFilePaths(directory):
   for dirpath,_,filenames in os.walk(directory):
	   for f in filenames:
		   yield os.path.abspath(os.path.join(dirpath, f))

# This function sets up python to monitor the directory "./CrawlerData"
# and its subdirectories for any .csv files created.
# It would pick up any existing files to insert to the DB first
def main(path):
	# Process existing files first.
	# The following loop will go through all subdirectories
	for f in absoluteFilePaths(path):
		if(f.endswith('.csv')):
			print("Process: [" + f + "]")
			FileEventHandler.process_event(FileEventHandler(), f)
		else:
			print("NOT handling: [" + f + "]")

	# Setup watch manager
	watchmanager = pyinotify.WatchManager()
	watch_dir = os.path.abspath(path)

	# rec: Adds watches recursively on all subdirectories
	# auto_add: Automatically adds watches on newly created directories
	watchmanager.add_watch(watch_dir, pyinotify.ALL_EVENTS, rec=True, auto_add=True)

	# Setup notifier (blocking call)
	notifier = pyinotify.Notifier(watchmanager, FileEventHandler())
	notifier.loop()

if __name__ == '__main__':
	main(str(sys.argv[1]))

