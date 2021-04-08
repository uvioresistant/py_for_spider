# 微博宫格验证码识别：新型交互式验证码，每个宫格间会有一条指示连线，指示了应该的滑动轨迹，要按照华东光轨迹依次从起始宫格滑动到
# 终止宫格，才可以完成验证
# 访问新浪微博移动版登录页面，看到如上验证码，链接https://passport.weibo.cn/signin/login频繁登录或者账号存在安全风险，出现
# 1.用程序来识别并通过微博宫格验证码的验证

# 2.Selenium库、ChromeDriver

# 3.识别思路：
# 规律：验证码的四个宫格一定是有连线经过的，每一条连线都会相应的指示箭头，形状多样，包括C、Z、X型
# 同一类型的连线轨迹相同，唯一不同的是连线的方向
# 反向连线和正向连线的连线轨迹是相同的，但指示箭头不同，导致滑动宫格顺序有所不同
# 要完全识别滑动宫格顺序，就需要具体识别出箭头的朝向。整个验证码箭头朝向一共有8种，会出现在不同的位置
# 箭头方向识别算法，需要考虑不同箭头所在位置，找出各个位置箭头的像素点坐标，计算像素点变化规律，工作量会变得比较大
# 可以考虑用模板匹配方法：将一些识别目标提前保存并做好标记，称作模板：将验证码图片做好拖动顺序的标记当做模板
# 对比要识别的目标和每一个模板，如果找到匹配的模板，就成功识别出要新识别的目标。
# 图像识别中，模板匹配也是常用的方法，实现简单且易用性好
# 收集到足够多的模板，模板匹配方法才会好，对于微博宫格验证码来说，宫格只有4个，样式最多4*3*2*1=24种，可以将所有模板都收集下来
# 何种模板匹配，只匹配箭头还是验证码全图？--全图匹配的方式
# a.精度：匹配箭头，对比目标只有几个像素点范围的箭头，一旦像素点有偏差，会直接错位。全图匹配，无需关心箭头所在位置，还有连线辅助
# b.工作量：匹配箭头，需要保存所有不同朝向的箭头模板，需要算出每个箭头位置并将其逐个截出保存成模板。全图匹配，不需计算箭头位置

# 4.获取模板：验证码是随机的，一共有24种，可以写一段程序来批量保存验证码图片，从中筛选出需要的图片
import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


USERNAME = ''
PASSWORD = ""

class CrackWeiboSlide():
    def __init__(self):
        self.url = 'https://passport.weibo.cn/signin/login'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.username = USERNAME
        self.password = PASSWORD

    def __del__(self):
        self.browser.close()

    def open(self):
        """
        打开网页输入用户名密码并点击
        :return: None
        """
        self.browser.get(self.url)
        username = self.wait.until(EC.presence_of_element_located((By.ID, 'loginName')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'loginPassword')))
        submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'loginAction')))
        username.send_keys(self.username)
        password.send_keys(self.password)
        submit.click()

def get_position(self):
    """
    获取验证码位置
    :return: 验证码位置元组
    """
    try:
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'patt-shadow')))
    except TimeoutException:
        print('未出现验证码')
        self.open()
    time.sleep(2)
    location = img.location
    size = img.size
    top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'],location['x'] + size['width']
    return (top, bottom, left, right)

def get_screenshot(self):
    """
    获取网页截图
    :return: 截图对象
    """
    screenshot = self.browser.get_screenshot_as_png()
    screenshot = Image.open(BytesIO(screenshot))
    return screenshot

def get_image(self, name='captcha.png'):
    """
    获取验证码图片
    :return: 图片对象
    """
    top, bottom, left, right = self.get_position()
    print('验证码位置', top, bottom, left, right, bottom)
    captcha.save(name)
    return captcha

def main(self):
    """
    批量获取验证码
    :return: 图片对象
    """
    count = 0
    while True:
        self.open()
        self.get_image(str(count) + '.png')
        count += 1
if __name__ == '__main__':
    crack = CrackWeiboSlide()
    crack.main()
# 需要将USERNAME和PASSWORD修改为自己微博的用户名和密码。运行一段时间后，本地多了很多以数字命名的验证码
# 挑选出不同的24张验证码图片并命名保存。名称取作宫格的滑动顺序：如4132，代表滑动顺序4-1-3-2
# 只需遍历模板进行匹配即可

