"""Explicit error term for Theorem 8.1: |A| <= N/50 + E(N), and C with |A| <= N/50 + C*N^0.81 for all N.
Every term is an upper bound; Y (B-side cut) and Y' (A-side cut) are free parameters, so any choice is valid.
Computed in log space with float64; a relative safety factor 1.001 is applied to the final constant.

Error accounting (r_t = residues mod 900 in type t; sum over C-types 72, over R-types 828;
42 C-types, 483 R-types):
  core C-types (forced)          : sum r_t                                  <= 72
  non-core C-types, q <= Y        : r_t per prime 7 <= q <= Y                 <= 72 pi(Y)
  non-core C-types, q > Y         : Lemma 3.5 per type                        <= 42 L_C
  R-types, p,q <= 500             : r_t (2 n1 n2 + n1)                        <= 828 (2 n1 n2 + n1)
  R-types, 500 < q <= Y           : r_t per prime q (p-condition dropped)     <= 828 pi(Y)
  R-types, q > Y                  : any-target lattice lemma per type         <= 483 L_any
  R-types, 500 < p <= Y'          : 2 r_t per prime                           <= 1656 pi(Y')
  R-types, p > Y'                 : Lemma 3.4 once over all of R (types disjoint)
"""
import math, numpy as np
from sympy import primerange

PR = list(primerange(2, 5000))
n1 = sum(1 for p in PR if 13 <= p <= 500 and p % 4 == 1)
n2 = sum(1 for p in PR if 7 <= p <= 500)
lnprim = np.cumsum([math.log(p) for p in PR])                  # ln of primorials
lnprim7 = np.cumsum([math.log(p) for p in PR if p >= 7])       # ln(7*11*...)
SIEVE = 10**7
_s = np.ones(SIEVE + 1, bool); _s[:2] = False
for i in range(2, int(SIEVE**.5) + 1):
    if _s[i]: _s[i*i::i] = False
picum = np.cumsum(_s)

def lse(xs):
    xs = [x for x in xs if x > -math.inf]
    m = max(xs)
    return m + math.log(sum(math.exp(x - m) for x in xs))

def lnpi(lx):
    """ln of an upper bound for pi(e^lx): exact below 10^7, Rosser-Schoenfeld above."""
    if lx < math.log(2): return -math.inf
    if lx <= math.log(SIEVE): return math.log(max(1, int(picum[int(math.exp(lx) + 1e-9)])))
    return math.log(1.25506) + lx - math.log(lx)

def lnEP(lN, lYp):
    """Lemma 3.4, counting all integers 2 <= m <= min(M, m_j) (admissibility not used)."""
    lM = 2*lN - 2*lYp + 1e-12
    terms = [lM]
    l2N = lN + math.log(2) + 1e-12
    j = 2
    while True:
        lT = l2N / (2*j - 1)
        lmj = 2*math.log(math.cosh(lT)) if lT < 300 else 2*(lT - math.log(2))
        if lmj < math.log(2): break
        terms.append(min(lmj, lM)); j += 1
    return lse(terms)

def omega_star(lN):  return int(np.searchsorted(lnprim, lN + 1e-12, side='right'))
def omega1_star(lN): return int(np.searchsorted(lnprim7, lN + 1e-12, side='right'))

def lnE(lN, a, b):
    lY, lYp = a*lN, b*lN
    w, w1 = omega_star(lN), omega1_star(lN)
    l1 = math.log1p(math.exp(-lN))                          # ln(1 + 1/N)
    lNN = 2*lN + math.log1p(math.exp(-2*lN))                # ln(N^2 + 1)
    lLany = (w + 1)*math.log(2) + lse([math.log(2) + lN + l1 - lY, lNN - 2*lY])
    lLC = w1*math.log(2) + lse([math.log(1.0668) + lN + l1 - lY, math.log(18.94) + 0.5*(lN + l1),
                                math.log(0.5334) + lNN - 2*lY, math.log(18.94)])
    lpY, lpYp = lnpi(lY), lnpi(lYp)
    T = [math.log(72),
         math.log(72) + lpY, math.log(42) + lLC,
         math.log(828*(2*n1*n2 + n1)),
         math.log(828) + lpY,
         math.log(483) + lLany,
         math.log(1656) + lpYp, lnEP(lN, lYp)]
    return lse(T)

AS = np.arange(0.40, 0.95, 0.0125)
BS = (0.5, 0.55, 0.6, 0.63, 0.66, 0.7)
def lnEbest(lN):
    return min((lnE(lN, a, b), a, b) for a in AS for b in BS)

if __name__ == "__main__":
    print("n1 =", n1, "n2 =", n2, flush=True)
    L10 = math.log(10)
    # cells [10^lo, 10^hi]: step 0.1 in log10 N from 1 to 601, refined to 0.01 on [10, 25]
    edges = [round(1 + 0.1*k, 2) for k in range(0, 91)] + [round(10 + 0.01*k, 2) for k in range(1, 1501)] \
            + [round(25 + 0.1*k, 2) for k in range(1, 5761)]
    lnC, arg = -math.inf, None
    for k in range(1, len(edges)):
        lo, hi = edges[k-1], edges[k]
        e, a, b = lnEbest(hi*L10)            # E nondecreasing in N for fixed (Y, Y'): bound at the top
        cell = min(math.log(0.98) + 0.19*hi*L10, e - 0.81*lo*L10)
        if cell > lnC: lnC, arg = cell, (round(lo, 1), round(hi, 1), a, b, omega_star(hi*L10))
        if hi in (7.0, 10.0, 13.0, 20.0, 30.0, 51.0, 101.0, 201.0, 301.0, 401.0, 501.0, 601.0):
            print("log10N=%5.1f  E/N=%.3e  E/N^(2/3)=%.3e  E/N^0.81=%.3e" %
                  (hi, math.exp(e - hi*L10), math.exp(e - hi*L10*2/3), math.exp(e - 0.81*hi*L10)), flush=True)
    print("C =", "%.4e" % (1.001*math.exp(lnC)), " worst cell (log10 lo, hi, a, b, omega*):", arg)
    L = 601*L10
    print("tail at 10^601 (Robin): 1001*2^omega*N^(2/3-0.81) <= %.3e" %
          (1001*math.exp((math.log(2)*1.38402/math.log(L) - (0.81 - 2/3))*L)))
    for k in (7, 10, 13, 20, 30, 60, 100):
        e, a, b = lnEbest(k*L10)
        print("N=1e%d: E(N)<=%.4e  E/N=%.3e  Y=N^%.4f Y'=N^%.2f  omega*=%d" %
              (k, math.exp(e), math.exp(e - k*L10), a, b, omega_star(k*L10)))
