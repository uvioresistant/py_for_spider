# import requests
#
# proxies = {
#     "http": "http://10.10.1.10:3128",
#     "https": "http://10.10.1.10:1080",
# }
#
# requests.get("https://www.taobao.com", proxies=proxies)

# 代理使用HTTP Basic Auth，可用http://user:password@host:port的语法来设置代理
# import requests
#
# proxies = {
#     "http": "http://user:password@10.10.1.10:3128/",
# }
# requests.get("https://www.taobao.com", proxies=proxies)


import requests

proxies = {
    'http': 'socks5://user:password@host:port',
    'https': 'socks5://user:password@host:port',
}
requests.get("https://www.taobao.com", proxies=proxies)

