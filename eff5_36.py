#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  161219 19:29:41
##################################
#5-36用subprocess模块来管理子进程
##################################
#
#并发(concurrency)的意思是指，计算机似乎是在同一时间做着很多不同的事。

#并行(parallelism)的意思则是说，计算机确实(acutally)是在同一时间做着很多不同的事。

#并发与并行的关键区别，就在于能不能提速（speedup)。

#用Python语言编写并发的程序，是比较容易的。通过系统调用、子进程和C语言扩展等机制，也可以用Python平行地处理一些事务。但是，要想使并发式的Python代码以真正平行的方式来运行，却相当困难。

#对当今的Python来说，最好用且最简单的子进程管理模块，应该是内置的subprocess模块。

#下面这段代码，用Popen构造器来启动程序。然后用communicate方法读取子进程的输出信息，并等待其终止。
import subprocess

proc = subprocess.Popen(['echo', 'Hello from the child!'], stdout=subprocess.PIPE)

out, err = proc.communicate()

print(out.decode('utf-8'))

#可以一边定期查询子进程的状态，一边处理其他事务。

proc = subprocess.Popen(['sleep', '0.3'])
while proc.poll() is None:
    print ('Working..')
    print ('doing other thing')
    # ...
print('Exit status', proc.poll())

#把子进程从父进程中剥离(decouple,解耦），意味着父进程可以随意运行很多条平行的子进程。为了实现这一点，我们可以先把所有的子进程都启动起来。
from time import time

def run_sleep(period):
    proc = subprocess.Popen(['sleep', str(period)])
    return proc

start = time()
procs = [] 
for _ in range(10):
    proc = run_sleep(0.1)
    procs.append(proc)

for proc in procs:
    proc.communicate()

end = time()
print('Finished in %.3f seconds' % (end - start))


