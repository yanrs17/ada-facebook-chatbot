# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from __future__ import absolute_import
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
	start_urls = ['https://www.reddit.com/r/UofT']

	# tell the Spider what to do on each of the start_urls
	# def parse(self, response):
	#     links = response.xpath('//p[@class="title"]/a[@class="title may-blank "]/@href').extract()
	#     titles = response.xpath('//p[@class="title"]/a[@class="title may-blank "]/text()').extract()
	#     dates = response.xpath('//p[@class="tagline"]/time[@class="live-timestamp"]/@title').extract()
	#     votes = response.xpath('//div[@class="midcol unvoted"]/div[@class="score unvoted"]/text()').extract()
	#     comments = response.xpath('//div[@id="siteTable"]//a[@class="comments may-blank"]/@href').extract()

		# for i, link in enumerate(comments):
		#     item = RedditItem()
		#     item['subreddit'] = str(re.findall('/r/[A-Za-z]*8?', link))[3:len(str(re.findall('/r/[A-Za-z]*8?', link)))-2]
		#     item['link'] = links[i]
		#     item['title'] = titles[i]
		#     item['date'] = dates[i]
		#     if votes[i] = u'\u2022':
		#         item['vote'] = 'hidden'
		#     else:
		#         item['vote'] = int(votes[i])
		#     # top_comment field need to be filled on the comment page

		#     request = Request(link, callback=self.parse_comment_page)
		#     request.meta['item'] = item
		#     yield request

	# # top_comment field need to be filled on the comment page
	# # tells the spider what to do with the request
	# def parse_comment_page(self, response):
		# item = response.meta['item']
		# top = response.xpath('//div[@class="commentarea"]//div[@class="md"]').extract()[0]

		# # BeautifulSoup removes HTML tags from the top comment
		# top_soup = BeautifulSoup(top, 'html.parser')
		# item['top_comment'] = top_soup.get_text().replace('\n', ' ')
		# yield item

	def parse(self, response):
		links = response.css('a.title.may-blank::attr(href)').extract()
		titles = response.css('a.title.may-blank::text').extract()
		for i, link in enumerate(links):
			if not re.search('\?', titles[i]):
			 	continue
			yield response.follow(link, callback=self.parse_comment_page)

	def parse_comment_page(self, response):
		content_post = response.css('div.expando div.md')

		# if the length of content post is greater than 60, the question is too specific
		if len(str(content_post.extract()).split()) > 60:
			return
		item = RedditItem()
		item['question'] = str(response.css('p.title a.title.may-blank::text').extract()[0])
		top = response.css('div.commentarea div.md')[0]
		top_content = top.css('p::text').extract()[0]
		item['answer'] = str(top_content)
		item['link'] = str(response.url)
		#print "question: %s" % str(item['question'])
		#print "answer: %s"  % str(top_content)
		#print "link: %s" % response.url







