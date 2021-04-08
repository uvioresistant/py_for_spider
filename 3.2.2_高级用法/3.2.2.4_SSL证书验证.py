# 发送HTTP请求的时候，会检查SSL证书，可以使用verify参数控制是否检查此证书，
# 如果不加verify参数，默认是True，自动验证
# import requests
#
# response = requests.get('https://www.12306.cn')
# print(response.status_code)


# import requests
#
# response =  requests.get('https://www.12306.cn', verify=False)
# print(response.status_code)
# 设置忽略警告的方式来屏蔽这个警告
# import requests
# from requests.packages import urllib3
#
# urllib3.disable_warnings()
# response = requests.get('https://www.12306.cn', verify=False)
# print(response.status_code)


# 通过捕获警告到日志的方式忽略警告：
# import logging
# import requests
# logging.captureWarnings(True)
# response = requests.get('https://www.12306.cn', verify=False)
# print(response.status_code)
# 指定一个本地证书用作客户端证书，可以是单个文件（包含密钥和证书）或一个包含两个文件路径的元组


import requests

response = requests.get('https://www.12306.cn', cert=('/path/server.crt', '/path/key'))
print(response.status_code)
# 上面的代码是演示实例，crt和key文件，指定它们的路径，本地私有证书的key必须是解密状态，加密状态的key是不支持的



