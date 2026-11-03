"""Exact maximum valid sets for 'ab + c never squarefree' at small N (igraph clique number), vs the predicted class."""
import sys, json, math, igraph as ig
from sympy import factorint
def sqfree(n): return all(e < 2 for e in factorint(n).values())
def run(c, Ns, cls):
    Nmax = max(Ns)
    V = [x for x in range(1, Nmax + 1) if not sqfree(x * x + c)]
    out = []
    for N in Ns:
        Vn = [x for x in V if x <= N]; n = len(Vn)
        E = [(i, j) for i in range(n) for j in range(i + 1, n) if not sqfree(Vn[i] * Vn[j] + c)]
        G = ig.Graph(n=n, edges=E); w = G.clique_number()
        cbest = max(sum(1 for x in range(1, N + 1) if pred(x)) for pred in cls)
        out.append((N, w, cbest))
    return out
if __name__ == "__main__":
    c = int(sys.argv[1]); mod = int(sys.argv[2]); rs = [int(x) for x in sys.argv[3].split(',')]
    cls = [(lambda r: (lambda x: x % mod == r))(r) for r in rs]
    print(c, run(c, [int(x) for x in sys.argv[4].split(',')], cls), flush=True)
