# referee: exact (integer) branch-and-bound proof that V_2 <= F = 2/25*beta + 23/25*alpha_s + 23/25*tailA
# over ALL type-sets P not inside C7-types and not inside C18-types; independent of HiGHS.
import sys, itertools, math
from fractions import Fraction as Fr
CATS=['7','18','R']; MUS=['E',1,3]; NUS=[0,1,2,4,5,7,8]
T=[(c,m,n) for c in CATS for m in MUS for n in NUS]; n=len(T)
def wt(t):  # 900*w_t, integer
    c,m,nu=t; base=(36 if c!='R' else 828); return base*(Fr(1,2) if m=='E' else Fr(1,4))*(Fr(1,3) if nu==0 else Fr(1,9))
W9=[int(wt(t)) for t in T]; assert all(wt(t)==W9[i] for i,t in enumerate(T)); assert sum(W9)==900
def forced(s,t):
    (cs,ms,ns),(ct,mt,nt)=s,t
    if ct=='R': return False
    if cs==ct: return True
    if ms!='E' and mt!='E' and (ms*mt)%4==3: return True
    if ns!=0 and nt!=0 and (ns*nt)%9==8: return True
    return False
FM=[sum(1<<j for j in range(n) if forced(T[i],T[j])) for i in range(n)]
Cmask=sum(1<<j for j in range(n) if T[j][0]!='R'); Rmask=((1<<n)-1)^Cmask
C7=sum(1<<j for j in range(n) if T[j][0]=='7'); C18=sum(1<<j for j in range(n) if T[j][0]=='18')
D=10**15
def up(x): return math.ceil(Fr(x)*D)        # rational upper rounding
beta=Fr(sys.argv[1]); alpha_s=Fr(sys.argv[2]); cR=Fr(sys.argv[3])
bI=math.ceil(beta*D); aI=math.ceil(alpha_s*D); cI=math.ceil(cR*D)
def wsum(mask):
    s=0
    while mask: j=(mask&-mask).bit_length()-1; s+=W9[j]; mask&=mask-1
    return s
# value*D*900 for witness-forced mask F and target set Tset
def val(Fmask,Tset):
    nC=wsum(Tset&Cmask); nF=wsum(Tset&Cmask&Fmask); nR=wsum(Tset&Rmask)
    return bI*nC+(D-bI)*nF+aI*nR+(cI*900 if Tset&Rmask else 0)
Ftarget=bI*72+aI*828+cI*900      # 900*D*F (beta*2/25*900=72 beta)
order=sorted(range(n),key=lambda j:(-(n-bin(FM[j]&Cmask).count('1')), T[j][0]=='R'))
nodes=0; worst=[0,None]
def ub(In,Tset):
    best=None; L=[j for j in range(n) if In>>j&1]
    for a in range(len(L)):
        fa=FM[L[a]]; v=val(fa,Tset); best=v if best is None or v<best else best
        for b in range(a+1,len(L)):
            v=val(fa&FM[L[b]],Tset)
            if v<best: best=v
    return best
def rec(k,In,Out):
    global nodes; nodes+=1
    Tset=((1<<n)-1)^Out
    if not (Tset & ~C7) or not (Tset & ~C18): return
    if In:
        u=ub(In,Tset)
        if u<=Ftarget: return
    if k==n:
        # leaf: P=In (=Tset), value u > F  -> counterexample
        worst[0]=max(worst[0],u); worst[1]=[T[j] for j in range(n) if In>>j&1]; return
    j=order[k]
    rec(k+1,In|(1<<j),Out); rec(k+1,In,Out|(1<<j))
rec(0,0,0)
print("nodes",nodes,"counterexample" if worst[1] else "PROVED: V_2 <= F", worst[0]/(900*D) if worst[1] else "", "F=",Ftarget/(900*D))
