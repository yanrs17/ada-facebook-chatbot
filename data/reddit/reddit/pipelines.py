# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

"""
	connect Spider to crawl and parse the HTML with database settings
"""
# check if a link has already been added, and skips processing that item if it has
class DuplicatesPipeline(object):
	def __init__(self):
		self.ids_seen = set()

	def process_item(self, item, spider):
		if item['link'] in self.ids_seen:
			raise DropItem("Duplicate item found: %s" % item)
		else:
			self.ids_seen.add(item['link'])
		return item

# defines the data persistence
class MongoDBPipeline(object):
	# connects to the database
	def __init__(self):
		connection = pymongo.MongoClient(
		settings['MONGODB_SERVER'],
		settings['MONGODB_PORT']
		)
		db = connection[settings['MONGODB_DB']]
		self.collection = db[settings['MONGODB_COLLECTION']]

	# processes the data and adds it to the collection
	def process_item(self, item, spider):
		valid = True
		for data in item:
			if not data:
				valid = False
				raise DropItem("Missing {0}!".format(data))
			if valid:
				self.collection.insert(dict(item))
				log.msg("Added to MongoDB database!",
				level=log.DEBUG, spider=spider)
		return item
