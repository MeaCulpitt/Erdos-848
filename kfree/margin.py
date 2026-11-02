"""For each k: at every vertex value N <= N_k, mu(N) = largest valid set not inside one class among vertices <= N,
and c(N) = max class count.  An exception is mu(N) >= c(N).  Reports the closest approach min_N (c(N) - mu(N)) over N
with mu(N) >= 1, the largest mu, and every N where mu(N) >= c(N)."""
import sys, json, igraph as ig
import kfree_analytic as KA, kfree_exact as K
def run(k):
    Nk = int(KA.Nk(k)[0]) + 1 if k <= 40 else 60 * 5**k
    q, r, ps, V, adj = K.setup(k, Nk); s = q - r; n = len(V)
    E = [(i, j) for i in range(n) for j in range(i + 1, n) if adj(V[i], V[j])]
    G = ig.Graph(n=n, edges=E); nb = [set(G.neighbors(i)) for i in range(n)]
    cls = [('r' if v % q == r else 's' if v % q == s else 'x') for v in V]
    seeds = [((i,), nb[i]) for i in range(n) if cls[i] == 'x'] + \
            [((i, j), nb[i] & nb[j]) for (i, j) in E if {cls[i], cls[j]} == {'r', 's'}]
    c = lambda N: max((N - r) // q + 1 if N >= r else 0, (N - s) // q + 1 if N >= s else 0)
    closest = None; exc = []; mu_max = 0
    for m in range(n):                                     # vertices 0..m present, N in [V[m], V[m+1])
        mu = 0
        for seed, common in seeds:
            if max(seed) > m: continue
            sub = sorted(x for x in common if x <= m)
            mu = max(mu, len(seed) + (G.subgraph(sub).clique_number() if sub else 0))
        if mu == 0: continue
        mu_max = max(mu_max, mu); cn = c(V[m]); gap = cn - mu
        if closest is None or gap < closest[0]: closest = (gap, mu, cn, V[m])
        if mu >= cn: exc.append((V[m], mu, cn))
    return dict(k=k, vertices=n, sporadic=cls.count('x'), cross_edges=sum(1 for (i, j) in E if {cls[i], cls[j]} == {'r', 's'}),
                mu_max=mu_max, closest_gap=None if closest is None else dict(gap=closest[0], mu=closest[1], c=closest[2], N=str(closest[3])),
                exceptions=[(str(a), b, cc) for a, b, cc in exc][:10])
if __name__ == "__main__":
    for k in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
        print(json.dumps(run(k)), flush=True)
