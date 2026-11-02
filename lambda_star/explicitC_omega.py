"""Explicit constant in Theorem 8.1 with the omega-refinement.

For k >= 1 split a valid A (not inside one class) as A' = {a : omega(a) < k}, A'' = {a : omega(a) >= k},
|A''| <= K_k(N) = #{n <= N : omega(n) >= k}.

  Case I  (A' not inside C7 and not inside C18): run the lambda* argument on A' with witnesses from A',
          so every witness has omega(b) <= k-1:   |A| <= N/50 + E_k(N) + K_k(N),
          E_k = the error of Section 8.5 with 2^{omega*(N)+1} -> 2^{min(k-1,omega*)+1} in L and
                2^{omega1*(N)} -> 2^{min(k-1,omega1*)} in L_C.
  Case II (A' inside C7, say; then some b in A'' lies outside C7 and A \\ C7 is inside A''):
          |A cap C7| <= g1 N + E_II(N), g1 = (1/3 + (2/3) beta+)/25 = 0.0146971 (b forces at most 12/36 of C7),
          E_II = 36 + 36 pi(Y2) + L_C(N, Y2) with the worst-case 2^{omega1*(N)}:
          |A| <= N/50 + E_II + K_k - (1/50 - g1) N.

K_k(N) by Rankin's trick (z >= 1):  K_k(N) <= z^-k N prod_{p<=N}(1+(z-1)/p) <= z^-k N exp((z-1) S(N)),
S(N) = sum_{p<=N} 1/p < log log N + B + 1/log^2 N  (Rosser-Schoenfeld 1962, x > 1), B = 0.2614972128;
z = k/S minimises the bound.  k = omega*(N)+1 gives K = 0 and recovers the unrefined bound exactly.

For a cell [N_lo, N_hi] all choices (Y, Y', Y2, k, z) are fixed at N_hi; every term is then nondecreasing in N, so
  C_cell = min( 0.98 N_hi^0.19,  max(E_k + K_k, E_II + K_k - (1/50-g1) N_lo)(N_hi) / N_lo^0.81 ).
"""
import math, numpy as np
import explicitC as E

B = 0.2614972128
G1 = (1/3 + (2/3)*0.051137) / 25          # beta+ = sum_{q>=7} q^-2 <= 0.051137
SLACK = 1/50 - G1
AS = np.arange(0.40, 0.95, 0.0125)
BS = (0.5, 0.55, 0.6, 0.63, 0.66, 0.7)

def lnS(lN): return math.log(lN) + B + 1/lN**2          # upper bound for sum_{p<=N} 1/p (as a value, not log)

def lnK(lN, k):
    if k > E.omega_star(lN): return -math.inf             # no n <= N has omega(n) >= k
    S = lnS(lN); z = max(1.0, k / S)
    return lN - k*math.log(z) + (z - 1)*S

def parts(lN, a, b):
    """Log of the pieces of E at cut-offs Y = N^a, Y' = N^b: fixed terms, and the bases of the two lattice terms."""
    lY, lYp = a*lN, b*lN
    l1 = math.log1p(math.exp(-lN)); lNN = 2*lN + math.log1p(math.exp(-2*lN))
    lpY, lpYp = E.lnpi(lY), E.lnpi(lYp)
    fixed = E.lse([math.log(72), math.log(72) + lpY, math.log(828*(2*E.n1*E.n2 + E.n1)),
                   math.log(828) + lpY, math.log(1656) + lpYp, E.lnEP(lN, lYp)])
    Lany_base = E.lse([math.log(2) + lN + l1 - lY, lNN - 2*lY])                    # times 2^{w+1}
    LC_base = E.lse([math.log(1.0668) + lN + l1 - lY, math.log(18.94) + 0.5*(lN + l1),
                     math.log(0.5334) + lNN - 2*lY, math.log(18.94)])               # times 2^{w1}
    return fixed, Lany_base, LC_base, lpY

def lnE_k(lN, k, P):
    w, w1 = min(k - 1, E.omega_star(lN)), min(k - 1, E.omega1_star(lN))
    return min(E.lse([fx, math.log(483) + (w + 1)*math.log(2) + la, math.log(42) + w1*math.log(2) + lc])
               for (fx, la, lc, _) in P)

def lnE_II(lN, P):
    w1 = E.omega1_star(lN)
    return min(E.lse([math.log(36), math.log(36) + lp, w1*math.log(2) + lc]) for (_, _, lc, lp) in P)

def cell(lo10, hi10):
    """Certified bound for C on [10^lo10, 10^hi10]; returns (ln C_cell, best k)."""
    L10 = math.log(10); lNh, lNl = hi10*L10, lo10*L10
    P = [parts(lNh, a, b) for a in AS for b in BS]
    eII = lnE_II(lNh, P)
    best = None
    for k in range(1, E.omega_star(lNh) + 2):
        K = lnK(lNh, k)
        caseI = E.lse([lnE_k(lNh, k, P), K])
        cII = E.lse([eII, K]); lsl = math.log(SLACK) + lNl          # case II: e^cII - SLACK*N_lo, in log space
        tot = caseI if cII <= lsl else max(caseI, cII + math.log1p(-math.exp(lsl - cII)))
        if best is None or tot < best[0]: best = (tot, k)
    return min(math.log(0.98) + 0.19*lNh, best[0] - 0.81*lNl), best[1]

if __name__ == "__main__":
    edges = [round(1 + 0.1*i, 2) for i in range(0, 91)] + [round(10 + 0.01*i, 2) for i in range(1, 1501)] \
            + [round(25 + 0.1*i, 2) for i in range(1, 5761)]
    lnC, arg = -math.inf, None
    for i in range(1, len(edges)):
        c, k = cell(edges[i-1], edges[i])
        if c > lnC: lnC, arg = c, (edges[i-1], edges[i], k)
        if edges[i] in (8.0, 10.0, 11.0, 12.0, 13.0, 15.0, 20.0, 30.0, 60.0, 100.0, 300.0, 601.0):
            print(f"log10 N = {edges[i]}: cell bound {math.exp(c):.2f}, k = {k}", flush=True)
    print(f"C = {1.001*math.exp(lnC):.2f}  worst cell [10^{arg[0]}, 10^{arg[1]}], k = {arg[2]}")
    print("Beyond 10^601 take k = omega*(N)+1 (no refinement): the unrefined tail bound of Section 8.5 applies.")
