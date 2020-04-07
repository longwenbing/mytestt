import json
# str='{"Code":200,"Msg":null,"UserData":{"ID":"16ab3c95-5985-4ee5-969d-c7900889c511","yangzhichangmingchen":"阜阳金牌养鸡总场","fuzerenxingming":"郝胜杰","fuzerendianhua":"18655836579","jiansheguimo":50.00,"xiancunlanliang":50.00,"BartonNumber":13,"OperationTime":15,"CategoryName":"红蛋,粉蛋","gudingdianhua":"18655836579","shengid":"13","sheng":"安徽省","shiid":"143","shi":"阜阳市","quid":"1474","qu":"市辖区","latitude":"32.836529","longitude":"115.85611","pic_1":"http://img.eggworld.com.cn/eggworld/product/2019_10/15/637067765413351120.jpg","pic_2":null,"pic_3":"http://img.eggworld.com.cn/eggworld/product/2019_10/15/637067766591261348.jpg","pic_4":"http://img.eggworld.com.cn/eggworld/product/2019_10/15/637067767559366710.jpg","jidanxiaoshouqudaotype":3,"jidanxiaoshouqudao":"自建渠道","jidanshougoushangxingming":"郝胜杰","jidanshougoushangdianhua":"18655836579","taotaijixiaoshouqudaotype":3,"taotaijixiaoshouqudao":"自建渠道","taotaijishougoushangxingming":"郝胜杰","taotaijishougoushangdianhua":"18655836576","shifouyouwuliuche":true,"wuliuchesijilist":[{"wuliuchesijixingming":null,"wuliuchesijidianhua":null}],"youwudaikuangxuqiu":false,"youwuhuayanxuqiu":false,"youwuzijidepingpai":true,"BrandName":"绿发，村姑，皖北","qitaxuqiu":false,"shengchanjingyingqitaxuqiu":null,"isjietilong":false,"iscengdielong":true,"issanyang":false,"iszidongqingfen":true,"iszidongweiliao":true,"isfenwuchulishebei":true,"isxiaodushebei":true,"iszidongjidanshebei":true,"isbeinongdayonghu":true,"isbeinongdajimiaoyonghu":true,"isbeinongdasiliaoyonghu":true,"yijianjianyi":null,"xingjipingfen":5,"piciList":[{"piciid":1412,"jizhongid":0,"jizhongstring":"京粉","riling":140,"shuliang":12,"isgoumaiyangzhibaoxian":false}],"CurrentUserID":54773,"IsVip":true,"IsAuthor":false,"IsOpen":true,"JiZhongText":"京粉","LastUpdateTime":"2019-10-15T22:54:32.163","FodderType":"预混料","FodderBrand":null,"CompanyIntroduce":null,"HasEggGradingDevice":false,"PassportUserID":54773,"MsgCode":null,"TokenString":null,"Address":null,"VaccineManufacturers":null,"IsFuGai":0,"FeatureID":0},"ErrorCode":200}'

# da = json.loads(str)
# loads = da["UserData"]
# cn = loads["yangzhichangmingchen"]
# leader=loads['fuzerenxingming']
# scale=loads['jiansheguimo']
# stock_on_hand=loads['xiancunlanliang']
# barton_number=loads['BartonNumber']
# operation_time=loads['OperationTime']
# category_name=loads['CategoryName']
# phone=loads['gudingdianhua']
# province=loads['sheng']
# city=loads['shi']
# municipal_district =loads['qu']
# latitude=loads['latitude']
# longitude=loads['longitude']
# jidanxiaoshouqudao=loads['jidanxiaoshouqudao']
# jidanshougoushangxingming=loads['jidanshougoushangxingming']
# jidanshougoushangdianhua=loads['jidanshougoushangdianhua']
# taotaijixiaoshouqudao=loads['taotaijixiaoshouqudaotype']
# taotaijishougoushangxingming=loads['taotaijishougoushangxingming']
# taotaijishougoushangdianhua=loads['taotaijishougoushangdianhua']
# wuliuchesijixingming=loads['wuliuchesijilist']['wuliuchesijixingming']
# wuliuchesijidianhua=loads['wuliuchesijilist']['wuliuchesijidianhua']
# jizhongtext=loads['JiZhongText']
# fodder_type=loads['FodderType']
# LastUpdateTime=loads['LastUpdateTime']
from datetime import datetime
release_time_temp='2020-2-2'
release_time=release_time_temp
if '-' in release_time_temp:
    split = release_time_temp.split('-')
    year = split[0]
    m = split[1]
    d = split[2]
    if len(m) == 1:
        m = '0' + m
    if len(d) == 1:
        d = '0' + d
    release_time = year + '-' + m + '-' + d
print(datetime.strptime('2019-10-15T22:54:32.163', '%Y-%m-%dT%H:%M:%S.%f'))



print(release_time)
def fommatetime(value):
    year = value[0: 4]
    month = value[5: 7]
    day = value[8: 10]
    hour = value[11: 13]
    min = value[14: 16]
    second = value[17:19]
    return year + "-" + month + "-" + day + " " + hour + ":" + min + ":"+second

t='2019-10-15T22:54:32.163'
print(fommatetime(t))

