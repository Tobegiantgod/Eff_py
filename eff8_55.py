#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  170111 16:15:54
##################################
#8-55 通过repr字符串来输出调试信息
##################################
#调试Python程序时，print函数不区分值类型,比如数值型的5和字符串类型的'5'。
print(5)
print('5')

#使用repr函数后再传给print函数，可以使print打印出字符串的形式，以便区分。

print(repr('5'))

#使用格式化字符串使用%r,则能够产生与repr函数的返回值相仿的可打印字符串。

print('%r' % '5')


#对于动态的Python对象来说，默认的易读字符串，与repr函数所返回的字符串是相同的，这就是说，我们只需要把动态对象直接传给print函数，即可打印出repr字符串的内容，而不需要再于打印前先调用repr函数，我们可以给类定义名为__repr__的特殊方法，并令该方法返回一个包含python表示的字符串，来使print函数更有意义。

class BetterClass(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'BetterClass(%d, %d)' % (self.x , self.y)

obj = BetterClass(1, 2)
print(obj)

#若是无法修改该类的定义，那我们可以通过对象的__dict__属性来查询它的实例字典。下面这段代码，可以打印出OpaqueClass实例的内容：

print(obj.__dict__)


