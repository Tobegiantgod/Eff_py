#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  161207 14:53:55
##################################
#4—33 用元类来验证子类
##################################

#元类最简单的一种用途，就是验证某个类定义的是否正确，定义元类的时候，要从type中继承，而对于使用该元类的其他类来说，Python默认会把那些类的class语句体中所含的内容，发送给元类的__new__方法。于是，我们就可以在系统构建出那种类型之前，先修改那个类的信息:
    
#定义元类

class Meta(type):
    def __new__(meta, name, bases, class_dict):
        print((meta, name, bases, class_dict))
        return type.__new__(meta, name, bases, class_dict)

class MyClass(object, metaclass=Meta):
    stuff = 123
    def foo(self):
        pass

#为了在定义某个类的时候,确保该类的所有参数都有效，我们可以把相关的验证逻辑添加到Meta.__new__方法中。例如，要用类来表示任意多边形。为此，我们可以定义一种特殊的验证类，使得多边形体系中的基类，把这个验证类当成自己的元类。

class MetaPolygon(type):
    def __new__(meta, name, bases, class_dict):
        #Don't validate the abstract Polygon class
        if bases != (object,):
            if class_dict['sides'] < 3:
                raise ValueError('Polygons need 3+ sides')
        return type.__new__(meta, name, bases, class_dict)

class Polygon(object, metaclass=MetaPolygon):
    sides = None # Specified by subclasses

    @classmethod
    def interior_angles(cls):
        return (cls.sides - 2) * 180

class Triangle(Polygon):
    sides = 3

print (Triangle.interior_angles())


#当定义一种边数少于3的多边形子类，那么class语句体刚一结束，元类中的验证代码立刻就会拒绝这个class。也就是说，如果开发者定义这样一种子类，那么程序根本就无法运行。

print('Before class')
class Line(Polygon):
    print('Before sides')
    sides = 1
    print('After sides')


#通过元类，我们可以在生成子类对象之前，先验证子类定义是否合乎规范。Python系统把子类的整个class语句体处理完毕之后，就会调用其元类的__new__方法。









