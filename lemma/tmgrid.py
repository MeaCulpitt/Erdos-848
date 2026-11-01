# Full cell-by-cell certification log for Theorem T on [1e7, 1e60]: one line per cell
#   N_lo N_hi slack params    where slack = min(caseI, caseII) of (0.04-G)*N_lo - 0.28 - E(N_hi) ; must be >= 0.
import sys
sys.argv=['x']; exec(open('n0lemma.py').read().split('if __name__')[0])
pts=grid(1e7,1e60); pts.append(1e60); mn=None; bad=0
with open('tmgrid.log','w') as f:
    for i in range(len(pts)-1):
        s,par,G,E1,E2=tm_ok(pts[i],pts[i+1],True)
        f.write(f"{pts[i]:.6e} {pts[i+1]:.6e} slack={s:.1f} {par}\n")
        if mn is None or s<mn[0]: mn=(s,pts[i])
        bad+= s<0
    f.write(f"CELLS={len(pts)-1} FAILURES={bad} MIN_SLACK={mn[0]:.1f} at N_lo={mn[1]:.6e}\n")
print("done", bad, mn)
