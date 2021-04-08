# 在将Scrapy项目放到各台主机运行时，可能采用的是文件上传或者Git同步的方式，这样需要各台主机都进行操作，如果有100台，工作量大
# 分布式爬虫部署方面可采取一些措施，以方便实现批量部署和管理

# 1.Scrapyd分布式部署：分布式爬虫完成并成功运行，但代码部署环节非常繁琐
# 如果采用上传文件方式部署代码，首先将代码压缩，然后采用SFTP或FTP方式将文件上传到服务器，之后再连接服务器将文件解压，每个都配置
# 如果采用Git同步方式部署代码，可以先把代码Push到某个Git仓库，然后再远程连接各台主机执行Pull操作，同步代码，每个需做一次
# 且代码突然有更新，必须更新每个服务器，且万一哪台主机版本没控制好，可能影响整体的分布式爬取状况
# 需要一个跟方便的工具了部署Scrapy项目，可以省去一遍遍逐个登录服务器部署的操作

# 1. 了解Scrapyd：一个运行Scrapy爬虫的服务程序，提供一系列HTTP接口来帮助部署、启动、停止、删除爬虫程序。
# Scrapyd支持版本管理，同时还可以管理多个爬虫任务，利用它可以非常方便地完成Scrapy爬虫项目的部署任务调度

# 2.准备：本机或服务器已经安装好Scrapyd

# 3.访问Scrapyd：访问服务器的6800端口，如服务器地址120.27.34.25，浏览器中打开：HTTP://120.27.34.25:6800,可看到Scrapyd的首页

# 4.Scrapyd的功能：提供一些列HTTP接口来实现各种操作：

# daemonstatus.json:此接口负责查看Scrapyd当前的服务和任务状态，可以用curl命令来请求这个接口，命令：
curl http://139.217.25.30:6800/daemonstatus.json
# 得到结果：
{"status": "ok", "finished": 90, "running": 9, "node_name": "datacrawl-vm", "pending": 0}
# 返回结果是JSON字符串，status是当前状态，finished代表当前已经完成的Scrapy任务，running代表正在运行的Scrapy任务，
# pending代表等待被调度的Scrapyd任务，node_name就是主机的名称

# addversion.json：此接口用来部署Scrapy项目。首先将项目打包成Egg文件，然后传入项目名称和部署版本，实现项目部署：
curl http://120.27.34.25:6800/addversion.json -F project=weibo -F version=first -F egg=@weibo.egg
# -F代表添加一个参数，同时还需将项目打包成Egg文件放到本地
# 发出请求后，得到结果：
{"status": "ok", "spiders": 3}
# 表明部署成功，且Spider数量为3

# schedule.json:此接口负责调度已部署好的Scrapy项目运行
crul http://120.27.34.25:6800/schedule.json -d project=weibo -d spider=weibocn
# 需传入两个参数，project即Scrapy项目名称，spider即Spider名称
# 返回结果：
{"status": "ok", "jobid": "6487ec79947edab326d6db28a2d86511e827444"}
# status代表Scrapy项目启动情况，jobid代表当前正在运行的爬取任务代号

# cancel.json: 用来取消某个爬取任务，如果这个任务是pending静态，那么将会被移除；如果是running状态，将会被终止
# 用命令来取消任务的运行：
curl http://129.27.34.25:6800/cancel.json -d project=weibo -d job=6487ec79947edab326d6db28a2d86511e827444
# 需要传入两个参数，project即Scrapy项目名称，job即爬取任务代号
# 返回结果：
{"status": "ok", "prevstate": "running"}
# status代表请求执行情况，prevstate代表之前的运行状态

# listprojects.json: 接口用来列出部署到Scrapyd服务器上的所有项目描述：
curl http://129.27.34.25:6800/listprojects.json
# 返回结果：
{"status": "ok", "projects": ["weibo", "zhihu"]}
# status代表请求执情况，projects是项目名称列表

# listverions.json：此接口用来获取摸个项目的所有版本好，版本号是按序排列的，最后一个条目是最新的版本号：
curl http://120.27.34.25:6800/listversion.json?project=weibo
# 需要一个参数project，即项目的名称
# 返回结果：
{"status": "ok", "versions": ["v1", "v2"]}
# status代表请求执行情况，versions是版本号列表

# listspiders.json: 此接口用来获取摸个项目最新版本的所有Spider名称
curl http://120.27.34.25:6800/listspiders.json?project=weibo
# 这里需要一个参数project，即项目名称
# 返回结果：
{"status": "ok", "spiders": ["weibocn"]}
# status代表请求执行情况，spiders是Spiders名称列表

# listjobs.json：此接口用来获取摸个项目当前运行的所有任务详情
curl http://120.27.34.25:6800/listjobs.json?project=weibo
# 这里需要一个参数project，即项目名称
# 返回结果：
{"status": "ok",
 "pending": [{"id": "78391ccofcaf11e1b0080800272a6d06", "spider": "weibocn"}],
 "runnig": [{"id": "422e608f9f28cef127b3d5ef93fe9399", "spider": "weibocn", "start_time": "2017-07-12 10:14:03.594664"}]
 "finished": [{"id": "2f16646cfcaf11e1b0090800272a6d06", "spider": "weibocn", "start_time": "2017-07-12 "
    "10:14:03.594664", "end_time": "2017-07-12 10:24:03.594664"}]}
# status代表请求执行情况，pending代表当前正在等待的任务，running代表当前正在运行的任务，finished代表已经完成的任务

# delversion.json: 此接口用来删除项目的某个版本
curl http://120.27.34.25:6800/delversion.json -d  project=weibo -d version=v1
# 这里需要一个参数project，即项目名称,还需一个参数version，即项目的版本
# 返回结果：
{"status": "ok"}
# status代表请求执行情况，删除成功

# delproject.json：用来删除某个项目
curl http://120.27.34.25:6800/delproject.json -d project=weibo

# 这里需要一个参数project，即项目名称,
# 返回结果：
{"status": "ok"}
# status代表请求执行情况，删除成功
# 以上接口是Scrapyd所有的接口，可以直接请求HTTP接口，即可控制项目的部署、启动、运行等操作

# 5.ScrapyAPI的使用：Scrapyd API库对这些接口做了一层封装，核心原理和HTTP接口请求方式并无二致，只不过Python封装后的库更便捷
# 建立Scrapy API:
from scrapyd_api import ScrapydAPI
scrapyd = ScrapydAPI('http://120.27.34.25:6800')
# 调用它的方法来实现对应接口的操作，如部署的操作：
egg = open('weibo.egg', 'rb')
scrapyd.add_version('weibo', 'v1', egg)
# 这样就可以将项目打包为egg文件，然后把本地打包的Egg项目部署到远程Scrapyd
# Scrapyd API还实现了所有Scrapyd提供的API接口，名称都是相同的，参数也是相同的
# 调用list_projects方法即可列出Scrapyd中所有已部署的项目：
scrapyd.list_projects()
['weibo', 'zhihu']
# 详细操作可参考官方文档：http://python-scrapyd-api.readthedocs.io/
