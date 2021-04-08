# pyquery提供一系列方法对节点进行动态修改
# 如为某个节点添加一个class，移除节点
# addClass和removeClass
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
li = doc('.item-0.active')          # 选中第三个li节点
print(li)
li.removeClass('active')            # 调用removeClass方法，将li节点的active这个class移除
print(li)
li.addClass('active')               # 调用addClass方法，将class添加回来
print(li)
# addClass和removeClass方法可以动态改变节点的class属性


# 除了操作class属性外，可以用attr方法对属性进行操作
# 还可以用text和html方法改变节点内部的内容
html = '''
<ul class="list">
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
</ul>
'''
from pyquery import PyQuery as pq
doc = pq(html)
li = doc('.item-0.active')              # 首先选中li节点
print(li)
li.attr('name', 'link')                 # 调用attr方法修改属性，第一个参数为属性名；第二个参数为属性值；
print(li)
li.text('changed item')                 # 调用text改变节点内部内容
print(li)
li.html('<span>changed item</span>')    # 调用html方法来改变节点内部内容
print(li)
# 调用attr方法后，li节点多了一个原来不存在的属性name，值为link
# 接着调用text方法，传入文本后，原节节点li内部的文本呗改为传入的字符串文本。
# 调用html方法传入HTML文本后，li节点内部变为传入的HTML文本了

# attr方法只传一个参数的属性名，则是获取这个属性值；若传入第二个参数，可以修改属性值
# text和html方法若不传2参数，则获取节点内纯文本和HTML文本；若传参数，进行赋值。


# remove方法：移除，会为信息提取带来非常大的遍历。
# 想提取Hell，World字符串，而不要p节点内部的字符串
html = '''
<div class="wrap">
    Hello, World
<p> This is a paragraph.</p>
</div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
wrap = doc('.wrap')             # 直接尝试提取class为wrap的节点内容
print(wrap.text())
# 结果还包含了内部p节点内容，即text把所有的纯文本提取出来了。
# 想去掉p节点内部文本，可以选择再把p节点内的文本提取一遍，从整个结果中移除整个子串，做法烦琐。


# 采用remove方法
wrap.find('p').remove()     # 选中p节点，调用remove方法移除，wrap内部只剩下Hello，World了
print(wrap.text())          # 利用text方法提取