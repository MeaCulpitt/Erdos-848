"""Uniform large-N bound for 'ab+1 never k-free' (k >= 3).  q = 5^k, r = smaller root of x^2 = -1 mod q.
Valid A inside neither C_r nor C_{q-r}:
  |A cap C_r|, |A cap C_{q-r}| <= N Z_k / q + 2 + pi((N^2+1)^(1/k))     each   (Z_k = 2^-k + 3^-k + sum_{p>=7} p^-k)
  |A outside both classes|      <= 2 N sigma_k + 2 pi((N^2+1)^(1/k))           (sigma_k = sum_{p = 1 mod 4, p >= 13} p^-k)
Need total < (N - q)/q  (< c_r(N)).  N_k = upper end of the last failing cell (ratio 1.01) below 10^(2k+40); beyond, every
term is o(N) and decreasing relative to N."""
import math, numpy as np
from sympy import primerange
P = list(primerange(2, 10**6))
LIM = 10**7
s = np.ones(LIM + 1, bool); s[:2] = False
for i in range(2, int(LIM**.5) + 1):
    if s[i]: s[i*i::i] = False
pic = np.cumsum(s)
def piU(x):
    x = int(math.floor(x)); return int(pic[x]) if x <= LIM else 1.25506 * x / math.log(x)
def consts(k):
    Z = 2.0**-k + 3.0**-k + sum(p**-float(k) for p in P if p >= 7) + 1e-6**(k-1) / (k - 1)
    sig = sum(p**-float(k) for p in P if p % 4 == 1 and p >= 13) + 1e-6**(k-1) / (k - 1)
    return Z, sig
def root(k):
    q = 5**k; t = 2                        # 2^2 = -1 mod 5; Hensel lift
    for j in range(2, k + 1):
        m = 5**j; t = (t - (t*t + 1) * pow(2*t, -1, m)) % m
    return min(t, q - t)
def total(N, k, Z, sig):
    q = 5**k; pk = piU((N*N + 1) ** (1.0 / k) + 1e-9)
    return 2 * (N * Z / q + 2 + pk) + 2 * N * sig + 2 * pk
def Nk(k):
    Z, sig = consts(k); q = 5**k
    lo = float(q); last = None
    while lo < 10.0 ** (2 * k + 40) and lo < 1e300:
        hi = lo * 1.01
        if not total(hi, k, Z, sig) < (lo - q) / q: last = hi
        lo = hi
    return last, Z, sig
if __name__ == "__main__":
    print(" k   r_k            Z_k       q*sigma_k   density ratio   N_k          N_k / 5^k")
    for k in list(range(3, 21)) + [25, 30, 40, 60, 100]:
        N, Z, sig = Nk(k); q = 5**k
        print(f"{k:3d}  {root(k):<14d} {Z:.3e}  {q*sig:.3e}   {2*Z + 2*q*sig:.4f}        {N:.3e}   {N/q:8.1f}")
