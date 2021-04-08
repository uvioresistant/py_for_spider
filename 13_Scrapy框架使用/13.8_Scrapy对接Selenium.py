# Scrapy抓取页面方式和requests库类似，都是直接模拟HTTP请求，而Scrapy也不能抓取JS动态渲染的页面。
# 抓取JS渲染的页面有两种方式：
# 一.分析Ajax请求，找到对应的接口抓取，Scrapy同样可以用此种方式抓取。
# 二、直接用Selenium或Splash模拟浏览器进行抓取，不需关心后台发生的请求，也不需分析渲染过程，只需关心页面最终结果即可，可见可爬
# Scrapy对接Selenium，Scrapy就可处理任何网站的抓取了

# 1.目标：以PhantomJS，抓取淘宝商品信息，抓取逻辑与Selenium抓取淘宝商品完全相同

# 2.准备：PhantomJS和MongoDB安装好，安装Scrapy、Selenium、PyMongo库

# 3.新建项目：名为scrapyseleniumtest：
# scrapy genspider taobao www.taobao.com
# 修改ROBOTSTXT_OBEY为Fales：
# ROBOTSTXT_OBEY = False

# 4.定义Item：名为ProductItem：
from scrapy import Item, Field

class ProductItem(Item):    # 定义6个Field，即6个字段，
    collection = 'products' # 定义一个collection属性，即此Item保存的MongoDB的Collection名称
    image = Field()
    price = Field()
    deal = Field()
    title = Field()
    shop = Field()
    location = Field()

# 初步实现Spider的start_requests方法：
from scrapy import Request, spider
from urllib.parse import quote
from scrapyseleniumtest.items import ProductItem

class TaobaoSpider(Spider):
    name = 'taobao'
    allowed_domains = ['www.taobao.com']
    base_url = 'https://s.taobao.com/search?q=' # 定义一个base_url，即商品列表的URL，然后拼接一个搜索关键字，即该关键字在
                                                # 淘宝的搜索结果商品列表页面

    def start_requests(self):   # 首先遍历关键字，遍历了分页页码，构造并生成Request
        for keyword in self.setting.get('KEYWORDS'):    # 关键字用KEYWORDS标识，定义为列表
            for page in range(1, self.settings.get('MAX_PAGE') + 1): # 最大翻页页码用MAX_PAGE表示，统一定义在settings.py中
                url = self.base_url + quote(keyword)
                yield Request(url=url, callback=self.parse, meta={'page': page}, dont_filter=True)  # 每次搜索的URL相同
                # 分页页码用meta参数来传递，同时设置dont_filter不去重。爬虫启动时，生成每个关键字对应的商品列表的每一页请求

# 最大翻页页码用MAX_PAGE表示，统一定义在settings.py中:
# KEYWORDS = ['ipad']
# MAX_PAGE = 100

# 5.对接Selenium：采用Downloader Middleware实现。在Middleware里的process_request方法里对每个抓取请求进行处理，启动渲染器
# 并进行页面渲染，再将渲染后的结果构造一个HTMLResponse对象返回：
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
from logging import getLogger

class SeleniumMiddleware():
    def __init__(self, timeout=None, service_args=[]):
        self.logger = getLogger(__name__)
        self.timeout = timeout
        self.browser = webdriver.PhantomJS(service_args=service_args)   # 初始化PhantomJS对象
        self.browser.set_window_size(1400, 700) # 设置页面大小
        self.browser.get_page_load_timeout(self.timeout)    # 设置页面加载超时时间
        self.wait = WebDriverWait(self.browser, self.timeout)   # 初始化WebDriver对象

    def __def__(self):
        self.browser.close()

    def process_request(self, request, spider):
        """
        用PhantomJS抓取页面
        :param request: Request对象
        :param spider: Spider对象
        :return: HTMLResponse
        """
        self.logger.debug('PhantomJS is Starting')
        page = request.meta.get('page', 1)  # 通过Request的meta属性获取当前需要爬取的页码
        try:
            self.browser.get(request.url)   # 调用PhantomJS对象的get方法访问Request对应的URL，相当于从Request对象里获取
            # 请求链接，然后再用PhantomJS加载，而不再使用Scrapy里的Downloader
            if page > 1:
                input = self.wait.until(
                    EC.present_of_element_located((By.CSS_SELECTOR, '#mainsrp-page div.form > input')))
                submit = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-page div.form > span.btn.J_Submit')))
                input.clear()
                input.send_keys(page)
                submit.click()
            self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '# mainsrp-pager li.item.active > span'),
                                                             str(page)))
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                                status=200) # 页面加载完成后，调用PhantomJS的page_source属性获取当前页面的源代码
        except TimeoutException:
            return HtmlResponse(url=request.url, status=500, request=request)   # 直接构造并返回一个HTMLResponse对象

        @ classmethod
        def from_crawler(cls, crawler):
            return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
                       service_args=crawler.settings.get('PHANTOMJS_SERVICE_ARGS'))
