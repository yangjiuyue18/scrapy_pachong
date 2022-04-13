# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class ScrapyPachongPipeline:
    def __init__(self):
        #连接数据库
        self.connect = pymysql.connect(host='192.168.1.103',port=3306,user='root',password='root',db='quanguo',charset='utf8')
        #游标，用来执行数据库
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):

        sql_foreign = ''
        for key in item['provincials_foreign']:
            #tup = ('2020-11-1','北京',3)
            tup = (item['date'],key,int(item['provincials_foreign'][key]))
            sql_foreign += (str(tup)+',')
        sql_foreign = sql_foreign.rstrip(',')

        sql_citys = ''
        for key in item['citys_china']:
            # tup = ('2020-11-1','大连市',3)
            tup = (item['date'],key,int(item['citys_china'][key]))
            sql_citys += (str(tup)+',')
        #去掉最后一个“，”
        sql_citys = sql_citys.rstrip(',')

        sql_citys_new = ''
        for key in item['citys_china']:
            # tup = ('2020-11-1','北京',3)
            tup = (item['date'],key,int(item['citys_china'][key]))
            sql_citys_new += (str(tup)+',')
        #去掉最后一个“，”
        sql_citys_new = sql_citys.rstrip(',')


        #港澳台地区（日期，香港累计人数，香港出院人数，香港死亡人数，澳门累计人数，澳门出院人数，澳门死亡人数，台湾累计人数，台湾出院人数，台湾死亡人数）
        sql_other_count = "insert into other_count (dt,xiang_number,xiang_heal,xiang_deal,ao_number,ao_heal,ao_deal,tai_number,tai_heal,tai_deal) values ('%s',%d,%d,%d,%d,%d,%d,%d,%d,%d)" \
              %(item['date'],int(item['xiang_number']),int(item['xiang_heal']),int(item['xiang_deal']),int(item['ao_number']),int(item['ao_heal']),int(item['ao_deal']),int(item['tai_number']),
                int(item['tai_heal']),int(item['tai_deal']))
        #全国今日新增（日期，当日新增确诊人数，当日新增境外输入，当日新增本土病例，当日新增疑似病例，当日新增死亡病例，当日新增死亡病例）
        sql_china_today = "insert into china_today (dt,number_today,foreign_today,citys_today,probable_today,deal_today,heal_today) values ('%s',%d,%d,%d,%d,%d,%d)" \
                          %(item['date'],int(item['number_today']),int(item['foreign_today']),int(item['citys_today']),int(item['probable_today']),int(item['deal_today']),int(item['heal_today']))
        #全国累计病例（日期，现有确诊人数，现有疑似病例，累计治愈出院病例，累计死亡病例，累计确诊病例）
        sql_china_count = "insert into china_count (dt,number_now,probable_now,heal_count,deal_count,number_count) values ('%s',%d,%d,%d,%d,%d)" \
                          %(item['date'],int(item['china_number_now']),int(item['china_probable_now']),int(item['china_heal_count']),int(item['china_deal_count']),int(item['china_number_count']))
        #累计境外输入病例（日期，境外输入现有确诊，累计确诊，累计出院人数）
        sql_foreign_count = "insert into foreign_count (dt,number_now,number_count,heal_count) values ('%s',%d,%d,%d)" \
                            %(item['date'],int(item['foreign_number_now']),int(item['foreign_number_count']),int(item['foreign_heal_count']))
        #境外新增（id，日期，省份，数量）
        sql_foreign_today = "insert into foreign_today (dt,provincials,ft_number) values %s;" %(sql_foreign)
        #本土病例（id，日期，省份，城市，数量）
        sql_citys_today = "insert into citys_today (dt,citys,ct_number) values %s;" %(sql_citys)
        #本土病例（新版）
        sql_citys_today_new = "insert into citys_today (dt,provincials,ct_number) values %s;" % (sql_citys_new)
        #由于本土病例缺少了省份，现在需要对应city表，把城市对应的省份拿过来
        sql_citys_provincials = "update citys_today set provincials = (select provincials from city where citys_today.citys = city.cityName)"
        #根据citys_today表中的时间和城市，来删除重复数据
        sql_delete_ct = "delete from citys_today where id in(select m.id from (select id from citys_today A, (select dt,citys from citys_today group by dt,citys having count(*)>1) B where A.dt = B.dt and A.citys = B.citys and A.id not in (select min(id) as ID from citys_today group by dt,citys having count(*)>1)) m)"
        #根据foreign_today表中的时间和省份，来删除重复数据
        sql_delete_ft = "delete from foreign_today where id in(select m.id from (select id from foreign_today A, (select dt,provincials from foreign_today group by dt,provincials having count(*)>1) B where A.dt = B.dt and A.provincials = B.provincials and A.id not in (select min(id) as ID from foreign_today group by dt,provincials having count(*)>1)) m)"

        # self.cursor.execute(sql_other_count)
        # self.cursor.execute(sql_china_today)
        # self.cursor.execute(sql_china_count)
        # self.cursor.execute(sql_foreign_count)
        # self.cursor.execute(sql_foreign_today)
        # self.cursor.execute(sql_citys_today)
        # self.cursor.execute(sql_citys_provincials)
        # self.cursor.execute(sql_delete_ct)
        # self.cursor.execute(sql_delete_ft)
        try:
            self.cursor.execute(sql_other_count)
        except IndexError:
            print("other_count表报错")
        try:
            self.cursor.execute(sql_china_today)
        except IndexError:
            print("china_today表报错")
        try:
            self.cursor.execute(sql_china_count)
        except IndexError:
            print("china_count表报错")
        try:
            self.cursor.execute(sql_foreign_count)
        except IndexError:
            print("foreign_count表报错")
        try:
            self.cursor.execute(sql_foreign_today)
            self.cursor.execute(sql_delete_ft)
        except IndexError:
            print("foreign_today表报错")
        # try:
        #     self.cursor.execute(sql_citys_today)
        #     self.cursor.execute(sql_citys_provincials)
        #     self.cursor.execute(sql_delete_ct)
        # except IndexError:
        #     print("citys_today爬虫出现城市问题")
        try:
            self.cursor.execute(sql_delete_ct)
            self.cursor.execute(sql_citys_today_new)
        except IndexError:
            print("citys_today2爬虫出现城市问题")

        self.connect.commit()
        return item


    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()