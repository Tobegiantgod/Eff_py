#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  170215 21:03:59
##################################
# 1-4 用辅助函数来取代复杂的表达式
##################################

# 使用python3运行此程序
from urllib.parse import parse_qs

my_values = parse_qs('red=5&blue=0&green=',keep_blank_values=True)

def get_first_int(values, key, default=0):
    found = values.get(key,[''])
    if found[0]:
        found = int(found[0])
    else:
        found = default
    return found

print (get_first_int(my_values,'red'))

# 把复杂的表达式移入辅助函数之中，如果要反复使用相同的逻辑，那就更应该这么做
