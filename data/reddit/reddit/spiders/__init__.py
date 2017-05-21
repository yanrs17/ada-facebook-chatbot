# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import re
from bs4 import BeautifulSoup
from scrapy import Spider, Request
from reddit.items import RedditItem

""" 
	allowed_domains: domains the Spider is allowed to crawl
	start_urls: where spider will start crawling
"""
class RedditSpider(Spider):
	name = 'reddit'
	allowed_domains = ['reddit.com']
	start_urls = ['https://www.reddit.com/r/circlejerk', 
	'https://www.reddit.com/r/gaming', 
	'https://www.reddit.com/r/floridaman',  
	'https://www.reddit.com/r/movies', 
	'https://www.reddit.com/r/science', 
	'https://www.reddit.com/r/seahawks', 
	'https://www.reddit.com/r/totallynotrobots', 
	'https://www.reddit.com/r/uwotm8', 
	'https://www.reddit.com/r/videos', 
	'https://www.reddit.com/r/worldnews']

	# tell the Spider what to do on each of the start_urls
 	def parse(self, response):
		links = response.xpath('//p[@class="title"]/a[@class="title may-blank "]/@href').extract()
		titles = response.xpath('//p[@class="title"]/a[@class="title may-blank "]/text()').extract()
		dates = response.xpath('//p[@class="tagline"]/time[@class="live-timestamp"]/@title').extract()
		votes = response.xpath('//div[@class="midcol unvoted"]/div[@class="score unvoted"]/text()').extract()
		comments = response.xpath('//div[@id="siteTable"]//a[@class="comments may-blank"]/@href').extract()

		for i, link in enumerate(comments):
			item = RedditItem()
			item['subreddit'] = str(re.findall('/r/[A-Za-z]*8?', link))[3:len(str(re.findall('/r/[A-Za-z]*8?', link)))-2]
			item['link'] = links[i]
			item['title'] = titles[i]
			item['date'] = dates[i]
			if votes[i] = u'\u2022':
				item['vote'] = 'hidden'
			else:
				item['vote'] = int(votes[i])
			# top_comment field need to be filled on the comment page

			request = Request(link, callback=self.parse_comment_page)
			request.meta['item'] = item
			yield request

	# top_comment field need to be filled on the comment page
	# tells the spider what to do with the request
 	def parse_comment_page(self, response):
		item = response.meta['item']
		top = response.xpath('//div[@class="commentarea"]//div[@class="md"]').extract()[0]

		# BeautifulSoup removes HTML tags from the top comment
		top_soup = BeautifulSoup(top, 'html.parser')
		item['top_comment'] = top_soup.get_text().replace('\n', ' ')
		yield item