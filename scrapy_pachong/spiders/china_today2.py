import scrapy
from scrapy_pachong.items import ScrapyPachongItem,ScrapytextItem
import re
import time
import jieba
import jieba.posseg as pseg

# 遗憾的是现在国家卫健委发布的信息中，本土病例不再精确到某一个城市，现在只能将代码进行修改
class QuanguoSpider(scrapy.Spider):
    #爬虫的名字
    name = 'china_today2'
    allowed_domains = ['www.jiangsu.gov.cn']
    start_urls = ['http://www.jiangsu.gov.cn/col/col76936/index.html?uid=298841&pageNum=1']

    def parse(self, response):
        #response是返回的对象，相当于request.get()
        news_list = response.xpath('/html/body/div[1]/div[8]/div/div/div/div/ul/li[1]')
        target = news_list.xpath('./a/text()').extract_first()
        new_url = news_list.xpath('./a/@href').extract_first()

        item = ScrapyPachongItem()
        item['target'] = target
        new_url = 'http://www.jiangsu.gov.cn' + new_url
        item['text_url'] = new_url

        yield item
        yield scrapy.Request(new_url, callback=self.parse_new)
        time.sleep(3)

    def parse_new(self,response):
        item = ScrapytextItem()
        #获取标题
        ps = response.xpath('//*[@id="barrierfree_container"]/div[7]/div[1]/div/div[1]')
        item['new'] = ps.xpath("./text()").extract_first()

        #通过re表达式来获取到日期
        data = response.xpath('//*[@id="barrierfree_container"]/div[7]/div[1]/div/div[2]/font[1]')
        rule = re.compile('\d+-\d+-\d+')
        item['date'] = rule.findall(data.xpath('./text()').extract_first())[0]

        #获取文本内容
        text_list_strong = response.xpath('//*[@id="zoom"]/p/strong/text()').extract()
        text_list = response.xpath('//*[@id="zoom"]/p')
        text=''
        count =0
        for ts in text_list:
            try:
                #判断文本中有没有strong标签
                if text_list_strong[0]:
                    if count == 0 :
                        text += ts.xpath('./text()').extract()[0]
                        text += text_list_strong[0]
                        text += ts.xpath('./text()').extract()[1]
                        text += text_list_strong[1]
                        text += ts.xpath('./text()').extract()[2]
                    elif count == 4:
                        text += ts.xpath('./text()').extract()[0]
                        text += text_list_strong[2]
                        text += ts.xpath('./text()').extract()[1]
                    # elif count == 6:
                    #     text += text_list_strong[2]
                    #     text += ts.xpath('./text()').extract()[0]
                    else:
                        text += ts.xpath('./text()').extract()[0]
                    count+=1
                else:
                    text += ts.xpath('./text()').extract()[0]
            except IndexError:
                pass

        item['text'] = text

        provincials = {'北京': '', '天津': '', '上海': '', '重庆': '', '河北': '', '山西': '', '台湾': '', '辽宁': '', '吉林': '',
                       '黑龙江': '', '江苏': '', '浙江': '', '安徽': '', '福建': '', '江西': '', '山东': '', '河南': '', '湖北': '',
                       '湖南': '', '广东': '', '甘肃': '', '四川': '', '贵州': '', '海南': '', '云南': '', '青海': '', '陕西': '',
                       '广西': '', '西藏自治区': '', '宁夏回族自治区': '', '新疆维吾尔自治区': '', '内蒙古': '', '澳门特别行政区': '', '香港特别行政区': ''}
        citys = {'北京': '', '天津': '', '上海': '', '重庆': '', '石家庄市': '', '唐山市': '', '秦皇岛市': '', '邯郸市': '', '邢台市': '',
                 '保定市': '', '张家口市': '', '承德市': '', '沧州市': '', '廊坊市': '', '衡水市': '', '太原市': '', '大同市': '', '阳泉市': '',
                 '长治市': '', '晋城市': '', '朔州市': '', '晋中市': '', '运城市': '', '忻州市': '', '临汾市': '', '吕梁市': '', '沈阳市': '',
                 '大连市': '', '鞍山市': '', '抚顺市': '', '本溪市': '', '丹东市': '', '锦州市': '', '营口市': '', '阜新市': '', '辽阳市': '',
                 '盘锦市': '', '铁岭市': '', '朝阳市': '', '葫芦岛市': '', '长春市': '', '吉林市': '', '四平市': '', '辽源市': '', '通化市': '',
                 '白山市': '', '松原市': '', '白城市': '', '延边朝鲜族自治州': '', '哈尔滨市': '', '齐齐哈尔市': '', '鹤岗市': '', '双鸭山市': '',
                 '鸡西市': '', '大庆市': '', '伊春市': '', '牡丹江市': '', '七台河市': '', '黑河市': '', '绥化市': '', '大兴安岭地区': '', '南京市': '',
                 '无锡市': '', '徐州市': '', '常州市': '', '苏州市': '', '南通市': '', '连云港市': '', '淮安市': '', '盐城市': '', '扬州市': '',
                 '镇江市': '', '泰州市': '', '宿迁市': '', '杭州市': '', '宁波市': '', '温州市': '', '嘉兴市': '', '湖州市': '', '绍兴市': '',
                 '金华市': '', '衢州市': '', '舟山市': '', '台州市': '', '丽水市': '', '合肥市': '', '芜湖市': '', '蚌埠市': '', '淮南市': '',
                 '马鞍山市': '', '淮北市': '', '铜陵市': '', '安庆市': '', '黄山市': '', '滁州市': '', '阜阳市': '', '宿州市': '', '巢湖市': '',
                 '六安市': '', '毫州市': '', '池州市': '', '宣城市': '', '福州市': '',
                 '厦门市': '', '莆田市': '', '三明市': '', '泉州市': '', '漳州市': '', '南平市': '', '龙岩市': '', '宁德市': '', '南昌市': '',
                 '景德镇市': '', '萍乡市': '', '九江市': '', '新余市': '', '鹰潭市': '', '赣州市': '', '吉安市': '', '宜春市': '', '抚州市': '',
                 '上饶市': '', '济南市': '', '青岛市': '', '淄博市': '', '枣庄市': '', '东营市': '', '烟台市': '', '潍坊市': '', '济宁市': '',
                 '泰安市': '', '威海市': '', '日照市': '', '莱芜市': '', '临沂市': '', '德州市': '', '聊城市': '', '滨州市': '', '菏泽市': '',
                 '郑州市': '', '开封市': '', '洛阳市': '', '平顶山市': '', '安阳市': '', '鹤壁市': '', '新乡市': '', '焦作市': '', '濮阳市': '',
                 '三门峡市': '', '南阳市': '', '商丘市': '', '信阳市': '', '周口市': '', '驻马店市': '', '济源市': '', '武汉市': '', '黄石市': '',
                 '十堰市': '', '荆州市': '', '宜昌市': '', '襄樊市': '', '鄂州市': '', '荆门市': '', '孝感市': '', '黄冈市': '', '咸宁市': '',
                 '随州市': '', '仙桃市': '', '天门市': '', '潜江市': '', '神龙架': '', '恩施土家苗族自治州': '', '长沙市': '', '株洲市': '',
                 '湘潭市': '', '衡阳市': '', '邵阳市': '', '岳阳市': '', '常德市': '', '张家界市': '', '益阳市': '', '郴州市': '', '永州市': '',
                 '怀化市': '', '娄底市': '', '详细土家苗族自治州': '', '广州市': '', '深圳市': '', '珠海市': '', '汕头市': '', '韶关市': '',
                 '佛山市': '', '江门市': '', '湛江市': '', '茂名市': '', '肇庆市': '', '惠州市': '', '梅州市': '', '汕尾市': '', '河源市': '',
                 '阳江市': '', '清远市': '', '东莞市': '', '中山市': '', '潮州市': '', '揭阳市': '',
                 '云浮市': '', '兰州市': '', '金昌市': '', '白银市': '', '天水市': '', '嘉峪关市': '', '武威市': '', '张掖市': '', '平凉市': '',
                 '酒泉市': '', '庆阳市': '', '定西市': '', '陇南市': '', '临夏回族自治州': '', '甘南藏族自治州': '', '成都市': '', '自贡市': '',
                 '攀枝花市': '', '泸州市': '', '德阳市': '', '绵阳市': '', '广元市': '', '遂宁市': '', '内江市': '', '乐山市': '', '南充市': '',
                 '眉山市': '', '宜宾市': '', '广安市': '', '达州市': '', '雅安市': '', '巴中市': '', '资阳市': '', '阿坝藏族羌族自治州': '',
                 '甘孜彝族自治州': '', '凉山彝族自治州': '', '贵阳市': '', '六盘水市': '', '遵义市': '', '安顺市': '', '铜仁': '', '毕节': '',
                 '黔西南布依族苗族自治州': '', '黔东南苗族侗族自治州': '', '黔南布依族苗族自治州': '', '海口市': '', '三亚市': '', '五指山市': '', '琼海市': '',
                 '儋州市': '', '文昌市': '', '万宁市': '', '东方市': '', '澄迈县': '', '屯昌县': '', '安定县': '', '临高县': '', '白沙黎族自治县': '',
                 '昌江黎族自治县': '', '乐东黎族自治县': '', '陵水黎族自治县': '', '保亭黎族苗族自治县': '', '琼中黎族苗族自治县': '', '昆明市': '', '曲靖市': '',
                 '玉溪市': '', '保山市': '', '昭通市': '', '丽江市': '', '思茅市': '', '临沧市': '', '文山壮族苗族自治州': '', '红河哈尼族彝族自治州': '',
                 '西双版纳傣族自治州': '', '楚雄彝族自治州': '', '大理白族自治州': '', '德宏傣族景颇族自治州': '', '怒江傈傈族自治州': '', '迪庆藏族自治州': '',
                 '西宁市': '', '海东': '', '海北藏族自治州': '', '黄南藏族自治州': '', '海南藏族自治州': '', '果洛藏族自治州': '',
                 '玉树藏族自治州': '', '海西蒙古族藏族自治州': '', '西安市': '', '铜川市': '', '宝鸡市': '', '咸阳市': '', '渭南市': '', '延安市': '',
                 '汉中市': '', '榆林市': '', '安康市': '', '商洛市': '', '南宁市': '', '柳州市': '', '桂林市': '', '梧州市': '', '北海市': '',
                 '防城港市': '', '钦州市': '', '贵港市': '', '玉林市': '', '百色市': '', '贺州市': '', '河池市': '', '来宾市': '', '崇左市': '',
                 '拉萨市': '', '那曲': '', '昌都': '', '山南': '', '日喀则': '', '阿里': '', '林芝': '', '银川市': '', '石嘴山市': '',
                 '吴忠市': '', '固原市': '', '中卫市': '', '乌鲁木齐市': '', '克拉玛依市': '', '石河子市': '', '阿拉尔市': '', '图木舒克市': '',
                 '五家渠市': '', '吐鲁番市': '', '阿克苏市': '', '喀什市': '', '哈密市': '', '和田市': '', '阿图什市': '', '库尔勒市': '', '昌吉市': '',
                 '阜康市': '', '米泉市': '', '博乐市': '', '伊宁市': '', '奎屯市': '', '塔城市': '', '乌苏市': '', '阿勒泰市': '', '呼和浩特市': '',
                 '包头市': '', '乌海市': '', '赤峰市': '', '通辽市': '', '鄂尔多斯市': '', '呼伦贝尔市': '', '巴彦淖尔市': '', '乌兰察布市': '',
                 '锡林郭勒盟': '', '兴安盟': '', '阿拉善盟': '', '澳门特别行政区': '', '香港特别行政区': ''}

        # 将括号（）变成文字 开始 与 结束
        text = text.replace('（', '开始')
        text = text.replace('）', '结束')
        text = text.replace('。', '句号')

        # 添加自定义数据库
        jieba.load_userdict('D:/毕设项目/爬虫项目/scrapy_pachong/ns.txt')

        #将所有需要获取的数据先赋值
        number_today = 0
        foreign_today = 0
        citys_today = 0
        deal_today = 0
        probable_today = 0
        heal_today = 0
        foreign_number_now = 0
        china_number_now = 0
        xiang_number = 0
        ao_number = 0
        tai_number = 0
        foreign_number_count = 0
        foreign_heal_count = 0
        china_number_count = 0
        china_heal_count = 0
        china_deal_count = 0
        china_probable_now = 0
        xiang_deal = 0
        xiang_heal = 0
        ao_deal = 0
        ao_heal = 0
        tai_deal = 0
        tai_heal = 0
        provincials_foreign = provincials.copy()
        citys_china = provincials.copy()

        #根据词性来对内容进行切割
        words = pseg.cut(text)
        lst = [x.word for x in words if x.flag == 'ns' or x.flag == 'm']
        print(lst)

        for index in range(len(lst)):
            try:
                if lst[index] == '新增确诊病例':
                    if number_today == 0:
                        number_today = lst[index + 1]

                elif lst[index] == '本土病例':
                    if citys_today == 0:
                        citys_today = lst[index + 1]
                        if lst[index + 2] == '开始' or lst[index + 1] == '开始':
                            for i in range(index + 2, len(lst)):
                                if lst[i] == '结束' and lst[i-1] != '开始':
                                    break
                                elif lst[i] in citys_china.keys() and not citys_china[lst[i]]:
                                    # # 因为在城市中会出现 ‘在’ 和 ‘均在’两个词，所以要对两个词进行特殊判断
                                    # if lst[i - 1] == '均在' or lst[i - 1] == '在':
                                    #     if lst[i - 2] == '开始' and not citys_china[lst[i]]:
                                    #         citys_china[lst[i]] = lst[i - 3]
                                    #     elif not citys_china[lst[i]]:
                                    #         citys_china[lst[i]] = lst[i - 2]
                                    # elif lst[i] == '北京' and lst[i + 1] == '开始' and lst[i + 2] == '结束':
                                    #     citys_china[lst[i]] = lst[i + 3]
                                    # elif lst[i - 2] == '均在' and lst[i] != '北京' and lst[i] != '天津' and lst[i] != '上海' and lst[i] != '重庆' and not citys_china[lst[i]]:
                                    #     citys_china[lst[i]] = lst[i - 4]
                                    # elif not citys_china[lst[i]]:
                                        citys_china[lst[i]] = lst[i + 1]
                            # 删除空数据的字典
                            for key in list(citys_china.keys()):
                                if not citys_china.get(key):
                                    del citys_china[key]

                elif lst[index] == '境外输入病例':
                    if lst[index - 1] == '均为' and not foreign_today:
                        foreign_today = lst[index - 2]
                    if foreign_today == 0:
                        foreign_today = lst[index + 1]
                    if lst[index + 2] == '开始' or lst[index + 1] == '开始':
                        # # range(start, stop[, step])将进步值step调整为2,start值默认为0，stop值不能为空
                        for i in range(index + 2, len(lst)):
                            if lst[i] == '结束' and lst[i-1] != '开始':
                                break
                            # 将字典中的key与文本中的内容进行比对，如果相同则将值存入
                            elif lst[i] in provincials_foreign.keys() and not provincials_foreign[lst[i]]:
                                provincials_foreign[lst[i]] = lst[i + 1]
                        # 删除空数据的字典
                        for key in list(provincials_foreign.keys()):
                            if not provincials_foreign.get(key):
                                del provincials_foreign[key]

                elif lst[index] == '新增死亡病例':
                    if lst[index - 1] == '无':
                        deal_today = 0
                    elif deal_today == 0:
                        deal_today = lst[index + 1]

                elif lst[index] == '新增疑似病例':
                    if lst[index - 1] == '无':
                        probable_today = 0
                    elif probable_today == 0:
                        probable_today = lst[index + 1]

                elif lst[index] == '新增治愈出院病例':
                    if lst[index - 1] == '无':
                        heal_today = 0
                    elif heal_today == 0:
                        heal_today = lst[index + 1]

                elif lst[index] == '境外输入现有确诊病例':
                    if foreign_number_now == 0:
                        foreign_number_now = lst[index + 1]
                    for i in range(index, len(lst)):
                        if lst[i] == '死亡病例':
                            break
                        elif lst[i] == '累计确诊病例':
                            foreign_number_count = lst[i + 1]
                        elif lst[i] == '出院':
                            foreign_heal_count = lst[i + 1]

                elif lst[index] == '现有确诊病例':
                    if lst[index - 1] == '无':
                        china_number_now = 0
                    elif china_number_now == 0:
                        china_number_now = lst[index + 1]
                    for i in range(index, len(lst)):
                        if lst[i] == '句号':
                            break
                        elif lst[i] == '出院':
                            china_heal_count = lst[i + 1]
                        elif lst[i] == '死亡病例':
                            china_deal_count = lst[i + 1]
                        elif lst[i] == '累计报告确诊病例':
                            china_number_count = lst[i + 1]
                        elif lst[i] == '现有疑似病例':
                            if lst[i - 1] == '无':
                                china_probable_now = 0
                            else:
                                china_probable_now = lst[i + 1]

                elif lst[index] == '香港特别行政区':
                    if xiang_number == 0:
                        xiang_number = lst[index + 1]
                        xiang_heal = 0
                        xiang_deal = 0
                    if lst[index + 2] == '开始':  # 香港
                        for i in range(index, len(lst)):
                            if lst[i] == '结束':
                                break
                            elif lst[i] == '出院':
                                xiang_heal = lst[i + 1]
                            elif lst[i] == '死亡':
                                xiang_deal = lst[i + 1]

                elif lst[index] == '澳门特别行政区':
                    if ao_number == 0:
                        ao_number = lst[index + 1]
                        ao_heal = 0
                        ao_deal = 0
                    if lst[index + 2] == '开始':  # 澳门
                        for i in range(index, len(lst)):
                            if lst[i] == '结束':
                                break
                            elif lst[i] == '出院':
                                ao_heal = lst[i + 1]
                            elif lst[i] == '死亡':
                                ao_deal = lst[i + 1]

                elif lst[index] == '台湾地区':
                    if tai_number == 0:
                        tai_number = lst[index + 1]
                        tai_heal = 0
                        tai_deal = 0
                    if lst[index + 2] == '开始':  # 台湾
                        for i in range(index, len(lst)):
                            if lst[i] == '结束':
                                break
                            elif lst[i] == '出院':
                                tai_heal = lst[i + 1]
                            elif lst[i] == '死亡':
                                tai_deal = lst[i + 1]

            except IndexError:
                pass

        item['number_today'] = number_today
        item['foreign_today'] = foreign_today
        item['citys_today'] = citys_today
        item['deal_today'] = deal_today
        item['probable_today'] = probable_today
        item['heal_today'] = heal_today
        item['foreign_number_now'] = foreign_number_now
        item['foreign_number_count'] = foreign_number_count
        item['foreign_heal_count'] = foreign_heal_count
        item['china_number_count'] = china_number_count
        item['china_heal_count'] = china_heal_count
        item['china_deal_count'] = china_deal_count
        item['china_number_now'] = china_number_now
        item['china_probable_now'] = china_probable_now
        item['xiang_deal'] = xiang_deal
        item['xiang_heal'] = xiang_heal
        item['xiang_number'] = xiang_number
        item['ao_deal'] = ao_deal
        item['ao_heal'] = ao_heal
        item['ao_number'] = ao_number
        item['tai_deal'] = tai_deal
        item['tai_heal'] = tai_heal
        item['tai_number'] = tai_number
        item['provincials_foreign'] = provincials_foreign
        item['citys_china'] = citys_china


        yield item
