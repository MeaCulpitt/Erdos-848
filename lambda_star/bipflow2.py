"""Exact best MIXED two-class configuration: X ⊆ C7, Y ⊆ C18, both nonempty, all cross pairs forced by
4, 9 or p^2 (p in extra).  Fix y0 (one per orbit of (a,b) -> (ua, b/u)) and x0 compatible with y0;
then X ⊆ Comp(y0), Y ⊆ Comp(x0), and the rest is a bipartite max-weight independent set (max-flow).
"""
import sys, itertools, time, numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow

def build(extra):
    MU = [('E', 2), (1, 1), (3, 1)]
    NU = [(0, 3)] + [(u, 1) for u in (1, 2, 4, 5, 7, 8)]
    mods = [p*p for p in extra]
    side = [(m, v, tuple(rs), wm*wv) for (m, wm), (v, wv), *rs in itertools.product(MU, NU, *[range(q) for q in mods])]
    m = np.array([0 if s[0] == 'E' else s[0] for s in side]); v = np.array([s[1] for s in side])
    F = ((m[:, None] * m[None, :]) % 4 == 3) & (m[:, None] > 0) & (m[None, :] > 0)
    F |= (v[:, None] > 0) & (v[None, :] > 0) & ((v[:, None] * v[None, :]) % 9 == 8)
    for k, q in enumerate(mods):
        r = np.array([s[2][k] for s in side]); F |= ((r[:, None] * r[None, :] + 1) % q == 0)
    return side, ~F, np.array([s[3] for s in side], dtype=np.int64), mods

def mwis(C, wx, wy):
    nx_, ny_ = len(wx), len(wy)
    if nx_ == 0 or ny_ == 0: return int(wx.sum() + wy.sum())
    ci, cj = np.nonzero(C)
    INF = int(wx.sum() + wy.sum() + 1)
    rows = np.r_[np.zeros(nx_, int), 1 + ci, 1 + nx_ + np.arange(ny_)]
    cols = np.r_[1 + np.arange(nx_), 1 + nx_ + cj, np.full(ny_, 1 + nx_ + ny_)]
    caps = np.r_[wx, np.full(len(ci), INF), wy].astype(np.int32)
    G = csr_matrix((caps, (rows, cols)), shape=(nx_ + ny_ + 2,) * 2)
    return int(wx.sum() + wy.sum()) - maximum_flow(G, 0, nx_ + ny_ + 1).flow_value

def run(extra):
    t0 = time.time()
    side, C, w, mods = build(extra); n = len(side)
    reps = []
    for i, s in enumerate(side):          # orbit reps for y0: mu in {E,1}, nu in {0,1}, r in {1, p, 0}
        if s[0] == 3 or s[1] not in (0, 1): continue
        if all(r in (0, 1, p) for r, p in zip(s[2], extra)): reps.append(i)
    best = (0, None)
    for y0 in reps:
        Xa = np.nonzero(~C[:, y0])[0]
        for x0 in Xa:
            Ya = np.nonzero(~C[x0, :])[0]
            val = mwis(C[np.ix_(Xa, Ya)], w[Xa], w[Ya])
            if val > best[0]: best = (val, (side[x0][:3], side[y0][:3]))
    norm = 36 * int(np.prod(mods)) if mods else 36
    print(f"extra {extra}: {n} types/side, {len(reps)} y0-reps; best mixed X+Y = {best[0]}/{norm} of a class "
          f"-> density {best[0]/norm/25:.6f} (1/50 = 0.02); witness pair {best[1]}; {time.time()-t0:.0f}s", flush=True)

if __name__ == "__main__":
    for ex in [[11], [13], [17]]:
        if ex and ex[0] > int(sys.argv[1] if len(sys.argv) > 1 else 7): break
        run(ex)
