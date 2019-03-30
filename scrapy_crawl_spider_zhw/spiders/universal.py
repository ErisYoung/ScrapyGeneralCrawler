# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_crawl_spider_zhw.utils import get_config_by_name
from scrapy_crawl_spider_zhw.rules import rules
from scrapy_crawl_spider_zhw.items import ScrapyCrawlSpiderZhwItem
from scrapy_crawl_spider_zhw.Itemloaders import *
from scrapy_crawl_spider_zhw import urls


class UniversalSpider(CrawlSpider):
    name = 'universal'

    def __init__(self, name, *args, **kwargs):
        config = get_config_by_name(name)
        print(name)
        self.config = config
        self.rules = rules.get(self.config.get('rules'))
        start_urls = config.get('start_urls')
        if start_urls:
            if start_urls.get('type')=='static':
                self.start_urls=start_urls.get('value')
            elif start_urls.get('type')=='dynamic':
                self.start_urls=eval("urls."+start_urls.get('method'))(*start_urls.get('args',[]))
        self.allowed_domains = config.get('allowed_domains')
        super().__init__(*args, **kwargs)

    def parse_item(self, response):
        item = self.config.get('item')
        if item:
            cls = eval(item.get('class'))()
            loader = eval(item.get("loader"))(cls, response=response)
            for key, value in item.get('attrs').items():
                for extractor in value:
                    if extractor.get('method') == 'xpath':
                        loader.add_xpath(key, *extractor.get('args'), **{"re": extractor.get('re')})
                    if extractor.get('method') == 'css':
                        loader.add_css(key, *extractor.get('args'), **{"re": extractor.get('re')})
                    if extractor.get('method') == 'value':
                        loader.add_value(key, *extractor.get('args'), **{"re": extractor.get('re')})
                    if extractor.get('method') == 'attr':
                        loader.add_value(key, getattr(response, *extractor.get('args')))
            yield loader.load_item()
