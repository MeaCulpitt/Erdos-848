import sys,math,numpy as np
sys.argv=['x']; exec(open('eref.py').read().split('K5={')[0])
K={int(l.split()[0]):int(l.split()[5]) for l in open('khis.txt')}
Nlo=6783800.0; worst=1e18
while Nlo<1.0e7:
    Nhi=math.ceil(Nlo*1.01); Ys=np.unique(np.round(np.logspace(4,6,250)))
    ea=min(medA(Nhi,17,Y)+pell(Nhi,Y) for Y in Ys); eb=min(medB(Nhi,13,Y)+lattice(Nhi,Y,4) for Y in Ys)
    eball=min(medB(Nhi,13,Y)+lattice(Nhi,Y,99) for Y in Ys)
    E1=2*38*9+38+570+ea+2*eb+K[Nhi]; E2=38*9+38+eball+K[Nhi]
    s1=(0.04-G)*Nlo-0.28-E1; s2=(0.04-g1)*Nlo-0.28-E2; worst=min(worst,s1,s2)
    print(f"[{Nlo:.0f},{Nhi}] K5={K[Nhi]} E1={E1:.0f} slackI={s1:.0f} slackII={s2:.0f}",flush=True)
    Nlo*=1.01
print("min slack",worst)
