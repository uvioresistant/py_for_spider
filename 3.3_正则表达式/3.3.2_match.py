# 1.向match传入要匹配的字符串以及正则表达式，可以检测这个正则表达式是否匹配字符串
# match尝试从字符创的起始位置匹配正则表达式，如匹配，就返回匹配成功结果；不匹配，返回None
# import re
#
# content = 'Hello 123 4567 World_This is a Regex Demo'
# print(len(content))
# result = re.match('^Hello\s\d\d\d\s\d{4}\s\w{10}', content)
# print(result)
# print(result.group())
# print(result.span())
# ^匹配字符串开头; \s匹配空白字符; \d匹配数字; {4}表示匹配前面规则4次; \w{10}匹配10个字母及下划线
# group方法输出匹配到的内容； span方法输出匹配范围

# 2.从字符串中提取一部分内容：使用()将想提取的子字符串括起来，实际上标记了一个子表达式开始和结束位置
# 被标记的每个子表达式一次对应每一个分组，调用group方法传入分组的索引，可获取提取的结果
#
# import re
#
# content = 'Hello 123456 World_This is a Regex Demo'
# result = re.match('^Hello\s(\d+)\sWorld', content)
# print(result)
# print(result.group())
# print(result.group(1))
# print(result.span())
# group()会输出完整的匹配结果； group()输出第一个被()包围的匹配结果

# 3.通用匹配：万能匹配：.*可以匹配任意字符（除换行符),代表匹配前面的字符无限次，组合在一起就可以匹配任意字符了
# import re
#
# content = 'Hello 123 4567 World_This is a Regex Demo'
# result = re.match('^Hello.*Demo$', content)
# print(result)
# print(result.group())
# print(result.span())
# 可以用.*简化正则表达式的书写

# 4.贪婪与非贪婪
# import re
#
# content = 'Hello 1234567 World_This is a Regex Demo'
# result = re.match('^He.*(\d+).*Demo$', content)
# print(result)
# print(result.group(1))
# 贪婪匹配下，.*会尽可能多的匹配字符；.*后面是\d+,至少一个数字，并没有指定具体多少个数字，给\d+留下满足条件的数字7
# 非贪婪匹配：.*?
# import re
#
# content = 'Hello 1234567 World_This is a Regex Demo'
# result = re.match('^He.*?(\d+).*Demo$', content)
# print(result)
# print(result.group(1))
# 做匹配时，字符串尽量使用非贪婪匹配，用.*?来代替.*,以免出现匹配结果缺失的情况
# 如果匹配结果在字符串结尾，.*?就可能匹配不到任何内容
# import re
#
# content = 'http://weibo.com/comment/kEraCN'
# result1 = re.match('http.*?comment/(.*?)', content)
# result2 = re.match('http.*?comment/(.*)', content)
# print('result1', result1.group(1))
# print('result2', result2.group(1))

# 5.修饰符：控制匹配模式
# import re
#
# content = '''Hello 1234567 World_This
# is a Regex Demo
# '''
# result = re.match('^He.*?(\d+).*?Demo$', content)
# print(result.group(1)
# 没有匹配到字符串，返回结构为None，调用group方法导致AttributeError
# .匹配的是除换行符外的任意字符，遇到换行符时，.*?就不能匹配了，导致匹配失败，只需加一个修饰符re.S
import re

content = '''Hello 1234567 World_This
is a Regex Demo
'''
result = re.match('^He.*?(\d+).*?Demo$', content, re.S)
print(result.group(1))
# 常用修饰符：re.S 和 re.I


# 6.转义匹配
# 目标字符串中包含. 需要用到转义匹配
import re
content = '(百度)www.baidu.com'
result = re.match('\(百度\)www.baidu\.com', content)
print(result)
# 遇到用于匹配的特殊字符时， 加反斜杠
