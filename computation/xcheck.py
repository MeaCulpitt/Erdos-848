# Independent brute force of the four case bounds (direct squarefree tests), plus the TRUE maximum
# over valid sets not contained in one class (exact clique), to confirm F >= true value.
import sys, networkx as nx
from sympy import factorint
def ns(x): return any(e>1 for e in factorint(x).values())
N=int(sys.argv[1])
V=[x for x in range(1,N+1) if ns(x*x+1)]
c=lambda x:x%25
R=[x for x in V if c(x) not in (7,18)]; C7=[x for x in V if c(x)==7]; C18=[x for x in V if c(x)==18]
H=lambda b,K:sum(1 for a in K if ns(a*b+1))
odd78=[a for a in C7+C18 if a%2]
vR=len(R); vRo=sum(1 for x in R if x%2)
mx=lambda it:max(it,default=0)
S1=vR+mx(H(b,C7)+H(b,C18) for b in R if b%2==0)
S2=vRo+mx(H(b,odd78) for b in R if b%2)
S3=vRo+max(mx(H(b,C7) for b in R if b%2)+mx(H(b,C18) for b in C7 if b%2==0),
           mx(H(b,C18) for b in R if b%2)+mx(H(b,C7) for b in C18 if b%2==0))
S4=mx(H(b,C7) for b in C18)+mx(H(b,C18) for b in C7)
F=max(S1,S2,S3,S4)
G=nx.Graph(); G.add_nodes_from(V)
for i,a in enumerate(V):
    for b in V[i+1:]:
        if ns(a*b+1): G.add_edge(a,b)
true=0
for b in R:   # cliques containing an element of R
    true=max(true,1+nx.max_weight_clique(G.subgraph(list(G[b])),weight=None)[1])
for b in C7:  # cliques meeting both C7 and C18
    nb=[a for a in G[b] if c(a)!=25]   # all neighbours
    for b2 in [a for a in G[b] if c(a)==18]:
        sub=[a for a in nb if a in G[b2]]
        true=max(true,2+nx.max_weight_clique(G.subgraph(sub),weight=None)[1])
print(f"N={N}: python S1={S1} S2={S2} S3={S3} S4={S4} F={F};  true max (not single-class)={true};  c7={(N-7)//25+1}")
