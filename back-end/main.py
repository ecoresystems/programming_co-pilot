def avglist(list):
    if len(list)=0:
        return 0
    else:
        i=0
        while i<=len(list):
            x=0
            x=x+list[i]
            i=i+1
        return x/len(list)
list=[1,2,3,4,5]
print(aavglist(list))