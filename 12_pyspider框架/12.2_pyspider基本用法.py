# 1.目标：爬取去哪儿网的旅游攻略，链接http://travel.qunar.com/travelbook/list.htm,将所有攻略的作者、标题、出发日期、
# 人均费用、攻略正文保存下来，存储到MongoDB

# 2.准备工作：安装了pyspider和PhantomJS，安装MongoDB并正常运行服务，安装PyMongo库

# 3.启动pyspider：执行命令pyspider all
# 启动pyspider所有组件，包括PhantomJS、ResulWorker、Processer、Fetcher、Scheduler、WebUi，都是pyspider运行必备组件
# 最后一行输出提示WebUI运行在5000端口，打开浏览器，输入链接http://localhost:5000会看到页面，此页面便是pyspider的WebUI
# 用它来管理项目、编写代码、在线调试、监控任务

# 4.创建项目：右边Create按钮，弹出的浮窗里输入项目的名称和爬取的链接，成功创建了一个项目，pyspider的项目编辑和调试页面
# 左侧是代码的调试页面，run单步调试爬虫程序，左侧下半部分可以预览当前的爬取页面。右侧是代码编辑页面，可以直接编辑代码和保存代码
# 右侧，pyspider已经生成了一段代码：

from pyspider.libs.base_handler import *


class Handler(BaseHandler): # Handler是pyspider爬虫主类，可在此定义爬取、解析、存储的逻辑，整个爬虫功能只需一个Handler即完成
    crawl_config = {    # crawl_config将本项目所有爬取配置统一定义到这里，如Headers、设置代理等，配置后全局生效
    }

    @every(minutes=24 * 60)
    def on_start(self): # 爬取入口，初始爬取请求会在这里产生
        self.crawl('http://travel.qunar.com/travelbook/list.htm', callback=self.index_page) # 通过调用crawl新建爬取请求
# 第一个参数是爬取的URL，自动替换成需定义的URL。crawl方法还有参数callback，指定页面爬取成功后用哪个方法解析，指定index_page
# 如果URL对应的页面爬取成功了，Response将交给index_page方法解析
    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response): # index_page方法恰好接受这个Response参数，Response对接了pyquery
        for each in response.doc('a[href^="http"]').items():    # 直接调用doc方法传入相应CSS选择器，想pyquery一样解析页面
# 代码中默认是a[href^="http"],即该方法解析了页面的所有链接，将链接遍历，再次调用crawl方法生成新的爬取请求
            self.crawl(each.attr.href, callback=self.detail_page)#再指定callback为detail_page，爬取成功调用detail_page解析

    @config(priority=2)
    def detail_page(self, response):    # detail_page接受Response作为参数，detail_page抓取的就是详情页信息，不生成新的请求
        return {
            "url": response.url,    # 只对Response对象做解析，解析后将结果以字典形式返回，也可以进行后续处理，保存到数据库
            "title": response.doc('title').text(),
        }

# 5.爬取首页：左栏右上角run按钮，可看到页面下方follows出现标注1，代表有新的爬取请求产生
# 左栏左上角出现当前run的配置文件，callback为on_start，说明点击run后实际是执行了on_start方法。
# on_start方法中，利用crawl方法生成一个爬取请求，下方follows部分数字1代表此爬取请求
# 点击下方follows，可看到生成的爬取请求的链接。每个链接右侧还有一个箭头按钮。
# 点击箭头，可对此链接进行爬取，就是爬取攻略的首页内容
# 上方callback已经变成了index_page，运行了index_page方法，接收到的response参数就是刚才生成的第一个爬取请求的Response对象
# index_page方法通过调用doc方法，传入提取所有a节点的CSS选择器，获取a节点的属性href，即获取第一个爬取页面中的所有链接
# 在index_page方法里遍历所有链接，同时调用crawl方法，把链接构造成新的爬取请求。即follows的数字标记，请求的URL呈现在当前页面
# 点击下方web按钮，可预览当前爬取结果的页面
# 当前看到的页面结果和浏览器看到的几乎完全一致，可方便查看页面请求的结果
# 点击html按钮可查看当前页面源代码，如需分析代码结构，可直接参考页面源码

