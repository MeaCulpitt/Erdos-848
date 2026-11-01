# Old case S1 refined: |A| <= max_{b in R∩V even} #{a in V, a<=N : ab+1 non-sqf}  (all a, not just C7∪C18).
# Local density as a function of the "correlation set" S(b) = {p ≡ 1 mod 4, p>=13 : p^2 | b^2+1}.
# Constraint: prod_{p in S} p^2 | b^2+1 <= N^2+1  => prod_{p in S} p <= ~N. Worst S for given N = smallest primes.
from sympy import primerange
PR=[p for p in primerange(7,2*10**6)]
P1=[p for p in PR if p%4==1]
def dens(S):
    noA=noB=noAB=1.0
    for p in PR:
        if p%4==3: noB*=1-1/p**2; noAB*=1-1/p**2
        else:
            x=1/p**2 if p in S else 0.0
            noA*=1-2/p**2; noB*=1-1/p**2; noAB*=1-3/p**2+x
    # b even in R, coprime to 3 (worst), b mod 25 coprime to 5 (worst: 25-event available)
    # a mod 4: b even => 4∤ab+1. a mod 9: 9|ab+1 iff a ≡ -1/b mod 9 (prob 1/9), and then only need a in V.
    # a in C7∪C18 (prob 2/25): a in V; event 25|ab+1 impossible (b in R). a in R (23/25): 25 event prob 1/23.
    pA=1-noA
    def both(extra):   # P(a∈V' and ab+1 nonsqf) with extra independent small event of prob `extra` for B
        nB=noB*(1-extra); nAB=noAB*(1-extra); return 1-noA-nB+nAB
    # small events for B: 9 (1/9) and 25 (as above)
    def comb(e25): e=1-(1-1/9)*(1-e25); return both(e)
    dC=2/25*(1-noB*(1-1/9)); dR=23/25*comb(1/23)
    return dC+dR, dC, dR
print("old S1 = vR + H7+H18 local density: see n0.py (0.0376)")
for k in range(0,8):
    S=set(P1[:k])
    pr=1
    for p in S: pr*=p
    d,dC,dR=dens(S); print(f"S = first {k} primes ≡1(4) from 13: {sorted(S)} (needs N >~ {pr}): refined S1 density {d:.5f} (C7∪C18 part {dC:.5f}, R part {dR:.5f})")
d,_,_=dens(set(P1)); print(f"S = all: {d:.5f}")
