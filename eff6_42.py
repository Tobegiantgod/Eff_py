#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  161228 14:57:59
##################################
#6-42.用functools.wraps定义函数修饰器
##################################

#Python用特殊语法来表示修饰器(decorator),这些修饰器可以用来修饰函数。这使得开发者可以在修饰器里面访问并修改原函数的参数及返回值，以实现约束语义(enforce semantics)、调试程序、注册函数等目标。

#下面定义一个打印所修饰的函数输入和输出值的修饰器

def trace(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print('%s(%r, %r) -> %r' % (func.__name__,args,kwargs,result))
        return result
    return wrapper

@trace
def fibonacci(n):
    """Return the n-th Fibonacci number"""
    if n in (0,1):
        return n
    return (fibonacci(n-2)+fibonacci(n-1))

fibonacci(3)

#上面这个修饰器虽然可以正常运作，但却会产生一种我们不希望看到的副作用。也就是说，修饰器所返回的那个值，其名称会和原来的函数不同，它现在不叫fibonacci了。

print(fibonacci)

#这样会使内置的help函数失效,它会显示trace内部定义的wrapper函数，而不是fibonacci。

#help(fibonacci)

#这个问题可以，可以使用内置的functools模块中名为wraps的辅助函数来解决。wraps本身也是修饰器，它可以帮助开发者编写其他修饰器。将wraps修饰器运用到wrapper函数之后，它就会把与内部函数相关的重要元数据全部复制到外围函数。

from functools import wraps

def trace_better(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print('%s(%r, %r) -> %r' % (func.__name__,args,kwargs,result))
        return result
    return wrapper


@trace_better
def fibonacci(n):
    """Return the n-th Fibonacci number"""
    if n in (0,1):
        return n
    return (fibonacci(n-2)+fibonacci(n-1))

fibonacci(3)

print(fibonacci)


#Python为修饰器提供了专门的语法，它使得程序在运行的时候，能够用一个函数来修改另一个函数。内置的functools模块提供了名为wraps的修饰器，开发这在定义自己的修饰器时，应该用wraps对其做一些处理，以避免一些问题。


