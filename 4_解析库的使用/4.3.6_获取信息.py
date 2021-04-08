# 提取节点后，提取节点所包含的信息
# 一是获取属性，二是获取文本
# 获取属性：提取到某个PyQuery类型的节点后，可以调用attr()方法获取属性：
html = '''
<div id="container">
<ul class="list">
<li class="item-0">first item</li>
<li class="item-1"><a href="link2.html">second item</a></li>
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
<li class="item-1 active"><a href="link4.html"><fourth item</a></li>
<li class="item-0"><a href="link5.html">fifth item</a></li>
</ul>
</div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
a = doc('.item-0.active a')     # 首先选中class为item-0和active的li节点内的a节点，类型是PyQuery类型
print(a, type(a))
print(a.attr('href'))           # 调用attr方法，在方法中传入属性的名称，就可以得到这个属性值了


# 也可以通过调用attr属性来获取属性
print(a.attr.href)


# 选中多个元素，然后调用attr()方法
a = doc('a')
print(a, type(a))
print(a.attr('href'))
print(a.attr.href)
# 返回结果包含多个节点时，调用attr()方法，只会得到第一个节点的属性


# 想获取所有a节点的属性，要用到前面所说的遍历了
from pyquery import PyQuery as pq
doc = pq(html)
a = doc('a')
for item in a.items():
    print(item.attr('href'))
# 进行属性获取时，观察返回节点是一个还是多个，如果是多个，需要遍历才能依次获取每个节点的属性。


# 获取文本
# 获取节点后的另一个主要操作就是获取内部的文本了，调用text方法实现：
html = '''
<div class="wrap">
<div id="container">
<ul class="list">
<li class="item-0">first item</li>
<li class="item-1"><a href="link2.html">second item</a></li>
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
<li class="item-1 active"><a href="link4.html">fourth item</a></li>
<li class="item-0"><a href="link5.html">fifth item</a></li>
</ul>
</div>
</div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
a = doc('.item-0.active a')     # 首先选中一个a节点
print(a)
print(a.text())                 # 然后调用text方法，可以获取其内部的文本信息，会忽略节点内部包含的所有HTML，只返回纯文字内容


# 想要获取节点内部的HTML文本，要用html方法
from pyquery import PyQuery as pq
doc = pq(html)
li = doc('.item-0.active')      # 选中第三个li节点
print(a)
print(a.html())                 # 调用html方法，返回结果是li节点内的所有HTML文本


# 选中的结果是多个节点，text或html返回什么内容？
html = '''
<div class="wrap">
<div id="container">
<ul class="list">
<li class="item-1"><a href="link2.html">second item</a></li>
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
<li class="item-1 active"><a href="link4.html">fourth item</a></li>
<li class="item-0"><a href="link5.html">fifth item</a></li>
</ul>
</div>
</div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
li = doc('li')
print(li.html())
print(li.text())
print(type(li.text()))
# html返回的是第一个li节点的内部HTML文本，而text则返回所有的li节点内部的纯文本，中间用空格分割开，返回结果是字符串