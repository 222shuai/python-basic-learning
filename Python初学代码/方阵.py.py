n,digit=map(int,input().split(" "))
i=1
j=1
while (i==1)or (i==n):
    if j<n:
        print(digit,end=" ")
        j+=1
    else:
        print(digit,end=" \n")
        j=1
        i+=1
    while 1<i<n:
        if j==1:
            print(digit,end=" ")
            j+=1
        elif 1<j<n:
            print(digit-1,end=" ")
            j+=1
        else:
            print(digit,end=" \n")
            j=1
            i+=1
