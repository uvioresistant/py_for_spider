# 用@符号可以获取节点属性
# 获取所有li节点下所有a节点的href属性
from lxml import etree

html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//li/a/@href')
print(result)
# 通过@href获取节点的href属性；和属性匹配方法不同
# 属性匹配是中括号加属性名和值来限定某个属性[@href="link1.html"];@href指的是获取节点的某个属性