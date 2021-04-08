# 需要抓取的是TOP100的电影，还需要遍历一下，给链接传入offset参数，添加如下调用
# if __name__== '__main__':
#     for i in range(10):
#         main(offset=i * 10)
# 需要将main方法修改一下，接收一个offset值作为偏移量，然后构造URL进行爬取
# def main(offset):
#     url = 'http://maoyan.com/board/4?offset=' + str(offset)
#     html = get_one_page(url)
#     for item in parse_one_page(html):
#         print(item)
#         write_to_file(item)
import json
import requests
from requests.exceptions import RequestException
import re
import time


def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36(KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],    # .strip()
            'actor': item[3].strip()[3:],   # if len(item[3]) > 3 else ''
            'time': item[4].strip()[5:],   # if len(item[4]) > 5 else ''
            'score': item[5] + item[6]    # .strip() .strip()
        }


def write_to_file(content):
    with open('result1.txt', 'a', encoding='utf-8') as f:
        # print(type(json.dumps(content)))
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(10):
        main(offset=i * 10)
        time.sleep(1)

# 10.代码地址：https://github.com/Python3WebSpider/MaoYan