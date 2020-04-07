import time
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import re

begin_url='http://localhost:4723/wd/hub'
cap = {
            "platformName": "Android",
            "platformVersion": "5",
            "deviceName": "127.0.0.1:62001",
            "appPackage": "app.eggworld.cn.android",
            "appActivity": ".MainActivity",
            "noRest": True
        }
account_number='18174504650'
pwd='123456'

def get_logined_driver(begin_url,cap,account_number,pwd):
    driver = webdriver.Remote(begin_url,cap)
    # login_button "//android.widget.Button[@text='登录']"
    try:
        if WebDriverWait(driver, 10, 0.2).until(
                lambda x: x.find_element_by_xpath("//android.widget.Button[@text='登录']")):
            driver.find_element_by_xpath("//android.widget.Button[@text='登录']").click()
            # account_number //android.widget.ListView/android.view.View[1]/android.widget.EditText[1]
            WebDriverWait(driver, 10, 0.2).until(
                lambda x: x.find_element_by_xpath(
                    '//android.widget.ListView/android.view.View[1]/android.widget.EditText[1]')).send_keys(
                account_number)
            # pwd
            WebDriverWait(driver, 10, 0.2).until(
                lambda x: x.find_element_by_xpath(
                    "//android.widget.ListView/android.view.View[2]/android.widget.EditText[1]")).send_keys(
                pwd)
            # login_button
            WebDriverWait(driver, 10, 0.2).until(
                lambda x: x.find_element_by_xpath("//android.widget.Button[@text='登  录']")).click()
            print("登录成功")
            driver.find_element_by_xpath('')
    except:
        print("已经登录")
        pass
    return driver
# //android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.view.View[1]/android.view.View[5]/android.view.View[2]/android.view.View[1]
# //android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.view.View[1]/android.view.View[5]/android.view.View[3]/android.view.View[1]
# //android.view.View[@resource-id='content']/android.view.View[2]/android.widget.ListView[1]/android.view.View[4]
# 进入鸡蛋黄页的 操作链
def enter_egg_yellow_pages_actions( driver):
    # 进入黄页
    WebDriverWait(driver, 20, 0.8).until(
     lambda x: x.find_element_by_xpath(
         "//android.view.View[@text='蛋鸡黄页']")).click()
    time.sleep(1.5)
    numbers = get_max_enterprise_number(driver)
    print(numbers)
    if numbers != None:
     # 保存到第几个就滑动几次
        for i in range(13, numbers + 2):
            for x in range(2, i):
                slide_litter_screen(driver)
                time.sleep(0.5)
            # try:
            WebDriverWait(driver, 5, 0.2).until(lambda x: x.find_element_by_xpath(
            "//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.view.View[1]/android.view.View[5]/android.view.View[%d]/android.view.View[1]" % i)).click()
            time.sleep(2)
            # while True:
            # try:
            WebDriverWait(driver, 10, 0.5).until(lambda x:x.find_element_by_xpath(
            "//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[1]")).click()
            time.sleep(2)

    else:
        print("没有企业信息！")


def get_max_enterprise_number(driver):
    # 重试三次查找
    for i in range(3):
        try:
            if WebDriverWait(driver, 20, 0.2).until(
                    lambda x: x.find_element_by_xpath(
                        "//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.view.View[1]/android.view.View[4]")):
                str_numbers = driver.find_element_by_xpath(
                    "//android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.webkit.WebView[1]/android.webkit.WebView[1]/android.view.View[1]/android.view.View[1]/android.view.View[4]").text
                return int(re.findall(r'([1-9]\d*)', str_numbers)[0])
        except:
            print("没找到企业，重试")
    return None

# 获取页面的大小
def get_screen_size( driver):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    return (x, y)
# 小滑动
def slide_litter_screen( driver):
    size = get_screen_size(driver)
    # slide_screen start
    x1 = int(size[0] * 0.5)
    y1 = int(size[1] * 0.5)
    # slide_screen end
    y2 = int(size[1] * 0.5 - 240)
    driver.swipe(x1, y1, x1, y2)
# 对齐
def slide_alignment(driver):
    size = get_screen_size(driver)
    # slide_screen start
    x1 = int(size[0] * 0.5)
    y1 = int(size[1] * 0.5)
    # slide_screen end
    y2 = int(size[1] * 0.5 - 45)
    driver.swipe(x1, y1, x1, y2)

def run():
    driver = get_logined_driver(begin_url=begin_url,cap=cap,account_number=account_number,pwd=pwd)
    enter_egg_yellow_pages_actions(driver)

run()