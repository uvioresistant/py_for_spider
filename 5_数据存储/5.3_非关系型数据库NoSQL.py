# NoSQL，Not Only SQL 泛指非关系型数据库，NoSQL基于键值对，不需要经过SQL层的解析，数据间无耦合性，性能高
# 键值存储数据库：Redis、Voldemort、Oracle BDB
# 列存储数据库： Cassandra、HBase、Riak
# 文档型数据库： CouchDB、MongoDB
# 图形数据库： Neo4J、InfoGrid、Infinite Graph

# 爬虫数据存储，一条数据可能存在某些字段提取失败而缺失，数据可能随时调整，数据之间存在嵌套关系
# 使用关系型数据库存储，一、需要提前建表；二、存在数据嵌套关系：需要进行序列化操作才可存储；非常不方便
# 非关系型数据库，可以避免一些麻烦，更简单高效