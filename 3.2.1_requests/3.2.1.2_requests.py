# urllib中的urlopen方法以GET方式请求网页，而requests中响应的方法就是get方法

import requests

r = requests.get('https://www.baidu.com/')
print(type(r))
print(r.status_code)
print(type(r.text))
print(r.text)
print(r.cookies)

# 调用get方法实现与urlopen相同的操作，得到一个Response对象，分别输出Response的类型、状态码、响应体的类型、内容、Cookies
# 返回类型是requests.models.Response,响应体的类型是str, Cookies的类型是RequestsCookieJar
# 使用get方法成功实现一个GET请求，更方便之处在于其他的请求类型依然可以用一句话来完成：
r = requests.post('http://httpbin.org/post')
r = requests.put('http://httpbin.org/put')
r = requests.delete('http://thhpbin.org/delete')
r = requests.head('http://httpbin.org/get')
r = requests.options('http://httpbin.org/get')
# 分别用post、put、delete方法实现了请求