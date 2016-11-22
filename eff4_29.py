#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  161121 17:04:51
##################################
#4-29 用纯属性取代get和set方法
##################################

#对于Python语言来说，基本不需要手工实现setter或getter方法，而应该直接使用简单的public属性。

class Resistor(object):
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0

re = Resistor(50e3)
re.ohms = 10e3
re.ohms += 10e3
print re.ohms 




#如果想以后在设置属性的时候实现特殊行为，那么可以改用@property修饰器和setter方法来做。在下面这个子类中，它在给voltage(电压）属性赋值的时候，还会同时修改current(电流)属性。

class VoltageResistance(object):
    def __init__(self, ohms):
        self.ohms = ohms

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self._voltage / self.ohms

foo = VoltageResistance(20)
foo.voltage = 40

print (foo.current)


#可以用@property来防止父类的属性遭到修改

class FixedResistance(Resistor):
    #...
    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, '_ohms'):
            raise AttributeError("Can't set attribite")
        self._ohms = ohms

r4 = FixedResistance(1e3)
r4.ohms = 2e3

#最后，要注意用@property方法来实现setter和getter时，不要把程序的行为写得太过奇怪。例如，我们不应该在某属性的getter方法里修改其他属性的值。

class MysteriousResistor(Resistor):
    @property
    def ohms(self):
        self.voltage = self._ohms * self.current #不应该在getter方法里面修改其他属性的值。
        return self._ohms
    # ...

#编写新类时，应该用简单的public属性来定义其接口，而不要手工实现set和get方法，如果访问对象的某个属性时，需要表现出特殊的行为，那就用@property来定义这种行为，@property方法需要执行得迅速一些，缓慢或复杂的工作，应该放在普通的方法里面。








