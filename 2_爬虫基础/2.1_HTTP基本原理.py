# 写爬虫前，还需要了解一些基础知识，如HTTP原理、网页的基础知识、爬虫的基本原理、Cookies的基本原理
# HTTP基本原理：在浏览器敲入URL到获取网页内容之间发生了什么
# 1.URI和URL：URI(Uniform Resource Identifier)统一资源标识符；URL(Universal Resource Locator）统一资源定位符；
# https://github.com/favicon.ico是GitHub的网站图标链接，是一个URL，也是一个URI。即有一个图标资源，用URL/URI来唯一指定访问方式
# 其中包括访问协议https、访问路径(/即根目录)和资源名称favicon.ico。通过这个链接，可以从互联网上找到这个资源
# URL是URI的子集，URI还包括一个子类URN(Universal Resource Name)统一资源名称。URN只命名资源而不指定如何定位资源
# urn:isbn:0451450523指定了一本书的ISBN，可以唯一标识这本书，但是没有指定到哪里定位这本书。
# 目前的互联网中，URN用得非常少，几乎所有的URI都是URL，一般的网页链接既可以称为URL，也可称为URI

# 2.超文本(hypertext):在浏览器里看到的网页超文本解析，其网页源代码是一系列HTML代码，里面包含了一系列标签，HTML就是超文本
# F12中Elements即可看到当前网页的源代码，这些源代码都是超文本

# 3.HTTP和HTTPS：就是访问资源需要的协议类型
# HTTP(Hyper Text Transfer Protocol):超文本传输协议，用于从网络传输超文本数据到本地浏览器的传送协议，能保证高效而准确地传送
# 超文本文档。
# HTTP由万维网协会(World wide Web Consortium)和Internet工作小组IETF(Internet Engineering Task Force)共同合作指定的规范

# HTTPS(Hyper Text Transfer Protocol over Secure Socket Layer)是以安全为目标的HTTP通道，简单讲是HTTP的安全版，即HTTP下加入
# SSL层，简称为HTTPS
# HTTPS的安全基础是SSL，因此通过它传输的内容都是经过SSL加密的，主要作用可以分为两种：
# a.建立一个信息安全通道来保证数据传输的安全
# b.确认网站的真实性，凡是使用了HTTPS的网站，都可以通过点击浏览器地址栏的锁头标志来查看网站认证后的真实信息，也可以通过CA
# 机构颁发的安全签章来查询
# 越来越多的网站和App都已经向HTTPS方向发展：
# 苹果强制所有iOS App在2017年1月1日全部改为使用HTTPS加密，否则App无法再应用商店上架
# 谷歌从2017年1月推出的Chrome56开始，对未进行HTTPS加密的网址链接亮出风险提示，
# 微信小程序的官方需求文档要求后台使用HTTPS请求精心网络通信，不满足条件的域名和协议无法请求
# 12306的CA证书是中国铁道部执行签发的，此证书是不被CA机构信任的，但它的数据传输依然是经过SSL加密的。如果要爬取这样的站点，就
# 需要设置忽略证书的选项，否则会提示SSL链接错误

# 4.HTTP请求过程：浏览器中输入一个URL，回车后会在浏览器中观察到页面内容。此过程是浏览器向网站所在的服务器发送了一个请求，网站
# 服务器接受到此请求后进行处理和解析，然后返回对应的响应，接着传回浏览器。响应里包含了页面的源代码等内容，浏览器再对其进行解析，
# 便将网页呈现了出来。
# Chrome的开发者模式下的Network监听演示，显示访问当前请求网页时发生的所有网络请求和响应。
# Chrome在Network页面下出现了一个个的条目，其中一个条目就代表一次发送请求和接收响应的过程。
# 先观察第一个网络请求，即www.baidu.com
# 第一列Name：请求的名称，一般会将URL的最后一部分内容当做名称
# 第二列Status：响应的状态码，显示为200，代表响应是正常的。通过转态码，可以判断发送了请求以后是否得到正常的响应
# 第三列Type：请求的文档类型。这里为document, 代表我们这次请求的是一个HTML文档，内容就是一些HTML代码
# 第四列 Initiator: 请求元。用于标记请求是由哪个对象或进程发起的
# 第五列 Size：从服务器下载的文件和请求的资源大小。如果是从缓存中取得的资源，则该列会显示from cache
# 第六列 Time：发起请求到获取响应所用的总时间
# 第七列 Waterfall：网络请求的可视化瀑布流

# 点击这个条目，即可看到更详细的信息：
# 首先是General部分，
# Request URL为请求的URL，
# Request Method为请求的方法，
# Status Code为响应状态码
# Remote Address为远程服务器的地址和端口
# Referrer Policy为Referer判别策略
# Response Headers：响应头
# Request Headers：请求头，带有许多请求信息，浏览器标识、Cookies、Host等信息，是请求的一部分，服务器会根据请求头内的信息，
# 判断请求是否合法，进而作出对应的响应。

