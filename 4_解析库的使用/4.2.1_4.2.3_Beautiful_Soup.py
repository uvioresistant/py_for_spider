# 借助网页的结构和属性来解析网页
# Beautiful Soup是HTML或XML解析库，可以方便的从网页中提取数据
# Beautiful Soup是一个工具箱，简单，不需要多少代码可以写出一个完整的应用程序
# Beautiful Soup将输入文档转换为Unicode编码，输出文档转换为UTF-8编码，可以省去很多繁琐的提取工作，提高了解析效率


# 解析器：Beautiful Soup 依赖解析器，支持第三方解析器：
# lxml HTML解析器  BeautifulSoup（markup， "lxml")   速度快、文档容错能力强     需要装C语言库
# lxml XML解析器   BeautifulSoup(markup, "xml")      速度快、唯一支持XML的解析器   需要装C语言库
# html5lib        BeautifulSopu(markup, "html5lib")  最好容错性、以浏览器方式解析文档、生成HTML5格式文档   速度慢
# 如果使用lxml，在初始化Beautiful Soup时，可以把第二个参数改为lxml
from bs4 import BeautifulSoup
soup = BeautifulSoup('<p>Hello</p>', 'lxml')
print(soup.p.string)