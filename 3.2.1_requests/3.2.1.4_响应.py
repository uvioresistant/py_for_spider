# 很多属性和方法可以用来获取其他信息
# import requests
#
# r = requests.get('http://www.jianshu.com')
# print(type(r.status_code), r.status_code)
# print(type(r.headers), r.headers)
# print(type(r.cookies), r.cookies)
# print(type(r.url), r.url)
# print(type(r.history), r.history)
# headers和cookies这两个属性得到的结果是CaseInsensitiveDict和RequestsCookieJar类型


# requests提供了一个内置的状态查询对象requests.codes
import requests

r = requests.get('http://www.jianshu.com')
exit() if not r.status_code == requests.codes.ok else print('Request Successfully')