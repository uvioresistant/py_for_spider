# request可以模拟提交一些数据，有的网站需要上传文件，可以用它来实现
import requests

files = {'file': open('favicon.ico', 'rb')}
r = requests.post("http://httpbin.org/post", files=files)
print(r.text)