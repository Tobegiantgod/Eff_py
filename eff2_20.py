#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  161025 16:10:47
##################################
#2-20用None和文档字符串来描述具有动态默认值的参数
##################################

#有时我们想要打印消息时，需要记录实时时间，这时我们可能需要采用一种非静态的类型，来做关键字参数的默认值，如下：

from datetime import datetime
from time import sleep

def log(message,when=datetime.now()):
    print('%s:%s'%(when,message))
log('Hi there!')
sleep(0.1)
log('Hi again!')

#但是两条消息的时间戳是一样的，这是因为datetime.now只执行了一次，也就是它只在函数定义的时候执行了一次。


#在Python中若想正确实现动态默认值，习惯上是把默认值设置为None,并在文档字符里面把None的实际行为描述出来。

def log_c(message,when=None):
    """Log a message with a timestamp.

    Args:
        message:Message to print.
        when:datetime of when then message occurred.
            Default to the present time.
    """
    when=datetime.now() if when is None else when
    print ('%s:%s'%(when,message))
log_c('Hi')
sleep(0.1)
log_c('Hi again')


#从编码为JSON格式的数据中载入某个值时。若解码时失败，则返回默认空的字典。我们可能会采用下面这种办法来实现此功能：
import json

def decode(data,default={}):
    try:
        return json.loads(data)
    except ValueError:
        return default


#由于defalut参数的默认值都只会在模块加载时评估一次，所以凡是以默认形式来调用decode函数的代码，都将共享一份字典。这会引发非常奇怪的行为。

foo=decode('bad data')
foo['stuff']=5
bar=decode('also bad')
bar['meep']=1
print ('Foo:',foo)
print ('Bar:',bar)

#上面bar和foo实际上是一个字典，并没有达到我们想要返回两个字典的目的，应该如下修改：

def decode_c(data,default=None):
    """Load JSON data from a string.

    Args:
        data:JSON data to decode.
        dafault:Value to return if decoding fails.
            Defaults to an empty dictionary.
    """
    if default is None:
        defalut={}
    try:
        return json.loads(data)
    except ValueError:
        return defalut


foo=decode_c('bad data')
foo['stuff']=5
bar=decode_c('also bad')
bar['meep']=1
print ('Foo:',foo)
print ('Bar:',bar)



