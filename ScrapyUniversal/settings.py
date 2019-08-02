BOT_NAME = 'ScrapyUniversal'
SPIDER_MODULES = ['ScrapyUniversal.spiders']
NEWSPIDER_MODULE = 'ScrapyUniversal.spiders'
ROBOTSTXT_OBEY = False
# LOG_LEVEL = 'WARNING'
SELENIUM_TIMEOUT = 20
PHANTOMJS_SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']
DOWNLOAD_PATH = 'project.txt'

RANDOMIZE_DOWNLOAD_DELAY = False
DOWNLOAD_DELAY = 60/600.0
# CONCURRENT_REQUESTS_PER_IP = 60

PROXYSERVER = "http://http-dyn.abuyun.com:9020"
PROXYUSER = "HX5HDV6W6J06U37D"
PROXYPASS = "AE629A4F0A399646"

DOWNLOADER_MIDDLEWARES = {
    # 'ScrapyUniversal.middlewares.SeleniumMiddleware': 543,
    # 'ScrapyUniversal.middlewares.RandomProxy': 303,
    'ScrapyUniversal.middlewares.RandomHeader': 302,
    # 'ScrapyUniversal.middlewares.ProxyMiddleware': 301,

}


ITEM_PIPELINES = {
    
    'ScrapyUniversal.pipelines.MongoPipeline': 300,
    
}


ALICE_MONGO_URI = 'mongodb://admin:admin@192.168.11.30:27017/admin'


MONGO_DB = 'bus1'
