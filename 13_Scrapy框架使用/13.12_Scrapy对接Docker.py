# 环境配置问题可能一直让我们头疼：包括
# a.本地写好了一个Scrapy爬虫项目，想要把它放到服务器上运行，但服务器上没有安装Python环境
# b.其他人给了一个Scrapy爬虫项目，项目使用包的版本和本地环境版本不一致，项目无法直接运行
# c.需要同时管理不同版本的Scrapy项目，如早期的项目依赖于Scrapy0.25,现在的项目依赖于Scrapy1.4.0
# 在这些情况下，我们需要解决的就是环境的安装配置、环境的版本冲突等问题
# 对Python来说，VirtualEnv的确可以解决版本冲突的问题，但VirtualEnv不太方便做项目部署，还是需要安装Python环境
# 用Docker来解决这些问题，Docker可以提供操作系统级别的虚拟环境，一个Docker镜像一般都包含一个完整的操作系统，这些系统内
# 也有已经配置好的开发环境，如Python3.6等
# 可以直接使用此Docker的Python3镜像运行一个容器，将项目直接放到容器里运行，就不用再额外配置Python3环境。解决了环境配置问题
# 也可进一步将Scrapy项目制作成一个新的Docker镜像，镜像里只包含适用本项目的Python环境。
# 如果要部署到其他平台，只需下载该镜像并运行就好，因为Docker运行时采用虚拟环境，和宿主机是完全隔离的，也不需担心环境冲突问题
# 如果能够把Scrapy项目做成一个Docker镜像，只要其他主机安装了Docker，将镜像下载并运行即可，不必担心环境配置或版本冲突问题

# 1.目标：将Scrapy入门项目打包成一个Docker镜像，项目爬取网址：http://quotes.toscrape.com/
# 入门项目已经实现了Scrapy对此站点的爬取过程，项目代码：https://github.com/Python3WebSpider/ScrapyTutorial

# 2.准备：安装好Docker和MongoDB并可以正常运行

# 3.创建Dockerfile：
# 首先在项目的根目录下新建一个requirements.txt文件，将整个项目依赖的Python环境报都列出来：
# scrapy
# pymongo
# 如果库需要特定的版本，还可以指定版本好：
# scrapy>=1.4.0
# pymongo>=3.4.0
# 在项目根目录下新建一个Dockerfile文件，文件不加任何后缀名，修改为：
FROM python：3.6 # 代表使用的Docker基础镜像，直接使用python:3.6镜像，在此基础上上运行Scrapy项目
ENV PATH /usr/local/bin:$PATH   # ENV是环境变量设置，将/usr/local/bin:$PAHT赋值给PATH，即增加这个环境变量
ADD ./code  # ADD是讲本地的代码放置到虚拟容器中。有两个参数：一：. 代表本地当前路径；
            # 二:/code，代表虚拟容器中的路径，将本地项目所有内容放到虚拟容器的/code目录下，以便于在虚拟容器中运行代码
WORKDIR /code   # 指定工作目录，将刚才添加的代码路径设成工作路径，此路径下的目录结构和当前目录结构是相同的
RUN pip3 install -r requirements.txt    # 执行某些命令来做一些环境准备工作，Docker虚拟容器只有PY3环境，没有需要的库
    # 需运行此命令来在虚拟容器中安装相应的Py库如Scrapy，这样就可以在虚拟容器中执行Scrapy命令了
CMD scrapy crawl quotes # 容器启动命令，在容器运行时，此命令会被执行，直接用scrapy crawl quotes来启动爬虫

# 4.修改MongoDB连接：修改MongoDB连接信息。如果继续用localhost是无法找到MongoDB的，因为在Docker虚拟容器里localhost实际
#   指向容器本身的运行IP，而容器内部并没有安装MongoDB，所以爬虫无法连接MongoDB。
# MongoDB地址可以有两种选择：
# 如果只想在本机测试：可以将地址修改为宿主机的IP，就是容器外部的本机ID，一般是一个局域网IP，使用ifconfig查看
# 如果部署到远程主机运行，一般MongoDB都是可公网访问的地址，修改为此地址即可
# 目标将项目打包成一个镜像，让其他远程主机也可运行这个项目，直接将此处MongoDB地址修改为某个公网可访问远程数据库地址，MONGO_URI：
# MONGO_URI = 'mongodb://admin:admin123@120.27.34.25:27017' # 此处地址可修改为自己的远程MongoDB数据库地址

# 5.构建镜像：执行命令：
# dockeer build -t quotes:latest
# 执行过程输出：
# ...
# Successfully built c8101aca6e2a   # 这样输出说明镜像构建成功，查看构建的镜像：
# docker images
# 返回结果：
# quotes latest 41c8499ce210    2 minutes age   769MB   # 即新构建的镜像

# 6.运行：镜像可先在本地测试运行，执行命令：
doceker run quotes
# 7.推送至Docker Hub：构建完成后，可将镜像Push到Docker镜像托管平台，如Docker Hub或私有的Docker Registry，可从远处服务器下载
# Docker Hub：如果项目包含一些私有的连接信息（数据库），最好将Repository设置为私有或者直接放到私有的Docker Registry
# 首先在https://hub.docker.com注册账号，新建Repository，名为quotes，此Repository地址就可以用germey/quotes表示
# 为新建的镜像打一个标签：
docker tag quotes:latest germey/quotes:latest
# 推送镜像到Docker Hub，命令：
docker push germey/quotes
# Docker Hub便会出现新推送的Docker镜像了：
# 如果想在其他主机上运行这个镜像，主机上安装后Docker后，可以直接执行命令：
docker run germey/quotes    # 就会自动下载镜像，启动容器运行，不需配置Python环境，不需关心版本冲突问题
# 整个项目爬取完成后，数据就可以存储到指定的数据库中
# 将Scrapy项目制作成Docker镜像并部署到远程服务器运行，使用此种方式，列出的问题都迎刃而解

