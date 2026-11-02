"""Exact analysis of 'ab+1 never k-free' for N <= N_k (the analytic threshold of kfree_analytic.py), for one k.

Vertices: V_k cap [N_k], listed directly as the roots of x^2 = -1 mod p^k (p = 5 or p = 1 mod 4) with p^k <= N_k^2 + 1.
Edges:    ab+1 not k-free, tested against every prime p with p^k <= N_k^2 + 1 (no other prime can have p^k | ab+1).

Mode 'clique' (all N <= N_k): at each vertex value v (the graph is constant on [v, next vertex)), enumerate all maximum
cliques; report every interval where the maximum is not c_r(N) or where a maximum set is not a full class.
Mode 'cells' (large vertex sets): exact cliques up to M0, then the one-witness bound on cells [lo, hi] of ratio 1.2:
  max_b H_r(b, hi) + max_b H_{q-r}(b, hi) + #(vertices <= hi outside both classes) < c_r(lo)."""
import sys, math, bisect, json
import igraph as ig
from sympy import primerange

def roots_mod_pk(p, k):
    m = p; t = next(t for t in range(2, p) if (t * t + 1) % p == 0)
    for _ in range(1, k):
        m2 = m * p; t = (t - (t * t + 1) * pow(2 * t, -1, m2)) % m2; m = m2
    assert (t * t + 1) % m == 0
    return [t, m - t]

def setup(k, Nmax):
    q = 5**k; r = min(roots_mod_pk(5, k))
    bound = Nmax * Nmax + 1
    from sympy import integer_nthroot
    ps = [p for p in primerange(2, integer_nthroot(bound, k)[0] + 2) if p**k <= bound]
    V = set()
    for p in ps:
        if p == 5 or p % 4 == 1:
            for t in roots_mod_pk(p, k):
                V.update(range(t, Nmax + 1, p**k))
    V.discard(0)
    V = sorted(V)
    pk = [p**k for p in ps]
    def adj(a, b):
        x = a * b + 1
        return any(x % m == 0 for m in pk if m <= x)
    return q, r, ps, V, adj

def c_of(N, r, q): return (N - r) // q + 1 if N >= r else 0

def run_clique(k, Nmax, V, adj, q, r, start=1):
    idx = {v: i for i, v in enumerate(V)}
    edges = [(i, j) for i in range(len(V)) for j in range(i + 1, len(V)) if adj(V[i], V[j])]
    G = ig.Graph(n=len(V), edges=edges)
    out = []; prev = None
    for n in range(len(V)):
        v = V[n]; nxt = V[n + 1] - 1 if n + 1 < len(V) else Nmax
        if nxt < start: continue
        H = G.subgraph(range(n + 1)); w = H.clique_number()
        c = max(c_of(v, r, q), c_of(v, q - r, q))
        sets = sorted(tuple(sorted(V[t] for t in cl)) for cl in H.largest_cliques())
        full = {tuple(x for x in V[:n + 1] if x % q == r), tuple(x for x in V[:n + 1] if x % q == q - r)}
        odd = [s for s in sets if s not in full]
        key = (w, c, tuple(odd))
        if w != c or odd:
            if key == prev and out: out[-1]["N_to"] = nxt          # same exception continues: extend the interval
            else: out.append(dict(N_from=v, N_to=nxt, max=w, c_r=c, extra_maximisers=[list(s) for s in odd][:6], n_extra=len(odd)))
        prev = key
    return out

def H_counts(cls, Vn, adj, N):
    best = 0
    for b in Vn:
        if b in cls: continue
        h = sum(1 for a in cls if a <= N and adj(a, b))
        best = max(best, h)
    return best

def run_cells(k, Nmax, V, adj, q, r, M0, ratio=1.2):
    res = []; lo = M0
    while lo < Nmax:
        hi = min(int(lo * ratio) + 1, Nmax)
        Vn = [v for v in V if v <= hi]
        Cr = [v for v in Vn if v % q == r]; Cs = [v for v in Vn if v % q == q - r]
        setr, sets_ = set(Cr), set(Cs)
        B = H_counts(Cr, [b for b in Vn if b not in setr], adj, hi) + H_counts(Cs, [b for b in Vn if b not in sets_], adj, hi) \
            + sum(1 for v in Vn if v % q not in (r, q - r))
        res.append((lo, hi, B, c_of(lo, r, q), B < c_of(lo, r, q)))
        lo = hi
    return res

if __name__ == "__main__":
    k = int(sys.argv[1]); Nmax = int(float(sys.argv[2])); mode = sys.argv[3] if len(sys.argv) > 3 else "clique"
    q, r, ps, V, adj = setup(k, Nmax)
    print(f"k={k}: q=5^{k}={q}, r={r}, N_k={Nmax}, |V_k cap [N_k]|={len(V)}, primes tested={len(ps)}", flush=True)
    if mode == "clique":
        ex = run_clique(k, Nmax, V, adj, q, r)
        print(json.dumps(dict(k=k, exceptions=ex)))
    else:
        M0 = int(float(sys.argv[4]))
        ex = run_clique(k, M0, [v for v in V if v <= M0], adj, q, r)
        print(json.dumps(dict(k=k, exceptions_below_M0=ex)), flush=True)
        cells = run_cells(k, Nmax, V, adj, q, r, M0)
        print(json.dumps(dict(k=k, cells=len(cells), failures=[c for c in cells if not c[4]], worst=max(c[2] / c[3] for c in cells))))
