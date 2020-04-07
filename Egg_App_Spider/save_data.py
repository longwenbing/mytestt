import pymysql

#数据存入mysql
def data2mysql(company_info):
    db = pymysql.connect(user='root', host='localhost', port=3306, password='123', db='egg_app_ods')
    cursor = db.cursor()
    sql1 = """
    CREATE TABLE if not exists ods_companies (
	cn VARCHAR(255) NOT NULL  COMMENT'公司名称',
	leader VARCHAR(255) DEFAULT NULL  COMMENT '负责人',
	phone VARCHAR(13) COMMENT'电话',
	operation_time VARCHAR(4) COMMENT '经营时间',
	brand_name VARCHAR(255) COMMENT '自己的品牌',
	category_name VARCHAR(255) COMMENT '鸡蛋种类',
	jizhong_text VARCHAR(255)COMMENT '鸡种信息',
	province VARCHAR(12) COMMENT '省份',
	city VARCHAR(15) COMMENT '城市',
	municipal_district VARCHAR(15) COMMENT '区',
	jidanxiaoshouqudao VARCHAR(12) COMMENT '鸡蛋销售渠道' ,
	jidanshougoushangxingming VARCHAR(16) COMMENT '鸡蛋收购商姓名' ,
	jidanshougoushangdianhua VARCHAR(16) COMMENT '鸡蛋收购商电话',
	taotaijixiaoshouqudao VARCHAR (16) COMMENT '淘汰鸡收购渠道',
	taotaijishougoushangxingming VARCHAR(16) COMMENT '淘汰鸡收购商姓名',
	taotaijishougoushangdianhua VARCHAR(16) COMMENT '淘汰鸡收购商电话',
	logistics_drivers_info VARCHAR(255) COMMENT '运输司机信息',
	fodder_type VARCHAR(255) COMMENT '用料种类',
	iszidongqingfen VARCHAR(5) COMMENT '是否自动处理',
	iszidongweiliao VARCHAR(5)COMMENT '是否自动喂料',
	isfenwuchulishebei VARCHAR(5)COMMENT '是否粪污处理设备',
	latitude VARCHAR(16) COMMENT '经度',
	longitude VARCHAR(16) COMMENT '纬度',
	LastUpdateTime VARCHAR(32) COMMENT '上一次更新时间'
)
    """

    cursor.execute(sql1)
    sql2 = "\
        insert into egg_app_ods.ods_companies values (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')\
        " % (company_info['cn'],company_info["leader"],company_info["phone"],company_info["operation_time"],company_info["BrandName"],company_info["jizhongtext"],
             company_info["category_name"],company_info["province"],company_info["city"],company_info["municipal_district"],
             company_info["jidanxiaoshouqudao"],company_info["jidanshougoushangxingming"],company_info["jidanshougoushangdianhua"],
             company_info["taotaijixiaoshouqudao"] ,company_info["taotaijishougoushangxingming"],company_info["taotaijishougoushangdianhua"],
             company_info["logistics_drivers_info"],company_info["fodder_type"],company_info["iszidongqingfen"],company_info["iszidongweiliao"],
             company_info["isfenwuchulishebei"],company_info["latitude"],company_info["longitude"] ,company_info["LastUpdateTime"])
    print(sql2)
    cursor.execute(sql2)
    print("插入成功")
    db.commit()
    cursor.close()
    db.close()
