#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  161117 20:14:44
##################################
#3-28 继承collections.abc以实现自定义的容器类型
##################################

#大部分的Python编程工作，其实都是在定义类。Python中的每一个类，从某种程度上来说都是容器，它们都封装了属性与功能。Python也直接提供了一些数据所用的内置容器类型，例如，list、tuple、set、dictionary。

#如果要设计用法比较简单的序列，可以直接继承Python内置的list类型。例如，要创建一种自定义的列表类型，并提供统计各元素出现频率的方法：

class FrequencyList(list):
    def __init__(self, members):
        super(FrequencyList, self).__init__(members)

    def frequency(self):
        counts = {}
        for item in self:
            counts.setdefault(item, 0)
            counts[item] += 1
        return counts

foo = FrequencyList(['a', 'b', 'a', 'c', 'b', 'a', 'd'])
print('Length is', len(foo))
foo.pop()
print('After pop:', repr(foo))
print('Frequency:', foo.frequency())


#现在，假设要编写这么一种对象：它本身虽然属于list子类，但是用起来却和list一样，也可以通过下标访问其中的元素。例如，我们要令下面这个表示二叉树节点的类，也能够像list或tuple等序列那样来访问：

class BinaryNode(object):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

#用下标访问序列中的元素时bar[0],Python会把访问代码转译为:bar.__getitem__(0)

class IndexableNode(BinaryNode):
    def _search(self, count, index):
        stack=[]
        found=None
        stack += [self]
        while count <= index and stack:
            found=stack.pop()
            if found.right != None:
                stack += [found.right]
            if found.left != None:
                stack += [found.left]
            count += 1                        
        return (found, count)


    def __getitem__(self, index):
        found,_= self._search(0, index)
        if not found:
            raise IndexError('Index out of range')
        return found.value


tree = IndexableNode(10, left = IndexableNode(5,left = IndexableNode(2),right = IndexableNode(6, right = IndexableNode(7))), right=IndexableNode(15, left = IndexableNode(11)))



print('Index 0 = %d' % tree[0])
print('Index 3 = %d' % tree[3])

                                                            
