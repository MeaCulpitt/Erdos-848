# Segmented sieve to XMAX: writes checkpoints every STEP of  pi(x)  and  pi(x;4,1)  (counts of primes <= x).
# Upper bounds for pi(y) are then read off at the next checkpoint >= y (rigorous upper bound).
import numpy as np, sys
XMAX=int(float(sys.argv[1])); STEP=int(float(sys.argv[2])); SEG=10**7
r=int(XMAX**0.5)+1
s=np.ones(r+1,bool); s[:2]=False
for i in range(2,int(r**0.5)+1):
    if s[i]: s[i*i::i]=False
base=np.nonzero(s)[0]
cp=[]; c1=[]; tot=0; tot1=0
for lo in range(0,XMAX+1,SEG):
    hi=min(lo+SEG,XMAX+1); seg=np.ones(hi-lo,bool)
    if lo==0: seg[:2]=False
    for p in base:
        p=int(p)
        if p*p>=hi: break
        st=max(p*p,((lo+p-1)//p)*p); seg[st-lo::p]=False
    idx=np.nonzero(seg)[0]+lo
    one=(idx%4==1)
    # checkpoints at multiples of STEP in [lo,hi)
    for x in range(((lo+STEP-1)//STEP)*STEP, hi, STEP):
        k=np.searchsorted(idx,x,side='right'); cp.append((x,tot+k,tot1+int(one[:k].sum())))
    tot+=len(idx); tot1+=int(one.sum())
np.save('pc.npy',np.array(cp,dtype=np.int64)); print("done",XMAX,tot,tot1)
