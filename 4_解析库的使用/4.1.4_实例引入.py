from lxml import etree
text = '''
<div>
<ul>
<li class="item-0"><a href="link1.html">first item</a></li>
<li class="item-1"><a href="link2.html">second item</a></li>
<li class="item-inactive"><a href="link3.html">third item</a></li>
<li class="item-1"><a href="link4.html">fourth item</a></li>
<li class="item-0"><a href="link5.html">fifth item</a>
</ul>
</div>
'''
# html = etree.HTML(text)
# result = etree.tostring(html)
# print(result.decode('utf-8'))

# 首先导入lxml库的etree模块；
# 声明一段HTML文本，调用HTML类进行初始化，构造了一个XPath解析对象，etree模块可以自动修正HTMl文本
# 调用tostring方法输出修正后的HTML代码，结果为bytes类
# 利用decode方法转化为str类


# 也可直接读取文本文件进行解析：
# from lxml import etree

html = etree.parse('./test.html', etree.HTMLParser())
result = etree.tostring(html)
print(result.decode('utf-8'))
