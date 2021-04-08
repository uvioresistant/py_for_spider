# 将提取的结果写入文件，直接写入到一个文本文件中
# 通过JSON库的dumps方法实现字典的序列化，指定ensure_ascii参数为False，可以保证输出结果是中文形式而不是Unicode编码
import json

def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        print(type(json.dumps(content)))
        f.write(json.dumps(content, ensure_ascii=False)+ '\n')
# 调用write_to_file即可实现将字典写入到文本文件的过程，此处的content参数就是提取结果，是一个字典