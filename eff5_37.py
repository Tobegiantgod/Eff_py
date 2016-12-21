#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  161221 16:16:46
##################################
#5-37 可以用线程来执行阻塞式I/O,但不要用它做平行计算
##################################

#标准的Python实现叫做CPython。CPython分两步来运行Python程序。首先，把文本形式的源代码解析并编译成字节码。然后，用一种基于栈的解释器来运行这份字节码。执行Python程序时，字节码解释器必须保持协调一致的状态。

#Python采用GIL(global interpreter lock,全局解释器锁）机制来确保这种协调性。


#GIL 有一种非常显著的负面影响。用C++或Java等语言写程序时，可以同时执行多条线程，以充分利用计算机所配备的多个CPU核心。Python程序尽管也支持多线程，但由于受到GIL保护，所以同一时刻，只有一条线程可以向前执行。这就意味着，如果想利用多线程做平行计算(parallel computation),并希望借此为Python程序提速，那么结果会非常令人失望。


#Python支持多线程的第二条理由，是处理阻塞式的I/O操作，Python在执行某些系统调用时，会触发此类操作。Python多线程可以使Python程序与这些耗时的I/O操作隔离开。


#例如，我们要通过串行端口(serial port, 简称串口)发送信号，以便远程控制一架直升飞机。采用一个速度较慢的系统调用(也就是select)来模拟这项活动。该函数请求操作系统阻塞0.1秒，然后把控制权交还给程序，这种效果与通过同步串口来发送信号是类似的。

import select
from time import time
def slow_systemcall():
    select.select([],[],[],0.1)

start = time()
for _ in range(5):
    slow_systemcall()
end = time()
print('Took %.3f seconds'%(end - start))

#上面这种写法的问题在于：主程序在运行slow_systemcall函数的时候，不能继续向下执行，程序的主线程会卡在select系统调用那里。


#下面这段代码，把多个slow_systemcall调用分别放到多个线程中执行，这样写，使得程序既能够与多个串口通信，又能够同时在主线程里执行所需的计算。
from threading import Thread

start = time()
threads = []
for _ in range(5):
    thread = Thread(target = slow_systemcall)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
end = time()

print('Took %.3f seconds' %(end - start))

#通过Python线程，我们可以平行地执行多个系统调用，这使得程序能够在执行阻塞式I/O操作的同时，执行一些运算操作。




