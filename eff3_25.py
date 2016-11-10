#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  161109 16:52:13
##################################
#3-25 用super初始化父类
##################################


#初始化父类的传统方式，是在子类里用子类实例直接调用父类的__init__方法

class MyBaseClass(object):
    def __init__(self, value):
        self.value=value

class MyChildClass(MyBaseClass):
    def __init__(self):
        MyBaseClass.__init__(self, 5)

    def read(self):
        value=self.value
        return value

A=MyChildClass()
print A.read()



#如果子类受到了多层继承的影响，那么直接调用超类的__init__方法，可能会产生无法预知的行为。

#在子类里调用__init__的问题之一，是它的调用顺序并不固定。例如，下面定义两个超类，它们都操作名为value的实例字段：

class TimesTwo(object):
    def __init__(self):
        self.value *= 2

class PlusFive(object):
    def __init__(self):
        self.value += 5


class OneWay(MyBaseClass, TimesTwo, PlusFive):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)


foo = OneWay(5)
print ('First ordering is (5 * 2) + 5', foo.value)

#下面这个类，用另一种顺序来定义它所继承的各个超类：

class AnotherWay(MyBaseClass, PlusFive, TimesTwo):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)

foo = AnotherWay(5)
print ('Second ordering  is still (5 * 2) + 5', foo.value)

#上述表示改变超类的继承顺序，并没有改变超类构造器的调用顺序。


#还有一个问题发生在钻石继承中。如果子类继承自两个单独的超类，而那个两个超类又继承自同一个公共基础类，那就构成了钻石继承体系。

#例如下面定义两个子类，都继承于MyBaseClass：

class TimesThree(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value *= 3

class PlusSix(MyBaseClass):
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value += 6


#然后定义一个子类，同时继承上面这两个类，这样MyBaseClass就成了钻石顶部的那个公共基类

class ThisWay(TimesThree, PlusSix):
    def __init__(self, value):
        TimesThree.__init__(self, value)
        PlusSix.__init__(self, value)

foo = ThisWay(5)

print('Should be (5*3) + 6 = 21 but is ', foo.value)


#上述在调用第二个超类构造器，也就是PlusTwo.__init__的时候，它会再度调用MyBaseClass.__init__,从而导致self.value重新变成5。

#Python增加了内置函数super,并且定义了方法解析顺序(method resolution order,MRO),以解决这一问题。MRO以标准的流程来安排超类之间的初始化顺序（例如，深度优先，从左至右),它也保证钻石顶部那个公共基础类的__init__方法只会运行一次。


class TimesThreeCorrect(MyBaseClass):
    def __init__(self, value):
        super(TimesThreeCorrect, self).__init__(value)
        self.value *= 3

class PlusSixCorrect(MyBaseClass):
    def __init__(self,value):
        super(PlusSixCorrect, self).__init__(value)
        self.value += 6


class ThisWayCorrect(PlusSixCorrect, TimesThreeCorrect):
    def __init__(self,value):
        super(ThisWayCorrect, self).__init__(value)



foo = ThisWayCorrect(5)

print('Should be (5 * 3) + 6 = ', foo.value)

#可以通过名为mro的类方法来查询类的MRO顺序

from pprint import pprint

pprint (ThisWayCorrect.mro())


#在python2中需要注意，super语句写起来有点麻烦。我们必须指定当前所在的类和self对象，而且还要指定相关的方法名称（通常是__init__)以及那个方法的参数。

























