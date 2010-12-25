#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import urrlib

class proxyCrawler:
	"""
	Class to find proxies
	"""
	
	__proxies = []
	
	def __init__(self):
		"""
		Constructor
		"""
		
		pass
		
	def find(self, criteria):
		"""
		Methot Function doc
	
		Params:
	
			criteria(dict): Criteria for searching proxies
	
		Return:
	
			(list): Proxies list matching given criteria
		"""
		
		proxies = []
		
	def __get_num_pages(self):
		
		page = urllib.urlopen('http://www.samair.ru/proxy/proxy-01.htm').read()
		
		num_pages = int(re.findall(u'total pages: (\d+)', page)[0])
		
		return num_pages
