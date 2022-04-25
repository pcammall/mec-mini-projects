import scrapy

class ScrapeXPathSpider(scrapy.Spider):

	name = 'toscrape-xpath'
	def start_requests(self):
		url = 'http://quotes.toscrape.com/'
		yield scrapy.Request(url, self.parse)
	
	def parse(self, response):
		
		#and this method is printing a blank file for some reason. But code works in scrapy shell?
		# text = response.xpath("//div[@class='quote']/span[@class='text']/text()")
		# author = response.xpath("//div[@class='quote']/span/small[@class='author']/text()")
		# d = dict(zip(text, author))
		# for x in d:
			# yield { 'text': x,
					# 'author': d[x],
			# }
		
		#and this one should be correct but isn't outputing the correct thing. Keeps repeating that first line (.get), or puts each page on one line (getall)
		#using ./span produces empty arrays
		for quote in response.xpath(".//div[@class='quote']"):
			yield {
				'text': quote.xpath(".//span[@class='text']/text()").extract(),
				'author': quote.xpath(".//small[@class='author']/text()").extract(),
				
			}
		
		#this only seems to pick up the first one from the page (using .get) or puts the entire page on one line in the json file (using .getall)
		# yield {
				# 'text': response.xpath("//span[@class='text']/text()").get(),
				# 'author': response.xpath("//small[@class='author']/text()").get(),
				
			# }
		
		
		
		#print("find next page link")
		next_page = response.xpath(".//li[@class='next']/a/@href").get()
		if next_page is not None:
		#	print('follow')
			yield response.follow(next_page, self.parse) 
	