#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#    Author :  Daydup
#    E-mail :  hainuzsr@gmail.com
#    Date   :  170105 15:25:41
##################################
#6-47 在重视精度的场合，应该使用decimal
##################################

#Python语言很适合用来编写与数值型数据打交道的代码。Python的数据类型，可以表达任意长度的值，其双精度浮点数类型，也遵循IEEE754标准。此外，Python还提供了标准的复数类型，用来表示虚数。然而这些数值类型，并不能覆盖每一种情况。

#例如，要根据通话时长和费率，来计算用户拨打国际长途电话所应支付的费用。假如用户打了3分42秒，从美国打往南极洲的电话，每分钟1.45美元，那么，这次通话费用是多少呢？

#使用浮点数进行计算

rate = 1.45
seconds = 3*60 + 42
cost = rate * seconds / 60
print(cost)

#但是我们想向分位取整之后，却发现，round函数把分位右侧的那些数字全舍去了，而不是向上取整

print(round(cost,2))

#假如通话长度很短，费率很低

rate = 0.05
seconds = 5
cost = rate * seconds / 60
print(cost)

print(round(cost, 2))


#内置的decimal模块中，有个Decimal类，可以解决上面那些问题。该类默认提供28个小数位，以进行定点(fixed point)数学运算。如果有需要，还可以把精确度调得更高一些。Decimal类解决了IEEE754浮点数所产生的精度问题，而且开发者还可以更加精准地控制该类的舍入行为。

from decimal import Decimal

rate = Decimal('1.45')
seconds = Decimal('222')
cost = rate * seconds / Decimal('60')
print(cost)

#Decimal类提供一个内置的函数，它可以按照开发者所要求的精度及舍入方式，来准确地调整整数值。

rounded = cost.quantize(Decimal('0.01'), rounding='ROUND_UP')
print(rounded)

#这个quantize方法，也能对那种时长很短、费用很低的电话，正确地进行计费。我们用Decimal类来改写之前的那段代码。改写之后，计算出来的电话费用，还是不足1分钱：

rate = Decimal('0.05')
seconds = Decimal('5')
cost = rate * seconds / Decimal('60')
print(cost)

#但是在调用quantize方法时，指定合理的舍入方式，从而确保该方法能够把不足1分钱的部分，上调为1分钱。

rounded = cost.quantize(Decimal('0.01'), rounding='ROUND_UP')
print(rounded)

#对于编程中可能用到的每一种数值，我们都可以拿对应的Python内置类型，或内置模块中的类表示。

#Decimal类非常适合用在那种对精度要求很高，且对舍入行为要求很严的场合，例如，涉及货币计算的场合。












