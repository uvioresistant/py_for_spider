# 介绍简单项目，完成一遍Scrapy抓取流程
# 1.目标：创建Scrapy项目、创建Spider抓取站点和处理数据、通过命令行将抓取内容导出、将抓取的内容保存到MongoDB数据库

# 2.准备:安装Scrapy框架、MongoDB和PyMongo库

# 3.创建项目：项目文件用scrapy命令生成：
scrapy startproject tutorial
# 命令可在任意文件夹运行，提示权限问题，加sudo运行，会创建一个名为tutorial文件夹，文件夹结构：
# scrapy.cfg        # Scrapy部署时的配置文件
# tutorial          # 项目的模块，需要从这里引入
# __init__.py
# items.py          # Items定义，定义爬取的数据结构
# middlewares.py    # Middlewares定义，定义爬取时的中间件
# pipelines.py      # Pipelines定义，定义数据管道
# settings.py       # 配置文件
# spiders           # 放置Spiders的文件夹
# __init.py

# 4.创建Spider:Spider是自定义类，Scrapy用它来从网页里抓取内容，解析抓取的结果。该类必须继承Scrapy提供的Spider类scrapy.Spider
# 还要定义Spider的名称和起始请求，以及怎样处理爬取后的结果的方法
# 也可用命令行创建一个Spider，如生成Quotes这个Spider，执行命令：
cd tutorial
scrapy genspider quotes quotes.toscrape.com # 第一个参数是Spider的名称，第二参数是网站域名
# 进入刚创建的tutorial文件夹，然后执行genspider命令，执行完毕后，spiders文件夹中多了一个quotes.py,就是刚创建的Spider:
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes" # name是每个项目唯一的名字，用来区分不同的Spider
    allowed_domains = ["quotes.toscrape.com"]   # 允许爬取的域名，如初始或后续的请求链接不是这个域名下的，则请求链接被过滤掉
    start_urls = ['http://quotes.toscrape.com/']    # 包含Spider在启动时爬取的url列表，初始请求是由它来定义的

    def parse(self, response):  # parse是Spider的方法，默认情况下，被调用时start_urls里面的链接构成的请求完成下载后，返回的
        # 响应就会作为唯一的参数传递给这个函数。该方法负责解析返回的响应、提取数据或者进一步生成要处理的请求
        pass

# 5.创建Item：Item是保存爬取数据的容器，使用方法和字典类似。相比字典，Item多了额外的保护机制，可以避免拼写错误或定义字段错误
# 创建Item需继承scrapy.Item类，且定义类型为scrapy.Field字段。观察目标网站，可获取到的内容有text、aauthor、tags
# 定义Item，将items.py修改为:
import scrapy

class QuoteItem(scrapy.Item):

    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
# 定义了三个字段，爬取时会使用到此Item

# 6.解析Response:parse方法的参数response是start_urls里的链接爬取后的结果，在parse方法中，可直接对response变量包含的内容解析，
# 如浏览请求结果或进一步分析源代码内容，或找出结果中的链接而得到下一个请求
# 可看到网页中既有想要的结果，又有下一页的链接，两部分内容都要进行处理
# 首先看网页结构，每一页都有多个class为quote的区块，每个区块都包含text、author、tags，先找出所有quote，然后提取每个quote的内容
# 提取方式可以是CSS选择器或XPath选择器。此处选择CSS选择器，parse方法改写如下：
def parse(self, response):
    qutoes = response.css('.quote') # 利用选择器选取所有quote，并将其赋值为quotes变量
    for quote in quotes:    # 利用for循环对每个quote遍历，解析每个quote内容
        text = qutoe.css('.text::text').extract_first() # 用.text选择器来选取，结果实际是带有标签的节点，获取正文可加::text
                                                        # 结果是长度为1的列表，还需用extract_first方法获取第一个元素
        author = quote.css('.author::text').extract_first()
        tags = quote.css('.tags.tag::text').extract()   # 对于tags来说，要获取所有标签，用extract方法获取整个列表即可

# 以第一个quote结果为例，各个选择方法及结果说明如下，源码如下：
<div class="quote" itemscope="" itemtype="http://schema.org/CreativeWork">
<span class="text" itemprop="text">“The world as we have created it is a process of our thinking. It cannot
    be changed without changing our thinking.”</span>
<span>by <small class="author" itemprop="author">ALbert Einstein</small>
<a href="/author/Albert-Einstenin">(about)</a>
</span>
<div class="tags">
            Tags:
