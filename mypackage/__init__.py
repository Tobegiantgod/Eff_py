#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  170106 11:17:24
##################################
#__init__.py
##################################
__all__ = []
from . models import *
__all__ += models.__all__
from . utils import *
__all__ += utils.__all__
#由于mypackage内部的那些模块，都已经提供了__all__属性，所以，我们只需要把内部模块中的所以内容都引入进来，并据此更新__init__。py的__all__属性，即可把mypackage的public接口适当地公布给外界。



