# Splash页面爬取时，若爬取量非常大，用一个Splash服务来处理，压力太大，可以考虑搭建一个负载均衡器来分散压力到各个服务器上
# 1.配置Splash服务
# 首先要有多个Splash服务，在4台远程主机的8050端口上都开启了Splash服务，服务地址分别为41.159.27.223:8050、41.159.27.221:8050、
# 41.159.27.9:8050、41.159.117.119:8050,4个服务完全一致，都是通过Docker的Splash镜像开启，访问任何一个，都可以用Splash服务
# 2.配置负载均衡
# 任意一台带有公网IP的主机来配置负载均衡
# 在主机上装好Nginx，修改Nginx的配置文件nginx.conf，添加如下内容：
# http {
#     upstream splash {                   # 通过upstream定义一个名为splash的服务集群配置
#         least_conn;                     # least_conn代表最少链接负载均衡：适合处理请求处理时间长短不一造成服务器过载的情况
#         server 41.159.27.223:8050;
#         server 41.159.27.221:8050;
#         server 41.159.27.9:8050;
#         server 41.159.117.119:8050;
# }
# server {
#     listen 8050;
#     location / {
#         proxy_pass http://splash;
#     }
# }
# }


# 也可不指定配置：
# upstream splash {   # 默认以轮询策略实现负载均衡，每个服务器压力相同；适合服务器配置相当、无状态且短平快的服务使用
#     server 41.159.27.223:8050;
#     server 41.159.27.221:8050;
#     server 41.159.27.9:8050;
#     server 41.159.117.119:8050;
# }


# # 还可以指定权重：
# upstream splash {   # weight参数指定各个服务的权重，权重越高，分配到处理的请求越多。不同的服务器配置差别比较的的话，可以使用
#     server 41.159.27.223:8050 weight=4;
#     server 41.159.27.221:8050 weight=2;
#     server 41.159.27.9:8050 weight=2;
#     server 41.159.117.119:8050 weight=1;
# }


# 3.配置认证：Splash可以公开访问，不想让其公开访问，可配置认证
# 可在server的location字段中添加auth_basic和auth_basic_user_file字段
# http {
#     upstream splash {
#     server 41.159.27.223:8050;
#     server 41.159.27.221:8050;
#     server 41.159.27.9:8050;
#     server 41.159.117.119:8050;
# }
# server {
#     listen 8050;
#     location / {
#         proxy_pass http://splash;
#         auth_basic "Restricted";
#         auth_basic_user_file /etc/nginx/conf.d/.htpasswd;     # 用户名和密码配置放在/etc/nginx/conf.d目录，htpasswd创建
#         }
#     }
# }

# 创建一个用户名为admin的文件
# htpasswd -c .htpasswd admin
# # 提示输入密码，输入两次后，生成密码文件
# cat .htpasswd
# amdin:5ZBxQr0rCqwbc
# 配置完成后，重启Nginx服务
# sudo nginx -s reload


# 4.测试：利用http:httpbin.org/get测试负载均衡的配置，看是不是每次请求会切换IP
# import requests
# from urllib.parse import quote
# import re
#
# lua = '''
#
# function main(splash, args)
#     local treat = require("treat")
#     local response = splash:http_get("http://httpbin.org/get")
#     return treat.as_string(response.body)
# end
# '''
#
# url = 'http://splash:8050/execute?lua_source=' + quote(lua) # URL中的splash字符串自行替换成自己Nginx服务器IP，
# response = requests.get(url, auth=('admin', 'admin'))
# ip = re.search('(\d+\.\d+\.\d+)'), response.text).group(1)
# print(ip)
# 多次运行代码，发现每次请求的IP都变化，说明负载均衡已经成功实现