# Appium是跨平台移动端自动化测试工具，可以模拟App内部的各种操作，如点击、滑动、文本输入，手工操作的动作Appium都可以完成。
# Appium继承了Selenium，Appium利用WebDriver实现App的自动化测试。
# 对iOS设备，Appium使用UIAutomation来实现驱动。对于Android来说，使用UiAutomator和Selendroid来实现驱动
# Appium相当于服务器，可以向Appium发送一些操作指令，Appium就会根据不同的指令对移动设备进行驱动，完成不同的动作
# 对于爬虫来说，用Selenium来抓取JS渲染的页面，可见即可爬。Appium同样也可以，用Appium来做App爬虫是一个好的选择
# 1.目标：用微信来演示Appium启动和操作App的方法，利用Appium进行自动化测试的流程以及相关API的用法

# 2.准备：PC安装好Appium、Android开发环境和Python的Appium API，安装好微信

# 3.启动App有两种：用Appium内置的驱动器打开App，利用Python程序实现
# 点击Start Server按钮，相当于开启了Appium服务器。通过Appium内置的驱动或Python代码向Appium服务器发送一系列操作指令，Appium根
# 据不同的指令对移动设备进行驱动，完成不同的动作
# Android手机数据线和运行Appium的PC相连，打开USB调试，
# 输入adb来测试连接情况：adb devices -l；出现List of devices attached，连接成功
# 点击Appium中的Start New Session，
# 需要配置启动App时的Desired Capablilities参数，
# 分别是platformName：平台名称，区分Android和IOS，此处填写Android
# deviceName：设备名称，手机具体类型
# appPackage：App程序包名
# appActivity：入口Activity名，通常以.开头




# 使用Python代码驱动App的方法：
# 在代码中指定一个Appium Server，此Server在打开Appium的时候已经开启了，在4723端口运行
# server = 'http://localhost:4723/wd/hub'
# 字典来配置Desired Capablities
# desired_caps = {
#     'platformName': 'Android',
#     'deviceName': 'MI 5',
#     'appPackage': 'com.tencent.mm',
#     'appActivity': '.ui.LauncherUI'
# }
# 新建一个Session，类似点击Appium的Start Session按钮功能：
# from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

# driver = webdriver.Remote(server, desired_caps)
# 运行，启动微信App，单仅仅是启动

# 再用代码模拟演示的两个动作：1.点击“登录”，2.输入手机号
# 刚才Appium内置的Recorder录制生成的Python代码，非常繁琐，点击“登录”：
# el1 = driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/"
#    "android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/"
#    "android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/"
#    "android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ImageView")
# el1.click()
# 此代码的XPath选择器路径太长，容易超时异常，修改为通过ID查找元素，设置延时等待，两次操作代码如下：
# wait = WebDriverWait(driver, 30)
# login = wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/cjk')))
# login.click()
# phone = wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/h2')))
# phone.set_text('13297916110')
# 完整代码：
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

server = 'http://localhost:4723/wd/hub'

desired_caps = {
    'platformName': 'Android',
    'deviceName': 'MI 5',
    'appPackage': 'com.tencent.mm',
    'appActivity': '.ui.LauncherUI'
}
driver = webdriver.Remote(server, desired_caps)
wait = WebDriverWait(driver, 30)
login = wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/cjk')))
login.click()
phone = wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/h2')))
phone.set_text('13297916110')


# 4.API
# 代码操作App、总结相关API用法，使用Python库为AppiumPythonClient，继承自Selenium，使用方法与Selenium有许多相同之处
# 初始化：配置Desired Capabilities：
from appium import webdriver
server = 'http://localhost:4723/wd/hub'

desired_caps = {    # 启动微信App，Appnium会自动查找手机上的包名和入口类，启动。
    'platformName': 'Android',
    'deviceName': 'MI 5',
    'appPackage': 'com.tencent.mm', # 包名和入口类的名称可以在安装包的AndroidManifext.xml文件获取
    'appActivity': '.ui.LauncherUI'
}
driver = webdriver.Remote(server, desired_caps)

# 打开的App没有在手机上安装，可以直接指定App参数为安装包所在路径，程序启动时会向手机安装并启动App
from appium import webdriver
server = 'http://localhost:4723/wd/hub'
desired_caps = {
    'platformName': 'Android',
    'deviceName': 'MI 5',
    'app': './weixin.apk'
}
driver = webdriver.Remote(server, desired_caps)

    # 查找元素：使用Selenium中通用查找方法实现元素查找
el = driver.find_element_by_id('com.tencent.mm:id/cjk')
# Android中，还可以使用UIAutomator进行元素选择
el = self.driver.find_element_by_android_uiautomator('new UiSelector().description("Animmation")')
els = self.driver.find_element_by_android_uiautomator('new UiSelector().clickable(trye)')

    # 点击:tap方法，可模拟手指（最多五个),可设置按时长短(毫秒):
tap(self, positions, duration=None) # positions:点击的位置组成的列表； duration:点击持续时间
# driver.tap([100, 20), (100, 60), (100, 100)], 500) 可以模拟点击屏幕的某几个点
# 对某个元素如按钮，可以直接调用click放啊模拟：
button = find_element_by_id('com.tencent.mm:id/btn')
button.click()

    # 屏幕拖动：scroll方法模拟屏幕滚动：
# scroll(self, origin_el, destination_el)   # original_el:被操作的元素； destination_el：目标元素
# 实现从元素origin_el滚动至元素destination_el
# driver.scroll(el1,el2）

# 使用swipe模拟A点滑动到B点，
# swipe（self, start_x, end_x, end_y, duratioin=None)    # start_x：开始位置的横坐标  start_y: 开始位置纵坐标
                                                         # end_x:终止位置横坐标； end_y： 终止位置纵坐标
                                                         # duration： 持续时间，单位毫秒
# driver.swipe(100, 100, 100, 400, 5000)    5s内，由(100, 100)滑动到(100,400)
# 使用flick放啊模拟从A点快速滑动到B点
# flick(self, start_x, start_y, end_x, end_y)           # start_x：开始位置的横坐标  start_y: 开始位置纵坐标
                                                        # end_x:终止位置横坐标； end_y： 终止位置纵坐标
# driver.flick(100, 100, 100, 400)

    # 拖拽:drag_and_drop将某个元素拖动到另一个目标元素上
# 实现将元素origin_el拖拽至元素destination_el
drag_and_drop(self, origin_el, destination_el)  # original_el：被拖拽元素； destination_el目标元素
driver.drag_and_drop(el1, el2)

    # 文本输入:使用set_text方法
# el = find_element_by_id('com.tencent.mm:id/cjk')
# el.set_text('Hello')

    # 动作链: 类似Selenium中的ActioinChains，可支持方法：tap、press、long_press、release、move_to、wait、cancel
# el = self.driver.find_element_by_class_name('listView')
a1 = TouchAction()
a1.press(els[0]).move_to(x=10, y=0).move_to(x=10, y=-75).move_to(x=10, y=-600).release()
a2 =TouchAction()
a2.prese(els[1]).move_to(x=10, y=10).move_to(x=10, y=-300).move_to(x=10, y=-600).release()


