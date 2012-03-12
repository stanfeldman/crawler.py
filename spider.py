from gevent import Greenlet
from abc import ABCMeta
from urllib2 import urlopen
from time import time
from lxml import html
import re
import utils


class Spider(Greenlet):
	__metaclass__ = ABCMeta
	
	def __init__(self, start_url, selectors, depth=3):
		self.urls = set()
		self.visited_urls = set()
		self.new_urls = set()
		self.new_urls.add(start_url)
		self.selectors = selectors
		self.depth = depth
		self.document = None
		Greenlet.__init__(self)
		
	def _run(self):
		for i in range(self.depth):
			print "depth: %s................" % i
			self.urls.update(self.new_urls)
			print self.urls
			for url in self.urls:
				print "depth: %s, url: %s" % (i, url)
				results = self.fetch(url)
				if results:
					self.process(results)
				self.grab_links()
		
	def grab_links(self):
		if self.document is not None:
			link_pattern = r"(http|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?"
			self.new_urls.update({item for item in self.document.xpath('//a/@href') if re.search(link_pattern, item) and item not in self.visited_urls})
		
	def fetch(self, url):
		results = []
		try:
			url = utils.iri2uri(url)
			self.document = html.document_fromstring(urlopen(url).read())
			self.document.make_links_absolute(url)
			for selector in self.selectors:
				# try css selector first, then xpath
				try:
					results.extend(self.document.cssselect(selector))
				except AssertionError:
					results.extend(self.document.xpath(selector))
		except Exception:
			print "bad url: " + url
		self.visited_urls.update(url)
		return results

