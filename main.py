# -*- coding: utf-8 -*-
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

			
class TanukiProcessor(Processor):	
	@property
	def start_url(self):
		return "http://new.tanuki.ru/menu/sushi/"
		
	@property
	def max_pages(self):
		return 1
		
	@property
	def selectors(self):
		return { "category": "#nav-secondary .active a", "products": ".good_list h4 a", "prices": ".good_list .cost-units .cost" }
		
	def process(self):
		print "processing %s" % self.url
		if self.category and self.products and self.prices:
			print "category:: %s" % self.category[0].text_content().strip()
			for i in xrange(len(self.products)):
				product = self.products[i].text_content().strip()
				price = self.prices[i].text_content().strip()
				price = price[:price.find(".")-3].strip()
				print "product:: %s: %s" % (product, price)
			print "processed %s" % self.url
			

if __name__ == "__main__":
	start_time = time()
	processor = TanukiProcessor()
	crawler = Crawler(processor)
	crawler.start()
	print "prog time: %s milliseconds" % ((time()-start_time)*1000)
	print "pages processed: %s" % crawler.pages_count
