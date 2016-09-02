#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  160902 15:42:41
#    Desc   :  

#尽量用异常来表示特殊情况，而不要返回None

#解决方法一，把返回值拆成两部分，首个元素，表示操作是否成功，接下来那个元素，才是真正的运算结果。

def divide_one(a,b):
    try:
        return True, a/b
    except ZeroDivisionError:
        return False, None

x,y=5,0
success,result=divide_one(x,y)
if not success:
    print('Invalid inputs')
else:
    print result

#第二种方法更好一些，那就是根本不返回None,而是把异常抛给上一级，使得调用者必须应对它

def divide_two(a,b):
    try:
        return a/b
    except ZeroDivisionError as e:
        raise ValueError('Invalid input') 

#test
try:
    result=divide_two(x,y)
except ValueError:
    print('Invalid inputs')
else:
    print('Result is %.1f'%result)


