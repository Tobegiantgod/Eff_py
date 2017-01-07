#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  170106 10:58:55
##################################
#7-50 用包来安装模块，并提供稳固的API
##################################

#包，是一种含有其他模块的模块

#在大多数情况下，我们会给目录中放入名为__init__.py的空文件，并以此来定义包。只要目录里有__init__.py,我们就可以采用相对于该目录的路径，来引入目录中的其他Python文件。例如，某个程序的目录结构如下

"""
eff7_50.py
mypackge/__init__.py
mypackge/models.py
mypackge/utils.py

"""
#为了以相对的方式引入utils模块，我们需要把上级模块的绝对名称，写在引入语句的from部分之中，也就是说，我们要在from关键字右侧，写出与mypackge包相对应的目录名。

from mypackage import utils

#凡是通过import语句引入的内容，都可以用as子句来改名，即使引入整个模块，我们也依然能用as为其改名。避免名称出现重复被覆盖。

#2.稳固的API

#Python包的第二种用途，是为了外部使用者提供严谨而稳固的API

#在Python程序中，我们可以为包或模块编写名为__all__的特殊属性，以减少其暴露外围API使用者的信息量。__all__属性的值，是一份列表，其中的每个名称，都作为本模块的一条公共API，导出给外部代码。

#如果外部用户以from foo import *的形式来使用foo模块，那么只有foo.__all__中列出的那些属性，才会从foo中引入。若是foo模块没有提供__all__，则只会引入public属性，也就是说，只会引入不以下划线开头的那些属性。


#在mypackge中，对__all__属性进行处理后，API使用者就可以直接引入mypackage,而不用再访问具体的内部模块了:

from mypackage import *

a = Projectile(1.5 ,5)
b = Projectile(4, 1.7)
after_a, after_b = simulate_collision(a, b)

