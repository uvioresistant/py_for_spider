# 利用requests构建GET请求的方法
# 构建一个GET请求，网站会判断如果客户端发起的是GET请求的话，返回相应的请求信息
# import requests
#
# r = requests.get('http://httpbin.org/get')
# print(r.text)

# 利用params添加额外的信息
# import requests
#
# data = {
#     'name': 'germey',
#     'age' : 22
# }
# r = requests.get('http://httpbin.org/get', params=data)
# print(r.text)
# 自动构造成了http://httpbin.org/get


# 想直接解析返回结果，得到一个字典格式的话，可以直接调用json方法
# import requests
#
# r = requests.get('http://httpbin.org/get')
# print(type(r.text))
# print(r.json())
# print(type(r.json()))
# 若返回结果不是JSON格式，便会出现解析错误，抛出json.decoder.JSONDecodeError

# 抓取网页
# import requests
# import re
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36(KHTML, like Gecko)'
#         'Chrome/52.0.2743.116 Safari/537.36'
# }
# r = requests.get("https://www.zhihu.com/explore", headers=headers)
# pattern = re.compile('explore-feed.*?question_link.*?>(.*?)</a>', re.S)
# titles = re.findall(pattern, r.text)
# print(titles)
# 加入了headers信息，包含了User-Agent信息，也就是游览器标识信息，如果不加，知乎会禁止抓取。


# 抓取二进制数据
# 想抓取图片、音频、视频等文件，本质上都是由二进制码组成的，有特定的保存格式和对应的解析方式，才可以看到，想要抓取它们，
# 就要拿到它们的二进制码
# import requests
#
# r = requests.get("https://github.com/favicon.ico")
# print(r.text)
# print(r.content)
# 抓取站点图标，就是游览器每一个标签页上的小图标
# 打印了Response对象属性：1.text；2.content；前者打印时转化为str类型，出现乱码；后者结果前带有一个b，代表bytes类型数据


# import requests
#
# r = requests.get("https://github.com/favicon.ico")
# with open('favicon.ico', 'wb')as f:
#     f.write(r.content)
# 用了open方法，第一个参数是文件名称，第二个参数代表以二进制写的形式打开，可以向文件里写入二进制数据
# 同样，音频和视频文件也可以用这种方法获取


# 添加headers
# 通过headers参数来传递头信息，如果不传递headers，就不能正常请求
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36(KHTML, like Gecko)'
        'Chrome/52.0.2743.116 Safari/537.36'
}
r = requests.get("https://www.zhihu.com/explore", headers=headers)
print(r.text)
