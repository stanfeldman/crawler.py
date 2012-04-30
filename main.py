from gevent import monkey
monkey.patch_all()
from crawler import Crawler, Processor
from time import time


class StackoverflowProcessor(Processor):	
	@property
	def start_url(self):
		return "http://stackoverflow.com/"
		
	@property
	def selectors(self):
		return { "links": "a.question-hyperlink", "tags": "a.post-tag" }
		
	def process(self):
		print "processing %s" % self.url
		if self.links and self.tags:
			print self.links[0].text_content()
			print self.tags[0].text_content()
			print "processed %s" % self.url
			

class MagentoProcessor(Processor):		
	@property
	def start_url(self):
		return "http://www.jonessoda.com/"
		
	@property
	def max_pages(self):
		return 10
		
	@property
	def concurrency(self):
		return 1000
		
	@property
	def selectors(self):
		return { "name": "#product_title", "price": "span.price", "category": "#breadcrumb a" }
		
	def process(self):
		print "processing %s" % self.url
		if self.name and self.price:
			print self.name[0].text_content()
			print self.price[0].text_content()
			category = ""
			for cp in self.category:
				category += cp.text_content() + "/"
			print category
			print "processed %s" % self.name[0].text_content()
			

start_time = time()
processor = StackoverflowProcessor()
crawler = Crawler(processor)
crawler.start()
print "prog time: %s milliseconds" % ((time()-start_time)*1000)
print "pages processed: %s" % crawler.pages_count
