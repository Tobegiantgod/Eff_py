#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  161227 16:24:50
##################################
#5-41 考虑用concurrent.futures来实现真正的平行计算
##################################

#编写Python程序时，我们可能遇见性能问题，即使优化来的代码，程序也依然有可能运行得很慢，无法满足我们对执行速度的要求。目前的计算机，其CPU核心数越来越多，于是，我们可以考虑通过平行计算(parallelism)来提升性能。

#但Python的全局解释器锁(GIL)使得我们没有办法用线程实现真正的平行计算。如果用C语言重写代码，是有很大代价的。短小而易读的Python代码，会变成冗长而费解的C代码。

#我们可以试着通过内置的concurrent.futures模块，来利用另一个名叫multiprocessing内置模块。从而实现这种需求。该做法会以子进程的形式，平行地运行多个解释器，从而令Python程序能够利用多核心CPU来提升速度。由于子进程与主解释器相分离，所以它们的全局解释器锁也是相互独立的。

#例如，我们现在要编写一个运算量很大的Python程序，并要在该程序中充分利用CPU的多个内核。采用查找两数最大公约数的算法，来演示这种编程方式。
from time import time

def gcd(pair):
    a, b = pair
    low = min(a, b)
    for i in range(low, 0, -1):
        if a % i == 0 and b % i == 0:
            return i

#由于我们没有做平行计算，所以程序会依次用gcd函数来求各组数字的最大公约数，这将导致程序的运行时间随着数据量的增多而变长。

numbers = [(1963309, 2265973),(2030677, 3814172),(1551645, 2229620), (2039045, 2020802)]

start = time()
results = list(map(gcd, numbers))
end = time()
print('Took %.3f seconds' % (end - start))

#用多条Python线程来改善上述程序，是没有效果的，因为全局解释器锁(GIL)使得Python无法在多个CPU核心上面平行地运行这些线程。下面这个程序，借助concurrent.futures模块来执行与刚才相同的运算，它使用ThreadPoolExecutor类及两个工作线程来实现(max_workers表示工作线程的数量，此参数应该与CPU的核心数同):
from concurrent.futures import ThreadPoolExecutor

start = time()
pool = ThreadPoolExecutor(max_workers=2)
results = list(pool.map(gcd, numbers))
end = time()
print('Took %.3f seconds' % (end - start))

#线程启动的时候，是有一定开销的，与线程池进行通信，也会有开销，所以上面这个程序运行得比单线程版本还要慢。

#然而神奇的是:我们只需要改动一行代码，就可以提升整个程序的速度。只要把ThreadPoolExecutor换成concurrent.futures模块里的ProcessPoolExecutor,程序的速度就上去了。
from concurrent.futures import ProcessPoolExecutor
start = time()
pool = ProcessPoolExecutor(max_workers=4)
results = list(pool.map(gcd, numbers))
end = time()
print('Took %.3f seconds' % (end - start))

#实际上，为了实现平行计算，multiprocessing模块和ProcessPoolExecutor在幕后做了大量的工作。如果改用其他编程语言来写，那么开发者只需要一把同步锁或一项原子操作，就可以把线程之间的通信过程协调好，而在Python语言中，我们必须使用开销较高的multiprocessing模块。multiprocessing的开销之所以比较大，原因就在于:主进程和子进程之间，必须进行序列化和反序列化操作，而程序中的大量开销，正是由这些操作所引发的。



#若想利用强大的multiprocessing模块，最恰当的做法，就是通过内置的concurrent.futures模块及其ProcessPoolExecutor类来使用它。

#multiprocessing模块所提供的那些高级功能，都特别复杂，所以开发者尽量不要直接使用它们。




