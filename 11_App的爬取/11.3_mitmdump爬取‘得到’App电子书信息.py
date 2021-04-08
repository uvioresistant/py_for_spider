# '得到’是一款碎片时间学习的App，官方网站https://www.igetget.com，没有对应的网页版，必须通过App才可以获取，练习mitmdump用法
# 1.目标：爬取App内电子书板块的电子书信息(名称、简介、封面、价格)，并将信息保存到MongoDB,侧重了解mitmdump，App爬取手动非自动
# mitmdump负责捕捉响应并将数据提取保存

# 2.准备：安装好mitmproxy和mitmdump，手机和PC处于同一局域网下，配置号mitmproxy的CA证书，安装好MongoDB并运行，安装PyMongo

# 3.抓取分析：探寻当前页面URL和返回内容：编写脚本：
def response(flow):
    print(flow.request.url)
    print(flow.response.text)
# 只输出请求的URL和响应的Body内容，就是请求链接和响应最关键的部分。脚本保存名称为script.py
# 运行mitmdump命令：mitmdump -s script.py
# 打开“得到”App的电子书页面，便可以看到PC端控制台有相应输出，包含了下一页的电子书内容。
# 可以看到URL为https：//dedao.igetget.com/v3/discover/bookList接口，后面还加了一个sign参数。确定这是获取电子书列表的接口
# 在URL的下方输出的是响应内容，是一个JSON格式的字符串，将它格式化
# 格式化的内容包含一个c字段、一个list字段、list的每个元素都包含价格、标题、描述。

# 4.数据抓取：需要对接口做过滤限制，抓取分析的接口，再提取结果中的对应字段
# 修改脚本：
import json
from mitmproxy import ctx

def response(flow):
    url = 'https://dedao.igetget.com/v3/discover/bookList'
    if flow.request.url.startswith(url):
        text = flow.response.text
        data = json.loads(text)
        books = data.get('c').get('list')
        for book in books:
            ctx.log.info(str(book))
# 重新滑动电子书页面，在PC端控制台观察输出：输出了图书的全部信息，一本图书信息对应一条JSON格式的数据

# 5.提取保存：需要提取信息，再把信息保存到数据库中。
import json
import pymongo
from mitmproxy import ctx
client = pymongo.MongoClient('localhost')
db = client['igetget']
collection = db['books']


def response(flow):
    global collection
    url = 'https://dedao.igetget.com/v3/discover/bookList'
    if flow.request.url.startswith(url):
        text = flow.response.text
        data = json.loads(text)
        books = data.get('c').get('list')
        for book in books:
            data = {
                'title': book.get('operating_title'),
                'cover': book.get('cover'),
                'summary': book.get('other_share_summary'),
                'price': book.get('price')
            }
            ctx.log.info(str(data))
            collection.insert(data)
# 输出的每一条内容都是经过提取后的内容，包含电子书的标题、封面、描述、价格
# 声明MongoDB的数据库连接，提取信息之后调用该对象的insert方法将数据插入到数据库即可

# 代码地址https://github.com/Python3Webspider/IGetGet

