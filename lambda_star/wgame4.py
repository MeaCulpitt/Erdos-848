"""General local witness game (exact), igraph/Cliquer backend.
   A ⊆ [N], f(a,b) and f(b,a) not k-free for all a,b in A (a=b allowed).
Residues mod M = prod_{p in S} p^k; forced(r,s): each order divisible by p^k for some p in S.
Local optimum = largest forced clique (loops required).  All optimal classes are collected
iteratively; mixed optimum = largest clique not contained in any optimal class.
beta = large-prime cross density (worst witness); rigidity = best share of an optimal class kept
by one outside element.  Heuristic local model: densities only, independence assumed.
"""
import sys, math, numpy as np, igraph as ig
from sympy import primerange

def densities(f, k, S, pmax=200):
    lb = 0.0
    for p in primerange(2, pmax):
        if p in S: continue
        q = p**k
        if q > 10**5: break
        x = np.arange(q)
        bs = range(q) if q <= 2000 else np.random.default_rng(0).integers(0, q, 2000)
        mx = max(int(np.count_nonzero(f(x, int(b)) % q == 0)) for b in bs)
        lb += math.log1p(-min(mx/q, .999))
    return 1-math.exp(lb)

def run(name, f, k, S):
    M = int(np.prod([p**k for p in S])); R = np.arange(M)
    F1 = np.zeros((M, M), bool); F2 = np.zeros((M, M), bool)
    for p in S:
        q = p**k; a = R[:, None] % q; b = R[None, :] % q
        F1 |= (f(a, b) % q == 0); F2 |= (f(b, a) % q == 0)
    F = F1 & F2; loop = np.diag(F).copy()
    beta = densities(f, k, S)
    V = [r for r in range(M) if loop[r]]; n = len(V)
    sub = F[np.ix_(V, V)]
    iu, ju = np.nonzero(np.triu(sub, 1))
    G = ig.Graph(n=n, edges=list(zip(iu.tolist(), ju.tolist())))
    nb = [set(G.neighbors(i)) for i in range(n)]
    def one_max(nodes):
        nodes = list(nodes)
        if not nodes: return []
        H = G.induced_subgraph(nodes); c = H.largest_cliques()[0]
        return [nodes[i] for i in c]
    K = one_max(range(n)); s1 = len(K)
    opts = [frozenset(K)]
    def best_outside():
        U = set().union(*opts); inside = lambda C: any(set(C) <= O for O in opts)
        best = (0, None)
        for v in range(n):
            if v in U: continue
            s = 1 + (G.induced_subgraph(list(nb[v])).clique_number() if nb[v] else 0)
            if s > best[0]: best = (s, v)
        out = (best[0], [best[1]] + one_max(nb[best[1]])) if best[1] is not None else (0, None)
        Ul = sorted(U)
        for i, u in enumerate(Ul):
            for v in Ul[i+1:]:
                if v not in nb[u] or inside([u, v]): continue
                cn = nb[u] & nb[v]
                s = 2 + (G.induced_subgraph(list(cn)).clique_number() if cn else 0)
                if s > out[0]:
                    C = [u, v] + one_max(cn)
                    if not inside(C): out = (s, C)
        return out
    while True:
        best = best_outside()
        if best[0] == s1 and best[1] and len(opts) < 40: opts.append(frozenset(best[1])); continue
        break
    toR = lambda C: [V[i] for i in C]
    def summ(C):
        out = []
        for p in S:
            q = p**k; cl = sorted({r % q for r in C})
            if len(cl) < q: out.append(f"mod {q}:{cl if len(cl) <= 3 else str(len(cl))+'cls'}")
        return ",".join(out) or "all"
    O0 = set(toR(opts[0])); rig = 0.0
    for b in range(M):
        if b in O0 or not loop[b]: continue
        rig = max(rig, sum(1.0 if F[b, t] else beta for t in O0)/len(O0))
    d1, d2 = s1/M, best[0]/M
    more = "+" if len(opts) >= 40 else ""
    print(f"{name:8s} k={k} M={M} beta={beta:.4f} | local max {d1:.5f} ({len(opts)}{more} classes: "
          f"{' | '.join(summ(toR(O)) for O in opts[:3])}) | best mixed {d2:.5f} ({summ(toR(best[1])) if best[1] else '-'}) "
          f"| gap {d1-d2:+.5f} ({(d1-d2)/d1:.0%}) | rigidity {rig:.3f}", flush=True)

VAR = {
 "ab+1":  (lambda a, b: a*b+1, 2, [2, 3, 5]),
 "ab-1":  (lambda a, b: a*b-1, 2, [2, 3, 5]),
 "ab+2":  (lambda a, b: a*b+2, 2, [2, 3, 5]),
 "ab+3":  (lambda a, b: a*b+3, 2, [2, 3, 5]),
 "ab+4":  (lambda a, b: a*b+4, 2, [2, 3, 5]),
 "ab+7":  (lambda a, b: a*b+7, 2, [2, 3, 5]),
 "a+b":   (lambda a, b: a+b, 2, [2, 3, 5]),
 "a2+b2": (lambda a, b: a*a+b*b, 2, [2, 3, 5]),
 "ab+1^3": (lambda a, b: a*b+1, 3, [2, 5]),
}
if __name__ == "__main__":
    for key in (sys.argv[1:] or VAR): run(key, *VAR[key])
