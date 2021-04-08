# 直接用Charles或mitmproxy来监听微信朋友圈的接口数据，无法实现爬取。因为数据都是加密的。
# Appium不同， Appium是自动化测试工具，可以直接模拟App的操作并获取当前所见的内容。即只要App显示了内容，就可以用Appium抓取

# 1.目标：Android平台，抓取朋友圈动态信息。包括好友昵称、正文、发布日期。
# 发布日期还需进行转换，日期显示1小时前，转换为今天，动态信息保存到MongoDB

# 2.准备：PC安装好Appium、Android studio、Python版本的Appium API，安卓手机装好微信App、PyMongo库；MongoDB并运行服务

# 3. 初始化：
# 新建Moments类：进行初始化配置
PLATFORM = 'Android'
DEVICE_NAME = 'MI 5'
APP_PACKAGE = 'com.tencent.mm'
APP_ACTIVITY = '.ui.LauncherUI'
DRIVER_SERVER = 'HTTP://LOCALHOST:4723/wd/hub'
TIMEOUT = 300
MONGO_URL = 'localhost'
MONGO_DB = 'moments'
MONGO_COLLECTION = 'moments'

class Moments():
    def __init__(self):
        """
        初始化
        """
        # 驱动配置
        self.desired_caps = {
            'platformName': PLATFORM,
            'deviceName': DEVICE_NAME,
            'appPackage': APP_PACKAGE,
            'appActivity': APP_ACTIVITY
        }
        self.driver = webdriver.Remote(DRIVER_SERVER, self.desired_caps)    # 驱动的配置
        self.wait = WebDriverWait(self.driver, TIMEOUT) # 延时等待配置
        self.client = MongoClient(MONGO_URL)    # MongoDB连接配置
        self.db = self.client[MONGO_DB]
        self.collection = self.db[MONGO_COLLECTION]

# 4.模拟登录：点击登录按钮、输入用户名、密码、提交登录
def login(self):
    # 登录按钮
    login = self.wait.until(EC.presence_of_elemetn_located((By.ID, 'com.tencent.mm:id/cjk')))
    login.click()
    # 手机输入
    phone = self.wait.until(EC.presence_of_elemetn_located((By.ID, 'com.tencent.mm:id/h2')))
    phone.set_text(USERNAME)
    # 下一步
    next self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/adj')))
    next.click()
    # 密码
    password = self.wait.until(
        EC.presence_of_elemetn_located((By.XPATH, '//*[@resource-id="com.tencent.mm:id/h2"][1]')))
            password.set_text(PASSWORD)
    # 提交
    submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/adj')))
    submit.click()

# 登录完成后，进入朋友圈页面。选中朋友圈所在选项卡，点击朋友圈按钮：
def enter(self):
    # 选项卡
tab = self.wait.until(
    EC.presence_of_elemetn_located((By.XPATH, '//*[@resource-id="com.tencent.mm:id/bw3"][3]')))
tab.click()
# 朋友圈
moments = self.wait.until(EC.presence_of_elemetn_located((By.ID, 'com.tencent.mm:id/atz')))
moments.click()

# 抓取动态：模拟无限拖动操作
# 滑动点
FLICK_START_X = 300
FLICK_START_Y = 300
FLICK_DISTANCE = 700

def crawl(self):
    while True:
        # 上滑
self.driver.swipe(FLICK_START_X, FLICK_START_Y + FLICK_DISTANCE, FLICK_START_X , FLICK_START_Y) # swipe方法，
# 传入起始和终止点实现拖动， 加入无限循环实现无限拖动

# 获取当前显示的朋友圈每条状态对应的区块元素，遍历每个区块元素，获取内部显示的用户名、正本和发布时间：
# 当前页面显示的所有状态：
items = self.wait.until(
    EC.presence__of_all_elements_located(
        (By.XPATH, '//*[@resource-id="com.tencent.mm:id/cve"]//android.widget.FrameLayout')))
# 遍历每条状态
for item in items:
    try:
    # 昵称
    nickname= item.find_element_by_id('com.tencent.mm:id/aig').get_attribute('text')    # 调用find_element_by_id获取昵称
    # 正文
    content = item.find_element_by_id('com.tencent.mm:id/cwm').get_attribute('text')
    # 日期
    date = item.find_element_by_id('com.tencent.mm:id/crh').get_attribute('text')
    # 处理日期
    date = self.processor.date(date)
    print(nickname, content, date)
    data = {
        'nickname': nickname,
        'content': content,
        'date': date,
    }
    except NoSuchElementException:
        pass

# 对日期的处理，调用一个processor类的date处理方法:
def date(self, datetime):
    """
    处理时间
    :param self: 原始时间
    :return: 处理后时间
    """
    if re.match('\d+分钟前', datetime):    # 使用正则匹配方法提取时间中的具体数字，利用时间转换函数实现时间转换
        minute = re.match('(\d+)', datetime).group(1)
        datetime = time.strftime('%Y-%m-%d', time.localtime(time.time() - float(minute) * 60))  # 5分钟前，提取5，减300
    if re.match('\d+小时前', datetime):
        hour =re.match('(\d+)', datetime).group(1)
        datetime = time.strftime('%Y-%m-%d', time.localtime(time.time() - float(hour) * 60 * 60))
    if re.match('昨天', datetime):
        datetime = time.strftime('%Y-%m-%d', time.localtime(time.time() - 24 * 60 * 60))
    if re.match('\d+天前', datetime):
        day = re.match('(\d+)', datetime).group(1)
        datetime = time.strftime('%Y-%m-%d', time.localtime(time.time()) - float(day) * 24 * 60 * 60)
    return datetime

# 调用MongoDB的API实现爬取结果的存储。
# 为了去除重复，调用update方法：
self.collection.update({'nickname': nickname, 'content': content}, {'$set': data}, True)
# 根据昵称和正文查询信息，如信息不存在，插入数据，否则更新数据。第三个参数True，设置为True，可以是实现存在即更新、不存在即插入
# 最后实现入口方法调用以上方法。调用即可开始爬取
def main(self):
    # 登录
    self.login()
    # 进入朋友圈
    self.enter()
    # 爬取
    self.crawl()

# 6.源代码地址：https://github.com/Python3WebSpider/Moments
# 利用Appium，做到可见即可爬，但实际运行后，Appium的解析比较繁琐，容易发生重复和中断。
# 可以用mitmdump监听App数据实时处理，Appium只负责自动化驱动，各负其责，整个爬取效率和解析效率会高很多
