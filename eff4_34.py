#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  161207 16:37:59
##################################
#4-34 用元类来注册子类
##################################

#元类还有一个用途，就是在程序中自动注册类型。对于需要反向查找（reverse,简称反查）的场合，这种注册操作是很有用的，它使我们可以在简单的标识符与对应的类之间，建立映射关系。

#下面这段代码，定义了一个通用的基类，它可以记录程序调用本类构造器时所用的参数，并将其转换为JSON字典:

import json

class Serializable(object):
    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({'args': self.args})

class Point2D(Serializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point2D(%d, %d)' % (self.x, self.y)

point = Point2D(2, 5)
print('Object:    ', point)
print('Serialized:', point.serialize())



#现在，我们需要对这种JSON字符串执行反序列化(deserialize)操作，并构建出该字符串所表示的Point2D对象。下面定义的这个Deserialize类，继承自Serializable,它可以把Serializable所产生的JSON字符串还原为Python对象：

class Deserializable(Serializable):
    @classmethod
    def deserialize(cls, json_data):
        params = json.loads(json_data)
        return cls(*params['args'])

class BetterPoint2D(Deserializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return 'BetterPoint2D(%d, %d)' % (self.x, self.y)

point = BetterPoint2D(5, 4)
print(point.__class__,point.__class__.__name__)
print('Before:     ', point)
data = point.serialize()
print('Serialized: ', data)
after = BetterPoint2D.deserialize(data)
print('After:      ', after)


#这中方案的缺点是，我们必须提前知道序列化的数据是什么类型(例如，是Point2D或BetterPoint2D等),然后才能对其做反序列化操作，理想方案是只需要一个公共的反序列化函数，就可以将任意的JSON字符串还原成相应应的Python对象。


#为此，我们可以把序列化对象的类名写到JSON数据里面。

class BetterSerializable(object):
    def __init__(self, *args):
        self.args = args
    
    def serialize(self):
        return json.dumps({
            'class': self.__class__.__name__,
            'args' : self.args,
            })
    
registry = {}

def register_class(target_class):
    registry[target_class.__name__] = target_class

def deserialize(data):
    params = json.loads(data)
    name = params['class']
    target_class = registry[name]
    return target_class(*params['args'])

class EvenBetterPoint2D(BetterSerializable):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.x = x
        self.y = y
    
    def __repr__(self):
        return 'EvenBetterPoint2D(%d, %d)' % (self.x, self.y)

register_class(EvenBetterPoint2D)

point = EvenBetterPoint2D(5, 3)
print('Before:    ', point)
data = point.serialize()
print('Serialized:', data)
after = deserialize(data)
print('After:     ', after)

#这种方案也有缺点，那就是开发者可能忘记调用register_class函数，这时我们就可以从元类中来注册新的子类，以免遗忘。

class Meta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        register_class(cls)
        return cls

class Vector2D(EvenBetterPoint2D, metaclass=Meta):
    def __repr__(self):
        return 'Vector2D(%d, %d)' % (self.x, self.y)

point = Vector2D(5, 3)
print('Before:    ', point)
data = point.serialize()
print('Serialized:', data)
after = deserialize(data)
print('After:     ', after)


































