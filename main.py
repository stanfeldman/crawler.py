from gevent import monkey
monkey.patch_all()
from spider import Spider
from crawler import Crawler
from mechanize import Browser, ParseResponse


class MySpider(Spider):
	def process(self, results):
		print "MySpider processing.............."
		print results[0].get("value")
		print results[1].get("title")
		print "MySpider processed.............."

address = "http://192.168.1.47/joomla/"
selectors = ["div.vmCartDetails div.vmCartChild input[name='product_id']", "input.addtocart_button"]
depth = 5
crawler = Crawler([MySpider(address, selectors, depth)])
crawler.start()
