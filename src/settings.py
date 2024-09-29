# Scrapy settings for src project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "alibaba-crawlerplus-v2"

SPIDER_MODULES = ["src.spiders"]
NEWSPIDER_MODULE = "src.spiders"


# Never obey robots.txt rules
ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 1
CONCURRENT_ITEMS = 1

DOWNLOAD_DELAY = 3

DOWNLOADER_MIDDLEWARES = {
    "src.middlewares.RandomUserAgentMiddleware": 543,
}

# ITEM_PIPELINES = {
#    "src.pipelines.SrcPipeline": 300,
# }

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
