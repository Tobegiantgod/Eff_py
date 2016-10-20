#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  160909 11:23:20
##################################
#
##考虑用生成器来改写直接返回列表的函数


#如果函数要产生一系列结果，那么最简单的做法就是把这些结果都放在一份列表里，并将其返回给调用者。

#如下，将字符串中每个词的首字母提取出来，存在列表里并返回：

mystr="I want study hard for our better lives"


def index_words(text):
    result=[text[0]]
    for index,letter in enumerate(text):
        if letter == ' ':
            result.append(text[index+1])
    return result

result=index_words(mystr)
print result

##以上方法有两个问题，第一个问题是，这段代码写得有点拥挤。每次找到新的结果都要调用append方法；第二个问题是，它在返回前，要先把所有的结果放在列表里面。如果输入量非常大，那么程序就有可能耗尽内存并崩溃。
##所以用生成器函数yield改写以上方法，调用生成器方法时，它并不会真正运行，而是会返回迭代器，函数的执行所耗的内存，由单行输入的最大字符数来界定的。

def index_words_iter(text):
    yield text[0]
    for index,letter in enumerate(text):
        if letter == ' ':
            yield text[index+1]

result=list(index_words_iter(mystr))
print result
