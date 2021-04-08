# Splash是JS渲染服务，是一个带有HTTP API的轻量级浏览器，对接了Python中的Twisted和QT库，可以实现动态渲染页面的抓取
# 利用Splash，可以实现如下功能：
# 异步方式处理多个网页渲染过程
# 获取渲染后的页面的源代码或截图
# 通过关闭图片渲染或者使用adblock规则来加快页面渲染速度
# 可执行特定的JS脚本
# 获取渲染的详细并通过HAR（HTTP Archive）格式呈现


# 通过Splash提供的Web页面来测试渲染过程
# 在本机8050端口上运行Splash服务，打开http://localhost:8050/看到Web页面
# 将输入框的内容改为https://www.baidu.com点击Render me阿牛开始渲染
# 网页的返回结果呈现了渲染截图、HAR加载统计数据、网页的源代码；
# 通过HAR可以看到，Splash执行了整个网页的渲染过程、包括CSS、JS过程
# 重新返回首页，可以看到实际上有一段脚本控制：
# function main(splash, args)
#     assert(splash:go(args.url))
#     assert(splash:wait(0.5))
#     return {
#         html = splash:html(),
#         png = splash:png(),
#         har = splash:har(),
#     }
# end
# 脚本为Lua语言写的脚本，大致了解到首先调用go方法加载页面，调用wait方法等待了一定时间，然后返回了页面的源码、截图和HAR信息
# 大体了解了Splash是通过Lua脚本来控制了页面的加载过程，加载过程完全模拟浏览器，最后可返回各种格式的结果


# 4.Splash Lua脚本
# Splash通过Lua脚本执行一系列渲染操作，可以用Splash模拟类似Chrome、PhantomJS操作
# Splash Lua脚本的入口和执行方式
# 入口及返回值
# function mian(splash,args)
#     splash:go("http://www.baidu.com")
#     splash:wait(0.5)
#     local title = splash:evaljs("document.title") # 通过evaljs方法传入JS脚本；document.title的执行结果就是返回网页标题
#     return {title=title}  # 执行完毕后将其赋值给一个title变量
# end
# 将代码粘贴到刚才打开的http://localhost:8050的代码编辑区域，点击Render me！按钮测试
# 定义的方法名称叫main，名称必须是固定的，Splash会默认调用这个方法
# 返回值既可以是字典形式，也可以是字符串形式，最后会转化为Splash HTTP Response
# function main(splash)
#    return {hello="world!"}
# end
# 返回了一个字典形式的内容
# function main(splash)
#     return 'hello'
# end
# 返回了一个字符串形式的内容


# 异步处理：Splash支持异步处理，没有显示回调方法，回调的跳转是在Splash内部完成的
# function main(splash, args)
#     local example_urls = {"www.baidu.com", "www.taobao.com", "www.zhihu.com"}
#     local urls = args.urls or example_urls
#     local results = {}
#     for index, url in ipairs(urls) do
#         local ok, reason = splash:go("http://" ..url) # Lua脚本中的字符串拼接使用..空字符，而不是+
#         if ok then
#             splash:wait(2)        # wait方法类似于Python中的sleep，参数为等待的秒数，Splash执行到时，会转而去处理其他任务
                                    # 指定的时间过后再回来继续处理
#             results[url] = splash:png()
#         end
#     end
#     return results
# end


# 5.Splash对象属性
# main方法的第一个参数是splash，类似于Selenium中的WebDriver对象，可以调用它的一些属性和方法来控制加载过程
# args：可以获取加载时配置的参数，如URL；若为GET请求，还可以获取GET请求参数；POST请求，可以获取表单提交的数据
# function main(splash, args)
#     local url = args.url  # 第二个参数args就相当于splash.args属性
# end


# js_enabled：是Splash的JS执行开关，可将其配置为true或false来控制是否执行JS代码，默认为true
# 禁止执行JS代码
# function main(splash, args)
# splash:go("https://www.baidu.com")
#     splash.js_enabled = false
#     local title = splash:evaljs("document.title")     # 重新调用evaljs方法执行JS代码，就会抛出异常
#     return {title=title}
# end
# 一般来说，不用设置，默认开启即可


# resource_timeout:可以设置加载的超时时间，单位是秒。设置为0或nil，代表不检测超时
# function main(splash)
#     splash.resource_timeout = 0.1     # 将超时时间设置为0.1秒，如果在0.1秒之间内没有得到响应，就会抛出异常
#     assert(splash:go('https://www.taobao.com'))
#     return splash:png()
# end
# 适合在网页加载速度较慢的情况下设置，如果超过某个时间无响应，则直接抛出异常并忽略即可


