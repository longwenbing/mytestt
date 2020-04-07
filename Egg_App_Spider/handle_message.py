import json
# str='{"Code":200,"Msg":null,"UserData":{"ID":"eb7c2604-5db9-4f4f-bf1a-3011db5b4cec","yangzhichangmingchen":"大城福泽家禽养殖 专业农民合作社","fuzerenxingming":"刘朋朋","fuzerendianhua":"13663168836","jiansheguimo":4.00,"xiancunlanliang":3.00,"BartonNumber":7,"OperationTime":2015,"CategoryName":"红蛋,粉蛋,其它","gudingdianhua":"13663168836","shengid":"4","sheng":"河北省","shiid":"46","shi":"廊坊市","quid":"580","qu":"大城县","latitude":"38.689935","longitude":"116.632883","pic_1":"http://img.eggworld.com.cn/eggworld/product/2018_11/07/636771715201317008.jpg","pic_2":"http://img.eggworld.com.cn/eggworld/product/2018_11/07/636771715267410348.jpg","pic_3":"http://img.eggworld.com.cn/eggworld/product/2018_11/07/636771715330222974.jpg","pic_4":"http://img.eggworld.com.cn/eggworld/product/2018_11/07/636771715449910216.jpg","jidanxiaoshouqudaotype":2,"jidanxiaoshouqudao":"上门收购","jidanshougoushangxingming":null,"jidanshougoushangdianhua":null,"taotaijixiaoshouqudaotype":2,"taotaijixiaoshouqudao":"上门收购","taotaijishougoushangxingming":null,"taotaijishougoushangdianhua":null,"shifouyouwuliuche":false,"wuliuchesijilist":[{"wuliuchesijixingming":"刘","wuliuchesijidianhua":"13663168836"}],"youwudaikuangxuqiu":true,"youwuhuayanxuqiu":false,"youwuzijidepingpai":false,"BrandName":null,"qitaxuqiu":false,"shengchanjingyingqitaxuqiu":null,"isjietilong":true,"iscengdielong":false,"issanyang":false,"iszidongqingfen":true,"iszidongweiliao":true,"isfenwuchulishebei":true,"isxiaodushebei":true,"iszidongjidanshebei":false,"isbeinongdayonghu":false,"isbeinongdajimiaoyonghu":false,"isbeinongdasiliaoyonghu":false,"yijianjianyi":null,"xingjipingfen":0,"piciList":[{"piciid":1384,"jizhongid":0,"jizhongstring":"罗曼褐","riling":340,"shuliang":10000,"isgoumaiyangzhibaoxian":false},{"piciid":1382,"jizhongid":0,"jizhongstring":"海兰褐","riling":230,"shuliang":10000,"isgoumaiyangzhibaoxian":false},{"piciid":1383,"jizhongid":0,"jizhongstring":"海兰褐","riling":440,"shuliang":10000,"isgoumaiyangzhibaoxian":false}],"CurrentUserID":51467,"IsVip":true,"IsAuthor":false,"IsOpen":true,"JiZhongText":"罗曼褐,海兰褐,海兰褐","LastUpdateTime":"2018-11-07T07:18:40.123","FodderType":"浓缩料","FodderBrand":"正大农牧","CompanyIntroduce":null,"HasEggGradingDevice":false,"PassportUserID":51467,"MsgCode":null,"TokenString":null,"Address":null,"VaccineManufacturers":"维奥兰羽","IsFuGai":0,"FeatureID":0},"ErrorCode":200}'


def handle_mes(mes):
    print(mes)
    print('*'*20)
    company_info={}
    loads = json.loads(mes)['UserData']
    company_info["cn"]=handle_None_data(loads["yangzhichangmingchen"])
    company_info["leader"]=handle_None_data(loads["fuzerenxingming"])
    if '未授权'in company_info["leader"]:
        company_info["leader"]=''
    company_info["phone"] = handle_None_data(loads['gudingdianhua'])
    if '未授权'in company_info["phone"]:
        company_info["phone"]=''
    year=handle_None_data(loads['OperationTime'])
    if year!=None and year>200  :
        company_info["operation_time"]=2020-year
    else:
        company_info["operation_time"] = handle_None_data(loads['OperationTime'])
    company_info["BrandName"]=handle_None_data(loads['BrandName'])
    company_info["jizhongtext"] = handle_None_data(loads['JiZhongText'])
    company_info["category_name"] = handle_None_data(loads['CategoryName'])
    company_info["province"] = handle_None_data(loads['sheng'])
    company_info["city"] = handle_None_data(loads['shi'])
    company_info["municipal_district"] = handle_None_data(loads['qu'])
    company_info["jidanxiaoshouqudao"] = handle_None_data(loads['jidanxiaoshouqudao'])
    company_info["jidanshougoushangxingming"] = handle_None_data(loads['jidanshougoushangxingming'])
    company_info["jidanshougoushangdianhua"] = handle_None_data(loads['jidanshougoushangdianhua'])
    company_info["taotaijixiaoshouqudao"] = handle_None_data(loads['taotaijixiaoshouqudao'])

    company_info["taotaijishougoushangxingming"] = handle_None_data(loads['taotaijishougoushangxingming'])
    company_info["taotaijishougoushangdianhua"] = handle_None_data(loads['taotaijishougoushangdianhua'])
    #物流司机列表
    logistics_drivers_info = ''
    if loads['wuliuchesijilist']!=None:
        for i in loads['wuliuchesijilist']:
            if i['wuliuchesijixingming']==None:
                pass
            else:
                logistics_drivers_info=logistics_drivers_info+i['wuliuchesijixingming']+','+i['wuliuchesijidianhua']+'；'
            print(i['wuliuchesijixingming'])
    if len(logistics_drivers_info)<=2:
        logistics_drivers_info=''
    else:
        logistics_drivers_info=logistics_drivers_info[0:len(logistics_drivers_info)-2]

    company_info["logistics_drivers_info"] = logistics_drivers_info
    company_info["fodder_type"] = handle_None_data(loads['FodderType'])
    company_info["iszidongqingfen"]=check_boolean_data(loads['iszidongqingfen'])

    company_info["iszidongweiliao"]=check_boolean_data(loads['iszidongweiliao'])
    company_info["isfenwuchulishebei"]=check_boolean_data(loads['isfenwuchulishebei'])
    company_info["latitude"] = handle_None_data(loads['latitude'])
    company_info["longitude"] = handle_None_data(loads['longitude'])
    last_update_time=fommatetime(loads['LastUpdateTime'])
    company_info["LastUpdateTime"] = last_update_time
    print(company_info)
    return company_info

def fommatetime(value):
    try:
        year = value[0: 4]
        month = value[5: 7]
        day = value[8: 10]
        hour = value[11: 13]
        min = value[14: 16]
        second = value[17:19]
    except:
        year = ''
        month = ""
        day =''
        hour = ''
        min = ''
        second = ''
    return year + "-" + month + "-" + day + " " + hour + ":" + min + ":"+second
#处理None数据
def handle_None_data(data):
    if data==None:
        return ''
    else:
        return data
#check Boolean
def check_boolean_data(data):
    if data==True:
        return '是'
    else:
        return '否'