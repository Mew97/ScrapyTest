from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

rules = (
    # Rule(LinkExtractor(allow='http://bus.mapbar.com/wuhan/xianlu/[0-9]{1,3}lu.*/', ),
    #      callback='parse_item', follow=True, ),
    Rule(LinkExtractor(allow='https://wuhan.8684.cn/x_.*', ),
         callback='parse_item', follow=False, ),
)
