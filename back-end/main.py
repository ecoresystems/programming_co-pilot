def count(x):
    j = 0
    dic = {}
    for i in range(0,len(x)):
        if x[i] in x:
            j = +1
            dic[x[i]] = j
            i = +1
        if x[i] in dic:
            dic[x[i]] = j + 1
            i = +1
    return dic      
             
print(count([1,4,1,4,2,1,3,5,6]))             