# POST请求
import requests

data = {'name': 'germey', 'age': '22'}
r = requests.post("http://httpbin.org/post", data=data)
print(r.text)
# form部分就是提交的数据，证明POST请求成功发送了
