#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import urllib
import urllib2
import optparse

from time import time
from sys import argv

class proxy:
	
	ip = ''
	port = ''
	type = ''
	country = ''
	url = ''
	response_time = 1001
	
	def __init__(self, ip, port, type, country):
		
		self.ip = ip
		self.port = port
		self.type = type
		self.country = country.lower()
		self.url = "http://%s:%s" % (self.ip, self.port)
		
	def __str__(self):
		
		return "http://%s:%s (%s) @ '%s'" % (self.ip, self.port, self.type, self.country)

class proxyCrawler:
	"""
	Class to find proxies
	"""
	
	proxies = []
	
	time_out = 1 # seconds
	
	def __init__(self):
		"""
		Constructor
		"""
		
		self.__get_all_proxies()
		
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
		
		# u'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?["]([+rjhsynw]+)\).*?<td>(.*?)</td><td>.*?</td><td>(.*?)</td>'
		
		pattern = u'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?["]([+' # ip
		
		substitutions = self.__get_substitutions(page)
		
		# port
		for i in substitutions.keys():
			pattern += i
		pattern += u']+)\)'
		pattern += u'.*?<td>(.*?)</td>' # type
		
		# country
		pattern += u'<td>.*?</td><td>(.*?)</td>'
		
		raw_proxies = re.findall(pattern, page)
		
		parsed_proxies = []
		
		for ip, port, type, country in raw_proxies:
			port = port.replace('+', '')
			for let in substitutions: # create the port
				port = port.replace(let, substitutions[let])
				
			parsed_proxies.append(proxy(ip, port, type, country))
		
		return parsed_proxies
	
	def get_fast(self, port = '', type = '', country = ''):
		"""
		Method to get the (maybe) fastest proxies with the given criteria
	
		Params:
	
			port(str): Proxy port
			type(str): Type of proxy
			country(str): Country
	
		Return:
	
			(list(proxy)): The fastest proxies detected
		"""
		
		faster = []
		
		filtered = self.get_proxies(port=port, type=type, country=country)
		for p in filtered:
			p.response_time = self.test_time(p)
			if p.response_time < self.time_out:
				faster.append(p)
				print "Fast proxy found: ", p , "( %.3f s. )" % (p.response_time)
				
		return faster
	
	def get_proxies(self, port = '', type = '', country = '', time_out = 0):
		"""
		Method to obtain a list of proxies with the given criteria
	
		Params:
	
			proxies(list): List of proxies
			port(str): port number to filter
			type(str): Type of proxy (anonymous CoDeen high-anonymous 
			transparent)
			country(str): Country where the proxy is located
			time_out(float): Maximum response time of proxies (in seconds)
	
		Return:
	
			(list): List of proxies filtered by the given criteria
		"""
		
		filtered = self.proxies[:]
		aux = filtered[:]
		
		if port:
			for p in aux:
				if p.port != port:
					filtered.remove(p)
			
		aux = filtered[:]
			
		if type:
			for p in aux:
				if type not in p.type:
					filtered.remove(p)
		
		aux = filtered[:]
			
		if country:
			country = country.lower()
			for p in aux:
				if country not in p.country:
					filtered.remove(p)
		
		aux = filtered[:]
		
		if time_out:
			for p in aux:
				if self.test_time(p) > time_out:
					filtered.remove(p)
			
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
				
	def test_time(self, p):
		"""
		Method to get the response time of a server
	
		Params:
	
			p(proxy): Proxy
	
		Return:
	
			(float): response time (seconds)
		"""
		
		# set proxy
		proxy_support = urllib2.ProxyHandler({'http': p.url})
		opener = urllib2.build_opener(proxy_support)
		urllib2.install_opener(opener)
		
		try:
		
			init_t = time()
		
			urllib2.urlopen("http://www.google.com", timeout=self.time_out)
		
			end_t = time()
			
			p.response_time = end_t - init_t
		
		# TODO: Terminate program
		except KeyboardInterrupt:
			
			print "Script terminated by user"
			raise SystemExit
		
		except urllib2.URLError, ex:
			
			if str(ex) == "<urlopen error timed out>":
				p.response_time = 999.9
			else:
				p.response_time = 1000.0
				#print "Unexpected urllib2.URLError:", ex
			
		finally:
			
			# disable proxy
			proxy_support = urllib2.ProxyHandler({})
			opener = urllib2.build_opener(proxy_support)
			urllib2.install_opener(opener)
			return p.response_time

if __name__ == "__main__":
	
	parser = optparse.OptionParser()
	parser.add_option('-c', '--country', help='proxies\' country')
	parser.add_option('-p', '--port', help='proxies\' port')
	parser.add_option('-t', '--type', help="proxies\' type ['anonymous', 'CoDeen', 'transparent']")
	parser.add_option('--time_out', '--to', type="int", help='Maximun proxies response time')
	parser.add_option("--fast", action="store_true", default=False, help='Check the fastest proxies')
	
	(options, args) = parser.parse_args(argv)
	
	country = options.country
	port = options.port
	type = options.type
	fast = options.fast
	time_out = options.time_out
	
	print "Fetching proxies... "
	pc = proxyCrawler()
	print "DONE"
	
	print len(pc.proxies), "proxies fetched"
	
	if fast:
		
		if(time_out):
			pc.time_out = time_out
			
		print "Getting fast proxies... (Response time < %d s.) " % pc.time_out
		print "This may take a while..."
		pc.get_fast(port=port, type=type, country=country)
	
	else:
		for p in pc.get_proxies(port=port, type=type, country=country):
			print p
	
	print "DONE"
	
	
