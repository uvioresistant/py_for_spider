# findall方法，获取匹配正则表达式的所有内容
# 想获取所有a节点的超链接、歌手和歌名，可以将search方法换成findall方法
# 有返回结果，就是列表类型，需要遍历一下来依次获取每组内容
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
results = re.findall('<li.*?href="(.*?)".*?singer="(.*?)">(.*?)</a>', html, re.S)
print(results)
print(type(results))
for result in results:
    print(result)
    print(result[0], result[1], result[2])
# 返回的列表中的每个元素都是元组类型，用对应的索引依次取出
# 获取第一个内容，用search，提取多个内容时，可以用findall方法
