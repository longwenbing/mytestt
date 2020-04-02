import datetime
import os

import numpy


def subStr(str):
    return str.strip('\\"[]')

def splits(s):
    return s.split(":")
import csv
now_time = datetime.datetime.now().strftime('%Y-%m-%d')
fieldnames=["商店名", "经营模式", "市场位置", "被浏览次数", "批发信息数量", "联系人", "电话", "手机", "电子邮箱", "地址", "邮编", "蛋种", "订货量", "单价","单位", "库存",
             "累计查看次数", "图片"]
local_market_paths=['D:\CCDY_data\武汉白沙洲批发市场','D:\CCDY_data\广西玉林批发市场']

# for path in local_market_paths:
#     if not os.path.exists(path):
#         os.makedirs(path)
# with open('D:\CCDY_data\武汉白沙洲批发市场\%s.csv' % now_time, 'w') as f1:
#         writer1 = csv.writer(f1)
#         writer1.writerow(fieldnames)
# with open('D:\CCDY_data\广西玉林批发市场\%s.csv' % now_time, 'w') as f2:
#     writer2 = csv.writer(f2)
#     writer2.writerow(fieldnames)

# a=[1,1,1,1,1,1,1,1,1,1,1,1,1]
# b=numpy.array(a).reshape(4,3)
# print(b)
a=[]
t=1
for i in [1,1,1,1,1,1,1,1,1,1]:
    t+=1
    a.append(i)
te=int (t/5)
print(numpy.array(a).reshape(te, 5))