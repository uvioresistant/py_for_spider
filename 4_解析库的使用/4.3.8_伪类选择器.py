# CSS选择器之所以强大，重要原因是支持多种多样的伪类选择器
# 如：选择第一个节点，最后一个节点，奇偶数节点、包含某一文本的节点
html = '''
<div class="wrap">
<div id="container">
<ul class="list">
<li class="item-0">first item</li>
<li class="item-1"><a href="link2.html">second item</a></li>
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
<li class="item-1 active"><a href="link4.html">fourth item</a></li>
<li class="item-0"><a href="link5.html"><fifth item</a></li>
</ul>
</div>
</div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
li = doc('li:first-child')      # 选择了第一个li节点
print(li)
li = doc('li:last-child')       # 最后一个li节点
print(li)
li = doc('li:nth-child(2)')     # 第二个li节点
print(li)
li = doc('li:gt(2)')            # 第三个li之后的li节点
print(li)
li = doc('li:nth-child(2n)')    # 偶数位置的li节点
print(li)
li = doc('li:contains(second)') # 包含second文本的li节点
print(li)
