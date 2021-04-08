# Scrapy-Redis的去重机制，将Request的指纹存储到了Redis集合中，每个指纹长度40，每一位都是16进制数。
# 计算此方式耗费的存储空间，每个16进制占用4b，1个指纹在哪用空间20B，1万个200KB，1亿个占用2GB，爬取数量达到上亿级别，Redis占用
# 的内从就会变得很大，且仅仅是指纹的存储。
# Redis还存储了爬取队列，内存占用会进一步提高，当爬取达到亿级别规模时，Scrapy-Redis提供的集合去重已经不能满足要求，需要使用
# 一个更加节省内存管的去重算法Bloom Filter

# 1.Bloom Filter：布隆过滤器，用来检测一个元素是否在一个集合中。空间利用率很高，可大大节省存储空间，使用位数组表示一个待检测
# 集合，可以快速通过概率算法判断一个元素是否存在于这个集合中，利用该算法可以实现去重效果

# 2.Bloom Filter的算法：使用位数组来辅助实现检测判断，初始状态下，声明一个包含m位的位数组，所有位都是0，即待检测集合，
# 表示为S={x1, x2, ..., xn},需要做的就是检测一个x是否已经存在于集合S中，
# 在Bloom Filter算法中，首先使用k个相互独立、随机的散列函数来将集合S中的每个元素x1、x2、...xn映射到长度为m的位数组上，散列
# 函数得到结果记作位置索引，然后将位数组该位置索引的位置1.如取k为3，表示有三个散列函数，x1经过三个散列函数映射得到的结果分别为
# 1、4、8，x2经过三个散列函数映射得到的结果分别为4、6、10,则位数组的1、 4、 6 、8 、10五位就会置为1
# 如果有一个新的元素x，要判断x是否属于S集合，仍然用k个散列函数对x求映射结果。如果所有结果对应的位数组位置均为1，那么x属于S这个
# 集合；如果有一个不为1，则x不属于S集合
# 如，新元素x经过三个散列函数映射的结果为4 、 6 、8，对应的位置均为1，则x属于S集合。如果结果为4、 6、 7，而7对应的位置为0，则
# x不属于S集合，m、n、k满足关系m>nk,即位数组的长度m要比集合元素n和散列函数k的积还要打
# 这样的判定方法很高效，但是也有代价，可能吧不属于这个集合的元素误认为属于这个集合。错误率：1-1/m的kn次方
# 一个不属于S的元素x如果误判定为在S中，这个概率就是k次散列运算得到的结果对应的位数组位置都为1，误判概率为[(1-(1-1/m)^(kn)]^k
# 根据lim(1-1/x)^(-x)=e,误判概率转换为[(1-(1-1/m)^(kn)]^k,给定m、n时，求出使得f最小化的k值为：0.7m/n
# 当k值确定时，随着m/n的增大，误判概率逐渐变小。当m/n的值确定时，当k月靠近最优K值，误判概率越小。
# 误判概率总体来看是绩效的，在容忍此误判概率的情况下，大幅减小存储空间和判定速度是完全值得的

# 3.对接Scrapy-Redis：实现Bloom Filter时，首先保证不能破坏Scrapy-Redis分布式爬取的运行架构。
# 需要修改Scrapy-Redis源码，将它的去重类替换掉。同时，Bloom Filter的实现需借助于一个位数组，位数组的维护直接使用Redis。
# 首先实现一个基本的散列算法，将一个值经过散列运算后映射到一个m位数组的某一位上：
class HashMap(object):  # 新建一个HashMap类
    def __init__(self, m, seed):    # 构造函数传入两个值，一是m位数组的位数，另一个是种子值seed
        self.m = m
        self.seed = seed    # 不同的散列函数需要有不同的seed，可保证不同的散列函数结果不会碰撞

    def hash(self, value):  # value是要被处理的内容，
        """
        Hash Algorithm
        :param value: Value
        :return: Hash Value
        """
        ret = 0
        for i in range(len(value)): # 遍历了value的每一位
            ret += self.seed * ret + ord(value[i])  # 利用ord方法取到每一位的ASCII码值，混淆seed进行迭代求和计算，得到一个值
            # 值的结果就由value和seed唯一确定
        return (self.m - 1) & ret   # 再将该数值和m进行按位，与运算，获取到m位数组的映射结果，实现字符串和seed确定的散列函数
    # m固定时，seed值相同，散列函数就是相同的，相同的value必然会映射到相同的位置。
    # 如果要构造几个不同的散列函数，只需改变其seed就好了，以上便是一个简易的散列函数的实现

