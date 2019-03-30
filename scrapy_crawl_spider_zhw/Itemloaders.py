from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, TakeFirst, Compose,MapCompose


class NewsLoader(ItemLoader):
    default_output_processor = TakeFirst()

def each_strip(x):
    for i in x:
        yield i.strip()

class ChinaLoader(NewsLoader):
    text_out = Compose(each_strip,Join())
    source_out = Compose(Join(), lambda s: s.strip())
