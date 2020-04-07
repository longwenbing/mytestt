import csv
import os

savePath = 'D://CSDY_data/蛋e网各省价格一览'
filePath = 'D://CSDY_data/蛋e网蛋价'
header = ('省份','城市', '蛋种', '销售方式', '价格/元', '单位/斤', '趋势', '其他信息', '时间')
provinces = os.listdir(filePath)

import pymysql


def data2mysql(data):
    db = pymysql.connect(user='root', host='localhost', port=3306, password='123', db='egg_app_ods')
    cursor = db.cursor()
    sql1 = """
    create table if not exists ods_egg_price(
    province varchar(255),
    area varchar(255),
    egg_type varchar(30),
    sale_mode varchar(30),
    price varchar(10),
    jin varchar(10),
    trend varchar(6),
    exter varchar(255),
    release_time varchar(16)
    )
    """
    for d in data:
        cursor.execute(sql1)
        sql2 = "\
        insert into egg_app_ods.ods_egg_price values (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')\
        "%(d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7],d[8])
        print(sql2)
        cursor.execute(sql2)
        print("插入成功")
    return (db,cursor)

def save_csv(province,data):
    if os.path.exists(savePath + '/' + province + '.csv'):
        with open(savePath + '/' + '%s.csv' % province, 'a', newline='', encoding='UTF-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
    else:
        with open(savePath + '/' + '%s.csv' % province, 'w+', newline='', encoding='UTF-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(list(header))
            writer.writerows(data)
    csvfile.close()
    print(savePath + '/' + province + '.csv'+'  写入完成')


def save():
    result=[]
    for province in provinces:
        province_datas_path = filePath + "/" + province
        data_list = os.listdir(province_datas_path)
        data_list.sort(reverse=True)
        with open(savePath + '/' + '%s.csv' % province, 'w+', newline='', encoding='UTF-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(list(header))
            for data in data_list:
                # if (os.path.isdir(filePath + '/'+province+'/' + data)):  # 判断是否是文件夹
                if (data[0] == '.'):  # 排除隐藏文件夹
                    pass
                else:  # 添加非隐藏文件
                    date_time = data.split('.')[0]
                    df = open(filePath + '/' + province + '/' + data, encoding="GBK")
                    for raw in df:
                        if "城市" in raw:
                            pass
                        else:
                            raw = province+','+raw.replace('\n', ' ') + ',' + date_time
                            split = list(raw.split(','))
                            print(split)
                            result.append(split)
            writer.writerows(result)
            print(province+" finished")
            mysql = data2mysql(result)
            mysql[0].commit()
            mysql[0].close()
            mysql[1].close()
            result.clear()
        csvfile.close()
        print(province + " 完成")
# save()
