# 将内容转化为URL编码的格式
# URL中带有中文参数时，有时可能会导致乱码问题，用这个方法可以将中文字符转化为URL编码
from urllib.parse import quote

keyword = '壁纸'
url = 'https://www.baidu.com/s?wd=' + quote(keyword)
print(url)

# 声明了一个中文的搜索文字，用quote方法对其进行URL编码