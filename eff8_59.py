#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  170113 21:03:15
##################################
#8-59 用tracemalloc 来掌握内存的使用及泄漏情况
##################################

#Python的默认实现方式CPython中，内存管理是通过引用计数来处理的，当指向某个对象的全部引用都过期的时候，受引用的这个对象也能够同时得到清理。

#但实际上，程序还是会因为保留了过多的引用而导致内存耗尽，调试内存使用状况的第一种办法，是向内置的gc模块进行查询，请它列出垃圾收集器当前所知的每个对象。

import gc
found_objects = gc.get_objects()
print('%d objects before' % len(found_objects))

bar = []
for i in range(100):
    bar.append(object())
found_objects = gc.get_objects()
print('%d objects after' % len(found_objects))
for obj in found_objects[:3]:
    print(repr(obj)[:100])

#gc.get_objects的缺点是，它不能告诉我们这些对象到底是如何分配出来的。

#Python3.4推出了一个新的内置模块，名叫tracemalloc可以把某个对象与该对象的内存分配地点联系起来。下面用tracemalloc可以把某个对象与该对象的内存分配地点联系起来。下面用tracemalloc打印出导致内存用量增大的前三对象:

import tracemalloc
tracemalloc.start(10)
time1 = tracemalloc.take_snapshot()
for i in range(100):
    bar.append(object())
time2 = tracemalloc.take_snapshot()

stats = time2.compare_to(time1, 'lineno')

for stat in stats[:3]:
    print(stat)

#还可以打印出Python系统在执行每一个分配内存操作时，所具备的完整信息栈。

top = stats[0]
print('\n'.join(top.traceback.format()))

#Python的内存使用情况和内存泄漏情况是很难判断的。内置的tracemalloc模块提供了许多强大的工具，使得我们可以找出导致内存使用量增大的根源。

