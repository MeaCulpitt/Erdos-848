"""explicitC_omega3.py plus the bound |A| <= |V cap [N]|  (every element of a valid set lies in V).

|V cap [N]| bound:
  * N <= 10^11: exact count of V_P (P = 10^5) at the grid point >= N, plus Vbig(N) (see explicitC_omega3.py);
  * all N: inclusion-exclusion over the primes p in Z = {5} u {p = 1 mod 4 : 13 <= p <= 100} (two classes mod p^2 each;
    error at most 3^|Z|), plus sum over p = 1 mod 4, 100 < p <= Y', of 2(N/p^2 + 1), plus EP(N, Y') for p > Y' (Lemma 3.4, any n).
A cell [N_lo, N_hi] then needs C >= (|V cap [N_hi]| - N_lo/50) / N_lo^0.81, which replaces the trivial 0.98 N^0.19
whenever it is smaller."""
import math, numpy as np
from sympy import primerange
import explicitC as E
import explicitC_omega as W
import explicitC_omega3 as W3

Z = [5] + [p for p in primerange(13, 101) if p % 4 == 1]
DZ = 1 - math.prod(1 - 2 / p**2 for p in Z)
T100 = sum(1 / p**2 for p in primerange(101, 10**7) if p % 4 == 1) + 2.51012 / (1e7 * math.log(1e7))
def lnVcount(lN):
    best = min(E.lse([lN + math.log(DZ), len(Z) * math.log(3), math.log(2 * T100) + lN, math.log(2) + E.lnpi(b * lN), E.lnEP(lN, b * lN)])
               for b in (0.5, 0.55, 0.6, 0.63, 0.66, 0.7))
    i = int(math.ceil(lN / math.log(10) * W3.D - 1e-9))
    if i <= W3.IB:
        best = min(best, E.lse([math.log(W3.VP[i].sum()), W3.lnVbig(lN)]))
    return best

def cell4(lo10, hi10):
    c, k = W.cell(lo10, hi10)
    L10 = math.log(10); lNl = lo10 * L10
    lv = lnVcount(hi10 * L10); l50 = lNl - math.log(50)
    if lv <= l50: return -math.inf, 'V'
    vt = lv + math.log1p(-math.exp(l50 - lv)) - 0.81 * lNl
    return (vt, 'V') if vt < c else (c, k)

if __name__ == "__main__":
    print(f"density bound for V from p <= 100: {DZ:.5f} + 2*{T100:.6f}")
    edges = [round(1 + 0.1*i, 2) for i in range(0, 41)] + [round(5 + 0.01*i, 2) for i in range(1, 2001)] \
            + [round(25 + 0.1*i, 2) for i in range(1, 5761)]
    lnC, arg = -math.inf, None
    for i in range(1, len(edges)):
        c, k = cell4(edges[i-1], edges[i])
        if c > lnC: lnC, arg = c, (edges[i-1], edges[i], k)
        if edges[i] in (8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 18.0, 20.0, 30.0, 100.0, 601.0):
            print(f"log10 N = {edges[i]}: cell bound {math.exp(c):.2f}, via {k}", flush=True)
    print(f"C = {1.001*math.exp(lnC):.2f}  worst cell [10^{arg[0]}, 10^{arg[1]}], via {arg[2]}")
