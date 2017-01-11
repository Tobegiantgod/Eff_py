#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  170110 15:55:03
##################################
#7-52.用适当的方式打破循环依赖关系
##################################

#在和他人协作时，我们难免会写出相互依赖的模块。而有的时候，即使自己一个人开发程序，也仍然写出相互依赖的代码。两个模块互相import时很容易出现问题。

#定义下面两个模块

##dialog.py

import app
class Dialog(object):
    def __init__(self, save_dir):
        self.save_dir = save_dir

save_dialog = Dialog(app.prefs.get('save_dir'))
def show():
    pass


##app.py

import dialog
class Prefs(object):
    # ...
    def get(self, name):
        # ...

prefs = Prefs()
dialog.show()

#如果想从主程序里调用app.py模块，app.py模块会import dialog,此时当dialog想要import app 并使用prefs会出现错误，因为app.py里面的prefs类的定义尚未得到运行。

#有三种方法调整引入顺序，来避免循环依赖关系。

#1.调整引入顺序

#要介绍的第一个办法，是调整引入顺序。例如，我们可以把引入dialog模块所用的那条import语句，移动到app模块底部，也就是说，先等app模块的主要内容运行完毕，然后再引入dialog模块，这样AttributeError错误就会消失。

#app.py

class Prefs(object):
    # ...

prefs = Prefs()

import dialog #moved
dialog.show()
#这种办法是可行的。这个办法虽然能避开AttributeError错误，但是却与PEP8风格指南不符。而且有可能令整个模块都无法运作。

#2.先引入、再配置、最后运行

#在每个模块中，定义一个configure()函数，等其他模块都引入完毕之后，我们要在该模块上面调用一次configure，而这个configure函数，则会访问其他模块的属性，以便将模块的状态准备好。等所有模块都引入完毕，那些模块中的属性肯定已经定义好了，于是我们就可以放心地执行configure了。



##dialog.py

import app
class Dialog(object):
    def __init__(self, save_dir):
        self.save_dir = save_dir

save_dialog = Dialog()

def show():
    pass

def configure():
    save_dialog.save_dir = app.prefs.get('save_dir')

##app.py

import dialog

class Prefs(object):
    # ...
    def get(self, name):
        # ...
prefs = Prefs()

def configure():
    ....

#现在，我们在main模块中，分三个阶段来执行代码:首先引入所有模块，然后配置它们，最后执行程序中的第一个动作。

#main.py
import app
import dialog

app.configure()
dialog.configure()

dialog.show()

#这种方案在很多情况下都非常合适，而且方便开发者实现依赖注入(dependency injection)等模式。但是，有时我们很难从代码中清晰地提取出configure步骤。另外，在模块内部划分不同的阶段，也会令代码变得不易理解因为这样做，会把对象的定义对对象的配置分开。


#3.动态引入

#下面，我们采用动态引入方案，来重新定义dialog模块。这一次，dialog.show函数要等到运行的时候，才会引入app模块，而不是像原来那样，在初始化的时候就引入app模块。


##dialog.py

import app
class Dialog(object):
    def __init__(self, save_dir):
        self.save_dir = save_dir

save_dialog = Dialog()

def show():
    import app #Dynamic import
    save_dialog.save_dir = app.prefs.get('save_dir')
    # ...

##app.py

import dialog

class Prefs(object):
    # ...
    def get(self, name):
        # ...
prefs = Prefs()

dialog.show()

#该方案的实际效果，与刚才提到的先引入、再配置、最后运行的那套方案，是相似的。区别在于，本方案不需要从结构上面修改模块的定义方式和引入方式。我们只是把循环引入推迟到了程序真正需要访问其他模块的那一刻。而在那个时间点上，我们则可以确信，其他模块都已经彻底初始化好了。

#一般来说，我们还是尽量不要使用这种动态引入方案。因为import语句的执行开销，还没有小到可以忽略不计的地步。


#1.如果两个模块必须相互调用对方，方才能完成引入操作，那就会出现循环依赖现象，这可能导致程序在启动的时候崩溃。

#2.打破循环依赖关系的最佳方案，是把导致两个模块相互依赖的那部分代码，重构为单独的模块，并把它放在依赖树的底部。

#3.打破循环依赖关系的最简方案，是执行动态的模块引入操作，这样既可以缩减重构所花的精力，也可以尽量降低代码的复杂度。





































































