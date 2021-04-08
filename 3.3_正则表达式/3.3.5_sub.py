# sub方法把一串文本中的所有数字都去掉
# import re
#
# content = '54aK54yr5oiR54ix5L2g'
# content = re.sub('\d+', '', content)
# print(content)
# 给第一个参数传入\d+匹配所有的数字；第二个参数为替换成的字符串（若去掉，赋值为空）；第三个参数是原字符串


#获取所有li节点的歌名，直接用正则提取可能比较繁琐
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
# results = re.findall('<li.*?>\s*?(<a.*?>)?(\w+)(</a>)?\s*?</li>', html, re.S)
# for result in results:
#     print(result[1])


# 借助sub，先用sub将a节点去掉，只留下文本，再利用findall提取
html = re.sub('<a.*?>|</a>', '', html)
print(html)
results = re.findall('<li.*?>(.*?)</li>', html, re.S)
for result in results:
    print(result.strip())

# 借助sub方法比较简单，用sub方法将a节点去掉，只留下文本；再利用findall直接提取
