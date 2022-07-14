str=input()
x=[]
for i in str:
    if 'z' >=i>= 'a' or 'Z' >=i>= 'A':
        if (i.upper() not in x)and(i.lower() not in x):
            x.append(i)
if len(x)<10:
    print('not found')
else:
    for i in range(9):
        print(x[i],end='')
    print(x[9])
