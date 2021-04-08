# Item Pipeline是项目管道，调用发生在Spider产生Item后Spider解析完Response后，Item就会传递到Item Pipeline，被定义的
# Item Pipeline组件会顺次调用，完成一连串的处理过程，如数据清洗、存储
# Item Pipeline主要功能有4点：
# a.清理HTML数据
# b.验证爬取数据，检查爬取字段
# c.查重饼丢弃重复内容
# d.将爬取结果保存到数据库

# 1.核心方法：可自定义，但必须实现process_item(item, spider)方法，比较实用的方法有：
# open_spider(spider)
# close_spider(spider)
# from_crawler(cls, crawler)

# process_item(item, spider):定义的Item Pipeline会默认调用次方法对Item进行处理。可进行数据处理或将数据写入到数据库。
# 必须返回Item类型的值或抛出一个DropItem异常。
# process_item参数有两个：item，Item对象，被处理的Item；spider，Spider对象，生成该Item的Spider
# process_item方法返回类型：返回Item，此Item会被低优先级的Item Pipeline的process_item方法处理，直到所有方法被调用完毕
#                           抛出的是DropItem异常，此Item会被丢弃，不再进行处理

# open_spider(spider):在Spider开启时被自动调用。可以做一些初始化操作，如开启数据库连接等，参数spider就是被开启的Spider对象

# close_spider(spider）：在Spider关闭时自动调用的。可以做一些收尾工作，如关闭数据库连接，参数spider就是被关闭的Spider对象

# from_crawler(cls, crawler):类方法，用@classmethod标识，一种依赖注入的方式。参数是crawler，通过crawler对象，可拿到Scrapy的
# 所有核心组件，如全局配置的每个信息，创建一个Pipeline实例。参数cls就是Class，最后返回一个Class实例

# 2.目标：爬取360摄影美图，分别实现MongoDB存储、MySQL存储、Image图片存储的三个Pipeline

# 3.准备：安装MongoDB和MySQL数据库，安装Python的PyMongo、PyMySQL、Scrapy框架

# 4.抓取分析:爬取网站：https://image.so.com，打开页面，切换到摄影页面，网页中呈现许多美图。F12，过滤器切换到XHR，下拉页面，
# 会呈现许多Ajax请求。
# 查看请求的详情，观察返回的数据结构：返回格式是JSON。list字段就是一张张图片的详情信息，包含30张图片的ID、名称、链接、缩略图。
# 观察Ajax请求的参数信息，参数sn一直在变化，是偏移量。sn为30，返回的是前30张图片，ch参数是摄影类型，listtype是排序方式
# 抓取时只需改变sn的数值。
# 用Scrapy实现图片的抓取，将图片的信息保存到MongoDB、MySQL，同时将图片存储到本地

# 5.新建项目：命令：
# scrapy startproject images360
# 新建Spider，命令：
# scrapy genspider images images.so.com

# 6.构造请求：定义爬取页数，如爬取50页、每页30张，也就是1500张图片，可先在settings.py里定义变量MAX_PAGE，添加定义：
# MAX_PAGE = 50
# 定义start_requests方法，用来生成50次请求：
def start_requests(self):
    data = {'ch': 'photography', 'listtyype': 'new'}
    base_url = 'https://image.so.com/zj?'
    for page in range(1, self.settings.get('MAX_PAGE') + 1):
        data['sn'] = page * 30  # sn参数是遍历循环生成
        params = urlencode(data)    # 利用urlencode方法将字典转化为URL的GET参数，
        url = base_url + params     # 构造出完整的URL，
        yield Request(url, self.parse)  # 构造并生成Request
# 还需引入scrapy.Request和urllib.parse模块：
from scrapy import Spider, Request
from urllib.parse import urlencode
# 修改settings.py中的ROBOTSTXT_OBEY变量，设置为False，否则无法抓取：
ROBOTSTXT_OBEY = False
# 运行爬虫，可看到链接都请求成功，执行命令：
scrapy crawl images

# 7.提取信息：
# 首先定义一个Item，叫ImageItem：
from scrapy import Item, Field  # 两个属性collection和table，都定义为images字符串，分别是MongoDB存储的Collection和MySQL表名
class ImageItem(Item):  # 定义4个字段
    collection = table = 'images'
    id = Field()    # 图片的ID
    url = Field()   # 链接
    title = Field() # 标题
    thumb = Field() # 缩略图
# 接下来提取Spider里有关信息，将parse改写为：
def parse(self, response):
    result = json.loads(response.text)  # 解析JSON，
    for image in result.get('list'):    # 遍历list字段，取出图片信息
        item = ImageItem()      # 对ImageItem赋值，生成Item对象
        item['id'] = image.get('imageid')
        item['url'] = image.get('qhimg_url')
        item['title'] = image.get('group_title')
        item['thumb'] = image.get('qhimg_thumb_url')
        yield item  # 完成信息的提取

# 8.存储信息：将图片的信息保存到MongoDB、MySQL、同时保存图片到本地
# MongoDB：用一个MongoPipeline将信息保存到MongoDB，在pipelines.py里添加类的实现：
import pymongo

