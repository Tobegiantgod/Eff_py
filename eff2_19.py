#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  161024 17:22:44
##################################
#2-19用关键字参数来表达可选的行为
##################################

def remainder(number,divisor):
    return number%divisor

#位置参数必须出现在关键字参数之前

#一下使用方法都是有效的
remainder(20,7)
remainder(20,divisor=7)
remainder(number=20,divisor=7)
remainder(divisor=7,number=20)

#以下方法是错误的，位置参数出现在了关键字参数后面
#remainder(number=20,7)


#定义函数时，可以为参数确定默认值，如下：

def flow_rate(weight_diff,time_diff,period=1,units_per_kg=1):
    return ((weight_diff*units_per_kg)/time_diff)*period

#最后在调用函数时，要尽量都使用关键字参数，以免影响程序的可读性和扩展性。

