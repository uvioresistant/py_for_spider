# 直接使用模拟浏览器运行的方式来实现，可以做到可见即可爬，python提供了许多模拟浏览器运行的库，如Selenium、Splash、PyV8、Ghost
# Selenium是自动化测试工具，利用它可以驱动浏览器执行指定的动作，如点击、下拉
# 2.Selenium 功能如下：
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# browser = webdriver.Chrome()    # 自动弹出一个Chrome浏览器
# try:
#     browser.get('https://www.baidu.com')    # 首先跳转到百度
#     input = browser.find_element_by_id('kw')
#     input.send_keys('Python')       # 在搜索框中输入Python，跳转到搜索结果
#     input.send_keys(Keys.ENTER)
#     wait = WebDriverWait(browser, 10)
#     wait.until(EC.presence_of_all_elements_located((By.ID, 'content_left')))
#     print(browser.current_url)  # 搜索结果加载出来后，分别输出当前的URL
#     print(browser.get_cookies()) # 当前的Cookies
#     print(browser.page_source)  # 网页源代码
# finally:
#     browser.close()
# 用Selenium驱动浏览器加载网页，可以直接拿到JS渲染的结果，不用担心使用的是什么加密系统

# 3.声明浏览器对象
# 初始化：
# from selenium import webdriver
#
# browser = webdriver.Chrome()    # 完成浏览器对象的初始化并将其赋值为browser对象
# browser = webdriver.Firefox()
# browser = webdriver.Edge()
# browser = webdriver.PhantomJS()
# browser = webdriver.Safari()
# 4.访问页面:get方法请求网页，参数传入链接URL，用get方法访问淘宝，然后打印出源代码
# from selenium import webdriver
#
# browser = webdriver.Chrome()
# browser.get('htttps://www.taobao.com')
# print(browser.page_source)
# browser.close()
# 弹出了Chrome浏览器并自动访问淘宝，控制台输出淘宝页面的源代码，游览器关闭


# 5.查找节点：
# Selenium提供了一系列查找节点的方法，可以用这些方法来获取想要的节点

# 单个节点：从淘宝页面中提取搜索框节点，观察源代码：
# 它的id是q，name也是q。如find_element_by_name是根据name值获取，find_element_by_id是根据id获取：
# from selenium import webdriver
# browser = webdriver.Chrome()
# browser.get('https://www.taobao.com')
# input_first = browser.find_element_by_id('q')   # 根据ID获取
# input_second = browser.find_element_by_css_selector('#q')   # 根据CSS选择器获取
# input_third = browser.find_element_by_xpath('//*[@id="q"]') # 根据XPath获取，返回结果完全一致
# print(input_first, input_second, input_third)
# browser.close()

# 列出所有获取单个节点的方法：
# find_element_by_id
# find_element_by_name
# find_element_by_xpath
# find_element_by_link_text
# find_element_by_partial_link_text
# find_element_by_tag_name
# find_element_by_class_name
# find_element_by_css_selector

# Selenium提供通用方法find_element，还需要传入两个参数：查找方式By和值，就是find_element_by_id方法的通用函数版本
# 比如find_element_by_id(id)就等价于find_element(By.ID, id)，二者结果完全一致
# from selenium import webdriver
# from selenium.webdriver.common.by import By
#
# browser = webdriver.Chrome()
# browser.get('https://www.taobao.com')
# input_first = browser.find_element(By.ID,'q')
# print(input_first)
# browser.close()


# 多个节点：find_elements方法
# 查找淘宝左侧导航条所有条目
# from selenium import webdriver
#
# browser = webdriver.Chrome()
# browser.get('https://www.taobao.com')
# lis = browser.find_elements_by_css_selector('.service-db li')
# print(lis)
# browser.close()
# 得到的内容变成了列表类型，每个节点都是WebElement类型
# find_elements_by_id
# find_elements_by_name
# find_elements_by_xpath
# find_elements_by_link_text
# find_elements_by_partial_link_text
# find_elements_by_tag_name
# find_elements_by_class_name
# find_elements_by_css_selector

