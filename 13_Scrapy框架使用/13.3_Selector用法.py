# 可利用Beautiful Soup、pyquery及正则表达式来提取网页数据
# Scrapy提供了自己的数据提取方法：Selector(选择器).基于lxml构建，支持XPath选择器、CSS选择器就正则，解析速度和准确度非常高
# 1.直接使用：独立模块，可直接利用Selector类构建一个选择器对象，调用相关方法如xpath、css来提取数据
# 针对一段HTML，用如下方式狗结案Selector对象提取数据：
from scrapy import Selector

body = '<html><head><title>Hello World</title></head><body></body></html>'
selector = Selector(text=body)
title = selector.xpath('//title/text()').extract_first()    # 查找title中的文本，XPath选择器最后加text方法发可实现文本提取
print(title)
# 没有在Scrapy框架中运行，把Scrapy中的Selector单独拿出来使用，构建时传入text参数，生成了Selector选择器对象，像Scrapy中的解析
# 方式一样，调用xpath、css方法来提取。

# 2.Scrapy shell:Selector主要与Scrapy结合使用，Scrapy的回调函数中response直接调用xpath或者css方法提取数据，
# 所以借助Scrapy shell模拟Scrapy请求过程，理解相关提取方法
# 用官方文档样例页面：http://doc.scrapy.org/en/latest/_static/selectors-sample1.html
# 开启Srapy shell,命令行输入：
scrapy shell http://doc.scrapy.org/en/latest/_static/selectors-sample1.html
# 进入到Scrapy shell模式。过程是，Scrapy发起一次请求，请求的URL是命令行下输入的URL，把可操作的变量request、response传递给我
# 可在命令行模式下输入命令调用对象的一些操作方法，回车后实时显示结果。
# 演示实例都将页面的源码作为分析目标，源码：
<html>
<head>
<base href='http://example.com/' />
<title>Example website</title>
</head>
<body>
<div id = 'images'>
<a href='imgae1.html'>Name: My image 1 <br /><img src='image1_thumb.jpg' /></a>
<a href='imgae1.html'>Name: My image 2 <br /><img src='image2_thumb.jpg' /></a>
<a href='imgae1.html'>Name: My image 3 <br /><img src='image3_thumb.jpg' /></a>
<a href='imgae1.html'>Name: My image 4 <br /><img src='image4_thumb.jpg' /></a>
<a href='imgae1.html'>Name: My image 5 <br /><img src='image5_thumb.jpg' /></a>
</div>
</body>
</html>

# 3.XPath选择器：进入Sccrapy shell后，主要操作response变量来解析。解析HTML，Selector自动使用HTML语法分析
# response有属性selector，调用response.selector返回的内容相当于用response的body构造了一个Selector对象。
# 通过Selector对象可以调用解析方法xpath、css等，通过向方法传入XPath或CSS选择器参数可实现信息的提取
# 实例：
result = response.selector.xpath('//a')
result
[<Selector xpath='//a' data='<a href="image1.html">Name: My image 1 <'>,
<Selector xpath='//a' data='<a href="image1.html">Name: My image 2 <'>,
<Selector xpath='//a' data='<a href="image1.html">Name: My image 3 <'>,
<Selector xpath='//a' data='<a href="image1.html">Name: My image 4 <'>,
<Selector xpath='//a' data='<a href="image1.html">Name: My image 5 <'>]
    type(result)
scrapy.selector.unified.SelectorList    # 打印结果形式是Selector组成的列表，是SelectorList类型，SelectorList和Selector都
# 可以继续调用xpath和css方法来进一步提取数据，提取了a节点
# 尝试继续调用xpath方法提取a节点内包含的img节点：
result.xpath('./img')   # 选择器最前方加.，代表提取元素内部的数据，没有加点，代表从根节点开始提取，./img代表从a节点里进行提取
[<Selector xpath='./img' data='<img src="image1_thumb.jpg">'>,
<Selector xpath='./img' data='<img src="image2_thumb.jpg">'>,
<Selector xpath='./img' data='<img src="image3_thumb.jpg">'>,
<Selector xpath='./img' data='<img src="image4_thumb.jpg">'>,
<Selector xpath='./img' data='<img src="image5_thumb.jpg">'>]
# 获得a节点里所有img节点，结果为5
# Scrapy提供两个可直接调用快捷方法，response.xpath和response.css功能等同于response.selector.xpath和response.selector.css
# 得到的是SelectorList类型变量，该变量由Selector对象组成的列表。可用索引单独取出其中某个Selector元素：
result[0]
<Selector xpath='//a' data='<a href="image1.html">Name: My image 1<'>,
# 可像操作列表一样操作这个SelectorList，现在获取的内容是Selector或SelectorList类型，并不是真正的文本内容，提取方式：
# 想提取a节点元素，利用extract方法：
result.extract()    # 使用extract方法，可以把真实需要的内容获取下来
['<a href='imgae1.html'>Name: My image 2 <br /><img src='image2_thumb.jpg' /></a>',
'<a href='imgae1.html'>Name: My image 3 <br /><img src='image3_thumb.jpg' /></a>',
'<a href='imgae1.html'>Name: My image 4 <br /><img src='image4_thumb.jpg' /></a>',
'<a href='imgae1.html'>Name: My image 5 <br /><img src='image5_thumb.jpg' /></a>']
# 还可改写XPaht，选取节点的内部文本和属性：
response.xpath('//a/text()').extract()  # 只需加一层/text就可以获取节点内部文本
['Name: My image 1 ', 'Name: My image 2', 'Name: My image 3 ', 'Name: My image 4 ', 'Name: My image 5 ']
response.xpath('//a/@href').extract()   # 加一层/@href就可以获取节点href属性，@符号后面内容是要获取的属性名称
['image1.html', 'image2.html', 'image3.html', 'image4.html', 'image5.html']

