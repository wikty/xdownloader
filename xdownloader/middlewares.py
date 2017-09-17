# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import os
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType


class DownloaderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class PhantomjsRequestMiddleware(object):
    
    def __init__(self, driver_path, extra_script_file=None, driver_args={}):
        '''
        Python script <---> Ghostdriver <---> PhantomJS
        GhostDriver is designed to be integral part of PhantomJS itself
        '''
        if not os.path.isfile(driver_path):
            raise Exception('phantomjs/driver path not exists: %s' % driver_path)
        if extra_script_file and not os.path.isfile(extra_script_file):
            raise Exception('extra script file not exists: %s' % extra_script_file)
        
        self.driver = webdriver.PhantomJS(executable_path=driver_path, **driver_args)
        if extra_script_file:
            with open(extra_script_file, 'r', encoding='utf8') as f:
                self.script = f.read()
        else:
            self.script = None

    @classmethod
    def from_crawler(cls, crawler):
        driver_path = crawler.settings.get('PHANTOMJS_PATH')
        extra_script_file = crawler.settings.get('EXTRA_SCRIPT_FILE')
        return cls(driver_path, extra_script_file)

    def process_request(self, request, spider):
        url, encoding = request.url, request.encoding
        self.driver.get(url)
        if self.script:
            self.driver.execute_script(self.script)
        url = self.driver.current_url
        body = self.driver.page_source.encode(encoding)
        response = HtmlResponse(url=url, body=body, encoding=encoding)
        return response # end any process_request methods


class ProxyPhantomjsRequestMiddleware(PhantomjsRequestMiddleware):

    def __init__(self, driver_path, extra_script_file, driver_args):
        super(ProxyPhantomjsRequestMiddleware, self).__init__(driver_path, extra_script_file, driver_args)

    @classmethod
    def from_crawler(cls, crawler):
        driver_path = crawler.settings.get('PHANTOMJS_PATH')
        extra_script_file = crawler.settings.get('EXTRA_SCRIPT_FILE')
        http_proxy = crawler.settings.get('HTTP_PROXY')
        if not http_proxy:
            raise Exception('http proxy setting is empty')
        driver_args = {
            'proxy': Proxy({
                'proxyType': ProxyType.MANUAL,
                'httpProxy': proxy,
                'ftpProxy': proxy,
                'sslProxy': proxy,
                'noProxy': ''
            })
        }
        return cls(driver_path, extra_script_file, driver_args)