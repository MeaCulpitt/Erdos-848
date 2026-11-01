"""Exact best two-class configuration X ⊆ C7, Y ⊆ C18 with every cross pair forced by some modulus in Q,
Q = {4, 9} ∪ {p^2 : p in extra primes}.  Inside each class 25 | ab+1, so validity = all cross pairs forced.
Types on each side: (a mod 4 class E/1/3, a mod 9 class with 3|a merged, a mod p^2 for each extra p).
Max weight independent set in the bipartite CONFLICT graph = total - min vertex cover = total - maxflow.
Density = (weight / (36 * prod p^2)) / 25.
"""
import sys, itertools, numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow

def run(extra):
    MU = [('E', 2), (1, 1), (3, 1)]
    NU = [(0, 3)] + [(u, 1) for u in (1, 2, 4, 5, 7, 8)]
    mods = [p*p for p in extra]
    res_lists = [list(range(q)) for q in mods]
    side = []
    for (m, wm), (v, wv), *rs in itertools.product(MU, NU, *res_lists):
        side.append((m, v, tuple(rs), wm*wv))
    n = len(side)
    # cross forcing between a in X (type i) and b in Y (type j)
    m = np.array([0 if s[0] == 'E' else s[0] for s in side]); v = np.array([s[1] for s in side])
    F = ((m[:, None] * m[None, :]) % 4 == 3) & (m[:, None] > 0) & (m[None, :] > 0)
    F |= (v[:, None] > 0) & (v[None, :] > 0) & ((v[:, None] * v[None, :]) % 9 == 8)
    for k, q in enumerate(mods):
        r = np.array([s[2][k] for s in side])
        F |= ((r[:, None] * r[None, :] + 1) % q == 0)
    conflict = ~F
    w = np.array([s[3] for s in side], dtype=np.int64)
    # flow network: 0 = source, 1..n = X, n+1..2n = Y, 2n+1 = sink
    INF = int(w.sum() * 4 + 10)
    ci, cj = np.nonzero(conflict)
    rows = np.r_[np.zeros(n, int), 1 + ci, n + 1 + np.arange(n)]
    cols = np.r_[1 + np.arange(n), n + 1 + cj, np.full(n, 2*n + 1)]
    caps = np.r_[w, np.full(len(ci), INF), w].astype(np.int32 if INF < 2**31 else np.int64)
    G = csr_matrix((caps, (rows, cols)), shape=(2*n + 2, 2*n + 2))
    f = maximum_flow(G, 0, 2*n + 1).flow_value
    total = 2 * int(w.sum())
    best = total - f
    norm = 36 * int(np.prod(mods)) if mods else 36
    lam = best / norm / 25
    print(f"extra primes {extra}: {n} types per side, conflict density {conflict.mean():.3f}, "
          f"best X+Y = {best}/{norm} of a class  ->  density {lam:.6f}  (1/50 = 0.020000)", flush=True)
    return lam

if __name__ == "__main__":
    for ex in ([], [7], [11], [13], [17], [19], [7, 11]):
        run(ex)