# 完成利用PhantomJS来代替Scrapy完成页面的加载，最后将Response返回即可。
# Request对象到这里，Scrapy就不再处理，也不会再像以前一样交给Downloader下载。Response会直接传给Spider进行解析

# Downloader Middleware的process_request方法的处理逻辑：
# 当process_request方法返回Response对象时，更低优先级的Downloader Middleware的process_request和process_exception方法就不会
# 继续调用了，转而开始执行每个Downloader Middleware的process_response方法，调用完毕后直接将Response对象发送给Spider处理
# 这里直接返回了一个HTMLResponse对象，是Response的子类，返回后便顺次调用每个Downloader Middleware的process_response方法。
# 在process_response中我们没有对其做特殊处理，会被发送给Spider，传给Request的回调函数进行解析
# settings.py里，设置调用刚才定义的SeleniumMiddleware:
DOWNLOADER_MIDDLEWARES = {
    'scrapyseleniumtest.middlewares.SeleniumMiddleware': 543,
}

# 6.解析页面：Response对象回传给Spider内定回调函数进行解析。下一步实现其回调函数，对网页来进行解析：
def parse(self, response):
    products = response.xpath(  # 用xpath进行解析，调用response变量的xpath方法即可
        '//div[@id="mainsrp-itemlist"]//div[@class="items"][1]//div[contains(@class, "item")]')
    for product in products:    # 对结果进行遍历，依次选取每个商品
        item = ProductItem()    # 传递选取所有商品对应的XPath,可匹配所有商品，
        item['price'] = ''.join(product.xpath('.//div[contains(@class, "price")]//text()').extract()).strip()   # 价格
        item['item'] = ''.join(product.xpath('.//div[contains(@class, "item")]//text()').extract()).strip() # 名称
        item['shop'] = ''.join(product.xpath('.//div[contains(@class, "shop")]//text()').extract()).strip()
        item['image'] = ''.join(product.xpath('.//div[contains(@class, "pic")]//text()').extract()).strip() # 图片
        item['deal'] = product.xpath('.//div[contains(@class, "deal-cnt")]//text()').extract_first()
        item['location'] = product.xpath('.//div[contains(@class, "location")]//text()').extract_first()
        yield item  # 构造并返回一个ProductItem对象

# 7.存储结果：最后实现一个Item Pipeline，将结果保存到MongoDB：
import pymongo

class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_uri=.settings.get('MONGO_RUI'), mongo_db=crawler.settings.get('MONGO_DB'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        self.db[item.collection].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()
# 实现和存储到MongoDB的方法完全一致，在settings.py中开启调用：
ITEM_PIPELINES = {
    'scrapyseleniumtest.pipelines.MongoPipeline': 300,
}
# MONGO_URI和MONGO_DB定义如下：
MONGO_URI = 'localhost'
MONGO_DB = 'taobao'

# 8.运行：执行命令启动抓取：
scrapy crawl taobao
# 查看MongoDB，便成功在Scrapy中对接Selenium并实现了淘宝商品的抓取

# 9.代码地址：https://github.com/Python3WebSpider/ScrapySeleniumTest
# 通过实现Downloader Middleware方式实现了Selenium的对接。但这种方式其实是阻塞式，即破坏了Scrapy异步处理的逻辑。为了不破坏
# 异步加载逻辑，可以使用Splash实现。
