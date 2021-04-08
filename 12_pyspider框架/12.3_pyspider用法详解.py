# 1.命令行：除pyspider all启动pyspide，还有很多可配置参数
# 完整命令行结构：pyspider [OPTIONS] COMMAND [ARGS]
# OPTIONS为可选参数，可指定如下参数：
# Options：
# -c, --config FILENAME     指定配置文件名称
# --logging-config TEXT     日志配置文件名称，默认：pyspider/pyspider/logging.conf
# debug                     开启调试模式
# --queue-maxsize INTEGER   队列的最大长度
# --taskdb TEXT             projectdb的数据库连接字符串，默认：sqlite
# --resultdb TEXT           resultdb的数据库连接字符串，默认：sqlite
# --message-queue TEXT      消息队列连接字符串，默认：multiprocessing.Queue
# --phantomjs-proxy TEXT    PhantomJS使用的代理，ip：port的形式
# --data-path TEXT          数据库存放的路径
# --version                 pyspider的版本
# --help                    显示帮助信息


# 2.crawl方法：实现了新请求的生成，只指定了URL和Callback。
# url：是爬取时的URL，可以定义为单个URL字符串，也可以定义成URL列表
# callback：是回调函数，指定该URL对应的响应内容用哪个来解析
def on_start(self):
    self.crawl('http://scrapy.org/', callback=self.index_page)
# 指定callback为index_page，代表爬取http://scrapy.org/链接得到的响应会用index_page方法来解析
# index_page方法的第一个参数是响应对象，
def index_page(self,response):
    pass
# response参数是请求URL得到的响应对象，可以直接在index_page方法中实现页面的解析。


# 3.任务区分：判断两个任务是否重复，是该任务对应的URL的MD5值作为任务的唯一ID，如果ID相同，那么判定相同，其中一个不会爬取
# 很多情况下，请求的链接是同一个，但POST参数不同。可重写task_id方法，改变ID的计算方式来实现不同任务的区分
import json
from pyspider.libs.utils import md5string

def get_taskid(self, task): # 重写get_taskid方法
    return md5string(task['url']+json.dumps(task['fetch'].get('data', ''))) # 利用URl和POST参数生成ID，
# URL相同，POST参数不同，两个任务的ID就不同，就不会被识别成重复任务

# 4.全局配置：使用crawl_config指定全局配置，配置中的参数会和crawl方法创建任务时的参数合并。全局配置一个Headers
class Handler(BaseHandler):
    crawl_config = {
        'headers': {
            'User-Agent': 'GoogleBot',
        }
    }

# 5.定时爬取：通过every属性设置爬取的时间间隔：
@every(minutes=24 * 60) # 设置每天执行一次爬取
def on_start(self):
    for url in urllist:
        self.crawl(url, callback=self.index_page)

# 有效时间设置得比重复时间更短，才可以实现定时爬取：
@every(minutes=24 * 60)
def on_start(self):
    self.crawl('http://www.example.org/', callback=self.index_page)

@config(age=10 * 24 * 60 * 60)  # 任务过期时间为10天，自动爬取时间间隔为1天。第二次尝试重新爬取时，pyspider检测到此任务未过期
def index_page(self):
    pass    # 不会执行爬取，需要将age设置得小于定时时间

# 6.项目状态：每个项目都有6个状态：TODO、STOP、CHECKING、RUNNING、PAUSE
# TODO：项目刚被创建还未实现的状态
# STOP：想停止项目的抓取，设置为STOP
# CHECKING：正在运行的项目被修改后就会变成CHECHING，或中途出错需要调整时
# DEBUG/RUNNING：对项目运行没有影响，设置为任意一个，都可以运行，但是可用来区分是否已经通过测试
# PAUSE：爬取过程出现连续多次错误，会自动设置为PAUSE，等待一定时间后继续爬取

# 7.抓取进度：抓取时，可看到抓取进度，progress会显示4个进度条，5m、1h、1d：5分、1小时、1天内的请求情况，all所有请求情况
# 蓝色请求代表等待被执行的任务、绿色代表成功的任务、黄色代表请求失败后等待重试的任务、红色代表失败次数过多而被忽略任务

# 8.删除项目：没有直接删除项目的选项。要删除项目，将项目的状态设置为STOP，将分组名称设置为delete，等待24小时，会自动删除

# 9.pyspider官方文档：http://docs.pyspider.org/