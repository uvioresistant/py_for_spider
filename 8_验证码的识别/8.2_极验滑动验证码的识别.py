# 1.目标：用程序来识别并通过极验验证码的验证：包括分析识别思路、识别缺口位置、生成滑块拖动路径、模拟实现滑块拼合、通过验证

# 2.Selenium库、ChromeDriver

# 3.了解极验验证码：
# 极验验证码官网：http://www.geetest.com/：专注于提供验证安全的系统，主要验证方式是拖动滑块拼合图像。若图像完全拼合，验证成功
# 斗鱼、魅族采用

# 4.极验验证码特点:
# 极验验证码增加了机器学习方法识别拖动轨迹，官网安全防护说明：
# 三角防护之防模拟：拥有超过4000万人机行为样本数据，机器学习和神经网络，构建多重静态、动态防御模型。识别模拟轨迹,界定人机边界
# 三角防护之防伪造：深度分析浏览器实际性能来辨识伪造信息，根据伪造时间不断更新黑名单，提高防伪造能力
# 三角防护之防暴力：拥有多种验证形态，每种形态有利于神经网络生成的海量图库储备，图库不断更新，极大提高暴力识别成本

# 5.识别思路：直接模拟表单提交、加密参数的构造是问题；直接模拟浏览器动作的方式完成验证
# 用Selenium完全模拟人的行为方式完成验证
# 带有极验验证的网站：如极验官方后台，https://account.geetest.com/login
# 同一会话，一段时间内二次点击会直接通过验证；不通过，弹出滑动验证窗口，拖动滑块拼合图像完成二步验证
# 识别验证需完成三步：
# 1)模拟点击验证按钮: 直接用Selenium模拟点击按钮
# 2)识别滑动缺口的位置: 识别缺口位置比较关键，需要用到图像相关处理方法;观察缺口，实现边缘检测算法找出缺口位置
# 利用和原图对比检测方式来识别缺口位置，在没有滑动滑块前，缺口并没有呈现
# 同时获取两张图片，设定对比阈值，遍历两张图片，找出相同位置像素RGB差距超过此阈值的像素点，此像素点位置就是缺口位置
# 3)模拟拖动滑块:匀速移动、随机速度移动都不能通过验证，完全模拟人的移动轨迹才可以通过验证，人的移动轨迹一般是先加速后减速

# 6.初始化：选定链接https://account.geetest.com/login，极验管理后台登录页面
# 初始化一些配置，Selenium对象的初始化及一些参数的配置
import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

EMAIL = 'ra8680592bode@163.com'     # 登录极验需要的用户名
PASSWORD = 'abc123456'              # 登录极验需要的密码
BORDER = 6
INIT_LEFT = 60

class CrackGeetest():
    def __init__(self):
        self.url = 'https://account.geetest.com/login'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.email = EMAIL
        self.password = PASSWORD

    def __del__(self):
        self.browser.close()

# 7.模拟点击：定义方法来获取按钮，利用显示等待方法实现
    def get_geetest_button(self):
        """
        获取初始验证按钮
        :return: 按钮对象
        """
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip')))  # 获取WebElement对象
        return button
        # 点击验证按钮
        # button = self.get_geetest_button()
        # button.click()  # 调用click方法模拟点击


# 8.识别缺口：识别缺口位置
# 获取前后两张比对图片，不一致的地方极为缺口，获取不带缺口图片，利用Selenium选取图片元素，得到所在位置和宽高，获取整个网页的截图
# 图片裁切下来
    def get_position(self):     # 获取图片对象
        '''
        获取验证码位置
        :return: 验证码位置元组
        '''
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_img')))
        time.sleep(2)
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], \
                                   location['x'] + size['width']
        # 获取位置和宽高
        return (top, bottom, left, right)   # 返回左上角和右下角坐标

    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

        # 获取第二张图片，就是带缺口的图片。要使图片出现缺口，点击下方滑块即可
    def get_slider(self):  # 利用get_slider方法获取滑块对象
        """
        获取滑块
        :return:滑块对象
        """
        slider = self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))  # 利用click触发点击
        return slider
        # slider = self.get_slider()
        # slider.click()

    def get_geetest_image(self, name='captcha.png'):    # 获取网页截图
        """
        获取验证码图片
        :return: 图片对象
        """
        top, bottom, left, right = self.get_position()
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))   # 调用crop方法将图片裁切出来
        captcha.save(name)
        return captcha  # 返回Image对象

    def open(self):
        """
        打开网页输入用户名密码
        :return: None
        """
        self.browser.get(self.url)
        email = self.wait.until(EC.presence_of_element_located((By.ID, 'email')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'password')))
        email.send_keys(self.email)
        password.send_keys(self.password)

    def get_gap(self, image1, image2):      # 获取缺口位置的方法，参数为两张图片，一张带缺口，一张不带
        """
        获取缺口偏移量
        :param image1: 不带缺口图片
        :param image2: 带缺口图片
        :return:
        """
        left = 60
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):   # is_pixel_equal()判断两张图片同一位置像素是否相同
                    left = i
                    return left
        return left

