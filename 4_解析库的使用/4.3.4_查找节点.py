# 子节点
# 查找子节点时，需要用到find方法传入的参数是CSS选择器
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
items = doc('.list')    # 选取class为list的节点
print(type(items))
print(items)
lis = items.find('li')  # 调用find方法，传入CSS选择器，选取内部li节点
print(type(lis))
print(lis)      # find方法会将符合条件的所有节点选择出来，结果类型是PyQuery类型


# find 的查找范围是节点的所有子孙节点，如果只想查找子节点，可以用children方法：
list = items.children()
print(type(lis))
print(lis)


# 如要筛选所有子节点中符合条件的节点，如筛选出子节点中class为active的节点，可以向children()方法传入CSS选择器.active:
lis = items.children('.active')     # 输出结果已做了筛选，留下了class为active的节点
print(lis)


# 父节点
# 用parent方法来获取某个节点的父节点
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
items = doc('.list')    # 用.list选取class为list的节点
container = items.parent()      # 调用parent方法得到其父节点，父节点为直接父节点。
print(type(container))
print(container)


# 获取某个祖先节点，用parents方法
from pyquery import PyQuery as pq
doc = pq(html)
items = doc('.list')    # 用.list选取class为list的节点
parents = items.parents()      # 调用parent方法得到其父节点，父节点为直接父节点。
print(type(parents))
print(parents)
# 输出结果有两个：一个是class为wrap节点；一个是id为container的节点，parents方法会返回所有的祖先节点


# 想要筛选某个祖先节点，向parents方法传入CSS选择器
parent = items.parents('.wrap')
print(parent)
# 只保留了class为wrap的节点


# 兄弟节点，使用siblings方法
from pyquery import PyQuery as pq
doc = pq(html)
li = doc('.list .item-0.active')        # 选择class为list的节点内部class为item-0和active的节点，即第三个li节点
print(li.siblings())
# 输出4个兄弟节点


# 如果筛选某个兄弟节点，依然可以向siblings方法传入CSS选择器，会从所有兄弟节点中挑选出符合条件的节点了：
from pyquery import PyQuery as pq
doc = pq(html)
li = doc('.list .item-0.active')        # 筛选class为active的节点，只有第四个li节点符合
print(li.siblings('.active'))


