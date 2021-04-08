# pyspider是国人binux编写的网络爬虫系统，地址：https://github.com/binux/pyspider,官方文档http://docs.pyspider.org/
# pyspider有强大的WebUI、脚本编辑器、任务监控器、项目管理器以及结果处理器、支持多种数据库后端、多种消息队列、JS渲染页面的爬取

# 1.pyspider基本功能：
#   方便易用的WebUI系统，可视化编写和调试爬虫
#   爬取进度监控、爬取结果查看、爬虫项目管理
#   支持多种后端数据库，MySQL、MongoDb、Redis、SQLite、Elasticsearch、PostgreSQL
#   支持多种消息队列，RabbitMQ、Beanstalk、Redis、Kombu
#   提供优先级控制、失败重试、定时抓取
#   对接PhantomJS，可抓取JS渲染页面
#   支持单机和分布式部署，支持Docker部署
# 想要快速方便地实现一个页面的抓取，可使用pyspider。

# 2.与Scrapy比较：
# pyspider提供WebUI，爬虫的编写、调试都在WebUI中进行。Scrapy原生不具备，采用代码和命令行操作，可以通过对接Portia实现可视化配置
# pyspider调试非常方便，WebUI操作便捷直观。Scrapy使用parse命令进行调试
# pyspider支持PhantomJS进行JS渲染页面的采集。Scrapy可对接Scrapy-Splash组件，需要额外配置
# pyspider内置pyquery作为选择器。Scrapy对接XPath、CSS选择器和正则匹配
# pyspider可拓展程度不足，可配置化程度不高。Scrapy对接Middleware、Pipeline、Extension组件实现强大功能，耦合度低，拓展性极高

# 3.pyspider构架：主要分为Scheduler(调度器)、Fetcher(抓取器)、Processer(处理器）三部分，整个过程受到Monitor(监视器)监控，
#                  抓取结果被Result Worker(结果处理器)处理。

# Scheduler发起任务调度
# Fetcher负责抓取网页内容
# Processer负责解析网页内容，将新生成的Request发给Scheduler调度，将生成的提取结果输出保存
# pyspider任务执行流程逻辑清晰，具体过程如下：
# 每个pyspider项目对应一个Python脚本，该脚本定义了一个Handler类，有一个on_start方法。首先调用on_start方法生成最初的抓取任务，
# 然后发送个Scheduler进行调度
# Scheduler将抓取任务分发给Fetcher抓取，Fetcher执行并得到响应，随后将响应发送给Processer
# Processer处理响应并提取出新URL生成新的抓取任务，通过消息队列方式通知Schduler当前抓取任务执行情况，将新生成抓取任务发送
# 给Scheduler。生成了新的提取结果，将其发送到结果队列等待Result Worker处理
# Scheduler接收新的抓取任务，查询数据库，判断如果是新的抓取任务或是需要重试的任务就继续进行调度，将其发送回Fetcher进行抓取
# 不断重复以上工作，知道所有任务都执行完毕，抓取接受。
# 抓取结束后，程序回调on_finisher方法，可以定义后处理过程
