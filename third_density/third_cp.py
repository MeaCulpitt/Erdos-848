"""Refined core game for the third-best density of Erdos 848 (CP-SAT, coregame.py).
Slabs (r mod 25, pi): pi = membership in S_p^+ / S_p^- (a = +-iota_p mod p^2) for p in PS, or '0'.
Cells: the 21 cells mod 36 of the paper (forcing by 4 or 9).  Lumps (r not in {7,18}, pi all 0) never self-force."""
import sys, math, itertools
sys.path.insert(0, __import__('os').path.join(__import__('os').path.dirname(__file__), '..', 'lambda_star'))
import closed as CL
from coregame import Game
import numpy as np
QMAX = 10**7
_s = np.ones(QMAX, bool); _s[:2] = False
for i in range(2, int(QMAX**.5) + 1):
    if _s[i]: _s[i*i::i] = False
PR = np.nonzero(_s)[0]
def run(PS, mode="union", time=5000):
    P1 = [int(p) for p in PR if p % 4 == 1 and p >= 13]
    kt = sum(1 / p**2 for p in P1 if p > max(PS)) + 1.1 / QMAX
    at = 2 * kt
    beta = sum(1 / float(q)**2 for q in PR if q >= 7) + 1.1 / QMAX
    betap = beta + sum(1 / (p * p - 2) - 1 / (p * p) for p in PS)
    if mode == "product":     # exact CRT density for q <= QMAX (one class mod q^2 each), union bound beyond
        lp = sum(math.log1p(-1 / float(q)**2) for q in PR if q >= 7 and q not in PS) + sum(math.log1p(-1 / (p * p - 2)) for p in PS)
        betap = 1 - math.exp(lp) + 1.1 / QMAX
        beta = 1 - math.exp(sum(math.log1p(-1 / float(q)**2) for q in PR if q >= 7)) + 1.1 / QMAX
    rho0 = math.prod(1 - 2 / p**2 for p in PS)
    jl = (at * betap + kt) / rho0
    pats = list(itertools.product('+-0', repeat=len(PS)))
    slabs = [(r, pi) for r in range(25) for pi in pats]
    def H(s, t):
        return (s[0] * t[0] + 1) % 25 == 0 or any(a == b != '0' for a, b in zip(s[1], t[1]))
    isC = lambda r: r in (7, 18)
    w = lambda s, a: CL.w[a] / 36 / 25 * math.prod((1 / p**2 if x != '0' else 1 - 2 / p**2) for p, x in zip(PS, s[1]))
    b = lambda s, a: betap if (isC(s[0]) or any(x != '0' for x in s[1])) else jl
    G = Game(slabs, CL.cells, H, lambda a, c: CL.f(a, c), w, b)
    ins = [lambda s, a: s[0] == 7, lambda s, a: s[0] == 18,
           lambda s, a: (s[0] == 7 and a[0] == 1) or (s[0] == 18 and a[0] == 3),
           lambda s, a: (s[0] == 7 and a[0] == 3) or (s[0] == 18 and a[0] == 1)]
    r = G.solve("U", [G.require_F_outside(f) for f in ins], time)
    print(f"PS={PS} mode={mode}: beta'={betap:.6f} j_lump={jl:.6f}  max U = {r['value']:.7f}, bound {r['bound']:.7f} [{r['status']}]")
    print("   core:", {s: sorted(v) for s, v in r['K'].items()})
    print("   F(K) slabs:", {s: len(v) for s, v in r['F'].items()} if len(r['F']) < 15 else len(r['F']))
    print(f"   target 1/25 - 1/(4 pi^2) = {1/25 - 1/(4*math.pi**2):.7f};  (12 + 25 beta)/900 = {(12+25*beta)/900:.7f}")
    return r
if __name__ == "__main__":
    PS = [int(x) for x in sys.argv[1].split(',')]
    run(PS, sys.argv[2] if len(sys.argv) > 2 else "union")
