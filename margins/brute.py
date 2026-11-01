# Independent brute force of the 63x63 matrix M[s][t] (direct squarefree tests via sympy) at given N,
# compared with typemat output; also the true max over valid non-single-class sets (exact clique, networkx).
import sys, networkx as nx
from sympy import factorint
sys.path.insert(0,'.')
from solve import read, NT
def ns(x): return any(e>1 for e in factorint(x).values())
def ty(a):
    k=0 if a%25==7 else (1 if a%25==18 else 2); mu=0 if a%2==0 else (1 if a%4==1 else 2)
    return (k*3+mu)*7+[0,1,2,0,3,4,0,5,6][a%9]
f=sys.argv[1]; data=read(f); clique='-c' in sys.argv
for N,Vc,M in data:
    V=[x for x in range(1,N+1) if ns(x*x+1)]
    B=[[0]*NT for _ in range(NT)]; cnt=[0]*NT
    for a in V: cnt[ty(a)]+=1
    for b in V:
        h=[0]*NT
        for a in V:
            if ns(a*b+1): h[ty(a)]+=1
        s=ty(b)
        for t in range(NT): B[s][t]=max(B[s][t],h[t])
    ok = B==M and cnt==Vc
    msg=f"N={N}: brute matrix == typemat: {ok}"
    if clique:
        G=nx.Graph(); G.add_nodes_from(V)
        for i,a in enumerate(V):
            for b in V[i+1:]:
                if ns(a*b+1): G.add_edge(a,b)
        best=0
        for A in nx.find_cliques(G):
            if all(x%25==7 for x in A) or all(x%25==18 for x in A): continue
            best=max(best,len(A))
        msg+=f"; true max non-single-class = {best}"
    print(msg,flush=True)
