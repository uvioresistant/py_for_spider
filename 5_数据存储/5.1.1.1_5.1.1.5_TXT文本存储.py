# 1.TXT文本存储
# TXT文本操作非常简单，且TXT文本兼容任何平台，缺点是不利于检索，若对检索和数据结构要求不高，可以采用
# 2.目标：保存知乎上“发现”页面的“热门话题”部分，将其问题和答案同一保存为文本形式
# 首先，用requests将网页源代码获取下来
# 然后，使用pyquery解析库解析
# 再将提取的标题、回答者、回答，保存到文本
import requests
from pyquery import PyQuery as pq

url = 'https://www.zhihu.com/explore'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36(KHTML, like Gecko)'
        'Chrome/58.0.3029.110 Safari/537.36'
}
html = requests.get(url, headers=headers).text      # requests提取知乎“发现”页面
doc = pq(html)
items = doc('.explore-tab .feed-item').items()
for item in items:
    question = item.find('h2').text()                   # 将热门话题的问题
    author = item.find('.author-link-line').text()      # 作者
    answer = pq(item.find('.content').html()).text()    # 答案全文提取出来
    file = open('explore.text', 'a', encoding='utf-8')  # open方法打开一个文本文件、获取一个文件操作对象，赋值file
    file.write('\n'.join([question, author, answer]))   # write方法将提取的内容写入文件
    file.write('\n' + '=' * 50 + '\n')
    file.close()                                        # 调用close方法关闭
# 主要演示文件保存方式，requests异常处理部分省去。
# 抓取的内容即可写入文本中了
# open方法第一个参数为：要保存得到目标文件名称；第二个参数为a：以追加方式写入到文本


# 3.打开方式:
# open方法第二个参数设置成了a，除此之外，还有以下几种：
# r：只读方式打开文件。文件的指针将会放在文件的开头。默认模式
# rb: 以二进制只读方式打开一个文件。文件指针将会放在文件的开头
# r+: 读写方式打开一个文件。文件指针将会放在文件的开头
# rb+: 二进制读写方式打开一个文件。文件指针放在文件开头
# w：写入方式打开一个文件。若文件已存在，将其覆盖；不存在，创建新文件
# wb：二进制写入方式打开文件。若文件已存在，将其覆盖；不存在，创建新文件
# w+: 读写方式打开文件。若文件已存在，将其覆盖；不存在，创建新文件
# wb+：二进制读写格式打开文件。若文件已存在，将其覆盖；不存在，创建新文件
# ab: 二进制追加方式打开文件。若文件存在，文件指针会放在文件结尾。文件打开时是追加模式，


# 4.简化写法
# 文件写入还有一种简写方法，使用with as写法。在with控制块结束时，文件自动关闭，不需要再调用close方法。
with open('explore.txt', 'a', encoding='utf-8') as file:
    file.write('\n'.join([question, author, answer]))
    file.write('\n' + '=' * 50 + '\n')

# 想保存时将原文清空，可以将第二个参数改写为w
with open('explore.txt', 'w', encoding='utf-8') as file:
    file.write('\n'.join([question, author, answer]))
    file.write('\n' + '=' * 50 + '\n')
# 以上是利用Python将结果保存为TXT文件的方法，简单易用，操作高效，是最基本的保存数据的方法
