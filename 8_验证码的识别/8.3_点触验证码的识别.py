# 点触验证码
# 专门提供点触验证码服务的站点TouClick，https://www.touclick.com/
# 1.目标：用程序识别并通过点触验证码的验证

# 2.Selenium，ChromeDriver

# 3.了解点触验证码
# TouClick与12306站点相似，这次是点击图片中的文字而非图片，交互形式略有不同，基本原理类似

# 4.识别思路：12306识别难点有两点：
# 1)文字识别：“漏斗”二字经过变形、放缩、模糊处理，如果借助OCR技术来识别
# 2)图像的识别：需要将图像重新转化文字，借助各种识图接口，识别的准确率非常低，经常出现匹配不正确或无法匹配的情况。
# 依靠图像识别点触验证码基本不可行
# 推荐网上验证码服务平台：超级鹰，https://www.chaojiying.com，提供的服务种类非常广泛，可识别的验证码类型非常多，包括点触验证码
# 超级鹰平台提供了如下一些服务：
# 英文数字：最多20位英文数字的混合识别
# 中文汉字：最多7个汉字识别
# 纯英文：最多12位的英文识别
# 纯数字：最多11位的数字识别
# 任意特殊字符：不定长汉字英文数字、拼音首字母、计算题、成语混合、集装箱号等
# 坐标选择识别：复杂计算题、选择题四选一、问答题、点击相同的字、物品、动物返回多个坐标的识别

# 5.注册账号：注册超级鹰账号并申请ID，页面链接https://www.chaojiying.com/user/reg/

# 6.获取API，官网下载对应Python API，链接https://www.chaojiying.com/api-14.html
import requests
from hashlib import md5


class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        self.password = md5(password.encode('utf8')).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.longwanli123,  # 超级鹰用户名
            'pass2': self.abc123456, # 密码
            'softid': self.soft_896969, # 软件ID
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def post_pic(self, im, codetype):   # 传入图片对象和验证码的代号，将图片对象和相关信息发给超级鹰的后台进行识别返回JSON
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def report_error(self, im_id):      # 发生错误时回调，如果验证码识别错误，会返回相应的题分
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()

# 以TouClick官网为例，演示点触验证码识别过程，链接http://admin.touclick.com/


# 7.初始化：一些变量，如WebDriver、Chaojiying对象等
EMAIL = 'ra8680592bode@163.com'
PASSWORD = 'abc123456'
# 超级鹰用户名、密码、软件ID、验证码类型
CHAOJIYING_USERNAME = 'longwanli123'
CHAOJIYING_PASSWORD = 'abc123456'
CHAOJIYING_SOFT_ID  = 896969
CHAOJIYING_KIND = 9102

class CrackTouClick():
    def __init__(self):
        self.url = 'http://admin.touclick.com/login.html'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.email = EMAIL
        self.password = PASSWORD
        self.chaojiying = Chaojiying(CHAOJIYING_USERNAME, CHAOJIYING_PASSWORD, CHAOJIYING_SOFT_ID)

# 8.获取验证码：完善相关表单，模拟点击呼出验证码
def open(self):         # open方法填写表单
    """
    打开网页输入用户名密码
    :return:None
    """
    self.browser.get(self.url)
    email = self.wait.until(EC.presence_of_element_located((By.ID, 'email')))
    password = self.wait.until(EC.presence_of_element_located((By.ID, 'password')))
    email.send_keys(self.email)
    password.send_keys(self.password)

def get_touclick_button(self):      # get_touclick_button方法获取验证码按钮
    """
    获取初始验证码按钮
    :param self:
    :return:
    """
    button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'touclick-hod-wrap')))  # 触发点击
    return button

# 类似极验验证码，获取验证码屠天的位置和大小，从网页截图里截取相应验证码图片：
def get_touclick_element(self):     # get_touclick_element从网页截图中截取对应的验证码图片
    """
    获取验证图片对象
    :return: 图片对象
    """
    element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'touclick-pub-content')))
    return element

def get_position(self):     # get_position得到验证码图片的相对位置坐标
    """
    获取验证码位置
    :return: 验证码位置元组
    """
    element = self.get_touclick_element()
    time.sleep(2)
    location = element.location
    size = element.size
    top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x']\
                               + size['width']
    return (top, bottom, left, right)

def get_screenshot(self):
    """
    获取网页截图
    :return: 截图对象
    """
    screenshot = self.browser.get_screenshot_as_png()
    screenshot = Image.open(BytesIO(screenshot))
    return screenshot

def get_touclick_image(self, name='captcha.png'):       # 得到Image对象
    """
    获取验证码图片
    :return: 图片对象
    """
    top, bottom, left, right = self.get_position()
    print('验证码位置', top, bottom, left, right)
    screenshot = self.get_screenshot()
    captcha = screenshot.crop((left, top, right, bottom))
    return captcha

# 9.识别验证码：调用Chaojiying对象的post_pic方法，可把图片发送给超级鹰后台，发送的图像是字节流格式
image = self.get_touclick_element()
bytes_array = BytesIO()
image.save(bytes_array, format='PNG')
result = self.chaojiying.post_pic(bytes_array.getvalue(), CHAOJIYING_KIND)
print(result)       # result变量就是超级鹰后台的识别结果
# 返回的结果是一个JSON，pic_str就是识别的文字坐标，以字符串形式返回，每个坐标都以|分隔，只需将其解析，模拟点击
def get_points(slef, captcha_result):   # get_points方法将识别结果变成列表形式
    """
    解析识别结果
    :param captcha_result:识别结果
    :return: 转化后的结果
    """
    groups = captcha_result.get('pic_str').split('|')
    locations = [[int(number) for number in group.split(',')] for group in groups]
    return locations

def touch_click_words(self, locations):     # touch_click_words方法调用move_to_element_with_offset依次传入解析后的坐标
    """
    点击验证图片
    :param locations:点击位置
    :return: None
    """
    for location in locations:
        print(location)
        ActionChains(self.browser).move_to_element_with_offset(self.get_touclick_element(), location[0],
           location[1]).click().perform()
        time.sleep(1)
# 模拟完成坐标的点选，最后点击提交验证的按钮，等待验证通过，再点击登录安妮即可成功登录
# 借助验证码平台完成了点触验证码识别，通用方法，也可以用此方法来识别12306等验证码
# 代码地址：https://github.com/Python3WebSpider/CrackTouClick
# 如果遇到难题，借助打码平台是一个极佳的选择

