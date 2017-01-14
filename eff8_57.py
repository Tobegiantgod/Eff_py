#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  170113 15:21:09
##################################
#8-57 考虑用pdb实现交互调试
##################################

#编写程序的时候，我们总会遇到代码中的bug。print函数可以帮我们追查到很多问题的来源。python的内置的交互调试器(interactive debugger)具有更强大的调试功能。我们只需引入内置的pdb模块，并运行其set_trace函数，即可触发调试器。

def complex_func(a, b, c):
    a=a
    b=b
    c=c
    import pdb; pdb.set_trace()
    return a ,b ,c

print (complex_func(1,2,4))
print (complex_func(2,4,5))


#我们可以修改Python程序，在想要调试的代码上方直接加入import pdb;pdb.set_trace()语句，以触发互动调试器。Python调试器也是一个完整的Python提示符界面，我们可以检视并修改受测程序的状态。


