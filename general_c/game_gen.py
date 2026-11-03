"""Unified witness game for 'ab + c never squarefree' (c >= 1 squarefree-free of p^2 for p >= 5 assumed).
Forcing layers: 4, 9 (cells = residues mod 36) and P^2 (slabs = residues mod P^2, P = 5 or the least prime with a root).
Refinements:  * slabs split by membership in the root classes S_p^+- mod p^2 for p in PS (shared sign forces);
              * cells split by divisibility by each luck prime q | c (q >= 5, q != P): delta = [q | a].
Luck primes: all primes q >= 5 other than P.  Non-forced bounds (fraction of the target type):
   self-forcing target: beta0 + sum_{q|c} (1/q if q|a else 1/(q-1))     (any non-forcing witness)
   other target (own witness, same delta): j = alpha_t beta0' + kappa_t  (q|c contributes nothing: q^2 | ab+c needs
                                           exactly one of q|a, q|b)
   with q in PS contributing 1/(q^2-2) and the split primes removed from alpha, kappa."""
import sys, json, math, itertools
from coregame import Game
import game_c2 as G2
PR = sorted(set(G2.PR + [5]))
def rho(c, p): return 0 if c % p == 0 else (2 if pow((-c) % p, (p - 1) // 2, p) == 1 else 0)
def run(c, P=5, k=1, time=1500):
    m = P * P
    luck = [q for q in PR if q != P]
    Qc = [q for q in luck if c % q == 0]
    PS = [p for p in luck if rho(c, p) == 2][:k]
    beta0 = sum(1 / q**2 for q in luck if c % q and q not in PS) + sum(1 / (p * p - 2) for p in PS) + 1.1 / G2.QMAX
    at = sum(rho(c, p) / p**2 for p in luck if p not in PS) + 2.2 / G2.QMAX
    kt = sum(1 / p**2 for p in luck if rho(c, p) == 2 and p not in PS) + 1.1 / G2.QMAX
    rho0 = math.prod(1 - 2 / p**2 for p in PS)
    jl = (at * beta0 + kt) / rho0
    pats = list(itertools.product('+-0', repeat=len(PS)))
    dels = list(itertools.product((0, 1), repeat=len(Qc)))
    slabs = [(r, pi) for r in range(m) for pi in pats]
    cells = [(a, de) for a in range(36) for de in dels]
    H0 = lambda r, s: (r * s + c) % m == 0
    H = lambda s, t: H0(s[0], t[0]) or any(x == y != '0' for x, y in zip(s[1], t[1]))
    g = lambda a, b: (a[0] * b[0] + c) % 4 == 0 or (a[0] * b[0] + c) % 9 == 0
    sf = lambda s, a: H(s, s) or g(a, a)
    def w(s, a):
        return math.prod((1 / p**2 if x != '0' else 1 - 2 / p**2) for p, x in zip(PS, s[1])) * \
               math.prod((1 / q if d else 1 - 1 / q) for q, d in zip(Qc, a[1])) / (36 * m)
    def b(s, a):
        if sf(s, a): return beta0 + sum((1 / q if d else 1 / (q - 1)) for q, d in zip(Qc, a[1]))
        return jl
    G = Game(slabs, cells, H, g, w, b)
    cons = []; cliques = []; d = None
    while len(cliques) < 30:
        r = G.solve("clique", cons, time)
        if r["status"] != "OPTIMAL": break
        if d is None: d = r["wK"]
        if r["wK"] < d - 1e-6: break
        cliques.append(r["K"]); K = r["K"]
        cons.append(G.require_K_outside(lambda s, a, K=K: s in K and a in K[s]))
    adm = [G.require_F_outside(lambda s, a, K=K: s in K and a in K[s]) for K in cliques]
    rV = G.solve("U", adm, time)
    r2 = G.solve("clique", [G.require_K_outside(lambda s, a, K=K: s in K and a in K[s]) for K in cliques], time)
    K0 = cliques[0] if cliques else {}
    return dict(c=c, P=P, PS=PS, Qc=Qc, d=d, n_max=len(cliques), clique_residues_mod_P2=sorted({s[0] for s in K0}),
                clique_cells_mod36=sorted({a[0] for s in K0 for a in K0[s]}), V=rV["bound"], status=rV["status"],
                gap=d - rV["bound"], second_clique=r2["wK"] if r2["status"] == "OPTIMAL" else None,
                beta0=round(beta0, 5), j_lump=round(jl, 5))
def first_P(c):
    if (c % 4 == 3) or (c % 3 == 2): return 5        # classes mod 4 / 9 exist; mod-25 layer kept
    return next(p for p in PR if rho(c, p) == 2)      # 5 if -c is a QR mod 5, else the least such prime
if __name__ == "__main__":
    k = int(sys.argv[1])
    for c in [int(x) for x in sys.argv[2:]]:
        print(json.dumps(run(c, first_P(c), k)), flush=True)
