import sys
from scrapy.utils.project import get_project_settings
# from scrapy_crawl_spider_zhw.spiders.universal import UniversalSpider
from scrapy_crawl_spider_zhw.utils import get_config_by_name
from scrapy.crawler import CrawlerProcess

def run():
    name=sys.argv[1]
    custom_settings=get_config_by_name(name)
    # 获取爬虫名称
    spider=custom_settings.get('spider','universal')
    # 合并项目全局设置
    project_settings=get_project_settings()
    settings=dict(project_settings.copy())
    settings.update(custom_settings.get('settings'))
    # 启动爬虫
    process=CrawlerProcess(settings)
    process.crawl(spider,**{'name':name})
    process.start()

if __name__ == '__main__':
    run()