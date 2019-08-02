# -*- coding: utf-8 -*-

# Scrapy settings for Drivy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Drivy'

SPIDER_MODULES = ['Drivy.spiders']
NEWSPIDER_MODULE = 'Drivy.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Drivy (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 10
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'fr',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'Drivy.middlewares.DrivySpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'Drivy.middlewares.DrivyDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'Drivy.pipelines.DrivyPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

ROTATING_PROXY_LIST = [
'165.22.105.131:3128',
'185.253.185.89:8080',
'190.111.246.128:80',
'183.111.25.253:8080',
'198.211.99.93:8080',
'103.77.8.59:8080',
'35.235.75.244:3128',
'129.205.138.186:54182',
'24.172.34.114:34154',
'180.183.244.193:8213',
'197.35.194.150:8080',
'165.22.134.199:3128',
'206.189.30.235:80',
'89.28.164.55:8080',
'165.227.30.130:3128',
'18.191.95.234:3128',
'109.169.65.206:8080',
'104.248.117.3:8080',
'103.199.99.84:8080',
'20.41.41.145:3128',
'196.25.12.2:56015',
'78.108.110.113:8080',
'3.212.104.192:3128',
'162.144.220.192:80',
'181.10.238.221:42286',
'104.43.244.233:80',
'139.180.175.178:8000',
'93.125.45.3:8080',
'213.141.93.60:44122',
'101.108.246.147:8080',
'80.67.195.201:81',
'221.4.172.162:3128',
'165.22.236.64:8080',
'165.227.82.122:8080',
'27.147.218.188:8080',
'81.92.202.192:80',
'75.151.213.85:8080',
'187.19.165.167:8080',
'184.191.162.4:3128',
'109.199.147.178:38339',
'174.138.59.60:3128',
'183.89.197.123:8080',
'31.220.51.173:80',
'165.227.94.159:3128',
'76.185.16.94:54079',
'52.200.15.237:80',
'82.85.144.92:48897',
'159.203.87.130:3128',
'66.43.34.50:8080',
'36.66.220.173:44233'

]

DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
}
SPLASH_URL = 'http://localhost:8050'
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
