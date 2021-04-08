# compile方法将正则字符串编译成正则表达式对象，在后面的匹配中复用
import re

content1 = '2016-12-15 12:00'
content2 = '2016-12-17 12:55'
content3 = '2016-12-22 13:21'
pattern = re.compile('\d{2}:\d{2}')
result1 = re.sub(pattern, '', content1)
result2 = re.sub(pattern, '', content2)
result3 = re.sub(pattern, '', content3)
print(result1, result2, result3)
# 分别将3个日期中的时间去掉，可以借助sub方法，第一个参数是正则表达式，没有必要重复写3个同样的正则表达式，
# 用compile方法将正则表达式编译成一个正则表达式对象，以便复用