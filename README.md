# scrapy_pachong

#### 介绍
需求是实现对疫情数据的爬取和自然语言的分析，拿到每日数据后存入mysql
#### 软件架构
软件架构说明


#### 安装教程

使用的scrapy和selenium，获取到数据后打算用jieba库来进行切割，将处理好的数据存入mysql

#### 使用说明

创建爬虫项目 scrapy startproject 项目名字
创建爬虫文件 cd scrapy_pachong\scrapy_pachong\spiders
	    scrapy genspider 爬虫文件名 爬取网页地址
运行爬虫代码 scrapy crawl 爬虫文件名

http://www.jiangsu.gov.cn/col/col76936/index.html

CrawlSpider
scrapy genspider -t crawl 爬虫文件名 爬取网页地址


