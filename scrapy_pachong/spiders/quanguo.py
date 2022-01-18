import scrapy
from scrapy_pachong.items import ScrapyPachongItem,ScrapytextItem

class QuanguoSpider(scrapy.Spider):
    #爬虫的名字
    name = 'quanguo'
    #运行访问的域名
    allowed_domains = ['www.jiangsu.gov.cn']
    #起始访问的地址
    start_urls = ['http://www.jiangsu.gov.cn/col/col76936/index.html']
    #执行start_urls后执行的方法
    def parse(self, response):
        #response是返回的对象，相当于request.get()
        news_list = response.xpath('//*[@id="298841"]/div/ul/li')
        for news in news_list:
            target = news.xpath('./a/text()').extract_first()
            new_url = news.xpath('./a/@href').extract_first()

            item = ScrapyPachongItem()
            item['target'] = target
            new_url = 'http://www.jiangsu.gov.cn' + new_url
            item['text_url'] = new_url

            yield item
            yield scrapy.Request(new_url, callback=self.parse_new)

    def parse_new(self,response):
        item = ScrapytextItem()
        ps = response.xpath('//*[@id="barrierfree_container"]/div[7]/div[1]/div/div[1]')
        item['new'] = ps.xpath("./text()").extract_first()
        text_list = response.xpath('//*[@id="zoom"]/p')
        ts=''
        for text in text_list:
            ts += text.xpath('./text()').extract_first()

        item['text'] = ts
        yield item
