# Exact admissible-m weights for the large-prime lattice lemma (Lemma 4).
# For witness b (only b mod 1800 and the 2-,3-,5-adic profile of b matter) and target residue set T_b mod 1800:
#   g_b(m) = rho_{b0}(m) * 1[m ∈ S_b],  S_b = {(ab+1) u mod 1800 : a ∈ T_b, u ∈ inverse squares of units mod 1800}
#   rho_{b0}(m) = #{s mod b0 : m s^2 ≡ 1 (mod b0)}, b0 = {2,3,5}-part of b: depends only on (v2(b) capped at 3, 3|b, 5|b) and m mod 8,3,5.
# Outputs per system: lam = max_b mean(g_b), cc = max_b sup_{x>=0} (sum_{1<=m<=x} g_b(m) - lam_b x)   [lam_b = mean of g_b]
# Systems: 'tm'  : T_b = {a ∈ C7∪C18 : 4∤ab+1, 9∤ab+1, 25∤ab+1}          (type-matrix C targets)
#          'old' : T_b = {a ∈ C7∪C18 : 25∤ab+1}                              (Sawhney cases, 3 sieved)
import numpy as np, json
MOD=1800
units=[u for u in range(MOD) if u%2 and u%3 and u%5]
isq=sorted({pow((u*u)%MOD,-1,MOD) for u in units})
def rho_b0(m,v2,t3,t5):
    if v2>=1 and m%2==0: return 0
    if t3 and m%3==0: return 0
    if t5 and m%5==0: return 0
    r=1
    if v2==2: r*= 2 if m%4==1 else 0
    if v2>=3: r*= 4 if m%8==1 else 0
    if t3: r*= 2 if m%3==1 else 0
    if t5: r*= 2 if m%5 in (1,4) else 0
    return r
def run(system, even_only=False):
    best_lam=0; best_cc=0; per={}
    for b in range(MOD):
        if even_only and b%2: continue
        T=[a for a in range(MOD) if a%25 in (7,18) and (a*b+1)%25 and
           (system!='tm' or ((a*b+1)%4 and (a*b+1)%9))]
        if not T: continue
        S=np.zeros(MOD,bool)
        for v in {(a*b+1)%MOD for a in T}:
            S[[(v*u)%MOD for u in isq]]=True
        # profiles compatible with b mod 1800: v2 in {v2(b mod 8)} (b%8==0 -> v2>=3), 3|b iff b%3==0, 5|b iff b%5==0
        v2=0 if b%2 else (1 if b%4 else (2 if b%8 else 3)); t3=b%3==0; t5=b%5==0
        g=np.array([rho_b0(m,v2,t3,t5)*S[m] for m in range(MOD)],float)
        lam=g.mean(); cs=np.cumsum(np.r_[g[1:],g[0]])  # sum_{m=1..x}
        x=np.arange(1,MOD+1); cc=max(0.0,(cs-lam*x).max())
        # sup over all x>=0 equals sup over one period since sum over a full period equals lam*MOD
        key=(v2,int(t3),int(t5))
        pl,pc=per.get(key,(0,0)); per[key]=(max(pl,lam),max(pc,cc))
    return per
out={}
for name,eo in [('tm',False),('old',False),('old_even',True)]:
    per=run('tm' if name=='tm' else 'old',eo); out[name]={str(k):v for k,v in per.items()}
    for k,v in sorted(per.items()): print(name,k,"lam=%.4f cc=%.4f"%v)
json.dump(out,open('mconst.json','w'),indent=1)
