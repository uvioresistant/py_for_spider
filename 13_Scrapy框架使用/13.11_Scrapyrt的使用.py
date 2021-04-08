# Scrapyrt为Scrapy提供了一个调度的HTTP接口。有了它，不需要再执行Scrapy命令，而是通过请求一个HTTP接口即可调度Scrapy任务，就
# 不再借助于命令行来启动项目了。如果项目是在远程服务器运行，利用它来启动项目是个不错的选择

# 1.目标：说明Scrapyrt的使用方法，源代码地址：https://github.com/Python3WebSpider/ScrapyTutorial

# 2.准备：确保Scrapyrt正确安装并正常运行

# 3.启动服务：将项目下载下来，在项目目录下运行Scrapyrt，假设当前服务运行在9080端口上

# 4.GET请求：支持如下参数：
# spider_name:Spider名称，字符串类型，必传参数。如果传递的Spider名称不存在，则返回404错误
# url：爬取链接，字符串类型，起始链接没有定义就必须要传递这个参数。如果传递了该参数，Scrapy会直接用该URL生成Request，
#       而直接忽略start_requests方法和start_urls属性的定义
# callback：回调函数名称，字符串类型，可选参数。如果传递了就会使用此回调函数处理，否则会默认使用Spider内定义的回调函数
# max_requests：最大请求数量，数值类型，可选参数。定义了Scrapy执行请求的Request的最大限制，如定义5，最多只执行5次Request请求
# start_request：代表是否要执行start_requests方法，布尔类型，可选参数。Scrapy项目中如果定义了start_requests方法，那么项目
# 启动时会默认调用该方法。但Scrapyrt中不一样，Scrapyrt默认不执行start_requests方法，如果要执行，需将start_requests设置为true
# 执行命令：
curl http://localhost://h=localhost:9080/crawl.json?spider_name=quotes&url=http://quotes.toscrape.com/
# 返回的是一个JSON格式的字符串，解析它的结构：
{
    "status": "ok"  # status显示了爬取的状态
    "items": [  # 省略了items绝大部分。items部分是Scrapy项目的爬取结果
    {
        "text": "“The world..."
    }
],
"items_dropped": [],    # items_dropped是被忽略的Item列表
"stats": { # stats是爬取结果的统计情况，此结果和直接运行Scrapy项目得到的统计是相同的
    "downloader/request_bytes": 2892,
    ...
},
"spider_name": "quotes"
}
# 通过HTTP接口调度Scrapy项目并获取爬取结果，如果Scrapy项目部署在服务器上，
# 可以通过开启一个Scrapyrt服务实现任务的调度并直接取到爬取结果，很方便

# 5.POST请求：此处Request Body必须是一个合法的JSON配置，在JSON里可以配置相应的参数，支持的配置参数更多
# JSON配置支持如下参数：
# spider_name：Spider名称，字符串类型，必传参数。如果传递的Spider名称不存在，则返回404错误
# max_requests：最大请求数量，数值类型，可选参数。定义了Scrapy执行请求的Request的最大限制，如定义为5，则最多只执行5次Request
# 请求，其余的会被忽略
# resquest：Request配置，JSON，比传参数。通过该参数可定义Request的各个参数，必须指定url字段来指定爬取链接，其他字段可选
{
    "request": {
        "url": "http://quotes.toscrape.com/",
        "callback": "parse",
        "dont_filter": "True",
        "cookies": {
            "foo": "bar"
        }
    },
    "max_requests": 2,
    "spider_name": "quotes"
}
# 执行命令，传递JSON配置并发起POST请求：
curl http://localhost:9080/crawl.json -d '{"request": {"url": "http://quotes.toscrape.com/", "dont_filter":' \
 '"True", "callback": "arse", "cookies": {"foo": "bar"}}, "max_requests":2, "spider_name": "quotes"}'