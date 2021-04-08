# 利用urllib的robotparser模块，可实现网站Robots协议的分析。
# 1.Robots协议(网络爬虫排除标准Robots Exclusion Protocol)：爬虫协议、机器人协议,用来告诉爬虫和搜索引擎哪些可以爬取，哪些不可
# 抓取。通常是一个robots.txt文本文件，一般放在网站的根目录下。
# 当搜索爬虫访问一个站点时，首先会检查这个站点根目录下是否存在robots.txt文件，如果存在，搜索爬虫会根据其中定义的爬虫范围来爬取
# 如果没有找到这个文件，搜索爬虫便会访问所有可直接访问的页面。
# robots.txt样例：
User-agent: *
Disallow: /
Allow: /public/     # 实现了对所有搜索爬虫只允许爬取public目录的功能，将上述内容保存在robots.txt文件，放在网站根目录下，
                    # 和网站的入口文件(index.php、index.html、index.jsp)放在一起

# 2.爬虫名称：BaiduSpider等

# 3.robotparser：使用robotparser模块来解析robots.txt。该模块提供了一个类RobotFileParser，可根据某网站的robots.txt文件来判断
# 一个爬取爬虫是否有权限来爬取这个网页。
# 该类只需在构造方法里传入robots.txt链接即可。首先看下它的声明:
urllib.robotparser.RobotFileParser(url='')