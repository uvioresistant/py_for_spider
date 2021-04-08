# 单个节点，可以直接打印输出，也可以直接转成字符串
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
li = doc('.list .item-0.active')
print(li)
print(str(li))


# 多个节点，需要遍历来获取
# 把每一个li节点进行遍历，需要调用items()方法
from pyquery import PyQuery as pq
doc = pq(html)
lis = doc('li').items()
print(type(lis))
for li in lis:
    print(li, type(li))
# 调用items方法后，会得到一个生成器，遍历后，就可以逐个得到li节点对象了，类型也是PyQuery类型