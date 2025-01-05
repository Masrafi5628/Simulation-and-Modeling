import numpy as np

np.random.seed(2)
k=0
while k<10:
    print(np.random.uniform(-5,10))
    k+=1
k=0
mp={0:0,1:0}
while k<100:
    n=np.random.rand()
    if(n<0.1):
        mp[0]+=1
    else:
        mp[1]+=1
    k+=1

print(mp)