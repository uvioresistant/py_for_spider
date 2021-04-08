# 用@进行属性过滤
# 选取class为item-1的li节点：
from lxml import etree
html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//li[@class="item-0"]')
print(result)
# 通过加入[@class="item-0"],限制了节点class属性为item-0，符合的节点有两个，结果应返回两个匹配到的元素