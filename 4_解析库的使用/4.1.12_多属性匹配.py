# 根据多个属性确定一个节点，需要同时匹配多个属性，用运算符and来连接
from lxml import etree
text = '''
<li class="li li-first" name="item"><a href = "link.html">first item</a></li>
'''
html = etree.HTML(text)
result = html.xpath('//li[contains(@class, "li") and @name="item"]/a/text()')
print(result)
# li节点增加属性name，要确定整这个节点，需要同时根据class和name属性来选择
# 一个条件是class属性里面包含li字符串；另一个条件是name属性为item字符串，两种用and相连，置于中括号内进行条件筛选
# 运算符参考来源：http://www.w3school.com.cn/xpath/xpath_operators.asp