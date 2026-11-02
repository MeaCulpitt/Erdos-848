"""Certified threshold N2(delta) for the third-order theorem (paper, Section 8.7).

For an admissible core K other than F's and its mirror's, U(K) <= 1/50 - GAP with GAP = 948860/(900*10^6) = 0.00105429...
(lamgap.c / LamGap.lean with beta = 0.05114 >= beta+, j = 0.01577 >= j+).  By Lemma 8.5 a valid A not inside one class has
|A| <= U(K) N + E(N), with E(N) the explicit error of Section 8.5 (explicitC.py, no omega-refinement).  So A's core is F's
(or the mirror's), hence A is inside F (or its mirror), as soon as E(N) < (GAP - delta) N.

A cell [N_lo, N_hi] passes if E(N_hi) <= (GAP - delta) N_lo (E is nondecreasing in N for fixed cut-offs).  Cells: step 0.01
in log10 N up to 10^40, then 0.1 up to 10^601; beyond 10^601 the bound E(N) <= 1001 * 2^omega*(N) N^(2/3) of Section 8.5
gives E(N)/N < 10^-150.  N2 = the upper end of the last failing cell."""
import math, sys
import explicitC as E

GAP = 948860 / (900 * 10**6)
L10 = math.log(10)

def certify(delta, start=15.0):
    edges = [round(start + 0.01*i, 2) for i in range(0, int((40 - start) * 100) + 1)] + [round(40 + 0.1*i, 2) for i in range(1, 5611)]
    last_fail = None; worst = None
    for i in range(1, len(edges)):
        lo, hi = edges[i-1], edges[i]
        e, _, _ = E.lnEbest(hi * L10)
        ok = e <= math.log(GAP - delta) + lo * L10
        if not ok: last_fail = hi
        elif last_fail is not None:
            r = math.exp(e - lo * L10) / (GAP - delta)
            if worst is None or r > worst[0]: worst = (r, lo)
    return last_fail, worst

if __name__ == "__main__":
    print(f"GAP = {GAP:.8f}")
    for delta in [float(a) for a in (sys.argv[1:] or ["0.0008", "0.0005"])]:
        lf, w = certify(delta)
        print(f"delta = {delta}: all cells pass from N = 10^{lf} on (largest E/((GAP-delta)N) after that: {w[0]:.3f} at 10^{w[1]})", flush=True)
