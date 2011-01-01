#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import urllib

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
		"""
		Method to obtain the number of pages
		
		Return:
		
			(int): Number of pages of proxies
		"""
		
		page = urllib.urlopen('http://www.samair.ru/proxy/proxy-01.htm').read()
		
		num_pages = int(re.findall(u'total pages: (\d+)', page)[0])
		
		return num_pages
		
	def __get_substitutions(self, page):
		"""
		Method to get the letters that substitute the numbers of the ports
		
		Return:
			(dict): Dictionary which key (str) is the letter and the value 
					(str) is the number
		
		"""

		subs = {}
		
		for let, num in re.findall(u'(.)=(\d)', page):
			
			subs[let] = num
			
		return subs
	
	def __parse_proxies(self, page):
		""" Function doc
	
		Params:
	
			PARAM(): DESCRIPTION
	
		Return:
	
			(): DESCRIPTION
		"""
		
		# u'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?["]([+rjhsynw]+)\).*?<td>(.*?)</td>'
		
		pattern = u'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?["]([+' # ip
		
		substitutions = self.__get_substitutions(page)
		
		# port
		for i in substitutions.keys():
			pattern += i
		pattern += u']+)\)'
		pattern += u'.*?<td>(.*?)</td>' # get proxy type
		
		# TODO: Get country
		
		raw_proxies = re.findall(pattern, page)
		
		parsed_proxies = []
		#TODO: parse ports
		for ip, port, type in raw_proxies:
			port = port.replace('+', '')
			for let in substitutions:
				port = port.replace(let, substitutions[let])
		
			parsed_proxies += (ip, port, type)
		
		return parsed_proxies
	
	# TODO: Filter by country
	def filter_proxies(self, proxies, port = '', type = ''):
		""" Function doc
	
		Params:
	
			proxies(list): List of proxies
			port(str): port number to filter
			type(str): Type of proxie (anonymous CoDeen high-anonymous 
			transparent)
	
		Return:
	
			(list): List of proxies filtered by the given criteria
		"""
		
		filtered = proxies[:]
		
		if port:
			for i in filtered:
				if i[2] != port:
					filtered.remove(i)
			
		if type:
			for i in filtered:
				if type not in i[3]:
					filtered.remove(i)
			
		#if country:
			
			#pass
			
	def get_all_proxies(self):
		"""
		Method to get all proxies
	
		Return:
	
			(list): List of all proxies in tuples 
			(ip (str), port (int), type (str))
		"""
		
		num_pages = self.__get_num_pages()
		
		proxies = []
		
		for i in xrange(1, num_pages+1):
			url = 'http://www.samair.ru/proxy/proxy-' + str(i).zfill(2) + '.htm'
			page = urllib.urlopen(url).read()
			proxies += self.__parse_proxies(page)
			
		return proxies


if __name__ == "__main__":
	p = proxyCrawler().get_all_proxies()
	print p[:10]
	
