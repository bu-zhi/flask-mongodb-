# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Test1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    download = scrapy.Field() #标题
    number = scrapy.Field()
    #Class = scrapy.Field()
    content = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    pass