# 直接用find_elements方法来选择，lis = browser.find_elements(By.CSS_SELECTOR, '.service-bd li')结果完全一致
# from selenium import webdriver
#
# browser = webdriver.Chrome()
# browser.get('https://www.taobao.com')
# lis = browser.find_elements(By.CSS_SELECTOR, '.service-bd li')
# print(lis)
# browser.close()


# 6.节点交互
# 让游览器模拟一些动作
# 输入文字：send_keys方法，清空文字：clear方法，点击按钮click方法
# from selenium import webdriver
# import time
#
# browser = webdriver.Chrome()
# browser.get('https://www.taobao.com')
# input = browser.find_element_by_id('q')
# input.send_keys('iphone')
# time.sleep(1)
# input.clear()
# input.send_keys('iPad pro')
# button = browser.find_element_by_class_name('btn-search')
# button.click()


# 7.动作链
# 交互动作都是针对某点节点执行的。
# 对于输入框，调用它的输入文字和清空文字方法；
# 对于按钮，调用它的点击方法
# 没有特定的执行对象，鼠标拖拽、键盘按键，用动作链来执行

# 如实现一个节点的拖拽操作，将某个节点从一处拖拽到另外一处
# from selenium import webdriver
# from selenium.webdriver import ActionChains
#
# browser = webdriver.Chrome()
# url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
# browser.get(url)    # 打开网页中的一个拖拽实例
# browser.switch_to.frame('iframeResult')
# source = browser.find_element_by_css_selector('#draggable')     # 依次选中要拖拽的节点
# target = browser.find_element_by_css_selector('#droppalbe')     # 拖拽到的目标节点
# actions = ActionChains(browser)     # 声明ActionChains对象并将其赋值为actions变量
# actions.drag_and_drop(source, target)   # 调用actions变量的drag_and_drop方法
# actions.perform()       # 调用perform方法执行动作，完成拖拽操作


# 8.执行JS
# selenium API并没有提供默写操作，如下拉进度条，可以直接模拟运行JS，使用execute_script方法即可实现
# from selenium import webdriver
#
# browser = webdriver.Chrome()
# browser.get('https://www.zhihu.com/explore')
# browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')    # 利用execute_script方法将进度条下拉到最底部
# browser.execute_script('alert("To Bottom")')     # 弹出alert提示框
# 基本上API没有提供的所有功能都可以执行JS方式来实现了


# 9.获取节点信息：get_attribute方法
# 获取节点的属性，前提是先选中这个节点
# from selenium import webdriver
# from selenium.webdriver import ActionChains
#
# browser = webdriver.Chrome()
# url = 'https://www.zhihu.com/explore'
# browser.get(url)
# logo = browser.find_element_by_id('zh-top-link-logo')
# print(logo)
# print(logo.get_attribute('class'))
# 通过get_attribute方法，传入想要获取的属性名，就可以得到它的值


# 获取文本值
# 每个WebElement节点都有text属性，调用，就可以得到节点内部的文本信息，相当于Beautiful Soup的get_text方法、pyquery的text方法
# from selenium import webdriver
#
# browser = webdriver.Chrome()
# url = 'https://www.zhihu.com/explore'
# browser.get(url)
# input = browser.find_element_by_class_name('zu-top-add-question')
# print(input.text)


# 获取id、位置、标签名和大小
# id属性：获取节点id；location属性：获取该节点在页面中的相对位置；tag_name属性可以获取标签名称；size属性可以获取节点大小即宽高
# from selenium import webdriver
#
# browser = webdriver.Chrome()
# url = 'https://www.zhihu.com/explore'
# browser.get(url)
# input = browser.find_element_by_class_name('zu-top-add-question')   # 获得“提问”按钮节点
# print(input.id)     # 调用其id
# print(input.location)
# print(input.tag_name)
# print(input.size)


# 切换Frame
# 网页中的子节点iframe，就是子Frame，相当于页面的子页面，结构和外部网页的结构完全一致
# Selenium默认在父级Frame里操作，如果页面中有子Frame，不能获取，需要用switch_to.frame方法来切换Frame
# import time
# from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
#
# browser = webdriver.Chrome()
# url = 'https://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
# browser.get(url)
# browser.switch_to.frame('iframeResult') # 通过switch_to.frame方法切换到子Frame里面
# try:
#     logo = browser.find_element_by_class_name('logo')   # 尝试获取父级Frame里的logo节点
# except NoSuchElementException:          # 不能找到，抛出NoSuchElementException异常
#     print('NO LOGO')
# browser.switch_to.parent_frame()    # 重新切换回父级Frame，想获取子Frame中的节点，调用switch_to.frame方法切换到对应的Frame
# logo = browser.find_element_by_class_name('logo')
# print(logo)
# print(logo.text)


