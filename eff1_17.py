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

visits=[15.0,35.0,80.0]
percentages=normalize(visits)
print(percentages)  

#为了应用更大的数据，使用生成器函数来实现以上函数

def read_visits(data_path):
    with open(data_path)as f :
        for line in f:
            yield int(line)

it=read_visits('my_numbers.txt')
percentages=normalize(it)
print(percentages)


#以上结果表示在已经用完的迭代器上面继续迭代时，不会报错.为了解决此问题,可以使用迭代器制作一份列表，将它的全部内容复制到这个列表里，然后可以在这个列表里多次迭代：

def normalize_copy(numbers):
    numbers=list(numbers)
    total=sum(numbers)
    result=[]
    for value in numbers:
        percent=100*value/total
        result.append(percent)
    return result

itt=read_visits('my_numbers.txt')
percentages=normalize_copy(itt)
print percentages

#上面的写法问题在于，待复制的那个迭代器，可能含有大量的输入数据，从而导致程序在复制迭代器的时候耗尽内存并崩溃。
#一种解决办法是通过参数来接受另一个函数，那个函数每次调用后，都能返回新的迭代器

def normalize_func(get_iter):
    total=sum(get_iter())
    result=[]
    for value in get_iter():
        percent=100*value/total
        result.append(percent)
    return result

path='my_numbers.txt'

percentages=normalize_func(lambda:read_visits(path))
#上面一句等价如下写法
#def get_iter():
#    return read_visits(path)
#percentages=normalize_func(get_iter)
print percentages











