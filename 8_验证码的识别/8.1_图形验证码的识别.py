# 图形验证码是最简单的验证码一般由4位字母或数字组成
# 中国知网注册页面http://my.cnki.net/elibregister/commonRegister.aspx
# 1.利用OCR技术识别图形验证码

# 2.识别图形验证码需要库tesserocr

# 3.获取验证码：f12，验证码元素是一张图片，src属性是CheckCode.aspx
# 直接打开连接http://my.cnki.net/elibregister/CheckCode.aspx，看到验证码右键保存，命名为code.jpg

# 4.识别测试：新建项目，将验证码放到项目根目录下，tesserocr库识别验证码：
# import tesserocr
# from PIL import Image
#
# image= Image.open('code.jpg')   # 新建一个Image对象
# result = tesserocr.image_to_text(image) # 调用tesserocr的image_to_text方法，传入Image对象，完成识别
# print(result)

# tesserocr还有更加简单的方法，可直接将图片文件转化为字符串
# import tesserocr
# print(tesserocr.file_to_text('code.jpg'))


# 5.验证码处理：
import tesserocr
from PIL import Image

image = Image.open('code2.jpg')
result = tesserocr.image_to_text(image)
print(result)
# 输出结果4IRP，有偏差，验证码内多余线条干扰了图片识别
# 额外处理，转灰度、二值化操作

# 利用Image对象的convers方法参数传入L，将图片转化为灰度图像
# image = image.convert('L')
# image.show()

# 传入1，将图片进行二值化处理
# image = image.convert('1')
# image.show()

# 指定二值化阈值，采用的默认阈值127，不能直接转化原图，将原图先转化为灰度图像，再指定二值化阈值
# image = image.convert('L')
# threshold = 130
# table = []
# for i in range(256):
#     if i < threshold:
#         table.append(0)
#     else:
#         table.append(1)
#
# image = image.point(table, '1')
# image.show()
# 验证码中线条已经去除，变得黑白分明，重新识别：
import tesserocr
from PIL import Image

image = Image.open('code2.jpg')

image = image.convert('L')
threshold = 127
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

image = image.point(table, '1')
result = tesserocr.image_to_text(image)
print(result)
# 结果4JRP，针对有干扰的图片，做一些灰度和二值化处理，会提高图片识别的正确率