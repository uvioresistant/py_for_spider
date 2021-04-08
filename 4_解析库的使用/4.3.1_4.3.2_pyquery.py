# 与Beautiful Soup一样，初始化pyquery时，也需要传入HTML文本来初始化一个PyQuery
# 初始化有多样，如直接传入字符串，传入URL，传入文件名等
# 字符串初始化
html = '''
<div>
<ul>
<li class="item-0">first item</li>
<li class="item-1"><a href="link2.html">second item</a></li>
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
<li class="item-1 active"><a href="link4.html"><fourth item</a></li>
<li class="item-0"><a href="link5.html">fifth item</a></li>
</ul>
</div>
'''
from pyquery import PyQuery as pq   # 引入PyQuery对象，取别名为pq
doc = pq(html)  # 声明长HTML字符串，将其当做参数传递给PyQuery类，完成初始化
print(doc('li'))


# URL初始化
# 初始化参数不仅可以以字符串的形式传递，还可以传入网页URL，只需要指定参数为url即可
from pyquery import PyQuery as pq
doc = pq(url='https://cuiqingcai.com')      # 用网页的源代码以字符串形式传递给PyQuery类来初始化
print(doc('title'))

# 文件初始化
# 除了传递URL，还可以传递本地的文件名，将参数指定为filename即可：
from pyquery import PyQuery as pq
doc = pq(filename='demo.html')      # 需要有一个本地HTML文件demo.html.内容是待解析的HTML字符串
print(doc('li'))

# 以上三种初始化方式均可，最常用的还是以字符串形式传递。