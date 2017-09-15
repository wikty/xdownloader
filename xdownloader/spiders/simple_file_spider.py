import os, re, hashlib


import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from xdownloader.items import XDownloaderItem
from xdownloader.utils import get_domain


class SimpleFileSpider(CrawlSpider):

	name = 'simple-file-spider'
	main_url_key = 'MAIN_URL' # start page url list
	follow_links_key = 'FOLLOW_LINKS' # {'allow': (), 'deny': ()}
	download_links_key = 'DOWNLOAD_LINKS' # {'allow': (), 'deny': ()}
	allowed_domains_key = 'ALLOWED_DOMAINS' # []
	link_tags = ['a', 'area']
	link_attrs = ['href']

	def __init__(self, *args, **kwargs):
		super(SimpleFileSpider, self).__init__(*args, **kwargs)

	def start_requests(self):
		main_url = self.settings.getlist(self.main_url_key, [])
		if not main_url:
			raise Exception('main url is empty')
		download_links = self.settings.getdict(self.download_links_key, {})
		if not download_links or not download_links.get('allow'):
			raise Exception('download links is invalid: %s' % str(download_links))
		follow_links = self.settings.getdict(self.follow_links_key, {})
		if follow_links and not follow_links.get('allow'):
			raise Exception('follow links is invalid: %s' % str(follow_links))
		allowed_domains = self.settings.getlist(self.allowed_domains_key, [])
		
		self.allowed_domains = allowed_domains
		self.follow_links = self.rule2regex(follow_links)
		self.download_links = self.rule2regex(download_links)
		for title, url in main_url:
			if not self.is_allowed_domain(url):
				continue
			request = scrapy.Request(url, callback=self.parse_page)
			request.meta['page_title'] = title
			request.meta['page_url'] = url
			request.meta['origin'] = title
			yield request

	def rule2regex(self, rule):
		'''
		rule: {'allow': [], 'deny':[]}
		'''
		allow_regex = []
		deny_regex = []
		for allow_rule in rule.get('allow', []):
			allow_rule = allow_rule.strip()
			if not allow_rule:
				continue
			allow_regex.append(re.compile(allow_rule))
		for deny_rule in rule.get('deny', []):
			deny_rule = deny_rule.strip()
			if not deny_rule:
				continue
			deny_regex.append(re.compile(deny_rule))
		return {
			'allow': allow_regex,
			'deny':deny_regex
		}

	def is_allowed_domain(self, url):
		if not self.allowed_domains:
			return True
		domain = get_domain(url)
		for allowed_domain in self.allowed_domains:
			if domain.endswith(allowed_domain):
				return True
		return False

	def is_allowed_url(self, url, allow_regex=[], deny_regex=[]):
		for regex in deny_regex:
			if regex.search(url):
				return False
		if not allow_regex:
			return True
		for regex in allow_regex:
			if regex.search(url):
				return True
		return False

	def is_followable(self, url):
		if not self.is_allowed_domain(url):
			return False
		return self.is_allowed_url(url, self.follow_links['allow'], self.follow_links['deny'])

	def is_downloadable(self, url):
		if not self.is_allowed_domain(url):
			return False
		return self.is_allowed_url(url, self.download_links['allow'], self.download_links['deny'])

	def generate_item(self, 
		origin, 
		download_url, 
		download_url_seq, 
		download_title, 
		page_url,
		page_title,
		):
		item = XDownloaderItem()
		item['origin'] = origin
		item['download_url'] = download_url
		item['download_url_seq'] = download_url_seq
		item['download_title'] = download_title
		item['page_url'] = page_url
		item['page_title'] = page_title
		item['mimetype'] = None
		item['filename'] = None
		item['data'] = None
		item['status'] = None
		item['path'] = None
		return item

	def parse_page(self, response):
		origin = response.meta['origin']
		page_url = response.url
		page_title = ''.join(response.xpath('//head[1]/title/text()').extract())
		if not page_title:
			page_title = ''.join(response.xpath('//h1[1]/text()').extract())
		if not page_title:
			page_title = response.meta['page_title']
		count = 0
		for tag in self.link_tags:
			for link in response.xpath('//{}'.format(tag)):
				title = link.xpath('text()').extract_first(default='').strip()
				url = ''
				for attr in self.link_attrs:
					url = link.xpath('@{}'.format(attr)).extract_first(default='').strip()
					if url:
						break
				if not url:
					continue
				url = response.urljoin(url)
				if self.is_followable(url):
					request = scrapy.Request(url, callback=self.parse_page, dont_filter=False)
					request.meta['page_url'] = url
					request.meta['page_title'] = title
					request.meta['origin'] = origin
					yield request
				elif self.is_downloadable(url):
					count += 1
					yield self.generate_item(origin, url, count, title, page_url, page_title)