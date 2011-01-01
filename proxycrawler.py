#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import urllib
import urllib2
from time import time

class proxyCrawler:
	"""
	Class to find proxies
	"""
	
	__proxies = []
	
	def __init__(self):
		"""
		Constructor
		"""
		
		self.timeout = 1 # secs
		
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
	
			page(str): Page to parse to get the proxies
	
		Return:
	
			(tuple): (ip (str), port (str)) Proxy info
		"""
		
		# u'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?["]([+rjhsynw]+)\)'
		
		pattern = u'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?["]([+'
		
		substitutions = self.__get_substitutions(page)
		
		for i in substitutions.keys():
			pattern += i
		pattern += u']+)\)'
		
		raw_proxies = re.findall(pattern, page)
		
		parsed_proxies = []
		#TODO: parse ports
		for ip, port in raw_proxies:
			port = port.replace('+', '')
			for let in substitutions:
				port = port.replace(let, substitutions[let])
		
			parsed_proxies.append((ip, port))
		
		return parsed_proxies
	
	def get_all_proxies(self):
		"""
		Method to get all proxies
	
		Return:
	
			(list): List of all proxies in tuples 
			(ip (str), port (str), type (str))
		"""
		
		num_pages = self.__get_num_pages()
		
		proxies = []
		
		for i in xrange(1, num_pages+1):
			url = 'http://www.samair.ru/proxy/proxy-' + str(i).zfill(2) + '.htm'
			page = urllib.urlopen(url).read()
			proxies += self.__parse_proxies(page)
			
		return proxies
				
	def test_time(self, ip, port):
		"""
		Method to get the response time of a server
	
		Params:
	
			ip(str): Proxy IP
			port(str): Proxy port
	
		Return:
	
			(float): response time
		"""
		
		init_t = time()
		
		proxie_url =  'http://' + ip + ':' + port
		
		# set proxy
		proxy_support = urllib2.ProxyHandler({'http': proxie_url})
		opener = urllib2.build_opener(proxy_support)
		urllib2.install_opener(opener)
		
		try:
		
			urllib2.urlopen("http://www.google.com", timeout=self.timeout)
		
			end_t = time()
			
			response_time = end_t - init_t
			
		except Exception, ex:
			
			response_time = 999
			
		finally:
			
			# disable proxy
			proxy_support = urllib2.ProxyHandler({})
			opener = urllib2.build_opener(proxy_support)
			urllib2.install_opener(opener)
			
			return response_time

if __name__ == "__main__":
	pc = proxyCrawler()
	p = pc.get_all_proxies()
	#print p[:10]
	
	print len(p), "proxies"
	
	for ip, port in p:
		
		print "%s:%s %.3f" % (ip, port, pc.test_time(ip, port))
		
