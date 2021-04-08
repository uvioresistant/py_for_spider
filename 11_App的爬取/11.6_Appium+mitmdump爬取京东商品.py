# 用mitmdump监听接口数据，
# 用Appium模拟App炒作，可以绕过复杂的接口参数又可以实现自动化抓取，此方式应是抓取App数据的最佳方式
# 某些特殊情况除外，如微信朋友圈数据又经过一次加密无法解析，只能用Appium提取
# 对大多数App来说，此方法是奏效的

# 1.目标：抓取京东App商品信息和评论，实现Appium和mitmdump二者结合的抓取。
# 抓取数据分为两部分：一部分是商品信息，获取商品的ID、名称和图片，组成一条商品数据
#                    另一部分是商品的评论信息，将评论人的昵称、评论正文、评论日期、发表图片都提取，加入商品ID字段，组成评论数据

# 2. 准备：PC装好Charles、mitmdump、Appium、Android studio、Python版的AppiumAPI。手机装好京东App，安装MongoDB，Pymongo库

# 3. Charles抓包分析：
# 将手机代理设置到Charles上，用Charles抓包分析获取商品详情和商品评论的接口
# 获取商品详情接口，提取到的接口来自cdnware.m.jd.com链接，返回结果是JSON字符串，包含商品ID和商品名称
# 获取商品评论的接口，接口来自api.m.jd.com，返回结果是JSON字符串，包含了商品的数条评论信息

# 4.mitmdump抓取：对接一个Python脚本实现数据的抓取
# 新建脚本文件，实现脚本提取这两个接口的数据。
# 首先提取商品信息：
def response(flow):
    url = 'cdnware.m.jd.com'    # 声明接口的部分链接内容，与请求的URL作比较
    if url in flow.request.url: # 如该链接出现在当前的URL中，证明当前响应就是商品详情的响应，
        text = flow.reponse.text
        data = json.loads(text) # 提取对应的JSON信息
        if data.get('wareInfo') and data.get('wareInfo').get('basicInfo'):
            id = info.get('wareId')
            name = info.get('wareId')
            name = info.get('name')         # 提取商品ID名称
            image = info.get('wareImage')   # 提取图片
            print(id, name, images)         # 提取出一条商品数据
# 再提取评论数据
url = 'api.m.jd.com/client.action'  # 指定接口的部分链接内容，
if url in flow.request.url: # 判断当前请求的URL是不是获取评论的URL
    pattern = re.compile('sku\".*?\"(\d+)\"')   # 商品ID隐藏在请求中，需要提取请求表单内容来提取，直接用正则表达式
    # Request请求参数中包含商品ID
    body = unquote(flow.request.text)
    # 提取商品ID
    id = re.search(pattern, body).group(1) if re.search(pattern, body) else None    # 满足条件，提取商品的ID
    # 提取Response Body
    text = flow.response.text   # 评论信息在响应中
    data = json.loads(text)     # 对JSON进行解析
    comments = data.get('commentInfoList') or []
    # 提取评论数据
    for comment in comments:    # 满足条件，提取评论信息
        if comment.get('commentInfo') and comment.get('commentInfo').get('commentData'):
            info = comment.get('commentInfo')
            text = info.text('commentData')         # 提取出商品评论正文
            date = info.get('commentDate')          # 提取出商品评论日期
            nickname = info.get('userNickName')     # 提取出商品评论人的昵称
            pictures = info.get('pictureInfoList')  # 提取出图片
            print(id, nickname, text, date, pictures)   # 和商品的ID组合起来，形成一条评论数据

# 最后用MongoDB将两部分数据分开保存到两个Collection
# 略

# 运行脚本：
# mitmdump -s script.py
# 手机代理设置到mitmdump上。
# 在京东App中打开摸个商品，下拉商品评论，即可看到控制台输出两部分的抓取结果，成功保存到MongoDB数据库，手动操作可做到抓取

# 5.Appium自动化：
# Appium驱动App完成一系列动作，进入App后，
# 需要做的操作：点击搜索框、输入搜索的商品名称、点击进入商品详情、进入评论页面、自动滚动刷新，操作逻辑和爬取朋友圈相同

# 京东App的Desired Capabilities配置：
{
    'platformName': 'Android',
    'deviceName': 'MI 5',
    'appPackage': 'com.jingdong.App.mall',
    'appActivity': 'main.ManActivity'
}

# 首先用Appium打开京东App
# 录制一系列动作，遭到各个页面的组件ID并做好记录，再改写成完整代码
form appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import  WebDriverWait
from selenium.webdriver.support import  expected_conditions as EC
form time import sleep

class Action():
    def __init__(self):
        # 驱动配置
        self.desired_caps = {
            'platformName': PLATFORM,
            'deviceName': DEVICE_NAME,
            'appPackage': 'com.jingdong.app.mall',
            'appActivity': 'main.MainActivity'
        }
        self.driver = webdriver.Remote(DRIVER_SERVER, self.desired_caps)
        self.wait = WebDriverWait(self.driver, TIMEOUT)

    def comments(self):
        # 点击进入搜索页面
        search = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jingdong.app.mall:id/mp')))
        search.click()
        # 输入搜索文本
        box = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jd.lib.search:id/search_box_layout')))
        box.set_text(KEYWORD)
        # 点击搜索按钮
        button = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jd.lib.search:id/product_list_item')))
        button.click()
        # 点击进入商品详情
        view = self.wait.until(EC.text_to_be_present_in_element((By.ID, 'com.jd.lib.search:id/product_list_item')))
        view.click()
        # 进入评论详情
        tab = self.wait.until(EC.presence_of_element_located((By.ID, 'com.jd.lib.productdetail:id/pd_tab3')))
        tab.click()

    def scroll(self):
        while True:
            # 模拟拖动
            self.driver.swipe(FLICK_START_X, FLICK_START_Y + FLICK_DISTANCE, FLICK_START_X ,FLICK_START_Y)
            sleep(SCROLL_SLEEP_TIME)

    def main(self):
        self.comments()
        self.scroll()

if __name__ == '__main__':
    action = Action()
    action.main()
# 由于App版本更新，交互流程和元素ID可能有更改
# 下拉过程已经省去了用Appium提取数据的过程，此过程用mitmdump帮助实现
# 代码运行后会启动京东App，进入商品详情页，然后进入评论页无限滚动，代替了人工操作。
# Appium实现模拟滚动，mitmdump进行抓取，App的数据就会保存到数据库中

# 代码地址：https://github.com/Python3WebSpider/MitmAppiumJD



