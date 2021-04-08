# 用//开头的XPath规则来选取所有符合要求的节点
# from lxml import etree
# html = etree.parse('./test.html', etree.HTMLParser())
# result = html.xpath('//*')
# print(result)

# 代表匹配所有节点,就是整个HTML文本中的所有节点都会被获取，
# 返回形式是一个列表，每个元素是Element类型，其后跟节点名称：html、body、div、ul、li、a等


# 匹配可以指定节点名称，想获取所有li节点
from lxml import etree
html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//li')
print(result)
print(result[0])