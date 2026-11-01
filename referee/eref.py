# referee: independent E_I, E_II at given N for (zA,zB,k0)=(17,13,5)
import numpy as np, math, json, sys
P1=10**7
s=np.ones(P1+1,bool); s[:2]=0
for i in range(2,int(P1**.5)+1):
    if s[i]: s[i*i::i]=0
PR=np.nonzero(s)[0].astype(float); PR1=PR[PR%4==1]
tail=2.51012/(P1*math.log(P1))   # sum_{p>1e7}1/p^2 (Rosser-Schoenfeld)
beta=1-(1-1/49)*(1-1/121)*(1-1/169)+float(np.sum(1/PR[PR>13]**2))+tail
alpha=1-(1-2/169)*(1-2/289)+2*float(np.sum(1/PR1[PR1>17]**2))+2*tail
G=2/25*beta+23/25*alpha; g1=(1/3+2/3*beta)/25
print("beta",beta,"alpha",alpha,"G",G,"delta",0.04-G,"g1",g1)
L=8*25*3*7*11*19*23
m=np.arange(L); ok=np.isin(m%8,[1,2,5])&(m%25!=0)
for q in (3,7,11,19,23): ok&=(m%q!=0)
CUM=np.cumsum(ok).astype(np.uint32); GP=int(CUM[-1]); del m,ok
def adm(x):  # #{2<=m<=x admissible}
    x=int(math.floor(x))
    if x<2: return 0
    return (x//L)*GP+int(CUM[x%L])-1
def pell(N,Y):
    M=(N*N+1)/(Y*Y); tot=0; j=1
    while True:
        T=(2*N+1)**(1/(2*j-1))
        if T<1+2**.5: break
        mj=((T+1/T)/2)**2*(1+1e-12)
        tot+=adm(min(M,mj)); j+=1
    return tot
MC={eval(k):v for k,v in json.load(open('mc.json')).items()}
PK=[1]
for q in [p for p in PR[:40] if p>=7]: PK.append(PK[-1]*int(q))
def lattice(N,Y,kcap):
    best=0
    for (v2,t3,t5),(lam,c) in MC.items():
        b0=(1,2,4,8)[v2]*(3**t3)*(5**t5)
        for k in range(kcap+1):
            bmin=max(7,b0*PK[k])
            if bmin>N: break
            best=max(best,2**k*(2*lam*(N+1)/Y+c*math.sqrt(bmin*N+1)/bmin+lam*(N*N+1)/Y**2+c))
    return best
def medB(N,zB,Y):
    p=PR[(PR>zB)&(PR<=Y)]; big=p*p>N
    return float(np.sum(np.where(big,1.0,np.minimum(np.minimum(38,2*N/(25*p*p)+2),N/(p*p)+1))))
def medA(N,zA,Y):
    p=PR1[(PR1>zA)&(PR1<=Y)]; big=p*p>2*N
    return float(np.sum(np.where(big,1.0,2*np.minimum(3,N/(p*p)+1))))
def EB(N,kcap):
    Ys=np.unique(np.round(np.logspace(2,math.log10(N),400)))
    return min((medB(N,13,Y)+lattice(N,Y,kcap),Y) for Y in Ys)
def EA(N):
    Ys=np.unique(np.round(np.logspace(2,math.log10(N),400)))
    return min((medA(N,17,Y)+pell(N,Y),Y) for Y in Ys)
K5={6783800:329,6851638:335,7000000:348,10000000:672}
for N in map(float,sys.argv[1:]):
    ea,ya=EA(N); eb4,yb=EB(N,4); eball,yb2=EB(N,99); K=K5.get(int(N))
    fixed=2*38*9+38+57*10
    E1=fixed+ea+2*eb4+K; E2=38*9+38+eball+K
    print(f"N={N:.7g} EA={ea:.0f}(Y={ya:.0f}) EB4={eb4:.0f}(Y={yb:.0f}) EBall={eball:.0f} K5={K} E1={E1:.0f} E2={E2:.0f} "
          f"slackI={(0.04-G)*N-0.28-E1:.0f} slackII={(0.04-g1)*N-0.28-E2:.0f}",flush=True)