# 将得到的两张图片对象，分别赋值给变量image1和image2.对比图片获取缺口，遍历图片每个坐标点，获取两张图片对应像素点RGB数据
# 二者RGB数据差距在一定范围内，代表两个像素相同，继续比对下一个像素点，差距超过一定范围，代表像素点不同，当前位置为缺口位置
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
        threshold = 60
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
            pixel1[2] - pixel2[2]) < threshold: # 比较两张图RGB绝对值是否均小于定义的阈值threshold，绝对值在阈值之内继续遍历
                                                # 否则代表不相同像素点，缺口位置
            return True
        else:
            return False

# 9.模拟拖动：尝试分段模拟，将拖动过程划分几段，每段设置一个平均速度，速度围绕该平均速度小幅度随机抖动，也无法完成验证
# 完全模拟加速减速过程通过验证，前端滑块做匀加速运动，后段滑块做匀减速运动，加速度公式完成验证
# 滑块滑动加速度a，当前速度v，初速度v0，位移x，所需时间t
# 利用x = v0 * t + 0.5 * a * t * t
# v = v0 + a * t    两个公式构造轨迹移动算法，计算出先加速，后减速的运动轨迹
    def get_track(self, distance):      # get_track方法，传入参数为移动的总距离
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []    # 移动轨迹用track表示，是一个列表，列表的每个元素代表每次移动多少距离
        # 当前位移
        current = 0     # 当前位移的距离变量current，初始为0,
        # 减速阈值
        mid = distance * 4 / 5  # 变量mid，减速的阈值，加速到什么位置开始减速，取4/5，前4/5加速，后1/5减速
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0

        while current < distance:   # 当前位移小于总距离
            if current < mid:       # 分段定义加速度，加速过程加速度为2
                # 加速度为正2
                a = 2
            else:
                # 加速度为负3        # 减速过程，加速度为-3
                a = -3
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离 x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t   # 套用位移公式，计算某个时间段内的位移
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))       # 将当前位移更新并记录到轨迹中，
        return track    # 直到运动轨迹达到总距离，循环终止，得到track记录每个时间间隔移动多少位移，滑块的运动轨迹得到了
    # 按照该运动轨迹拖动滑块：
    def move_to_gap(self, slider, track):  # 传入参数为滑块对象和运动轨迹
        """
        拖动滑块到缺口处
        :param slider:滑块
        :param tracks: 轨迹
        :return:
        """
        ActionChains(self.browser).click_and_hold(slider).perform() # 调用ActionChains的click_and_hold方法按住底部滑块
        for x in track:    # 遍历运动轨迹获取每小段位移距离
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()   # 调用move_by_offset移动位移
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()  # 调用release方法松开鼠标
    # 成功登陆后跳转到后台，此识别方法同样适用于其他使用极验验证码3.0网站
    # 代码地址：https://github.com/Python3WebSpider/CrackGeetest
    def login(self):
        """
        登录
        :param self:
        :return:None
        """
        submit = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'login-btn')))
        submit.click()
        time.sleep(10)
        print('登录成功')

    def crack(self):
        # 输入用户名密码
        self.open()
        # 点击验证按钮
        button = self.get_geetest_button()
        button.click()
        # 获取验证码图片
        image1 = self.get_geetest_image('captcha1.png')
        # 点按呼出缺口
        slider = self.get_slider()
        slider.click()
        # 获取带缺口的验证码图片
        image2 = self.get_geetest_image('captcha2.png')
        # 获取缺口位置
        gap = self.get_gap(image1, image2)
        print('缺口位置', gap)
        # 减去缺口位移
        gap -= BORDER
        # 获取移动轨迹
        track = self.get_track(gap)
        print('滑动轨迹', track)
        # 拖动滑块
        self.move_to_gap(slider, track)

        success = self.wait.until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, 'geetest_success_radar_tip_content'), '验证成功'))
        print(success)

        # 失败后重试
        if not success:
            self.crack()
        else:
            self.login()


if __name__ == '__main__':
    crack = CrackGeetest()
    crack.crack()