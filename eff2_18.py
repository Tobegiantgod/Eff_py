#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  161020 15:22:57
##################################
#
#第十八条：用数量可变的的位置参数减少视觉杂讯
#
##################################


#在定义函数时当我们能够确定输入的参数个数比较少时，可以使用函数接受*arg式的变长参数，可以简化程序员的编程工作，并使得代码更加易读。

def log(message, *values):
    if not values:
        print(message)
    else:
        value_str=','.join(str(x) for x in values)
        print('%s: %s' % (message,value_str))

favorities=[9,19,11,02]
log('Favorite colors',*favorities)

#注意：对生成器要尽量避免使用*作为位置参数传递，如果使用*传递生成器，python就必须把生成器完整的迭代一遍，并把生成器所生成的每一个值，都放入元组中。这可能会消耗大量内存，导致程序崩溃。
