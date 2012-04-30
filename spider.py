from gevent import Greenlet
from abc import ABCMeta
from urllib2 import urlopen
from time import time
from lxml import html
import re
from urlparse import urlparse, urldefrag


class Spider(Greenlet):
	__metaclass__ = ABCMeta
	
	def __init__(self, crawler, processor, url):
		self.crawler = crawler
		self.processor = processor
		self.url = urldefrag(url)[0]
		self.document = None
		Greenlet.__init__(self)
		
	def _run(self):
		print "starting %s" % self.url
		start_time = time()
		self.process_page(self.url)
		print "fetching %s: %s milliseconds" % (self.url, (time()-start_time)*1000)
		self.grab_links()
		
	def grab_links(self):
		if self.document is not None:
			for item in self.document.xpath('//a/@href'):
				item = urldefrag(item)[0]
				url = urlparse(item)
				if url.geturl() and item not in self.crawler.visited_urls and self.crawler.base_host == url.hostname:
						self.crawler.urls.put(item)
		
	def process_page(self, url):
		results = []
		url = urlparse(url).geturl()
		self.crawler.visited_urls_lock.acquire()
		self.crawler.visited_urls.add(url)
		self.crawler.visited_urls_lock.release()
		resp = urlopen(url)
		if resp.headers.gettype() != "text/html":
			return
		html_content = resp.read()
		self.document = html.document_fromstring(html_content)
		self.document.make_links_absolute(url)
		for attr, selector in self.processor.selectors.items():
			# try css selector first, then xpath
			try:
				setattr(self.processor, attr, self.document.cssselect(selector))
			except AssertionError:
				setattr(self.processor, attr, self.document.xpath(selector))
		self.processor.url = url
		self.processor.process()


