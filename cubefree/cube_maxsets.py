# All maximum valid sets for "ab+1 never cube-free" (a = b allowed), for every N <= NMAX.
import sys, igraph as ig
from sympy import factorint
def notcf(n): return any(e >= 3 for e in factorint(n).values())
NMAX = int(sys.argv[1])
V = [x for x in range(1, NMAX + 1) if notcf(x*x + 1)]
c = lambda N, r: (N - r) // 125 + 1 if N >= r else 0
G = ig.Graph(n=len(V), edges=[(i, j) for i in range(len(V)) for j in range(i+1, len(V)) if notcf(V[i]*V[j] + 1)])
prev = None
for N in range(1, NMAX + 1):
    idx = [i for i, a in enumerate(V) if a <= N]
    if not idx: continue
    H = G.subgraph(idx); w = H.clique_number()
    sets = sorted(tuple(sorted(V[idx[t]] for t in cl)) for cl in H.largest_cliques())
    if w != max(c(N, 57), c(N, 68)): print("MAX DIFFERS at N =", N, w, c(N, 57)); break
    key = (w, tuple(sets))
    if key != prev: print(f"N >= {N}: max {w}, maximum sets {sets}"); prev = key
