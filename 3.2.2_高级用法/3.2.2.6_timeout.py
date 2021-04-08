# 为了防止服务器不能及时响应，应该设置一个超时时间，超过了这个时间还没有得到响应，就报错。
# timeout，时间的计算是发出请求到服务器返回响应的时间
import requests

r = requests.get("https://www.taobao.com", timeout = 1)
print(r.status_code)
# 可以将超时时间设置为1秒，如果1秒内没有响应，就抛出异常
# 请求分为两个阶段，连接connect和读取read，timeout将用作连接和读取两者的timeout总和
#分别制定，可以传入一个元组：
r = requests.get('https://www.taobao.com', timeout=(5,11, 30))
#永久等待，直接将timeout设置为None，或者不设置直接留空，默认是None，永远不会返回超时错误
r = requests.get('https://www.taobao.com', timeout=None)
# 或直接不加参数
r = requests.get('https://www.taobao.com')