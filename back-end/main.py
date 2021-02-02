def maxlist(x):
    if len(x)==0:
        return 0
    else:
        k=x[0]
        while i<len(x):
            if x[i]>k:
                k=x[i]
                i+=1
            elif x[i]<=m:
                i+=1
        return k
    print(maxlist([1, 4, 5]))