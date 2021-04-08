# 1.请求分析
# 打开XHR过滤器，一直滑动页面以加载新的微博内容，可以看到，会不断有Ajax请求发出
# 选定其中一个请求，分析参数信息，进入详情界面
# 可以发现这是一个GET类型的请求，链接为https//m.weibo.cn/api/container。请求的参数有4个：type、value、containerid和page
# type始终为uid、value得到值就是页面链接中的数字，就是用户的id，containerid就是107603加上用户id。
# 改变的值是page，这个参数是用来控制分页的，page=1代表第一页，page=2代表第二页

# 2.分析响应：观察请求的响应内容：是JSON格式的，最关键的两部分就是cardlistInfo和cards：前者包含比较重要的信息total，微博总数量
# 根据total数字来估算分也数；cards是一个列表，包含10个元素，展开后有一个比较重要的字段mblog。包含的正是微博的attitudes_count赞
# comments_count评论数目、reposts_count转发数目、created_at发布时间、text微博正文
# 请求一个接口、就可以得到10条微博、请求时只需要改变page参数即可，只需要简单做一个循环、就可以获取所有微博了

# 3.实战演练：用程序模拟Ajax请求，将前10页微博全部爬取下来
# 定义方法获取每次请求的结果，page是一个可变参数，将它作为方法的参数传递下来
from urllib.parse import urlencode
import requests
base_url = 'https://m.weibo.cn/api/container/getIndex?' # base_url表示请求的URL的前半部分

headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/2830678474',
    'User-Agent': 'Mozilla/5.0(Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36(KHTML, like Gecko)'
        'Chrome/58.0.3090.110 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
}
def get_page(page): # 构造参数字典，type、value、containerid是固定参数、page是可变参数
    params = {
        'type': 'uid',
        'value': '2830678474',
        'containerid': '1076032830678474',
        'page': page
    }
    url = base_url + urlencode(params)  # 调用urlencode方法将参数转化为URL的GET请求参数，类似type=uid&value=2830678474&
    #containerid=107632830678474&page=2的形式；base_url与参数拼合形成一个新的URL
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:   # 用requests请求这个链接，加入headers参数。判断响应的状态码，200，直接调用json
        print('Error', e.args)


# 定义一个解析方法，从结果中提取想要的信息；如想保存微博的id、正文、赞数、评论数和转发数
# 先遍历cards、然后获取mblog中的各个信息，赋值为一个新的字典返回
from pyquery import PyQuery as pq   # 借助pyquery将正文中的HTML标签去掉

def parse_page(json):
    if json:
        items = json.get('data').get('cards')
        for item in items:
            item = item.get('mblog')
            weibo = {}
            weibo['id'] = item.get('id')
            weibo['text'] = pq(item.get('text')).text()
            weibo['attitudes'] = item.get('attitudes_count')
            weibo['comments'] = item.get('comments_count')
            weibo['reposts'] = item.get('reposts_count')
            yield weibo


# 遍历page，一共10页，将提取到的结果打印输出：
if __name__ == '__main__':
    for page in range(1,11):
        json = get_page(page)
        results = parse_page(json)
        for result in results:
            print(result)


# 还可以加一个方法将结果保存到MongoDB数据库：
from pymongo import MongoClient

client = MongoClient()
db = client['weibo']
collection = db['weibo']

def save_to_mongo(result):
    if collection.insert(result):
        print('Saved to Mongo')
# 所有功能就完成了，运行程序后，查看一下MongoDB，相应的数据被保存到MongoDB
# 通过分析Ajax并编写爬取下来的微博列表。代码地址：https://github.com/Python3WebSpider/WeiboList
