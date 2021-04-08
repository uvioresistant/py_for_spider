#与rulunparse类似，也是将链接各个部分组合成完整链接的方法，传入的参数也是一个可迭代对象，唯一区别是长度必须为5
from urllib.parse import urlunsplit

data = ['http', 'www.baidu.com', 'index.html', 'a=6', 'comment']
print(urlunsplit(data))