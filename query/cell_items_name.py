#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

fundation_table_request= {"2013" : [u"證券代號", u"證券名稱", u"外資賣出股數", u"投信買進股數", u"投信賣出股數", u"自營商買進股數", u"自營商賣出股數", u"三大法人買賣超股數" ] }


def information():
   print (fundation_table_request["2013"])

if  __name__ == '__main__':
   information()
