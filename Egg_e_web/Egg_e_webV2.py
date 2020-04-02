import csv
import os
import time
import requests
from lxml import etree
import re


class Egg_ewebV2():
    def __init__(self):
        # 发起请求时使用的请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        }
        #全国蛋价早报
        self.beginurl='http://bbs.eggworld.cn/forum-36-1.html'
        #蛋E网的官网
        self.website='http://bbs.eggworld.cn/'

        self.page='http://bbs.eggworld.cn/forum-36-%d.html'

        self.save_path='D://CSDY_data//蛋e网蛋价'

        self.fieldnames=['城市','蛋种','销售方式','价格/元','单位/斤','趋势','其他信息']
        #一页中的省份名
        self.provinces=[]
        #一页中的信息集合
        self.content=[]

        self.c=0
        self.columns_number=[]


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
    #获取需要html的位置元素
    def get_xpath(self, url, xpath):
        i=1
        try:
            request = self.request(url)
        except:
            i+=1
            print('重试')
            if i==3:
                exit(0)
            request=self.request()
        html = etree.HTML(request.content)
        html_xpath = html.xpath(xpath)
        return html_xpath

    #获取所需栏目的html
    def get_columns(self, url):
        etree_htmls = self.get_xpath(url, '/html/body/div[6]/div[1]/div[4]/div/div/div[4]/div[2]/form/table/tbody')
        return etree_htmls

    # 获取message方式
    def get_message(self, etree_html, xp):
        xpath = etree_html.xpath(xp)
        return xpath

    # 获取最大页面数
    def get_max_page(self):
        a = self.get_xpath(self.beginurl, '//*[@id="fd_page_bottom"]/div/a[10]/@href')
        last_page_url = a[len(a) - 1]
        number = int (re.match(r'.*?-([0-9]*).html', last_page_url, re.M | re.I).group(1))
        # print(number)
        return number

    #判断数据是否为空 空则返回0
    def check_message(self,mes):
        if mes==None or mes==[]:
            return '0'
        else:
            return mes[0]

    def title_split(self,str):
        try:
            temp=str.split('日')[1]
            if '蛋'in temp:
                area=temp.split('蛋')[0]
                return area
            else:
                return temp
        except:
            return str
    #获取文本内容/html/body/div[6]/div[1]/div[4]/div[2]/div[1]/table/tbody/tr[1]/td[2]/div[2]/div/div[1]/table/tbody/tr/td
    def handling_content(self,url,release_time):
        texts = self.get_xpath(url,'//*[@class="t_f"]/text()')
        # print(texts)
        # 处理文章内容
        first_in=True
        #2020-9-18 河北出错
        for t in texts:
            text=t.strip()
            if text=='' or text==None:
                pass
            else:
                # print(text)
                # print('')
                if '【' in t :
                    try:
                        province = re.findall(r'【([\u4e00-\u9fa5]+)', text)[0]
                    except:
                        province=re.findall(r'([\u4e00-\u9fa5]+)】', text)[0]
                    if province=='停收':
                        pass
                    else:
                        if (release_time == '2020-2-21' and province == '湖北') :
                            pass
                        else:
                            self.provinces.append(province)
                        if first_in or self.c == 0:
                            first_in=False
                        else:
                            self.columns_number.append(self.c)
                            self.c = 0
                else:
                    message = self.split_content(text)
                    if message != None:
                        print(message)
                        self.content.append(message)
                        self.c += 1
        self.columns_number.append(self.c)
        self.c=0
        if release_time=='2019-9-18':
            self.provinces.pop()
        for i in range(len(self.provinces)):
            crruent_province = self.provinces[i]
            print(crruent_province)
            number=self.columns_number[i]
            # print(self.provinces)
            # print(self.columns_number)
            offest=0
            # print(self.provinces)
            # print(self.columns_number)
            for x in range(i):
                offest+=int(self.columns_number[x])
            self.storage_infos(crruent_province,self.content,release_time,offest,number)
            time.sleep(0.3)
        self.content=[]
        self.provinces=[]
        self.columns_number=[]
        time.sleep(0.3)
        return self.provinces,self.content
    #分割消息，并保存
    #['北京', '上海', '山东', '河北', '辽宁', '吉林', '黑龙江', '江苏', '河南', '湖南', '重庆', '四川', '湖北', '辽宁', '吉林', '黑龙江', '湖北', '陕西', '江西', '山西', '广东', '河北', '河北']
