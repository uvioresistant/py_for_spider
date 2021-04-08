# 某些属性同时匹配了多个节点，但只想要其中某个节点
# 第二个节点或者最后一个节点，利用中括号传入索引的方法获取特定次序的节点
from lxml import etree

text='''
<div>
<ul>
<li class="item-0"><a href="link1.html">first item</a></li>
<li class="item-1"><a href="link2.html">second item</a></li>
<li class="itemm-inactive"><a href="link3.html">third item</a></li>
<li class="item-1"><a href="link4.html">fourth item</a></li>
<li class="item-0"><a href="link5.html">fifth item</a>
</ul>
</div>
'''
html = etree.HTML(text)
result = html.xpath('//li[1]/a/text()')
print(result)
result = html.xpath('//li[last()]/a/text()')
print(result)
result = html.xpath('//li[position()<3]/a/text()')
print(result)
result = html.xpath('//li[last()-2]/a/text()')
print(result)
# 第一次选择，选取了第一个li节点，中括号传入数字1，和代码中不同，序号是以1开头，不是以0开头
# 第二次选择，选取了最后一个li节点，中括号传入last即可，返回的便是最后一个li节点
# 第三次选择，选取了位置小于3的li节点，就是位置序号为1和2的节点，得到的结果就是前连个li节点
# 第四次选择，选取倒数第三个li节点，中括号传入last()-2即可，last是最后一个，last()-1就是倒数第三个
