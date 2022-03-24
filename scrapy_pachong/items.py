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
    #时间
    date = scrapy.Field()
    number_today = scrapy.Field()
    foreign_today = scrapy.Field()
    citys_today = scrapy.Field()
    deal_today = scrapy.Field()
    probable_today = scrapy.Field()
    heal_today = scrapy.Field()
    foreign_number_now = scrapy.Field()
    foreign_number_count = scrapy.Field()
    foreign_heal_count = scrapy.Field()
    china_number_count = scrapy.Field()
    china_heal_count = scrapy.Field()
    china_deal_count = scrapy.Field()
    china_number_now = scrapy.Field()
    china_probable_now = scrapy.Field()
    xiang_deal = scrapy.Field()
    xiang_heal = scrapy.Field()
    xiang_number = scrapy.Field()
    ao_deal = scrapy.Field()
    ao_heal = scrapy.Field()
    ao_number = scrapy.Field()
    tai_deal = scrapy.Field()
    tai_heal = scrapy.Field()
    tai_number = scrapy.Field()
    provincials_foreign = scrapy.Field()
    citys_china = scrapy.Field()