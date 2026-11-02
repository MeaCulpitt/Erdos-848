"""explicitC_omega.py with K_k(N) = min(Rankin, envelope) for N <= 10^18 (omega_envelope.py), Rankin beyond."""
import math, numpy as np
import explicitC_omega as W
U = np.load('omega_envelope.npy'); D = 200; IMAX = U.shape[1] - 1
rankin = W.lnK
def lnK_env(lN, k):
    r = rankin(lN, k)
    i = int(math.ceil(lN / math.log(10) * D - 1e-9))          # grid point >= N
    if i > IMAX or k >= U.shape[0]: return r
    s = U[k:, i].sum()
    return min(r, math.log(s)) if s > 0 else -math.inf
W.lnK = lnK_env
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
