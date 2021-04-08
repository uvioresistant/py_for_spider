# 回到网页看一下页面的真实源码，在开发者模式下NETwork监听组件中查看源代码
# 不要再Elements中查看，可能经过JavaScript操作而与原始请求不同
# 一部电影信息对应的源代码是一个dd节点，用正则来提取这里的一些信息
# 首先需要提取排名信息，在class为board-index的i节点内，利用非贪婪提取i节点内的信息
# <dd>.*?board-index.*?>(.*?)</i>
# 随后，提取电影的图片，提取第二个img节点的data-src属性，正则改写为：
# <dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)"
# 再提取电影的名称，在后面的p节点内，class为name，用name做标志位，进一步提取到内a节点的正文内容
# <dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>
# 提取主演、发布时间、评分等内容，最后，正则：
# <dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releaset
# ime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction>(.*?)</i>.*?</dd>
# 匹配了七个信息，调用findall方法提取出所有内容
# 定义解析界面方法parse_one_page,通过正则从结果中提取出内容
import requests
import re
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

def parse_one_page(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.'
        '*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction>(.*?)</i>.*?</dd>',
        re.S)
    items = re.findall(pattern, html)
    print(items)


# 将匹配结果处理一下，遍历提取结果并生成字典

def parse_one_page(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.'
        '*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction>(.*?)</i>.*?</dd>',
        re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': items[1],
            'title': item[2].strip(),
            'actor': item[3].strip()[3:] if len(item[3]) > 3 else '',
            'time': item[4].strip()[5:] if len(item[4]) > 5 else '',
            'score': item[5].strip() + item[6].strip()
        }

# 可以成功提取出电影的排名、图片、标题、演员、时间、评分，赋值为一个个的字典，形成结构化数据
# 成功提取了单页的电影信息
