# match方法从字符串开头开始匹配，一旦开头不匹配，就失败
# import re
#
# content = 'Extra strings Hello 1234567 World_This is a Regex Demo Extra stings'
# result =re.match('Hello.*?(\d+).*?Demo', content)
# print(result)
# match更适合用来检测字符串是否符合某个正则表达式规则
# search 在匹配时扫描整个字符串，返回第一个成功匹配的结果，正则表达式可以是字符串的一部分
# import re
#
# content = 'Extra strings Hello 1234567 World_This is a Regex Demo Extra stings'
# result =re.search('Hello.*?(\d+).*?Demo', content)
# print(result)


# HTML文本，正则表达式实例实现相应信息的提取
import re

html = '''<div id ="songs-list">
<h2 class="title">经典老歌</h2>
<p class="introduction">
经典老歌列表
</p>
<ul id="list" class="list-group">
<li data-view="2">一路上有你</li>
<li data-view="7">
<a href="/2.mp3" singer="任贤齐">沧海一声笑</a>
</li>
<li data-view="4" class="active">
<a href="/3.mp3" singer="齐秦">往事随风</a>
</li>
<li data-view="6"><a href="/4.mp3" singer="beyond">光辉岁月</a></li>
<li data-view="5"><a href="/5.mp3" singer="程慧琳">记事本</a></li>
<li data-view="5">
<a href="/6.mp3" singer="邓丽君">但愿人长久</a>
</li>
</ul>
</div>'''
# result = re.search('<li.*?active.*?singer="(.*?)">(.*?)</a>', html, re.S)
# if result:
#     print(result.group(1), result.group(2))


# 若不加active(匹配不带class为active的节点）
# result = re.search('<li.*?singer="(.*?)">(.*?)</a>', html, re.S)
# if result:
#     print(result.group(1), result.group(2))
# 从字符串开头开始搜索，符合条件的节点变成第二个li节点，后面不再匹配


# 若不加re.S,
result = re.search('<li.*?singer="(.*?)">(.*?)</a>', html)
if result:
    print(result.group(1), result.group(2))
# 包含换行符的不会匹配，不包含换行符的成功匹配