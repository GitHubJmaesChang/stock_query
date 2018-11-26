#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import requests
import datetime
import time
from fake_useragent import UserAgent
import random
from bs4 import BeautifulSoup

ua = UserAgent() # generate a random user agent
proxyList = [] 	 # current proxy list: [ip, port]
proxy = []	 # the proxy for html request
refreshProxyList = 0 # counts to rebuild the proxy list
refreshReqProxy = 0  # counts to rebuild current proxy

def buildProxyList():
    global proxyList

    # Retrieve latest proxies
    proxies_req = requests.get('https://www.sslproxies.org/')
    proxies_req.headers["User-Agent"] = ua.random

    soup = BeautifulSoup(proxies_req.content, "html.parser")
    proxies_table = soup.find(id='proxylisttable')


    # Save proxies in the array
    for row in proxies_table.tbody.find_all('tr'):
        proxyList.append({
          'ip':   row.find_all('td')[0].string,
          'port': row.find_all('td')[1].string
    })


def doPost(url, header, tout, payload, proxy):
    print("html POST")
    return requests.post(url, proxies=proxy, headers=header, timeout=tout, data=payload)
    
def doGet(url, header, tout, payload, proxy):
    print("html GET")
    return requests.get(url, proxies=proxy, headers=header, timeout=tout)

restful_dict = {
                    'post': doPost,
                    'get': doGet
               }



def htmlRequest(url, restful, payload):
    global refreshProxyList
    global refreshReqProxy
    global proxy
    global proxyList
    global restful_dict

    htmltimeout = 5
    retrytimeout = 10

    print("***htmRequest***")

    if(refreshProxyList % 200 == 0):
        refreshProxyList = 0
	refreshReqProxy = 0
    	buildProxyList()
	print("htmlRequest: refresh proxy list")

    refreshProxyList = refreshProxyList + 1

    keeptrying = True
    while(keeptrying == True):
        # Generate a new proxy for every 10 requests
        if(refreshReqProxy % 10 == 0):
            proxy_index = random_proxy()
            proxy = proxyList[proxy_index]
	    print("htmlRequest: generate new proxy")

        refreshReqProxy = refreshReqProxy + 1

	# Setup request proxy
        proxies = {
            "https": "https://{}:{}/".format(proxy['ip'], proxy['port']),
            "http": "http://{}:{}/".format(proxy['ip'], proxy['port'])
        }

        # Setup request header
        headers = {'User-Agent': ua.random}

        # Setup request timeout
        htmltimeout = (htmltimeout + 3)%30

        try:
    	    #req = requests.get(url, proxies=proxies, headers=headers, timeout=htmltimeout)
	    # Parameters: url, header, tout, payload, proxy
	    req = restful_dict[restful](url, headers, htmltimeout, payload, proxies)
        except Exception as e:
    	    del proxyList[proxy_index]
            print('htmlRequest: Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' deleted.')
	    print(e)
	    if(len(proxyList) < 3):
	    	print("htmlRequest: All removed, rebuild Proxy List")
	        buildProxyList()
            proxy_index = random_proxy()
            proxy = proxyList[proxy_index]
	    time.sleep(retrytimeout)
	    retrytimeout = retrytimeout + 3
	    if(retrytimeout > 40):
	    	keeptrying = False
		raise Exception
	else:
	    keeptrying = False

    return(req)

 
	

# Retrieve a random index proxy (we need the index to delete it if not working)
def random_proxy():
    return random.randint(0, len(proxyList) - 1)


if __name__ == '__main__':
    htmlRequest("http://icanhazip.com", "get", "")

