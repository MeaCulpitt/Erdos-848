# Exact maximum valid sets for "ab+1 never cube-free" (a = b allowed) at small N, by max clique on V3 = {x : x^2+1 not cube-free}.
import sys, igraph as ig
from sympy import factorint
def notcf(n): return any(e >= 3 for e in factorint(n).values())
NMAX = int(sys.argv[1])
V = [x for x in range(1, NMAX + 1) if notcf(x*x + 1)]
print(f"|V3 cap [{NMAX}]| = {len(V)}; first elements: {V[:12]}")
c57 = lambda N: (N - 57) // 125 + 1 if N >= 57 else 0
c68 = lambda N: (N - 68) // 125 + 1 if N >= 68 else 0
checks = sorted(set([N for N in range(57, NMAX + 1, 125)] + [N for N in range(68, NMAX + 1, 125)] + [N - 1 for N in range(57, NMAX + 1, 125)] + [NMAX]))
edges = []
for i, a in enumerate(V):
    for j in range(i + 1, len(V)):
        if notcf(a * V[j] + 1): edges.append((i, j))
print(f"edges: {len(edges)}")
G = ig.Graph(n=len(V), edges=edges)
bad = []
for N in checks:
    idx = [i for i, a in enumerate(V) if a <= N]
    H = G.subgraph(idx); w = H.clique_number() if idx else 0
    best = max(c57(N), c68(N))
    cl = [sorted(V[idx[t]] for t in c) for c in H.largest_cliques()] if idx else [[]]
    other = [c for c in cl if not (all(a % 125 == 57 for a in c) or all(a % 125 == 68 for a in c))]
    if w != best or other: bad.append((N, w, best, other[:3]))
print("N where the maximum is not max(c57, c68), or is also attained outside one class:")
for b in bad: print("  ", b)
if not bad: print("   none")