# 接下来再实现Bloom Filter，需用到k个散列函数，对这几个散列函数指定相同的m值和不同的seed值，构造：
BLOOMFILTER_HASH_NUMBER = 6 # 传入散列函数的个数，用来生成几个不同的seed
BLOOMFILTER_BIT = 30

class BloomFilter(object):
    def __init__(self, server, key, bit=BLOOMFILTER_BIT, hash_number=BLOOMFILTER_HASH_NUMBER):
        """
        Initialize BloomFilter
        :param server: Redis Server
        :param key: BloomFilter Key
        :param bit: m = 2 ^ bit
        :param hash_number: the number of hash function
        """
        # default to 1<< 30 = 10,7374,1824 = 2^30 = 128MB,max filter 2^30/hash_number = 1,7895,6870 fingerprints
        self.m = 1 << bit
        self.seeds = range(hash_number) # 用不同的seed来定义不同的散列函数，就可以构造一个散列函数列表
        self.maps = [HashMap(self.m, seed) for seed in self.seeds]  # 遍历seed，构造带有不同seed值的HashMap对象，将
                                                                    # HashMap对象保存成变量maps供后续使用
        self.server = server    # server就是Redis连接对象
        self.key = key  # key就是m位数组的名称
# 由于需要亿级别的数据去重，即算法中的n为1亿以上，散列函数的个数k大约取10左右的量级。而m>kn,这里的m值大约保底在10亿，
# 数值比较大，所以 用移位操作来实现，传入位数bit，定义为30，做移位操作1<<30，相当于2的30次方，等于1073741824，量级在10亿左右
# 由于是位数组，所以位数组占用的大小就是2^30 b=128MB,而Scrapy-Redis去重的占用空间大约在2GB左右，故Bloom Filter空间利用率高

# 接下来实现关键的两个方法：一、判定元素是否重复的方法exists；二、天剑元素到集合中的方法insert：
def exists(self, value):    # 判定是否重复的逻辑，方法参数value为待判断的元素
    """
    if value exists
    :param value:
    :return:
    """
    if not value:
        return False
    exist = 1   # 首先定义变量exist
    for map in self.maps:  # 遍历所有散列函数对value进行散列运算，得到映射位置
        offset = map.hash(value)
        exist = exist & self.server.getbit(self.key, offset)    # 用getbit方法取得映射位置的结果，循环进行与运算，只有
    # 每次getbit得到的结果都为1时，最后的exist采薇True，代表value属于这个集合，只要有1次getbit得到结果为0，最终exist为False
    return exist

def insert(self, value):    # Bloom Filter算法会逐个调用散列函数对放入集合中的元素进行运算，得到在m位位数组中的映射位置
                            # 将位数组对应的位置置1
    """
    add value to bloom
    :param value:
    :return:
    """
    for f in self.maps:     # 遍历初始化好的散列函数，
        offset = f.hash(value)  # 调用hash方法算出映射位置offset
        self.server.setbit(self.key, offset, 1) # 再利用Redis的setbit方法将该位，置1

# Bloom Filter实现完成，用例子来测试：
conn = StrictRedis(host='localhost', port=6379, password='foobared')    # 首先定义Redis连接对象
bf = BloomFilter(conn, 'testbf', 5, 6)  # 传递给Bloom Filter，避免内存占用过大，传的位数bit较小，为5，散列函数个数设置为6
bf.insert('Hello')  # 调用insert方法插入Hello
bf.insert('World')  # 调用insert方法插入World
result = bf.exists('Hello')     # 判断Hello字符串是否存在
print(bool(result))
result = bf.exists('Python')    # 判断Python字符串是否存在
print(bool(result))

