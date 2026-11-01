#!/usr/bin/env python3
"""Explicit error bound E(N) for the medium/large-prime parts of the Erdos-848 case bounds, and N0.

usage:
  python3 n0lemma.py tm                 # type-matrix system, Theorem T of README (2 witnesses, omega-refinement)
  python3 n0lemma.py tm-plain           # same without the omega-refinement (Lemma 6 not used)
  python3 n0lemma.py old DELTA [NW] [even|all]   # Sawhney-type case: margin DELTA, NW witness counts H over C7∪C18
  python3 n0lemma.py old-table          # N0 for DELTA in {0.0016,0.0024,0.005,0.01,0.015}, NW=1,2
Needs (built by tables.py, primecount.py, mconst2.py, omegaV.c, vk2.py): primes1e7.npy pc.npy pellcum.npy
mconst.json omegaV1e7.txt omegaV1e8.txt v2grid.json.

Check performed.  Grid N_0 < N_1 < ... (ratio 1.01 up to 1e13, then 1.1, up to 1e60).  Each component of E is
nondecreasing in N for fixed parameters (z, Y, k0), so with parameters optimised at N_{i+1}:
      E(N) <= E(N_{i+1}) <= delta*N_i - 0.28 <= delta*N - 0.28        for all N in [N_i, N_{i+1}],
and c7(N) >= (N-7)/25, so  (0.04-delta)*N + E(N) <= c7(N).  N0 = left end of the first cell after the last failure.
Lemma numbers refer to README.md."""
import sys, os, json, math, numpy as np
D=os.path.dirname(os.path.abspath(globals().get('__file__','./x')))
PR=np.load(f'{D}/primes1e7.npy').astype(np.float64); PR1=PR[PR%4==1]
P1=1e7
PC=np.load(f'{D}/pc.npy')                       # rows (x, pi(x), pi(x;4,1)), x = 0, 1e5, ..., 4e9
PELL=np.load(f'{D}/pellcum.npy'); LP=len(PELL); GP=int(PELL[-1])
MC=json.load(open(f'{D}/mconst.json'))
def _K(fn):
    a=np.loadtxt(f'{D}/{fn}',dtype=np.int64); return a
KT=[_K('omegaV1e7.txt'), _K('omegaV1e8.txt')]
# ---------------- prime-counting helpers (rigorous upper/lower bounds) ----------------
def T_sq(x):  # sum_{p>x} 1/p^2 <= int_x^inf 2 pi(t)/t^3 dt <= 2*1.25506/(x ln x)   (x >= 1e7)
    return 2.51012/(x*math.log(x))
def sum_inv_sq_gt(z, cls1=False):
    arr=PR1 if cls1 else PR; return float(np.sum(1/arr[arr>z]**2))+T_sq(P1)
def pi_up(x, cls1=False):
    if x<2: return 0
    if x<=P1: return int(np.searchsorted(PR1 if cls1 else PR, math.floor(x), side='right'))
    if x<=PC[-1,0]:
        i=int(np.searchsorted(PC[:,0], x, side='left')); return int(PC[i,2 if cls1 else 1])
    return 1.25506*x/math.log(x)                # Rosser-Schoenfeld
def pi_low_exact(x, cls1=False):                # exact for x <= 1e7
    return int(np.searchsorted(PR1 if cls1 else PR, math.floor(min(x,P1)), side='right'))
# ---------------- Lemma 2: medium primes ----------------
def medium_curve(N, z, roots, cls1, e, f, g):
    """Return function Y -> sum over primes z<p<=Y (p≡1 mod 4 if cls1) of the excess of Lemma 2:
         roots*min(e, f*N/p^2+g, N/p^2+1)   if p^2 <= roots*N,      1   if p^2 > roots*N."""
    arr=PR1 if cls1 else PR; thr=math.sqrt(roots*N); a=min(thr,P1)
    p=arr[(arr>z)&(arr<=a)]
    ex=roots*np.minimum(np.minimum(e, f*N/p**2+g), N/p**2+1); cs=np.concatenate([[0.0],np.cumsum(ex)])
    extra_mid = roots*(N*T_sq(P1)) if thr>P1 else 0.0       # primes in (1e7, thr]: roots*(N/p^2+1)
    def F(Y):
        if Y<=z: return 0.0
        tot=float(cs[int(np.searchsorted(p, min(Y,a), side='right'))])
        if thr>P1 and Y>P1: tot+=extra_mid+roots*pi_up(min(Y,thr),cls1)
        if Y>thr: tot+= (pi_up(Y,cls1)-pi_low_exact(thr,cls1)) if thr<=P1 else pi_up(Y,cls1)
        return tot
    return F
