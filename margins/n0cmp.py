# Crude comparison of the analytic threshold: reuse ../n0.py's explicit error E(N) (for one H(b) count plus vR),
# and ask when  k*E(N) < margin*N  for margin 0.0024 (old) vs 0.02 (type matrix), k = number of witness counts.
exec(open('../n0.py').read().split('for k in range(6,16)')[0])
import math
for margin,k,lab in [(0.04-mainS1,1,"old S1"),(0.02,1,"type matrix, 1 witness"),(0.02,9,"type matrix, 9 witnesses"),(0.02,63,"type matrix, 63 witnesses")]:
    lo=None
    for e10 in [x/4 for x in range(24,200)]:
        N=10**e10; err,Y=E(N)
        if k*err<margin*N: lo=e10; break
    print(f"{lab:28s} margin {margin:.4f}: first N=10^{lo} with k*E(N) < margin*N")
