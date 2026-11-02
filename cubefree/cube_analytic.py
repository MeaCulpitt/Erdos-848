"""Analytic bound for 'ab+1 never cube-free'.  For valid A inside neither C57 nor C68 (classes mod 125):
  |A cap C57| <= N (1/8 + 1/27 + beta3)/125 + 2 + pi((N^2+1)^(1/3))        (witness b outside C57; 125 never divides ab+1)
  |A cap C68| <= the same
  |A cap R|   <= 2 N sigma3 + 2 pi((N^2+1)^(1/3))                        (R cap V3: p^3 | x^2+1, p = 1 mod 4, p >= 13)
beta3 = sum_{q >= 7} q^-3, sigma3 = sum_{p = 1 mod 4, p >= 13} p^-3 (exact to 10^7, tail <= 1/(2 x^2) per Rosser-Schoenfeld style bound
sum_{p > x} p^-3 <= sum_{n > x} n^-3 <= 1/(2 x^2)).  Need the total < (N - 57)/125 <= c57(N) - something: then |A| < c57(N).
Cells [N_lo, N_hi] of ratio 1.01: total(N_hi) < (N_lo - 57)/125."""
import math, numpy as np
from sympy import primerange
P = list(primerange(7, 10**7))
beta3 = sum(q**-3.0 for q in P) + 1 / (2 * 1e14)
sigma3 = sum(p**-3.0 for p in P if p % 4 == 1 and p >= 13) + 1 / (2 * 1e14)
LIM = 10**8
s = np.ones(LIM + 1, bool); s[:2] = False
for i in range(2, int(LIM**.5) + 1):
    if s[i]: s[i*i::i] = False
pic = np.cumsum(s)
def piU(x):
    x = int(math.floor(x))
    if x <= LIM: return int(pic[x])
    return 1.25506 * x / math.log(x)
def total(N):
    pq = piU((N * N + 1) ** (1 / 3) + 1e-9)
    return 2 * (N * (1/8 + 1/27 + beta3) / 125 + 2 + pq) + 2 * N * sigma3 + 2 * pq
if __name__ == "__main__":
    print(f"beta3 = {beta3:.6f}, sigma3 = {sigma3:.7f}; main density {2*(1/8+1/27+beta3)/125 + 2*sigma3:.6f} vs 1/125 = 0.008")
    lo = 100.0; last_fail = None
    while lo < 1e40:
        hi = lo * 1.01
        if not total(hi) < (lo - 57) / 125: last_fail = hi
        lo = hi
    print(f"analytic bound gives |A| < c57(N) for all N >= {last_fail:.4g}")
