# 使用Scrapyd-Client成功将Scrapy项目部署到Scrapyd运行，前提是需要提前在服务器上安装好Scrapyd并运行Scrapyd服务，过程麻烦。
# 如果同时将一个Scrapy项目部署到100台服务器上，需要手动配置每台服务器的Python环境，更改Scrapyd配置
# 如果这些服务器的Python环境是不同版本，同时还运行其他的项目，版本冲突又会造成不必要的麻烦
# 需要解决一个通电，就是Python环境配置问题和版本冲突解决问题。
# 如果将Scrapyd直接打包成一个Docker镜像，在服务器上只需要执行Docker命令就可启动Scrapyd服务，就不用关心Python环境+版本冲突问题
# 将Scrapyd打包制作成一个Docker镜像

# 1.准备：安装好了Docker

# 2.对接Docker：新建项目scrapyd.conf,即Scrapyd的配置文件
[scrapyd]
eggs_dir        = eggs
logs_dir        = logs
items_dir       =
jobs_to_keep    = 5
dbs_dir         = dbs
max_proc        = 0
max_proc_per_cpu    = 10    # 原本是4，更改为10，也可执行设置
finished_to_keep    = 100
poll_interval       = 5.0
bind_address        = 0.0.0.0   # 原本是127.0.0.1，不能公开访问，修改为0.0.0.0即可解除此限制
http_port           = 6800
debug               = off
runner              = scrapyd.runner
application         = scrapyd.app.application
launcher            = scrapyd.launcher.Launcher
webroot             = scrapyd.website.Root

[services]
schedule.json       = scrapyd.webservice.Schedule
cancel.json         = scrapyd.webservice.Cancel
addversion.json     = scrapyd.webservice.Addversion
listprojects.json   = scrapyd.webservice.ListProjects
listversions.json   = scrapyd.webservice.ListVersions
listspiders.json    = scrapyd.webservice.ListSpiders
delproject.json     = scrapyd.webservice.DeleteProject
delversion.json     = scrapyd.webservice.DeleteVersion
listjobs.json       = scrapyd.webservice.ListJobs
daemonstatus.json   = scrapyd.webservice.DaemonStatus
# 实际上是修改自官方文档的配置文件:https://scrapyd.readthedocs.io/en/stable/config.html#example-configuration-file

# 新建一个requirements.txt，将一些Scrapy项目常用的库都列进去
requests
selenium
aiohttp
beautifulsoup4
pyquery
pymysql
redis
pymongo
flask
django
scrapy
scrapyd
scrapyd-client
scrapy-redis
Scrapy-splash

# 新建一个Dockerfile：
FROM python:3.6
ADD . /code
WORKDIR /code
COPY ./scrapyd.conf /etc/scrapyd
EXPOSE 6800
RUN pip3 install -r requirements.txt
CMD scrapyd

# 基本工作完成，运行命令：
docker build -t scrapyd:latest
# 成功后测试：
docker run -d -p 6800:6800 scrapyd
# 打开http://localhost:6800，可观察到Scrapyd服务，则Scrapyd Docker镜像构建完成并成功运行
# 可将此镜像上传到Docker Hub，用户名为germey，新建一个名为scrapyd的项目，首先为已经向打一个标签来标识一下
docker tag scrapyd:latest germey/scrapyd:latest # 自行替换成项目名称
# 然后Push:
docker push germey/scrapyd:latest
# 在其他主机运行此命令后，即可启动Scrapyd服务
docker run -d -p 6800:6800 germey/scrapyd   # Scrapyd成功在其他服务器上运行