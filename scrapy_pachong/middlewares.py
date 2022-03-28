# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import time
from scrapy import signals
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.http.response.html import HtmlResponse

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
# Options.add_argument('-headless')
# Options.add_experimental_option("excludeSwitches", ['enable-automation'])

class ScrapyPachongSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ScrapyPachongDownloaderMiddleware:


    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)

        return s

    def spider_opened(self,spider):
        #创建selenium的chrome浏览器对象
        # chromedriver.exe已配置在环境变量path中

        chromeOptions = webdriver.ChromeOptions()
        # 加载无窗口浏览器
        chromeOptions.add_argument('--headless')
        chromeOptions.add_argument('--disable-dev-shm-usage')
        chromeOptions.add_argument('--no-sandbox') # 以根用户打身份运行Chrome，使用-no-sandbox标记重新运行Chrome,禁止沙箱启动
        self.chrome = Chrome(chrome_options=chromeOptions)

    def spider_closed(self,spider):
        self.chrome.quit()

    def process_request(self,request,spider):
        self.chrome.get(request.url)
        time.sleep(2)
        return HtmlResponse(url=request.url, body=self.chrome.page_source, request=request, encoding='utf-8',
                            status=200)
