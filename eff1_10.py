#coding:utf-8

#尽量用enumerate取代range

#对于字符串这样的序列式数据结构，可以直接在上面迭代。

flavor_list=['vanilla','chocolate','pecan','strawberry']

for flavor in flavor_list:
    print('%s is delicious' %flavor)

#当迭代列表的时候，通常还想知道元素在列表的索引，通常做法如下：

for i in range(len(flavor_list)):
    flavor=flavor_list[i]
    print('%d: %s is delicous'%(i+1,flavor))

#用内置的enumerate函数，可以将上面代码改为如下更简洁的代码：

for i,flavor in enumerate(flavor_list):
    print('%d:%s'%(i+1,flavor))

#还可以直接指定enumerate函数开始计数数所用的值，这样能使代码更简洁：

for i,flavor in enumerate(flavor_list,1):
    print('%d: %s'%(i,flavor))
