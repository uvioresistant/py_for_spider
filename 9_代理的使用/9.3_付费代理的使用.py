# 1.付费代理分为两类：
#   a.提供接口获取海量代理，按天或按量收费：迅代理
#   b.搭建了代理隧道，直接设置固定域名代理：阿布云代理

# 2.迅代理：http://www.xdaili.cn/
# 优质代理：适合对代理IP需求量非常大，但能接受较短有效时长的小部分不稳定的客户
# 独享动态：适合对代理IP稳定性要求非常高且可以自主控制的客户，支持地区筛选
# 独享秒切：适合对代理IP稳定性要求非常高且可以自主控制的客户,可快速获取IP，地区随机分配
# 动态混拨：适合对代理IP需求量大、代理IP使用失效短（3分钟）、切换快的客户
# 优质定制：定制服务
# 一般第一类优质代理即可，代理的量比较大，稳定性不高，一些代理不可用，需要借助代理池，再做一次筛选，确保代理可用
# 迅代理会提供一个API来提取代理：http://www.xdaili.cn/ipagent/greatRecharge/getGreatIp?spiderID=da289b78fec24fl9b392e04
#106253f2a&orderno=YZ20177140586mTTnd7&returnType=2&count=20
# 指定了提取数量为20，提取格式为JSON，直接访问链接即可提取代理，解析这个JSON，将其放入代理池中
# 只需在Crawler中再加一个crawl开头的方法：
def crawl_xdaili(self): # 代理池中接入了迅代理，获取迅代理的结果后，解析JSON，返回代理即可
    """
    获取迅代理
    :param self: 代理
    :return:
    """
    url =
        'http://www.xdaili.cn/ipagent/greatRecharge/getGreatIp?da289b78fec24f19b392e04106253f2a&orderno=' \
        'YZ20177140586mTTnd7&returnType=2&count=20'
    html = get_page(url)
    if html:
        result = json.loads(html)
        proxies = result.get('RUSULT')
        for proxy in proxies:
            yield proxy.get('ip') + ':' + proxy.get('port')


# 阿布云代理：提供代理隧道，速度快且非常稳定，https://www.abuyun.com/
# 分两种，专业版和动态版，定制版
# 专业版：多个请求锁定一个代理IP，海量IP资源池需求，使用与请求IP连续型业务
# 动态版：每个请求分配一个随机代理IP，海量IP资源池需求，使用与爬虫类业务
# 定制版：灵活按照需求定制，定制IP区域，定制IP使用时长，定制IP每秒请求数
# 代理的连接域名：proxy.abuyun.com，端口9020，每次使用后IP都会更改，该过程其实就是利用了代理隧道实现
# 云代理通过代理隧道的形式提供高匿名代理服务，支持HTTP/HTTPS协议
# 云代理在云端维护一个全局IP池供代理隧道使用，池中的IP会不间断更新，保证同一时刻IP池中有几十到几百个可用代理IP
# 代理IP池中部分IP可能会在当天重复出现多次
# 动态版HTTP代理隧道会为每个请求从IP池中挑选一个随机代理IP
# 无需切换代理IP，每一个请求分配一个随机代理IP
# HTTP代理隧道有并发请求限制，默认每秒只允许5个请求。如果需要更多请求数，须另外购买
import requests

url = 'http://httpbin.org/get'

# 代理服务器
proxy_host = 'proxy.abuyun.com'
proxy_port = '9020'
# 代理隧道验证信息
proxy_user = 'H01234567890123D'
proxy_pass = '0123456789012345'

proxy_meta = 'http://%(user)s:%(pass)s@%(host)s:%(port)s' % {
    'host': proxy_host,
    'port': proxy_port,
    'user': proxy_user,
    'pass': proxy_pass,
}
proxies = {
    'http': proxy_meta,
    'https': proxy_meta,
}
response = requests.get(url, proxies=proxies)
print(response.status_code)
print(response.text)
# 输出结果的origin即为代理IP的实际地址，多次运行测试，每次origin都会在变化，即动态代理的效果
