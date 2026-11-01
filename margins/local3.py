# Local model, 63 types: worst total (a) unrestricted, (b) P containing >=1 R type, (c) P containing >=1
# non-forced (s,t) entry used in the minimum -- reported via (b). Worst-b assumption S = all p≡1(4), p>=13.
import numpy as np
exec(open('local.py').read().split('if __name__')[0])
from scipy.optimize import milp, LinearConstraint, Bounds
def types63():
    R25=tuple(r for r in range(25) if r not in (7,18))
    return [(a,b,c) for a in [(7,),(18,),R25] for b in [(0,2),(1,),(3,)] for c in [(0,3,6)]+[(u,) for u in (1,2,4,5,7,8)]]
def solve2(T,M,extra):
    n=len(T); W=[max(M[s][t] for s in range(n)) for t in range(n)]
    rows=[];lo=[];hi=[]
    for t in range(n):
        r=np.zeros(2*n); r[n+t]=1; r[t]=-W[t]; rows.append(r); lo.append(-np.inf); hi.append(0)
        for s in range(n):
            if M[s][t]>=W[t]-1e-15: continue
            r=np.zeros(2*n); r[n+t]=1; r[s]=W[t]-M[s][t]; rows.append(r); lo.append(-np.inf); hi.append(W[t])
    for mask,l in extra:
        r=np.zeros(2*n); r[:n]=mask; rows.append(r); lo.append(l); hi.append(np.inf)
    res=milp(-np.concatenate([np.zeros(n),np.ones(n)]),constraints=LinearConstraint(np.array(rows),lo,hi),
             integrality=np.concatenate([np.ones(n),np.zeros(n)]),bounds=Bounds(np.zeros(2*n),np.concatenate([np.ones(n),W])))
    return -res.fun,[T[i] for i in range(n) if res.x[i]>0.5]
P1=[p for p in PR if p%4==1 and p>=13]
T=types63()
nm=lambda t:(str(t[0][0]) if len(t[0])==1 else 'R')+{(0,2):'E',(1,):'1',(3,):'3'}[t[1]]+str(t[2][0])
for Sn,S in [("empty",set()),("all",set(P1))]:
    b3=big(S); M=[[entry(s,t,b3) for t in T] for s in T]
    not7=[0 if t[0]==(7,) else 1 for t in T]; not18=[0 if t[0]==(18,) else 1 for t in T]; isR=[1 if len(t[0])>1 else 0 for t in T]
    base=[(not7,1),(not18,1)]
    v,P=solve2(T,M,base); print(f"S={Sn}: unrestricted worst {v:.5f}",[nm(t) for t in P])
    v,P=solve2(T,M,base+[(isR,1)]); print(f"S={Sn}: with an R type   {v:.5f}",[nm(t) for t in P])
    v,P=solve2(T,M,[(isR,1)]); print(f"S={Sn}: R type, single-class allowed {v:.5f}",[nm(t) for t in P])
