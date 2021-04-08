# 淘宝整个页面数据是通过Ajax获取的，但是这些Ajax接口参数比较复杂，可能会包含加密密钥，想自己构造Ajax参数，还是比较困难的
# 最方便快捷的抓取方法就是通过Selenium模拟游览器操作，抓取淘宝的商品信息，并将结果保存到MongoDB
# 2.PhantomJS和Firefox配置好了GeckoDriver

# 3.接口分析：
# 打开淘宝，搜索ipad，f12，接货Ajax请求，可以发现获取商品列表的接口：链接包含了几个GET参数
# 想构造Ajax链接，但Ajax接口包含几个参数，其中_ksTS、 rn参数不能直接发现规律，去探索会很烦琐
# 直接用Selenium来模拟浏览器，只要在浏览器中可以看到的，都可以爬取

# 4.页面分析：商品条目：包含商品图片、名称、价格、购买人数、店铺名称、店铺所在地，将这些信息都抓取下来
# 抓取入口为淘宝的搜索页面，链接可以直接构造参数访问；搜索iPad，直接访问https://s.taobao.com/search?q=iPad，呈现第一页结果
# 页面下方有分页导航，既包括前5页链接，也包括下一页链接，还有一个输入任意页码跳转的链接
# 搜索结果最大为100页，获取每一页内容，只需将页面从1到100顺序遍历即可
# 不直接点击”下一页“的原因是：一旦出现异常退出，再点击”下一页‘就无法快速切换到对应的后续页面；此外爬取过程中，
# 需要记录当前也马上，页面加载失败，还需要做异常检测，检测当前页面是加载到了第几页
# 故选择用直接跳转的方式来爬取页面
# 成功加载出某一页商品列表时，利用Selenium可获取页面源代码，再用相应解析库解析，选用pyquery进行解析

# 5.获取商品列表
# 首先，构造抓取的URL：https://s.taobao.com/search?q=iPad;q就是要搜索的关键字，只要改变中国参数，即可获取不同商品的列表
# 将商品的关键字定义成变量，构造URL
# 用Selenium进行抓取，实现如下抓取列表页方法：
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
import pymongo

browser = webdriver.Chrome()        # 构造一个WebDriver对象，使用浏览器是Chrome
wait = WebDriverWait(browser, 10)   # 等待加载，使用WebDriverWait对象，可以指定等待时间，同时指定最长等待时间10s
KEYWORD = 'iPad'            # 指定关键词iPad

def index_page(page):       # 定义index_page方法，用于抓取商品列表页
    """抓取索引页
    :param page: 页码
    """
    print('正在爬取第', page, '页')
    try:
        url = 'https://s.taobao.com/search?q=' + quote(KEYWORD) # 访问搜索商品的链接
        browser.get(url)
        if page > 1:        # 判断当前页码，若大于1，进行跳页
            input = wait.until(     # 翻页操作，赋值为input，
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
            submit = wait.until(    # 获取确定按钮，赋值为submit
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form >'
                                                             'span.btn.J_Submit')))
            input.clear()           # 清空输入框，调用clear方法
            input.send_keys(page)   # 调用send_keys方法将页码填充到输入框中
            submit.click()          # 点击"确定”按钮
        wait.until(         # 否则等待页面加载完成
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), #使用等待条件
# text_to_be_present_in_element，会等待指定文本出现在某一个节点里时，返回成功，将高亮页码节点对应CSS选择器和要跳转页码通过参数
         #传递给这个等待条件，会检测高亮页码节点是不是传过来的页码数，是，就证明页面成功跳转到了这一页，页面跳转成功
        str(page))) # 刚才实现的index_page方法可以传入对应的页码
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemliset .items .item'))) # 最终等待商品信息，
        # 加载出来，指定presence_of_element_located条件，然后传入.m-itemlist .items .item选择器，对应内容就是商品信息块
        get_products()  # 加载成功，执行后续get_products()方法，提取商品信息
    except TimeoutException:    # 到了最大等待时间还没有加载出来，抛出超时异常
        index_page(page)

# 6.解析商品列表：实现get_products方法解析商品列表
# 直接获取页面源代码，用pyquery进行解析
from pyquery import PyQuery as pq
def get_products():
    """
    提取商品数据
    """
    html = browser.page_source  # 调用page_source属性获取页码的源代码
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items() # 构造PyQuery解析对象，提取商品列表
    # 使用的CSS选择器#mainsrp-itemlist .items .item
    for item in items:      # 进行遍历，for循环将每个结果分别解析，每次循环把它赋值为item变量，每个item变量都是PyQuery对象
        product = {
            'image': item.find('.pic .img').attr('data-src'),   # 调用find方法，传入CSS选择器，可以获取单个商品特定内容
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location':item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)


# 7.保存到MongoDB
MONGO_URL = 'localhost'     # 创建MongoDB连接对象
MONGO_DB = 'taobao'
MONGO_COLLECTION = 'products'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]   # 指定数据库
def save_to_mongo(result):
    """保存至MongoDB
    :param result: 结果
    """
    try:
        if db[MONGO_COLLECTION].insert(result):     # 指定Collection名称，调用insert方法将数据插入MongoDB，
            # result变量就是get_products()方法传来的product，包含单个商品的信息
            print('存储到MongoDB成功')
    except Exception:
        print('存储到MongoDB失败')


# 8.遍历每页
# 定义的get_index方法需要接受参数page页码，实现页码遍历
MAX_PAGE = 100
def main():
    """
    遍历每一页
    """
    for i in range(1, MAX_PAGE + 1):    # 调用一个for循环，定义最大页码数100，range方法返回1到100列表，顺序遍历
        index_page(i)

# 9.运行：首先会弹出一个Chrome浏览器，然后访问淘宝页面，控制台输出相应提取结果
# 商品信息结果都是字典形式，被存储到MongoDB


# 10.Chrome Headless模式：无界面模式，不弹出浏览器，
# 启用Headless模式方式：
# chrome_options = webdriver.ChromeOptions()  # 创建ChromeOptions对象
# chrome_options.add_argument('--headless')   # 添加headless参数
# browser = webdriver.Chrome(chrome_options=chrome_options)   # 初始化Chrome对象时，通过chrome_options传递ChromeOptions对象

# 11.对接Firefox：只需更改一处
# browser = webdriver.Firefox()


# 12.对接PhantomJS：抓取时不会弹出敞口，只需将WebDriver声明修改一下
# browser = webdriver.PhantomJS()
# 还支持命令行配置，可以设置缓存和禁用图片加载功能，提高爬取效率
# SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']
# browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
# 代码地址：https://github.com/Python3WebSpider/TaobaoProduct
