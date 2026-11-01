# Independent check: squarefreeness via a numpy "has square divisor" sieve up to N^2+1
import sys, numpy as np
N=int(sys.argv[1]); M=N*N+2
nsq=np.zeros(M,dtype=bool)
p=2
isp=np.ones(int(M**0.5)+2,dtype=bool); isp[:2]=False
for i in range(2,len(isp)):
    if isp[i]:
        isp[i*i::i]=False
        nsq[i*i::i*i]=True
a=np.arange(N+1)
Vm=nsq[a*a+1]; Vm[0]=False
cls=a%25
C7=Vm&(cls==7); C18=Vm&(cls==18); R=Vm&~(cls==7)&~(cls==18)
def H(b,mask): return int(np.count_nonzero(mask & nsq[a*b+1]))
odd=(a%2==1)
S1=S2=S3a=S3b=S3c=S3d=m4a=m4b=0
for b in np.nonzero(Vm)[0]:
    b=int(b)
    if R[b]:
        if b%2==0: S1=max(S1,H(b,C7)+H(b,C18))
        else:
            S2=max(S2,H(b,(C7|C18)&odd)); S3a=max(S3a,H(b,C7)); S3c=max(S3c,H(b,C18))
    elif C7[b]:
        m4b=max(m4b,H(b,C18))
        if b%2==0: S3b=max(S3b,H(b,C18))
    else:
        m4a=max(m4a,H(b,C7))
        if b%2==0: S3d=max(S3d,H(b,C7))
vR=int(R.sum()); vRo=int((R&odd).sum())
print(f"N={N} S1={vR+S1} S2={vRo+S2} S3={vRo+max(S3a+S3b,S3c+S3d)} S4={m4a+m4b} c7={(N-7)//25+1}")
