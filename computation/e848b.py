import networkx as nx, sys, time
from sympy import factorint
def nonsqf(x): return any(e>1 for e in factorint(x).values())
LIM=int(sys.argv[1]); t0=time.time()
V=[a for a in range(1,LIM+1) if nonsqf(a*a+1)]
G=nx.Graph(); G.add_nodes_from(V)
for i,a in enumerate(V):
    for b in V[i+1:]:
        if nonsqf(a*b+1): G.add_edge(a,b)
print("vertices",len(V),"edges",G.number_of_edges(),f"{time.time()-t0:.0f}s",flush=True)
for N in range(31,LIM+1,25):   # last N before candidate count increases
    H=G.subgraph([v for v in V if v<=N])
    cl,size=nx.max_weight_clique(H,weight=None)
    cand=sum(1 for n in range(1,N+1) if n%25==7)
    flag="  <-- EXCEEDS" if size>cand else ""
    if size>cand or N%200<25: print(f"N={N}: max={size} candidate={cand}{flag}  {time.time()-t0:.0f}s",flush=True)
    if size>cand: break
print("done to",N)
