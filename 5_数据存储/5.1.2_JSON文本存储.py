# JSON，就是JavaScript对象标记，通过对象和数组的组合来表示数据，构造简洁但结构化程度非常高，是轻量级的数据交换格式
# 1.对象和数组
# JS中一切都是对象，任何支持类型都可以通过JSON表示，如字符串、数字、对象、数组等，但对象和数组是比较特殊且常用的两种类型
# 对象：在JS中是使用{}包裹的内容，数据结构为{key1: value1,key: value2,...}的键值对结构；
# 面向对象的语言中，key为对象属性，value为对应的值。键名可以使用整数和字符串表示。值的类型可以是任意类型

# 数组：在JS中是[]包裹的内容，数据结构为["java", "javasccript", "vb", ...]的索引结构
# 在JS中，数组是比较特殊的数据类型，可以向对象那样使用键值对，但还是索引用得多。值的类型可以是任意类型
# JSON对象可以写为如下形式：
[{
    "name": "Bob",
    "gender": "male",
    "birthday": "1992-10-18"
},{
    "name": "Selina",
    "gender": "female",
    "birthday": "1995-10-18"
}]
# 中括号包围的相当于列表类型，列表中的每个元素可以是任意类型
# JSON可以有以上两种形式自由组合而成，可以无限次嵌套，结构清晰，是数据交换的极佳方式


# 2.读取JSON
# Python提供了JSON库，实现JSON文件的读写操作；
# 可以调用JSON库的loads方法将JSON文本字符串转为JSON对象
# 可以嗲用JSON库的dumps方法将JSON对象转为文本字符串
# import json
#
# str ='''
# [{
#     "name": "Bob",
#     "gender": "male",
#     "birthday": "1992-10-18"
# }, {
#     "name": "Selina",
#     "gender": "female",
#     "birthdat": "1995-10-28"
# }]
# '''
# print(type(str))
# data = json.loads(str)          # 使用loads方法将字符串转为JSON对象，最外层是中括号，最终类型是类表形式
# print(data)
# print(type(data))


# 利用索引来获取对应的内容
# 获取第一个元素里的name属性：
# import json
#
# str = '''
# [{
#     "name": "Bob",
#     "gender": "male",
#     "birthday": "1992-10-18"
# }, {
#     "name": "Selina",
#     "gender": "female",
#     "birthdat": "1995-10-28"
# }]
# '''
# # print(type(str))
# data = json.loads(str)  # 使用loads方法将字符串转为JSON对象，最外层是中括号，最终类型是列表形式
# data[0]['name']         # 通过中括号加0索引，得到第一个字典元素，调用其键名即可得到相应键值
# data[0].get('name')     # 获取键值有两种方式：一种是中括号+键名；一种是get方法传入键名，推荐get方法，返回None
# print(data[0]['name'])
# print(type(data[0].get('name')))


# get方法还可以传入第二个参数(默认值)
# import json
#
# str = '''
# [{
#     "name": "Bob",
#     "gender": "male",
#     "birthday": "1992-10-18"
# }, {
#     "name": "Selina",
#     "gender": "female",
#     "birthdat": "1995-10-28"
# }]
# '''
# # print(type(str))
# data = json.loads(str)
# data[0].get('age')              # 尝试获取年龄age，原字典中该键名不存在，默认返回None
# data[0].get('age', 25)          # 若传入第二个参数(默认值),不存在的情况下返回该默认值
# print(data[0].get('age'))
# print(data[0].get('age', 25))


# JSON的数据需要用双引号包围，不能用单引号
# import json
#
# str = '''
# [{
#     'name': 'Bob',
#     'gender': 'male',
#     'birthday': '1992-10-28'
# }]
# '''
# data = json.loads(str)
# 会出现JSON解析错误。千万注意JSON字符串的表示需要用双引号，否则loads方法解析失败


# 如果从JSON文本中读取内容
# 如data.json文本文件，可以先将文本文件内容读出，再利用loads方法转化
# import json
#
# with open('data.json', 'r') as file:
#     str = file.read()
#     data = json.loads(str)
#     print(data)


# 3.输出JSON
# 调用dumps方法将JSON对象转化为字符串
import json

data = [{
    "name": "Bob",
    "gender": "male",
    "birthday": "1992-10-18"
}]
with open('data.json', 'w')as file:     # 将JSON对象转化为字符串，再调用文件的write方法写入文本
    file.write(json.dumps(data))


# 想保存JSON格式，可以再加一个参数indent，代表缩进字符个数
with open('data.json', 'w')as file:
    file.write(json.dumps(data, indent=2))      # 得到的内容会自动带缩进，格式更加清晰


# 若JSON中包含中文字符，中文字符会变成Unicode字符
import json

data = [{
    'name': '王伟',
    'gender': '男',
    'birthday': '1992-10-18'
}]
with open('data.json', 'w') as file:
    file.write(json.dumps(data, indent=2))
    