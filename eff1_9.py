#coding:utf-8

#用生成器表达式来改写数据量较大的列表推导

list_1=[[x for x in range(6)],[x for x in range(7)],[x for x in range(8)]]
print list_1

it = (len(x) for x in list_1)
print it

print next(it)
print next(it)

roots=((x,x**0.5) for x in it)

print(next(roots))

