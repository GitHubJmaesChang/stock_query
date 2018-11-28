import os
import shutil
import pyinotify
from AddStock_db import inserFoundationExchangeDB
from AddStock_db import insertInsertStockExchangeDB
from AddStock_db import insertInsertMarginTradeDB

class FileEventHandler(pyinotify.ProcessEvent):
    insert_db_dict = {
                         'FoundationExchange': inserFoundationExchangeDB,
                         'StockExchange': insertInsertStockExchangeDB, 
		         'MarginTrade': insertInsertMarginTradeDB
                     }

    def process_IN_CLOSE_NOWRITE(self, event):
        print "CLOSE_NOWRITE event:", event.pathname

    def process_IN_CLOSE_WRITE(self, event):
        print "CLOSE_WRITE event:", event.pathname
        
	try:
	    FileEventHandler.process_event(self, event.pathname)
        except Exception as e:
	    print(e)

    def process_IN_CREATE(self, event):
        print "CREATE event:", event.pathname

    def process_event(self, evtPath):
        fn = evtPath.split("/")[-2]
        print(fn)
        if fn in FileEventHandler.insert_db_dict:
            try:
                #FileEventHandler.insert_db_dict[fn](event.pathname)

                # if inserted, move process file to another folder
                dstpath = evtPath.replace("CrawlerData", "CrawlerData_Inserted")
                shutil.move(evtPath, dstpath)
		print("File moved from: [" + evtPath + "] to (" + dstpath + ")")
            except Exception as e:
                print(e)
		raise Exception
        else:
            print("Error: function key not found")

def absoluteFilePaths(directory):
   for dirpath,_,filenames in os.walk(directory):
       for f in filenames:
           yield os.path.abspath(os.path.join(dirpath, f))

def main():
    # Process existing files first
    for f in absoluteFilePaths("./CrawlerData"):
    	print("Process: [" + f + "]")
	FileEventHandler.process_event(FileEventHandler(), f)

    # Setup watch manager
    watchmanager = pyinotify.WatchManager()
    watch_dir = os.path.abspath("/home/thomaschen/tmp/stock_query/CrawlerData")

    # rec: Adds watches recursively on all subdirectories
    # auto_add: Automatically adds watches on newly created directories
    watchmanager.add_watch(watch_dir, pyinotify.ALL_EVENTS, rec=True, auto_add=True)

    # Setup notifier (blocking call)
    notifier = pyinotify.Notifier(watchmanager, FileEventHandler())
    notifier.loop()

if __name__ == '__main__':
    main()