# images_enabled:可以设置图片是否加载，默认情况下是加载，禁用后，可以节省网络流量并提高网页加载速度，禁用可能会影响JS渲染
# function main(splash,args)
#     splash.images_enabled = false
#     assert(splash:go('https://www.jd.com'))
#     return {png=splash:png()}
# end
# 返回的页面截图就不会带有任何图片，加载速度也会快很多


# plugins_enabled:可以控制浏览器插件（如Flash）是否开启，默认情况下，属性是false，表示不开启
# splash.plugins_enabled = true/false


# scroll_position:控制页面上下或左右滚动，这是比较常用的属性
# function main(splash, args)
#     assert(splash:go('https://www.taobao.com'))
#     splash.scroll_position = {y=400}      # 可以控制页面向下滚动400像素值，如果页面左右滚动，可以传入x参数
#     return {png=splash:png()}
# end


# 6.Splash对象的方法
# 1)go：用来请求某个链接，而且可以模拟GET和POST请求，同时支持传入请求头、表单等数据
# ok, reason = splash:go{url, baseurl=nil, http_method="GET", body=nil,formata=nil}
# 参数说明如下：
# url:请求的URL
# baseurl:可选参数，默认为空，表示资源加载相对路径
# headers：请求头
# http_method:默认GET，同时支持POST
# body:发POST请求时的表单数据，使用的Content-type为application/x-www-form-urlencoded
# formdata:POST的时候表单数据，使用的Content-type为application/x-wwww-form-urlencoded

# # 返回结果是结果ok和原因reason的组合，如果ok为空，代表网页加载出现了错误，此时reason变量中包含了错误的原因，否则页面加载成功
# function main(splash, args)
#     local ok, reason = splash:go{"http://httpbin.org/post", http_method="POST", body="name=Germey"} # 模拟一个POST请求
#     if ok then
#         return splash:html()
#     end
# end


# 2)wait:此方法控制页面的等待时间
# ok, reason = splash:wait{time, cancel_on_redirect=false, cancel_on_error=true}
# time: 等待的秒数
# cancel_on_redirect: 可选参数，默认false，发生了重定向就停止等待，返回重定向结果
# cancel_on_error: 可选参数，默认false，如果发生了加载错误，就停止等待
# 返回结果是结果ok和原因reason的组合
# function main(splash)
#     splash:go("https://www.taobao.com") # 访问淘宝并等待2秒
#     splash:wait(2)
#     return {html=splash:html()} # 返回页面源代码的功能
# end


# 3)jsfunc：直接调用JS定义的方法，所调用的方法需要用双中括号包围，相当于实现了JS方法到Lua脚本的转换
# function main(splash, args)
#     local get_div_count = splash:jsfunc([[
#     function (){
#         var body = document.body;
#         var divs = body.getElementsByTagName('div');
#         return divs.length;
#     }
# ]])
# splash:go("https://www.baidu.com")
# return ("There are %s DIVs"):format(
#     get_div_count())
# end


# 4)evaljs: 执行JS并返回最后一条JS语句的返回结果
# result = slash:evaljs(js)
# 获取页面标题：
# local title = splash:evaljs("document.title")


# 5)runjs: 与evaljs功能类似，但是跟偏向于执行某些动作或申明某些方法
# function main(splash, args)
#     splash:go("https://www.baidu.com")
#     splash:runjs("foo = function(){ return 'bar'}") # runjs先声明了一个JS定义方法
#     local result = splash:evaljs("foo()")   # 通过evaljs来调用得到的结果
#     return result
# end


# 6)autoload：设置每个页面访问时自动加载的对象
# ok, reason = splash:autoload{source_or_url, source=nil, url=nil}
# 参数说明：
# source_or_url: JS代码或者JS库链接
# source：JS代码
# url：JS库链接
# 此方法只负责加载JS代码或库，不执行任何操作，如果要执行操作，可以调用evaljs或runjs方法
# function main(splash, args)
#     splash:autoload([[        # 调用autoload方法声明一个JS方法
#         function get_documet_title(){
#             return document.title;
#         }
#     ]])
#     splash:go("https://www.baidu.com")
#     return splash:evaljs("get_document_title()")  # 通过evaljs方法执行JS方法
# end


# 也可以使用autoload方法加载某些方法库，如jQuery
# function main(splash, args)
    # assert(splash:autoload("https://code.jquery.com/jquery-2.1.3.min.js"))
    # assert(splash:go("https://taobao.com"))
    # local version = splash:evaljs("$.fn.jquery")
    # return 'JQuery version: '.. version
# end


