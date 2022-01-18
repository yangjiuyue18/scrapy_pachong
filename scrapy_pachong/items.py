# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyPachongItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #标题
    target = scrapy.Field()
    #内容链接(href)
    text_url = scrapy.Field()

class ScrapytextItem(scrapy.Item):
    #标题
    new = scrapy.Field()
    #内容
    text = scrapy.Field()