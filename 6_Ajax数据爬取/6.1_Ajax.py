# Ajax：Asynchronous JavaScript and XML，异步的JavaScript和XML，不是一门变成语言，利用JavaScript在保证页面不被刷新、
# 页面链接不改变的情况下与服务器交换数据并更新部分网页的技术
# 传统的网页，想更新内容，必须要刷新整个页面，有了Ajax，可以在页面不全部刷新的情况下更新内容。
# 页面实际上是在后台与服务器进行了数据交互，获取数据后，再利用JavaScript改变网页，这样网页内容就会更新


# 1.微博页面其实并没有整个刷新，意味着页面的链接没有变化，网页中却多了新内容，就是通过Ajax获取数据并呈现的过程


# 2.基本原理：发送请求、解析内容、渲染网页
# JavaScript可以实现页面的各种交互功能，Ajax也不例外，也是由JavaScript实现的，执行了如下代码：
# var xmlhttp;
# if (window.XMLHttpRequest){                                       # 新建了XMLHttpRequest对象
#     // code for IE7+, Firefox, Chrome,Opera, Safari
#     xmlhttp=new XMLHttpRequest();
# }else {// code for IE6, IE5
#     xmlhttp=new ActiveXObject("Microsoft.XMLHTTP")
# }
# xmlhttp.onreadystatechange=function(){                            # 调用onreadystatechange属性设置监听
#     if(xmlhttp.readyState==4 && xmlhttp.status==200){             # 服务器响应时，对应方法被触发，方法里解析响应内容即可
#         document.getElementById("myDiv").innerHTML=xmlhttp.responseText;
#     }
# }
# xmlhttp.open("POST","/ajax/",true);                               # 调用open方法，像某个链接（服务器）发送请求
# xmlhttp.send();                                                   # 调用send方法，像某个链接（服务器）发送请求
# JavaScript对Ajax最底层的实现

# 解析内容


# 渲染网页


