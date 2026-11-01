# referee: independent grid-cell check of Theorem T, (zA,zB)=(17,13), N in [6783800, NMAX], ratio 1.01.
# Cell [Nlo,Nhi]: need E(Nhi) <= (0.04-G)*Nlo - 0.28 (case I) and E2(Nhi) <= (0.04-g1)*Nlo-0.28 (case II).
# Primes > 1e7 (only reached when Y>1e7; then p^2 > 2N since N<5e13) cost 1 each, counted by
# pi(Y) <= min(1.25506 Y/ln Y [Rosser-Schoenfeld 1962, x>1], Y/lnY(1+1/lnY+2.51/ln^2Y) [Dusart 2010, x>=355991]).
import sys, math, json, numpy as np
P1=10**7
s=np.ones(P1+1,bool); s[:2]=0
for i in range(2,int(P1**.5)+1):
    if s[i]: s[i*i::i]=0
PR=np.nonzero(s)[0].astype(float); PR1=PR[PR%4==1]; PI1E7=len(PR); assert PI1E7==664579
tail=2.51012/(P1*math.log(P1))
beta=1-(1-1/49)*(1-1/121)*(1-1/169)+float(np.sum(1/PR[PR>13]**2))+tail
alpha=1-(1-2/169)*(1-2/289)+2*float(np.sum(1/PR1[PR1>17]**2))+2*tail
G=2/25*beta+23/25*alpha+1e-12; g1=(1/3+2/3*beta)/25+1e-12
L=8*25*3*7*11*19*23
m=np.arange(L); ok=np.isin(m%8,[1,2,5])&(m%25!=0)
for q in (3,7,11,19,23): ok&=(m%q!=0)
CUM=np.cumsum(ok).astype(np.int64); GP=int(CUM[-1]); del m,ok
def adm_vec(x):            # x: float array; #{2<=m<=x admissible}; exact below 1e17, else (x/L+1)*GP
    big=x>1e17; xs=np.where(big,1.0,x)
    xi=np.floor(xs*(1+1e-12)).astype(np.int64); xi=np.maximum(xi,1)
    return np.where(big,(x/L+1)*GP,((xi//L)*GP+CUM[xi%L]-1).astype(float))
def piup(Y):
    lY=np.log(Y); a=1.25506*Y/lY; d=Y/lY*(1+1/lY+2.51/lY**2); return np.where(Y>=355991,np.minimum(a,d),a)
MC={eval(k):v for k,v in json.load(open('mc.json')).items()}
PK=[1]
for q in [p for p in PR[:60] if p>=7]: PK.append(PK[-1]*int(q))
def pell_vec(N,Y):
    M=(N*N+1)/Y**2; tot=np.zeros_like(Y); j=1
    while True:
        T=(2*N+1)**(1/(2*j-1))
        if T<1+2**.5: break
        mj=((T+1/T)/2)**2*(1+1e-12)
        tot+=adm_vec(np.minimum(M,mj)); j+=1
    return tot
def lat_vec(N,Y,kcap):
    best=np.zeros_like(Y)
    for (v2,t3,t5),(lam,c) in MC.items():
        b0=(1,2,4,8)[v2]*(3**t3)*(5**t5)
        for k in range(min(kcap,len(PK)-1)+1):
            bmin=max(7,b0*PK[k])
            if bmin>N: break
            best=np.maximum(best,2**k*(2*lam*(N+1)/Y+c*math.sqrt(bmin*N+1)/bmin+lam*(N*N+1)/Y**2+c))
    return best
def med_vec(N,Y,which):
    if which=='B':
        p=PR[PR>13]; v=np.where(p*p>N,1.0,np.minimum(np.minimum(38,2*N/(25*p*p)+2),N/(p*p)+1))
    else:
        p=PR1[PR1>17]; v=np.where(p*p>2*N,1.0,2*np.minimum(3,N/(p*p)+1))
    cs=np.r_[0.0,np.cumsum(v)]; out=cs[np.searchsorted(p,np.minimum(Y,P1),side='right')]
    r=1 if which=='B' else 2
    if r*N<=P1**2: return out+np.where(Y>P1,piup(np.maximum(Y,2.0))-PI1E7,0.0)
    # primes p>1e7 with p^2<=rN: excess <= r(N/p^2+1); others 1.  Upper bound r*N*sum_{p>1e7}1/p^2 + r*(pi(Y)-pi(1e7))
    return out+np.where(Y>P1,r*N*tail+r*(piup(np.maximum(Y,2.0))-PI1E7),0.0)
K5={}
for l in open('khis2.txt'): f=l.split(); K5[int(f[0])]=(int(f[5]),int(f[6]))   # K5, K6
def E(N,Kk):
    Y=np.unique(np.logspace(max(1.5,math.log10(N)/3),math.log10(N)+0.3,600))
    ea=float(np.min(med_vec(N,Y,'A')+pell_vec(N,Y)))
    mB=med_vec(N,Y,'B'); eball=float(np.min(mB+lat_vec(N,Y,99)))
    res=[]
    fixed1=2*38*9+38+570; fixed2=38*9+38
    res.append((fixed1+ea+2*eball, fixed2+eball, 'plain'))
    if Kk:
        for k0,K in ((5,Kk[0]),(6,Kk[1])):
            ebk=float(np.min(mB+lat_vec(N,Y,k0-1)))
            res.append((fixed1+ea+2*ebk+K, fixed2+eball+K, f'k0={k0}'))
    return res
NMAX=float(sys.argv[1]); Nlo=float(sys.argv[2]) if len(sys.argv)>2 else 6783800.0; dec={}; worst=(1e300,None)
while Nlo<NMAX:
    RAT=1.01 if Nlo<1e13 else 1.1
    Nhi=math.ceil(Nlo*RAT); best=None
    for E1,E2,tag in E(float(Nhi),K5.get(Nhi)):
        s1=(0.04-G)*Nlo-0.28-E1; s2=(0.04-g1)*Nlo-0.28-E2; sl=min(s1,s2)
        if best is None or sl>best[0]: best=(sl,tag,E1)
    d=int(math.floor(math.log10(Nlo))); r=dec.get(d)
    if r is None or best[0]<r[0]: dec[d]=(best[0],Nlo,best[1],best[0]/Nlo)
    if best[0]<0: print("FAIL cell",Nlo,Nhi,best,flush=True)
    Nlo*=RAT
for d in sorted(dec): print(f"decade 1e{d}: min slack {dec[d][0]:.4g} at Nlo={dec[d][1]:.6g} ({dec[d][2]}) slack/N={dec[d][3]:.5f}")
