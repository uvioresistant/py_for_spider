# 1.urlparse:该方法可以实现URL的识别和分段：
# from urllib.parse import urlparse
#
# result = urlparse('http://www.baidu.com/index.html;user?id=5#comment', allow_fragments=False) # 利用urlparse进行URL解析
# print(type(result), result)   # 然后将结果也输出出来，返回结果是一个ParseResult类型的对象，包含6个部分，scheme、netloc、
#                                 path、params、query和fragment


# http://www.baidu.com/index.html;user?id=5#comment
# 特定的分隔符，如：://前面的就是scheme；第一个/符号前面便是netloc,即域名，后面是path，访问路径；后面是params，表示参数；
# 问号?后面查询条件query,一般用作GET类型的URL，井号#后面是锚点，用于直接定位页面内部的下拉位置。
# 标准链接格式：
# scheme://netloc/path;params?query#fragment
# 标准URL都会符合这个规则，利用urlparse方法可将它拆分开，API用法：
urllib.parse.urlparse(urlstring, scheme='', allow_fragments=True)

# from urllib.parse import urlparse
#
# result = urlparse('http://www.baidu.com/index.html#comment', allow_fragments=False)
# print(result)


from urllib.parse import urlparse

result = urlparse('http://www.baidu.com/index.thml#comment', allow_fragments=False)
print(result.scheme, result[0], result.netloc, result[1], sep='\n')
