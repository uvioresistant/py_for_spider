# 利用Scrapy-Redis实现分布式的对接

# 1.准备：实现Scrapy新浪微博爬虫，Scrapy-Redis库正确安装

# 2.搭建Redis服务器：实现分布式部署，多台主机需要共享爬取队列和去重集合，这两部分内容都是存于Redis数据库中的，
# 需要搭建一个可公网访问的Redis服务器
# 推荐Linux服务器，可购买阿里云、腾讯云、Azure等提供的云主机，一般都配有公网IP,搭建方式同Redis数据库的安装方式
# Redis安装完成后就可远程连接了，部分商家（阿里云、腾讯云）服务器需要配置安全组放通Redis运行端口才可远程访问，如不能远程连接，
# 可排查安全组的设置。
# 需记录Redis的运行IP、端口、地址，供后面配置分布式爬虫用。当前配置的Redis的IP为服务器IP120.27.34.25，端口6379，密码foobared

# 3.部署代理池和Cookies池：新浪微博项目需要用到代理池和Cookies池，之前的代理池和Cookies池都是在本地运行的。
# 所以需要将二者放到可以被公网访问的服务器上运行，将代码上传到服务器，修改Redis的连接信息，同样方式运行代理池和Cookies池
# 远程访问代理池和Cookies池提供的接口，获取随机代理和Cookies。如果不能远程访问，先确保在0.0.0.0这个Host上运行，再检查安全组配置
# 当前配置好的代理池和Cookies池的运行IP都是服务器的*IP，120.27.34.25，端口分别为5555和5556
# 接下来要修改Scrapy新浪项目中的访问链接：   具体修改方式根据实际配置的IP和端口做响应调整
PROXY_URL = 'http://120.27.34.25:5555/random'
COOKIES_URL = 'http://120.27.34.25:5556/weibo/random'

# 4.配置Scrapy-Redis：只需修改一下settings.py配置文件即可：
# A.核心配置：需要将调度器的类和去重类替换为Scrapy-Redis提供的类，在settings.py里添加配置：
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# B.Redis连接配置：两种配置方式：
# 一：通过连接字符串配置，可用Redis的地址、端口、密码来构造一个Redis连接字符串，支持的连接形式：
redis://[:password]@host:port/db    # password是密码，以冒号开头，中括号即可无，host是Redis地址，port运行端口，db数据库代号
rediss://[:password[@host:port/db   # redis://:foobared@120.27.34.25:6379
unix://[:password]@/path/to/socket.sock?db=db
# 直接在settings.py中配置为REDIS_URL变量：
REDIS_URL = 'redis://:foobared@120.27.34.25:6379'
# 二：分项单独配置，更加直观明了：
REDIS_HOST = '120.27.34.25'
REDIS_PORT = 6379
REDIS_PASSWORD = 'foobared'
# 如果配置了REDIS_URL,那么Scrapy-Redis将优先使用REDIS_URL连接，会覆盖上面的三项配置。想分项单独配置，不要配置REDIS_URL

# C.配置调度队列：可选，默认使用PriorityQueue，想更改，可配置SCHEDULER_QUEUE_CLASS:
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.LifoQueue'
# 任选其一配置，可切换爬取队列的存储方式

# D.配置持久化：可选，默认False，默认会在爬取全部完成后清空爬取队列和去重指纹集合
# 如果不想自动清空爬取队列和去重指纹集合，可增加配置：
SCHEDULER_PERSIST = True
# 如果强制中断爬虫的运行，爬取队列和去重指纹集合是不会自动清空的。

# E.配置重爬：可选，默认False，配置持久化或强制中断了爬虫，爬虫队列和指纹集合不会清空，重启后会接着上次爬取，想重现爬取，配置：
SCHEDULER_FLUSH_ON_START = True
# 此配置在单机爬取时比较方便，分布式爬取不常使用此配置

# F.Pipeline配置：可选，默认不启动，Scrapy-Redis实现了一个存储到Redis的Item Pipeline，启用会把生成的Item存储到Redis数据库中，
# 数据量比较大的情况下，一般不会这么做，因为Redis是基于内存的，利用的是它处理速度快的特性，用来做存储未免太浪费了，配置：
ITEM_PIPELINES = {
    'scrapy_redis.pipelines.RedisPipeline': 300
}

# 5.配置存储目标：之前Scrapy爬取新浪微博用的存储是MongoDB，且是本地运行的，连接的是localhost。
# 但，当爬虫程序分发到各台主机运行的时候，爬虫就会连接各自的MongoDB。所以需要再各台主机上都安装MongoDB，有两个缺点：
# 一：搭建MongoDB环境比较繁琐；二：各台主机的爬虫会把爬取结果分散存到各自主机上，不方便统一管理
# 所以最好将存储目标到同一个地方，如都存到同一个MongoDB数据库中，可以在服务器上搭建一个MongoDB服务，或者直接购买MongoDB存储服务
# 使用服务器上搭建MongoDB服务，IP仍然为120.27.34.25，用户名admin，密码admin123，修改MONGO_URI：
MONGO_RUI = 'mongodb://admin:admin123@120.27.34.25:27017'   # 完成Scrapy分布式爬虫的配置

# 6.运行，将代码部署到各台主机行，每台主机都需要配好对应的Python环境，执行命令，启动爬取：
scrapy crawl weibocn
# 每台主机启动了此命令后，会从配置的Redis数据库中调度Request，做到爬取队列共享和指纹集合共享。
# 同时每台主机占用各自的带宽和处理器，不会相互影响，爬取效率成倍提高

# 7.结构：一段时间后，可用RedisDesktop观察远程Redis数据库的信息，会出现两个Key：
# 一：weibocn:dupefilter存储指纹；另一个weibocn:requests爬取队列，指纹集合会不断增长，爬取队列动态变化，数据也被存储到MongoDB

# 8.代码地址https://github.com/Python3WebSpider/Weibo/tree/distributed
# 部署还是有很多不方便的地方，且爬取量特别大的haul，Redis的内存也是个问题，需要优化方案