#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  161129 15:38:52
##################################
#4-31 用描述符来改写需要复用的@property方法
##################################

#Python内置的@property修饰器,有个明显的缺点，就是不便于复用。受它修饰的这些方法，无法为同一类中的其他属性所复用，而且，与之无关的类，也无法复用这些方法。

#现在假设要把这套验证逻辑放在考试成绩上面，而考试成绩又时由多个科目的小成绩，每一科都要单独计分。

class Exam(object):
    def __init__(self):
        self._writing_grade = 0
        self._math_grade = 0

    @staticmethod
    def _check_grade(value):
        if not (0 <= value <=100):
            raise ValueError('Grade must be between 0 and 100')

    #Exam类的代码写起来非常枯燥,因为每添加一项科目，就要重复编写一次@property方法，而且还要把相关的验证逻辑也重做一遍。
    @property
    def writing_grade(self):
        return self._writing_grade

    @writing_grade.setter
    def writing_grade(self, value):
        self._check_grade(value)
        self._writing_grade = value

    @property
    def math_grade(self):
        return self._math_grade

    @math_grade.setter
    def math_grade(self, value):
        self._check_grade(value)
        self._math_grade = value

#以上的方法在需要添加科目成绩的时候需要重写一次@property方法，太麻烦，可以采用Python的描述符(descriptor)来做，同时可以使用Python的内置weakref模块的WeakKeyDictionary，便于系统更好的回收内存，如下：

from weakref import WeakKeyDictionary

class Grade(object):
    def __init__(self):
        self._values = WeakKeyDictionary()

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not( 0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._values[instance] = value


class Exam(object):
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()

first_exam = Exam()
first_exam.writing_grade = 82
second_exam = Exam()
second_exam.writing_grade = 75
print('First ', first_exam.writing_grade, 'is right')
print('Second', second_exam.writing_grade, 'is right')

#如果想复用@property方法及其验证机制，那么可以自己定义描述符类。
#WeakKeyDictionary可以保证描述符类不会泄漏内存。

        






