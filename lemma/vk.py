# V_k = max over type-sets P (not inside C7, not inside C18) of  min over witness sets W ⊆ P, |W| <= k, of
#       sum_{t in P} val_W(t),   val_W(t) = w_t*beta if t is a C-type served (not forced) by some s in W,
#                                 w_t if t is a C-type forced by every s in W,   w_t*alpha if t is an R-type.
# (R-types are bounded by |V ∩ t| only -- no witness needed.)  Solved exactly as a MILP (HiGHS).
import itertools, sys, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
CATS=['7','18','R']; MUS=['E',1,3]; NUS=[0,1,2,4,5,7,8]
T=[(c,m,n) for c in CATS for m in MUS for n in NUS]
def w(t):
    c,m,n=t; return (1/25 if c!='R' else 23/25)*(1/2 if m=='E' else 1/4)*(1/3 if n==0 else 1/9)
def forced(s,t):            # s = witness type, t = target type; True if p^2 | ab+1 for all a in t, b in s, p in {2,3,5}
    (cs,ms,ns),(ct,mt,nt)=s,t
    if ct!='R' and cs==ct: return True
    if ms!='E' and mt!='E' and (ms*mt)%4==3: return True
    if ns!=0 and nt!=0 and (ns*nt)%9==8: return True
    return False
def name(t): return f"{t[0]}{t[1]}{t[2]}"
def Vk(k,alpha,beta,verbose=False):
    n=len(T); Ws=[W for j in range(1,k+1) for W in itertools.combinations(range(n),j)]
    A=lil_matrix((len(Ws)+2,n+1)); lo=[];hi=[]
    for r,W in enumerate(Ws):
        for t in range(n):
            tt=T[t]
            if tt[0]=='R': c=w(tt)*alpha
            else: c=w(tt)*(1.0 if all(forced(T[s],tt) for s in W) else beta)
            A[r,t]=-c
        for s in W: A[r,s]+=1.0
        A[r,n]=1.0; lo.append(-np.inf); hi.append(len(W))
    A[len(Ws),:n]=[0 if t[0]=='7' else 1 for t in T]; lo.append(1); hi.append(np.inf)
    A[len(Ws)+1,:n]=[0 if t[0]=='18' else 1 for t in T]; lo.append(1); hi.append(np.inf)
    c=np.zeros(n+1); c[n]=-1
    res=milp(c,constraints=LinearConstraint(A.tocsr(),lo,hi),integrality=np.r_[np.ones(n),0],
             bounds=Bounds(np.zeros(n+1),np.r_[np.ones(n),1.0]),options={"mip_rel_gap":1e-9})
    P=[T[i] for i in range(n) if res.x[i]>0.5]
    return -res.fun, P, -res.mip_dual_bound
if __name__=="__main__":
    alpha=float(sys.argv[1]); beta=float(sys.argv[2]); K=int(sys.argv[3])
    for k in range(1,K+1):
        v,P,db=Vk(k,alpha,beta); print(f"k={k}: V_k={v:.6f} (dual {db:.6f}) |P|={len(P)} P={[name(t) for t in P]}",flush=True)