# 11.延时等待：get方法会在网页框架加载结束后结束执行，此时获取page_source在网页源代码中不一定能获取，需要延时等待，确保加载出来
# 隐式等待：Selenium没有在DOM中找到节点，继续等待，超出设定时间后，抛出找不到节点的异常，默认等待时间为0
# from selenium import webdriver
#
# browser = webdriver.Chrome
# browser.implicitly_wait(10)     # 用implicitly_wait方法实现隐式等待
# browser.get('https://www.zhihu.com/explore')
# input = browser.find_element_by_class_name('zu-top-add-question')
# print(input)


# 显示等待：指定要查找的节点，指定一个最长等待时间，规定时间内加载出来，返回；否则抛出超时异常
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import excepted_conditions as EC


browser = webdriver.Chrome()
browser.get('https://www.taobao.com/')
wait = WebDriverWait(browser, 10)       # 引入WebDriver对象，指定最长等待时间
input = wait.until(EC.presence_of_element_located((By.ID, 'q')))    # 调用until方法，传入等待条件expected_conditions
    # 参数是节点的定位元组，即ID为q的节点搜索框，10秒内如果ID为q的节点（搜索框）加载出来，返回节点，否则抛出异常
button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-search')))
print(input, button)
# 对于按钮，更改一下等待条件，可点击，改为element_to_be_clickable；查找CSS选择器为.btn-search的按钮，10s内可点击，加载成功


# 12.前进和后退：back方法后退，forward方法前进
import time
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.baidu.com/')  # 连续
browser.get('https://www.taobao.com/') # 访问3个
browser.get('https://www.python.org/') # 页面
browser.back()  # 调用back方法回到第二个页面
time.sleep(1)
browser.forward()   # 调用forward方法前进到第三个页面
browser.close()


# 13.Cookies：使用selenium可以对Cookies进行操作，获取、添加、删除Cookies
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.zhihu.com/explore')    # 访问知乎
print(browser.get_cookies())    # 调用get_cookies方法获取所有Cookies
browser.add_cookie({'name': 'name', 'domain': 'www.zhihu.com', 'value': 'germey'})  # 添加一个Cookie，传入字典
print(browser.get_cookies())    # 再次获取所有Cookies
browser.delete_all_cookies()    # 用delete_all_cookies方法删除所有Cookies
print(browser.get_cookies())    # 重新获取，结果为空


# 14.选项卡管理
import time
from selenium import webdriver

browser = webdriver.Chrom()
browser.get('https://www.baidu.com')        # 访问百度
browser.execute_script('window.open()')     # 调用execute_script方法，传入window.open这个JS语句开启选项卡
print(browser.window_handles)       # window_handles获取当前开启的所有选项卡，返回选项卡代号列表
browser.switch_to_window(browser.window_handles[1])     # 切换选项卡，调用switch_to_window，参数是选项卡代号，打开新页面
browser.get('https://www.taobao.com')       # 在第二个选项卡下打开一个新页面
time.sleep(1)
browser.switch_to_window(browser.window_handles[0])     # 切换回第一个选项卡，重新调用switch_to_window方法
browser.get('https://python.org')


# 15.异常处理：超时、节点未找到，用try except来捕获各种异常
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.baidu.com')    # 打开百度页面
browser.find_element_by_id('hello')     # 尝试选择一个并不存在的节点，就会遇到异常
# 抛出NoSuchElementException异常，通常是节点未找到的异常。为了防止程序遇到异常而中断，需要捕获这些异常
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException

browser = webdriver.Chrome()
try:                                        # try except来获取各类异常
    browser.get('https://www.baidu.com')
except TimeoutException:
    print('Time Out')
try:
    browser.find_element_by_id('hello')     # 对find_element_by_id查找节点方法捕获NoSuchElementException异常
except NoSuchElementException:
    print('No Element')
finally:
    browser.close()

