# Redis是一个基于内存的高效键值型非关系数据库，存取效率极高，支持多种存储数据结构，使用简单
# 2.redis-py库提供两个类Redis及StrictRedis实现Redis的命令
# StrictRedis实现了绝大部分官方命令，Redis是StrictRedis的子类，主要功能是向后兼容旧版本库的方法


# 3.连接Redis:已经在本地安装了Redis并运行在6379端口，密码：foobared，连接Redis并测试
# from redis import StrictRedis
#
# redis = StrictRedis(host='localhost', port=6379, db=0,) # 传入Redis的地址、运行端口、使用数据库和密码，声明StrictRedis对象
# redis.set('name', 'Bob')                                # 调用set方法，设置一个键值对
# print(redis.get('name'))                                # 获取并打印
# 说明连接成功，并可以执行set和get操作
# 然而redis.conf中并没有设置密码，因此报ResponseError: Client sent AUTH, but no password is set
# 解决方法：将password字段去除即可



# 还可以使用ConnectionPool连接
from redis import StrictRedis, ConnectionPool

# pool = ConnectionPool(host='localhost', port=6379, db=0,)
# redis = StrictRedis(connection_pool=pool)


# ConnectionPool还支持通过URL来构建，URL的格式支持有如下3种：
# redis://[:password]@host:port/db                  # 创建Redis TCP连接
# rediss://[:password]@host:port/db                 # 创建Redis TCP+SSL连接
# unix://[:password]@/path/to/socket.sock?db=db     # 创建Redis UNIX socket连接
# 只需构造任意一种URL即可，password没有可以不写
url = 'redis://@localhost:6379/0'               # 使用第一种连接字符串进行连接，声明一个Redis连接字符串
pool = ConnectionPool.from_url(url)             # 调用from_url方法创建ConnectPool
redis = StrictRedis(connection_pool=pool)       # 将其传给StrictRedis完成连接


# 4.键操作


# 5.字符串操作：Redis支持最基本的键值对形式存储


# 6.列表操作：列表内的元素可以重复，而且可以从两端存储


# 7.集合操作：集合中的元素都是不重复的


# 8.有序集合操作:有序集合比集合多了一个分数字段，可以对集合中的数据进行排序


# 9.散列操作：用name指定一个散列表的名称，表内存储了各个键值对


# 10.RedisDump：提供了强大的Redis数据导入和导出功能
# RedisDump提供了两个可执行命令：redis-dump用于导出数据，redis-load用于导入数据
# redis-dump
# 命令行中输入：redis-dump -h
# Usage: C:/Ruby24-x64/bin/redis-dump [global options] COMMAND [command options]
#     -u, --uri=S                      Redis URI (e.g. redis://hostname[:port]) # Redis连接字符串
#     -d, --database=S                 Redis database (e.g. -d 15)              # 数据库代号
#     -a, --password=S                 Redis password (e.g. -a 'my@pass/word')
#     -s, --sleep=S                    Sleep for S seconds after dumping (for debugging) # 导出后的休眠时间
#     -c, --count=S                    Chunk size (default: 10000) # 分块大小，默认10000
#     -f, --filter=S                   Filter selected keys (passed directly to redis' KEYS command) # 导出时的过滤器
#     -b, --base64                     Encode key values as base64 (useful for binary values)
#     -O, --without_optimizations      Disable run time optimizations # 禁用运行时优化
#     -V, --version                    Display version # 显示版本
#     -D, --debug       # 开启测试
#         --nosafe


# 本地Redis测试，运行在6379端口上，密码为foobared
# redis-dump -u :foobared@localhost:6379
# 没有密码，可以不加密码前缀
# redis-dump -u localhost:6379
# 运行后，可将本地0至15号数据库所有数据输出：
{"db":0,"key":"name","ttl":-1,"type":"string","value":"James","size":5}
# 每条数据包含6个字段，db即数据库代号，key即键名，ttl即该键值对的有效时间，type即键值类型，value即内容，size即占用空间
# 想要输出为JSON行文件：
# redis-dump -u:foobared@local:6379 > ./redis_data.jl


# 使用-d参数指定某个数据库的导出
# redis-dump -u :foobared@localhost:6379 -d 1 > ./redis_data.jl

# 只想导出特定的内容，想以adsl开头的数据，可以加入-f参数用来过滤
# redis-dump -u :foobared@localhost:6379 -f adsl:* > ./redis.data.jl
# 其中-f参数即Redis的keys命令的参数


# redis-load
# redis-load -h
# Usage: C:/Ruby24-x64/bin/redis-load [global options] COMMAND [command options]
#     -u, --uri=S                      Redis URI (e.g. redis://hostname[:port])
#     -d, --database=S                 Redis database (e.g. -d 15)
#     -a, --password=S                 Redis password (e.g. -a 'my@pass/word')
#     -s, --sleep=S                    Sleep for S seconds after dumping (for debugging)
#     -b, --base64                     Decode key values from base64 (used with redis-dump -b)
#     -n, --no_check_utf8
#     -V, --version                    Display version
#     -D, --debug
#         --nosafe
# -u代表Redis连接字符串；-d代表数据库代号，默认是全部，-s代表导出后的休眠时间，-n代表不检测UTF-8编码；
# -V表示显示版本；-D表示开启调试
# 将JSON行文件导入到Redis数据库中
# < redis_data.json redis-load -u :foobared@localhost:6379      # 成功将JSON行文件导入行文件导入到数据库中
# cat redis_data.json | redis -load -u :foobared@localhost:6379
# 会利用Redis实现很多架构，如维护代理池、Cookies池、ADSL拨号代理词、Scrapy-Redis分布式架构
