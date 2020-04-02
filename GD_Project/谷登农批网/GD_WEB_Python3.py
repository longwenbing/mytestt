import csv
import os
import datetime
import numpy
import requests
from lxml import etree

class GD_Python(object):
    def __init__(self):
        # 发起请求时使用的请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'Cookie': 'username=18174504650; pgv_pvi=4994044928; marketId=1; IESESSION=alive; pgv_si=s5746251776; Hm_lvt_171a81124f328875e7ce819aadac291e=1584490418,1584506940,1584507235,1584581420; Hm_lvt_e2dcda84fba5f34e3f6954d2990a58fa=1584490418,1584506940,1584507235,1584581420; gjsession=FE1167D98468FC6947CB5953D0E39D5F; Hm_lpvt_171a81124f328875e7ce819aadac291e=1584581429; Hm_lpvt_e2dcda84fba5f34e3f6954d2990a58fa=1584581429; SERVERID=df977beec67d4f2164dfac969c183b5f|1584581437|1584581423'
        }
        # 起始url
        self.begin_urls = ["https://www.gdeng.cn/baishazhou/market/112.html",
                           "https://www.gdeng.cn/yulin/market/433.html"]
        # 保存文件的路径
        self.local_market_paths = ['D:\CSDY_data\谷登农批网\武汉白沙洲批发市场', 'D:\CSDY_data\谷登农批网\广西玉林批发市场']
        # 主要栏目名称
        self.columns = ['禽蛋', '鸡蛋']
        # 保存的fieldnames
        self.fieldnames = ["商店名", "经营模式", "市场位置", "被浏览次数", "批发信息数量", "联系人", "电话", "手机", "电子邮箱", "地址", "邮编", "蛋种", "订货量",
                           "单价", "单位", "库存",
                           "累计查看次数", "图片"]

    # 用于统一处理请求
    def request(self, url):
        # 尝试三次
        for _ in range(3):
            try:
                from time import sleep
                # sleep(0.5)
                print("request %s" % url)
                r = requests.get(url, headers=self.headers, timeout=(5, 60))
                return r
            # 处理异常
            except requests.exceptions.ReadTimeout:
                print("timeout")
            except requests.exceptions.ConnectionError:
                print("connection error")
        return None

    # 总页数
    def page_hrefs(self):
        all_hrefs = []
        for url in self.begin_urls:
            xpath = self.get_xpath(url, '//*[@id="gduiPage_1"]/a/@href')
            for i in xpath:
                all_hrefs.append(i)
        return all_hrefs

    # 判断是否有禽蛋类并返回栏目
    # /html/body/div[4]/div/div[1]/div/div[7]/ul/li[1]/a
    # /html/body/div[4]/div/div[1]/div/div[4]/h5/a
    # /html/body/div[4]/div/div[1]/div/div
    # /html/body/div[4]/div/div[1]/div/div[1]/h5/a
    def egg_columns(self, url):
        colums = []
        clolumns_xpath = self.get_xpath(url, '/html/body/div[4]/div/div[1]/div/div')
        for c in clolumns_xpath:
            colums_name = c.xpath('h5/a/text()')[0]
            if colums_name in self.columns:
                colums.append(c.xpath('h5/a/@href'))
        return colums

    # 一页总产品/html/body/div[4]/div/div[2]/div[2]/div/div/div[1]/ul/li[1]/p[1]/a
    def shop_products(self, url):
        products = []
        i = 1
        flag = True
        while True:
            print(url + "dhohoho")
            request = self.request(url)
            etree_html = etree.HTML(request.text)
            # /html/body/div[4]/div/div[2]/div[2]/div/div/div[1]/ul/li/p[1]/a
            product_view = etree_html.xpath('/html/body/div[4]/div/div[2]/div[2]/div/div/div[1]/ul')
            if product_view == None or product_view == []:
                continue
            else:
                product_view = product_view[0]
                break
        product_columns = product_view.xpath('li')
        size = len(product_columns)
        if size == 1:
            # / html / body / div[4] / div / div[2] / div[2] / div / div / div[1] / ul / li / p[1] / a
            products.append(product_columns[0].xpath('p[1]/a/@href'))
            # print(products)
            flag = False
            return products
        while flag:
            product = product_view.xpath('li[%s]/p[1]/a/@href' % i)
            if product == None or product == []:
                continue
            else:
                products.append(product)
                i += 1
            if i == size:
                break
        return products

    def get_info(self, url, xpath):
        while True:
            info = url.xpath(xpath)
            if info == None or info == []:
                continue
            else:
                return info

    def get_message(self, url):
        info = []
        # 商品信息
        # shop_info=self.get_xpath(url,'/html/body/div[3]/div[6]/div[1]/div[1]')
        shopname = self.get_xpath(url, '/html/body/div[3]/div[6]/div[1]/div[1]/div[1]/h3/text()')[0].strip()
        management_model = self.get_xpath(url, '/html/body/div[3]/div[6]/div[1]/div[1]/div[1]/p[2]/text()')[0].strip()
        if management_model != None:
            management_model = management_model.split("：")[1]
        market_location = self.get_xpath(url, '/html/body/div[3]/div[6]/div[1]/div[1]/div[1]/p[3]/text()')[0].strip()
        if market_location != None:
            market_location = market_location.split("：")[1]
        view_time = self.get_xpath(url, '/html/body/div[3]/div[6]/div[1]/div[1]/div[2]/p[1]/text()')[0]
        if view_time != None:
            view_time = view_time.split("：")[1].strip()
        send_message_pice = self.get_xpath(url, '/html/body/div[3]/div[6]/div[1]/div[1]/div[2]/p[2]/text()')[0].strip()
        if send_message_pice != None:
            send_message_pice = send_message_pice.split("：")[1]
        info.append(shopname)
        info.append(management_model)
        info.append(market_location)
        info.append(view_time)
        info.append(send_message_pice)
        # 联系信息方式
        # ['闻鸡起舞', '个人经营', '武汉白沙洲批发市场', '25913', ['批发信息数量', '3条'], '联 系 人：刘炎林', '电 话：', '',
        # '电子邮箱：', '地 址：湖北省襄阳市南漳县巡检镇', '邮 编：', '土鸡蛋', '≥1', '150.00', '60', '4820', 'https://img.gdeng.cn/2017/4/6/3b2cade69de346dfaa28a0b2d6aba134370_370.jpg']
        # contact_info = etree_html.xpath('//*[@id="leftTit-2"]/div/text()')
        boss_name = self.get_xpath(url, '/html/body/div[3]/div[6]/div[1]/div[2]/div/p[1]/text()')[0]
        if boss_name != None:
            try:
                boss_name = boss_name.split("：")[1].strip()
            except:
                boss_name = ''
        landline = self.get_xpath(url, '/html/body/div[3]/div[6]/div[1]/div[2]/div/p[2]/text()')[0]
        if landline != None:
            try:
                landline = landline.split("：")[1].strip()
            except:
                landline = ''
        phone_number = \
            self.get_xpath(url, '/html/body/div[3]/div[6]/div[1]/div[2]/div/p[3]/span/text()')[
                0]
        email = self.get_xpath(url, '/html/body/div[3]/div[6]/div[1]/div[2]/div/p[4]/text()')[0]
        try:
            email = email.split("：")[1].strip()
        except:
            email = ''
        address = self.get_xpath(url, '/html/body/div[3]/div[6]/div[1]/div[2]/div/p[5]/text()')[0]
        try:
            address = address.split("：")[1].strip()
        except:
            address = ''
        zip_code = self.get_xpath(url, '/html/body/div[3]/div[6]/div[1]/div[2]/div/p[6]/text()')[0]
        try:
            zip_code = zip_code.split("：")[1].strip()
        except:
            zip_code = ''
        # print(phone_number)
        # print(boss_name)
        info.append(boss_name)
        info.append(landline)
        info.append(phone_number.strip())
        info.append(email)
        info.append(address)
        info.append(zip_code)
        # 产品信息
        # product_info=etree_html.xpath('/html/body/div[3]/div[6]/div[3]/div[1]/div/text()')[0]
        product_name = self.get_xpath(url, '/html/body/div[3]/div[6]/div[3]/div[1]/div/div[2]/h3/text()')[0].strip()
        base_order_amount = \
            self.get_xpath(url, '/html/body/div[3]/div[6]/div[3]/div[1]/div/div[2]/ul/li[2]/span[1]/text()')[0].strip()
        unit_price = \
            self.get_xpath(url, '/html/body/div[3]/div[6]/div[3]/div[1]/div/div[2]/ul/li[2]/span[2]/text()')[0].strip()
        unit = self.get_xpath(url, '/html/body/div[3]/div[6]/div[3]/div[1]/div/div[2]/ul/li[2]/text()')[0].strip()
        stock = \
            self.get_xpath(url, '/html/body/div[3]/div[6]/div[3]/div[1]/div/div[2]/div/ul/li[1]/span/text()')[
                0].strip()
        commodity_heat = \
            self.get_xpath(url, '/html/body/div[3]/div[6]/div[3]/div[1]/div/div[2]/div/ul/li[2]/span/text()')[
                0].strip()
        product_picture = self.get_xpath(url, '/html/body/div[3]/div[6]/div[3]/div[1]/div/div[1]/div[1]/img/@src')[
            0].strip()
        # print(product_name)
        # print(unit_price)
        info.append(product_name)
        info.append(base_order_amount)
        info.append(unit_price)
        info.append(unit)
        info.append(stock)
        info.append(commodity_heat)
        info.append(product_picture)
        return info

    def get_xpath(self, url, xpath):
        while True:
            request = self.request(url)
            etree_html = etree.HTML(request.text)
            html_xpath = etree_html.xpath(xpath)
            if html_xpath == None or html_xpath == []:
                continue
            else:
                return html_xpath

    # 保存结果到csv文件
    def storage_infos(self):
        self.check_dir()
        now_time = datetime.datetime.now().strftime('%Y-%m-%d')
        baishazhou = []
        # 信息数
        b = 0
        y = 0
        yulin = []
        typ = True
        for market in self.begin_urls:
            o = 1
            for page in self.page_hrefs():
                if o == 1 and typ:
                    page = 'https://www.gdeng.cn/baishazhou/market/112.html'
                elif o == 1 and typ == False:
                    page = 'https://www.gdeng.cn/yulin/market/433.html'
                print(page)
                for i in self.shop_products(page):
                    message = self.get_message(i[0])

                    ##保存数据：['闻鸡起舞', '个人经营', '武汉白沙洲批发市场', '25977', '3条', '刘炎林', '', '13823759728', '',
                    # '湖北省襄阳市南漳县巡检镇', '', '土鸡蛋', '≥1', '150.00', '', '60', '4858',
                    # 'https://img.gdeng.cn/2017/4/6/3b2cade69de346dfaa28a0b2d6aba134370_370.jpg']

                    if typ == True:
                        baishazhou.append(message)
                        b += 1
                    else:
                        yulin.append(message)
                        y += 1
                    print(message)
                    o += 1
            typ = False
        with open(self.local_market_paths[0] + '\%s.csv' % now_time, 'w',newline = '') as f1:
            writer1 = csv.writer(f1)
            writer1.writerow(self.fieldnames)

            reshape1 = numpy.array(baishazhou).reshape(b, 18)
            writer1.writerows(reshape1)
            f1.close()
            print(self.local_market_paths[0] + '\%s.csv' % now_time + "  文件录入完成")
        with open(self.local_market_paths[1] + '\%s.csv' % now_time, 'w',newline = '') as f2:
            writer2 = csv.writer(f2)
            writer2.writerow(self.fieldnames)
            reshape2 = numpy.array(yulin).reshape(y , 18)
            writer2.writerows(reshape2)
            f2.close()
            print(self.local_market_paths[1] + '\%s.csv' % now_time + "  文件录入完成")

    def check_dir(self):
        for path in self.local_market_paths:
            if not os.path.exists(path):
                os.makedirs(path)

    def run(self):
        start=datetime.datetime.now()
        self.storage_infos()
        endt=datetime.datetime.now()
        print("总时间：")
        print(endt-start)

if __name__ == '__main__':
    a = GD_Python()
    a.run()
