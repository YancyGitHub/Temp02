#encoding=utf-8

import os
import os.path
import re


# 正则匹配文件名，失败返回 0，成功返回文件名字符串
def match_file_name(str):
    matchObj = re.match( r'document\.write\(.*align=center.*a name=\'(.*)\'>(.*)</b.*', str, re.M|re.I)
 
    if matchObj: # 匹配到内容
        ret = "[" + matchObj.group(1) + "]" + matchObj.group(2) + ".html"
        return ret
    else:
        return 0

# 文件前后分别插入指定内容
def insert_html_header_tail(fp):
        head_data = """<!DOCTYPE html>\n<html>\n<head></head>\n<body>\n<script>\n"""
        tail_data= """\n</script>\n</body>\n</html>"""

        fp.seek(0, 0)         # 移动指针到文件头
        old = fp.read()
        fp.seek(0, 0)         # 移动指针到文件头
        fp.write(head_data)   # 插入文件开始内容
        fp.write(old)         # 写入文件原始内容
        fp.seek(0, 2)         # 移动指针到文件尾
        fp.write(tail_data)   # 插入文件末尾内容

# 获取新的文件名
def get_new_file_name(fp):
    fp.seek(0, 0)         # 移动指针到文件头

    new_file_name = 0
    while True:
        line = fp.readline()
        if not line:        # 读到文件尾
            break
        
        new_file_name = match_file_name(line)
        if(new_file_name != 0): # 匹配到内容
            break

    return new_file_name

def modify_file(parent, filename):
    with open(os.path.join(parent, filename), 'r+') as fp:
        new_file_name = get_new_file_name(fp)
        insert_html_header_tail(fp)

        if new_file_name != 0: # 成功获取新文件名，则重命名文件
            print os.path.join(parent, filename), " => ", os.path.join(parent, new_file_name)
            os.rename(os.path.join(parent, filename), os.path.join(parent, new_file_name))

        fp.close()


def modify_all_test_files():
    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    for parent, dirnames, filenames in os.walk("./tt"):
        for filename in filenames:
            modify_file(parent, filename)



# 获取文件获取文件列表
# 读文件内容，取文件名
# 修改文件内容
# 重命名文件


def create_test_files():
    file_content = """
document.write("<p align=center style='FONT-SIZE:13.5pt;font-family:宋体'><b><a name='%(maj)d-%(naj)d'>测试标题%(num)d</b><p>");

document.write('<p><p>afssssssssssfafasdasd<p><p>')
"""
    for maj in range(1, 10):
        for naj in range(1, 20):
            content = file_content%{'maj':maj, 'naj':naj, 'num':naj}
            file_name = "%d-%d.txt"%(maj, naj)
            with open(os.path.join("./tt", file_name), "w+") as fp:
                fp.write(content)
                fp.close()


flag = 0

if flag == 1:
    create_test_files()
else:
    modify_all_test_files()
