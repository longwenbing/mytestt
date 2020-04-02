import csv
import os
import time
import datetime

import numpy
import requests
from lxml import etree
import re
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


class ZC_py():
    def __init__(self):
        # 发起请求时使用的请求头
        self.headers = {
            # "code": 100, "left_ip": 20, "left_time": 86507, "number": 1, "domain": "183.129.244.16","port": [27001],
                        'Cookie': 'guid=d75c9fec-4408-f994-b649-8a11c1454312; UM_distinctid=170e8140d95e5-0947631014181f-b363e65-144000-170e8140d964aa; BAIDU_SSP_lcr=https://www.sogou.com/link?url=DSOYnZeCC_qa5NmuItVaPADydjxbYhws; Hm_lvt_44c27e8e603ca3b625b6b1e9c35d712d=1584441541,1584930416,1584938829,1585009518; isCloseOrderZHLayer=0; route=5381fa73df88cce076c9e01d13c9b378; ASP.NET_SessionId=qji2hiaho3sl1smjcm33wqwu; STATReferrerIndexId=1; Hm_lvt_8dcae0723b4b41ad3a4f6bedfbe3d37d=1584930506,1584930950,1584952176,1585009532; Hm_lpvt_44c27e8e603ca3b625b6b1e9c35d712d=1585026979; CNZZDATA1262038091=540191500-1584436592-%7C1585026929; STATcUrl=; Hm_lpvt_8dcae0723b4b41ad3a4f6bedfbe3d37d=1585027402',
                        }
        self.proxies={'http':'183.129.244.16:27001','https':'183.129.244.16:27001'}

        # 起始url
        self.beginurl = 'https://cm.sci99.com/channel/eggschil/'
        self.the_official_website = 'https://cm.sci99.com/'
        self.china_provinces = ['https://cm.sci99.com/news/2928_2942-0-0-6_7_8-0-1-B7DBBFC720BAD6BFC7BCA6B5B0.html',
                                'https://cm.sci99.com/news/2928_2942-0-0-9_10_15_13_12_11-0-1-B7DBBFC720BAD6BFC7BCA6B5B0.html',
                                'https://cm.sci99.com/news/2928_2942-0-0-2_35_3_4-0-1-B7DBBFC720BAD6BFC7BCA6B5B0.html',
                                'https://cm.sci99.com/news/2928_2942-0-0-23_25_24_20_22-0-1-B7DBBFC720BAD6BFC7BCA6B5B0.html',
                                'https://cm.sci99.com/news/2928_2942-0-0-16_17_18_14_19-0-1-B7DBBFC720BAD6BFC7BCA6B5B0.html',
                                'https://cm.sci99.com/news/2928_2942-0-0-27_5_28_30_31-0-1-B7DBBFC720BAD6BFC7BCA6B5B0.html']
        self.prefs = {
            'profile.default_content_setting_values': {
                'images': 2,
                'javascript': 2  # 2即为禁用的意思
            }
        }

        # 鸡蛋种类
        self.egg_species = ['褐壳鸡蛋', '粉蛋']
        # 保存文件路径
        self.save_path = '卓创咨询'
        # 保存的fieldnames
        self.fieldnames = ['公司', '经营地区', '联系人', '电话', '固话', '入驻团膳/年', '承包食堂', '团膳等级', 'ISO22000', 'ISO9001', '中央厨房',
                           '投保', '上市公司', '公司官网']
        self.result = []
        # 驱动
        self.driver_chrome = r'C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver'

    # 用于统一处理请求
    def request(self, url):
        # 尝试三次
        for _ in range(3):
            try:
                from time import sleep
                # sleep(0.5)
                print("request %s" % url)
                r = requests.get(url, headers=self.headers, timeout=(30, 60))
                return r
            # 处理异常
            except requests.exceptions.ReadTimeout:
                print("timeout")
            except requests.exceptions.ConnectionError:
                print("connection error")
        return None

    # def login(self):
    #
    #     driver = webdriver.Chrome(r'C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver')
    #     driver.get('https://cm.sci99.com/include/login.aspx?RequestId=53f8f13ecddf2852')
    #     time.sleep(3)
    #     driver.find_element_by_xpath('//*[@id="chemname"]').send_keys('18174504650')
    #     time.sleep(0.2)
    #     driver.find_element_by_xpath('//*[@id="chempwd"]').send_keys('123456')
    #     submmit=driver.find_element_by_xpath('//*[@id="frm_login"]/div[3]/div[2]/ul/li[3]/input')
    #     options = webdriver.ChromeOptions()
    #     options.add_experimental_option('prefs', self.prefs)
    #     submmit.click(driver)
    #     cookie = driver.get_cookie()
    #     print('宝贝')
    #     driver.close()
    #     driver.quit()
    #     return cookie

    def get_xpath(self, url, xpath):
        request = self.request(url)
        html = etree.HTML(request.content)
        html_xpath = html.xpath(xpath)
        return html_xpath

    def get_columns(self, url):
        etree_htmls = self.get_xpath(url, '/html/body/form/div[7]/div[1]/div[2]/div/ul/li')
        while etree_htmls != None or etree_htmls != []:
            etree_htmls = self.get_xpath(url, '/html/body/form/div[7]/div[1]/div[2]/div/ul/li')
        return etree_htmls

    # 获取message 方式
    def get_message(self, etree_html, xp):
        xpath = etree_html.xpath(xp)
        return xpath

    def run(self):
        requests1 = requests.get('https://cm.sci99.com/news/2928_2942-0-0-6_7_8-0-1-B7DBBFC720BAD6BFC7BCA6B5B0.html',
                                 self.headers, timeout=(30, 60))
        # print(requests1)
        time.sleep(5)
        html = etree.HTML(requests1.text)
        hrefs = self.get_message(html,'/html/body/form/div[7]/div[1]/div[2]/div/ul/li/a/@href')
        print(hrefs)
        # print(html)


if __name__ == '__main__':
    a = ZC_py()
    a.run()
