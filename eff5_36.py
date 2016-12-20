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

#开发者也可以向子进程输送数据，然后获取子进程的输出信息。这使得我们可以利用其他程序来平行地执行任务。

import os

def run_openssl(data):
    env = os.environ.copy()
    env['password'] = b'\xe24U\n\xd0Q13S\x11'
    proc = subprocess.Popen(['openssl', 'enc' ,'-des3', '-pass', 'env:password'], env = env,stdin = subprocess.PIPE, stdout = subprocess.PIPE)
    proc.stdin.write(data)
    proc.stdin.flush() #Ensure the child gets input
    return proc

procs = []
for _ in range(3):
    data = os.urandom(10)
    proc = run_openssl(data)
    procs.append(proc)

for proc in procs:
    out, err = proc.communicate()
    print(out[-10:])


#此外，我们还可以像UNIX管道那样，用平行的子进程来搭建平行的链条，所谓搭建链条(chain),就是把第一个子进程的输出，与第二个子进程的输入联系起来，并以此方式继续拼接下去。下面这个函数，可以启动一个子进程，而该进程会用命令行式的md5工具来处理输入流中的数据：

def run_md5(input_stdin):
    proc = subprocess.Popen(['md5sum'], stdin = input_stdin, stdout=subprocess.PIPE)
    return proc

#现在，启动一套openssl进程，以便加密某些数据，同时启动另一套md5进程，以便根据加密后的输出内容来计算其哈希码（hash, 杂凑码）

input_procs = []
hash_procs = []
for _ in range(3):
    data = os.urandom(10)
    proc = run_openssl(data)
    input_procs.append(proc)
    hash_proc = run_md5(proc.stdout)
    hash_procs.append(hash_proc)

for proc in input_procs:
    proc.communicate()
for proc in hash_procs:
    out, err = proc.communicate()
    print(out.strip())

#如果你担心子进程一直不终止，或担心它的输入管道及输出管道由于某些原因发生了阻塞，那么可以给communicate方法传入timeout参数。该子进程若在指定时间段内没有给出响应，communicate方法则会抛出异常，我们可以在处理异常的时候，终止出现意外的子进程。

proc = run_sleep(10)
try:
    proc.communicate(timeout = 0.1)
except subprocess.TimeoutExpired:
    proc.terminate()
    proc.wait()

print('Exit status', proc.poll())

#可以用subprocess模块运行子进程，并管理其输入流与输出流。
#Python解释器能够平行地运行多条子进程，这使得开发者可以充分利用CPU的处理能力。
#可以给communicate方法传入timeout参数，以避免子进程死锁或失去响应(hanging, 挂起）。