# 7)call_later:设置定时任务和延迟时间来实现任务延时执行，可以在执行前通过cancel方法重新执行定时任务
# function main(splash, args)
#     local snapshots = {}
#     local timer = splash:call_later(function()
#         snapshots["a"] = splash:png)
#         splash:wait(1.0)
#         snapshots["b"] = splash:png()
#     end, 0.2)     # 设置一个定时任务，0.2秒的时候获取网页截图，然后等待，1.2秒时再次获取网页截图
#     splash:go("https://www.taobao.com")   # 访问的页面是淘宝
#     splash:wait(3.0)
#     return snapshots      # 最后将截图结果返回
# end
# 第一次截图时网页还没有加载出来，截图为空，第二次网页便加载成功了


# 8)http_get:可以模拟发送HTTP的GET请求
# response = splash:http_get{url, headers=nil, follow_redirects=true}
# 参数说明：
# url：请求URL
# headers： 可选参数，请求头
# follow_redirects： 可选参数，是否启动自动重定向，默认为true
# function main(splash, args)
#     local treat = require("treat")
#     local response = splash:http_get("http://httpbin.org/get")
#         return{
#             html=treat.as_string(response.body),
#             url=response.url,
#             status=response.status
#         }
# end


# 9)http_post:模拟发送POST请求，多了一个参数body：
# response = splash:http_post{url, headers=nil, follow_redirects=true, body=nil}
# 参数说明：
# url:请求URL
# headers：请求头
# follow_redirects:可选参数，是否启动自动重定向，默认true
# body：可选参数，即表单数据，默认为空


# function main(splash, args)
#     local treat = require("treat")
#     local json = require("json")
#     local response = splash:http_post{"http://httpbin.org/post",
#                                       body=json.encode({name="Germey"}),
#     headers={["content-type"]="application/json"}
#     }
#     return {
#         html=treat.as_string(response.bdoy),
#         url = response.url,
#         status=response.status
#     }
# end


# 10)set_content:设置页面的内容
# function main(splash)
#     assert(splash:set_content("<html><body><h1>hello</h1></body></html>"))
#     return splash:png()
# end


# 11)html:获取网页的源代码，是非常简单又常用
# function main(splash, args)
#     splash:go("https://httpbin.org/get")
#     return splash:html())
# end


# 12)png:获取PNG格式的网页截图
# function main(splash, args)
#     splash:go("https://www.taobao.com")
#     return splash:png()
# end


# 13)jpeg:用来获取JPEG格式的网页截图
# function main(splash, args)
#     splash:go("https://www.taobao.com")
#     return splash:jpeg()
# end


# 14)har:用来获取页面加载过程描述
# function main(splash, args)
#     splash:go("https://www.baidu.com")
#     return splash:har()
# end


# 15)url:获取当前正在访问的URL
# function main(splash,args)
#     splash:go("https://www.baidu.com")
#     return splash:url()
# end


# 16)get_cookies:获取当前页面的Cookies
# function main(splash, args)
#     splash:go("https://www.baidu.com")
#     return splash:get_cookies()
# end


# 17)add_cookie:为当前页面添加Cookie
# cookies = splash:add_cookie{name, value, path=nil, domain=nil, expires=nil, httpOnly=nil, secure=nil}
# 各个参数代表Cookie的各个属性
# function main(splash)
#     splash:add_cookie{"sessionid", "237465ghgfsd", "/", domain="http://example.com"}
#     splash:go("http://example/")
#     return splash:html()
# end


# 18)clear_cookies:清除所有的Cookies
# function main(splash)
#     splash:go("https://www.baidu.com/")
#     splash:clear_cookies()                  # 清除所有的Cookies
#     return splash:get_cookies()             # 调用get_cookies将结果返回
# end


# 19）get_viewport_size:获取当前浏览器页面的大小，即宽高
# function main(splash)
#     splash:go("https://www.baidu.com/")\
#     return Splash:get_viewport_size()
# end


# 20)set_viewport_size:设置当前浏览器页面的大小，即宽高
# splash：set_viewport_size(width, height)
# function main(splash)
#     splash:set_viewport_size(400, 700)
#     assert(splash:go("https://cuiqingcai.com"))
#     return splash:png()
# end


# 21)set_viewport_full:设置浏览器全屏显示
# function mian(splash)
#     splash:set_viewport_full()
#     assert(splash:go("https://cuiqingcai.com"))
#     return splash:png()
# end


# 22)set_user_agent:设置浏览器的User-Agent
# function mian(splash)
#     splash:set_user_agent('Splash')     # 将浏览器的User-Agent设置为Splash
#     splash:go("http://httpbin.org/get")
#     return splash:html()
# end


# 23)set_custom_headers():设置请求头
# function main(splash)
#     splash:set_custom_headers({
#         ["User-Agent"] = "Splash",  # 设置了请求头中的User-Agent和Site属性
#         ["Site"] = "Splash",
#     })
#     splash：go("http://httpbin.org/get")
#     return splash:html()
# end


