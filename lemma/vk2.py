# V_2 for the rigorous model used in n0lemma.py (Theorem T of README):
#   value(P,W) = sum_{C-types t in P} w_t * (1 if every s in W forces t else beta)
#                + sum_{R-types t in P} w_t * alpha_s  +  [P contains an R type] * (23/25)*tailA
# alpha_s = 1 - prod_{13<=p<=zA, p≡1(4)} (1-2/p^2)  (small primes, counted on the union of R types in P);
# tailA   = 2 sum_{p>zA, p≡1(4)} 1/p^2 (primes > zA, counted over ALL of R once any R type is present).
# V_k = max over type-sets P (not inside the C7 types, not inside the C18 types) of min over W ⊆ P, 1<=|W|<=k.
# Exact MILP (HiGHS); the reported value is max(primal, dual bound).
import itertools, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
from vk import T, w, forced, name
def Vk2(k, alpha_s, tailA, beta):
    n=len(T); Ws=[W for j in range(1,k+1) for W in itertools.combinations(range(n),j)]
    isR=[t[0]=='R' for t in T]; cR=23/25*tailA
    nv=n+2   # x_0..x_{n-1}, y (R present), z (objective)
    A=lil_matrix((len(Ws)+3,nv)); lo=[];hi=[]
    for r,W in enumerate(Ws):
        for t in range(n):
            tt=T[t]
            if isR[t]: A[r,t]=-w(tt)*alpha_s; continue
            A[r,t]=-w(tt)*(1.0 if all(forced(T[s],tt) for s in W) else beta)
        A[r,n]=-cR
        for s in W: A[r,s]+=1.0
        A[r,n+1]=1.0; lo.append(-np.inf); hi.append(len(W))
    i=len(Ws)
    A[i,:n]=[0 if t[0]=='7' else 1 for t in T]; lo.append(1); hi.append(np.inf)
    A[i+1,:n]=[0 if t[0]=='18' else 1 for t in T]; lo.append(1); hi.append(np.inf)
    A[i+2,:n]=[-1 if isR[t] else 0 for t in range(n)]; A[i+2,n]=1; lo.append(-np.inf); hi.append(0)  # y <= sum x_R
    c=np.zeros(nv); c[n+1]=-1
    res=milp(c,constraints=LinearConstraint(A.tocsr(),lo,hi),integrality=np.r_[np.ones(n+1),0],
             bounds=Bounds(np.zeros(nv),np.r_[np.ones(n+1),1.0]),options={"mip_rel_gap":1e-9})
    P=[T[i] for i in range(n) if res.x[i]>0.5]
    return -res.fun, P, -res.mip_dual_bound
if __name__=="__main__":
    import sys, json
    sys.argv=['x']; exec(open('n0lemma.py').read().split('if __name__')[0])
    out={}
    for zA in (17,29,37,41):
        for zB in (13,17,19,23):
            a,b=alpha_up(zA),beta_up(zB); tA=2*sum_inv_sq_gt(zA,True); v,P,db=Vk2(2,a-tA,tA,b); f=2/25*b+23/25*a
            print(zA,zB,f"alpha={a:.6f} beta={b:.6f} V2={v:.7f} dual={db:.7f} formula={f:.7f} |P|={len(P)}",flush=True)
            out[f"{zA},{zB}"]=max(v,db,f)
    json.dump(out,open('v2grid.json','w'),indent=1)
