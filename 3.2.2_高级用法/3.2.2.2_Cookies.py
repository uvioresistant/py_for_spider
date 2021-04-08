# 有了requests，获取和设置Cookies只需一步即可完成
import requests

r = requests.get("https://www.baidu.com")
print(r.cookies)
for key, value in r.cookies.items():
    print(key + '=' + value)
# 首先调用cookies属性，可成功得到Cookies，可以发现它是RequestCookieJar类型
# 然后用items方法将其转化为元组组成的列表，遍历输出每一个Cookie的名称和值，实现Cookie的遍历解析


# 直接用Cookie来维持登陆状态。
# 将知乎Headers中的Cookie复制下来
# import requests
#
# headers = {
#     'Cookie':'_zap=181060b2-7a15-4640-8b56-dbeb5f349b01;'
#          ' z_c0="2|1:0|10:1524481379|4:z_c0|92:Mi4xNk8tbUFnQUFBQUFBMEdDMWpKNThEU1lBQUFCZ0FsVk5Zd3ZMV3dBU1NodE1KQzByRXFMaHE2TkxzMW9zZ3RoNU5R|2e8760e312639d44457c1a23ed98e5ee5c42838b1a518bcd054cefce8ed24b99"; '
#          'd_c0="ANBgDO1FiA2PTnBV1ZzJHkdi8s-9JPuqy_8=|1525263435"; __utmv=51854390.100--|2=registration_date=20160221=1^3=entry_date=20160221=1; q_c1=12451e4d66df43d1a540a4e66bcf18b2|1529502956000|1523278672000; _xsrf=Fto89SVBa423QNdCOl5JOGaZ9mIUL1T4; '
#          '__utmz=51854390.1530967771.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/20645098; __utma=51854390.1249901121.1527765840.1530967771.1531145328.3; __utmc=51854390; tgw_l7_route=931b604f0432b1e60014973b6cd4c7bc'
#     'Host': 'www.zhihu.com',
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36',
# }
# r = requests.get('https://www.zhihu.com', headers = headers)
# print(r.text)

import requests

cookies = '_zap=181060b2-7a15-4640-8b56-dbeb5f349b01; z_c0="2|1:0|10:1524481379|4:z_c0|92:Mi4xNk8tbUFnQUFBQUFBMEdDMWpKNThEU1lBQUFCZ0FsVk5Zd3ZMV3dBU1NodE1KQzByRXFMaHE2TkxzMW9zZ3RoNU5R|2e8760e312639d44457c1a23ed98e5ee5c42838b1a518bcd054cefce8ed24b99"; d_c0="ANBgDO1FiA2PTnBV1ZzJHkdi8s-9JPuqy_8=|1525263435"; __utmv=51854390.100--|2=registration_date=20160221=1^3=entry_date=20160221=1; q_c1=12451e4d66df43d1a540a4e66bcf18b2|1529502956000|1523278672000; _xsrf=Fto89SVBa423QNdCOl5JOGaZ9mIUL1T4; __utmz=51854390.1530967771.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/20645098; __utma=51854390.1249901121.1527765840.1530967771.1531145328.3; __utmc=51854390jar = requests.cookies.RequestsCookieJar()'
jar = requests.cookies.RequestsCookieJar()
headers = {
    'Host': 'www.zhihu.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36'
}
for cookie in cookies.split(';'):
    key, value = cookie.split('=', 1)
    jar.set(key, value)
r = requests.get("https://www.zhihu.com", cookies=jar, headers=headers)
print(r.text)

# 先创建一个RequestCookieJar对象
# 将复制下来的cookies利用split方法分割
# 利用set方法设置好每个Cookie的key和value
# 通过调用requests的get方法并传递给cookies参数即可
# 知乎本身的限制，headers参数不能少，只不过不需要在原来的headers参数里面设置cookie字段了。