# 将请求表示为数据结构Prepared Request
from requests import Request, Session

url = 'http://httpbin.org/post'
data = {
    'name': 'germey'
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36(KHTML, like Gecko)'
         'Chrome/52.0.2743.116 Safari/537.36'
}
s = Session()
req = Request('POST', url, data=data, headers=headers)
prepped = s.prepare_request(req)
r = s.send(prepped)
print(r.text)
# 引入了Request，用rul、data和heeaders参数构造一个Request对象，再调用Session的prepare_request将其转换为
# Prepared Request对象，调用send发送即可
# 大道同样的POST请求效果
# 有了Request，可以将请求当做独立的对象看待，在进行队列调度时会非常方便。