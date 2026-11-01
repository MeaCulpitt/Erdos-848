# Reads typemat output; for each N computes
#   F(N) = max over type-sets P (not all-C7, not all-C18) of  sum_{t in P} min_{s in P} M[s][t]
# by MILP (HiGHS). Data are integers; result is rounded and re-verified by direct evaluation of the reported P.
# Rigorous upper bound on |A|: for valid A ⊆ [1,N], A ⊆ V, P = types met by A; for t in P and any b in A of
# type s, every a in A∩t has ab+1 non-sqf, so |A∩t| <= H_t(b,N) <= M[s][t].
import sys, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
NT=63
def tname(t):
    k=['7','18','R'][t//21]; mu=['E','1','3'][(t//7)%3]; nu=['0','1','2','4','5','7','8'][t%7]; return k+mu+nu
def evalP(M,P): return sum(min(M[s][t] for s in P) for t in P)
def solve(M,V):
    n=NT; W=[int(max(M[s][t] for s in range(n))) for t in range(n)]
    isC7=[t//21==0 for t in range(n)]; isC18=[t//21==1 for t in range(n)]
    act=[V[t]>0 for t in range(n)]
    rows=[];lo=[];hi=[]
    for t in range(n):
        r=np.zeros(2*n); r[n+t]=1; r[t]=-W[t]; rows.append(r); lo.append(-np.inf); hi.append(0)
        for s in range(n):
            if M[s][t]>=W[t]: continue
            r=np.zeros(2*n); r[n+t]=1; r[s]=W[t]-M[s][t]; rows.append(r); lo.append(-np.inf); hi.append(W[t])
    r=np.zeros(2*n); r[:n]=[0 if isC7[t] else 1 for t in range(n)]; rows.append(r); lo.append(1); hi.append(np.inf)
    r=np.zeros(2*n); r[:n]=[0 if isC18[t] else 1 for t in range(n)]; rows.append(r); lo.append(1); hi.append(np.inf)
    ub=np.concatenate([np.array([1.0 if act[t] else 0.0 for t in range(n)]),np.array(W,float)])
    res=milp(-np.concatenate([np.zeros(n),np.ones(n)]),constraints=LinearConstraint(np.array(rows),lo,hi),
             integrality=np.concatenate([np.ones(n),np.zeros(n)]),bounds=Bounds(np.zeros(2*n),ub),
             options={"mip_rel_gap":0,"time_limit":600})
    P=[t for t in range(n) if res.x[t]>0.5]
    return int(round(-res.fun)), P, res.mip_dual_bound
def read(f):
    out=[]; L=open(f).read().split('\n'); i=0
    while i<len(L):
        if L[i].startswith('N '):
            N=int(L[i].split()[1]); V=list(map(int,L[i+1].split()[1:])); M=[list(map(int,L[i+2+s].split())) for s in range(NT)]
            out.append((N,V,M)); i+=2+NT
        else: i+=1
    return out
if __name__=="__main__":
    for N,V,M in read(sys.argv[1]):
        F,P,db=solve(M,V); c7=(N-7)//25+1
        assert evalP(M,P)==F
        print(f"N={N} F={F} F/N={F/N:.5f} c7={c7} dual_bound={-db:.2f} |P|={len(P)} P={[tname(t) for t in P][:12]}{'...' if len(P)>12 else ''}",flush=True)
