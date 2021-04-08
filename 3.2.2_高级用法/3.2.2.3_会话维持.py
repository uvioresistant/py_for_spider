# 直接利用get或post模拟网页请求实际上是相当于不同的会话，相当于用了两个浏览器打开不同的页面
# Session对象，维持同一个会话，相当于打开一个新的浏览器选项卡而不是新开一个浏览器，不用每次设置cookies
# import requests
#
# requests.get('http://httpbin.org/cookies/set/number/123456789')
# r = requests.get('http://httpbin.org/cookies')
# print(r.text)

# 请求一个测试网站http://httpbin.org/cookies/set/number/123456789，设置了一个cookie，名称叫做number，内容是123456789，
# 随后请求http://httpbin.org/cookies，此网址可以获取当前的Cookies


import requests

s = requests.Session()
s.get('http://httpbin.org/cookies/set/number/123456789')
r = s.get('http://httpbin.org/cookies')
print(r.text)
# 利用Session，可以做到模拟同一个会话而不用担心Cookies的问题，通常用于模拟登录成功后进行下一步的操作
# Session平常用得非常广泛，用于模拟在一个浏览器中打开同一站点的不同页面
