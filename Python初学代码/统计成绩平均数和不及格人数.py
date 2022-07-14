n=int(3)
if(n==0):
    print('average = 0.0')
    print('count = 0')
    exit(0)
lst = list(map(int,40,60,80.split()))
sum = sum(lst)
aver=sum/n
new_lst = [x for x in lst if x >= 60]
cnt = len(new_lst)
print('average = {:.1f}'.format(aver))
print('count = {:d}'.format(cnt))