# 5.请求：由客户端向服务端发出，分为4部分内容：
# 请求方法(Request Method):1.常见请求方法两种：
#                               GET：浏览器中直接输入URL并回传，便发起了一个GET请求，请求的参数会直接包含到URL中，
# 百度中搜索Python，就是一个GET请求，链接为https://www.baidu.com/s?wd=Python,URL中包含请求的参数信息，参数wd即要搜寻的关键字
#                               POST：在表单提交时发起
# 一个登陆表单，输入用户名和密码后，点击“登陆”按钮，会发起一个POST请求，数据以表单形式传输，不体现在URL中。
# 区别：
# GET请求中的参数包含在URL里，数据可以在URL中看到，POST请求的URL不会包含这些数据，都通果表单传输，包含在请求体中
# GET请求提交的数据最多只有1024字节，而POST方式没有限制
# 登录时，需提交用户名和密码，包含敏感信息，使用GET方式请求，密码会暴露在URL里，造成密码泄露，最好以POST方式传送。
# 上传文件，内容比较大，也选用POST方式。
# 请求的网址(Request URL)：即统一资源定位符URL，可以唯一确定想请求的资源
# 请求头(Request Headers): 说明服务器要使用的附加信息,比较重要信息有Cookie、Referer、User-Agent,是请求的重要组成部分，需设定
# Accept：请求报头域：指定客户端可接受哪些类型的信息
# Accept-Language：指定客户端可接受的语言类型
# Accept-Encoding：指定客户端可接受的内容编码
# Host：指定请求资源的主机IP和端口号，内容为请求URL的原始服务器或网关的位置。请求必须包含此内容
# Cookie(Cookies):网站为了辨别用户进行会话跟踪而存储在用户本地的数据，主要功能是维持当前访问会话。
#       如，输用户名和密码成功登录某个网站后，服务器用会话保存登录状态，每次刷新或请求该站点的其他页面时，会发现都是登录状态
# Cookies里有信息标识了所对应的服务器的会话，每次浏览器在请求该站点的页面时，都会在请求头中加上Cookies并将其发送给服务器，
# 服务器通过Cookies识别出是自己，并且查出当前状态是登录状态，所以返回结果就是登录后才能看到的网页内容
# Referer：标识这个请求是从哪个页面发过来的，服务器可以拿到这一信息并做响应的处理，如做来源统计、防盗链处理。
# User-Agent：UA，特殊的字符串头，可使服务器识别客户使用的操作系统及版本、浏览器及版本等信息，在做爬虫时加上此信息，可以伪装
# 为浏览器；如果不加，很可能会被识别出为爬虫。
# Content-Type：互联网媒体类型(Internet Media Type)或MIME类型，在HTTP协议消息头中，用来表示具体请求中的媒体类型信息。
#       对应关系可查看对照表：http://tool.oschina.net/ccommons
# 请求体(Request Body)：POST请求中的表单数据，对于GET请求，请求体为空
#   登录GitHub是捕获到的请求和响应：登录前，填写了用户名和密码信息，提交时这些内容就会以表单数据的形式提交给服务器，
#   此时需要注意Request Headers中指定Content-Type为application/x-www-form-urlencoded，只有设置Content-Type为application/
#   x-www-form-urlencoded，才会以表单数据的形式提交。也可将Content-Type设置为application/json来提交JSON数据，或者设置为
#   multipart/form-data来上传文件。
# Content-Type和POST提交数据方式的关系：
# application/x-www-form-urlencoded       表单数据
# multiipart/form-data                    表单文件上传
# application/json                        序列化JSON数据
# text/xml                                XML数据
# 爬虫中，如果要构造POST请求，需要使用正确的Content-Type，并了解各种请求库的各个参数设置时使用的是哪种Content-Type，不然可能
# 导致POST提交后无法正常响应

# 6.响应：服务器返回给客户端，可分为三部分：
#       A.响应状态码(Response Status Code):表示服务器的响应状态，200正常，404页面未找到，500服务器内部错误

#       B.响应头:包含服务器对请求的应答信息：
#               Data：标识响应产生的时间
#               Last-Modified：指定资源的最后修改时间
#               Content-Encoding: 指定响应内容的编码
#               Server： 包含服务器的信息，如名称、版本号等
#               Content-Type： 文档类型，指定返回的数据类型是什么，如text/html代表返回HTML文档
#               Set-Cookie：设置Cookies。告诉浏览器需要将此内容放在Cookies中，下次请求携带Cookies请求
#               Expires：指定响应的过期时间，可以使代理服务器将加载的内容更新到缓存中。再次访问时，就可从缓存中加载，降低服务器
#                             负载，缩短加载时间

#       C.响应体：响应体的正文数据都在响应体中，如请求网页时，响应体就是网页的HTML代码，请求一张图片时，响应体就是图片的二进制
# 数据。做爬虫请求网页后，要解析的内容就是响应体。F12中点击Preview，看到网页的源代码，就是响应体的内容，是解析的目标。
# 做爬虫时，主要通过响应体得到网页的源代码、JSON数据等，然后从中做相应内容的提取。

