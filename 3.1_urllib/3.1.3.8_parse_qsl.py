# parse_qsl用于将参数转化为元组组成的列表
from urllib.parse import parse_qsl

query = 'name=germey&age=22'
print(parse_qsl(query))

# 运行结果是一个列表，列表中的每一个元素都是一个元组
# 元组的第一个内容是参数名，第二个内容是参数值