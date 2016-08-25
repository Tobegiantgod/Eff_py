values={'red'='5','blue'='1','green'=''}

def get_first_int(values,key,default=0):
    found=values.get(key,[''])
    if found[0]:
        found=int(found[0])
    else：
        found=default
    return found

print get_first_int(my_values,'red')
