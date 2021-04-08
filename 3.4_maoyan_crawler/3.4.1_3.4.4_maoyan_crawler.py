# 3.4.1
# 选用正则表达式来作为解析工具
# 3.4.1目标
# 提取出猫眼电影TOP100的电影名称、时间、评分、图片，站点URL为http://maoyan.com/board/4，提取结果以文件形式保存下来
# 3.4.2
# 安装requests库
# 3.4.3
# 网页滚动到最下方，可以发现有分页的列表，点击第2页，发现URL变成了http://maoyan.com/board/4?offset=10,比之前的URL多了
# 一个offset偏移量值，如果偏移量为n，则显示的电影序号为n+1到n+10，每页显示10个，想获取TOP100，只需分开请求10次
# 3.4.4
#  首先抓取第一页内容，实现了get_one_page方法，传入url参数，将抓取的页面结果返回，再通过main方法调用
import requests

def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36(KHTML, like Gecko)'
                      'Chrome/52.0.2743.116 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None

def main():
    url = 'http://maoyan.com/board/4'
    html = get_one_page(url)
    print(html)

main()