# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os, csv, hashlib, time
from urllib.parse import quote
import scrapy

from xdownloader.utils import str2dict, filter_filename, unique_filename


class BasePipeline(object):

	origin_key = 'origin'
	download_url_key = 'download_url'
	download_url_seq_key = 'download_url_seq'
	download_title_key = 'download_title'
	page_url_key = 'page_url'
	page_title_key = 'page_title'
	mimetype_key = 'mimetype'
	filename_key = 'filename'
	data_key = 'data'
	status_key = 'status'
	path_key = 'path'

	def process_item(self, item, spider):
		return item


class DownloadFilePipeline(BasePipeline):

	def __init__(self, *args, **kwargs):
		super(DownloadFilePipeline, self).__init__(*args, **kwargs)

	def process_item(self, item, spider):
		# encoded_url = quote(item[self.download_url_key])
		request = scrapy.Request(item[self.download_url_key])
		dfd = spider.crawler.engine.download(request, spider)
		# request.meta['dont_redirect'] = False
		dfd.addBoth(self.return_item, item)
		return dfd

	def return_item(self, response, item):
		if response.status != 200:
			item[self.status_key] = response.status
		else:
			item[self.status_key] = 0
			item[self.data_key] = response.body
			s = response.headers.get('Content-Disposition', b'').decode('utf8')
			d = str2dict(s, ';', '=', '"')
			item[self.filename_key] = d.get('filename', None) if d else None
			item[self.mimetype_key] = response.headers.get('Content-Type', b'').decode('utf8').split(';')[0]
		return item

class SaveFilePipeline(BasePipeline):

	naming_methods = {
		1: 'download link title',
		2: 'download page title',
		3: 'download link md5 hash',
		4: 'download filename' # default method
	}

	def __init__(self, storage_dir, report_csv, naming_method, mimetype_extension_file, *args, **kwargs):
		super(SaveFilePipeline, self).__init__(*args, **kwargs)
		if not os.path.exists(storage_dir):
			raise Exception('storage directory not exists: %s' % storage_dir)
		if not os.path.exists(mimetype_extension_file):
			raise Exception('mimetype_extension file not exists: %s' % mimetype_extension_file)

		self.storage_dir = storage_dir
		self.naming_method = naming_method
		self.mimetype_extension_file = mimetype_extension_file
		self.default_extension = '.data'
		self.mimetype2extension = {}
		self.report_csv = report_csv
		self.report = []

	def open_spider(self, spider):
		with open(self.mimetype_extension_file, 'r', encoding='utf8', newline='') as f:
			reader = csv.reader(f)
			for item in reader:
				if item[1] not in self.mimetype2extension:
					self.mimetype2extension[item[1]] = []
				self.mimetype2extension[item[1]].append(item[0])

	def close_spider(self, spider):
		with open(self.report_csv, 'a+', newline='') as f:
			writer = csv.writer(f)
			writer.writerows(self.report)

	def add_report(self, item):
		self.report.append([
			item[self.path_key],
			time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
			item[self.download_title_key],
			item[self.download_url_key],
			item[self.page_title_key],
			item[self.page_url_key],
			item[self.status_key],
			item[self.origin_key]
		])

	@classmethod
	def from_crawler(cls, crawler):
		return cls(
			crawler.settings.get('STORAGE_DIR'),
			crawler.settings.get('REPORT_CSV'),
			crawler.settings.get('NAMING_METHOD'),
			crawler.settings.get('MIMETYPE_EXTENSION')
		)

	def process_item(self, item, spider):
		if not item[self.status_key] and item[self.data_key]:
			mimetype = item[self.mimetype_key]
			extensions = self.mimetype2extension.get(mimetype, [])
			if len(extensions) == 1:
				ext = extensions[0]
			elif len(extensions) > 0:
				ext = ''.join(extensions)
			elif item[self.filename_key]:
				ext = os.path.splitext(item[self.filename_key])[1]
			else:
				ext = self.default_extension
			
			if self.naming_method == 1:
				filename = item[self.download_title_key]
			elif self.naming_method == 2:
				filename = '{} {}'.format(item[self.page_title_key], item[self.download_url_seq_key])
			elif self.naming_method == 3:
				filename = hashlib.md5(item[self.download_url_key].encode('utf8')).hexdigest()
			else:
				filename = item[self.filename_key]

			if not filename:
				filename = hashlib.md5(item[self.download_url_key].encode('utf8')).hexdigest()

			origin = filter_filename(item[self.origin_key])
			origin_dir = os.path.join(self.storage_dir, origin)
			if not os.path.exists(origin_dir):
				os.makedirs(origin_dir)

			filename = filter_filename(filename) + ext
			filename = os.path.join(origin_dir, filename)
			filename = unique_filename(filename)

			item[self.path_key] = filename
			
			data = item[self.data_key]
			with open(filename, 'wb') as f:
				f.write(data)

		self.add_report(item)
		return item