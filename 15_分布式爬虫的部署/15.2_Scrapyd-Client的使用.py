# 现成的工具来完成部署过程，叫Scrapyd-Client

# 1.Scrapyd-Client正确安装

# 2.Scrapyd-Client的功能：为方便Scrapy项目的部署，提供两个功能：
# 将项目打包成Egg文件
# 将打包生成的Egg文件通过addversion.json接口部署到Scrapyd上
# Scrapyd-Client吧部署全部实现了，不需再去关心Egg文件是怎样生成的，不需再去读Egg文件并请求接口上传了，只需执行一个命令即可部署

# 3.Scrapyd-Client部署：首先需要修改项目的配置文件。如Scrapy微博爬虫项目，在项目的第一层会有一个scrapy.cfg文件：
[settings]
default = weibo.settings

[deploy]
#url = http://localhost:6800/
project = weibo
# 需配置deploy部分，如将项目部署到120.27.32.25的Scrapyd上，修改内容：
[deploy]
url = http://120.27.34.25:6800/
project = weibo
# 再在scrapy.cfg文件所在路径执行命令：
scrapyd-deploy
# 运行结果：表示部署成功
Packing version 1501682277
Deploying to project "weibo" in http://120.27.34.25:6800/addversion.json
Server response (200):
{"status": "ok", "spiders": 1, "node_name": "datacrawl-vm", "project": "weibo", "version": "1501682277"}
# 项目版本默认为当前时间戳，也可指定项目版本，通过version参数传递即可，如
scrapyd-deploy --version 201707131455

# 如果有多态主机，可以配置各台主机的别名，修改配置文件：
[deploy:vm1]
url = http://120.27.34.24:6800/
project = weibo

[deploy:vm2]
url = http://139.217.26.30:6800/
project = weibo
# 在此统一配置多态主机，一台主机对应一组配置，在deploy后加上主机别名即可。如果想将项目部署到IP为139.217.26.30的vm2主机，执行：
scrapyd-deploy vm2
# 只需在scrapy.cfg文件中配置好各台主机的Scrapyd地址，然后调用scrapyd-deploy+主机名称即可实现部署

# 如果Scrapyd设置了访问限制，可以在配置文件中加入用户名和密码的配置，同时修改端口成Nginx代理端口
[deploy:vm1]
url = http://120.27.34.24:6801/
project = weibo
username = admin
password = admin
# 通过加入username和password字段，我们就可以在部署时自动进行Auth验证，然后成功实现部署
