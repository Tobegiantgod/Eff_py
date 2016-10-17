#coding: utf-8

#1-8不要使用含有两个以上表达式的列表推导

matrix=[[1,2,3],[4,5,6],[7,8,9]]
flat=[x for row in matrix for x in row]
print flat

squared=[[x**2 for x in row] for row in matrix]

print squared

#列表推导也支持多个if条件，下面两个表达式等效

a=[x for x in range(10)]

b=[x for x in a if x>4 if x%2==0]
c=[x for x in a if x>4 and x%2==0]
print a
print b
print c

#每一级循环的for表达式后面都可以指定条件，可以实现简短的代码实现较复杂的逻辑，但这样代码非常难懂。

filtered=[[x for x in row if x%3==0] for row in matrix if sum(row)>=10]

print filtered
