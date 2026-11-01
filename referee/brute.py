# referee brute force of Lemma 3 (Pell) and Lemma 4 (lattice) on small parameters
import math, json, numpy as np, sys
from sympy import isprime, primerange, factorint
# ---------- Lemma 3 ----------
L=8*25*3*7*11*19*23
def adm_direct(x):  # direct count of admissible m in [2,x] (no table)
    X=int(math.floor(x)); tot=0
    for lo in range(2,X+1,5*10**6):
        m=np.arange(lo,min(X,lo+5*10**6-1)+1,dtype=np.int64)
        ok=np.isin(m%8,[1,2,5])&(m%25!=0)
        for q in (3,7,11,19,23): ok&=(m%q!=0)
        tot+=int(ok.sum())
    return tot
def pell_bound(N,Y):
    M=(N*N+1)/(Y*Y); tot=0; j=1
    while True:
        T=(2*N+1)**(1/(2*j-1))
        if T<1+2**.5: break
        tot+=adm_direct(min(M,((T+1/T)/2)**2*(1+1e-12))); j+=1
    return tot
def sqrtm1(p):
    q=p*p
    for g in range(2,p):
        t=pow(g,(p-1)//4,p)
        if t*t%p==p-1: break
    r=(t-(t*t+1)*pow(2*t,-1,q))%q; assert (r*r+1)%q==0; return r
print("Lemma 3 (Pell): actual = #{x<=N, x mod 25 not in {7,18}: p^2|x^2+1 for a prime p>Y}")
for N,YY in ((20000,(20,60,200,1000,5000)),(100000,(20,60,200,1000,5000)),(300000,(300,1000,5000,20000))):
    for Y in YY:
        hit=set()
        for p in primerange(int(Y)+1, math.isqrt(N*N+1)+1):
            if p%4!=1: continue
            r=sqrtm1(p); q=p*p
            for r0 in (r,q-r):
                for x in range(r0,N+1,q):
                    if x%25 not in (7,18):
                        hit.add(x); m=(x*x+1)//q
                        assert m%8 in (1,2,5) and m%25 and all(m%t for t in (3,7,11,19,23)) and 2<=m<(N*N+1)/Y**2
        b=pell_bound(N,Y); print(f"  N={N} Y={Y}: actual={len(hit)} bound={b} ok={len(hit)<=b}",flush=True)
# ---------- Lemma 4 ----------
MC={eval(k):v for k,v in json.load(open('mc.json')).items()}
def inV(b): return any(e>=2 for p,e in factorint(b*b+1).items())
print("Lemma 4 (lattice): actual = #{a<=N in T_b : p^2|ab+1, p prime > Y}; bound with b's own profile/omega and b itself")
worst=0
for N,Ys,bs in ((3000,(10,20,50,150),'all'),(20000,(15,40,120,400),'sample')):
    Vb=[b for b in range(7,N+1) if inV(b)]
    if bs=='sample':
        import random; random.seed(1); Vb=sorted(random.sample(Vb,150)+[b for b in Vb if b%120==0][:20]+Vb[-10:])
    MX={}
    for b in Vb:
        lst=[]
        for a in range(1,N+1):
            if a%25 not in (7,18): continue
            v=a*b+1
            if v%4==0 or v%9==0 or v%25==0: continue
            ps=[p for p,e in factorint(v).items() if e>=2]
            if ps: lst.append(max(ps))
        MX[b]=np.array(lst)
    for Y in Ys:
        wr=0; nb=0
        for b in Vb:
            v2=0 if b%2 else (1 if b%4 else (2 if b%8 else 3)); key=(v2,int(b%3==0),int(b%5==0)); lam,c=MC[key]
            om=len([p for p in factorint(b) if p>=7])
            bound=2**om*(2*lam*(N+1)/Y+c*math.sqrt(b*N+1)/b+lam*(b*N+1)/Y**2+c)
            act=int((MX[b]>Y).sum())
            nb+=1; wr=max(wr,act/bound)
            if act>bound: print("  VIOLATION",N,Y,b,act,bound)
        worst=max(worst,wr); print(f"  N={N} Y={Y}: {nb} witnesses, max actual/bound = {wr:.4f}",flush=True)
print("worst ratio",worst)
