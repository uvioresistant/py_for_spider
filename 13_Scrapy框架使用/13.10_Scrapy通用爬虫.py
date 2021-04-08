# 通过Scrapy，可轻松完成一个站点爬虫的编写，但如果抓取的站点量非常大，如爬取各大媒体的新闻信息，多个Spider可能包含很多重复代码
# 如果将各个站点的Spider的公共部分保留下来，不同的部分提取出来作为单独的配置，如爬取规则，页面解析方式等抽离出来
# 做成一个配置文件，那么我们在新增一个爬虫的时候，只需要实现这些网站的爬取规则和提取规则即可

# 1.CrawlSpider：官方文档：http://scrapy.redthedocs.io/en/lates/topics/spiders.html#crawlspider
# CrawlerSpider是Scrapy提供的一个通用Spider。
# 在Spider里，可指定一些爬取规则来实现页面的提取，爬取规则由一个专门的数据结构Rule表示。
# Rule里包含提取和跟进页面的配置，Spider会根据Rule来确定当前页面汇总的那些链接需要继续爬取、那些页面的爬取结果需用哪个方法解析
# CrawlSpider继承自Spider类。除了Spider类的所有方法和属性，还提供了一个非常重要的属性和方法：
# rules：是爬取规则属性，是包含一个或多个Rule对象的列表。每个Rule对爬取网站网站的动作都做了定义，CrawlSpider会读取rules的
# 每一个Rule并进行解析
# parse_start_url：是可重写的方法，当start_urls里对应的Request得到Response时，该方法被调用，分析Response并返回Item或Request
# 最重要的内容是Rule的定义：
class scrapy.contrib.spider.Rule(link_extractor, callback=None, cb_kwargs=None, follow=None,
    process_links=None, process_request=None)
# Rule的参数：
# link_extractor：Link Extractor对象。通过它，Spider可以知道从爬取的页面中提取哪些链接。提取出的链接会自动生成Request，又是
# 一个数据结构，一般常用LxmlLinkExtractor对象作为参数，定义和参数：
# class scrapy.linkextractors.lxmlhtml.LxmlLinkExtractor(allow=(), deny=(), allow_domains=(),deny_domains=(),
#     deny_domains=(), deny_extensions=None, restrict_xpaths=(), restrict_css=(), tags=('a', 'area'),
#     attrs=('href', ), canonicalize=False, unique=True, process_value=None, strip=True)
# allow是一个正则表达式或正则表达式列表，定义了从当前页面提取出的链接哪些是符合要求的，只有符合的链接才会被跟进
# deny相反
# allow_domains定义了符合要求的域名，只有此域名的链接才会被跟进生成新的Request，相当于域名白名单
# deny_domains相反，域名黑名单
# restrict_xpaths定义了从当前页面中XPath匹配的区域提取链接，值是XPath表达式或XPath表达式列表
# restrict_css定义了从当前页面中CSS选择器匹配的区域提取链接，值是CSS选择器或列表
# 其他参数代表提取链接的标签、是否去重、链接的处理等内容，使用频率不高
# 参考参数说明：http://scrapy.readthedocs.io/en/latest/topics/link-extractors.html#module-scrapy.linkextractors.lxmlhtml

# callback：回调函数，和Request的callback相同意义，每次从link_extractor中获取到链接时，该函数会调用。
# 该回调函数接收一个response作为其第一个参数，返回一个包含Item或Request对象的列表。避免使用parse作为回调函数
# 由于CrawlSpider使用parse方法来实现逻辑，如果parse方法覆盖了，CrawlSpider将会运行失败

# cb_kwargs：字典，包含传递给回调函数的参数

# follow：布尔值，True或False，指定根据该规则从response提取的链接是否需要跟进。callback为None，follow默认为True，否则False

# process_links:指定处理函数，从link_extractor中获取到链接列表时，该函数将会调用，用于过滤

# process_request：指定处理函数，根据该Rule提取每个Request时，该函数都会调用，对Request进行处理。必须返回Request或None
# CrawlSpider中的核心Rule的基本用法，但还不足以完成一个CrawlSpider爬虫
# 利用CrawlSpider实现新闻网站的爬取：

