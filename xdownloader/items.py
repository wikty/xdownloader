# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XDownloaderItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	origin = scrapy.Field()
	download_title = scrapy.Field()
	download_url = scrapy.Field()
	download_url_seq = scrapy.Field()
	page_title = scrapy.Field()
	page_url = scrapy.Field()
	mimetype = scrapy.Field()
	filename = scrapy.Field()
	data = scrapy.Field()
	status = scrapy.Field()
	path = scrapy.Field()