import csv
import os
import time
import datetime

import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait



class Egg_e_web():
    def __init__(self):
        # 发起请求时使用的请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        }
        # 起始url
        self.beginurl = 'http://m.eggworld.cn/views/information/taotaiji_list.html?returnurl=../../views/information/hangqing.html&returnurl2='
        self.the_official_website = 'http://m.eggworld.cn/views/eggworld/index.html'

#     http://m.eggworld.cn/views/eggworld/index.html
    def login(self):
        driver = webdriver.Chrome(r'C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver')
        # try:
        driver.get(self.the_official_website)
        time.sleep(3)
        try:
            login_button=WebDriverWait(driver, 20, 0.2).until(lambda x: x.find_element_by_xpath('/html/body/div[2]/div/button[2]'))
            time.sleep(1)
            login_button.click()
            WebDriverWait(driver, 20, 0.2).until(
                lambda x: x.find_element_by_xpath('//*[@id="bdCon"]/div[1]/ul/li[1]/input')).send_keys('18174504650')
            WebDriverWait(driver, 20, 0.2).until(
                lambda x: x.find_element_by_xpath('//*[@id="bdCon"]/div[1]/ul/li[2]/input')).send_keys('123456')
            submmit_button=WebDriverWait(driver, 20, 0.2).until(
                lambda x: x.find_element_by_xpath('//*[@id="bdCon"]/div[1]/button'))
            time.sleep(1)
            submmit_button.click()
        except:
            pass
        print('登录成功')
        return driver

    # 蛋价早报
    def egg_daily_paper(self,driver):
        # 蛋价讨论区
        WebDriverWait(driver, 20, 0.2).until(
            lambda x: x.find_element_by_xpath('//*[@id="content"]/div/div[3]/h3/a/span')).click()
        time.sleep(1)
        # 蛋价早报
        WebDriverWait(driver, 20, 0.2).until(
            lambda x: x.find_element_by_xpath('//*[@id="bdCon"]/div[2]/ul/li[1]/label/img')).click()

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

    def get_size(self,driver):
        x = driver.get_window_size()['width']
        y=driver.get_window_size()['height']
        return x,y

    def run(self):
        driver = self.login()
        self.egg_daily_paper(driver)


        time.sleep(30)



if __name__ == '__main__':
    a = Egg_e_web()
    a.run()


