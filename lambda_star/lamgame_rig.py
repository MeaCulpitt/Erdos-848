"""Large-prime-weighted witness game for lambda* (Erdős 848): best density of a valid set NOT inside one class.
Types: (a mod 25, mu in {E,1,3}, nu = a mod 9 with 3|a merged)  -> 25*3*7 = 525 types, weights from mod 900.
Every element of A is a witness, so |A ∩ t| <= w_t * min_{s in P} M[s][t] with
   M[s][t] = d_t                      if s forces t (4, 9 or 25 divides ab+1 for all a in t, b in s)
           = beta                     if t is a C-type (d_t = 1) and not forced
           = j                        if t is an R-type and not forced   (needs a in V AND ab+1 non-sqf)
   d_t = 1 for C-types, alpha for R-types (a^2+1 non-squarefree via p >= 13).
Model 1 (independent): j = alpha*beta.  Model 2 (worst correlation): j = alpha*beta + kappa,
   kappa = sum_{p≡1(4), p>=13} 1/p^2  (p^2 | a^2+1 and p^2 | ab+1 together when a ≡ b mod p^2).
value(P) = sum_t z_t, maximised over P not inside the C7-types and not inside the C18-types (exact MILP).
"""
import sys, itertools, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
from sympy import primerange

PR = list(primerange(7, 10**6))
TAIL = 2.51012/(1e6*np.log(1e6))
beta = sum(1/p**2 for p in PR) + TAIL            # union bound beta+
P1 = [p for p in PR if p % 4 == 1 and p >= 13]
alpha = sum(2/p**2 for p in P1) + 2*TAIL          # union bound alpha+
kappa = sum(1/p**2 for p in P1) + TAIL

def key(r):
    mu = 'E' if r % 2 == 0 else (1 if r % 4 == 1 else 3)
    nu = 0 if r % 3 == 0 else r % 9
    return (r % 25, mu, nu)

T = sorted({key(r) for r in range(900)}, key=str)
idx = {t: i for i, t in enumerate(T)}
w = np.zeros(len(T))
for r in range(900): w[idx[key(r)]] += 1/900
isC = np.array([t[0] in (7, 18) for t in T])
def forced(s, t):
    (cs, ms, ns), (ct, mt, nt) = s, t
    if (cs*ct + 1) % 25 == 0: return True
    if ms != 'E' and mt != 'E' and (ms*mt) % 4 == 3: return True
    if ns and nt and (ns*nt) % 9 == 8: return True
    return False
n = len(T)
FM = np.array([[forced(s, t) for t in T] for s in T])

def solve(j, label):
    d = np.where(isC, 1.0, alpha)
    nf = np.where(isC, beta, j)
    M = np.where(FM, d[None, :], nf[None, :]) * w[None, :]      # M[s][t]
    W = (d * w)
    rows = []; lo = []; hi = []
    A = lil_matrix((n + n*n + 2, 2*n)); r = 0
    for t in range(n):
        A[r, n+t] = 1; A[r, t] = -W[t]; lo.append(-np.inf); hi.append(0); r += 1
    for t in range(n):
        for s in range(n):
            if M[s, t] >= W[t] - 1e-15: continue
            A[r, n+t] = 1; A[r, s] = W[t] - M[s, t]; lo.append(-np.inf); hi.append(W[t]); r += 1
    c7 = np.array([t[0] == 7 for t in T]); c18 = np.array([t[0] == 18 for t in T])
    A[r, :n] = (~c7).astype(float); lo.append(1); hi.append(np.inf); r += 1
    A[r, :n] = (~c18).astype(float); lo.append(1); hi.append(np.inf); r += 1
    A = A[:r].tocsr()
    res = milp(-np.r_[np.zeros(n), np.ones(n)], constraints=LinearConstraint(A, lo, hi),
               integrality=np.r_[np.ones(n), np.zeros(n)], bounds=Bounds(0, np.r_[np.ones(n), W]),
               options={"time_limit": 1500, "mip_rel_gap": 1e-7})
    x = res.x[:n] > .5; z = res.x[n:]
    P = [T[i] for i in range(n) if x[i]]
    core = [T[i] for i in range(n) if x[i] and z[i] > W[i] - 1e-12]
    summ = lambda S: sorted({(t[0], t[1]) for t in S}, key=str)
    print(f"[{label}] j={j:.5f}: value {-res.fun:.6f} (dual bound {-res.mip_dual_bound:.6f}, status {res.status}) "
          f"|P|={len(P)} types; fully-forced core (mod25,mod4): {summ(core)[:8]}", flush=True)
    return -res.fun, -res.mip_dual_bound

if __name__ == "__main__":
    print(f"beta={beta:.5f} alpha={alpha:.5f} kappa={kappa:.5f}; {n} types", flush=True)
    solve(0.0, "small primes only (beta=0 check)") if False else None
    solve(alpha*beta + kappa, "rigorous union-bound model")
