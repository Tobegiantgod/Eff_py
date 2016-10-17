#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  160905 20:13:05
#    Desc   :  
#
##了解如何在闭包里使用外围作用域中的变量

def sort_priority(values,group):
    def helper(x):
        if x in group:
            return (0,x)
        return (1,x)
    values.sort(key=helper)

numbers=[8,3,1,2,5,4,7,6]
group={2,3,5,7}
sort_priority(numbers,group)
print(numbers)

#以上函数能够正常运行，是基于下列三个原因：
   #1.Python支持闭包
   #2.Python的函数式一级对象，也就是说，我们可以直接引用函数、把函数赋给变量、把函数当成参数传给其他函数。
   #3.Python使用特殊的规则来比较两个元组


def sort_priority2(numbers,group):
    found=False
    def helper(x):
        if x in group:
            found=True
            return(0,x)
        return (1,x)
    numbers.sort(key=helper)
    return found

found=sort_priority2(numbers,group)
print('Found:',found)
print(numbers)

#在函数里添加了found变量用于判断是否有匹配的对象，但是found的值并没有改变，因为在helper（）里对found赋值并没有改变上级变量域的found值，而是相当于在helper（）内又重新定义了一个变量found


#可以使用下面的方式达成想要的效果

def sort_priority3(numbers,group):
    found=[False]
    def helper(x):
        if x in group:
            found[0]=True
            return (0,x)
        return (1,x)
    number.sort(key=helper)
    return found[0]

#列表本身是可供修改的，所以获取到这个found列表后，我们就可以在闭包里面通过found[0]=True语句，来修改found的状态
