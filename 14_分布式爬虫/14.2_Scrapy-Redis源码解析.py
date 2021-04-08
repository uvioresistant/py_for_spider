# Scrapy-Redis库已经提供了Scrapy分布式的队列、调度器、去重等功能，GitHub地址：https://github.com/rmax/scrapy-redis
# 1.获取源码：克隆源码，执行命令： 核心源码在scrapy-redis/src/scrapy_redis目录下
git clone https://github.com/rmax/scrapy-redis.git

# 2.爬取队列：源码文件为queue.py，有三个队列的实现，首先实现一个父类Base，提供一些基本方法和属性：
class Base(object):
    """
    Per-spider base queue class
    """
    def __init__(self, server, spider, key, serializer=None):
        if serializer is None:
            serializer = picklecompat
        if not hasattr(serializer, 'loads'):
            raise TypeError("serializer dose not implement 'loads' function:%r" % serializer)
        if not hasattr(serializer, 'dumps'):
            raise TypeError("serializer '%s' does not implement 'dumps' function: %r" % serializer)
        self.server = server
        self.spider = spider
        self.key = key % {'spider': spider.name}
        self.serializer = serializer

    def _encode_request(self, request): # 要把一个Request对象存储到数据库中，但数据库无法直接存储对象，先要将Request序列化
        obj = request_to_dict(request, self.spider) # 成字符串，_encode_request可实现序列化
        return self.serializer.dumps(obj)

    def _decode_requeset(self, encoded_request):    # _decode_request可实现反序列化，此过程利用pickle库来实现
        obj = self.serializer.loads(encoded_request)
        return request_from_dict(obj, self.spider)

    def __len__(self):
        """Return the length of the queue"""
        raise NotImplementedError

    def push(self, request):    # 队列Queue在调用push方法将Request存入数据库时，调用_encode_request进行序列化
        """Push a request"""
        raise NotImplementedError

    def pop(self, timeout=0):   # 调用pop取出Request时，会调用_decode_request进行反序列化
        """Pop a request"""
        raise NotImplementedError

    def clear(self):
        """Clear queue/stack"""
        self.server.delete(self.key)
# 父类中，__len__、push和pop三个方法都是未实现的，三个方法直接抛出NotImplementedError异常，因此这个类不能直接使用。
# 必须实现一个子类来重写这三个方法，不同的子类就会有不同的实现和不同的功能
# 接下来定义一些子类来继承Base类，并重写这几个犯法。源码中有三个子类的实现，分别是：
class FifOQueue(Base):  # 该类继承了Base类，重写三个方法，都是对server对象进行操作
    """
    Per-spider FIFO queue
    """
    def __len__(self):  # 获取列表的长度
        """Return the length of the queue"""
        return self.server.llen(self.key)   # server对象就是一个Redis连接对象，可以直接调用其操作Redis的方法对数据库操作
    # 操作方法有llen、lpush、rpop等，就代表此爬取队列使用了Redis的列表，序列化后的Request会存入列表中

    def push(self, request):
        """Push a request"""
        self.server.lpush(self.key, self._encode_request(request))  # 调用lpush操作,从列表左侧存入数据

    def pop(self, timeout=0):
        """Pop a request"""
        if timeout > 0:
            data = self.server.brpop(self.key, timeout)
            if isinstance(data, tuple):
                data = data[1]
        else:
            data = self.server.rpop(self.key)   # 调用rpop操作，从列表右侧取出数据
        if data:
            return self._decode_requeset(data)
# Request在列表中的存取顺序是左侧进，右侧出，先进先出（FIFO），此类的名称就叫做FifoQueue
# 与之相反的实现类，LifoQueue：先进后出（LIFO），类名称LifoQueue，类似栈，也可称作StackQueue
class LifoQueue(Base):  # 该类继承了Base类，重写三个方法，都是对server对象进行操作
    """
    Per-spider Lifo queue
    """

    def __len__(self):  # 获取列表的长度
        """Return the length of the stack"""
        return self.server.llen(self.key)  # server对象就是一个Redis连接对象，可以直接调用其操作Redis的方法对数据库操作

    # 操作方法有llen、lpush、rpop等，就代表此爬取队列使用了Redis的列表，序列化后的Request会存入列表中

    def push(self, request):
        """Push a request"""
        self.server.lpush(self.key, self._encode_request(request))  # 调用lpush操作,从列表左侧存入数据

    def pop(self, timeout=0):
        """Pop a request"""
        if timeout > 0:
            data = self.server.brpop(self.key, timeout)
            if isinstance(data, tuple):
                data = data[1]
        else:
            data = self.server.lpop(self.key)   # 调用lpop操作，从列表左侧取出数据
        if data:
            return self._decode_requeset(data)

