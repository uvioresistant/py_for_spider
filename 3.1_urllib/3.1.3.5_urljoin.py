#有了urlunparse和urlunsplit方法，就可以完成链接的合并，前提必须要有特定长度的对象，每一部分都要清晰分开
#生成链接另一个方法：urljoin，可以提供一个base_url(基础链接)作为第一个参数，将新的链接作为第二个参数，
# 该方法会分析base_url的scheme、netloc和path，并对新链接缺失的部分进行补充，返回结果
from urllib.parse import urljoin

print(urljoin('http://www.baidu.com', 'FAQ.html'))
print(urljoin('http://www.baidu.com', 'https://cuiqingcai.com/FAQ.html'))
print(urljoin('http://www.baidu.com/about.html', 'https://cuiqingcai.com/FAQ.html'))
print(urljoin('http://baidu.com/about.html', 'https://cuiqingcai.com/FAQ.html?question=2'))
print(urljoin('http://www.baidu.com?wd=abc', 'https://cuiqingcai.com/index.php'))
print(urljoin('http://www.baidu.com', '?category=2#comment'))
print(urljoin('www.baidu.com', '?category=2#comment'))
print(urljoin('www.baidu.com#comment', '?category=2'))

#base_url提供了三项内容scheme、netloc和path，如果3项在新的链接里不存在，就予以补充
#如果新链接存在，就使用新的链接的部分，而base_url中的params、query和fragment不起作用
#通过urljoin方法，可以轻松实现链接的解析、拼合与生成