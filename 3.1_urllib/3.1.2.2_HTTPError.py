# 2.HTTPError：是URLerror的子类，专门处理HTTP请求错误，如认证请求失败，有3个属性：
# code：返回HTTP状态码，404表示网页不存在，500表示服务器内部错误
# reason：同父类，返回错误的原因
# headers： 返回请求头
from urllib import request, error

try:
    response = request.urlopen('https://cuiqingcai.com/index.htm')  # 同样的网址
except error.HTTPError as e:    # 先捕获HTTPError异常
    print(e.reason, e.code, e.headers, seq='\n')    # 获取它的错误状态码、输出了reason、code、headers属性
except error.URLError as e: # 先捕获子类的错误、再去捕获父类的错误，不是HTTPError异常，就捕获URLError异常，
    print(e.reason) # 输出错误原因
else:       # else来处理正常的逻辑
    print('Request Successfully')

# 有时，reason属性返回的不一定是字符串，也可能是一个对象：
import socket
import urllib.request
import urllib.error

try:
    response = urllib.request.urlopen('https://www.baidu.com', timeout=0.01)    # 设置超时时间
except urllib.error.URLError as e:
    print(type(e.reason))
    if isinstance(e.reason, socket.timeout):    # reason的结果是socket.timeout类，用isinstance来判断类型
        print('TIME OUT')   # 强制抛出timeout异常