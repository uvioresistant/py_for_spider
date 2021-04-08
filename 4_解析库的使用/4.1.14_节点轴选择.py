# XPath提供很多节点轴选择方法：获取子元素、兄弟元素、父元素、祖先元素
from lxml import etree
text = '''
<div>
<ul>
<li class="item-0"><a href="link1.html">first item</a></li>
<li class="item-1"><a href="link2.html">second item</a></li>
<li class="item-inactive"><a href="link3.html">third item</a></li>
<li class="item-1"><a href="link4.html">fourth item</a></li>
<li class="item-0"><a href="link5.html">fifth item</a>
</ul>
</div>
'''
html = etree.HTML(text)
result = html.xpath('//li[1]/ancestor::*')  #调用ancestor轴，获取所有祖先节点，后面需要跟两个冒号，节点选择器直接用*，包括html、body、div、ul
print(result)
result = html.xpath('//li[1]/ancestor::div')    #加限定条件，冒号后div，结果只有div这个祖先节点
print(result)
result = html.xpath('//li[1]/attribute::*')     #同1
print(result)
result = html.xpath('//li[1]/child::a[@href="link1.html"]')     #调用child轴，获取所有直接子节点，加条件，选href属性为link1.html的a节点
print(result)
result = html.xpath('//li[1]/descendant::span')     #调用descendant轴，获取所有子孙节点，加条件获取span节点，返回结果包含span节点不含a节点
print(result)
result = html.xpath('//li[1]/following::*[2]')      #调用following轴，获取当前节点后的所有节点，加了索引选择，只获取第二个后续节点
print(result)
result = html.xpath('//li[1]/following-sibling::*')     #调用following-sibling轴，获取当前节点后的所有同级节点，获取所有后续同级节点
print(result)
