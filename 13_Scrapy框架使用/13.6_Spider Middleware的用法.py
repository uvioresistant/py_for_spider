# Spider Midddleware是介入到Scrapy的Spider处理机制的钩子框架，架构：
# 当Downloader生成Response后，Response被发送给Spider，发送给Spider前，Response首先经过Spider Middleware处理，当Spider处理
# 生成Item和Request后，Item和Request还会经过Spider Middleware的处理：
# Spider Middleware三个作用：
# a.在Downloader生成的Response发送给Spider前，对Response进行处理
# b.在Spider生成的Request发送给Scheduler前，对Request进行处理
# c.在Spider生成的Item发送给Item Pipeline前，对Item进行处理

# 1.使用说明：Scrapy提供了许多Spider Middleware，被SPIDER_MIDDLEWARES_BASE变量定义：
{
    'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': 50,
    'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': 500,
    'scrapy.spidermiddlewares.refererRefererMiddleware': 700,
    'scrapy.spidermiddlewares.urllength.UrlLengtthMiddleware': 800,
    'scrapy.spidermiddlewares.depth.DepthMiddleware': 900,
}
# 和Downloader Middleware一样，Spider Middleware首先加到SPIDER_MIDDLEWARES设置中，该设置和Scrapy中SPIDER_MIDDLEWARES_BASE
# 定义的Spider Middleware合并。然后根据键值的数字优先级排序，得到一个有序列表。第一个Middleware最靠近引擎，最后一个Middleware
# 最靠近Spider

# 2.核心方法：Scrapy内置的Spider Middleware为Scrapy提供了基础的功能。如果想要拓展其功能，只需实现4个核心方法：
# a.process_spider_input(response, spider)
# b.process_spider_output(response, result, spider)
# c.process_spider_exception(response, exception, spider)
# d.process_start_requests(start_requests, spider)
# 只需实现其中一个方法就可定义一个Spider Middleware。

# process_spider_input(response, spider)    # Response被Spider Middleware处理时，process_spider_input方法被调用
# process_spider_input方法参数有两个：response，Response对象，被处理的Response；spider，Spider对象，该Response对应的Spider
# process_spider_input应该返回None或抛出一个异常：
# 返回None，Scrapy将不会调用其他Spider Middleware的process_spider_input方法，而调用Request的errback方法。
# errback输出将被重新输入到中间件中，使用process_spider_output方法处理，抛出异常则调用process_spider_exception处理

# process_spider_output(response, result, spider)   # Spider处理Response返回结果时，process_spider_output方法被调用
# process_spider_output方法参数有三个：response，Response对象，生成该输出的Response；result，含Request或Item对象的可迭代对象
# 即Spider返回的结果；spider，Spider对象，其结果对应的Spider
# process_spider_out必须包含Request或Item对象的可迭代对象

# process_spider_exception(response, exception, spider) # Spider或Spider Middleware的process_spider_intput抛出异常时，
# process_spider_exception方法被调用
# process_spider_exception方法的参数有三个：response,Response对象，异常被抛出时被处理的Response；exception，Exception对象，
# 被抛出的异常；spider，Spider对象，抛出该异常的Spider
# process_spider_exception要么返回None，Scrapy继续处理该异常，调用其他Spider Middleware中的process_spider_exception方法
# 要么返回一个包含Response或Item对象的可迭代对象；其他Spider Middleware的process_spider_output被调用，其他exception不调用

# process_start_requests(start_requests, spider):以Spider启动的Request为参数被调用，执行过程类似于process_spider_output,
# 不过没有相关联的Response，且必须返回Request
# process_start_requests方法的参数有两个：start_requests,包含Request的可迭代对象Start Requests；spider，Spider对象，
# process_start_requests必须返回另一个包含Request对象的可迭代对象
# Spider Middleware的使用频率不如Downloader Middleware高，必要的情况下可以用来方便数据的处理