# index_page方法提取了所有链接并生成了新的爬取请求，但只需攻略详情页面链接，修改index_page提取链接时抵达CSS选择器
# 切换到Web页面，找到攻略标题，点击下方enable css selector helper，点击标题，右侧代码选中要更改区域，点击左栏右箭头
# 此时上方出现标题的CSS选择器会被替换到右侧代码中，完成CSS选择器的替换

# 重新点击左栏右上角run，可重新执行index_page方法，此时follos变成了10，即提取的只有当前页面的10个攻略
# 抓取的指数第一页内容，还需抓取后续页面，还需一个爬取链接，即爬取下一页的攻略列表页面
# 在利用crawl添加下一页的爬取请求，在index_page里添加代码并保存：
next = response.doc('.next').attr.href  # 利用CSS选中下一页的链接，获取它的href属性，也就获取了页面的URL
self.crawl(next, callback=self.index_page)  # 将该URL传给crawl方法，同时指定回调函数，仍然指定为index_page方法
# 重新点击run，可以看到11个爬取请求。follows显示11，成功添加了下一页的爬取请求，完成索引列表页的解析过程

# 6.爬取详情页：任选一个详情页进入，点击前10个爬取请求中的任意一个右箭头，执行详情页的爬取
# 切换到Web页面预览效果，页面下拉后，头图中的一些图片一直加载中
# 查看源代码，没有看到img节点，原因是pyspider默认发送HTTP请求，不包含img节点，但在浏览器中看到了图片，图片是后期经过JS出现的
# 用pyspider内部对接的PhantomJS，修改一个参数即可
# 将index_page中生成抓取详情页的方法添加一个参数fetch_type，改写的index_page变为：
def index_page(self, response):
    for each in response.doc('li > .tit > a').items():
        self.crawl(each.attr.href, callback=self.detail_page, fetch_type='js')
    next = response.doc('.next').attr.href
    self.crawl(next, callback=self.index_page)
# 点击左栏上方的左箭头返回，重新调用index_page生成新的爬取详情页的Request，再点击新生成的详情页Request爬取按钮。
# 图片被成功渲染出来，启用了PhantomJS渲染后的结果，只需要添加一个fetch_type参数即可
# 最后将详情页中需要的信息提取出来，过程略。detail_page方法改写如下：
def detail_page(self, response):
    return {
        'url': response.url,    # 分别提取了页面链接
        'title': response.doc('#booktitle').text(),     # 标题
        'date': response.doc('.when .data').text(),     # 出行日期
        'day': response.doc('.howlong .data').text(),   # 出行天数
        'who': response.doc('.who .data').text(),       # 人物
        'text': response.doc('#b_panel_schedule').text(),   # 攻略正文
        'image': response.doc('.cover_img').attr.src    # 头图信息
    }
# 将这些信息构造成一个字典

# 7.启动爬虫：返回爬虫主页面，将爬虫的status设置成DEBUG或RUNNING，点击右侧的Run按钮可开始爬取
# 最左侧为定义项目的分组。rate/burst代表当前的爬取速率，rate代表1秒发出多少个请求，burst相当于流量控制中的令牌桶算法的令牌数
# rate和burst设置的越大，爬取速率越快，速率需要考虑本机性能和爬取过快被封的问题。
# process中的5m、1h、1d代表最近5分、1小时、1天内的请求情况，all代表所有请求情况。
# 请求有不同颜色表示，蓝色代表等待被执行的请求；绿色代表成功的请求；黄色的代表请求失败后等待重试的请求；红色代表失败过多被忽略
# 点击Active Tasks，可查看最近请求的详细状况
# 点击Result，可查看所有的爬取结果
# 点击右上角的JSON、CSV可获取数据

# 代码地址：https://github.com/Python3WebSpider/Qunar