# 2.Item Loader：Rule没有对Item的提取方式做规则定义。对于Item的提取，需要借助另一个模块Item Loader来实现
# Item Loader提供便捷的机制来方便地提取Item。提供的一系列API可以分析原始数据对Item进行赋值。Item提供保存抓取数据的容器，
# Item Loader提供填充容器的机制，数据的提取会变得更加规则化。
# Item Loader的API：
# class scrapy.loader.ItemLoader([item, selector, response, ] **kwargs)
# Item Loader的API返回一个新的Item Loader来填充给定的Item。如果没有给出Item，则使用中的类，自动实例化default_item_class,
# 它传入selector和response参数来使用选择器或相应参数实例化。
# 依次说明Item Loader的API参数：
# item：是Item对象，可以调用add_xpath、add_css、add_value等方法来填充Item对象
# selector：是Selector对象，用来提取填充数据的选择器
# response：是Response对象，用于使用构造选择器的Response
# 典型的Item Loader：
from scrapy.loader import ItemLoader
from project.items import Product

def parse(self, response):  # 首先声明一个Product Item，
    loader = ItemLoader(item=Product(), response=response)  # 用该Item和Response对象实例化ItemLoader
    loader.add_xpath('name', '//div[@class="product_name"]')    # 调用add_xpath把两个不同位置的数据提取出来，分配给name属性
    loader.add_xpath('name', '//div[@class="product_title"]')   # 再用add_xpath
    loader.add_xpath('name', '//div[@class="price"]')
    loader.add_css('stock', 'p#stock]') # add_css
    loader.add_value('last_updated', 'today')   # add_value方法对不同属性依次赋值
    return loader.load_item()   #最后调用load_item方法实现Item的解析
# 这种方法比较规则化，可以把一些参数和规则单独提取出来做成配置文件后存到数据库，可实现可配置化
# Item Loader每个字段都包含了一个Input Processor(输入处理器)和一个Ouput Processor(输出处理器).
# Input Processor收到数据立刻提取数据，结果被收集起来冰球保存在ItemLoader内，但不分配给Item
# 收集到所有数据后，load_item被调用来填充再生成Item对象。调用时会先调用Output Processor来处理之前收集到的数据
# 再存入Item中，这样就生成了Item
# 内置的Processor：

# Identity：最简单的Processor，不进行任何处理，直接返回原来的数据

# TakeFirst：返回列表的第一个非空值，类似extract_first功能，常用作Output Processor：
from scrapy.loader.processors import TakeFirst
processor = TakeFirst()
print(processor(['', 1, 2, 3])) # 经过此Processor处理后的结果返回了第一个不为空的值

# Join：相当于字符串的join方法，可把列表拼合成字符串，字符串默认用空格分隔：
from scrapy.loader.processors import Join
processor = Join()
print(processor(['one', 'two', 'three']))
# 也可以通过参数更改默认的分隔符，如改为逗号：
from scrapy.loader.processors import Join
processor = Join(',')
print(processor(['one', 'two', 'three']))

# Compose:用给定的多个函数的组合而构造的Processer，每个输入值被传递到第一个函数，输出在传递到第二个函数，直到
# 最后一个函数返回整个处理器的输出
from scrapy.loader.processors import Compose
processor = Compose(str.upper, lambda s: s.strip()) # 构造一个Compose Processor，传入一个开头带有空格的字符串
    # Compose Processer参数有两个:第一个是str.upper，可将字母全部转成大写；第二个是匿名函数，调用strip方法去除头尾空白字符、
    # Compose顺次调用两个参数
print(processor(' hello world'))    # 最后返回结果的字符串全部转化为大写并且去除了开头的空格

# MapCompose：与Compose类似，MapCompose可迭代处理一个列表输入值
from scrapy.loader.processors import MapCompose
processor = MapCompose(str.upper, lambda s: s.strip())  # 被处理内容是一个可迭代对象，MapCompose会将该对象遍历，依次处理
print(processor(['Hello', 'World', 'Python']))

# SelectJmes：可查询JSON，传入Key，返回查询所得的Value。需先安装jmespath库，命令：
# pip3 install jmespath
# 安装好jmespath后，便可以使用Processor了：
from scrapy.loader.processors import SelectJmes
proc = SelectJmes('foo')
processor = SelectJmes('foo')
print(processor({'foo': 'bar'}))

# 3.目标：抓取中华网科技类新闻，了解CrawlSpider和Item Loader的用法，再提取可配置信息实现可配置化。
# 官网链接：http://tech.china.com/需爬取它的科技类新闻内容，链接http://tech.china.com/articles/
# 抓取新闻列表中所有分页的新闻详情，包括标题、正文、时间、来源等信息

