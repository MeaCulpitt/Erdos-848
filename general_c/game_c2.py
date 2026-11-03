"""Witness game for 'ab + c never squarefree' via coregame.py (CP-SAT).  See game_c.py for the model."""
import sys, json, math
from sympy import primerange, legendre_symbol
from coregame import Game
QMAX = 10**6
import numpy as np
_s = np.ones(QMAX, bool); _s[:2] = False
for _i in range(2, int(QMAX**.5) + 1):
    if _s[_i]: _s[_i*_i::_i] = False
PR = [int(p) for p in np.nonzero(_s)[0] if p >= 7]
def consts(c):
    beta = sum((1 / q if c % q == 0 else 1 / q**2) for q in PR) + 1.1 / QMAX
    rho = lambda p: 0 if c % p == 0 else (2 if pow((-c) % p, (p - 1) // 2, p) == 1 else 0)
    alpha = sum(rho(p) / p**2 for p in PR) + 2.2 / QMAX
    kappa = sum(1 / p**2 for p in PR if rho(p) == 2) + 1.1 / QMAX
    return beta, alpha, kappa, alpha * beta + kappa
def run(c, time=600):
    beta, alpha, kappa, j = consts(c)
    H = lambda r, s: (r * s + c) % 25 == 0
    g = lambda a, b: (a * b + c) % 4 == 0 or (a * b + c) % 9 == 0
    selff = lambda r, a: H(r, r) or g(a, a)
    G = Game(list(range(25)), list(range(36)), H, g, lambda s, a: 1 / 900, lambda s, a: beta if selff(s, a) else j)
    # maximum cliques
    cons = []; cliques = []; d = None
    while len(cliques) < 30:
        r = G.solve("clique", cons, time)
        if d is None: d = r["value"]
        if r["wK"] < d - 1e-7: break
        K = r["K"]; cliques.append(K)
        ins = (lambda K: (lambda s, a: s in K and a in K[s]))(K)
        cons.append(G.require_K_outside(ins))
    insides = [(lambda K: (lambda s, a: s in K and a in K[s]))(K) for K in cliques]
    adm = [G.require_F_outside(f) for f in insides]
    rV = G.solve("U", adm, time)
    r2 = G.solve("clique", [G.require_K_outside(f) for f in insides], time)
    desc = lambda K: dict(mod25=sorted(K), cells=sorted({a for s in K for a in K[s]}) if len({frozenset(v) for v in K.values()}) == 1 else "varies",
                          mod4=sorted({a % 4 for s in K for a in K[s]}), mod9=sorted({a % 9 for s in K for a in K[s]}))
    return dict(c=c, beta=round(beta, 5), j=round(j, 5), d=d, n_max=len(cliques), max_clique=desc(cliques[0]),
                V=rV["bound"], V_status=rV["status"], V_core=desc(rV["K"]) if rV["K"] else "empty",
                second_clique=r2["wK"], second=desc(r2["K"]), gap=d - rV["bound"])
if __name__ == "__main__":
    for c in [int(x) for x in sys.argv[1:]]:
        print(json.dumps(run(c)), flush=True)
