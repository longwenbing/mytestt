list1=[('北京大洋路', '红蛋', '散框批发', '120-125', '44', '落', '8车'), ('北京回龙观', '红蛋', '散框批发', '124', '44', '落', ''), ('北京石门', '红蛋', '散框批发', '124', '44', '落', '') ]
mysql_data=[]
import numpy as np
for l in list1:
    array = np.array(l)
    tolist = array.tolist()
    tolist.insert(0,'ppp')
    tolist.append('lll')
    mysql_data.append(tolist)
print(mysql_data)

import requests

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
        }

get = requests.get('http://www.baidu.com',headers=headers)
print(get.text)
