# import matplotlib.pyplot as plt
# from bs4 import BeautifulSoup
# from  lxml import etree
# import numpy as np
# import pandas as pd
# x=np.arange(-np.pi,np.pi,0.01)
# y=np.sin(x)
# plt.plot(x,y,'g')
# plt.show()
# import datetime
# now_time = datetime.datetime.now().strftime('%Y-%m-%d')
# print(now_time)
#
# import pandas as pd
# from pandas import DataFrame
#
# df = DataFrame([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]], index=[0, 1, 2], columns=list("ABCD"))
# df.to_excel('test.xls')
# print("ok")
import datetime
import re

import pandas as pd


# python+pandas 保存list到本地
# def deal():
#     # 二维list
#     company_name_list = [['腾讯', '北京'], ['阿里巴巴', '杭州'], ['字节跳动', '北京']]
#
# 	# list转dataframe
#     df = pd.DataFrame(company_name_list, columns=['company_name', 'local'])
#
# 	# 保存到本地excel
#     df.to_excel("company_name_li.xlsx", index=False)
#
#
# if __name__ == '__main__':
#     deal()


# def split_content( text):
#     print(text)
#     egg_types = ['红蛋', '粉蛋', '褐壳蛋']
#     split_fields = ['蛋价', '价']
#     egg_type = '红蛋'
#     field = '蛋价'
#     for t in egg_types:
#         if t in text:
#             egg_type = t
#             break
#     for f in split_fields:
#         if f in text:
#             field = f
#             break
#     print(egg_type, field)
#
# split_content('aaaaa褐蛋bbbb价cccc')
# s='重庆沙坪坝红蛋纸箱批发价3.7-3.8元稳粉蛋纸箱批发价3.8-4元稳'
# d='北京大洋路红蛋散框批发价125-127元44斤涨（3车)'
# egg_type='红蛋'
# field='价'
# print(re.findall(r'%s(.*?)%s'%(egg_type,field),s)[0])
# print(re.findall(r'元([\u4E00-\u9FA5]{1})',s)[0])
# print(re.findall(r'（(.*?)）',d)[0])
# def split_content( text):
#     # print(text)
#     egg_types = ['红蛋', '粉蛋', '褐壳蛋']
#     split_fields = ['蛋价', '价']
#     egg_type = '红蛋'
#     field = '蛋价'
#     for t in egg_types:
#         if t in text:
#             egg_type = t
#             break
#     for f in split_fields:
#         if f in text:
#             field = f
#             break
#     area = text.split(egg_type)[0]
#     sale_mode = re.findall(r'%s(.*?)%s' % (egg_type, field), text)[0]
#     price = re.findall(r'%s(.*?)元' % field, text)[0]
#     unit = re.findall(r'(\d+)斤', text)
#     if unit == None or unit == []:
#         unit = '0.5'
#     else:
#         unit = re.findall(r'元(.*?)斤', text)[0]
#     # [\u4E00-\u9FA5] 中文
#     trend = '稳'
#     trend_temp = re.findall(r'(斤[\u4E00-\u9FA5]{1})', text)
#     if trend_temp == None or trend_temp == []:
#         trend = re.findall(r'(元[\u4E00-\u9FA5]{1})', text)[0]
#     else:
#         trend = trend_temp[0]
#     extra = ''
#     extra_temp = re.findall(r'，?\(?(.*?)\)?', text)
#     if extra_temp == None or extra_temp == []:
#         pass
#     else:
#         extra = extra_temp[0]
#     print(area, sale_mode, price, unit, trend, extra)
#     return area, sale_mode, price, unit, trend, extra
t='辽宁大连红蛋散框到户蛋价66元45斤'

# print(re.findall(r'（(.*?)）',t)[0])

# if re.findall(r'元([\u4E00-\u9FA5]{1})', t) != []:
#     print("有")
# else:
#     print('无')
# 21吉林
# print(re.findall(r'(\d+)斤', t))

now = datetime.datetime.now()
delta = datetime.timedelta(days=-3)
n_days = now + delta
print(n_days.strftime('%Y-%m-%d'))
