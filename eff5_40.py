#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  161226 16:33:31
##################################
#5-40 考虑用协程来并发地运行多个函数
##################################
#Python可以使用线程来运行多个函数，使这些函数看上去好像是在同一时间得到执行。

#然而线程有三个显著的特点。

#一.为了确保数据安全，我们必须使用特殊的工具来协调这些线程。使得多线程代码要比单线程的过程式代码更加难懂，维护更加困难。

#二.线程需要占用大量内存，每个正在执行的线程，大约占据8MB内存。

#三.线程启动时的开销比较大。不停的启动多线程来执行函数时，会拖慢整个程序的速度。


#Python的协程可以避免上述问题，它使得Python程序看上去好像是在同时运行多个函数。协程的实现方式，实际上是对生成器的一种扩展。

#协程的工作原理是这样的：每当生成器函数执行到yield表达式的时候，消耗生成器的那段代码，就通过send方法给生成器回传一个值。而生成器在收到了经由send函数所传进来的这个值之后，会将其视为yield表达式的执行结果。

def my_coroutine():
    while True:
        received = yield
        print('Recevied:', received)

it =my_coroutine()
next(it)
it.send('First')
it.send('Second')

#我们要编写一个生成器协程，并给它依次发送许多数值，而协程每收到一个数值，就会给出当前所统计到的最小值。

import random

def minimize():
    current = yield
    while True:
        value = yield current
        current = min(value, current)

it = minimize()
next(it)
for _ in range(10):
    print(it.send(random.randint(10,100)))

#生成器函数似乎会一直运行下去，每次在它上面调用send之后，都会产生新的值与线程类似，协程也是独立函数，它可以消耗由外部环境所传进来的输入数据，并产生相应的输出结果。


