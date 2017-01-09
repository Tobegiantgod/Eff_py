#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  170109 14:05:55
##################################
#7-51 为自编的模块定义根异常，以便将调用者与API相隔离
##################################
import logging
from mypackage import my_moudle
try:
    weight = my_moudle.determine_weight(1,-1)
except my_moudle.Error as e:
    logging.error('Unexpected error: %s', e)
    
#API所抛出的异常，如果向上传播得太远，就会令程序崩溃，而使用try/except语句，则可以防止这种情况，因为它会把调用代码与API隔开。通过捕获根异常，调用者可以得知他们在使用你的API时，所编写的调用代码是否正确。若是某种异常没有得到处理，那么该异常就会传播到try/except语句中负责处理模块根异常的那个except块里面，而那个except块，则会把该异常告知API的使用者，提醒他们应该为这种类型的异常添加适当的处理逻辑。

try:
    weight = my_moudle.determine_weight(1,-1)
except my_moudle.InvalidDensityError:
    weight = 0
except my_moudle.Error as e:
    logging.error('Bug in the calling code: %s', e)

#不过，上面那种try/except语句，并不能把API使用者与API模块代码中的bug相隔离。如果要隔离，那么调用者需要再添加一个except块，以捕获Python的Exception基类。这样他们就能够查出:API模块的实现代码里面是不是留有尚待修复的bug。


try:
    weight = my_moudle.determine_weight(1,-1)
except my_moudle.InvalidDensityError:
    weight = 0
except my_moudle.Error as e:
    logging.error('Bug in the calling code: %s', e)
except Exception as e:
    logging.error('Bug in the API code: %s', e)
    raise

#添加了这个新的NegativeDensityError异常以后，原有的调用代码仍然能够继续运作，因为它所捕获的InvalidDensityError异常，正是这个新异常的父类。

try:
    weight = my_moudle.determine_weight(1,-1)
except my_moudle.NegativeDensityError as e:
    raise ValueError('Must supply non-negative density') from e
except my_moudle.InvalidDensityError:
    weight = 0
except my_moudle.Error as e:
    logging.error('Bug in the calling code: %s', e)
except Exception as e:
    logging.error('Bug in the API code: %s', e)
    raise

#1.为模块定义根异常，可以把API的调用者与模块的API相隔离。

#2.调用者在适应API时，可以通过捕获根异常，来发现调用代码中隐藏的bug。

#3.调用者可以通过捕获Python的Exception基类，来帮助模块的开发者找寻API实现代码中的bug。


