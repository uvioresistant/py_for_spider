# 反序列化，有一串GET请求参数，利用parse_qs方法，可以将它转回字典
from urllib.parse import parse_qs

query = 'name=germey&age=22'
print(parse_qs(query))