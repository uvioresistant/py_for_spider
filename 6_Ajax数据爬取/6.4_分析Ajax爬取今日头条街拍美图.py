# 抓取目标是今日头条的街拍美图，完成后，将每组图片分文件夹下载本地并保存下来
# 2.抓取分析：
# 分析抓取逻辑：今日头条首页:http://www.toutiao.com/,右上角搜索入口，尝试抓取街拍美图，输入"街拍"搜索
# 首先打开第一个网络请求，这个请求得到URL就是当前链接：http://www.toutiao.com/search/?keyword=街拍，
# 打开Preview选项卡查看Response Body，如果页面中的内容是根据第一个请求得到的结果渲染出来的，则请求的源代码必然会包含页面的文字
# 源代码中并没有包含这两个字，搜索匹配结果数目为0，可以初步判断这些内容是由Ajax加载，用JS渲染出来的，切换XHR，查看Ajax
# 点击data展开，点击第一条，发现有一个title字段，值就是页面中第一条数据的标题
# 每条数据还有一个image_detail字段，是列表形式，，其中就包含组图的所有图片列表
# 只需将列表汇总的rul字段提取出来，并下载就好了，每一组图都建立一个文件夹，文件夹的名称就为组图的标题
# 直接用有、Python来模拟这个Ajax请求，然后提取出相关美图链接并下载，先需要分析URL的规律
# 切换回Headers选项卡，观察它的请求RUL和Headers信息
# 这是一个GET请求，请求URL的参数有：offset、format、keyword、autoload、count、cur_tab
# 滑动页面，多加载一些新结果，加载的同时可以发现，Network中又出现了许多Ajax请求，观察后续链接的参数，发现变化的参数只有offset
# 第二次的offset为20，第三次为40，offset就是偏移量，进而推断出count参数就是一次性获取的数据条数，可以用offset来控制数据分页
# 通过接口批量获取数据，然后将数据解析，将图片下载下来

# 3.实现方法get_page来加载单个Ajax请求的结果，唯一变化的参数就是offset，把它当做参数传递
import requests
from urllib.parse import urlencode

def get_page(offset):
    params = {
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1',
    }
    url = 'http://www.toutiao.com/search_content/?' + urlencode(params) #urlencode方法构造请求的GET参数
    try:
        response = requests.get(url) # 用requests请求这个链接，
        if response.status_code == 200: # 如果返回状态码为200，
            return response.json()      # 则调用response方法将结果转为JSON格式，然后返回
    except requests.ConnectionError:
        return None

# 再实现一个解析方法：提取每条数据的image_detail字段中的每一张图片链接，将图片链接和图片所属的标题一并返回，构造一个生成器
def get_images(json):
    if json.get('data'):
        for item in json.get('data'):
            title = item.get('title')
            images = item.get('image_detail')
            for image in images:
                yield {
                    'image': image.get('url'),
                    'title': title
                }



# 接下来，实现保存图片的方法save_image,item就是前面get_images方法返回的一个字典。
import os
from hashlib import md5

def save_image(item):
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        response = requests.get(item.get('image'))
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}'.format(item.get('title'), md5(response.content).hexdigest(), 'jpg')
            if not os.open.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print('Already Downloaded', file_path)
    except requests.ConnectionError:
        print('Failed to Save Image')
# 只需要构造一个offset数组，遍历offset，提取图片链接，并下载即可
from multiprocessing.pool import Pool

def main(offset):
    json = get_page(offset)
    for item in get_images(json):
        print(item)
        save_image(item)


GROUP_START = 1     # 定义了分页的起始页数
GROUP_END = 20      # 定义了分页的终止页数

if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_END, GROUP_END + 1)])
    pool.map(main.groups)   # 利用了多线程的线程池，调用map方法实现多线程下载
    pool.close()
    pool.join()
# 本节的代码地址：https://github.com/Python3WebSpider/Jiepai.了解了Ajax分析的流程、Ajax分页的模拟以及图片的下载过程