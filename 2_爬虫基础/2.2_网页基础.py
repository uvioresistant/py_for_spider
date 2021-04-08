# 网页的组成：分为三大部分：HTML骨架、CSS皮肤、JS肌肉。三者结合才能形成一个完善的网页

# 1>HTML(Hyper Text Markup Lanuguage):超文本标记语言，不同类型的文字通过不同类型的标签来表示，图片img，视屏video、段落p，
# 它们之间的布局通过布局标签div嵌套组合而成，各种标签通过不同的排列和嵌套才形成了网页的框架
# 整个网页就是各种标签嵌套组合而成的，标签定义的节点元素相互嵌套和组合形成了复杂的层次关系，形成了网页的架构

# 2>CSS(Cascading Style Sheets):层叠样式表，“层叠”指当在HTML中引用了数个样式文件，并且样式发生冲突时，浏览器能依据层叠
# 顺序处理。“样式”指网页中文字大小、颜色、元素间距、排列等格式；目前唯一的网页页面排版样式标准
#head_wrapper.s-ps-islite 。s-p-top {          # 大括号前是一个CSS选择器，首先选中id为head_wrapper且class为s-ps-islite节点
                                               # 然后再选中内部class为s-p-top的节点
    position:absolute;               # 大括号内部写是一条条样式规则，position布局方式为绝对布局
    bottom: 40px;                    # bottom指定元素的下边距为40像素
    width: 100%;                     # width指定宽度为100%占满父元素
    height: 181px;                   # height指定元素的高度
}
# 网页中，一般统一定义整个网页的样式规则，写入CSS文件中(后缀为.css)，在HTML中，只需用link标签即可引入写好的CSS文件。

# 3>JS：脚本语言。网页中看到的交互和动画效果，如下载进度条、提示框、轮播图等，使得用户与信息之间不只是一种浏览与显示的关系，而是
# 一种实时、动态、交互的页面功能。
# JS也是以单独的文件形式加载，后缀.js，HTML中通过script标签即可引入
<script src="jquery-2.1.0.js"></script>
# HTML定义了网页的内容和结构，CSS描述了网页的布局，JS定义了网页的行为

# 2.网页的结构：新建文本，名称自取，后缀html
<!DOCTYPE html> # 用COCTYPE定义文档类型
<html>  # 最外层是html标签
  <head>    # 内部是head标签，网页头，
    <title>2.2.2_网页结构.html</title>  # title定义网页标题，会显示在网页选项卡中，不会显示在正文中
    <meta http-equiv="content-type" content="text/html; charset=UTF-8"> # 定义一些页面的配置和引用，网页编码UTF-8
  </head>

  <body>    # body标签，网页体，在网页正文中显示的内容
   <div id="container"> # div定义了网页中的区块，id是container，非常有用的属性，且id内容在网页中唯一，通过它来寻找中国区块
   <div class="wrapper">    # 区块内又有一个div标签，class为wrapper，非常常用的属性与CSS配合设定样式
   <h2 class="title">Hello World</h2>   # 区块内部有h2标签，代表二级标题，有各自的class属性
   <p class="text">Hello, this is a paragraph.</p>  # p标签，代表一个段落，两者中直接写入相应内容即可在网页中呈现出来
   </div></div>
  </body>
</html>

# 3.节点树及节点间的关系：
# HTML中，所有标签定义内容都是节点，构成了一个HTML DOM树
# DOM(Document Object Model):是W3C（万维网联盟)的标准，文档对象模型，定义了访问HTML和XML文档的标准：
# W3C文档对象模型(DOM)中立于平台和语言的接口，允许程序和脚本动态地访问和更新文档的内容、结构和样式
# W3C DOM被分为3个不同的部分：
# a.核心DOM：针对任何结构化文档的标准模型
# b.XML DOM：针对XML文档的标准模型
# c.HTML DOM: 针对HTML文档的标准模型
# 根据W3C的HTML DOM标准，HTML文档中的所有内容都是节点：
# A.整个文档是一个文档节点
# B.每个HTML元素是元素节点
# C.HTML元素内的文本是文本节点
# D.每个HTML属性是属性节点
# E.注释是注释节点
# HTML DOM将HTML文档视作树结构，节点树，通过HTML DOM，树中的所有节点均可通过JS访问，所有HTML节点元素均可被修改，创建，删除
# 节点树中的节点彼此拥有层级关系，常用父、子、兄弟来描述
# 节点树中，顶端节点为根节点(root)

# 4.选择器:CSS选择器定位节点，div节点的id为container，可表示为#container，#开头代表选择id，后紧跟id的名称；
#               想选择class为wrapper的节点，使用.wrapper,以点(.)开头代表选择class，后紧跟class名称
#               还有一种选择方式，根据标签名筛选，选择二级标题，直接用h2接口。
# CSS选择器还支持嵌套选择，各个选择器键加上空格分隔开便可以代表嵌套关系，
# 如，#container .wrapper p代表先选择id为container的节点，然后选中内部的class为wrapper的节点，再进一步选中内部的p节点
#                         不加空格，代表并列关系，
# 如，div#container .wrapper p.text代表先选择id为container的div节点，选中内部的class为wrapper，进一步选中class为text的p节点
# CSS选择器的其他语法规则：
选择器             例子                  例子描述
.class           .intro              选择class="intro"的所有节点
#id              #firstname          选择id="firstname"的所有节点
*                   *                选择所有节点
elemet               p               选择所有p节点
element,element    div,p             选择所有div节点和所有p节点
...