#    [5,        3,      33,     10,     17,     7,      6,   12,     16,        10,  3,     2,      5,      10,        7,   4,      6,      6,      6,      6,       6,     6]
    def split_content(self,text):
        # print(text)
        egg_types=['红蛋','粉蛋','褐壳蛋']
        split_fields=['蛋价','价']
        egg_type=''
        field=''
        wrong_data_flag=False
        for t in egg_types:
            if t in text:
                egg_type=t
                break
        for f in split_fields:
            if f in text:
                field=f
                break
        if egg_type==''or field=='':
            wrong_data_flag=True
        if wrong_data_flag==True:
            return None
        area = text.split(egg_type)[0]
        # print(area,egg_type,field)
        sale_mode=re.findall(r'%s(.*?)%s'%(egg_type,field),text)
        if sale_mode!=[]:
            sale_mode=re.findall(r'%s(.*?)%s'%(egg_type,field),text)[0]
        else:
            print('salemode 空',text)
            return None
        price=''
        price_temp = re.findall(r'%s(.*?)元'%sale_mode , text)
        if price_temp!=[]:
            price=re.findall(r'%s(.*?)元'%field,text)[0]

        unit=self.get_jin(text)
        # [\u4E00-\u9FA5] 中文
        trend='稳'
        trend_temp = re.findall(r'斤([\u4E00-\u9FA5]{1})',text)
        if trend_temp ==None or trend_temp==[]:
            trend = re.findall(r'元([\u4E00-\u9FA5]{1})', text)
            if trend!=[]:
                trend= re.findall(r'元([\u4E00-\u9FA5]{1})', text)[0]
            else:
                print('无趋向',text)
                return None
        else:
            trend=trend_temp[0]
        text_new=text.replace('(','（').replace(')','）')
        extra=re.findall(r'.*?（(.*?)）',text_new)
        if extra==None or extra==[]:
            extra=''
        else:
            extra=extra[0]
        return area,egg_type,sale_mode,price,unit,trend,extra

    def get_jin(self,text):
        unit='1'
        case1=re.findall(r'元(.*?)斤',text)
        case2=re.findall(r'元(\d+)',text)
        case3 = re.findall(r'(\d+)斤', text)
        case=[]
        if case1!=[]:
            case.append(case1[0])
        if case2 != []:
            case.append(case2[0])
        if case3 != []:
            case.append(case3[0])
        if case==[]:
            1
        else:
            max = case[0]
            for b in case:
                if len(b)>len(max):
                    max=b
            unit=max
        return unit

    # 保存数据
    def storage_infos(self,provice,content,t,offset,number):
        self.check_dir(provice,t)
        list=[]
        for i in range(offset,offset+number):
            list.append(content[i])
        with open(self.save_path + '/' + provice +'/'+ '%s.csv'%t, 'a', newline='') as file:
            writer1 = csv.writer(file)
            writer1.writerows(list)
            file.close()
            print(self.save_path + '/' + provice + '%s.csv'%t+ " 文件录入完成")

    # 检查文件是否存在
    def check_dir(self,provice,t):
        path =self.save_path+'/'+provice
        if not os.path.exists(path):
            os.makedirs(path)
        file =self.save_path + '/' + provice +'/'+ '%s.csv'%t
        if not os.path.exists(file):
            with open(self.save_path + '/' + provice +'/'+ '%s.csv'%t, 'w', newline='') as file:
                writer1 = csv.writer(file)
                writer1.writerow(self.fieldnames)
                file.close()

    def run(self):
        page_max_number = self.get_max_page()
        for i in range(24,page_max_number+1):
            page=self.page%i
            columns=self.get_columns(page)
            for column in columns:
                # column's href
                #tr/th/a[2]/@href
                #http://bbs.eggworld.cn/thread-10100-1-1.html
                href = self.website+self.check_message(self.get_message(column, 'tr/th/a[2]/@href'))
                #column's title
                #tr/th/a[2]/text()
                title=self.check_message(self.get_message(column,'tr/th/a[2]/text()'))
                #column's time
                #/tr/td[2]/em/span/span/@title
                #//*[@id="normalthread_10071"]/tr/td[2]/em/span/span
                #//*[@id="normalthread_10070"]/tr/td[2]/em/span
                release_time = self.check_message(self.get_message(column,'tr/td[2]/em/span/span/@title'))
                if release_time=='0':
                     release_time=self.check_message(self.get_message(column,'tr/td[2]/em/span/text()'))
                print(href,title,release_time)
                time.sleep(1)
                if '全国' in title:
                    self.handling_content(href,release_time)
                # print(href,title)

if __name__ == '__main__':
    a = Egg_ewebV2()
    a.run()
