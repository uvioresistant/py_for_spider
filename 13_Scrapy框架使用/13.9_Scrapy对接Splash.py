# Scrapy对接Selenium抓取淘宝商品，是一种抓取JS动态渲染页面的方式，除了Selenium，Splash也可以实现同样的功能

# 1. 准备：Splash正确安装，安装好Scrapy-Splash库

# 2.新建项目：名为scrapysplashtest：
# scrapy startproject scrapysplashtest
# 新建一个Spider：
# scrapy genspider taobao www.taobao.com

# 3.添加配置：参考Scrapy-Splash的配置说明进行配置：链接：https://github.com/scrapy-plugins/scrapy-splash#configuration
# 修改settings.py，配置SPLASH_URL，由于Splash在本地运行，可以直接配置本地的地址：
# SPLASH_URL = 'http://localhost:8050'
# 如果Splash在远程服务器运行，此处就配置为远程的地址。如运行在IP为120.27.34.25的服务器上，应该配置为：
# SPLASH_URL = 'http://120.27.43..25:8050'
# 还需配置几个Middleware：
DOWNLOADER_MIDDLEWARES = {  # 配置三个Downloader Middleware
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy_downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}
SPIDER_MIDDLEWARES = {  # 配置一个Spider Middleware,是Scrapy-Splash的核心部分
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}
# 不需想对接Selenium那样实现一个Downloader Middleware，Scrapy-Splash库都准备好了，直接配置即可
# 还需配置一个Cache存储HTTPCACHE_STORAGE:
# HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# 4.新建请求：利用Splash来抓取页面，可直接生成一个SplashRequest对象并传递相应的参数，Scrapy会将此请求转发给Splash，Splash
# 对页面进行渲染加载，然后再将渲染结果传递回来。此时Response的内容就是渲染完成的页面结果，最后交给Spider解析即可,如：
# yield SplashRequest(url, self.parse_result, # 构造了SplashRequest对象，前两个参数是请求的URL和回调函数
#     args={    # 通过args传递一些渲染参数
#         # optional; parameters passed to Splash HTTP API
#         'wait': 0.5   # 等待时间
#         # 'url' is prefilled from request url
#         # 'http_method' is set to 'POST' for POST requests
#         # 'body' is set to request body for POST requests
#         },
#         endpoint='render.json', # optional; default is render.html    # 根据endpoint参数指定渲染接口
#         splash_url='<url>',     # optional； overrides SPLASH_RUL
# )
# 更多参数可参考文档说明：https://github.com/scrapy-plugins/scrapy-splash#requests
# 还可生成Request对象，Splash的配置可通过meta属性配置：
# yield scrapy.Request(url, self.parse_result, meta={   # SplashRequest对象通过args来配置，Request对象通过meta来配置，相同
#     'splash': {
#         'args': {
#             # set rendering arguments here
#             'html': 1,
#             'png': 1,
#             # 'url' is prefilled from request url
#             # 'http_method' is set to 'POST' for POST requests
#             # 'body' is set to request body for POST requests
#         },
#         # optional parameters
#         'endpoint': 'render.json', # optional; default is render.json
#         'splash_url': '<url>',     # optional; overrides SPLASH_URL
#         'splot_policy': scrapy_splash.SlotPolicy.PER_DOMAIN,
#         'splash_header': {},       # optional, default is False
#         'dont_process_response': True, # optional, default is False
#         ''magic_response': False, # optional, default is True'
#     }
# })

# 抓取淘宝商品信息，涉及页面加载等待，模拟点击翻页等，可以首先定义一个Lua脚本，实现页面加载、模拟点击翻页的功能：
function main(splash, args)
    args = {    # 定义三个参数
        url="https://s.taobao.com/search?q=ipad", # 请求的链接url
        wait=5, # 等待时间wait
        page=5  # 分页页码page
    }
    splash.images_enabled = false   # 禁用图片加载
    assert(splash:go(args.url))
    assert(splash:wait(args.wait))
    js = string.format("document.querySelector('#mainsrp-pager div.form > input').value=%d;"    # 实现页码填充
       "document.querySelector('#mainsrp-pager div.form > span.btn.J_Submit').click()", args.page)  # 翻页点击
    splash:evaljs(js)   # 通过evaljs方法调用JS代码
    assert(splash:wait(args.wait))
    return splash:png() #返回页面截图
end
# 将脚本放到Splash中运行，正常获取到页面截图，翻页操作也成功实现，和传入的页码page参数是相同的
# 只需在Spider里用SplashRequest对接Lua脚本就好：
from scrapy import Spider
from urllib.parse import quote
from scrapysplashtest.items import ProductItem
from scrapy_splash import SplashRequest
script = """    # 把Lua脚本定义成长字符串
function main(splash, args) # 通过SplashRequest的args来传递参数，
    splash.images_enabled = false   
    assert(splash:go(args.url))
    assert(splash:wait(args.wait))
    js = string.format("document.querySelector('#mainsrp-pager div.form > input').value=%d;
    document.querySelector('#mainsrp-pager div.form > span.btn.J_Submit').click()".args.page)
    splash:evaljs(js)
    assert(splash:wait(args.wait))
    return splash:html()
end
"""

class TaobaoSpider(Spider):
    name = 'taobao'
    allowed_domains = ['www.taobao.com']
    base_url = 'https://s.taobao.com/search?q='

    def start_requests(self):
        for keyword in self.settings.get('KEYWORDS'):
            for page in range(1, self.settings.get('MAX_PAGE') + 1):
                url = self.base_url + quote(keyword)
                yield SplashRequest(url, callback=self.parse,endpoint='execute', args={'lua_source':script,
                      'page': page, 'wait': 7}) # 接口改为execute，args参数里还有一个lua_source用于指定Lua脚本内容
# 其他配置不需要更改，Item、Item Pipeline等设置与对接Selenium的方式相同，parse回调函数也是完全一致的

# 5.运行：通过命令运行爬虫：
# scrapy crawl taobao
# Splash和Scrapy都支持异步处理，可以看到同事会有多个抓取成功的结果。
# 在Selenium的对接过程中，每个页面渲染是在Downloader Middleware里完成的，所以整个过程是阻塞式的，Scrapy会等待整个过程后
# 再继续处理和调度其他请求，影响了爬取效率
# 使用Splash的爬取效率比Selenium高很多
# 结果同样正常保存到MongoDB中

# 6.代码地址：https://github.com/Python3WebSpider/ScrapySplashTest
# 在Scrapy中，建议使用Splash处理JS动态渲染的页面，这样不会破坏Scrapy中的异步处理过程，大大提高爬取效率。且Splash的安装
# 和配置比较简单，通过API调用的方式实现了模块分离，大规模爬取的部署也更加方便
