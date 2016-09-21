#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  160921 11:32:32
##################################
#
#在参数上迭代时，要多加小心#

#统计一个列表里数据在总体上的百分比

def normalize(numbers):
    total = sum(numbers)
    result= [] 
    for value in numbers:
        percent=100*value/total
        result.append(percent)
    return result

visits=[15,35,80]
percentages=normalize(visits)
print(percentages)  


