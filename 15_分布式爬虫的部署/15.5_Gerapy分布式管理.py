# 可以通过Scrapyd-Client将Scrapy项目部署到Scrapyd上，且可以通过Scrapyd API来控制Scrapy的运行
# 分析可以优化的问题：
# a.使用Scrapyd-Client部署时，需要再配置文件中配置好各台主机的地址，然后利用命令行执行部署过程。
# 如果省去各台主机的地址配置，将命令行对接图形界面，只需点击按钮即可实现批量部署，更方便
# b.使用Scrapyd API可以控制Scrapy任务的启动、终止等工作，但很多操作还是需要代码来实现，同时获取爬取日志比较繁琐。
# 如果有一个图形界面，只需点击按钮即可启动和终止爬虫任务，同时还可以实时查看爬取日志报告，将节省时间和精力

# 终极目标是：    通过Gerapy来实现
# A.更方便地控制爬虫运行；
# B.更直观地查看爬虫状态；
# C.更实时地查看爬取结果；
# D.更简单地实现项目部署；
# E.更统一地实现主机管理；

# Gerapy是一个基于Scrapyd、Scrapyd API、Django、Vue.js搭建的分布式爬虫管理框架

# 1.准备：安装好了Gerapy

# 2.使用说明：利用Gerapy命令新建一个项目：
gerapy init
# 当前目录下生成一个gerapy文件夹。进入gerapy文件夹，发现一个空的projects文件夹，先对数据库进行初始化：
gerapy migrate
# 会生成一个SQLite数据库，数据库保存各个主机配置信息、部署版本等
# 启动Gerapy服务，命令：
gerapy runserver
# 即可在默认8000端口上开启Gerapy服务。用浏览器打开：http://localhost:8000，可进入Gerapy的管理页面，提供了主机管理和项目管理
# 主机管理中添加各台主机的Scrapyd运行地址和端口，并加以名称标记。之后各台主机便会出现在主机列表中。
# Gerapy会监控各台主机的运行状况并加以不同的状态标识
# gerapy目录下有一个空的projects文件夹，就是存放Scrapy目录的文件夹，如果想要部署某个Scrapy项目，只需将该项目文件放入projects
# 放入sinaapi、zhihusite两个Scrapy项目，重新回到Gerapy管理界面，点击项目管理，可看到当前项目列表
# Gerapy提供了项目在线编辑功能。点击编辑，即可可视化的对项目进行编辑，如果项目没有问题，可以点击部署精心打包和部署。
# 部署前需要打包项目，打包时可以指定版本描述
# 打包完成后，直接点击部署按钮即可将打包好的Scrapy项目部署到对应的云主机上，同时也可以批量部署
# 部署完毕后就可以回到主机管理页面进行任务调度。点击调度即可进入任务管理页面，可查看当前主机所有任务的运行状态
# 通过点击新任务、停止等按钮来实现任务的启动和停止操作，同时也可以通过开展任务条目查看日志详情，即可实时查看各个任务运行状态
# 通过Gerapy，可以更加方便地管理、部署和监控Scrapy项目，尤其是对分布式爬虫来说，使用Gerapy会更加方便
# Gerapy的GitHub地址：https://github.com/Gerapy