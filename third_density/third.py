# Third-best density: max U(K) over closed admissible cores K = (M7, M18) whose F(K) contains a type outside
# C7, outside C18, outside F and outside F' (so F(K) admits a type set not inside one class, F or F').
import math
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lambda_star'))
from closed import cells, w, A, fam, ALL
W = lambda s: sum(w[c] for c in s)
closed = sorted({A(S) for S in fam}, key=lambda s: -W(s))
inF  = lambda c, cls: (c[0] == 1) if cls == 7 else (c[0] == 3)
inF2 = lambda c, cls: (c[0] == 3) if cls == 7 else (c[0] == 1)
def run(b, j, top=8):
    out = []
    for M7 in closed:
        A7 = A(M7) if M7 else ALL
        for M18 in closed:
            if not M18 <= A7: continue
            A18 = A(M18) if M18 else ALL; AR = A7 & A18
            C7p, C18p = A18, A7
            types = [(7, c) for c in C7p] + [(18, c) for c in C18p] + [('R', c) for c in AR]
            if not any(t[0] != 7 for t in types) or not any(t[0] != 18 for t in types): continue
            if all(t[0] != 'R' and inF(t[1], t[0]) for t in types): continue
            if all(t[0] != 'R' and inF2(t[1], t[0]) for t in types): continue
            v = W(M7) + W(M18) + b * (W(C7p) - W(M7) + W(C18p) - W(M18)) + 23 * j * W(AR)
            out.append((v / 900, sorted(M7), sorted(M18), sorted(C7p - M7), sorted(C18p - M18), sorted(AR)))
    out.sort(key=lambda x: -x[0])
    for x in out[:top]: print(f"U={x[0]:.6f} (1/50-{0.02-x[0]:.6f})  M7={x[1]}  M18={x[2]}\n   extra C7={x[3]} extra C18={x[4]} R={x[5]}")
    return out
if __name__ == "__main__":
    bex = 1 - math.prod(1 - 1/p**2 for p in __import__('sympy').primerange(7, 10**6))
    print("beta union 0.05114, beta product", bex)
    run(0.05114, 0.01577)
