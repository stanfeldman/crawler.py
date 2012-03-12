import gevent


class Crawler(object):
	def __init__(self, spiders):
		self.spiders = spiders
		
	def start(self):
		for spider in self.spiders:
			spider.start()
		gevent.joinall(self.spiders)
