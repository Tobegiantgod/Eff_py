#coding: utf-8

#不要在for和while循环后面写else块


#以下写法else会在执行完整个循环后立刻运行：

for i in range(3):
    print('Loop %d'%i)
else:
    print('Else block!')

#只有循环主体遇到break时，循环后面的else才不会执行

for i in range(3):
    print('Loop %d'%i)
    if i%2==0:
        break
else:
    print('Else block!')

#不要在循环后面使用else块，因为这个写法既不直观，又容易引人误解