# 5.模板匹配
# 调用get_image方法，得到验证码图片对象。然后，对验证码图片对象进行模板匹配
from os import listdir      # listdir获取所有模板的文件名称

def detect_image(self, image):
    """
    匹配图片
    :param image: 图片
    :return: 拖动顺序
    """
    for template_name in listdir(TEMPLATES_FOLDER):     # TEMPLATE_FOLDER为模板所在文件夹
        print('正在匹配', template_name)
        template = Image.open(TEMPLATES_FOLDER + template_name)
        if self.same_image(image, template):    # same_image方法对验证码和模板进行对比
            # 返回顺序
            numbers = [int(number) for number in list(template_name.split('.')[0])]     # 匹配成功，将模板文件名转换为列表
            print('拖动顺序', numbers)
            return numbers

# 对比方法实现如下：
def is_pixel_equal(self, image1, image2, x, y):
    """
    判断两个像素是否相同
    :param image1: 图片1
    :param image2: 图片2
    :param x: 位置x
    :param y: 位置y
    :return: 像素是否相同
    """
    # 取两个图片的像素点
    pixel1 = image1.load()[x, y]
    pixel2 = image2.load()[x, y]
    threshold = 20
    if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
            pixel1[2] - pixel2[2]) < threshold:
        return True
    else:
        return  False
def same_image(self, image, template):  # same_image方法接受两个参数，image为待检测验证码图片对象，template是模板对象
    """
    识别相似验证码
    :param image: 待识别验证码
    :param template: 模板
    :return:
    """
    # 相似度阈值
    threshold = 0.99        # 阈值设定为0.99
    count = 0
    for x in range(image.width):    # 遍历图片所有像素点
        for y in range(image.height):
            # 判断像素是否相同
            if self.is_pixel_equal(image, template, x, y):
                count += 1              # 对比二者同一位置的像素点，如果像素点相同，计数加1
    result = float(count) / (image.template, x, y):     # 计算相同像素点占中像素的比例
    if result > threshold:      # 该比例超过一定阈值，判定图片完全相同，匹配成功
        print('成功匹配')
        return True
    return False

# 6.模拟拖动
# 根据滑动顺序拖动鼠标，连接各个宫格
def move(self, numbers):    # 接收参数就是宫格的点按顺序
    """
    根据顺序拖动
    :param numbers:
    :return:
    """
    # 获得四个按点
    circles = self.browser.find_elements_by_css_selector('.patt-wrap .patt-circ')   # 获取4个宫格元素
    dx = dy = 0
    for index in range(4):      # 遍历宫格的点按顺序，做一系列对应操作
        circle = circles[numbers[index] - 1]    # 列表形式，每个元素代表一个宫格
        # 如果第一次循环
        if index == 0:      # 当前遍历的是第一个宫格
            # 点击第一个按点
            ActionChains(self.browser) \
                .move_to_element_with_offset(circle, circle.size['width'] / 2, circle.size['height'] /2) \
                .click_and_hold().perform()     # 直接鼠标点击并保持动作
        else:                               # 否则移动到下一个宫格
            # 小幅移动次数
            time = 30
            # 拖动
            for i in range(times):
                ActionChains(self.browser).move_by_offset(dx / times, dy /times).perform()
                time.sleep(1 / times)
            # 如果是最后一次循环
            if index == 3:      # 最后一个宫格，松开鼠标
                # 松开鼠标
                ActionChains(self.browser).release().perform()
            else:
                # 计算下一次偏移   # 不是最后一个宫格，计算移动到下一个宫格的偏移量
                dx = circles[numbers[index + 1] - 1].location['y'] - circle.location['x']
                dy = circles[numbers[index + 1] - 1].location['y'] - circle.location['y']
# 通过4次循环，便可以成功操作浏览器完成宫格验证码的拖拽填充，松开鼠标后，识别成功
# 鼠标会慢慢从起始位置移动到终止位置，识别完成，验证码窗口会自动关闭，直接点击登录按钮即可登录微博
# 代码地址：https://github.com/Python3WebSpider/CrackWeiboSlide