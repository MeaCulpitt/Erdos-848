import sys, numpy as np
X=int(sys.argv[1]); 
Ns=[int(l.split()[0][2:]) for l in open(sys.argv[2]) if l.startswith('N=')]
M=X*X+2
nsq=np.zeros(M,dtype=bool)
lim=int(M**0.5)+2; isp=np.ones(lim,dtype=bool); isp[:2]=False
for i in range(2,lim):
    if isp[i]: isp[i*i::i]=False; nsq[i*i::i*i]=True
a=np.arange(X+1); Vm=nsq[a*a+1]; Vm[0]=False; cls=a%25
C7=Vm&(cls==7); C18=Vm&(cls==18); R=Vm&(cls!=7)&(cls!=18); odd=a%2==1
Ns=np.array(Ns)
def cum(mask): c=np.cumsum(mask); return c[Ns]
m={k:np.zeros(len(Ns),dtype=np.int64) for k in "1 2 3a 3b 3c 3d 4a 4b".split()}
for b in np.nonzero(Vm)[0]:
    b=int(b); act=Ns>=b; hit=nsq[a*b+1]
    def up(k,v): m[k]=np.where(act,np.maximum(m[k],v),m[k])
    if R[b]:
        if b%2==0: up('1',cum(hit&C7)+cum(hit&C18))
        else: up('2',cum(hit&(C7|C18)&odd)); up('3a',cum(hit&C7)); up('3c',cum(hit&C18))
    elif C7[b]:
        h=cum(hit&C18); up('4b',h)
        if b%2==0: up('3b',h)
    else:
        h=cum(hit&C7); up('4a',h)
        if b%2==0: up('3d',h)
vR=cum(R); vRo=cum(R&odd)
S1=vR+m['1']; S2=vRo+m['2']; S3=vRo+np.maximum(m['3a']+m['3b'],m['3c']+m['3d']); S4=m['4a']+m['4b']
bad=0
for i,l in enumerate([l for l in open(sys.argv[2]) if l.startswith('N=')]):
    f=dict(x.split('=') for x in l.split() if '=' in x and x.startswith('S'))
    if (int(f['S1']),int(f['S2']),int(f['S3']),int(f['S4']))!=(S1[i],S2[i],S3[i],S4[i]): bad+=1; print("MISMATCH",l.strip(),S1[i],S2[i],S3[i],S4[i])
print("edges",len(Ns),"mismatches",bad)
