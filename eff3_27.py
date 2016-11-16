#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  161116 15:16:29
##################################
#3-27 多用public属性，少用private属性
##################################

#Python编译器无法严格保证private字段的私密性，只是重命名存储了它。

#应该多用protected属性，并在文档中把这些字段的合理用法告诉子类的开发者，而不要试图用private属性来限制子类访问这些字段。

#只有当子类不受控制时，才可以考虑用private属性来避免名称冲突。


