#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  161208 14:11:55
##################################
#4-35 用元类来注解类的属性
##################################

#元类还有一个更有用处的功能，那就是可以在某个类刚定义好但是尚未使用的时候，提前修改或注解该类的属性。


class Field(object):
    def __init__(self, name):
        self.name = name
        self.internal_name = '_' + self.name

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')


#接下来定义表示数据行的Customer类，定义该类的时候，我们要为每个类属性指定对应的列名。

class Customer(object):
    first_name = Field('first_name')
    lirst_name = Field('last_name')


foo = Customer()
print('Before:', repr(foo.first_name), foo.__dict__)
foo.first_name = 'Euclid'
print('After:', repr(foo.first_name), foo.__dict__)

#上述Customer类中,对于属性的赋值有点重复，通过元类来简化

class BetterField(object):
    def __init__(self):
        #These will be assigned by the metaclass
        self.name = None
        self.internal_name = None
    
    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')
class Meta(type):
    def __new__(meta, name, bases, class_dict):
        for key, value in class_dict.items():
            if isinstance(value, BetterField):
                value.name = key
                value.internal_name = '_' + value.name
        cls = type.__new__(meta, name, bases, class_dict)
        return cls

class DatabaseRow(object, metaclass=Meta):
    pass

class BetterCustomer(DatabaseRow):
    first_name = BetterField()
    last_name = BetterField()

#新的BetterCustomer类的行为与旧的Customer类相同
foo = BetterCustomer()
print('Before:', repr(foo.first_name), foo.__dict__)
foo.first_name = 'Euclid'
print('After:', repr(foo.first_name), foo.__dict__)









