#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  161222 16:46:14
##################################
#5-38 在线程中使用Lock来防止数据竞争
##################################

#Python使用全局解释器锁(GIL)机制使得Python线程无法平行地运行在多个CPU核心上面，那么也会对程序中的数据结构起到保护锁定作用，例如列表或者字典。

#但是实际上GIL并不会保护开发者自己所编写的代码。如果开发者尝试从多个线程中同时访问某个对象，那么上述情形就会引发危险的结果。

#假如我们要编程统计一个事务，新建一个Counter类：

from threading import Thread, Lock

class Counter(object):
    def __init__(self):
        self.count = 0

    def increment(self, offset):
        self.count += offset


#在查询传感器读数的过程中,会发生阻塞式I/O操作，所以，我们要给每个传感器分配它自己的工作线程(worker thread)。

def worker(sensor_index, how_many, counter):
    for _ in range(how_many):
        counter.increment(1)

#下面定义的这个run_threads函数，会为每个传感器启动一条工作线程，然后等待它们完成各自的采样工作：
    
def run_threads(func, how_many, counter):
    threads = []
    for i in range(5):
        args = (i, how_many, counter)
        thread = Thread(target=func, args=args)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

#平行地执行这5条线程。我们觉得: 这个程序的结果，应该是非常明确的。

how_many = 10**5
counter = Counter()
run_threads(worker, how_many, counter)
print('Counter should be %d, found %d' % (5*how_many, counter.count))

#但是，看到输出信息之后，我们却发现，它与正确的结果相差很远。因为为了保证所有线程都能够公平地执行，Python解释器会给每个线程分配大致相等的处理器时间。为了达成这样的分配策略，Python系统可能当某个线程正在执行的时候，将其暂停(suspend),然后使另一个线程继续往下执行。问题就在于，开发者无法准确获知Python系统会在何时暂停这些线程。


#我们可以Python内置的threading模块里提供的Lock类，该类相当于互斥锁(也叫做互斥体）


class LockingCounter(object):
    def __init__(self):
        self.lock = Lock()
        self.count = 0

    def increment(self, offset):
        with self.lock:
            self.count += offset

counter = LockingCounter()
run_threads(worker, how_many, counter)
print('Counter should be %d, found %d' % (5 * how_many, counter.count))


