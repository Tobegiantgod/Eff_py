#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  161104 16:08:50
##################################
#3-23简单的接口应该接受函数，而不是类的实例
##################################


#Python有许多内置API都允许调入在传入函数，以定制其行为。API在执行的时候会通过这些挂钩(hook)函数，回调函数内的代码。

#例如list类型的sort方法接受可选的key参数，下面这段代码，用lambda表达式充当key挂钩，以便根据每个字的名字的长度来排序。

names=['Scorates', 'Archimedes', 'Plato', 'Aristotle']
names.sort(key=lambda x: len(x))
print(names)


#Python中的函数之所以能充当挂钩，原因就在于，它是一级对象，也就是说，函数与方法可以像语言中其他值那样传递和引用。

#例如，要定制defaultdict类的行为。这种数据结构允许使用者提供一个函数，以后在查询本字典时，如果里面没有待查的键，那就用这个函数为该键创建新值。当字典中没有待查的键时，此函数必须返回那个键所应具备的默认值。

#下面定义的这个挂钩函数会在字典里找不到待查询的键时打印一条信息，并返回0，以作为该键所对应的值。

from collections import defaultdict

def key_missing():
    print 'Key added'
    return 0

current={'zsr':100, 'lzw':88, 'lzj':77}

add_dict={'zsr':55, 'dc':77, 'lc':66}

result=defaultdict(key_missing,current)

print 'Before:',dict(result)
for key in add_dict:
    result[key] += add_dict[key]
print result
print 'After:',dict(result)


#现在要给defaultdict传入一个产生默认值的挂钩，并令其统计出该字典一共遇到了多少个缺失的键，一种实现方式是使用带状态的闭包，如下：

current={'zsr':100, 'lzw':88, 'lzj':77}

add_dict={'zsr':55, 'dc':77, 'lc':66}

def add_with_report(current, add_dict):
    addkey_count = [0]

    def key_missing():
        addkey_count[0] += 1
        return 0

    
    result=defaultdict(key_missing,current)

    for key in add_dict:
        result[key] += add_dict[key]
    
    return dict(result), addkey_count[0]


result, count = add_with_report(current, add_dict)

print result

print count

#把带状态的闭包函数有一个缺点，就是读起来要比无状态的函数难懂一些，可以使用定义一个小型的类，把需要追踪的状态封装起来:

current={'zsr':100, 'lzw':88, 'lzj':77}

add_dict={'zsr':55, 'dc':77, 'lc':66}

class CountMissing(object):
    def __init__(self):
        self.addkey_count = 0

    def countmissing(self):
        self.addkey_count += 1
        return 0

countmissing = CountMissing()

result = defaultdict(countmissing.countmissing, current)

for key in add_dict:
    result[key] += add_dict[key]

print dict(result)
print countmissing.addkey_count


#我们可以在python中定义名为__call__的特殊方法，使相关对象能够像函数那样得到调用：


current={'zsr':100, 'lzw':88, 'lzj':77}

add_dict={'zsr':55, 'dc':77, 'lc':66}

class CountMissing(object):
    def __init__(self):
        self.addkey_count = 0

    def __call__(self):
        self.addkey_count += 1
        return 0

countmissing = CountMissing()

result = defaultdict(countmissing, current)

for key in add_dict:
    result[key] += add_dict[key]

print dict(result)
print countmissing.addkey_count


"""
总结：

1.对于连接各种python组件的简单接口来说，通常应该给其直接传入函数，而不是先定义某个类，然后再传入该类的实例。

2.Python中函数和方法都可以像一级类那样引用，因此，它们与其他类型的对象一样，也能够放在表达式里面。

3.通过名为__call__的特殊方法，可以使类的实例能够像普通的Python函数那样得到调用，如果要用函数来保存状态，就应该定义新的类，并令其实现__call__方法，而不要定义带状态的闭包。

"""
















