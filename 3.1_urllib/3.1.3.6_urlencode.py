# urlencode构造GET请求参数的时候非常有用
from urllib.parse import urlencode

params = {
    'name': 'germey',
    'age': 22
}
base_url = 'http://www.baidu.com?'
url = base_url + urlencode(params)
print(url)

# 非常常用，为了更加方便地构造参数，事先用字典来表示，要转化为URL的参数时，只需要调用该方法即可。
