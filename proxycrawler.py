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
	
	proxies = []
	
	def __init__(self):
		"""
		Constructor
		"""
		
		self.timeout = 1 # secs
		
		self.__get_all_proxies()
		
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
		
			parsed_proxies.append((ip, port, type))
		
		return parsed_proxies
	
	def get_faster(self, port = '', type = 'anonymous'):
		"""
		Method to get the faster proxie with the given criteria
	
		Params:
	
			port(str): Proxy port
			type(str): Type of proxy
	
		Return:
	
			(tuple): (ip(str), port(str), type(str))
		"""
		
		faster = None
		faster_t = 1000
		
		filtered = self.get_proxies(port=port, type=type)
		
		for p in filtered:
			proxy_t = self.test_time(p[0], p[1])
			if proxy_t < faster_t:
				faster_t = proxy_t
				faster = p
				print "A faster proxie found: ", p , "( %.3f seconds )" % (faster_t)
				
		return faster
	
	# TODO: Filter by country
	def get_proxies(self, port = '', type = 'anonymous'):
		"""
		Method to obtain a list of proxies with the given criteria
	
		Params:
	
			proxies(list): List of proxies
			port(str): port number to filter
			type(str): Type of proxie (anonymous CoDeen high-anonymous 
			transparent)
	
		Return:
	
			(list): List of proxies filtered by the given criteria
		"""
		
		filtered = self.proxies[:]
		aux = filtered[:]
		
		if port:
			for i in aux:
				if i[1] != port:
					filtered.remove(i)
			
		aux = filtered[:]	
			
		if type:
			for i in aux:
				if type not in i[2]:
					filtered.remove(i)
			
		#if country:
			
			#pass
			
		return filtered
			
	def __get_all_proxies(self):
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
			
		self.proxies = proxies
				
	def test_time(self, ip, port):
		"""
		Method to get the response time of a server
	
		Params:
	
			ip(str): Proxy IP
			port(str): Proxy port
	
		Return:
	
			(float): response time
		"""
		
		proxie_url =  'http://' + ip + ':' + port
		
		# set proxy
		proxy_support = urllib2.ProxyHandler({'http': proxie_url})
		opener = urllib2.build_opener(proxy_support)
		urllib2.install_opener(opener)
		
		try:
		
			init_t = time()
		
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
	
	print "Fetching proxies... "
	pc = proxyCrawler()
	print "DONE"
	
	print len(pc.proxies), "proxies fetched"
	
	print "Getting faster proxie... "
	p = pc.get_faster(port = '80')
	print "DONE"
	
	
