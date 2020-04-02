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


class TS_python(object):
    def __init__(self):
        # 发起请求时使用的请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'Cookie': '__cfduid=df54098c4946c3b915c5999d4fed3a5841584329114; ASPSESSIONIDQCCTQTQQ=DHFKPLDBBMKPDFIGFFLPNACJ; ASPSESSIONIDSABTQSQR=GKGKGGNAFDELOACNLEKJPNJB; Hm_lvt_a3a2d3af6a33805cae54b13133559a7d=1584329122,1584582966,1584587333; u%5Fn=18174504650; p%5Fud=XXSCC214; Hm_lpvt_a3a2d3af6a33805cae54b13133559a7d=1584590042'
        }
        # 起始url
        self.beginurl = 'https://www.tansent.com/tscom/?page=1&cid=0&rz=&kw='

        self.website='https://www.tansent.com/tscom/?page=%d&cid=0&rz=&kw='
        self.gw='https://www.tansent.com/tscom'

        #保存文件路径
        self.save_path='团膳网公司一览'
        # 保存的fieldnames
        self.fieldnames =['公司','经营地区','联系人','电话','固话','入驻团膳/年','承包食堂','团膳等级','ISO22000','ISO9001','中央厨房','投保','上市公司','公司官网']
        self.result=[]

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

    def get_xpath(self, url, xpath):
        request = self.request(url)
        html = etree.HTML(request.content)
        html_xpath = html.xpath(xpath)
        return html_xpath

    # 总页数
    #xpath=/html/body/table/tbody/tr/td/a[12]
    def get_all_page_number(self):
        a=self.get_xpath(self.beginurl,'/html/body/table/tbody/tr/td/a/@href')
        last_page_url = a[len(a) - 1]
        #匹配 到最大页面数
        number = int(re.match(r'\?page=([0-9]*)&.*', last_page_url,re.M|re.I).group(1))
        return number
    #获取每个公司框架文本
    def get_one_page_columns(self,url):
        etree_htmls=self.get_xpath(url,'//*[@id="s_list"]/div')
        return etree_htmls

    #获取message 方式
    def get_message(self,etree_html,xp):
        xpath = etree_html.xpath(xp)
        return xpath

    #判断数据是否为空 空则返回0
    def check_message(self,mes):
        if mes==None or mes==[]:
            return '0'
        else:
            return mes[0]

    #判断标签名
    def check_flag(self,flag):
        a = 'c' in flag
        if a:
            return '否'
        else:
            return '是'

    #一页中的公司数//*[@id="s_list"]/div
    # 获取每个公司的信息
    def get_company_message(self,url,etree_html,i):
        #self.get_message(etree_html, 'div[2]/div[1]/div[1]/div[1]/a/text()')[0] 这样会乱码
        cname = self.check_message(self.get_message(etree_html, 'div[2]/div[1]/div[1]/div[1]/a/text()'))
        company_official_website=self.check_message(self.get_message(etree_html,'div[2]/div[1]/div[1]/div[1]/a/@href'))
        if 'http' not in company_official_website:
            company_official_website=self.gw+company_official_website
        # landline=''
        # phone=''
        operating_areas=self.check_message( self.get_message(etree_html,'div[2]/div[1]/div[2]/div[1]/div[2]/text()')).split("：")[1]
        access_time=self.check_message( self.get_message(etree_html,'div[2]/div[1]/div[1]/div[3]/span/text()'))
        contracted_canteen=self.check_message(self.get_message(etree_html,'div[2]/div[1]/div[1]/div[4]/font/b/text()'))
        if contracted_canteen=='*':
            contracted_canteen='保密'
        level=self.check_message(self.get_message(etree_html,'div[2]/div[2]/div/div[1]/text()'))
        level_label=self.check_message(self.get_message(etree_html,'div[2]/div[2]/div/div[2]/img/@src'))
        level_flag=self.check_flag(level_label)
        if 'c' in level_label and level_label=='团膳专家':
            level_label="无"
        attestation_flag1=self.check_flag(self.check_message(self.get_message(etree_html,'div[2]/div[2]/div/div[4]/img/@src')))
        attestation_flag2 = self.check_flag(self.check_message(self.get_message(etree_html,'div[2]/div[2]/div/div[6]/img/@src')))
        central_kitchen_flag = self.check_flag(self.check_message(self.get_message(etree_html,'div[2]/div[2]/div/div[8]/img/@src')))
        effect_insurance_flag = self.check_flag(self.check_message(self.get_message(etree_html,'div[2]/div[2]/div/div[10]/img/@src')))
        quoted_company_flag = self.check_flag(self.check_message(self.get_message(etree_html,'div[2]/div[2]/div/div[12]/img/@src')))
        contacts_info=self.selenium_get_message(url,i)
        contacts_name=contacts_info[0]
        phone=contacts_info[1]
        landline=contacts_info[2]
        return (cname,operating_areas,contacts_name,phone,landline,access_time,contracted_canteen,level,attestation_flag1,attestation_flag2,central_kitchen_flag,effect_insurance_flag,quoted_company_flag,company_official_website)

    #查询点击内容
    def selenium_get_message(self,url,i):
        list=[]
        driver = webdriver.Chrome(r'C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver')
        try:
            driver.get(url)
            # # 超时时间为30秒，每0.2秒检查1次，直到xpath的元素出现
            button = WebDriverWait(driver,30,0.2).until(lambda x:x.find_element_by_xpath('/html/body/div[6]/div[1]/div[%d]'%i+'/div[2]/div[1]/div[2]/div[1]/div[1]'))
            button.click()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(0.5)
            text = WebDriverWait(driver, 30, 0.2).until(lambda x: x.find_element_by_xpath('/html/body/div[6]/div[1]/div[%d]'%i+'/div[2]/div[1]/div[2]/div[1]/div[1]')).text
            messages = text.split("：")[1]
            contacts=messages.split(" ",1)
            name=''
            phone=''
            landline=''
            if len(contacts)>1:
                pattern1 = re.compile(r'0?[13|14|15|18|17][0-9]{10}')
                pattern2 = re.compile(r'0?\d{2,4}-?\d{7,8}')
                contact1=pattern1.findall(contacts[1])
                contact2=pattern2.findall(contacts[1])
                if contact1:
                    phone=contact1[0]
                    if len(contact1)>1:
                        for i in contact1:
                            phone=phone+'、'+i
                if contact2:
                    landline=contact2[0]
                    if len(contact2)>1:
                        for i in contact2:
                            landline=landline+'、'+i
                name=contacts[0]
            else:
                name=messages
            list.append(name)
            list.append(phone)
            list.append(landline)
            driver.close()  # 关闭页面
            driver.quit()  # 关闭整个浏览器
        except:
            print('重新获取')
            list=self.selenium_get_message(url,i)
        return list
    #保存数据
    def storage_infos(self):
        self.check_dir()
        end=self.get_all_page_number() + 1
        # for i in range(5,6): 23
        for i in range(1,end):
            url = self.website%i
            columns = self.get_one_page_columns(url)
            c_id=1
            start = datetime.datetime.now()
            for column in  columns:
                message=self.get_company_message(url,column,c_id)
                c_id+=1
                self.result.append(message)
                print(message)
            #五页保存一次
            if i%5 ==0 and i>=5 or i==self.get_all_page_number():
                with open(self.save_path + '/' + self.save_path + '.csv', 'a', newline='') as file:
                    writer1 = csv.writer(file)
                    reshape1 = numpy.array(self.result)
                    writer1.writerows(reshape1)
                    file.close()
                    self.result.clear()
                    print(self.save_path + "  文件录入完成")
            end = datetime.datetime.now()
            print(end - start)

    #检查文件是否存在
    def check_dir(self):
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
            with open(self.save_path + '/' + self.save_path + '.csv', 'w', newline='') as file:
                writer1 = csv.writer(file)
                writer1.writerow(self.fieldnames)
                file.close()
    #主程序
    def run(self):

        self.storage_infos()
if __name__ == '__main__':
    a = TS_python()
    a.run()