def fac(n):
    if n==0:
        f=1
    else:
        f=fac(n-1)*n
    return(f)

n=int(input())
f=fac(n)
sum=0
for i in range(1,n+1):
    sum=sum+fac(i)
print("fact(10)=%d"%f)
print("sum=%d"%sum)
