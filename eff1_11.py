#coding: utf-8

#用ZIP函数同时遍历两个迭代器

from itertools import izip


names=['Cecilia','Lise','Marie']
letters=[len(n) for n in names]

#用names源列表的长度来执行循环

longest_name=None
max_letters=0

for i in range(len(names)):
    count=letters[i]
    if count>max_letters:
        longest_name=names[i]
        max_letters=count

print(longest_name)


#用enumerate函数改写以上程序

for i,name in enumerate(names):
    count=letters[i]
    if count>max_letters:
        longest_name=name
        max_letters=count

print(longest_name)


#使用Python内置的zip函数，能够使上述代码变得更为简洁：

#在Python2中zip并不知生成器，如果输入数据过大会占用大量内存并导致程序崩溃，所以应该使用itertools内置模块中的izip函数：

for name,count in izip(names,letters):
    if count>max_letters:
        longest_name=name
        max_letters=count
print(longest_name)
