# Exhaustiveness / validity test of the case bounds on actual cliques: for small N, enumerate ALL maximal
# valid sets A (cliques in the graph with loops required) not inside C7 or C18, assign each to a case, and
# check |A| <= that case's bound (the bound computed at the same N).
import sys, networkx as nx
from sympy import factorint
def ns(x): return any(e>1 for e in factorint(x).values())
N=int(sys.argv[1])
V=[x for x in range(1,N+1) if ns(x*x+1)]
cl=lambda x:x%25
C7=[x for x in V if cl(x)==7]; C18=[x for x in V if cl(x)==18]; R=[x for x in V if cl(x) not in (7,18)]
H=lambda b,K:sum(1 for a in K if ns(a*b+1))
mx=lambda it:max(it,default=0)
vR=len(R); vRo=sum(x%2 for x in R)
S1=vR+mx(H(b,C7)+H(b,C18) for b in R if b%2==0)
S2=vRo+mx(H(b,[a for a in C7+C18 if a%2]) for b in R if b%2)
S3=vRo+max(mx(H(b,C7) for b in R if b%2)+mx(H(b,C18) for b in C7 if b%2==0),mx(H(b,C18) for b in R if b%2)+mx(H(b,C7) for b in C18 if b%2==0))
S4=mx(H(b,C7) for b in C18)+mx(H(b,C18) for b in C7)
G=nx.Graph(); G.add_nodes_from(V)
for i,a in enumerate(V):
    for b in V[i+1:]:
        if ns(a*b+1): G.add_edge(a,b)
cnt={1:0,2:0,3:0,4:0}; worst={1:0,2:0,3:0,4:0}; viol=0; n=0
for A in nx.find_cliques(G):
    s=set(A)
    if s<=set(C7) or s<=set(C18): continue
    n+=1
    AR=[x for x in A if cl(x) not in (7,18)]; AC=[x for x in A if cl(x) in (7,18)]
    if AR and any(x%2==0 for x in AR): c,bd=1,S1
    elif AR and all(x%2 for x in AC): c,bd=2,S2
    elif AR: c,bd=3,S3
    else:
        assert any(cl(x)==7 for x in A) and any(cl(x)==18 for x in A); c,bd=4,S4
    cnt[c]+=1; worst[c]=max(worst[c],len(A))
    if len(A)>bd: viol+=1; print("VIOLATION",c,len(A),bd,sorted(A))
print(f"N={N} maximal cliques not single-class: {n}, by case {cnt}, max size by case {worst}, bounds S1..S4={S1,S2,S3,S4}, violations={viol}")
