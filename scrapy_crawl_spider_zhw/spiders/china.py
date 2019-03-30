# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_crawl_spider_zhw.items import ScrapyCrawlSpiderZhwItem
from scrapy_crawl_spider_zhw.Itemloaders import ChinaLoader


class ChinaSpider(CrawlSpider):
    name = 'china'
    allowed_domains = ['tech.china.com']
    start_urls = ['https://tech.china.com/articles/']
    rules = (
        Rule(LinkExtractor(allow=r'article\/.*\.html', restrict_xpaths="//div[@class='con_item']"),
             callback='parse_item'),
        Rule(LinkExtractor(restrict_xpaths="//div[@id='pageStyle']/a[contains(.,'下一页')]"), follow=True),
    )

    def parse_item(self, response):
        loader = ChinaLoader(item=ScrapyCrawlSpiderZhwItem(), response=response)
        # item = ScrapyCrawlSpiderZhwItem()
        loader.add_xpath('title', "//h1[@id='chan_newsTitle']/text()")
        loader.add_value('url', response.url)
        loader.add_xpath('text', "//div[@id='chan_newsDetail']//text()")
        loader.add_xpath('datetime', "//div[@id='chan_newsInfo']/text()", re=r"(\d+-\d+-\d+\s\d+:\d+:\d+)")
        loader.add_xpath('source', "//div[@id='chan_newsInfo']/text()", re=r"来源：(.*)")
        loader.add_value('website', '中华网')
        yield loader.load_item()
