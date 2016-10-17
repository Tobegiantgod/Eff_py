#coding: utf-8
a=['a','b','c','d','e','f','g','h']
print('First four:',a[:4])
print('Last four:',a[-4:])
print('Middle two:',a[3:-3])
first_twenty_items=a[:20]
last_twenty_items=a[-20:]

#使用切片操作替换列表内容
print ('Before ',a)
a[2:7]=[99,22,14]
print ('After ',a)

b=a[:]
assert b==a and b is not a
print b 

#赋值时使用切片操作，将把右边的值赋值给左边，不会产生新的列表，a和b还是同一列表
b=a
print('Before',a)
a[:]=[101,102,103]
assert a is b
print('After ',a)
print('b is ',b)

