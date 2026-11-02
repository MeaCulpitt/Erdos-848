"""Explicit constant with the omega-refinement, using exact counts up to 10^11 (segomega.c, file seg1e11.txt).

K_k(N) bounds #{a in A : omega(a) >= k}. Since A is inside V:
  * N <= 10^11:  K_k(N) <= #{n <= N : n in V_P, omega(n) >= k} + Vbig(N)      (exact count, P = 10^5)
                 Vbig(N) = #{n <= N : p^2 | n^2+1 for some prime p > P}
                         <= 2 N sum_{p > P} p^-2 + 2 pi(Y') + EP(N, Y')            (Lemmas 3.3 and 3.4, any Y' >= P)
  * every N <= 10^18: the Hardy-Ramanujan envelope over all integers, now started from exact counts at 10^11;
  * every N: Rankin's bound.
K_k is the smallest of the available bounds. All counts are taken at the grid point >= N_hi (nondecreasing in N).
"""
import math, numpy as np
from sympy import primerange
import explicitC as E
import explicitC_omega as W

D = 200; IMAX = 3600
rows = np.loadtxt('seg1e11.txt', dtype=np.float64)
IB = int(rows[-1, 0])
ALL = np.zeros((IB + 1, 16)); VP = np.zeros((IB + 1, 16))
ALL[rows[:, 0].astype(int)] = rows[:, 2:18]; VP[rows[:, 0].astype(int)] = rows[:, 18:34]
g = 10.0 ** (np.arange(IMAX + 1) / D)

# ---- envelope over all integers, started at 10^(IB/200) ----
def piU(x):
    L = math.log(x); return x / L * (1 + 1 / L + 2.51 / L**2)
KMAX = 15
U = np.zeros((KMAX + 1, IMAX + 1)); U[:, :IB + 1] = ALL[:, :KMAX + 1].T
for i in range(IB + 1, IMAX + 1): U[1, i] = piU(g[i]) + 2 * math.sqrt(g[i])
U[0, :] = 1
pp = np.diff(ALL[:, 1], prepend=0)
def Uat(k, li):
    j = int(math.ceil(li - 1e-9)); return U[k, min(j, IMAX)]
for k in range(1, KMAX):
    Nk = ALL[:, k]
    for i in range(IB + 1, IMAX + 1):
        half = i / 2.0; jmax = int(math.floor(half + 1e-9))
        A = sum((Nk[j] - Nk[j - 1]) * Uat(1, i - (j - 1)) for j in range(1, jmax + 1) if Nk[j] != Nk[j - 1])
        if jmax < half: A += (Nk[jmax + 1] - Nk[jmax]) * Uat(1, i - jmax)
        Bs = sum(pp[j] * Uat(k, i - (j - 1)) for j in range(1, min(jmax + 1, IB) + 1) if pp[j])
        U[k + 1, i] = (A + Bs / (k + 1)) * (1 + 1e-9)

# ---- Vbig ----
P = 10**5
TP = sum(1 / p**2 for p in primerange(P + 1, 10**7) if p % 4 == 1) + 2.51012 / (1e7 * math.log(1e7))
def lnVbig(lN):
    N = math.exp(lN)
    cands = [math.log(P)] + [b * lN for b in (0.5, 0.55, 0.6, 0.63, 0.66, 0.7) if b * lN > math.log(P)]
    return min(E.lse([math.log(2 * N * TP), math.log(2) + E.lnpi(lYp), E.lnEP(lN, lYp)]) for lYp in cands)

rankin = W.lnK
def lnK3(lN, k):
    best = rankin(lN, k)
    i = int(math.ceil(lN / math.log(10) * D - 1e-9))
    if i <= IMAX and k < U.shape[0]:
        s = U[k:, i].sum(); best = min(best, math.log(s) if s > 0 else -math.inf)
    if i <= IB and k < 16:
        s = VP[i, k:].sum(); best = min(best, E.lse([math.log(s) if s > 0 else -math.inf, lnVbig(lN)]))
    return best
W.lnK = lnK3

if __name__ == "__main__":
    edges = [round(1 + 0.1*i, 2) for i in range(0, 41)] + [round(5 + 0.01*i, 2) for i in range(1, 2001)] \
            + [round(25 + 0.1*i, 2) for i in range(1, 5761)]
    lnC, arg = -math.inf, None
    for i in range(1, len(edges)):
        c, k = W.cell(edges[i-1], edges[i])
        if c > lnC: lnC, arg = c, (edges[i-1], edges[i], k)
        if edges[i] in (8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 15.0, 18.0, 20.0, 30.0, 100.0, 601.0):
            print(f"log10 N = {edges[i]}: cell bound {math.exp(c):.2f}, k = {k}", flush=True)
    print(f"C = {1.001*math.exp(lnC):.2f}  worst cell [10^{arg[0]}, 10^{arg[1]}], k = {arg[2]}")