# 源码中还有一个子类PriorityQueue，优先级队列：
class PriorityQueue(Base):
    """Per-spider priority queue abstraction using redis' sorted set"""
    def __len__(self):  # 使用了server对象的zcard操作,存储结果是有序集合，每个元素都可以设置一个分数，分数就代表优先级
        """Return the length of the queue"""
        return self.server.zcard(self.key)  # 调用了zcard操作，返回的就是有序集合的大小，就是爬取队列的长度

    def push(self, requesst):   # 使用了server对象的zadd操作
        """Push a request"""
        data = self._encode_request(requesst)
        score = -request.priority   # push数低的会排在集合的前面，高优先级的Request会在集合的最前面
        self.server.execute_command('ZADD', self.key, score, data)  #

    def pop(self, timeout=0):   # 使用了server对象的zrange操作
        """
        Pop a request
        timeout not support in this queue class
        """
        pipe = self.server.pipeline()
        pipe.multi()
        pipe.zrange(self.key, 0, 0).zremrangebrrank(self.key, 0, 0) # 调用zrange操作，将这个元素删除，完成取出并删除操作
        results, count = pipe.execute()
        if results:
            return self._decode_requeset(results[0])
# 次队列是默认使用的对了，即爬取队列默认是使用有序集合来存储的

# 3.去重过滤：Scrapy的去重是利用集合来实现的，在Scrapy分布式中的去重就需要利用共享的集合，使用Redis中的集合数据结构，
# 源码是dupefilter.py，内部实现了一个RFPDupeFilter类：
class RFPDupeFilter(BaseDupeFilter):
    """Redis-based request duplicates filter.
    This class can also be used with default Scrapy's scheduler.
    """
    logger = logger
    def __init__(self, server, key, debug=False):
        """Initialize the duplicates filter.
        Parameters
        ----------
        server : redis.StrictRedis
            The redis server instance.
        key : str
            Redis key Where to store fingerprints.
        debug : bool, optional
            Whether to log filtered requests.
        """
        self.server = server
        self.key = key
        self.debug = debug
        self.logdupes = True
        ...

    def request_seen(selfself, request):    # 实现了一个request_seen方法，和Scrapy中的request_seen方法类似
        """Returns True if request was already seen.
        Parameters
        ----------
        request : scrapy.http.Request
        Returns
        -------
        bool
        """
        fp = self.request_fingerprint(request)
        added = self.server.sadd(self.key, fp)  # 集合使用的是server对象的sadd操作，就是集合不再是一个简单数据结构了，
                                                # 而是换成了数据库的存储方式
        return added == 0

    def request_fingerprint(self, request): # 鉴别重复的方式还是使用指纹，依靠request_fingerprint方法获取
        """Returns a fingerprint for a given request."""
        return request_fingerprint(request) # 获取指纹后直接向集合添加指纹，添加成功，说明原本不存在于集合中，返回值1
        ...

# 4.调度器：Scrapy-Redis还实现了配合Queue、DupeFilter使用的调度器Scheduler，源文件scheduler.py，可指定一些配置，
# 如SCHEDULER_FLUSH_ON_START（是否在爬取开始时清空爬取队列）、SCHEDULER_PERSIST(是否爬取解锁后保持爬取队列不清除)
# 可以在settings.py中只有配置，调度器很好地实现了对接，两个核心存取方法：
def enqueue_request(self, request):     # enqueue_request可向队列中添加Request
    if not request.dont_filter and self.df.request_seen(request):
        self.df.log(request, self.spider)
        return False
    if self.stats:
        self.stats.inc_value('scheduler/enqueued/redis', spider=self.spider)
        self.queue.push(request)    # 核心操作就是调用Queue的push操作，还有一些统计和日志操作
        return True

def next_requst(self):  # 从队列中取Request
    block_pop_timeout = self.idle_before_close
    reuest = self.queue.pop(block_pop_timeout)  # 核心操作就是调用Queue的pop操作
    if request and self.stats:  # 此时如果队列中还有Request，直接取出来，爬取继续，如果队列为空，爬取则重新开始
        self.stats.inc_value('scheduler/dequeued/redis', spider=self.spider)
    return request

# 5.总结：三个分布式问题解决：
# a.爬取队列的实现：提供了三种队列，使用了Redis的列表或有序集合来维护
# b.去重的实现：使用Redis的集合来保存Request的指纹，已提供重复过滤
# c.中断后重新爬取的实现：中断后Redis的队列没有清空，爬取再次启动时，调度器的next_request会从队列中取到下一个Request，爬取继续