<meta class="keywords" itemprop="keywords" content="change,deep=thoughts,thinking,world">
<a class="tag" href="/tag/change/page/1/">change</a>
<a class="tag" href="/tag/deep-thoughts/page/1/">deep-thoughts</a>
<a class="tag" href="/tag/thingking/page/1/">thinking</a>
<a class="tag" href="/tag/world/page/1">world</a>
</div>
</div>

# 不同选择器返回结果：
# quote.css('.text')
# [<Selector xpath="descendant-or-self::*[@class and contains(concat(' ', normalize-space(@class),' '),' text ')]"
# data='<span class="text" itemprop="text">“The '>]

# quote.css('.text::text')
# [<Selector xpath="descendant-or-self::*'@class and contains(concat(' ', normalize-space(@class),' '),'text')]/text()"
# data='"The world as we have created it is a pr'>]

# quote.css('.text').extract()
# ['<span class="text" itemprop="text">“The world as we have created it is a process of our thinking. It cannot be
# changed without changing our thinking.”</span>']

# quote.css('.text::text').extract()
#['"The world as we have created it is a process of our thinking. It connot be changed without changing our thinging."']

# quote.css('.text::text').extract_first()
# "The world as we have created it is a process of our thinking.It cannot be changed without changing our thinking."
# 对于text，获取结果的第一个元素即可，使用extract_first方法
# 对于tags，获取所有结果组成的列表，使用extract方法

# 7.使用Item:Item可理解为一个字典，在声明时需要实例化，依次用刚才解析的结果赋值Item的每一个字段，最后将Item返回
# QuotesSpider改写：
import scrapy
from tutorial.items import QuoteItem

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            item = QuoteItem()
            item['text'] = quote.css('.text::text').extract_first()
            item['author'] = quote.css('.authour::text').extract_first()
            item['tags'] = quote.scc('.tags .tag::text').extract()
            yield item
# 首页得到所有内容被解析出来，并被赋值成了一个个QuoteItem

# 8.后续Request：需要从当前页面中找到信息来生成下一个请求，然后在下一个请求的页面里找到信息再构造下一个请求。循环迭代，整站爬取
# 将页面拉到最底部，有一个Next按钮。查看源代码，发现链接是/page/2/，全链接是http://quotes.toscrape.com/page/2，构造下个请求
# 构造请求时需用到scrapy.Request。传递两个参数url和callback
# url:请求链接
# callback:回调函数。指定回调函数的请求完成后，获取响应，引擎会将该响应作为参数传递给这个回调函数。回调函数进行解析或生成下一个
# 请求，回调函数如parse所示
# parse就是解析text、author、tags的方法，下一页的结构和解析过的页面结构一样，所以可以再次使用parse方法做页面解析

# 接下来利用选择器得到下一页链接并生成请求，在parse方法后追加代码：
next = response.css('.pager .next a::attr(href)').extract_first()   # 通过CSS选择器获取下个页面的链接，获取a链接中href属性，
                                                                    # 用到了::attr(href)操作，再调用extract_first方法获取
url = response.urljoin(next)    # 调用urljoin方法，可以相对于URL构造成一个绝对的URL
yield scrapy.Request(url=url, callback=self.parse)  # 调用url和callback构造一个新的请求，callback使用parse方法
# 请求完成后，响应会重新经过parse方法处理，得到第二页的解析结果，然后生成第二页的下一页，即第三页的请求，爬虫进入循环，直到最后
# 改写后整个Spider类：
import scrapy
from tutorial.items import QuoteItem

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.css('.uote')
        for quote in quotes:
            item = QuoteItem()
            item['text'] = quote.css('.text::text').extract_first()
            item['author'] = quote.css('.author::text').extract_first()
            item['tags'] = quote.css('.tags .tag::text').extract()
            yield item

        next = response.css('.pager .next a:attr("href")').extract_first()
        url = response.urljoin(next)
        yield scrapy.Request(url=url, callback=self.parse)

# 9.运行：进入目录，运行命令：scrapy crawl quotes
# 运行结果：首先，Scrapy输出了当前所应用的Middlewares和Pipelines。Middlewares默认启用，可以在settings.py中修改。
# Pipelines默认是空，也可以在settings.py中配置。
# 接下来抓取各个页面的抓取结果，可以看到爬虫一遍解析，一遍翻页，直至将所有内容抓取完毕，然后终止。
# 最后，Scrapy输出整个抓取过程的统计信息，如请求的字节数、请求次数、响应次数、完成原因

