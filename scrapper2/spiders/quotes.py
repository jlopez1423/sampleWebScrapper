#quotes_spider.py
#originally it did not save any data, rather it just saved the whole webpage
#using the keyword 'yield' in our callback method will assist in that
#modifying this code even further to look for next pages
import scrapy

class QuotesSpider(scrapy.Spider):
	name = "quotes"


	''' This can be written in short hand as
	def start_requests(self):
		urls = [
			'http://quotes.toscrape.com/page/1/',
			'http://quotes.toscrape.com/page/2/',
		]

		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	This:'''

	start_urls = [
		'http://quotes.toscrape.com/page/1/',
		# 'http://quotes.toscrape.com/page/2/',
	]

	#parse is scrapy's default callback
	# def parse(self, response):
	# 	page = response.url.split("/")[-2]
	# 	filename = 'quotes-%s.html' % page
	# 	with open(filename, 'wb') as f:
	# 		f.write(response.body)
	# 	self.log('Saved file %s' % filename)

	def parse( self, response ):
		for quote in response.css('div.quote'):
			yield {
				'text': quote.css('span.text::text').extract_first(),
				'author': quote.css('span small::text').extract_first(),
				'tags': quote.css('div.tags a.tag::text').extract(),
			}
		next_page = response.css('li.next a::attr(href)').extract_first()
		if next_page is not None:
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback=self.parse)
		 