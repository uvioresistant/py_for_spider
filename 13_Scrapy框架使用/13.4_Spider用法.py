# Scrapy中，抓取网站的链接配置、抓取逻辑、解析逻辑都是在Spider中配置的。
# 1.Spider运行流程：Scrapy爬虫项目时，最核心的类便是Spider类，定义了如何爬取摸个网站的流程和解析方式，如下两件：
# a.定义爬取网站的动作
# b.分析爬取下来的网页
# Spider整个爬取循环过程：
# a.初始URL初始化Request，设置回调函数。当该Request成功请求并返回，Response生成并作为参数传给该回调函数
# b.回调函数内分析返回的网页内容。
#   返回结果两种：一种是解析的有效结果返回字典或Item对象，可以经过处理后保存。
#                另一种是解析得到下一页链接，利用此链接构造Request并设置新的回调函数，返回Request等待后续调度
# c.返回的是字典或Item对象，可通过Feed Exports组件将返回结果存入到文件。设置了Pipeline，可使用Pipeline处理(过滤、修正)并保存
# d.返回的是Request，Request执行成功得到Response后，Response会被传递给Request中定义的回调函数，在回调函数中可以再次使用
#   选择器分析新的数据生成Item，循环往复进行，完成站点的爬取

# 2.Spider类分析：scrapy.spiders.Spider是最简单最基本的Spider类，其他类必须继承这个类
# scrapy.spider.Spider类提供了start_requests方法的默认实现，读取并请求start_urls属性，返回的结果调用parse方法解析，属性如下：
# A.name:爬虫名称，定义Spider名字的字符串。定义Scrapy如何定位并初始化Spider，必须唯一，可生成多个相同Spider实例，数量没限制
#        Spider爬取单个网站，以该网站域名名称来命名Spider。爬取pywebsite.com，命名为mywebsite
# B.allowed_domains:允许爬取的域名，可选配置，不再此范围的链接不会被跟进爬取
# C.start_urls:起始URL列表，没有实现start_requests方法是，默认从此列表开始爬取
# D.custom_settings：字典，专属于本Spider的配置，此设置会覆盖项目全局的设置，必须在初始化前被更新，必须定义成类变量
# E.crawler:由from_crawler方法设置，代表本Spider类对应的Crawler对象。包含许多项目组件，常见的是获取项目设置信息Settings
# F.settings:直接获取项目的全局设置变量
# G.start_requests()：用于生产初始请求，必须返回一个可迭代对象。默认使用start_urls里面的URL来构造Request，且Request是GET请求。
#                     想在启动时以POST方式访问某个站点，可以直接重写此方法，发送POST请求使用FormRequest即可
# H.parse：Response没有指定回调函数时，该方法会默认被调用。负责处理Response，处理返回结果，并从中提取出想要的数据和下一步请求，
#          需要返回一个包含Request或Item的可迭代对象
# I:closed()：Spider关闭时，方法会被调用，一般会定义释放资源的一些操作或其他收尾操作
