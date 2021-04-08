# 关系型数据库是基于关系模型的数据库，而关系模型是通过二维表来保存的，存储方式就是行列组成的表，每列是一个字段，每行是记录
# 表可以看作某个实体的集合，实体之间存在联系，需要表与表之间的关联关系来体现。
# 多个表组成一个个数据库，就是关系型数据库

# 连接数据库
# 尝试连接一下数据库，当前MySQL运行在本地，用户名root，密码123456，运行端口3306
# 利用PyMySQL先连接MySQL，创建一个新的数据库，名为spiders
import pymysql

db = pymysql.connect(host='localhost', user='root', password='123', port=3306)  # 通过PyMySQL的connect方法声明MySQL连接db
# 需要传入MySQL运行的host(IP).MySQL在本地运行，传入的是localhost。如果在远程运行，传入公网IP地址，port为端口(默认3306)
cursor = db.cursor()        # 调用cursor方法获得MySQL的操作游标，利用游标执行SQL语句
cursor.execute('SELECT VERSION()')      # 直接从execute方法执行
# data = cursor.fetchone()                # 调用fetchone方法获得第一条数据
# print('Database version:', data)
cursor.execute("CREATE DATABASE spiders DEFAULT CHARACTER SET utf8")    #  SQL执行创建数据库的操作，名为spiders，默认UTF-8
db.close()


# 3.创建表
# 创建数据库的操作只需执行一次，也可以手动创建数据库，以后操作都在spiders数据库上执行
# 创建数据库后，连接时需要额外指定一个参数db
# 新创建一个数据表students，执行创建表的SQL语句
# id    学号      类型
# name  姓名      varchar
# age   年龄      int

import pymysql

db = pymysql.connect(host='localhost', user='root', password='123', port=3306, db='spiders')
cursor = db.cursor()
sql = 'CREATE TABLE IF NOT EXISTS students (id VARCHAR(255) NOT NULL, name' \
      ' VARCHAR(255) NOT NULL, age INT NOT NULL, PRIMARY KEY (id))'
# cursor.execute(sql)
# db.close()

# 4.插入数据
# 爬取了一个学生信息，学号为20120001，名字为Bob，年龄为20岁
# import pymysql
#
# id = '20120001'
# user = 'Bob'
# age = 20
# db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='spiders')
# cursor = db.cursor()
# sql = 'INSERT INTO students(id, name, age) values(%s, %s, %s)'    # 首先构造了一个SQL语句，Value值没有用字符串拼接方式构造-
# # 选择直接用格式化符%s来实现，有几个Value写几个%s，只需在execute方法第一个参数传入SQL语句，Value值用统一的元组传过来
# try:
#       cursor.execute(sql, (id, user, age))
#       db.commit()       # 需要执行db对象的commit方法可实现数据插入，此方法为提交到数据库执行的方法，数据插入、更新、删除都需要
# except:
#       db.rollback()     # 加了一层异常处理，执行失败，调用rollback执行数据回滚，相当于什么都没有发生过
# db.close()
# 事务机制(事物的原子性)：确保数据的一致性，要么发生了，要么没有发生。
# 事务的4个属性:原子性(atomicity)、一致性(consistency)、隔离性(isolation)和持久性(durability)
# 插入、更新和删除操作都是对数据库进行更改的操作，更改操作都必须为一个事务
# try:
#       cursor.execute(sql)
#       db.commit()             # commit方法可以保证数据的一致性
# except:
#       db.rollback()           # rollback方法可以保证数据的一致性
# 上面插入的操作是通过构造SQL语句实现的，极其不方便的地方是突然增加了性别字段gender，SQL语句需要改成：
# INSERT INTO students(id, name, age, gender) values(%s, %s, %s, %s)
# 相应元组参数需改成
# (id, name, age, gender)
# 需要做成一个通用方法，只需要传入一个动态变化的字典就可以了
# {
#       'id': '20120001',
#       'name': 'Bob',
#       'age': 20
# }
# SQL 语句会根据字典动态构造，元组也动态构造，才能实现通用的插入方法
# data = {                            # 传入的数据是字典，定义为data变量，需要构造插入id、name和age
#       'id': '20120001',
#       'name': 'Bob',
#       'age': 20
# }
# table = 'students'                  # 表名定义成变量table
# keys = ', '.join(data.keys())       # 将data键名拿过来，用逗号分隔；结果就是id, name, age
# values = ', '.join(['%s'] * len(data))    # 需要构造多个%s当作占位符，有几个字段构造几个
# # sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)   # 利用format方法
# sql = 'INSERT INTO students(id, name, age) VALUES (%s, %s, %s)'.format(table=table, keys=keys, values=values)   # 利用format方法
# # 将表名、字段名、占位符构造出来，最终SQL语句就被动态构造成了：
# # INSERT INTO students(id, name, age) VALUES (%s, %s, %s)
# try:
#       if cursor.execute(sql, tuple(data.values())):   # execute方法的第一个参数传入sql变量；第二个参数传入data的键值构造元组
#             print('Successful')
#             db.commit()
# except:
#       print('Failed')
#       db.rollback()
# db.close()
# # 实现了传入一个字典来插入数据的方法，不需要再去修改SQL语句和插入操作
#
#
# # 5.更新数据
# # 数据更新操作实际上也是执行SQL语句，最简单的方式就是构造一个SQL语句
sql = 'UPDATE students SET age = %s WHERE name = %s'
try:
      cursor.execute(sql, (25, 'Bob'))                      # 用占位符方式构造SQL，执行execute方法，传入元组形式的参数
      db.commit()                                           # 执行commit方法
