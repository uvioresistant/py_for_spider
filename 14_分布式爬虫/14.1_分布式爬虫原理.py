# 在同一台主机上运行的框架，爬取效率比较有限，如果多台主机协同爬取，那么爬取效率必然会成倍增长，就是分布式爬虫的优势
# Scrapy虽然爬虫是异步+多线程的，但只能在一台主机上运行，爬取效率有限，分布式爬虫是讲多台主机组合起来，共同完成一个爬取任务，
# 大大调高爬取的效率

# 1.分布式爬虫架构：
# Scrapy单机爬虫中有一个本地爬取队列Queue，这个队列是利用deque模块实现的，如果新的Request生成就会放到队列里面，随后Request被
# Scheduler调度后，Request交给Downloader执行爬取。
# 如果两个Scheduler同事从队列里面取Request，每个Scheduler都有其对应的Downloader，那么在带宽足够、正常爬取且不考虑队列存取压力
# 的情况下，爬取效率会翻倍。
# 这样,Scheduler可以扩展多个，Downloader也可扩展多个。爬取队列Queue始终为一个，即共享爬取队列，才能保证Scheduler从队列里调度
# 某个Request后，其他Scheduler不会重复调度此Request，就可以做到多个Scheduler同步爬取。这就是分布式爬虫的基本雏形。
# 需要做的就是在多态主机上同事运行爬虫任务协同爬取，协同爬取的前提就是共享爬取队列。这样各台主机就不需各自维护爬取队列，而是
# 从共享爬取队列存取Request。但各台主机还是有各自的Scheduler和Downloader，所以调度和下载功能分别完成，如果不考虑队列性能消耗，
# 爬取效率还是会成倍提高。

# 2.维护爬取队列：首先需要考虑的就是性能问题，自然想到基于内存存储的Redis，支持多种数据结构，如列表（list）、集合（set），
# 有序集合（Sorted Set)等，存取的操作也非常简单。
# Redis支持的几种数据结构存储各有优点：
# a.列表有lpush、lpop、rpush、rpop方法，可用来实现先进先出式爬取对了，也可以实现先进后出栈式爬取队列
# b.集合的元素是无序的且不重复的，这样可以非常方便地实现随机排序且不重复的爬取对了
# c.有序集合带有分数表示，而Scrapy的Request也有优先级的控制，可用来实现带优先级调度的队列

# 3.如何去重：Scrapy有自动去重，使用了Python中的集合，此集合记录了Scrapy中每个Request的指纹，此指纹实际上就是Request的散列值，
# Scrapy源代码：
import hashlib
...
# request_fingerprint就是计算Request指纹的方法，其方法内部使用的是hashlib的sha1方法，计算的字段包括Request的Method、URL、
# Body、Headers及部分内容，只要有一点不同，name计算的结果就不同。计算得到的结果是加密后的字符串，也就是指纹。
# 每个Request都有独有的指纹，指纹就是一个字符串，判定字符串比判定Request对象是否重复容易多，故指纹是判定Request是否重复的依据
# Scrapy判定重复的实现：
def __init__(self):
    self.fingerprints = set()

def request_seen(self, request):    # 在去重类RFPDupeFilter中，有request_seen方法，此方法有一个参数request,
    # 就是检测Request是否重复，这个方法调用request_fingerprint获取该Request的指纹，检测此指纹是否存在于fingerprints变量中，
    fp = self.request_fingerprint(request)
    if fp in self.request_fingerprint:          # 而fingerprints是一个集合，集合的元素都是不重复的。
        return True     # 如指纹存在，就返回True，说明该Request是重复的，
    self.fingerprint.add(fp)    # 否则该指纹加入到集合中，如果下次还有相同Request传递过来，Request对象判定重复，去重目的实现
# Scrapy的去重过程就是，利用集合元素的不重复特性来实现Request的去重。
# 对分布式爬虫来说，不能再用每个爬虫各自的集合来去重，因为这样还是每个主机单独维护自己的集合，不能做到共享。多台主机如果生成了
# 相同的Request，只能各自去重，各个主机之间就无法做到去重了
# 要实现去重，这个指纹集合也需共享，Redis正好又集合的存储数据结构，可以利用Redis集合作为指纹集合，这样去重集合也是利用redis
# 共享的。每台主机新生成Request后，把该Request的指纹与集合比对，如果指纹已经存在，说明重复，否则将Request加入到该集合中即可。
# 以同样的原理，不同的存储结构也实现了分布式的Request的去重

# 4.防止中断：Scrapy中，爬虫运行时的Request队列放在内存中。爬虫运行中断后，这个队列的空间就被释放，此队列就被销毁了，
# 所以一旦爬虫运行中断，再次运行相当于全新的爬取过程。
# 要做到中断后继续爬取，可以将队列中的Request保存起来，下次爬取直接读取保存数据即可获取上次爬取的队列。
# 在Scrapy中指定一个爬取队列的存储路径即可，这个路径使用JOB_DIR变量来表示，实现命令：
scrapy crawl spider -s JOB_DIR=crawls/spider
# 详细使用，官方文档：https://doc.scrapy.org/en/latest/topics/jobs.html
# Scrapy中，实际是把爬取队列保存到本地，第二次爬取直接读取并回复队列即可，在分布式架构中不需要担心这个问题，爬取队列本身就是
# 用数据库保存的，如果爬虫中断了，数据库中的Request依然存在，下次启动会接着上次中断的地方继续爬取
# 当Redis队列为空，爬虫会重新爬取；当Redis的队列不为空，爬虫便会接着上次中断之处继续爬取

# 5.架构实现：首先实现一个共享的爬取队列，还要实现去重的功能；另外，重写一个Scheduler的功能，是之可以从共享爬取队列存取Request
# 这些逻辑和架构，已经实现并发布成Scrapy-Redis的Python包