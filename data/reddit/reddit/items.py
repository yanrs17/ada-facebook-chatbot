# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RedditItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    subreddit = Field()
	link = Field()
	title = Field()
	date = Field()
	vote = Field()
	top_comment = Field()
