# 在网络不好的情况下，如果出现了异常，不处理的话，程序会因报错而终止运行，异常处理十分必要
# urllib的error模块定义了由request模块产生的异常，如果出现了问题，request模块便会抛出errror模块中定义的异常
# 1.URLError：来自urllib库的error模块，继承自OSError类，是error异常模块的基类，由request模块生成的异常都可以通过捕获该类处理
from urllib import request, error
try:
    response = request.urlopen('https://cuiqingcai.com/index.htm')
except error.URLError as e:
    print(e.reason) # 属性reason，返回错误的原因