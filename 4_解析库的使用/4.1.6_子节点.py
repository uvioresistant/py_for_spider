# 通过/或//查找元素的子节点或子孙节点
# 选择li节点的所有直接a子节点
# from lxml import etree
#
# html = etree.parse('./test.html', etree.HTMLParser())
# result = html.xpath('//li/a')
# print(result)
# 追加/a选择了所有li节点的所有直接a子节点；//li选中所有li节点，/a选中li节点的所有直接节点a
# 组合后，获取所有li节点的所有直接a子节点


# 获取所有子孙节点用//
# 获取ul节点下的所有子孙a节点
from lxml import etree

html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//ul//a')
print(result)
# 如果用//ul/a，无法获取任何结果；因为在ul节点下没有直接的a子节点，只有li节点
