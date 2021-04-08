# 某些节点的某个属性可能有多个值
# from lxml import etree
# text = '''
# <li class="li li-first"><a href ="link.html">first item</a></li>
# '''
# html = etree.HTML(text)
# result = html.xpath('//li[@class="li"]/a/text()')
# print(result)
# HTML文本中li节点class属性有两个值li和li-first，用之前的属性匹配获取，无法匹配
# 需用contains函数，改写如下：
from lxml import etree
text = '''
<li class="li li-first"><a href ="link.html">first item</a></li>
'''
html = etree.HTML(text)
result = html.xpath('//li[contains(@class, "li")]/a/text()')
print(result)