# 4.新建项目:名为scrapyuniversal
# scrapy startproject scrapyuniversal
# 创建一个CrawlSpider，需先制定一个模板。可先看看有哪些可用模板，命令：
Available templates：
    basic   # 创建Spider时，默认使用第一个模板basic
    crawl
    csvfeed
    xmlfeed
# 要创建CrawlSpider，需要使用第二个模板crawl，命令：
scrapy genspider -t crawl china tech.china.com
# 运行后会生成一个CrawlSpider：
from scrapy.linkextractors import LinkExeractor
from scrapy.spiders import CrawlSpider, Rule

class ChinaSpider(CrawlSpider):
    name = 'china'
    allowed_domains = ['tech.china.com']
    start_urls = ['http://tech.china.com/']

    rules = (   # 此次生成的Spider内容多了一个rules属性的定义
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),   # Rule的第一个参数是LinkExtractor
    )   # 即LxmlLinkExtractor，只是名称不同。
    def parse_item(self, response): # 同时，默认的回调函数也不再是parse，而是parse_item
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]'.extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i

# 5.定义Rule：要实现新闻的爬取，需要做的就是定义好Rule，实现解析函数
# 首先将start_urls修改为起始链接：
start_urls = ['http://tech..china.com/articles/']   # Spider爬取start_urls里面的每一个链接。
# 第一个爬取的页面就是刚才定义的链接。得到Response后，Spider就会根据每一个Rule来提取这个页面内的超链接，去生成进一步的Request
# 接下来，需要定义Rule来指定提取哪些链接
# 新闻列表页，下一步将列表中的每条新闻详情的链接提取出来。直接指定这些链接所在区域即可。查看源代码，所有链接都在ID为left_side里
# 具体来说是它内部的class为con_item的节点
# 此处可用LinkExtractor的restrict_xpaths属性来指定，Spider就会从这个区域提取所有的超链接并生成Request。
# 但每篇文章的导航中还有一些其他的超链接标签，指向吧需要的新闻链接提取出来。
# 真正的新闻链接路径都是以article开头，用一个正则表达式将其匹配出来在赋值给allow参数即可
# 另外，这些链接对应的页面其实就是对应的新闻详情页，需要解析的就是新闻的详情信息，此处还需要指定一个回调函数callback
# 可构造出一个Rule：
Rule(LinkExeractor(allow='article/\.*\.html', restrict_xpaths='//div[@id="left_side"]//div[@class="con_item"]'),
                                                              callback='parse_item')
# 接下来，还要让当前页面实现分页功能，所以还需提取下一页的链接。分析网页源码后，可以发现下一页链接时在ID为pageStyle的节点内
# 但，下一页节点和其他分页链接区分度不高，要取出此链接，可以直接用XPath的文本匹配方式，直接用LinkExtractor的restrict_xpaths
# 来指定提取的链接即可。
# 另，不需要像新闻详情页一样去提取此分页链接对应的页面详情信息，即不需要生成Item，所以不需加callback参数。
# 另外，下一页的页面如果请求成功了就需要继续像上述情况一样分析，还需加一个follow参数为True，代表继续跟进匹配分析
# follow参数也可以不加，当callback为空时，follow默认为True，此处Rule定义：
Rule(LinkExeractor(restrict_xpath='//div[@id="pageStyle"]//a[contains(., "下一页")]'))
# 所以，现在下一页就变成了：
rules = (
    Rule(LinkExeractor(allow='article/\.*/.html',
                       restrict_xpaths='//div[@id="left_side"]//div[@class="con_item"]'), callback='parse_item'),
    Rule(LinkExeractor(restrict_xpahts='//div[@id="pageStyle"]//a[contains(., "下一页")]'))
)
# 运行代码，命令：
scrapy crawl china
# 已经是吸纳页面的翻页和详情页的抓取了，仅仅通过定义了两个Rule即实现了这样的功能

# 6.解析页面：将标题、发布时间、正文、来源提取出来即可。
# 首先定义一个Item：
from scrapy import Field, Item

class NewsItem(Item):   # 字段分别指
    title = Field() # 新闻标题
    url = Field()   # 链接
    text = Field()  # 正文
    datetime = Field()  # 发布时间
    source = Field()    # 来源
    website = Field()   # 站点名称，直接赋值为中华网
