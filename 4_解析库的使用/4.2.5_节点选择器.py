# 直接调用节点的名称就可以选择节点元素，再调用string属性得到节点内的文本，如果单个节点结构层次清晰，可选用
# # 1.选择元素
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
print(soup.title)   # 打印输出title节点的选择结果，是title节点+里面的文字内容
print(type(soup.title))     # 输出它的类型，是bs4.element.Tag类型，Beautiful Soup中一个重要数据结构，
print(soup.title.string)    # Tag属性（string）得到节点的文本内容
print(soup.head)        # 尝试选择了head节点，结果是，节点+内部所有内容
print(soup.p)           # 选择p节点，当有多个节点时，只会选择第一个匹配的节点，后面节点都忽略


# 2.提取信息
# 获取节点属性的值、节点名
# 2.1)获取名称：利用name属性获取节点的名称，选取title节点，然后调用name属性就可以得到节点名称：
print(soup.title.name)
# 2.2)获取属性：每个节点可能有多个属性，如id和class，选择这个节点元素后，可以调用attrs获取所有属性：
print(soup.p.attrs)
print(soup.p.attrs['name'])
# attrs返回结果是字典形式，把选择的节点所有属性和属性值结合成一个字典。
# 要获取name属性，相当于从字典中获取某个键值，需要中括号加属性名
# 更简单的获取方式，不用写attrs，直接在节点元素后面加中括号，传入属性名就可以获取属性值了
print(soup.p['name'])
print(soup.p['class'])
# 需要注意的是，返回结果是字符串或字符串组成的列表，注意判断类型
# 2.3)获取内容：利用string属性获取节点元素包含的文本内容
print(soup.p.string)
# 选择到的p节点是第一个p节点，获取的文本也是第一个p节点里面的文本
# 嵌套选择：每一个返回结果都是bs4.element.Tag类型，可以继续调用节点进行下一步的选择
# 获取了head节点元素，可以继续调用head来选取其内部的head节点元素
html = """
<html><head><title>The Dormouse's story</title></head>
<body>
"""
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
print(soup.head.title)
print(type(soup.head.title))
print(soup.head.title.string)
# 调用head后再次调用title选择的title节点元素，打印输出了它的类型，仍是bs4.element.Tag类型；
# 即在Tag类型的基础上再次选择得到的依然还是Tag类型，每次返回的结果都相同，就可以做嵌套选择了
# 输入它的string属性，就是节点里的文本内容。

# 关联选择
# 做选择得到实惠，不能做到一步就选到想要的节点元素，需要先选中某一个节点元素，再选择它的子节点、父节点、兄弟节点
# 1)子节点和子孙节点
# 选取节点元素，想要获取它的直接节点，contents属性
html = """
<html>
<head>
<title>The Dormouse's story</title>
</head>
<body>
<p class="story">
            Once upon a time there were three litthle sisters; and their names were
<a href="http://example.com/elsie" class ="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class ="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class ="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.
</p>
<p class="story">...</p>
"""
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
print(soup.p.contents)
# 返回结果是列表形式。p节点里既包含文本，包含节点，以列表形式统一返回
# 每个元素都是p节点的直接子节点。


# 调用children属性得到相应的结果：
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
print(soup.p.children)
for i, child in enumerate(soup.p.children):
    print(i, child)
# 调用了children属性来选择，返回结果是生成器类型，用for循环输出相应内容
# 要得到所有的子孙节点，调用descendants属性：
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
print(soup.p.descendants)
for i, child in enumerate(soup.p.descendants):
    print(i, child)
# 返回结果还是生成器，遍历输出可看出，输出结果包含了span节点。descendants会递归查询所有子节点，得到所有子孙节点
# 2)父节点和祖先节点
# 获取某个几点元素的父节点，可调用parent属性：
html = """
<html>
<head>
<title>The Dormouse's story</title>
</head>
<body>
<p class="story">
            Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">
<span>Elsie</span>
</a>
</p>
<p class="story">...</p>
"""
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
print(soup.a.parent)
# 选择第一个a节点的父节点元素，父节点是p节点，输出结果是p节点及其内部的内容
# 输出的仅仅是a节点的直接父节点，没有再向外寻找父节点的祖先节点。
# 想获取所有祖先节点，可以调用parents属性
html = """
<html>
<body>
<p class="story">
<a href="http://example.com/elsie" class="sister" id="link1">
<span>Elsie</span>
</a>
</p>
"""
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
print(type(soup.a.parent))
print(list(enumerate(soup.a.parents)))
# 返回结果是生成器，用列表输出它的索引和内容列表中的元素就是a节点的祖先节点。


# 3)兄弟节点
# 获取同级节点（兄弟节点）：
html = """
<html>
<body>
<p class="story">
            Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">
<span>Elsie</span>
</a>
            Hello
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a>
            and
<a href="http://example.como/tillie" class="sister" id="link3">Tillie</a>
            and they lived at the bottom of a well.
</p>
"""
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
print('Next Sibling', soup.a.next_sibling)
print('Prev Sibling', soup.a.previous_sibling)
print('Next Siblings', list(enumerate(soup.a.next_siblings)))
print('Prev Siblings', list(enumerate(soup.a.previous_sibling)))
# next_sibling和previous_sibing分别获取节点的下一个和上一个兄弟元素，next_siblings和previous_sibings
# 则分别返回所有前面和后面的兄弟节点的生成器。


# 4)提取信息
# 关联元素节点的选择方法，想要获取它们的一些信息，如文本、属性等
html = """
<html>
<body>
<p class="story">
            Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Bob</a><a href="http://example.com/lacie"
class ="sister" id="link2">Lacie</a>
</p>
"""
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, 'lxml')
print('Next Sibling:')
print(type(soup.a.next_sibling))
print(soup.a.next_sibling)
print(soup.a.next_sibling.string)
print('Parent:')
print(type(soup.a.parents))
print(list(soup.a.parent)[0])
print(list(soup.a.parents)[0].attrs['class'])
# 直接调用string、attrs属性获得其文本和属性；返回结果是多个节点的生成器，可以转为列表后取出某个元素
# 再调用string、attrs等属性获取其对应节点的文本和属性
# 返回结果是单个节点，直接调用string、attrs等属性获得文本和属性；
# 返回结果是多个节点，可以转为列表后取出某个元素，在调用string、attrs属性获取对应节点的文本和属性。