class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),    # 存储到MongoDB的链接地址
            mongo_db=crawler.settings.get('MONGO_DB')   # 存储到数据库名称
        )
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self,item, spider):
        self.db[item.collection].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()
# 在settings.py里添加这两个变量：
MONGO_URI = 'localhost'
MONGO_DB = 'images360'
# 保存到MongoDB的Pipeline创建好了。最主要的方法是process_item方法，直接调用Collection对象的insert方法即可完成数据的插入，
# 最后返回Item对象。

# MySQL：
# 新建一个数据库，名字还是images360，SQL语句：
# CREATE DATABASE images360 DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci
# 新建数据表，包含id、url、title、thumb四个字段，SQL语句：
# CREATE TABLE images (id VARCHAR(255) PRIMARY KEY, url VARCHAR（255） NULL , title VARCHAR(255) NULL ,thumb VARCHAR(255)
# NULL)
# 执行完SQL语句后，成功创建好了数据表。接下来可以往表里存储数据了
# 接下来实现一个MySQLPipeline：
import pymysql

class MysqlPipeline():
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8', port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%'] * len(data))
        sql = 'insert into %s (%s) values (%s)' % (item.table, keys, values)
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()
        return item
# 这里用到的数据插入方法是一个动态构造SQL语句的方法
# 还需要几个MySQL的配置，在settings.py里添加几个变量：
MYSQL_HOST = 'localhost'    # 分别定义了MySQL的地址
MYSQL_DATABASE = 'images360'    # 数据库名称
MYSQL_PORT = '3306' # 端口
MYSQL_USER = 'root' # 用户名
MYSQL_PASSWORD = '123456'   # 密码

# Image Pipeline：Scrapy提供了专门处理下载的Pipeline，包括问价下载和图片下载。下载文件和图片的原理与抓取页面的原理一样，下载
# 过程支持异步和多线程，下载十分高效。
# 官方文档地址：https://doc.scrapy.org/en/latest/topics/media-pipeline.html
# 首先定义存储文件的路径，需要定义一个IMAGES_STORE变量，settings.py中添加：
IMAGES_STORE = './images'
# 将路径定义为当前路径下的images子文件夹，下载的图片都会保存到本项目的images文件夹中。
# 内置的ImagesPipeline会默认读取Item的image_urls字段，并认为该字段是一个列表形式，会遍历Item的image_urls字段，然后取出每个
# URL进行图片下载
# 但现在生成的Item图片链接字段并不是image_urls字段表示的，也不是列表形式，而是单个的URL。为了实现下载，需要重新定义下载的
# 部分逻辑，即定义ImagePipeline，继承内置的ImagesPipeline，重写几个方法：
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline  # 继承Scrapy内置的ImagePipeline
class ImagePipeline(ImagesPipeline):    # 实现了ImagePipeline，
    def file_path(self, request, response=None, info=None): # 参数request就是当前下载对应的Request对象，返回保存的文件名
        url = request.url   # 直接将图片链接的最后一部分当做文件名保存。
        file_name = url.split('/')[-1]  # 利用split函数分割链接并提取最后一部分
        return file_name    # 返回结果。此图片下载后保存的名称就是该函数返回的文件名。

    def item_completed(self, results, item, info):  # 当单个Item完成下载时的处理方法。并不是每张图片都会下载成功，分析并剔除
        # 如果某张图片下载失败，就不需保存此Item到数据库。results就是该Item对应的下载结果，列表形式，每个元素是一个元组，
        # 包含下载成果获失败的信息
        image_paths = [x['path'] for ok, x in results if ok]    # 遍历下载结果找出所有成功的下载列表。
        if not image_paths: # 列表为空
            raise DropItem('Image Downloaded Failed')   # 该Item对应的图片下载失败，爬出异常DropItem，该Item忽略
        return item # 否则返回Item，Item有效

    def get_media_requests(self, item, info): # 第一个参数item是爬取生成的Item对象。
        yield Request(item['url'])  # 将它的url字段取出来，然后直接生成Request对象。此Request加入调度队列，等待被调度，下载
# 三个Item Pipeline定义完成，只需启用就可以，修改settings.py，设置ITEM_PIPELINSE:
ITEM_PIPELINSE = {
    'images360.pipelinse.ImagePipeline': 300, # 优先顺序，优先调用ImagePIEline对Item做下载后的筛选，失败忽略，不保存
    'images360.pipelinse.MongoPipeline': 301, # 再调用其他两个Pipeline
    'images360.pipelinse.MysqlPipeline': 302  # 确保存入数据库的图片都是下载成功的
}
# 运行程序，执行爬取：边爬取边下载，下载速度非常快，对应输出日志
scrapy crawl images
# 查看本地images文件夹，图片都已经成功下载，
# 查看MySQL，下载成功的图片信息也已成功保存
# 查看MongoDB，下载成功的图片信息也已成功保存

# 9.代码地址：https://github.com/Python3WebSpider/Images360
# Item Pipeline是Scrapy非常重要的组件，数据存储几乎都是通过此组件实现的。