# 既然通用爬虫，肯定还有很多爬虫也来爬取同样结构的其他站点的新闻内容，所以需要一个字段来区分一下站点名称
# 提取内容，直接调用response变量的xpath、css方法即可。parse_item方法的实现：
def parse_item(self, response):
    item = NewsItem()   # 把每条新闻的信息提取形成了一个NewsItem对象
    item['title'] = response.xpath('//h1[@id="chan_newsTitle"]/text()').extract_first()
    item['url'] = response.url
    item['text'] = ''.join(response.xpath('//div[@id="chan_newsDetail"]//text()').extract()).strip()
    item['datetime'] = response.xpath('//div[@id="chan_newsInfo"]/test()').re_first('(\d+-\d+-\d+\s\d+:\d+:\d+)')
    item['source'] = response.xpath('//div[@id="chan_newsInfo"]/text()').re_first('来源：(.*)').strip()
    item['websit'] = '中华网'
    yield item
# 完成了Item的提取，再运行一下Spider：
scrapy crawl china
# 成功将每条新闻的信息提取出来，但这种提取方式非常不规整。再用Item Loader,通过add_xpath、add_css、add_value方式实现配置化提取
# 改写parse_item：
def parse_item(self, response):
    loader = ChinaLoader(item=NewsItem(), response=response)    # 定义了一个ItemLoader的子类，名为ChinaLoader
    loader.add_xpath('title', '//h1[@id="chan_newsTitle"]/text()')
    loader.add_value('url', response.url)
    loader.add_xpath('text', '//div[@id="chan_newsDetail"]//text()')
    loader.add_xpath('datetime', '//div[@id="chan_newsInfo"]/text()', re='(\d+-\d+-\d+\s\d+:\d+:\d+)')
    loader.add_xpath('source', '//div[id="chan_newsInfo"]/text()', re='来源：(.*)')
    loader.add_value('website', '中华网')
    yield loader.load_item()
# 定义了一个ItemLoader的子类，名为ChinaLoader，实现：
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, Compose

class NewsLoader(ItemLoader):
    default_output_processor = TakeFirst()  # 其内定义了一个通用的Out Processer为TakeFirst，相当于extract_first的功能

class ChinaLoader(NewsLoader):  # ChinaLoader继承了NewsLoader类，有两个参数：
    text_out = Compose(Join(), lambda s: s.strip()) # 第一个参数Join也是Processer，可以把列表拼接合成一个字符串
    source_out = Compose(Join(), lambda s: s.strip())   # 第二个参数是一个匿名函数，可将字符串的头尾空白字符去掉
# 经过一系列处理后，就将列表形式的提取结果转化为去重头尾空白字符的字符串
# 重新运行，提取效果是完全一样的，至此，已经实现了爬虫的半通用化配置

# 7.通用配置抽取：需要扩展其他站点，仍然需要创建一个新的CrawlSpider，定义这个站点的Rule，单独实现parse_item方法。
# 还有很多代码是重复的，如CrawlSpider的变量、方法名几乎都是一样的，可以把多个类似的几个爬虫的代码公用，把完全不相同的地方抽离，
# 做成可配置文件
# 所有变量都可以抽取，如name、allowed_domains、start_urls、urles，这些变量在CrawlSpider初始化的时候赋值即可。
# 可以新建一个通用的Spider来实现这个功能，命令：
# scrapy genspider -t crawl universal universal # 全新的Spider名为universal，将刚才缩写的Spider内的属性抽离出来配置成JSON
# 命名为china.json，放到configs文件夹内，和spiders文件夹并列：
{
    "spider": "universal",  # spider即Spider名称，这里是universal
    "website": "中华网科技", # 站点描述，名称
    "type": "新闻",   # 类型
    "index": "http://tech.china.com/",  # 首页
    "settings": {   # settings是该Spider特有的settings配置，如果要覆盖全局项目，settings.py内的配置可以单独为其配置
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko)"
                      "Chrome/60.0.3112.90 Safari/537.36"
    },
    "start_urls": [ # Spider的一些属性
        "http://tech.china.com/articles/"
    ],
    "allowed_domains": [
        "tech.china.com"
    ],
    "rules": "china"
}
# rules可单独定义成一个rules.py文件，做成配置文件，实现Rule的分离：
from scrapy.linkextractor import LinkExtractor
from scrapy.spiders import Rule

