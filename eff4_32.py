#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  161201 15:59:04
##################################
#4-32 用__getattr__、__getarribute和__setattr__实现按需生成的属性
##################################
#Python语言提供了一些挂钩，使得开发者很容易就能编写出通用的代码，以便将多个系统黏合起来。

#如果类定义了__getattr__，同时系统在该类对象的实例字典中又找不到待查询的属性，那么，系统就会调用这个方法。

class LazyDB(object):
    def __init__(self):
        self.exists = 5

    def __getattr__(self, name):
        value = 'Value for %s ' % name
        setattr(self, name ,value)
        return value

#下面访问data对象所缺失的foo属性。这会导致Python调用刚才定义的__getattr__方法，从而修改实例的__dict__字典：

data = LazyDB()
print('Before:', data.__dict__)
print('foo', data.foo)
print('After:', data.__dict__,'\n')


#为了把程序对__getattr__的调用行为记录下来。为了避免无限递归，我们需要在LoggingLzayDB子类里面通过super().__getattr__()来获取真正的属性值。

class LoggingLazyDB(LazyDB):
    def __getattr__(self, name):
        print('Called __getattr__(%s)' % name)
        return super().__getattr__(name)

data = LoggingLazyDB()
print('exists:', data.exists)
print('foo', data.foo)
print('foo', data.foo,'\n')

#Python中程序每次访问对象的属性时，都会调用另一个挂钩，也就是__getattribute__，及时属性字典里面已经有了该属性，也依然会触发__getattribute__方法。这样就可以在每次访问属性时，检查全局事物状态。

class ValidatingDB(object):
    def __init__(self):
        self.exists = 5

    def __getattribute__(self, name):
        print('Called __getattribute__(%s)' % name)
        try:
            return super().__getattribute__(name)
        except AttributeError:
            value = 'Value for %s' % name
            setattr(self, name, value)
            return value


data = ValidatingDB()
print('exists:', data.exists)
print('foo:', data.foo)
print('foo:', data.foo,'\n')

#使用内置的hasattr函数来判断对象是否已经拥有了相关属性，和使用内置的getattr函数来获取属性值。这些函数会在实例字典中搜索待查询的属性。然后再调用__getattr__。


data = LoggingLazyDB()
print('Before', data.__dict__)
print('foo exists', hasattr(data, 'foo'))
print('After', data.__dict__)
print('foo exists', hasattr(data, 'foo'),'\n')


#上述__getattr__方法只调用了一次。反之，如果本类实现的是__getattribute__方法，那么每次在对象上面调用hasattr或getattr函数时，此方法都会执行。


data = ValidatingDB()
print('Before', data.__dict__)
print('foo exists', hasattr(data, 'foo'))
print('After', data.__dict__)
print('foo exists', hasattr(data, 'foo'),'\n'  )


#只要对实例的属性赋值，无论是直接赋值，还是通过内置的setattr函数赋值，都会触发__setattr__方法。

class SavingDB(object):
    def __setattr__(self, name, value):
        print('Call __setattr__(%s, %r)' % (name, value))
        super().__setattr__(name, value)

data = SavingDB()
print('Before: ', data.__dict__)
data.foo = 5
print('After: ', data.__dict__)
data.foo = 7
print('Finally:', data.__dict__)


#通过__getattr__和__setattr__,我们可以用惰性的方式来加载并保存对象的属性。

#要理解__getattr__与__getattribute__区别：前者只会在待访问的属性缺失时触发，而后者则会在每次访问属性时触发。

#如果要在__getattribute__和__setattr__方法中访问实例属性，那么应该直接通过super()（也就是object类的同名方法）来做，以免无限递归。





















