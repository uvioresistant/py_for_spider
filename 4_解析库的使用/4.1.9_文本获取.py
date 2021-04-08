# 用XPath方法获取节点中的文本，尝试获取前面li节点中的文本
# from lxml import etree
#
# html = etree.parse('./test.html', etree.HTMLParser())
# result = html.xpath('//li[@class= "item-0"]/text()')
# print(result)
# 没有获取到任何文本，只获取到一个换行符，因为XPath中test前面是/，而此处/含义是：选取直接子节点，li的直接子节点都是a节点
# 文本都是在a节点内部的，所以匹配到的结果就是被修正的li节点内部的换行符，自动修正的li节点标尾签换行了，选中的是：
# <li class="item-1"><a href="link4.html">fourth item</a></li>
# <li class="item-0"><a href="link5.html">fifth item</a>
# </li>
# 提取文本得到的唯一结果是li节点的尾标签和a节点的尾标签之间的换行符
# 想获取li节点内部的文本：1.先选取a节点再获取文本；2.使用//；区别如下：
# from lxml import etree
#
# html = etree.parse('./test.html', etree.HTMLParser())
# result = html.xpath('//li[@class="item-0"]/a/text()')
# print(result)
# 逐层选取，先选取li节点，又利用/选取了其直接子节点a，再选取其文本
# 另一种方式，使用//选取的结果
from lxml import etree

html = etree.parse('./test.html', etree.HTMLParser())
result = html.xpath('//li[@class="item-0"]//text()')
print(result)
# 想获取子孙节点内部的所有文本，直接用//加text方式，可以保证获取到最全面的文本信息，可能会夹杂换行符等特殊字符
# 想获取某些特定子孙节点下所有文本，先选取特点的子孙节点，再调用text方法获取其内部文本，可以保证获取的结果是整洁的