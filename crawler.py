import gevent
from spider import Spider
from urlparse import urlsplit
from gevent.pool import Pool
from gevent.queue import Queue, Empty
from gevent.coros import RLock
from abc import ABCMeta, abstractmethod, abstractproperty


class Crawler(object):
	def __init__(self, processor):
		self.processor = processor
		self.pool = Pool(self.processor.concurrency)
		self.base_host = urlsplit(self.processor.start_url).hostname
		self.urls = Queue()
		self.urls.put(self.processor.start_url)
		self.visited_urls = set()
		self.visited_urls_lock = RLock()
		self.pages_count = 0
		
	def start(self):
		while True:
			if self.pages_count >= self.processor.max_pages:
				self.urls = Queue()
				break
			try:
				url = self.urls.get_nowait()
				self.pool.wait_available()
				spider = Spider(self, self.processor, url)
				self.pool.start(spider)
				self.pages_count += 1
			except Empty:
				break
		self.pool.join()
		if not self.urls.empty():
			self.start()
			

class Processor(object):
	__metaclass__ = ABCMeta
	
	@abstractproperty
	def start_url(self):
		return ""
		
	@property
	def allowed_urls(self):
		return [urlsplit(self.start_url).hostname]
	
	@abstractproperty
	def selectors(self):
		return {}
		
	@abstractmethod
	def process(self):
		pass
		
	@property
	def max_pages(self):
		return 10
		
	@property
	def concurrency(self):
		return 1000