except:
      db.rollback()
db.close()


# 更新数据而不是重复保存一次；如果数据存在，更新数据，不存在，插入数据
data = {
      'id': '20120001',
      'name': 'Bob',
      'age': 21
}

table = 'students'
keys = ', '.join(data.keys())
values = ', '.join(['%s'] * len(data))

sql = 'INSERT INTO {table}({keys})VALUES({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys,
      values=values)          # 构造的SQL语句是插入语句，在后面加了ON DUPLICATE KEY UPDATE:如果主键已经存在，执行更新操作
update = ', '.join([" {key} = %s".format(key=key) for key in data])
sql += update
try:
      if cursor.execute(sql, tuple(data.values())*2):
            print('Successful')
            db.commit()
except:
      print('Failed')
      db.rollback()
db.close()
# # 如传入数据id仍然为20120001，但是年龄由20变成21，这条数据不会被插入，而是直接更新id为20120001的数据
# # INSERT INTO students(id, name, age) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE id = %s, name = %s, age = %s
# # 变为6个%s,在后面的execute方法的第二个参数元组就需要乘以2变为原来的两倍。
#
#
# # 6.删除数据：直接用DELETE语句，需要指定要删除的目标表名和删除条件，且仍然需要使用db的commit方法
# table = 'students'
# condition = 'age > 20'
#
# sql = 'DELETE FROM {table} WHERE {condition}'.format(table=table, condition=condition)
# try:
#       cursor.execute(sql)
#       db.commit()
# except:
#       db.rollback()
#
# db.close()
# # 直接将条件当做字符串来传递，实现删除操作。
#
#
# # 7.查询数据：SELECT语句
# sql = 'SELECT * FROM students WHERE age >= 20'        # 将年龄20岁及以上的学生查询出来，
#
# try:
#       cursor.execute(sql)                             # 将其传给execute方法，不再需要db的commit方法
#       print('Count:', cursor.rowcount)                # 调用cursor的rowcount属性获取查询结果的条数
#       one = cursor.fetchone()                         # 调用fetchone方法，可以获取结果的第一条数据，
#       print('One:', one)                              # 返回结果是元组形式，元组顺序跟字段一一对应
#       results = cursor.fetchall()                     # 调用fetchall方法，可以得到结果的所有数据
#       print('Results:', results)
#       print('Results Type:', type(results))           # 结果和类型是二重元组，
#       for row in results:                             # 每个元素是一条记录，将其遍历输出
#             print(row)
# except:
#       print('Error')
# # fetchall方法内部实现有一个偏移指针用来指向查询结果，最初调用了一次fetchone方法，结果偏移指针指向下一条数据，
# # 返回的是偏移指针指向的数据一直到结束的所有数据，故获取的结果只剩下3个
#
#
# # 用while循环加fetchone方法获取所有数据，而不是用fetchall全部获取，fetchall将结果以元组形式全部返回，推荐逐条取数据
# sql = 'SELECT * FROM students WHERE age >=20'
# try:
#       cursor.execute(sql)
#       print('Count:', cursor.rowcount)
#       row = cursor.fetchone()
#       while row:
#             print('Row:', row)
#             row = cursor.fetchone()
# except:
#       print('Error')
# # 每循环一次，指正偏移一条数据，简单高效