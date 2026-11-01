# referee: independent lambda,c for Lemma 4, brute-force rho
import numpy as np, json
MOD=1800
units=[u for u in range(MOD) if u%2 and u%3 and u%5]
sq=sorted({u*u%MOD for u in units})
res={}
for b in range(MOD):
    T=[a for a in range(MOD) if a%25 in(7,18) and (a*b+1)%4 and (a*b+1)%9 and (a*b+1)%25]
    if not T: continue
    v2=0 if b%2 else (1 if b%4 else (2 if b%8 else 3)); t3=b%3==0; t5=b%5==0
    b0=(1,2,4,8)[v2]*(3 if t3 else 1)*(5 if t5 else 1)
    # m in S iff m*s^2 == ab+1 (mod 1800) for some unit s, a in T
    targ={(a*b+1)%MOD for a in T}
    S=np.zeros(MOD,bool)
    for m in range(MOD):
        if any((m*s)%MOD in targ for s in sq): S[m]=True
    g=np.array([ (sum(1 for s in range(b0) if (m*s*s-1)%b0==0) if S[m] else 0) for m in range(MOD)],float)
    lam=g.mean(); G=np.cumsum([g[m%MOD] for m in range(1,MOD+1)]); cc=max(0,(G-lam*np.arange(1,MOD+1)).max())
    k=(v2,int(t3),int(t5)); L,C=res.get(k,(0,0)); res[k]=(max(L,lam),max(C,cc))
for k in sorted(res): print(k,"%.6f %.6f"%res[k])
json.dump({str(k):v for k,v in res.items()},open('mc.json','w'))
