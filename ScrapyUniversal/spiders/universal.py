from scrapy.spiders import CrawlSpider
from ScrapyUniversal.items import UniversalItem
from ScrapyUniversal.loaders import UniversalLoader
from ScrapyUniversal.rules import rules
from ScrapyUniversal.custom_settings import SPIDER, START_URS, ALLOWED_DOMAINS, ITEM
import re

"""
职位名称，岗位类别，薪资范围，城市，公司名字，主营业务，公司规模，公司福利，岗位职责，岗位要求，发布时间(最好近3年)，发布网站
"""


class UniversalSpider(CrawlSpider):
    name = SPIDER
    start_urls = START_URS
    allowed_domains = ALLOWED_DOMAINS

    rules = rules

    def parse_item(self, response):
        item = UniversalItem()
        item['bus_num'] = response.xpath('//*[@id="bus_line"]/div[1]/div/div[1]/h1/text()').extract_first().strip().replace("&nbsp", "")
        item['bus_list'] = response.xpath('//*[@id="bus_line"]/div[5]/div/div/a/text()').extract()

        print(item)

        # c_welfare_l = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/div/div//text()').extract()
        # c_welfare_str = ""
        # for i in c_welfare_l:
        #     if i == "":
        #         pass
        #     else:
        #         c_welfare_str = c_welfare_str + i.strip() + ' '
        # item['c_welfare'] = c_welfare_str
        # j_responsibilities_l = response.xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div//text()').extract()
        # j_responsibilities_str = ""
        # for i in j_responsibilities_l:
        #     if i == "":
        #         pass
        #     else:
        #         j_responsibilities_str = j_responsibilities_str + i.strip() + ' '
        # item['j_responsibilities'] = j_responsibilities_str
        #
        # all_job_l = ['初中及以下', '高中', '中技', '中专', '大专', '本科', '硕士', '博士']
        # j_r = response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()[3]').extract_first().strip()
        # if j_r not in all_job_l:
        #     j_r = '无要求'
        # item['j_requirements'] = j_r
        # str_re_time = str(response.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()').extract())
        # re_a = ".*(..-....).*"
        # re_a_af = re.match(re_a, str_re_time)
        # if re_a_af:
        #     print(re_a_af.group(1))
        #     item['release_time'] = re_a_af.group(1)
        #
        # item['release_web'] = '51job'
        yield item




