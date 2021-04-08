# 如果需要部署10台主机，每台主机都安装Docker，然后再去运行Scrapyd服务，工作量不小
# 一种方案：一台主机已经安装好各种开发环境，取到它的镜像，然后用镜像来批量复制多台主机，批量部署就可轻松实现
# 另一种方案：新建主机的时候直接制定一个运行脚本，脚本里写好配置各种环境的命令，指定其在新建主机的时候自动执行，主机创建后
# 所有的环境就按照自定义的命令配置好了，也可以很方便地实现批量部署
# 目前很多服务商都提供云主机服务，如阿里云、腾讯云、Azure、Amazon等，不同的服务商提供了不同的批量部署云主机的方式。
# 腾讯云提供了创建自定义镜像的服务，在新建主机的时候使用自定义镜像创建新的主机即可，这样就可以批量生成多个相同的环境。
# Azure提供了模板部署的服务，可以再模板中指定新建主机时执行的配置环境的命令，这样在主机创建后环境就配置完成了。

# 1.镜像部署：腾讯云，首先需要有一台已经安装好环境的云主机，Docker和Scrapyd镜像均已正确安装，Scrapyd镜像启动加到开机启动脚本中
# 进入腾讯云后台，点击更多选项制作镜像
# 输入镜像的一些配置信息：
# 确认制作镜像，稍等片刻即可制作成功
# 接下来，创建新的主机，在新建主机时选择已经制作好的镜像，后续配置过程按照提示进行即可
# 配置完成后登陆到云主机，可看到当前主机Docker和Scrapyd镜像都已经安装好。Scrapyd服务已经正常运行，即通过自定义镜像方式实现了

# 2.模板部署：Azure的云主机部署时都会使用一个部署模板，这个模板实际上是一个JSON文件，里面包含了很多部署时的配置选项，
# 如主机名称、用户名、密码、主机型号等。在模板中我们可以指定新建完云主机后执行的命令行脚本，如安装Docker、运行镜像等
# 等部署工作全部完成后，新创建的云主机就已经完成环境配置，同时运行相关服务
# 提供一个部署Linux主机自动安装Docker和运行Scrapyd镜像的模板，模板内容太多，\
# 源文件：https://github.com/Python3WebSpider/ScrapydDeploy/blob/master/azuredeploy.json
# 模板中Microsoft.Computer/virtualMachines/extensions部分有一个commandToExecute字段，可以指定建立主机后自动执行的命令。
# 命令完成的是安装Docker并运行Scrapyd镜像服务的过程

# 首先安装一个Azure组件，安装过程参考：https://docs.azure.cn/zh-cn/xplat-cli-install，之后可使用azure命令行进行部署。
# 登录Azure，登录的是中国区，命令：
azure login -e AzureChinaCloud
# 没有资源组，需要新建一个资源组，命令：
azure group create myResourceGroup chinanorth   # myResourceGroup是资源组的名称，可自行定义
# 使用该模板进行部署，命令：
azure group deployment create --template-file azuredeploy.json myResourceGroup myDeploymentName # myDeploymentName任务名
# 如，部署一台Linux主机的过程：
azure group deployment create --template-file azuredeploy.json MyResourceGroup SingleVMDeploy
info:   Executing command group deployment create
info:   Supply values for the following parameters
adminUsername:  datacrawl
adminPassword:  DataCrawl123
vmSize: Standard_D2_v2
vmName: datacrawl-vm
dnsLabelPrefix:     datacrawlvm
storageAccountName:     datacrawlstorage
# 运行命令后，提示输入各个配置参数，如主机用户名、密码等。之后等待整个部署工作完成即可，命令行会自动退出。
# 然后登陆云主机即可查看到Docker已经成功安装并且Scrapyd服务正常运行。

# 大规模分布式爬虫架构中，如果需要批量部署多个爬虫环境，使用如上方法可以快速批量完成环境的搭建工作，不用逐个主机配置环境
# 解决了皮力量部署的问题，创建主机完毕后即可直接使用Scrapyd服务