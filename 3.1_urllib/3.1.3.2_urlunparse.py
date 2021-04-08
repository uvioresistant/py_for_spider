# urlparse对立方法,接受的参数是一个可迭代对象，长度必须是6，否则会抛出参赛数量不足或者过多
from urllib.parse import urlunparse

data = ['http', 'www.baidu.com', 'index.html', 'user', 'a=6', 'comment']
print(urlunparse(data))