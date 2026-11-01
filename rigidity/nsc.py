# Exact max |A| over valid A ⊆ [1,N] NOT contained in C7 and NOT contained in C18 (m(N)),
# checked at N = 6 + 25k (right ends of the blocks on which c7 is constant), N <= LIM.
# Valid: ab+1 non-squarefree for all a,b in A (a=b included).  Independent of the repo code.
import sys, networkx as nx
from sympy import factorint
def nsf(x): return any(e > 1 for e in factorint(x).values())
LIM = int(sys.argv[1])
V = [x for x in range(1, LIM+1) if nsf(x*x+1)]
G = nx.Graph(); G.add_nodes_from(V)
for i, a in enumerate(V):
    for b in V[i+1:]:
        if nsf(a*b+1): G.add_edge(a, b)
cls = lambda x: x % 25
def omega(nodes):
    if not nodes: return 0
    return nx.max_weight_clique(G.subgraph(nodes), weight=None)[1]
worst = None
for N in range(6, LIM+1, 25):
    VN = [v for v in V if v <= N]
    m = 0
    # (i) A contains an element r outside C7 ∪ C18
    for r in VN:
        if cls(r) in (7, 18): continue
        m = max(m, 1 + omega([v for v in G[r] if v <= N]))
    # (ii) A ⊆ C7 ∪ C18, meeting both classes
    for u in VN:
        if cls(u) != 7: continue
        for w in G[u]:
            if w > N or cls(w) != 18: continue
            m = max(m, 2 + omega([v for v in G[u] if v <= N and v in G[w] and cls(v) in (7, 18)]))
    c7 = (N-7)//25 + 1 if N >= 7 else 0
    ok = (m < c7) or (m == 0 and c7 == 0)
    gap = c7 - m
    if worst is None or gap < worst[0]: worst = (gap, N)
    print(f"N={N} m={m} c7={c7} {'ok' if ok else 'FAIL'}", flush=True)
print("min gap c7-m over N>=7:", worst)
