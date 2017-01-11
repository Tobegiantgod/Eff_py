#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  170111 15:23:12
##################################
#8-54 考虑用模块级别的代码来配置不同的部署环境
##################################

#本demo不能作为python程序直接运行!

#python开发时，我们一般在自己的开发环境中进行开发，但我们真正需要产品运行的环境很多时候都与我们的开发环境不同。

#解决此类问题的最佳方案，是在程序启动的时候，覆写其中的某些部分，以便根据部署环境，来提供不同的功能。

#例如，我们可能会编写两份不同的__main__文件，一份用于生产环境，另一份用于开发环境。

# dev_main.py
TESTING = True
import db_connection
db = db_connection.Database

# prod_main.py
TESTING = False
import db_connection
db = db_connection.Database

# db_connection.py
import __main__
class TestingDatabase(object):
    # ...

class RealDatabase(object):
    # ...

if __main__.TESTING:
    Database = TestingDatabase
else:
    Database = RealDatabase

#这个范例的关键点在于：出现在模块范围之内，但又不包含在函数或方法之中的那些代码，实际上就是普通的Python代码。于是，我们可以在这种模块级的代码中，用if语句来决定本模块应该如何定义相关的变量。


