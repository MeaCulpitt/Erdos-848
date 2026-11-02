# Galois-closed cell sets for the cross-forcing relation on the 21 cells mod 36
MU=[0,1,3]; NU=[0,1,2,4,5,7,8]
cells=[(m,n) for m in MU for n in NU]
w={c:(2 if c[0]==0 else 1)*(3 if c[1]==0 else 1) for c in cells}
def f(a,b):
    return (a[0] and b[0] and a[0]*b[0]%4==3) or (a[1] and b[1] and a[1]*b[1]%9==8)
ALL=frozenset(cells)
def A(M): return frozenset(c for c in cells if all(f(m,c) for m in M))
fam={ALL}; frontier=[ALL]
while frontier:
    S=frontier.pop(); 
    for c in cells:
        T=S & A([c])
        if T not in fam: fam.add(T); frontier.append(T)
closed=sorted({A(S) for S in fam}, key=lambda s:(-sum(w[c] for c in s)))
if __name__=='__main__':
    print(len(fam),"A-sets;",len(closed),"closed sets")
    W=lambda s:sum(w[c] for c in s)
    best=[]
    for b,j in [(0.052,0.0169)]:
      for M7 in closed:
        A7=A(M7) if M7 else ALL
        for M18 in closed:
          if not M18<=A7: continue
          A18=A(M18) if M18 else ALL; AR=A7&A18
          WC7=W(A18); WC18=W(A7)
          if not ((WC18>0 or W(AR)>0) and (WC7>0 or W(AR)>0)): continue
          v=W(M7)+W(M18)+b*(WC7-W(M7)+WC18-W(M18))+23*j*W(AR)
          best.append((v,sorted(M7),sorted(M18)))
    best.sort(reverse=True); print(len(best),"closed pairs"); 
    for x in best[:6]: print(round(x[0],4), x[1], x[2])
    idx={c:i for i,c in enumerate(cells)}
    L=sorted({tuple(sorted(idx[c] for c in s)) for s in fam})
    print("LIST", " ,\n  ".join("{"+", ".join(map(str,s))+"}" if s else "∅" for s in L))
