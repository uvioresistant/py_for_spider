# CSV：Comma-Separated Values, 逗号分隔值或字符分隔值，其文件以纯文本形式存储表格数据。
# CSV是一个字符序列，由任意数目的记录组成，记录间以某种换行符分隔。
# 每条记录由字段组成，字段间的分隔符是其他字符或字符串，常见的是逗号或制表符
# 所有记录都有完全相同的字段序列，即结构化表的纯文本形式。
# 比Excel文件更加简洁，XLS文本是电子表格，包含了文本、数值、公式和格式；CSV中不包含这些，就是特定字符分隔的纯文本，结构简单

# 1.写入
# import csv
#
# with open('data.csv', 'w') as csvfile:              # 打开data.csv文件，指定打开模式为w（写入），获得文件句柄
#     writer = csv.writer(csvfile)                    # 调用csv的writer方法初始化写入对象，传入句柄
#     writer.writerow(['id', 'name', 'age'])          # 调用writerow方法传入每行的数据
#     writer.writerow(['10001', 'Mike', 20])
#     writer.writerow(['10002', 'Bob', 22])
#     writer.writerow(['10003', 'Jordan', 21])
# 生成一个data.csv的文件，写入文本默认以逗号分隔


# 修改列与列之间的分隔符，传入delimiter参数
# import csv
#
# with open('data.csv', 'w') as csvfile:
#     writer = csv.writer(csvfile, delimiter=' ')
#     writer.writerow(['id', 'name', 'age'])
#     writer.writerow(['10001', 'Mike', 20])
#     writer.writerow(['10002', 'Bob', 22])
#     writer.writerow(['10003', 'Jordan', 21])


# 调用writerows方法同时写入多行，此时参数需要为二维列表
import csv

with open('data.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'name', 'age'])
    writer.writerow([['10001', 'Mike', 20], ['10002', 'Bob', 22], ['10003', 'Jordan', 21]])
# 一般情况下，爬虫爬取的是结构化数据，一般用字典来表示
import csv

with open('data.csv', 'w') as csvfile:
    fieldnames = ['id', 'name', 'age']                                  # 定义3个字段，用filenams表示
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)             # 传给DictWriter来初始化一个字典写入对象
    writer.writeheader()                                                # 调用writeheader方法写入头信息
    writer.writerow({'id': '10001', 'name': 'Mike', 'age': 20})         # 调用writerow方法传入相应字典
    writer.writerow({'id': '10002', 'name': 'Bob', 'age': 22})
    writer.writerow({'id': '10003', 'name': 'Jordan', 'age': 21})


# 追加写入，修改文件的打开模式，将open函数的第二个参数改成a
import csv

with open('data.csv', 'a') as csvfile:
    fieldnames = ['id', 'name', 'age']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writerow({'id': '10004', 'name': 'Durant', 'age': 22})


# 中文内容，给open参数指定编码格式
import csv

with open('data.csv', 'a', encoding='utf-8') as csvfile:
    fieldnames = ['id', 'name', 'age']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writerow({'id': '10005', 'name': '王伟', 'age': 22})


# 2.读取：使用csv库来读取CSV文件
import csv

with open('data.csv', 'r', encoding='utf-8') as csvfile:        # CSV文件中包含中文，需指定文件编码
    reader = csv.reader(csvfile)                                # 构造Reader对象
    for row in reader:                                          # 遍历输出每行的内容，每一行都是一个列表形式
        print(row)