# ---------------- Lemma 3: Pell (large primes for x^2+1) ----------------
def adm_count(x):          # #{2<=m<=x : m admissible (Lemma 3)}; exact below 1e15, upper bound above
    if x<2: return 0
    if x<1e15:
        x=int(x); return (x//LP)*GP+int(PELL[x%LP])-1        # -1: m=1 is admissible in the table
    return (x/LP+1)*GP
def pell(N, Y):
    M=(N*N+1)/(Y*Y)            # x^2+1 = m p^2, p > Y  =>  m < M
    if M<2: return 0
    tot=0; j=1; L2=2*N+1
    while True:
        T=L2**(1.0/(2*j-1))
        if T<2.414: break
        mj=(T+1/T)**2/4*(1+1e-9)+1           # all m with sqrt(m-1)+sqrt(m) <= T  (safety margin)
        tot+=adm_count(min(M,mj)); j+=1
    return tot
# ---------------- Lemma 4/5: lattice for a witness b, primes p > Y ----------------
PK=[1]
for q in PR[3:60]: PK.append(PK[-1]*int(q))   # products of the first k primes >= 7
def lattice(N, Y, msys, kcap=99):
    best=0.0
    for key,(lam,cc) in MC[msys].items():
        v2,t3,t5=eval(key); b0=(1,2,4,8)[v2]*(3 if t3 else 1)*(5 if t5 else 1)
        for k,Pk in enumerate(PK):
            bmin=max(7,b0*Pk)
            if bmin>N or k>kcap: break
            val=2**k*(2*lam*(N+1)/Y + cc*math.sqrt(bmin*N+1)/bmin + lam*(N*N+1)/(Y*Y) + cc)
            if val>best: best=val
    return best
# ---------------- densities ----------------
def alpha_up(zA):
    pr=[p for p in PR1 if 13<=p<=zA]; return 1-math.prod(1-2/p**2 for p in pr)+2*sum_inv_sq_gt(zA,True)
def beta_up(zB):
    pr=[p for p in PR if 7<=p<=zB]; return 1-math.prod(1-1/p**2 for p in pr)+sum_inv_sq_gt(zB)
def kA_of(zA): return int(np.sum((PR1>=13)&(PR1<=zA)))
def kB_of(zB): return int(np.sum((PR>=7)&(PR<=zB)))
# ---------------- assembled errors ----------------
def Ygrid(N): return np.logspace(1, math.log10(N)+0.5, 100)
def EA(N, zA):          # Lemma 2 (A side, U = all of R: e=3, class count 23/25 N/p^2 + 3) + Lemma 3, optimised in Y
    F=medium_curve(N,zA,2,True,3.0,23/25,3.0); return min(F(Y)+pell(N,Y) for Y in Ygrid(N))
def EB(N, zB, msys, kcap, e, f, g):   # Lemma 2 (B side) + Lemma 4, optimised in Y (Y may depend on the witness)
    F=medium_curve(N,zB,1,False,e,f,g); return min(F(Y)+lattice(N,Y,msys,kcap) for Y in Ygrid(N))
def K_omega(N, k0):     # #{b<=N in V : omega(b1) >= k0}, rigorous upper bound via next checkpoint; None if unknown
    if k0>9: return 0
    for t in KT:
        if N<=t[-1,0]:
            i=int(np.searchsorted(t[:,0],N,side='left')); return int(t[i,k0])
    return None
V2=None
def tm_bound(N, refine=True):
    """min over parameters of  E_total(N) - (0.04 - G)*N  (must be <= -0.28 + ...); returns (slack, params)
       slack = (0.04-G)*N_lo... computed by caller.  Here we return list of (G, E_total, params) candidates."""
    global V2
    if V2 is None: V2=json.load(open(f'{D}/v2grid.json'))
    out=[]
    eAs={zA:EA(N,zA) for zA in (17,29,37,41)}
    for zB in (13,17,19,23):
        kB=kB_of(zB); bB=beta_up(zB); g1=(1/3+2/3*bB)/25
        EB_all=EB(N,zB,'tm',99,38.0,2/25,2.0)
        caps=[99]+([4,5,6,7,8] if refine else [])
        for kcap in caps:
            Kc=0 if kcap==99 else K_omega(N,kcap+1)
            if Kc is None: continue
            EBk=EB_all if kcap==99 else EB(N,zB,'tm',kcap,38.0,2/25,2.0)
            for zA in (17,29,37,41):
                kA=kA_of(zA); G=V2[f"{zA},{zB}"]
                EIE=2*38*(1+2**kB)+38+57*(1+3**kA)
                E1=EIE+eAs[zA]+2*EBk+Kc                     # case I  (good witnesses)
                E2=38*(1+2**kB)+38+EB_all+Kc                 # case II (A' inside one C class): density g1
                out.append((G,E1,g1,E2,dict(zA=zA,zB=zB,k0=kcap+1 if kcap<99 else None)))
    return out
def tm_ok(Nlo, Nhi, refine=True):
    best=None
    for G,E1,g1,E2,par in tm_bound(Nhi,refine):
        s1=(0.04-G)*Nlo-0.28-E1; s2=(0.04-g1)*Nlo-0.28-E2
        s=min(s1,s2)
        if best is None or s>best[0]: best=(s,par,G,E1,E2)
    return best
def old_E(N, nw, msys, zA=17, zB=23):
    kA=kA_of(zA); kB=kB_of(zB)+2                      # primes 2,3 also in the IE for the old system
    EIE=3*(1+3**kA)+nw*2*(1+2**kB)
    return EIE+EA(N,zA)+nw*EB(N,zB,msys,99,2.0,2/25,2.0)
def grid(Nstart, Nmax=1e60):
    pts=[]; N=Nstart
    while N<Nmax: pts.append(N); N*=1.01 if N<1e13 else 1.1
    return pts
def find_N0(check, Nstart, Nmax=1e60):
    pts=grid(Nstart,Nmax); last_bad=-1
    for i in range(len(pts)-1):
        if not check(pts[i],pts[i+1]): last_bad=i
    return pts[last_bad+1]
if __name__=="__main__":
    mode=sys.argv[1]
    if mode in ('tm','tm-plain'):
        ref = mode=='tm'
        for N in [3e6,5e6,7e6,1e7,1.5e7,2e7,3e7,1e8]:
            s,par,G,E1,E2=tm_ok(N,N,ref)
            print(f"N={N:.3g}: best params {par}  G={G:.6f}  E_caseI={E1:.0f} ({E1/N:.5f}N)  E_caseII={E2:.0f}  slack={s:.0f}",flush=True)
        N0=find_N0(lambda a,b: tm_ok(a,b,ref)[0]>=0, 3e6)
        print(f"N0({mode}) = {N0:.5g}")
    elif mode=='old':
        d=float(sys.argv[2]); nw=int(sys.argv[3]) if len(sys.argv)>3 else 1
        msys='old_even' if (len(sys.argv)<=4 or sys.argv[4]=='even') else 'old'
        print(f"old delta={d} nw={nw} {msys}: N0 = {find_N0(lambda a,b: old_E(b,nw,msys)<=d*a-0.28, 1e4):.4g}")
    elif mode=='old-table':
        for nw,msys in ((1,'old_even'),(2,'old')):
            for d in (0.0016,0.0024,0.005,0.01,0.015,0.02):
                print(f"nw={nw} ({msys}) delta={d}: N0 = {find_N0(lambda a,b: old_E(b,nw,msys)<=d*a-0.28, 1e4):.4g}",flush=True)
