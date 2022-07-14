a=map(int,input().split(","))
a=list(a)
x=[]
for i in range(6,11):
    if i not in a:
        x.append(i)
for y in range(0,len(x)):
    x[y]=int(x[y])
    if y<len(x)-1:
        print(x[y],end=" ")
    else:
        print('{:d}'.format(x[y]),end="")