# 10.保存到文件：运行完Scrapy，只在控制台看到输出结果，想保存不需额外任何代码，Scrapy提供 Feed Exports将抓取结果输出
# 想将结果保存成JSON文件，执行命令：
scrapy crawl quotes -o quotes.json
# 运行后，项目内多了一个quotes.json文件，文件包含了刚才抓取的所有内容，JSON格式
# 还可以每一个Item输出一行JSON，输出后缀为jl，为jsonline的缩写，命令：
# scrapy crawl quotes -o quotes.jsonlines
# 输出格式还支持csv、xml、pickle、marshal，还支持ftp、s3等远程输出，还可自定义ItemExporter来实现其他的输出
scrapy crawl quotes -o quotes.csv
scrapy crawl quotes -o quotes.xml
scrapy crawl quotes -o quotes.pickle
scrapy crawl quotes -o quotes.marshal
scrapy crawl quotes -o ftp://user:pass@ftp.example.com/path/to/quotes.csv   # ftp需要正确配置用户名、密码、地址、输出路径
# Scrapy提供的Feed Exports，可以轻松地输出抓取结果到文件。对小型项目足够了，输出到数据库，可使用Item Pileline完成

# 11.使用Item Pipeline：项目管道，当Itme生成后，会自动送到Item Pipeline进行处理，常用Item Pipeline做如下操作：
# 清理HTML数据
# 验证爬取数据，检测爬取字段
# 查重并丢弃重复内容
# 将爬取结果保存到数据库
# 实现Item Pipeline，只需定义一个类并实现process_item方法即可。
# 启用Item Pipeline后，Item Pipeline会自动调用此方法，process_item方法必须返回包含数据的字典或Item对象，或抛出DropItem异常
# process_item方法有两个参数：item：每次Spider生成的Item都会作为参数传递过来；spider：就是Spider的实例

# 实现一个Item Pipeline，筛掉text长度大于50的Item，并将结果保存到MongoDB：
# 修改项目里的Pipelines.py文件，用命令行自动生成的文件内容可以删掉，增加一个TextPipeline类：
from scrapy.exceptions import DropItem

class TextPipeline(object):
    def __init__(self):     # 构造方法里定义了限制长度为50
        self.limit = 50

    def process_item(self, item, spiider):  # 实现process_item方法，参数是item和spider
        if item['text']:    # 判断item的text属性是否存在
            if len(item['text']) > self.limit:  # 如果存在，在判断长度是否大于50，
                item['text'] = item['text'][0:self.limit].rstrip() + '...'  # 如果大于，截断然后拼接省略号
            return item     # 将item返回
        else:
            return DropItem('Missing Text') # 如果不存在，抛出DropItem异常

# 将处理后的item存入MongoDB，定义另外一个Pipeline，在Pipeline.py中，实现另一类MongoPipeline：
import pymongo

class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler): # 类方法，用@classmethod标识，是一种依赖注入方式。参数是crawler，通过crawler拿到配置信息
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),# 定义MONGO_URI指定MongoDB连接需要的地址
            mongo_db=crawler.settings.get('MONGO_DB')   # 定义MONGO_DB指定MongoDB连接需要的数据库名称
    )   # 拿到配置信息后返回类对象，定义主要是用来获取settings.py中的配置

def open_spider(self, spider):  # Spider开启，方法被调用，进行一些初始化操作
    self.client = pymongo.MongoClient(self.mongo_uri)
    self.db = self.client[self.mongo_db]

def process_item(self, item, spider):
    name = item.__class__.__name__
    self.db[name].insert(dict(item))
    return item

def close_spider(self, spider): # Spider关闭，将数据库连接关闭
    self.client.close()

# 定义好TextPipeline和MongoPipeline两个类后，需要再settings.py中使用。MongoDB连接信息还需要定义
# 在settings.py中加入
 ITEM_PIPELINES = {  # 赋值ITME_PIPELINES字典，
    'tutorial.pipelines.TextPipeline': 300, # 键名Pipeline的类名称，键值是调用优先级，是一个数字，数字越小对应Pipeline先调用
    'tutorial.pipelines.MongoPipeline': 400,
    }
MONGO_URI='localhost'
MONGO_DB='tutorial'
# 重新执行爬取，命令：
scrapy crawl quotes
# 爬取结束后，MongoDB中创建了一个tutorial数据库、QuoteItem的表，长的text已经被处理并追加省略号，短的text保持不变
# 代码地址：https://github.com/Python3WebSpider/ScrapyTutorial
