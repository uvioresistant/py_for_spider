# 很多情况下，页面信息需要登录才可查看，故需要模拟登录，实际上是在客户端生成Cookies，保存了SessionID信息，后续请求会携带Cookies
# 发送给服务器，服务器根据Cookies判断出对应的SessionID，找到会话。当前会话有效，服务器判断用户已经登录，返回请求的页面信息。
# 核心是获取登录后的Cookies，可手动输入用户密码，再把Cookies复制下俩，明显增加人工工作量，爬虫目的是自动化，即用程序模拟登录
# 模拟登陆后页面的抓取过程，原理在于模拟登录后Cookies的维护
# 1.目标：爬取GitHub登陆后才可以访问的页面信息，如好友动态、个人信息等

# 2.环境准备：安装requests和lxml库

# 3.分析登录过程：探究后台的登录请求是怎样发送的，登录后又有怎样的处理过程；
# 退出GitHub登录，清除Cookies，登录页面https://github.com/login，输入密码，F12，勾选Preserve Log，显示持续日志
# 登录，开发者工具中点击第一个请求，URL为https://github.com/session，请求方式POST，观察Form Data和Headers中内容
# Headers包含Cookies、Host、Origin、Referer、User-Agent
# Form Data包含5个字段：commit：固定的字符串Sign in、utf8：勾选字符、authenticity_token：Base64加密的字符串、login：用户名
# password：密码
# 无法直接构造内容：Cookies和authenticity_token，获取方式：
# 在访问登录页的时候设置，退出登录，回到登录页，清空Cookies，重新访问登录页，截获发生的请求，访问登录页面的请求。
# Response Headers有Set-Cookie字段，就是设置Cookies的过程
# 网页源代码中隐藏式表单元素有authenticity_token信息

# 4.代码：
#       定义Login类，初始化变量：
class Login(object):
    def __init__(self):
        self.headers = {
            'Referer': 'https://github.com/',
            'User-Agent': 'Mozilla/5.0 (windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  'Chrome/57.0.2987.133 Safari/537.36',
            'Host': 'github.com'
        }
        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/session'
        self.logined_url = 'https://github.com/settings/profile'
        self.session = requests.Session()   # 最重要的变量requests库的Session，维持会话，可以自动处理Cookies

# 登录页面完成两件事：a通过此页面获取初始Cookies，b提取出authenticity_token
# 实现token方法：
from lxml import etree

def token(self):
    response = self.session.get(self.login_url, headers=self.headers)   # 用Session对象的get方法访问GitHub登录页面
    selector = etree.HTML(response.text)
    token = selector.xpath('//div/input[2]/@value')[0]  # XPath解析登录所需authenticity_token信息
    return token    # 返回authenticity_token

# 已经获取初始的Cookies和authenticity_token，模拟登录，实现login方法
def login(self, email, password):
    post_data = {           # 构造表单
        'commit': 'Sign in',
        'utf-8': 'y',
        'authenticity_token': self.token(),
        'login': email,     # email以变量形式传递
        'password': password    # password以变量形式传递
    }

    response = self.session.post(self.post_url, data=post_data, headers=self.headers)  # 用Session对象的post方法模拟登陆
        # requests自动处理重定向信息，登录成功后直接跳转到首页，显示所关注人的动态信息，
    if response.status_code == 200:
        self.dynamics(response.text)    # 响应后,dynamics方法处理

    response = self.session.get(self.logined_url, headers=self.headers) # Session对象请求个人详情页
    if response.status_code == 200:
        self.profile(response.text) # 用profile方法处理个人详情页信息

# dynamics方法和profile方法实现：
def dynamics(self, html):
    selector = etree.HTML(html)
    dynamics = selector.xpath('//div[contains(@class, "news")]//div[contains(@class, "alert")]') # 使用XPath提取信息
    for item in dynamics:   # 提取所有动态信息，遍历输出
        dynamic = ' '.join(item.xpath('.//div[@@class="title"]//text()')).strip()
        print(dynamic)

def profile(self, html):
    selector = etree.HTML(html)
    name = selector.xpath('//input[@id="user_profile_name"]/@value')[0] # 提取个人昵称
    email = selector.xpath('//select[@id="user_profile_email"]/option[@value!=""]/text()')  # 提取绑定的邮箱
    print(name, email)

# 5.运行：新建Login对象，运行程序
if __name__ == "__mian__":
    login = Login()
    login.login(email='2099131945@qq.com', password='abc123456')

# 代码地址：https://github.com/Python3WebSpider/GithubLogin