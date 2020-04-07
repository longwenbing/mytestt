import csv
import os
import time
from datetime import datetime

import numpy as np
import requests
from lxml import etree
import re

from merge_data import save_csv


class mycollector():
    def __init__(self):
        # 发起请求时使用的请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
        }
        # 全国蛋价早报
        self.beginurl = 'http://bbs.eggworld.cn/forum-36-1.html'
        # 蛋E网的官网
        self.website = 'http://bbs.eggworld.cn/'

        self.page = 'http://bbs.eggworld.cn/forum-36-%d.html'

        self.save_path = 'D://CSDY_data//蛋e网蛋价'

        self.fieldnames = ['城市', '蛋种', '销售方式', '价格/元', '单位/斤', '趋势', '其他信息']
        # 一页中的省份名
        self.provinces = []
        # 一页中的信息集合
        self.content = []
        self.c = 0
        self.columns_number = []

    # 用于统一处理请求
    def request(self, url):
        # 尝试三次
        for _ in range(3):
            try:
                from time import sleep
                # sleep(0.5)
                print("request %s" % url)
                r = requests.get(url, headers=self.headers, timeout=(30, 60))
                # 方便调试
                time.sleep(5)
                return r
            # 处理异常
            except requests.exceptions.ReadTimeout:
                print("timeout")
            except requests.exceptions.ConnectionError:
                print("connection error")
        return None

    # 获取需要html的位置元素
    def get_xpath(self, url, xpath):
        i = 1
        try:
            request = self.request(url)
        except:
            i += 1
            print('重试')
            if i == 3:
                print("找不到 %s 的 %s"%(url,xpath))
                exit(0)
            request = self.request(url)
        html = etree.HTML(request.content)
        html_xpath = html.xpath(xpath)
        return html_xpath

    # 获取所需栏目的html
    def get_columns(self, url):
        etree_htmls = self.get_xpath(url, '/html/body/div[6]/div[1]/div[4]/div/div/div[4]/div[2]/form/table/tbody')
        return etree_htmls

    def handling_content(self, url, release_time):
        texts = self.get_xpath(url, '//*[@class="t_f"]/text()')
        # print(texts)
        # 处理文章内容
        first_in = True
        shandong_4_6flag=True
        for t in texts:
            text = t.strip()
            if text == '' or text == None:
                pass
            else:
                # print(text)
                # print('')
                if '【' in t:
                    province = re.findall(r'【(.*?)】', text)[0]
                    # if release_time == '2020-2-21' and province == '湖北':
                    #     pass
                    # else:
                    #     self.provinces.append(province)
                    if release_time=='2020-4-6' and province=='山东' and shandong_4_6flag:
                        shandong_4_6flag=False
                    else:
                        #将每个省份写入列表
                        self.provinces.append(province)
                    if first_in or self.c == 0:
                        first_in = False
                    else:
                        #记录省份下的数据条数
                        self.columns_number.append(self.c)
                        self.c = 0
                else:
                    #切分每条数据
                    message = self.split_content(text)
                    if message != None:
                        print(message)
                        # 将切分后的数据写入列表
                        self.content.append(message)
                        self.c += 1
        self.columns_number.append(self.c)
        self.c = 0
        # print(self.provinces.zip(self.columns_number),self.content)
        for i in range(len(self.provinces)):
            crruent_province = self.provinces[i]
            print(crruent_province)
            number = self.columns_number[i]
            # print(self.provinces)
            # print(self.columns_number)
            offest = 0
            for x in range(i):
                offest += int(self.columns_number[x])
            self.storage_infos(crruent_province, self.content, release_time, offest, number, release_time)
            time.sleep(0.3)
        self.content = []
        self.provinces = []
        self.columns_number = []
        time.sleep(0.3)

    # 分割消息，并保存
    def split_content(self, text):
        # print(text)
        egg_types = ['红蛋', '粉蛋', '褐壳蛋']
        split_fields = ['蛋价', '价']
        egg_type = ''
        field = ''
        wrong_data_flag = False
        for t in egg_types:
            if t in text:
                egg_type = t
                break
        for f in split_fields:
            if f in text:
                field = f
                break
        if egg_type == '' or field == '':
            wrong_data_flag = True
        if wrong_data_flag == True:
            return None
        area = text.split(egg_type)[0]
        # print(area,egg_type,field)
        sale_mode = re.findall(r'%s(.*?)%s' % (egg_type, field), text)
        if sale_mode != []:
            sale_mode = re.findall(r'%s(.*?)%s' % (egg_type, field), text)[0]
        else:
            print('salemode 空', text)
            return None
        price = ''
        price_temp = re.findall(r'%s(.*?)元' % sale_mode, text)
        if price_temp != []:
            price = re.findall(r'%s(.*?)元' % field, text)[0]

        unit = self.get_jin(text)
        # [\u4E00-\u9FA5] 中文
        trend = '稳'
        trend_temp = re.findall(r'斤([\u4E00-\u9FA5]{1})', text)
        if trend_temp == None or trend_temp == []:
            trend = re.findall(r'元([\u4E00-\u9FA5]{1})', text)
            if trend != []:
                trend = re.findall(r'元([\u4E00-\u9FA5]{1})', text)[0]
            else:
                print('无趋向', text)
                return None
        else:
            trend = trend_temp[0]
        text_new = text.replace('(', '（').replace(')', '）')
        extra = re.findall(r'.*?（(.*?)）', text_new)
        if extra == None or extra == []:
            extra = ''
        else:
            extra = extra[0]
        return area, egg_type, sale_mode, price, unit, trend, extra

    def get_jin(self, text):
        unit = '1'
        case1 = re.findall(r'元(.*?)斤', text)
        case2 = re.findall(r'元(\d+)', text)
        case3 = re.findall(r'(\d+)斤', text)
        case = []
        if case1 != []:
            if u'\u4e00' <= case1[0] <= u'\u9fff':
                case.append([''])
            else:
                case.append(case1[0])
        if case2 != []:
            case.append(case2[0])
        if case3 != []:
            case.append(case3[0])
        if case == []:
            1
        else:
            max = case[0]
            for b in case:
                if len(b) > len(max):
                    max = b
            unit = max
        return unit

    # 保存数据
    def storage_infos(self, provice, content, t, offset, number, release_time):
        from merge_data import data2mysql
        self.check_dir(provice, t)
        list = []
        for i in range(offset, offset + number):
            list.append(content[i])
        print(list)
        #保存本地csv
        with open(self.save_path + '/' + provice + '/' + '%s.csv' % t, 'w', newline='') as file:
            writer1 = csv.writer(file)
            writer1.writerows(list)
            file.close()
            print(self.save_path + '/' + provice + '%s.csv' % t + " 文件录入完成")
        mysql_data=[]
        for l in list:
            array = np.array(l)
            tolist = array.tolist()
            tolist.insert(0, provice)
            tolist.append(release_time)
            np_array = np.array(tolist)
            mysql_data.append(np_array)
        print(mysql_data)
        if mysql_data==[]:
            pass
        else:
            #保存数据库
            data2mysql(mysql_data)
            #保存本地csv
            save_csv(provice,mysql_data)



    # 检查文件是否存在
    def check_dir(self, provice, t):
        path = self.save_path + '/' + provice
        if not os.path.exists(path):
            os.makedirs(path)
        file = self.save_path + '/' + provice + '/' + '%s.csv' % t
        if not os.path.exists(file):
            with open(self.save_path + '/' + provice + '/' + '%s.csv' % t, 'w', newline='') as file:
                writer1 = csv.writer(file)
                writer1.writerow(self.fieldnames)
                file.close()
        # 获取message方式

    def get_message(self, etree_html, xp):
        xpath = etree_html.xpath(xp)
        return xpath

    def check_message(self, mes):
        if mes == None or mes == []:
            return '0'
        else:
            return mes[0]

    def get_new_tuples(self, day):
        #02-02
        new_columns = self.get_columns(self.beginurl)
        hrefs = []
        release_times = []
        for new_column in new_columns:
            # tr/td[4]/em/a/span
            href = self.website + self.check_message(self.get_message(new_column, 'tr/th/a[2]/@href'))
            title = self.check_message(self.get_message(new_column, 'tr/th/a[2]/text()'))
            # /html/body/div[6]/div[1]/div[4]/div/div/div[4]/div[2]/form/table/tbody[1]/tr/td[2]/em/span/span
            release_time_temp = self.check_message(self.get_message(new_column, 'tr/td[2]/em/span/span/@title'))
            release_time=release_time_temp
            if '-'in release_time_temp:
                split = release_time_temp.split('-')
                year =split[0]
                m=split[1]
                d=split[2]
                if len(m)==1:
                    m='0'+m
                if len(d)==1:
                    d='0'+d
                release_time=year+'-'+m+'-'+d
            print(release_time)
            try:
                print(release_time, day)
                # exit(0)
                if day <= release_time:
                    if '全国' in title:
                        hrefs.append(href)
                        release_times.append(day)
            except:
                pass
        return list(zip(hrefs, release_times))

    def run(self):
        today = time.strftime('%Y-%m-%d')
        tuple_list = self.get_new_tuples(today)
        print(tuple_list)
        for tuple in tuple_list:
            self.handling_content(tuple[0], tuple[1])


if __name__ == '__main__':
    a = mycollector()
    a.run()
