import sys,math,numpy as np
sys.argv=['x']; exec(open('eref.py').read().split('K5={')[0])
def run(N,kcap,K,Ymax=1e7):
    Ys=np.unique(np.round(np.logspace(2,math.log10(min(N,Ymax)),300)))
    ea=min(medA(N,17,Y)+pell(N,Y) for Y in Ys); eb=min(medB(N,13,Y)+lattice(N,Y,kcap) for Y in Ys)
    eball=eb if kcap==99 else min(medB(N,13,Y)+lattice(N,Y,99) for Y in Ys)
    E1=2*38*9+38+570+ea+2*eb+K; E2=38*9+38+eball+K
    return E1,E2
# grid cell at N0: E(N_hi) <= delta*N_lo - 0.28 ?
Nlo=6783800; Nhi=Nlo*1.01
for K in (335,):
    E1,E2=run(Nhi,4,K); print(f"cell [{Nlo},{Nhi:.0f}] k0=5: E1(Nhi)={E1:.0f}  delta*Nlo-0.28={(0.04-G)*Nlo-0.28:.0f}  ok={E1<=(0.04-G)*Nlo-0.28}; caseII ok={E2<=(0.04-g1)*Nlo-0.28}",flush=True)
for N in (2e7,5e7,1e8,1e9,1e10,1e11):
    E1,E2=run(N*1.01,99,0); print(f"unrefined cell at {N:.0e}: slackI={(0.04-G)*N-0.28-E1:.0f} ({E1/N:.5f}N)",flush=True)
