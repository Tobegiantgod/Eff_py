#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  170114 11:12:39
##################################
# 1-3 了解bytes、str与unicode的区别
##################################

# Python3 有两种表示字符序列的类型：bytes和str。前者的实例包含原始的8位值;后者的实例包含Unicode字符。

# Python2 也有两种表示字符序列的类型，分别叫做str和unicode。与Python3不同的是，str实例包含原始的8位值；而unicode的实例，则包含Unicode字符。

# 程序的核心部分应该使用Unicode字符类型(也就是Python3中的str、Python2中的unicode),一定要把编码和解码放在最外围来做，在编码时最好使用('UTF-8'）

# 编写辅助函数，使得转换后的输入数据能够符合开发者的预期。

# 在Python3中，我们需要编写接受str或bytes,并总是返回str的方法:

# Python3
def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes): 
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value

# 接受str或bytes,总是返回bytes的方法：

def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode('utf-8')
    else:
        value = bytes_or_str
    return value


# 在Python2中，需要接受str或unicode,并总是返回unicode的方法:

#Python2
def to_unicode(str_or_unicode):
    if isinstance(str_or_unicode, str):
        value = str_or_unicode.decode('utf-8')
    else:
        value = str_or_unicode
    return value

# 接受str或unicode,并总是返回str的方法:
def to_str(str_or_unicode):
    if isinstance(str_or_unicode, unicode):
        value = str_or_unicode.encode('utf-8')
    else:
        value = str_or_unicode
    return value


# 在Python中使用原始8位值与Unicode字符时，有两个问题需要主要。第一个问题可能会出现在Python2里面。如果str只包含7位ASCII字符，那么unicode和str实例似乎就成了同一种类型。可以用+操作符把这种str与unicode连接起来。可以用等价与不等价操作符，在这种str实例与unicode实例之间进行比较。在格式字符串中，可以用'%s'等形式来代表unicode实例。

# 这些行为意味着，在只处理7位ASCII的情景下，如果函数接受str, 那么可以给它传入unicode; 如果函数接受unicode, 那么也可以给它传入str。而在Python3中，bytes与str实例则绝对不会等价，即使是空字符串也不行。所以，在传入字符序列的时候必须留意其类型。

# 在Python2中打开文件，需要写入一些二进制数据，需要向下面这样写

import os
with open('test.txt', 'w') as f:
    f.write(os.urandom(10))
f.close()

# 在Python3中打开文件，需要写入一些二进制数据，需要用二进制写入模式('wb')来开启待操作的文件，而不能像原来那样，采用字符写入模式('w')。按照下面这种方式来使用open函数，即可同时适配Python2与Python3:
with open('test.txt', 'wb') as f:
    f.write(os.urandom(10))
f.close()


# 所以，从文件中读取二进制数据，或向其中写入二进制数据时，总应该以'rb'或'wb'等二进制模式来开启文件。










