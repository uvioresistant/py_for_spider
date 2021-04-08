# pyspider可配置化程度不高，异常处理能力有限，对于反爬程度非常强的网站的爬取力不从心
# Scrapy功能非常强大，爬取效率高，相关拓展组件多，可配置和可扩展程度高，几乎可以应对所有反爬网站，Python中使用最广泛的爬虫框架
# Scrapy是基于Twisted的异步处理框架，是纯Python实现的爬虫框架，构架清晰，模块之间耦合程度低，可拓展性极强，只需定制开发模块爬虫
# 1.构架：
# a.Engine：引擎，处理整个系统的数据流处理、触发事务，整个框架的核心
# b.Item：项目，定义爬取结果的数据结构，爬取数据会被赋值成该Item对象
# c.Scheduler:调度器，接受引擎发过来的请求并将其加入队列中，在引擎再次请求时将请求提供给引擎
# d.Downloader:下载器，下载网页内容，将网页内容返回给蜘蛛
# e.Spiders：蜘蛛，定义爬取逻辑和网页的解析规则，主要负责解析响应并生成提取结果和新的请求
# f.Item Pipeline：项目管道，处理由蜘蛛从网页中抽取的项目，任务是清洗、验证和存储数据
# g.Douwnloader Middlewares：下载器中间件，位于引擎和下载器之间的钩子框架，处理引擎与下载器之间的请求及响应
# h.Spider Middlewares：蜘蛛中间件：位于引擎和蜘蛛件的钩子构架，处理蜘蛛输入的响应和输出的结果及新的请求

# 2.数据流：由引擎控制，过程如下：
# (1).Engine打开一个网站，找到处理该网站的Spider，向该Spider请求第一个要爬取的URL
# (2).Engine从Spider中获取到第一个要爬取的URL，通过Scheduler以Request的形式调度
# (3).Engine向Scheduler请求下一个要爬取的URL
# (4).Scheduler返回下一个要爬取的URL给Engine，Engine将URL通过Downloader Middlewares转发给Downloader下载
# (5).页面下载完毕，Downloader生成该页面的Response，将其通过Downloader Middlewares发送给Engine
# (6).Engine从下载器中接收到Response，将其通过Spider Middlewares发送给Spider处理
# (7).Spider处理Response，并返回爬取到的Item及新的Request给Engine
# (8).Engine将Spider返回的Item给Item Pipeline，将新的Request给Scheduler
# (9).重复(2)到(8)，直到Scheduler中没有更多的Request，Engine关闭该网站，结束爬取
# 通过多个组件的相互协作、不同组件完成工作的不同、组件对异步处理的支持，Scrapy最大限度利用了网络宽带，提高数据爬取和处理效率

# 3.项目结构：与pyspider不同，通过命令行来创建项目，代码编写还需要IDE，项目创建后，文件结构如下：
# sccrapy.cfg   # scrapy.cfg:Scrapy项目配置文件，定义项目的配置文件路径、部署相关信息等内容
# project/
#     __init__.py
#     items.py        # 定义Item数据结构，所有Item定义都可以放这里
#     piplines.py     # 定义Item Pipeline实现，所有Item Pipeline实现都可以放这里
#     settings.py     # 定义项目的全局配置
#     middlewares.py  # 定义Spider Middlewares和Downloader Middlewares的实现
#     spiders/        # 包含一个个Spider实现，每个Spider都有一个文件
#         __init__.py
#         spider1.py
#         spider2.py
#         ...