rules = {   # 将基本的配置抽取出来，要启动爬虫，只需从改配置文件汇总读取然后动态加载到Spider即可
    'china': (
        Rule(LinkExtractor(allow='article/\.*\.html', restrict_xpaths='//div[@id="left_side"]//div[@class="con_item"]'),
             callback='parse_itme'),
        Rule(LinkExtractor(restrict_xpaths='//div[@id="pageStyle"]//a[contains(., "下一页")]'))
    )
}
# 定义一个读取该JSON文件的方法：
from os.path import realpath, dirname
import json
def get_config(name):
    path = dirname(realpath(__file__)) + '/configs/' + name + '.json'
    with open(path, 'r', encoding='utf-9') as f:
        return json.loads(f.read())
# 定义get_config方法后，向其传入JSON配置文件的名称，即可获取此JSON配置信息。
# 定义入口文件run.py，放在项目根目录下，作用是启动Spider：
import sys
from scrapy.utils.project import get_project_settings
from scrapyuniversal.spiders.universal import UniversalSpider
from scrapy.crawler import CrawlerProcess

def run():
    name = sys.argv[1]  # 首先获取命令行的参数并赋值为name，name就是JSON文件的名称，也是爬取目标网站的名称
    custom_settings = get_config(name)  # 利用get_config方法，传入该名称读取刚才定义的配置文件
    # 爬取使用的Spider名称、
    spider = custom_settings.get('spider', 'universal')
    project_settings = get_project_settings()   # 配置文件中的settings配置
    settings = dict(project_settings.copy())    # 将获取到的settings配置和项目全局的settings配置做了合并
    # 合并配置
    settings.update(custom_settings.get('settings'))
    process = CrawlerProcess(settings)  # 新建一个CrawlSpider，传入爬取使用的配置
    # 启动爬虫
    process.crawl(spider, **{'name': name}) # 调用crawl
    process.start() # 调用start启动爬取

if __name__ == '__main__':
    run()

# 在universal中，新建一个__init__方法，进行初始化配置：
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapyuniversal.utils import get_config
from scrapyuniversal.rules import rules

class UniversalSpider(CrawlSpider):
    name = 'universal'
    def __init__(self, name, *args, **kwargs):  # init方法中，、、
        config = get_config(name)
        self.config = config
        self.rules = rules.get(config.get('rules')) # rules属性另外读取了rules.py的配置
        self.start_urls = config.get('allowed_domains') # start_urls被赋值
        self.allowed_domains = config.get('allowed_domains')    # allowed_domains被赋值
        super(UniversalSpider, self).__init__(*args, **kwargs)

    def parse_item(self, response):
        i = {}
        return i
# 执行命令运行爬虫：
python3 run.py china
# 程序首先读取JSON配置文件，将配置中的一些属性赋值给Spider，然后启动爬取
# 已经对Spider的基础属性实现了可配置化。剩下的解析部分同样需要实现可配置化，原解析函数：
def parse_item(self, response):
    loader = ChinaLoader(item=NewsItem(), response=response)    # 定义了一个ItemLoader的子类，名为ChinaLoader
    loader.add_xpath('title', '//h1[@id="chan_newsTitle"]/text()')
    loader.add_value('url', response.url)
    loader.add_xpath('text', '//div[@id="chan_newsDetail"]//text()')
    loader.add_xpath('datetime', '//div[@id="chan_newsInfo"]/text()', re='(\d+-\d+-\d+\s\d+:\d+:\d+)')
    loader.add_xpath('source', '//div[id="chan_newsInfo"]/text()', re='来源：(.*)')
    loader.add_value('website', '中华网')
    yield loader.load_item()
# 需将这些配置也抽离出来，变量主要有Item Loader类的选用、Item类的选用、Item Loader方法参数的定义，在JSON文件中添加item配置：
"item": {
    "class": "NewsItem", # 定义class属性，代表Item所使用的类
    "loader": "ChinaLoader",    # 定义loader属性，代表Item Loader所使用的类
    "attrs": {  # 定义了attrs属性来定义每个字段的提取规则
    "title": [  # 定义的每一项都包含一个method属性，代表使用的提取方法
        {
            "method": "xpath",  # xpaht代表调用Item Loader的add_xpath方法
            "args": [   # args参数，就是add_xpath的第二个参数，XPath表达式
                "//h1[@id='chan_newsTitle']/text()"
            ]
        }
    ],
    "url": [
        {
            "method": "attr",
            "args": [
                "url"
            ]
        }
    ],
    "text": [
        {
            "method": "xpath",
            "args": [
                "//div[@id='chan_newsDetail']//text()"
            ]
        }
    ],
    "datetime": [
        {
            "method": "xpath",
            "args": [
                "//div[@id='chan_newsInfo']/text()"
            ],
            "re": "(\\d-\\d+-\\d+\\s\\d+:\\d+:\\d+)"    # datetime字段，用了一次正则提取，定义re参数来传递提取时所用的正则
        }
    ],
    "source": [
        {
            "method": "xpath",
            "args": [
                "//div[@id='chan_newsInfo']//text()"
            ],
            "re": "来源: (.*)"
        }
    ],
    "website": [
        {
            "method": "value",
            "args": [
                "中华网"
            ]
        }
    ]
}
}

