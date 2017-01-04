#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  170104 11:11:10
##################################
#6-46 使用内置算法与数据结构
##################################

#Python的标准程序库里面，内置了各种算法与数据结构，以便开发者使用。这些常见的算法与数据结构，不仅执行速度比较快，而且还可以简化编程工作。所以，我们应该直接使用这些Python自带的功能，而不要重新去实现它们，以节省时间和精力。

#1.双向队列

#collections模块中的deque类，是一种双向队列(double-ended queue, 双端队列)这一特性，使得它非常适合用来表示先进先出(first-in-firsr-out, FIFO)的队列。

from collections import deque
fifo = deque()
fifo.append(1)
x = fifo.popleft()
print (x)

#2.有序字典

#标准的字典是无序的。也就是说，在拥有相同键值对的两个dict上面迭代，可能会出现不同的迭代顺序。标准的字典之所以会出现这种奇怪的现象，是由于其快速哈希表(fast hash table)的实现方式而导致的。

#collections模块中的OrderedDict类，是一种特殊的字典，它能够按照键的插入顺序，来保留键值对在字典中的次序。在OrderedDict上面根据键来迭代，其行为是确定的。这种确定的行为，可以极大地简化测试与调试工作。

from collections import OrderedDict
a = OrderedDict()
a['foo'] = 1
a['bar'] = 2
b = OrderedDict()
b['foo'] = 'red'
b['bar'] = 'blue'

for value1, value2 in zip(a.values(), b.values()):
    print (value1, value2)

#3.带有默认值的字典

#字典可用来保存并记录一些统计数据。但是，由于字典里面未必有我们要查询的那个键，所以在用字典保存计数器的时候，就必须要用稍微麻烦一些的方式，才能够实现这种简单的功能。
stats = {}
key = 'my_counter'
if key not in stats:
    stats[key] = 0
stats[key] += 1

#我们可以用collecions模块中的defaultdict类来简化上述代码。如果字典里面没有待访问的键，那么它就会把某个默认值与这个键自动关联起来。

from collections import defaultdict
stats = defaultdict(int)
stats['my_counter'] += 1

#4.堆队列（优先级队列）

#堆(heap)是一种数据结构，很适合用来实现优先级队列。heapq模块提供了heappush、heappop和namallest等一些函数，能够在标准的list类型之中创建堆结构。

#各种优先级的元素，都可以按任意顺序插入堆中。

from heapq import heappush, heappop, nsmallest

a = []
heappush(a, 5)
heappush(a, 3)
heappush(a, 7)
heappush(a, 4)

#只要访问堆中下标为0的那个元素，就总能够查出最小值。
print (a[0])

#在这种list上面调用sort方法之后，该list依然能够保持堆的结构。
print('Before:', a)
a.sort()
print('After: ', a)

#这些元素总是会按照优先级从高到低的顺序，从堆中弹出(数值较小的元素，优先级较高)

print(heappop(a), heappop(a), heappop(a), heappop(a))

#这些heapq操作所耗费的时间，与列表长度的对数成正比。如果在普通的Python列表上面执行相关操作，那么将会耗费线性级别的时间。

#5.二分查找

#在list上面使用index方法来搜索某个元素，所耗的时间会与列表的长度呈线性比例。

from time import time

x = list(range(10**6))
now = time()
i = x.index(991234)
print (i)
after = time()
print ('taken %.6f seconds' %(after - now))

#bisect模块中的bisect_left等函数，提供了高效的二分折半搜索算法，能够在一系列排好顺序的元素之中搜寻某个值。由bisect_left函数所返回的索引，表示待搜寻的值在序列中的插入点。

from bisect import bisect_left
now = time()
i=bisect_left(x,991234)
print (i)
after = time()
print ('taken %.6f seconds' %(after - now))

#二分搜索算法的复杂度，是对数级别的。这就意味着，用bisect来搜索包含一百万个元素的列表，与用index来搜索包含14个元素的列表，所耗的时间差不多。由此可见，这种对数级别的算法，要比线性级别的算法快很多。



#我们应该用Python内置的模块来描述各种算法和数据结构
#开发者不应该自己去重新实现那些功能，因为我们很难把它写好。

