# Asymptotic local-density model of M(s,t) = max_b #{a in T_t ∩ V, a<=N : ab+1 non-sqf}/N, b in T_s ∩ V.
# Types t=(kappa,mu): kappa in {7,18,R} (a mod 25 class), mu in {E,1,3} (a even / 1 mod 4 / 3 mod 4).
# Events A_p: p^2 | a^2+1 ; B_p: p^2 | ab+1.  Independent over p by CRT. Worst b: coprime to all small p,
# and with p^2 | b^2+1 for every p in S (then A_p∩B_p has density 1/p^2; otherwise A_p∩B_p = ∅).
import itertools
from sympy import primerange
PR=[p for p in primerange(3,2*10**6) if p!=5]
def prods(S):
    noB=noA=noAB=1.0
    for p in PR:
        if p%4==3: noB*=1-1/p**2; noAB*=1-1/p**2
        else:
            x=1/p**2 if p in S else 0.0
            noA*=1-2/p**2; noB*=1-1/p**2; noAB*=1-3/p**2+x
    return noA,noB,noAB
def matrix(S):
    noA,noB,noAB=prods(S)
    K=['7','18','R']; MU=['E','1','3']; T=[(k,u) for k in K for u in MU]
    def m(s,t):
        ks,ms=s; kt,mt=t
        two = ms!='E' and mt!='E' and ms!=mt
        w=(1/25 if kt!='R' else 23/25)*(1/2 if mt=='E' else 1/4)
        if kt!='R':
            if two or ks==kt: return w
            return w*(1-noB)
        f5 = 1/23 if ks=='R' else 0.0     # 25 | ab+1 forces a ≡ -1/b mod 25, an R class iff b in R
        if two: return w*(1-noA)
        # P(not B) for a in R-classes includes the 25-event; P(not A and not B)
        nB=noB*(1-f5); nAB=noAB*(1-f5)
        return w*(1-noA-nB+nAB)
    return T,{(s,t):m(s,t) for s in T for t in T}
def worst(T,M,allow=lambda P:True):
    best=[]
    for r in range(1,len(T)+1):
        for P in itertools.combinations(T,r):
            if all(k=='7' for k,_ in P) or all(k=='18' for k,_ in P): continue
            if not allow(P): continue
            v=sum(min(M[s,t] for s in P) for t in P); best.append((v,P))
    best.sort(reverse=True); return best
if __name__=="__main__":
    P1=[p for p in PR if p%4==1]
    for name,S in [("S=empty",set()),("S={13}",{13}),("S=all",set(P1))]:
        T,M=matrix(S)
        b=worst(T,M)
        print(f"{name}: worst {b[0][0]:.5f} at {b[0][1]}")
        for v,P in b[1:4]: print(f"      next {v:.5f} {P}")
        if name=="S=all":
            print("matrix rows=source s, cols=target t (x1e4)")
            print("        "+" ".join(f"{k+u:>6s}" for k,u in T))
            for s in T: print(f"{s[0]+s[1]:>6s}  "+" ".join(f"{1e4*M[s,t]:6.1f}" for t in T))
