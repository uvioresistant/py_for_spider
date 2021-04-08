# 使用CSS选择器，只需要调用select()方法，传入相应的CSS选择器即可
html='''
<div class="panel">
<div class="panel-heading">
<h4>Hello</h4>
</div>
<div class="panel-body">
<ul class="list" id ="list-1">
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
print(soup.select('.panel .panel-heading'))
print(soup.select('ul li'))
print(soup.select('#list-2 .element'))
print(type(soup.select('ul')[0]))


# 嵌套选择
# 先选择所有rl节点，再遍历每个ul节点，选择其li节点
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
for ul in soup.select('ul'):
    print(ul.select('li'))


# 获取属性
# 尝试获取每个ul节点的id属性
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
for ul in soup.select('ul'):
    print(ul['id'])
    print(ul.attrs['id'])


# 获取文本
# 除了string属性，还可以用get_text()
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
for li in soup.select('li'):
    print('Get Text:', li.get_text())
    print('String:', li.string)
# 效果完全一致
# 推荐使用lxml解析库，必要时使用html.parser
# 节点选择，筛选功能弱但是速度快
# 建议使用find或者find_all查询匹配当个结果或多个结果
# 如果对CSS选择器熟悉，可以使用select()方法选择