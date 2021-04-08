# Downloader Middleware：下载中间件，处于Scrapy的Request和Response之间的处理模块。
# Scheduler从队列中拿出一个Request发送给Downloader执行下载，这个过程会经过Downloader Middleware的处理。
# 当Downloader将Request下载完成得到Response返回给Spider时会再次经过Downloader Middleware处理
# Downloader Middleware在整个架构中起作用的位置是两个：
# a.Scheduler调度出队列的Request发送给Downloader下载之间，就是我们可以在Request执行下载前对其进行修改
# b.下载后生成的Response发送给Spider之前，就是我们可以在生成Response被Spider解析之前对其进行修改
# Downloader Middleware的功能十分强大，修改User-Agent、处理重定向、设置代理、失败重试、设置Cookies等功能都需借助它来实现。

# 1.使用说明：Scrapy已经提供了许多Downloader Middleware，负责失败重试、自动重定向等功能的Middleware，
# 被DOWNLOADER_MIDDLEWARES_BAES变量定义，字典格式，
{
    'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,  # 字典键名Scrapy内置的Downloader Middleware的名称
    'scrapy.downloadermiddlewares.httppauth.HttpAuthMiddleware': 300,   # 键值代表调用的优先级，越小代表越靠近Scrapy引擎，
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,  # 越大越靠近Downloader
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeaderMiddleware': 400, # 数字小的Downloader Middleware优先调用
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 500,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
    'scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware': 560,
    'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 580,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMMiddleware': 590,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
    'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,
    'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
}

# 2.核心方法：Scrapy内置的Downloader Middleware为Scrapy提供基础功能，实际中需要单独定义Downloader Middleware。
# 每个Downloader Middleware都定义了一个或多个方法的类，核心方法有三个：
# process_request(request, spider)
# process_response(request, response, spider)
# process_exception(request, exception, spider)

# process_request(request, spider)
# Request被Scrapy引擎调度个Downloader之前，process_request方法会被调用，在Request从队列里调度出来到Downloader下载执行前，可
# 用process_request方法对Request进行处理。方法的返回值必须为None、Response对象、Request对象之一，或抛出IgnoreRequest异常。
# process_request方法参数有两个：
# request，是Request对象，即被处理的Request
# spider，是Spider对象，此Request对应的Spider
# 返回值不同，产生的效果也不同：
# A.返回None，Scrapy继续处理该Request，接着执行其他Downloader Middleware的process_request方法，一直到Downloader把Request
#   执行后得到Response才结束。此过程就是修改Request，不同的Downloader Middleware按照设置的优先级顺序依次对Request修改，
#   最后送至Downloader执行
# B.返回Response对象，更低优先级的Downloader Middleware的process_request和process_exception方法不会被继续调用，每个
#    Downloader Middleware的process_response方法转而被依次调用。调用完毕后，直接将Response对象发送给Spider处理
# C.返回Request对象，更低优先级的Downloader Middleware的process_request会停止执行。此Request会重新放到调度队列里，其实就是
#   一个全新的Request，等待被调度。如果被Scheduler调度，所有的Downloader Middleware的process_request方法会被重新按顺序执行
# D.IgoreRequest异常抛出，所有Downloader Middleware的process_exception会依次执行。没有一个方法处理该异常，那么Request的
#   errorback方法会回调。该异常还没有被处理，必会被忽略

# process_response(request, response, spider)
# Downloader执行Request下载后，会得到对应的Response。Scrapy引擎便会将Response发送给Spider解析。发送前，都可以用
# process_response方法来对Response进行处理。方法的返回值必须为Request对象、Response对象之一，或者抛出IgnoreRequest异常
# process_response方法的参数有如下三个：
# request,是Request对象，此Response对应的Request
# response，是Response对象，此被处理的Response
# spider，是Spider对象，此Response对应的Spider
# A.返回值为Request对象，更低优先级的Downloader Middleware的process_response不会继续调用。该Request对象会重新放到调度队列
#   等待被调度，相当于一个全新的Request。然后，该Request会被process_request方法顺次处理
# B.返回值为Response对象，更低优先级的DownloaderMiddleware的process_response方法会继续调用，继续对该Response对象进行处理
# C.IgnoreRequest异常抛出，则Request的errorback方法会回调。该异常还没有被处理，会被忽略

# process_exception(request, exception, spider)
# 当Downloader或process_request方法抛出异常时，例如抛出IgnoreRequest异常，process_exception方法就会被调用。
# 返回值必须为None、Response对象、Request对象之一
# process_exception方法的参数有如下三个：
# request,是Request对象，产生异常的Request
# exception，是Exception对象，即抛出的异常
# spider，是Spider对象，即Request对应的Spider
# A.返回为None时，更低级的Downloader Middleware的process_exception会被继续顺次调用，直到所有方法调度完毕
# B.返回为Response对象时，更低级的Downloader Middleware的process_exception也不会再被继续调用，每个Downloader Middleware的
#   process_response方法转而被依次调用。
# C.返回为Request对象时，更低优先级的Downloader Middleware的process_exception也不再被继续调用，该Request对象会重新放到调度
#   队列里面等待被调度，它相当于一个全新的Request。然后，该Request又会被process_request方法顺次处理。
# 自定义Downloader Middleware的时候，一定要注意每个方法的返回类型

