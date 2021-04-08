# 1.查看请求：Chrome浏览器打开微博链接http://m.weibo.cn/u/2830678474
# 浏览器的Elements选项卡中观察源代码 ，右侧是节点样式
# 切换到Network，刷新,出现的条目就是在页面加载过程中浏览器与服务器之间发送请求和接受响应的所有记录
# Ajax特殊的请求类型：xhr，名称以getIndex开头的请求，Type为xhr，就是一个Ajax请求，
# 右侧观察Request Headers、URL、Response Headers。其中Request Headers中有一个信息为X-Reuested-With：XMLHTTPRequest标记Ajax
# 点击Preview，可看到响应内容，是JSON格式的，可展开和收起相应内容
# 返回的是个人信息：昵称、简介、头像，用来渲染个人主页所使用的数据，JS接收数据后，再执行相应的渲染方法，页面就渲染出来了
# 切换到Response选项卡，观察到真实返回数据
# 且回到第一个请求，观察Response是什么，最原始的链接https返回的结果，代码只有不到50行，结构也非常简单，只执行一些JS
# 看到的微博页面的真实数据并不是最原始的页面返回的，而是后来执行JS后再次向后台发送了Ajax请求，浏览器再进一步渲染出来

# 2.过滤请求
# 利用Chrome筛选功能筛选出所有的Ajax请求,XHR下方的所有请求便都是Ajax请求。
# 不断滑动页面，看到页面底部有一条条新的微博被刷出，开发者工具下一个个地出现Ajax请求，就可以获取到所有的Ajax请求了
# 随意点开一个条目，都可以清楚地看到Request URL、Request Headers、Response Headers、Response Body，想要模拟请求和提取就简单了
# 已经分析出Ajax请求的一些详细信息了，接下来只需用程序模拟这些Ajax请求，就可以轻松提取所需要的信息了。