#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  170113 16:02:30
##################################
#8-58 先分析性能，然后再优化
##################################

#由于Python是一门动态语言，所以Python程序的运行效率可能与我们预想的结果有很大差距。
#有一些操作我们认为应该执行得比较慢，但实际上却很快：对字符串的操作，以及生成器等。
#另外一些语言特性，我们认为应该执行得比较快，但实际上却很慢，例如，属性访问及函数调用等操作。

#应对性能问题的最佳方式，是在优化程序之前先分析其性能，而不是靠直觉去判断。

#python提供了内置的profiler，一种是纯Python的profiler(名字叫做profile),另一种是C语言扩展模块(名字叫做cProfile)。在这两者中，内置的cProfile模块更好，因为她在做性能分析时，对受测程序的效率只会产生很小的影响，而纯Python版的profiler，则会产生较大的开销，从而使测试结果变得不够准确。

#我们定义下面的插入排序法(insertion sort)来进行测试

from bisect import bisect_left

def insertion_sort(data):
    result = []
    for value in data:
        insert_value(result, value)
    return result

def insert_value(array, value):
    i = bisect_left(array, value)
    array.insert(i, value)

from random import randint

max_size = 10**4
data = [randint(0, max_size) for _ in range(max_size)]
test = lambda: insertion_sort(data)

#下面实例化cProfile模块中的Profile对象，并通过runcall方法来运行刚才定义的test函数：
from cProfile import Profile

profiler = Profile()
profiler.runcall(test)

#我们采用内置的pstats模块和模块中的Stats类来分析数据

from pstats import Stats

stats = Stats(profiler)
stats.strip_dirs()
stats.sort_stats('cumulative')
stats.print_stats()


#当程序中很多模块都会调用一个函数时，我们可以通过下面的方法来知道谁调用的更多。

def my_utility(a, b):
    pass

def first_func():
    for _ in range(1000):
        my_utility(4, 5)

def second_func():
    for _ in range(10):
        my_utility(1, 3)

def my_program():
    for _ in range(20):
        first_func()
        second_func()

test = lambda: my_program()

profiler = Profile()
profiler.runcall(test)
stats = Stats(profiler)
stats.strip_dirs()
stats.sort_stats('cumulative')
stats.print_callers()

#做性能分析时，应该使用cProfile模块，而不要使用profile模块，因为前者能够给出更为精确的性能分析数据。








