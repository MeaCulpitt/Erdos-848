# Local (asymptotic) model of the "type-matrix" bound, with configurable type refinement, solved by MILP.
# Type of a: (r25, r4, r9) after optional coarsening. Entry M(s,t) = w_t * g(s,t):
#   forced(s,t) = some modulus q^2 in {4,9,25} divides ab+1 for ALL a in t, b in s (only possible if both
#   types fix the residue mod q^2 and r_s r_t ≡ -1).  If forced: g = P(a in V | t).
#   else: g = P(a in V and ab+1 nonsqf | t) with the q^2 events treated by exact residue counting inside the
#   (possibly coarse) type and p>=7 events independent; worst b: coprime, p^2|b^2+1 for all p in S.
import itertools, numpy as np, sys
from sympy import primerange
from scipy.optimize import milp, LinearConstraint, Bounds
PR=[p for p in primerange(7,2*10**6)]
def big(S):
    noA=noB=noAB=1.0
    for p in PR:
        if p%4==3: noB*=1-1/p**2; noAB*=1-1/p**2
        else:
            x=1/p**2 if p in S else 0.0
            noA*=1-2/p**2; noB*=1-1/p**2; noAB*=1-3/p**2+x
    return noA,noB,noAB
def types(split25, split9, split4=True):
    # residue sets per modulus for each type
    R25=[r for r in range(25) if r not in (7,18)]
    c25=[(7,),(18,)]+([ (r,) for r in R25] if split25 else [tuple(R25)])
    c4=[(0,2),(1,),(3,)] if split4 else [(0,1,2,3)]
    c9=[(0,3,6)]+[(u,) for u in (1,2,4,5,7,8)] if split9 else [tuple(range(9))]
    return [(a,b,c) for a in c25 for b in c4 for c in c9]
def entry(s,t,big3):
    noA,noB,noAB=big3
    # for target t, average over residues (a25,a4,a9) uniformly in t; b residue: s must be a single residue to force
    w=len(t[0])/25*len(t[1])/4*len(t[2])/9
    inV=all(r in (7,18) for r in t[0])
    # worst b in s: choose b residues in s maximizing; enumerate b residues
    best=0
    for b25 in s[0]:
        for b4 in s[1]:
            for b9 in s[2]:
                tot=0; n=0
                for a25 in t[0]:
                    for a4 in t[1]:
                        for a9 in t[2]:
                            n+=1
                            small=((a4*b4+1)%4==0) or ((a9*b9+1)%9==0) or ((a25*b25+1)%25==0)
                            v=a25 in (7,18)
                            if v: g=1.0 if small else 1-noB
                            else: g=(1-noA) if small else 1-noA-noB+noAB
                            tot+=g
                best=max(best,tot/n)
    return w*best
def solve(T,M,isC7,isC18):
    n=len(T); c=np.concatenate([np.zeros(n),-np.ones(n)])   # vars x(n), z(n)
    w=np.array([M[t][t] if False else 0 for t in range(n)])
    rows=[];lo=[];hi=[]
    W=[max(M[s][t] for s in range(n)) for t in range(n)]
    for t in range(n):
        r=np.zeros(2*n); r[n+t]=1; r[t]=-W[t]; rows.append(r); lo.append(-np.inf); hi.append(0)
        for s in range(n):
            r=np.zeros(2*n); r[n+t]=1; r[s]=W[t]; rows.append(r); lo.append(-np.inf); hi.append(M[s][t]+W[t])
    r=np.zeros(2*n); r[:n]=[0 if isC7[t] else 1 for t in range(n)]; rows.append(r); lo.append(1); hi.append(np.inf)
    r=np.zeros(2*n); r[:n]=[0 if isC18[t] else 1 for t in range(n)]; rows.append(r); lo.append(1); hi.append(np.inf)
    res=milp(c,constraints=LinearConstraint(np.array(rows),lo,hi),integrality=np.concatenate([np.ones(n),np.zeros(n)]),
             bounds=Bounds(np.zeros(2*n),np.concatenate([np.ones(n),np.array(W)])))
    x=res.x[:n]; return -res.fun,[T[i] for i in range(n) if x[i]>0.5]
if __name__=="__main__":
    P1=[p for p in PR if p%4==1 and p>=13]
    Sopt={"empty":set(),"13":{13},"13,17":{13,17},"all":set(P1)}
    for split25,split9 in [(False,False),(False,True),(True,False),(True,True)]:
        for Sn in ["empty","13","all"]:
            b3=big(Sopt[Sn]); T=types(split25,split9)
            M=[[entry(s,t,b3) for t in T] for s in T]
            isC7=[t[0]==(7,) for t in T]; isC18=[t[0]==(18,) for t in T]
            v,P=solve(T,M,isC7,isC18)
            print(f"split25={split25} split9={split9} S={Sn:6s} ntypes={len(T)} worst={v:.5f} |P|={len(P)}",flush=True)
            if Sn=="all": print("   P sample:",P[:6])