# 24)select:选中符合条件的第一个节点，若有多个节点符合条件，只返回一个，参数是CSS选择器
# function main(splash)
#     splash:go("https://www.baidu.com/")
#     input = splash:select("#kw")
#     input:send_text('Splash')
#     splash:wait(3)
#     return splash:png()
# end


# 25)select_all:选中所有符合条件的节点，参数是CSS选择器
# function main(splash)
#     local treat = require('treat')
#     assert(splash:go("http://quotes.toscrape.com/"))
#     assert(splash:wait(0.5))
#     local texts = splash:select_all('.quote .text') # 通过CSS选择器选中节点正文内容，遍历所有节点，将其中的文本获取下来
#     local results = {}
#     for index, text in ipairs(texts) do
#         results[index] = text.node.innerHTML
#     end
#     return treat.as_array(results)
# end


# 26)mouse_click: 模拟鼠标点击操作，传入的参数为坐标值x和y，也可以直接选中某个节点，然后调用此方法
# function main(splash)
#     splash:go("https://www.baidu.com/")
#     input = splash:select("#kw")    # 选中页面的输入框
#     input:send_text('Splash')       # 输入文本
#     submit = splash:select('#su')   # 选中"提交"按钮
#     submit:mouse_click()            # 调用mouse_click方法提交查询
#     splash:wait(3)                  # 页面等待三秒
#     return splash:png()             # 返回截图
# end


# 7.Splash API调用:利用Splash渲染页面，和Python程序结合使用并抓取JS渲染的页面
# Splash提供了一些HTTP API接口，只需要请求这些接口并传递相应的参数即可
# 7.1)render.html:用于获取JS渲染页面的HTML代码，接口地址是：Splash的运行地址+此接口名称；如http://localhost:8050/render.html
# import requests
# url = 'http://localhost:8050/render.html?url=https://www.baidu.com'
# response = requests.get(url)
# print(response.text)
# 即可输出百度页面渲染后的源代码


# 还可指定其他参数，如通过wait指定等待秒数，要确保页面完全加载出来，可以增加等待时间：
# import requests
# url = 'http://localhost:8050/render.html?url=https://www.taobao.com&wait=5' # 多等待5s才获取淘宝源代码
# response = requests.get(url)
# print(response.text)


# 7.2)render.png：可以获取网页截图，参数比render.html多几个，如width和height控制宽高，返回的是PNG格式的图片二进制数据
# import requests
#
# url = 'http://localhost:8050/render.png?url=https://www.jd.com&wait=5&width=1000&height=700' # 获取京东首页渲染后的截图
# response = requests.get(url)
# with open('taobao.png', 'wb') as f:
#     f.write(response.content)


# 7.3)render.jpeg:返回JPEG格式的图片二进制数


# 7.4)render.har: 获取页面加载的HAR数据，返回结果是一个JSON格式的数据，包含页面加载过程中的HAR数据


# 7.5)render.json:此接口包含前面接口的所有功能，返回结果是JSON
# 可以通过传入不同参数控制返回结果
# 传入html=1，返回结果增加源代码数据；传入png=1，结果增加PNG截图数据；传入har=1，获得页面HAR数据
# curl http://localhost=8050/render.json?url=https://httpbin.org&html=1&har=1


# 7.6)execute:此接口可实现与Lua脚本的对接
# render.html与render.png对于一般的JS渲染页面是足够了，但不能实现交互操作，需要使用execute接口
# 通过最简单的脚本，直接返回数据：
# function main(splash)
#     return 'hello'
# end

# 脚本转化为URL编码后的字符串，拼接到execute接口后
# curl http://localhost:8050/execute?lua_source=function+main%28splash%29%0D80A++return+%27hello%27%0D%0Aend


# import requests
# from urllib.parse import quote
#
# lua = '''               # 三引号将Lua脚本括起来
#
# function main(splash)
#     return 'hello'
# end
# '''
#
# url = 'http://localhost:8050/execute?lua_source=' + quote(lua) # urllib.parse中的quote方法将脚本进行URL转码
# response = requests.get(url)    # 构造Splash请求URL，作为lua_source参数传递
# print(response.text)

# import requests
# from urllib.parse import quote
#
# lua = '''
# function main(splash, args)
#     local treat = require("treat")
#     local response = splash:http_get("http：//httpbin.org/get")
#         return {
#             html=treat.as_string(response.body),
#             url=response.url,
#             status=response.status
#         }
# end
# '''
#
# url = 'http://localhost:8050/execute?lua_source=' + quote(lua)
# response = requests.get(url)
# print(response.text)


# 返回结果是JSOn形式，成功获取了请求URL、状态码和网页源代码
# 之前所说的Lua脚本均可用此种方式与Python对接，所有网页的动态渲染、模拟点击、表单提交、页面滑动、延时等待的结果均可自由控制
# 获取页面源码和截图都不在话下
