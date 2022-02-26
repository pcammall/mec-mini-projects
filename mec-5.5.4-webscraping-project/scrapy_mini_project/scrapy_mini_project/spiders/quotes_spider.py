import scrapy

class QuotesSpider(scrapy.Spider):
	name = "quotes"
	
	# def start_requests(self):
		# urls = [ 'http://quotes.toscrape.com/page/1/', 'http://quotes.toscrape.com/page/2/', ]
		
		# for url in urls:
			# yield scrapy.Request(url=url, callback=self.parse)
			
	def start_requests(self):
		url = 'http://quotes.toscrape.com/'
		tag = getattr(self, 'tag', None)
		if tag is not None:
			url = url + 'tag/' + tag
		yield scrapy.Request(url, self.parse)
	
	def parse(self, response):
	
		#original spider. This just fetches a web page
		#page = response.url.split("/")[-2]
		#filename = 'quotes-%s.html' % page
		#with open(filename, 'wb') as f:
		#	f.write(response.body)
		#self.log('Saved file %s' % filename)
		
		#second spider. This will capture the quote text, its author, and any tags the quote has
		# for quote in response.css('div.quote'):
			# yield {
				# 'text': quote.css('span.text::text').get(),
				# 'author': quote.css('small.author::text').get(),
				# 'tags': quote.css('div.tags a.tag::text').getall(),
				# }
				
		#third spider, with page following (by searching for the link to the next page)
		# for quote in response.css('div.quote'):
			# yield {
				# 'text': quote.css('span.text::text').get(),
				# 'author': quote.css('small.author::text').get(),
				# 'tags': quote.css('div.tags a.tag::text').getall(),
				# }
				
			# next_page = response.css('li.next a::attr(href)').get()
			# if next_page is not None:
				# next_page = response.urljoin(next_page)
				# yield scrapy.Request(next_page, callback=self.parse)

		#fourth spider, which uses the shortcut for moving to the next page (note the last three lines of the function)
		# for quote in response.css('div.quote'):
			# yield {
				# 'text': quote.css('span.text::text').get(),
				# 'author': quote.css('small.author::text').get(),
				# 'tags': quote.css('div.tags a.tag::text').getall(),
			# }
			
			# next_page = response.css('li.next a::attr(href)').get()
			# if next_page is not None:
				# yield response.follow(next_page, callback=self.parse)
				
		#fifth. Uses a parameter passed to scrapy crawl quote <params> to find quotes with specific tags
		for quote in response.css('div.quote'):
			yield {
				'text': quote.css('span.text::text').get(),
				'author': quote.css('small.author::text').get(),
				}
				
			next_page = response.css('li.next a::attr(href)').get()
			if next_page is not None:
				yield response.follow(next_page, self.parse)
			
				
class AuthorSpider(scrapy.Spider):
	name = 'author'
	start_urls = ['http://quotes.toscrape.com/']
	
	def parse(self, response):
		author_page_links = response.css('.author + a')
		yield from response.follow_all(author_page_links, self.parse_author)
		
		pagination_links = response.css('li.next a')
		yield from response.follow_all(pagination_links, self.parse)
		
	def parse_author(self, response):
		def extract_with_css(query):
			return response.css(query).get(default='').strip()
			
		yield {
			'name': extract_with_css('h3.author-title::text'),
			'birthdate': extract_with_css('.author-born-date::text'),
			'bio': extract_with_css('.author-description::text'),
		}
		
