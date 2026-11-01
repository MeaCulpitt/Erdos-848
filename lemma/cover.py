# Max over source sets S (within one class-25 category) of the minimum sub-cover size reproducing the
# served-target set.  Cells (mu,nu): mu in {E,1,3}, nu in {0,1,2,4,5,7,8}; s serves t iff no mod-4 / mod-9 forcing.
import itertools
MU=['E',1,3]; NU=[0,1,2,4,5,7,8]
cells=[(m,n) for m in MU for n in NU]
def serves(s,t):
    (ms,ns),(mt,nt)=s,t
    if ms!='E' and mt!='E' and (ms*mt)%4==3: return False
    if ns!=0 and nt!=0 and (ns*nt)%9==8: return False
    return True
mask=[sum(1<<j for j,t in enumerate(cells) if serves(s,t)) for s in cells]
n=len(cells); best=0; arg=None
# min cover size via BFS over sizes (sizes <= 4 suffice to check)
from functools import lru_cache
for S in range(1,1<<n):
    idx=[i for i in range(n) if S>>i&1]
    U=0
    for i in idx: U|=mask[i]
    # distinct masks only
    ms=sorted(set(mask[i] for i in idx))
    k=None
    for r in range(1,5):
        for c in itertools.combinations(ms,r):
            u=0
            for x in c: u|=x
            if u==U: k=r;break
        if k: break
    if k is None: k=5
    if k>best: best=k; arg=[cells[i] for i in idx]; print(best,arg,flush=True)
print("max min-cover size per category:",best)
