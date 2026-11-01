# referee: per-m check of Lemma 4's intermediate inequalities (membership m in S_b, rho bound, class count)
import math
from sympy import factorint
from collections import Counter
MOD=1800
units=[u for u in range(MOD) if u%2 and u%3 and u%5]; sq={u*u%MOD for u in units}
def inV(b): return any(e>=2 for e in factorint(b*b+1).values())
bad=0; checked=0; tight=0
for N,Y in ((3000,10),(3000,40),(6000,25)):
    for b in range(7,N+1):
        if not inV(b): continue
        T=[a for a in range(MOD) if a%25 in(7,18) and (a*b+1)%4 and (a*b+1)%9 and (a*b+1)%25]
        targ={(a*b+1)%MOD for a in T}
        Sb=lambda m: any((m*s)%MOD in targ for s in sq)
        v2=0 if b%2 else (1 if b%4 else (2 if b%8 else 3)); b0=(1,2,4,8)[v2]*(3 if b%3==0 else 1)*(5 if b%5==0 else 1)
        om=len([p for p in factorint(b) if p>=7])
        cnt=Counter()
        for a in range(1,N+1):
            if a%25 not in (7,18): continue
            v=a*b+1
            if v%4==0 or v%9==0 or v%25==0: continue
            ps=[p for p,e in factorint(v).items() if e>=2 and p>Y]
            if ps: p=max(ps); cnt[v//(p*p)]+=1
        for m,c in cnt.items():
            checked+=1
            rho=sum(1 for s in range(b) if (m*s*s-1)%b==0)
            rho0=sum(1 for s in range(b0) if (m*s*s-1)%b0==0)
            S=math.isqrt((b*N+1)//m)
            okS=Sb(m%MOD); okr=rho<=rho0*2**om; okc=c<=rho*(S/b+1)
            if c==rho*(S//b+1): tight+=1
            if not(okS and okr and okc): bad+=1; print("FAIL",N,Y,b,m,c,rho,rho0,om,okS,okr,okc)
    print(f"N={N} Y={Y}: checked (b,m) pairs so far {checked}, failures {bad}, tight cases {tight}",flush=True)
