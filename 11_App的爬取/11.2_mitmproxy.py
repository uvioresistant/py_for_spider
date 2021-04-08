# mitmproxy 是支持HTTP和HTTPS的抓包程序，类似Fiddler、Charles的功能，是控制台的形式操作
# mitmproxy还有两个关联组件，一个是mitmdump，是mitmproxy的命令行接口，可以对接Python脚本，用Python实现监听后的处理。
# 另一个是mitmweb，是一个Web程序，可以清楚观察mitmproxy捕获的请求

# 1.准备：安装好mitmproxy，且手机和PC处于同一局域网下，同事配置好了mitmproxy的CA证书

# 2.mitmproxy功能：
# 拦截HTTP和HTTPS请求和响应
# 保存HTTP会话并进行分析
# 模拟客户端发起请求，模拟服务端返回响应
# 利用反向代理将流量转发给指定的服务器
# 支持Mac和Linux上的透明代理
#利用Python对HTTP请求和响应进行实时处理

# 3.抓包原理：mitmproxy运行与PC上，在8080端口运行，开启一个代理服务，此服务实际上是一个HTTP/HTTPS的代理
# mitmproxy起了中间人的作用，抓取所有，手机访问互联网时，流量数据包会流经mitmproxy，mitproxy在转发数据包到真实服务器，返回同理
# 此过程还可对接mitmdump，抓取到的Request和Response具体内容可以直接用Python处理，可以直接解析，然后存入数据库

# 4.设置代理：
# 运行mitmproxy，启动命令：mitmproxy，会在8080端口运行一个代理服务

# 或启动mitmdump，也会监听8080端口

# 手机和PC链接在同一局域网，设置代理为当前代理，查看PC当前局域网IP，Windows：ipconfig，Linux：ifconfig，手机设置192. . .

# 5.使用mitmproxy:运行命令：mitmproxy，设置成功后，只需在手机游览器访问任意网页或浏览任意App即可，
# 每个请求开头都有GET或POST，是各个请求的请求方式，紧接的是请求的URL，第二行开头数字是请求对应的响应状态码，后面是响应内容类型
# 想查看某个请求的详情，可以敲击回车，进入请求详情页面，可以看到Headers的详细信息，Host、Cookies、User-Agent
# 最上方是Request、Response、Detail的列表，点击TAB，可查看请求对应的响应详情
# mitmproxy提供命令行式的编辑功能，可在此页面中重新编辑请求，敲击e键即可进入编辑功能，输入要编辑内容名称的首字母
# 敲击q，修改GET请求参数Query，没有任何参数，可以敲击a来增加一行，即可输入参数对应的Key和Value
# esc和q，返回之前页面，e和p修改Path，敲击a增加Path内容，修改为s，esc和q返回，
# 可看到最上面的请求链接变为https://www.baidu.com/s?wd=NBA,访问页面，可看到搜索NBA关键词的搜索结果，敲击a保存修改，r重新发请求
# 可看到上方请求方式前多了一个回旋箭头，说明重新执行了修改后的请求，再观察响应体内容，可看到搜索NBA的页面结果的源代码
# mitmproxy的强大在于另一个工具mitmdump，可以直接对接Python，对请求进行处理

# 6.mitmdump，是mitmproxy的命令行接口，可以对接Python对请求进行处理，可以不用手动截获和分析HTTP请求和响应，只需写好请求和响应
# 的处理逻辑即可，还可实现数据的解析、存储等，这些过程都可通过Python实现
# 使用命令启动mitmproxy，把截获的数据保存到文件中：mitmdump -w outfile,且outfile名称任意，截获的数据都会保存到此文件中
# 指定脚本来处理截获的数据，使用-s参数即可：mitmdump -s script.py,指定当前处理脚本为script.py，需要放置在当前命令执行的目录下
# 脚本里写入如下代码:
def request(flow):  # 定义request方法，参数flow，其实是一个HTTPFlow对象
    flow.request.headers['User-Agent'] = 'MitmProxy' # 通过request属性即可获取到当前请求对象，
    print(flow.request.headers) # 打印输出请求的请求头，将请求头的User-Agent修改成MitmProxy
# 运行后，在手机端访问http:/httpbin.org/get，
# 手机端返回结果的Headers实际上就是请求的Headers，User-Agent被修改成了mitmproxy
# PC控制台输出修改后的Headers内容，User-Agent内容是mitmproxy
# 三行代码可以完成对请求的改写，print方法输出结果可以呈现在PC端控制台，可以方便进行调试

# 日志输出：mitmdump提供了专门的日志输出功能：可设定不同级别以不同颜色输出结果
from mitmproxy import ctx   # 调用了ctx模块，有一个log功能，调用不同的输出方法，可输出不同颜色的结果，方便调试

def request(flow):
    flow.request.headers['User-Agent'] = 'MitmProxy'
    ctx.log.info(str(flow.request.headers))     # info方法输出内容是白色
    ctx.log.warn(str(flow.request.headers))     # warn方法输出内容是黄色
    ctx.log.error(str(flow.request.headers))    # error方法输出内容是红色
# 不同颜色对应不同级别的输出，可以将不同的结果合理划分级别输出，更方便查看调试信息

# Request：常用功能
from mitmproxy import ctx

def request(flow):
    request = flow.request
    info = ctx.log.info
    info(request.url)
    info(str(request.headers))
    info(str(request.cookies))
    info(request.host)
    info(request.method)
    info(str(request.port))
    info(request.scheme)
# 结果中分别输出了请求链接、请求头、请求Cookies、请求Host、请求方法、请求端口、请求协议
# 还可以对任意属性进行修改，就像修改Headers一样，直接赋值即可，
# 修改URL脚本：
def requeset(flow):
    url = 'https://httpbin.org/get'
    flow.request.url = url
# 手机端浏览器最上方还是百度URL，但是页面已经变成了httpbin.org页面，Cookies还是百度的Cookies，只是用简单的脚本就把请求修改为
# 其他的站点，通过此方式修改和伪造请求变得轻而易举
# 了解了基本用法，会很容易获取和修改Request的任意内容，可以用修改Cookies/添加代理等方式来规避反爬

# 响应：对于爬虫，更加关心的其实是响应的内容，mitmdump也提供了对应的处理接口与，就是response方法
from mitmproxy import ctx

def response(flow):
    response = flow.response
    info = ctx.log.info
    info(str(response.status_code)) # 打印输出响应的status_code
    info(str(response.headers))     # 打印输出响应的headers
    info(str(response.cookies))     # 打印输出响应的cookies
    info(str(response.text))        # 打印输出响应的text，最主要的text属性就是网页的源代码
# 脚本修改为如上内容，手机访问http://httpbin.org/get
# 通过response方法获取每个请求的响应内容，在进行响应的信息提取和存储，就成功完成爬取了