# 3.项目实战：新建项目，命令：
# scrapy startproject scrapydownloadertest  # 新建了一个Scrapy项目，名为scrapydownloadertest。进入项目，新建一个Spider
# scrapy genspider httpbin httpbin.org  # 新建了一个Spider，名为httpbin，源代码：
import scrapy
class HttpbinSpider(scrapy.Spider):
    name = 'httpbin'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/']

    def parse(self, response):
        pass
# 修改start_urls为：[http://httpbin.org/](http://httpbin.org/)随后将parse方法添加一行日志输出，将response变量的text属性输出
# 便可以看到Scrapy发送的Request信息了：
import scrapy

class HttpbinSpider(scrapy.Spider):
    name = 'httpbin'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/get']

    def parse(self, response):
        self.logger.debug(response.text)

# 运行此Spider，执行命令：
scrapy crawl httpbin

# Scrapy运行结果包含Scrapy发送的Request信息，内容如下：
{
    "args": {},
    "headers": {    # Headers,
        "Accept": "text/html,application/xhtml+xml,applictaion/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip,deflate,br",
        "Accept-Language": "en",
        "Connection": "close",
        "Host": "httpbin.org",
        "User-Agent": "Scrapy/1.4.0 (+http:/scrapy.org)"# 发送的Request使用的User-Agent是Scrapy/1.4.0(+http://scrapy.org)
    },
    "origin": "60.207.237.85",
    "url": "http://httpbin.org/get"
}

# UserAgentMiddleware的源码：
from scrapy import signals

class UserAgentMiddleware(object):
    def __init__(self, user_agent='Scrapy'):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler): # from_crawler中，尝试获取settings里面USER_AGENT
        o = cls(crawler.settings['USER_AGENT']) # USER_AGENT传递给__init__初始化，其参数就是user_agent
        crawler.signals.connect(o.spider_opened, signals=signals.spider_opened)
        return o

    def spider_opened(self, spider):
        self.user_agent = getattr(spider, 'user_agent', self.user_agent)

    def process_request(self, request, spider): # process_request方法中，将user-agent变量设置为headers变量的一个属性
        if self.user_agent:
            request.headers.setdefault(b'User-Agent', self.user_agent)  # User-Agent通过此Downloader Middleware设置
# 修改请求时的User-Agent有两种方式：一是修改settings里的USER_AGENT变量；二是通过Downloader Middleware的process_request修改
# 第一种简单，只需在setting.py里加一行USER_AGENT：
# USER_AGENT = 'Mozilla/5.0 (Mactintosh; Inter Mac OS X 10_12_6) AppleWebKit/537.36 (KHML, like Gecko)'
#     'Chrome/59.0.3071.115 Safari/537.36'
# 第二种：设置随机User-Agent，需借助Downloader Middleware，在middlewares.py里添加RandomUserAgentMiddleware：
import random

class RandomUserAgentMiddleware():
    def __init__(self): # 定义三个不同的User-Agent,用列表来表示
            self.user_agents = [
            'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2',
            'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1'
        ]

    def process_request(self, request, spider): # 参数request，直接修改request的属性即可
        request.headers['User-Agent'] = random.choice(self.user_agents) # 直接设置了request的headers属性User-Agent
# 要生效还需要再去调用Downloader Middleware。settings.py将DOWNLOADER_MIDDLEWARES取消注释，设置为：
DOWNLOADER_MIDDLEWARES = {
    'scrapydownloadertest.middlewares.RandomUserAgentMidleware': 543
}
# 重新运行Spider，
{
    "args": {},
    "headers": {    # Headers,
        "Accept": "text/html,application/xhtml+xml,applictaion/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip,deflate,br",
        "Accept-Language": "en",
        "Connection": "close",
        "Host": "httpbin.org",
        "User-Agent": "Scrapy/1.4.0 (+http:/scrapy.org)"# 发送的Request使用的User-Agent是Scrapy/1.4.0(+http://scrapy.org)
    },
    "origin": "60.207.237.85",
    "url": "http://httpbin.org/get"
}
# 通过实现Downloader Middleware并利用process_request成功设置了随机的User-Agent。
# Downloader Middleware还有process_response方法。Downloader对Request执行下载后会得到Response，Scrapy引擎会将Response发送
# 回Spider进行处理。但是在Response被发送给Spider之前，同样可以使用process_request方法对Response进行处理。
# 如修改Response的状态码，在RandomUserAgentMiddleware添加代码：
def process_response(self, request, reponse, spider):
    response.status = 201   # 将response变量的status属性修改为201，
    return response # 随后将response返回，这个被修改后的Response就会被发送到Spider
# 再在Spider里面输出修改后的状态码，在parse方法中添加输出语句：
[httpbin] DEBUG: Status Code: 201   # Response的状态码成功修改了
# 想对Response进行后处理，可借助于process_request方法，还有一个process_exception方法，用来处理异常的方法。
# 需要异常处理的话，我们可以调用此方法。
# 4.代码地址：https://github.com/Python3WebSpider/ScrapyDownloaderTest
