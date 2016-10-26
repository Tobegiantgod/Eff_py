#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  161026 14:55:17
##################################
#2-21用只能以关键字形式指定的参数来确保代码明晰
##################################

#为了使程序更易读，表达更明确，我们可以在书写代码时，让函数调用者只能使用关键字参数传递参数。

#Python2中我们可以使用操作符**如下方法进行实现:

def safe_division_d(number,divisor,**kwargs):
    ignore_overflow=kwargs.pop('ignore_overflow',False)
    ignore_zero_div=kwargs.pop('ignore_zero_division',False)
    if kwargs:
        raise TypeError('Unexpected **kwargs: %r' % kwargs)

    try:
        return number/divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_div:
            return float('inf')
        else:
            raise

#下面我们可以用如下方法进行调用函数：

#safe_division_d(1,0)
print safe_division_d(1,0,ignore_zero_division=True)
print safe_division_d(1,10**500,ignore_overflow=True)

#Python3中有明确的语法*来指定只能以关键字指定的参数，python2中的函数可以接受**kwargs参数，并手工抛出TypeError异常，以便模拟只能以关键字形式来指定的参数。

