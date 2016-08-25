#coding: utf-8

#用列表推导来取代map和filter

a=[1,2,3,4,5,6,7,8,9,10]

squares=[x**2 for x in a]
print(squares)

squares=map(lambda x: x**2,a)
even_squares=[x**2 for x in a if x%2 ==0]
print(even_squares)

alt=map(lambda x:x**2,filter(lambda x:x%2==0,a))
print alt
assert even_squares==alt

#字典与集也有和列表类似的推导机制。编写算法时，可以通过这些推导机制来创建衍生的数据结构。

chile_ranks={'ghost':1,'hahanero':2,'cayenne':3}
print chile_ranks.items()
rank_dict={rank:name for name,rank in chile_ranks.items()}
print rank_dict
chile_len_set={len(name) for name in rank_dict.values()}
print chile_len_set

