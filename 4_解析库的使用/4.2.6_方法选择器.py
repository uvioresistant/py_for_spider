# 通过属性来选择的方法，非常快，如果进行复杂的选择的话，就比较繁琐
# find_all和find，调用它们，传入响应的参数，就可以灵活查询
# find_all:查询所有符合条件的元素，传入一些属性和文本，得到符合条件的元素。
# API如下：
# find_all(name, attrs, recursive, text, **kwargs)
# 1)name
# 根据节点点查询元素
html ='''
<div class="panel">
<div class="panel-heading">
<h4>Hello</h4>
</div>
<div class="panel-body">
<ul class="list" id="list-1">
<li class="element">Foo</li>
<li class="element">Bar</li>
<li class="element">Jay</li>
</ul>
<ul class="list list-small" id="list-2">
<li class="element">Foo</li>
<li class="element">Bar</li>
</ul>
</div>
</div>
'''
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
print(soup.find_all(name='ul'))
print(type(soup.find_all(name='ul')[0]))
# 调用find_all方法，传入name参数，参数值为ul。
# 想要查询所有ul节点，返回结果是列表类型，长度为2，每个元素依然都是bs4.element.Tag类型


# 都是Tag类型，可以进行嵌套查询，查询出所有ul节点后，再继续查询其内部的li节点：
for ul in soup.find_all(name='ul'):
    print(ul.find_all(name='li'))
    for li in ul.find_all(name='li'):
        print(li.string)
# 2)attrs
# 除了节点查询，还可以传入属性来查询
html ='''
<div class="panel">
<div class="panel-heading">
<h4>Hello</h4>
</div>
<div class="panel-body">
<ul class="list" id="list-1">
<li class="element">Foo</li>
<li class="element">Bar</li>
<li class="element">Jay</li>
</ul>
<ul class="list list-small" id="list-2">
<li class="element">Foo</li>
<li class="element">Bar</li>
</ul>
</div>
</div>
'''
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
print(soup.find_all(attrs={'id': 'list-1'}))
print(soup.find_all(attrs={'name': 'elements'}))
# 查询时传入的是attrs参数，参数类型是字典类型


# 对于常用的属性，如id和class等，可以不用attrs来传递
# 如要查询id为list-1的节点，可以直接传入id这个参数,换一种方式来查询
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
print(soup.find_all(id='list-1'))
print(soup.find_all(class_='element'))
# 直接传入id='list-1',可以查询id为list-1的节点元素，对于class来说，由于class在Python是关键，所以后面需要加下划线


# 3)text可匹配节点的文本，传入形式可以是字符串，可以是正则表达式对象
import re
html = '''
<div class="panel">
<div class="panel-body">
<a>Hello, this is a link</a>
<a>Hello, this is a link, too</a>
</div>
</div>
'''
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
print(soup.find_all(text=re.compile('link')))
# 两个a节点，内部包含文本信息，在find_all方法中传入text参数，该参数为正则表达式对象，返回匹配正则节点文本组成的列表


# find方法：返回单个元素，就是第一个匹配的元素，
html ='''
<div class="panel">
<div class="panel-heading">
<h4>Hello</h4>
</div>
<div class="panel-body">
<ul class="list" id="list-1">
<li class="element">Foo</li>
<li class="element">Bar</li>
<li class="element">Jay</li>
</ul>
<ul class="list list-small" id="list-2">
<li class="element">Foo</li>
<li class="element">Bar</li>
</ul>
</div>
</div>
'''
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
print(soup.find(name='ul'))
print(type(soup.find(name='ul')))
print(soup.find(class_='list'))
# 返回结果不再是列表形式，而是第一个匹配的节点元素，类型依然是Tag类型


# 其他查询方法：
# find_parents()和find_parent(): 前者返回所有祖先节点，后者返回直接父节点
# find_next_siblings()和find_next_sibling():前者返回后面所有的兄弟节点，后者返回后面第一个兄弟节点
# find_previous_siblings()和find_previous_sibling():前者返回前面所有兄弟节点，后者返回前面第一个兄弟节点
# find_all_next()和find_next():前者返回节点后所有符合条件的节点，后者返回第一个符合条件的节点
# find_all_previous()和find_previous():前者返回节点后所有符合条件的节点，后者返回第一个符合条件的节点。
