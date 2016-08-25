#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  160818 16:54:33
#    Desc   :  
#

##合理利用try/except/else/finally结构中的每个代码块

#如果既要将异常向上传播，又要在异常发生时执行清理工作，那就可以使用try/finally结构：

handle=open('test.txt')
try:
    data=handle.read() 
finally:
    handle.close()


#try/except/else结构可以清晰的描述出哪些异常会由自己的代码来处理、哪些异常会传播到上一级，如果try没有发生异常，那么就执行else块：

import json

data={'1':'asd','2':'fdf','3':'gfgd'}

def load_json_key(data,key):
    try:
        result_dict=json.loads(data)
    except Exception , e:
        print 'could not load file:',e
    else:
        return result_dict[key]
load_json_key(data,2)

#我们可以用try块来读取文件并处理其内容，用except块来应对try块中可能发生的相关异常，用else块实时地更新文件并把更新中可能出现的异常回报给上级代码，然后用finally块来清理文件句柄:

UNDEFINED=object()

def divide_json(path):
    handle=open(path, 'r+')
    try:
        data=handle.read()
        op=json.loads(data)
        value=(op['numerator']/op['denominator']
    except ZeroDivisionError , e:
        return UNDEFINED
    else:
        op['result']=value
        result=json.dumps(op)
        handle.seek(0)
        handle.write(result)
        return value
    finally:
        handle.close()

#这种写法很有用，因为这四块代码互相配合得非常到位。例如，即使在else块写入result数据时发生异常，finally块中关闭文件句柄的那行，依然能执行。
