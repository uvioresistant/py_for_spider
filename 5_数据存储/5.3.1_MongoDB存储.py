# MongoDB有C++编写，基于分布式文件存储的开源数据库系统，内容存储形式类似JSON对象，字段值可以包含其他文档、数组、文档数组


# 2.连接MongoDB
# 连接时，需要使用PyMongo库里的MongoClient，传入MongoDB的IP及端口即可，第一个参数为地址host，第二个参数为端口port（默认27017）
import pymongo
client = pymongo.MongoClient(host='localhost', port=27017)
# 第一个参数host还可以直接传入mongoDB的链接字符串，以Mongodb开头
# client = MongoClient('mongodb://localhost:27017/')


# 3.指定数据库，以test数据库指定说明
db = client.test
# 调用client的test属性即可返回test数据库，也可以这样指定：
# db = client['test']


# 4.指定集合
# MongoDB每个数据库包含许多集合（collection），类似于关系型数据库中的表；指定集合名称为students
# collection = db.students
# 或
collection = db['students']
# 便声明了一个Collection对象


# 5.插入数据：对于students集合、新建一个学生数据，以字典形式表示：
student = {
    'id': '20170101',
    'name': 'Jordan',
    'age': 20,
    'gender': 'male'
}
# 指定了学生的学号、姓名、年龄和性别，直接调用collection的insert方法即可
# result = collection.insert(student)     # 官方已经不推荐用insert方法
# print(result)
# # 官方推荐insert_one和insert_many来分别插入单条记录和多条记录
# student = {
#     'id': '20170101',
#     'name': 'Jordan',
#     'age': 20,
#     'gender': 'male'
# }
# result = collection.insert_one(student)
# print(result)
# print(result.inserted_id)       # 与insert方法不同，返回的是InsertOneResult对象，调用其inserted_id获取_id
#
#
# # 对于insert_many方法，将数据以列表形式传递
# student1 = {
#     'id': '20170101',
#     'name': 'Jordan',
#     'age': 20,
#     'gender': 'male'
# }
# student2 = {
#     'id': '20170102',
#     'name': 'Mike',
#     'age': 21,
#     'gender': 'mile'
# }
# result = collection.insert_many([student1, student2])
# print(result)
# print(result.inserted_ids)      # 返回类型是InsertManyResult，调用inserted_ids可以获取插入数据的_id列表
#

# 6.查询:用find_one：单个结果或find：返回一个生成器对象，查询
# result = collection.find_one({'name': 'Mike'})      # 查询name为Mike的数据
# print(type(result))                                 # 返回结果是字典类型
# print(result)
# 多了_id属性，就是MongoDB在插入过程中自动添加的


# 也可以根据ObjectId查询，需要使用bson库里的objectid
# from bson.objectid import ObjectId
# result = collection.find_one({'_id': ObjectId('5b5abf0d5e340b135ccd5dd2')})
# print(result)
# 查询结果不存在，返回None


# 多条数据的查询，可以使用find方法，如查找年龄为20的数据
# results = collection.find({'age': 20})
# print(result)
# for result in results:
#     print(result)
# 返回结果是Cursor类型，相当于一个生成器，需要遍历取到所有的结果，每个结果都是字典类型


# 要查询年龄大于20 的数据
# results = collection.find({'age': {'$gt': 20}})     # 查询的条件键值已经不是单纯的数字，而是一个字典
# print(result)
# for result in results:
#     print(result)

# 比较符号：
# $lt     小于      {'age': {'$lt': 20}}
# $gt     大于      {'age': {'$gt': 20}}
# $lte    小于等于  {'age': {'$lte': 20}}
# $gte    大于等于  {'age': {'$gte': 20}}
# $ne     不等于    {'age': {'$ne': 20}}
# $in     在范围内   {'age': {'$in': [20, 23]}}
# $nin    不在范围内 {'age': {'$nin': [20, 23]}}


# 可以用正则匹配
# 查询以M开头的学生数据
# results = collection.find({'name': {'$regex': '^M.*'}})     # 使用$regex来指定正则匹配，^M.*表示以M开头的正则表达式
# print(result)
# for result in results:
#     print(result)

# 功能符号
# $regex      匹配正则表达式     {'name':{'$regex': '^M.*'}}     name以M开头
# $exists     属性是否存在       {'nem': ['$exists': True]}      name属性存在
# $type       类型判断           {'age': {'$tyep': 'int'}}       age的类型为int
# $mod        数字模操作          {'age': {'$mod': [5,0]}}       年龄模5余0
# $text       文本查询            {'$text': {'$search': 'Mike'}} text类型的属性中包含Mike字符串
# $where      高级条件查询        {'$where': 'obj.fans_count == obj.follows_count'}     自身粉丝数等于关注数

# 7.计数：统计结果多少条数据，调用count方法
# 统计所有数据条数
# count = collection.find().count()
# print(count)
# # 或统计符合某个条件的数据
# count = collection.find({'age': 20}).count()
# 结果是数值，即符合条件的数据条数


# 8.排序：调用sort方法，在其中传入排序的字段及升降序标志
# results = collection.find().sort('name', pymongo.ASCENDING)
# print([result['name'] for result in results])


# 9.偏移:用skip方法偏移几个位置
# 偏移2，就忽略前两个元素，得到第三个及以后元素
# results = collection.find().sort('name', pymongo.ASCENDING).skip(2)
# print([result['name'] for result in results])


# limit方法指定要取的结果个数
# results = collection.find().sort('name', pymongo.ASCENDING).limit(2)
# print([result['name'] for result in results])
# 如果不使用limit方法，会返回三个结果，限制后，会截取两个结果返回
# 数据库大时，不要使用的的偏移量来查询，很可能导致内存溢出，可用如下查询
# from bson.objectid import ObjectId
# collection.find({'_id':{'$gt': ObjectId('5b5aca235e340b06b0a685fb')}})


# 10.更新：update方法，指定更新的条件和更新后的数据
condition = {'name': 'Kevin'}
student = collection.find_one(condition)
student['age'] = 25
result = collection.update(condition, student)
print(result)
# 返回结果是字典形式，ok代表执行成功，nModified代表影响的数据条数


# 使用$set操作符对数据进行更新
# result = collection.update(condition, {'$set': student})    # 可以只更新student字典内存在的字段，原先还有其他字段，不会更新
# print(result)
# 如果不用$set，会把之前的数据全部用student字典替换；原本存在其他字段，会被删除
# update也是不推荐的方法，分为updata_one和update_many，第二额参数需要使用$类型操作符作为字典的键名
# condition = {'name': 'Kevin'}
# student = collection.find_one(condition)
# student['age'] = 26
# result = collection.update_one(condition,{'$set': student}) # 调用了update_one方法，第二个参数不能再直接传入修改后的字典，
# print(result)
# print(result.matched_count, result.modified_count)   # 分别调用matched_count和modified_count属性，获得匹配、影响的数据条数
#
#
# # 11.删除：用remove方法指定删除条件，符合条件的所有数据均被删除
result = collection.remove({'name', 'Kevin'})
print(result)

# 12.其他操作
# PyMongo还提供一些组合方法：find_one_delete查找后删除、find_one_and_replace查找后替换、find_one_and_update查找后更新