# 将这些配置后动态加载到parse_item里，最重要的是实现parse_item方法：
def parse_item(self, response):
    item = self.config.get('item')  # 首先获取Item的配置信息
    if item:
        cls = eval(item.get('class'))() # 然后获取class的配置，将其初始化，初始化Item Loader
        loader = eval(item.get('loader'))(cls, response=response)
        # 动态获取属性配置
        for key, value in item.get('attrs').items():    # 遍历Item的各个属性依次进行提取
            for extractor in value: # 判断method字段，调用对应的处理方法进行处理
                if extractor.get('method') == 'xpath':
                    loader.add_xpath(key, *extractor.get('args'), **{'re': extractor.get('re')})
                if extractor.get('mehtod') == 'css':    # method为css，嗲用Item Loader的add_css进行提取
                    loader.add_css(key, *extractor.get('args'), **{'re': extractor.get('re')})
                if extractor.get('method') == 'value':
                    loader.add_value(key, *extractor.get('args'), **{'re': extractor.get('re')})
                if extractor.get('method') == 'attr':
                    loader.add_value(key, getattr(response, *extractor.get('args')))
        yield  loader.load_item()   # 所有配置动态加载完毕后，调用load_item方法将Item提取出来

# 回过头看一下start_urls的配置。这里start_urls只可以配置具体的链接。如果这些链接有100个、1000个，也需要动态配置。
# 将start_urls分成两种，一种是直接配置URL列表，一种是调用方法生成，分别定义为static和dynamic类型
# 本例中的start_urls明显是static类型的，所以start_urls配置改写为：
"start_urls": {
    "type": "static",
    "value": [
        "http://tech.china.com/articles/"
    ]
}
# 如果start_urls是动态生成的，可以调用方法传参数：
"start_urls": {
    "type": "dynamic",  # 这里start_urls定义为dynamic类型，
    "method": "china",  # 指定方法为urls_china
    "args": [
        5, 10   # 传入参数5和10，来生成第5到10页的链接，只需实现该方法即可，统一新建一个urls.py文件
    ]
}
# 传入参数5和10，来生成第5到10页的链接，只需实现该方法即可，统一新建一个urls.py文件：
def china(start, end):
    for page in range(start, end + 1):
        yield 'http://tech.china.com/articls/index_' + str(page) + '.html'
# 其他站点可以自行配置，某些链接需要用到时间戳，加密参数等，均可通过自定义方法实现。
# Spider的__init__方法中，start_urls的配置改写：
from scrapyuniversal import urls

start_urls = config.get('start_urls')
if start_urls:  # 通过判定start_urls的类型分别进行不同的处理，就可以实现start_urls的配置了
    if start_urls.get('type') == 'static'
        self.start_urls = start_urls.get('value')
    elif start_urls.get('type') == 'dynamic':
        self.start_urls = list(eval('urls.' + start_urls.get('method'))(*start_urls.get('args', [])))
# 至此，Spider的设置、起始链接、属性、提取方法都已经实现了全部的可配置化
# 整个项目的配置包括：
# spider：指定所使用的Spider的名称
# settings： 可以专门为Spider定制配置信息，会覆盖项目级别的配置
# start_urls：指定爬虫爬取的起始链接
# allowed_domains:允许爬取的站点
# rules：站点的爬取规则
# item：数据的提取规则
# 实现了Scrapy的通用爬虫，每个站点只需要修改JSON文件即可实现自由配置

# 8.代码地址：https://github.com/Python3WebSpider/ScrapyUniversal

# 9.Scrapy通用爬虫的实现，将所有配置抽离出来，每增加一个爬虫，就只需要增加一个JSON文件配置，之后只需要维护这些配置文件即可。
# 如果要更加方便的管理，可以将规则存入数据库，再对接可视化管理页面即可
