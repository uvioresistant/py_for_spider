html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name ="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://exampel.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
print(soup.prettify())
print(soup.title.string)
# 首先声明变量html，是一个HTML字符串，但body和html都未闭合
# 接着当做第一个参数传给BeautifulSoup对象，第二个参数为解析器的类型，lxml，完成了BeautifulSoup对象的初始化
# 然后赋值给soup变量
# 调用prettify方法，把要解析的字符串以标准的缩进格式输出，输出结果包含body和html，初始化BeautifulSoup时就完成了
# 再调用soup.title.string，输出HTML中title节点的文本内容
# 所以，soup.title可以选出HTML中的title节点，再调用string属性就可以得到里面的文本了