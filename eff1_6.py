#coding: utf-8

#在单次切片操作内，不要同时指定start、end和stride

a=['red','orange','yellow','green','blue','purple']
odds=a[::2]
evens=a[1::2]
print odds
print evens

x=b'mongoose'
y=x[::-1]
print y

#负数步进值表示从尾部开始取
print a[::2]
print a[::-2]

b=a[::2]
c=b[1:-1]

print b
print c

#尽量使用stride为正数，且不带start或end索引的切割操作