# 继续修改Scrapy-Redis源码，将它的dupefilter逻辑替换为Bloom Filter的逻辑，主要是修改RFPDupeFilter类的request_seen方法：
def request_seen(self, request):
    fp = self.request_fingerprint(request)  # 利用request_fingerprint方法获取Request指纹
    if self.bf.exists(fp):  # 调用Bloom Filter的exists方法判定该指纹是否存在，
        return True # 存在，说明Request重复，返回True
    self.bf.insert(fp)  # 否则调用Bloom Filter的insert方法将该指纹添加
    return False    # 并返回False
# 成功利用Bloom Filter替换了Scrapy-Redis的集合去重

# 对Bloom Filter的初始化定义，可将__init__方法修改为：
def __init__(self, server, key, debug, bit, hash_number):
    self.server = server
    self.key = key
    self.debug = debug
    self.bit = bit          # bit需使用from_settings方法传递
    self.hash_number = hash_number  # hash_number需使用from_settings方法传递
    self.logdupes = True
    self.bf = BloomFilter(server, self.key, bit, hash_number)
# bit、hash_number需使用from_settings方法传递：
@classmethod
def from_settings(cls, settings):
    server = get_redis_from_settings(settings)
    key = defaults.DUPEFILTER_KEY % {'timestamp': int(time.time())}
    debug = settings.getbool('DUPEFILTER_DEBUG', DUPEFILTER_DEBUG)
    bit = settings.getint('BLOOMFILTER_BIT', BLOOMFILTER_HASH_NUMBER)
    return cls(server, key=key, debug=debug, bit=bit, hash_number=hash_number)
# 常量DUPEFILTER_DEBUG和BLOOMFILTER_BIT统一定义在defaults.py中，默认：
BLOOMFILTER_HASH_NUMBER = 6
BLOOMFILTER_BIT = 30
# 实现Bloom Filter和Scrapy-Redis的对接

# 4.代码地址：https://gibhub.com/Python3WebSpider/ScrapyRedisBloomFilter

# 代码已经打包成一个Py报并发布到PyPi，链接：https://pypi.python.org/pypi/scrapy-redis-bloomfilter，
# 可直接使用ScrapyRedisBloomFilter，无需自己实现
# 可直接用pip来安装：
pip3 install scrapy-redis-bloomfilter
# 使用方法和Scrapy-Redis基本相似，几个关键配置
# 去重类，要使用BloomFilter请替换DUPEFILTER_CLASS
DUPEFILTER_CLASS = "scrapy_redis_bloomfilter.dupefilter.RFPDupeFilter"
# 散列函数的个数，默认为6，可执行修改
BLOOMFILTER_HASH_NUMBER = 6
# Bloom Filter的bit传参数，默认30，占用128MB空间，去重量级1亿,如果对应爬取量级在10亿、20亿甚至100亿，务必将此参数对应调高
BLOOMFILTER_BIT = 30

# 6.测试：源代码附有一个测试项目，放在tests文件夹，该项目使用了ScrapyRedisBloomFilter来去重，Spider实现：
from scrapy import Request, Spider

class TestSpider(Spider):
    name = 'test'
    name_url = 'https://www.baidu.com/s?wd='

    def start_requests(self):
        for i in range(10): # start_requests首先循环10次，
            url = self.base_url + str(i)    # 构造参数为0~9的URl
            yield Request(url, callback=self.parse)

        # Here contains 10 duplicated Requests
        for i in range(100):    # 然后重新循环100次
            url = self.base_url + str(i)    # 构造参数为0~99的URl
            yield Request(url, callbacck=self.parse)    # 包含10个重复的Request

    def parse(self, response):
        self.logger.debug('Response of ' + response.url)
# 运行项目测试一下：
scrapy crawl test
# 统计的第一行的结果：
'bloomfilter/filtered': 10, # 就是Bloom Filter 过滤后的统计结果，过滤个数为10个，就是成功将重复的10个Request识别出来了，通过
# Bloom Filter的使用可以大大节省Redis内存，在数据量大的情况下推荐此方案
