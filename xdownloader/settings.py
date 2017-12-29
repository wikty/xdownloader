# -*- coding: utf-8 -*-

# Scrapy settings for downloader project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'xdownloader'

SPIDER_MODULES = ['xdownloader.spiders']
NEWSPIDER_MODULE = 'xdownloader.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'downloader (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'downloader.middlewares.DownloaderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'xdownloader.middlewares.DownloaderSpiderMiddleware': 543,
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'xdownloader.pipelines.DownloadFilePipeline': 123,
   'xdownloader.pipelines.SaveFilePipeline': 124
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

LOG_FILE='logs'
LOG_LEVEL='ERROR'

###
# custom settings
###
# mimetype to extension mapping
MIMETYPE_EXTENSION='mimetype_extension.txt'
# start page's url
MAIN_URL=[
	# ('Machine Learning Tom Mitchell', 'http://www.cs.cmu.edu/~tom/10601_fall2012/lectures.shtml'),
	# ('Statistical Data Mining Tutorials Andrew Moore', 'https://www.autonlab.org/tutorials/list.html')
	# ('厦门大学经济学院', 'http://soe.xmu.edu.cn/info/graduate/2017-09-15-17251.html'),
    ('CAUSALITY by Judea Pearl', 'http://bayes.cs.ucla.edu/BOOK-99/book-toc.html'),

]
ALLOWED_DOMAINS=[]
# the directory to store files
STORAGE_DIR='/downloads'
# report file
REPORT_CSV='/downloads/report.csv'
# download file naming method
# 1 使用下载链接的名字来命名
# 2 使用下载页面的 Title 结合数字编号来命名
# 3 使用下载链接的 md5(URL) 结合数字编码来命名
# 4 使用网站为下载资源指定的文件名来命名
# 5 使用下载链接的 basename 来命名
NAMING_METHOD = 1
# follow links
# FOLLOW_LINKS={
# 	'allow':[r'/tutorials/\w+\.html$'],
# 	'deny': []
# }
# download links
DOWNLOAD_LINKS={
	'allow': [r'/\w+\.pdf$'],
	'deny': []
}
# DOWNLOAD_LINKS={
# 	'allow': [r'/AttachmentDownload\.aspx\?id=\{[-\d\w]+\}$'],
# 	'deny': []
# }