# 专门提取单个元素extract_first：
response.xpath('//a[@href="image1.html"]/text()').extract_first()   # 将匹配的第一个结果提取出来，不用担心数组越界问题
'Name: My image 1 '
# response.xpath('//a[@href="image1"]/text()').extract_first('Default Image') # 传递默认参数，如果XPath匹配不到，默认代替


# 4.CSS选择器：response.css方法可以使用CSS选择器来选择对应的元素
response.css('a')
[<Selector xpath='descendant-or-self::a' data='<a href="image1.html">Name: My image 1 <'>,
<Selector xpath='descendant-or-self::a' data='<a href="image2.html">Name: My image 2 <'>,
<Selector xpath='descendant-or-self::a' data='<a href="image3.html">Name: My image 3 <'>,
<Selector xpath='descendant-or-self::a' data='<a href="image4.html">Name: My image 4 <'>,
<Selector xpath='descendant-or-self::a' data='<a href="image5.html">Name: My image 5 <'>]
# 调用extract方法可提取出节点：
response.css('a').extract()
[<Selector xpath='descendant-or-self::a' data='<a href="image1.html">Name: My image 1 <'>,
<Selector xpath='descendant-or-self::a' data='<a href="image2.html">Name: My image 2 <'>,
<Selector xpath='descendant-or-self::a' data='<a href="image3.html">Name: My image 3 <'>,
<Selector xpath='descendant-or-self::a' data='<a href="image4.html">Name: My image 4 <'>,
<Selector xpath='descendant-or-self::a' data='<a href="image5.html">Name: My image 5 <'>]
# 用法和XPath选择完全一样，也可进行属性选择和嵌套选择:
response.css('a[href="image1.html"]').extract()
['<a href="image1.html">Name: My image 1 <br><img src="image1_thumb.jpg"></a>'] # 用[href="image.html"]限定href属性
response.cee('a[href="image1.html"] img').extract() # 想查找a节点的img节点，只需加一个空格和img即可
['<img src="image1_thumb.jpg">']
# 也可使用extract_first提取列表的第一个元素：
response.css('a[href="image1.html"] img').extract_first()
'<img src="image1_thumb.jpg">'
# 节点内部文本和属性的获取:
response.css('a[href="image1.html"]::text').extract_first() # 获取文本需要::text写法
'Name: My image 1'
response.css('a[href="image1.html"] img::attr(src)').extract_first()    # 获取文本需要::attr写法
'image1_thumb.jpg'
# 嵌套选择：可先用XPath选择器选中所有a节点，再利用CSS选择器选中img节点，再用XPath选择器获取属性:
response.xpath('//a').css('img').xpath('@src').extract()
['image1_thumb.jpg', 'image2_thumb.jpg', 'image3_thumb.jpg', 'image4_thumb.jpg', 'image5_thumb.jpg'] # 获取所有img节点src
# 可以随意使用xpath和ccss方法二者自由结合实现嵌套查询，二者完全兼容

# 5.正则匹配:
# re方法提取出Name: My image 1 中Name:后面的内容
response.xpath('//a/text()').re('Name:\s(.*)')
['My image 1 ', 'My image 2 ', 'My image 3 ', 'My image 4 ', 'My image 5 ']# (.*)就是要匹配的内容，输出结果是正则分组
# 同时存在两个分组，结果依然按序输出:
response.xpath('//a/text()').re('(.*?):/s(.*)')
['Name', 'My image 1 ','Name', 'My image 2 ','Name', 'My image 3 ','Name', 'My image 4 ','Name', 'My image 5 ']
# 类似extract_first，re_first方法可选取列表的第一个元素:
response.xpath('//a/text()').re_first('(.*?):/s(.*)')
'Name'
response.xpath('//a/text()').re_first('Name:\s(.*)')
'My image 1 '
# response对象不能直接调用re和re_first方法,想要对全文进行正则匹配，可先调用xpath方法再正则匹配:
response.re('Name:\s(.*)')  # 直接调用re方法会提示没有re属性
    Traceback ...
response.xpaht('.').re('Name:\s(.*)<br>')   # 先调用了xpath('.')选中全文，然后调用re和re_first方法，就可进行正则匹配了
['image1_thumb.jpg', 'image2_thumb.jpg', 'image3_thumb.jpg', 'image4_thumb.jpg', 'image5_thumb.jpg']
response.xpath('.').re_first('Name:\s(.*)<br>')
'My image 1 '