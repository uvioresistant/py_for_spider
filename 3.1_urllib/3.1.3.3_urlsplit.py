# 和urlparse非常相似，不过不再单独解析params这部分，只返回5个结果
# from urllib.parse import urlsplit
#
# result = urlsplit('http://www.baidu.com/index.html;user?id=5#comment')
# print(result)


from urllib.parse import urlsplit

result = urlsplit('http://www.baidu.com/index.html;user?id=5#comment')
print(result.scheme, result[0])