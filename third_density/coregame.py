"""Core game solved exactly with CP-SAT.  Types = (slab, cell).  (s,a) forces (t,b) iff H(s,t) or g(a,b).
Core K: a closed cell set K_s per slab (closed sets of g, WLOG), forming a clique; F(K)_t = intersection of A(K_s) over
slabs s with K_s nonempty and not H(s,t).  U(K) = sum_{K} w + sum_{F(K) minus K} b w.
Objective coefficients are rounded UP to integers in units of 1/SCALE, so the optimum / SCALE is a rigorous upper
bound for max U (up to the floating values of w, b, which are themselves upper bounds)."""
import math
from ortools.sat.python import cp_model

SCALE = 10**9

def closed_sets(cells, g):
    ALL = frozenset(cells); Nb = {a: frozenset(b for b in cells if g(a, b)) for a in cells}
    def A(M):
        X = ALL
        for a in M: X = X & Nb[a]
        return X
    fam = {ALL}; fr = [ALL]; nbs = set(Nb.values())
    while fr:
        S = fr.pop()
        for m in nbs:
            X = S & m
            if X not in fam: fam.add(X); fr.append(X)
    cl = sorted({A(S) for S in fam} - {frozenset()}, key=lambda s: (-len(s), sorted(s)))
    return cl, A

class Game:
    def __init__(self, slabs, cells, H, g, w, b):
        self.slabs, self.cells, self.H, self.g, self.w, self.b = slabs, cells, H, g, w, b
        self.opts, self.A = closed_sets(cells, g)
        self.Aopt = [self.A(o) for o in self.opts]
    def build(self):
        m = cp_model.CpModel(); S, C, O = self.slabs, self.cells, self.opts
        # a slab not H-related to itself can only hold a cell clique (o inside A(o))
        self.allowed = {s: [k for k in range(len(O)) if self.H(s, s) or O[k] <= self.Aopt[k]] for s in S}
        z = {(s, k): m.NewBoolVar("") for s in S for k in self.allowed[s]}
        y = {(t, a): m.NewBoolVar("") for t in S for a in C}
        for s in S: m.AddAtMostOne([z[s, k] for k in self.allowed[s]])
        for (s, k), v in z.items():
            for a in O[k]: m.AddImplication(v, y[s, a])
        f = {(s, a): m.NewBoolVar("") for s in S for a in C}       # f[s,a]: slab s's core excludes cell a
        for s in S:
            for a in C:
                for k in self.allowed[s]:
                    if a not in self.Aopt[k]: m.AddImplication(z[s, k], f[s, a])
        for t in S:
            for a in C:
                for s in S:
                    if not self.H(s, t): m.AddBoolOr([f[s, a].Not(), y[t, a].Not()])
        self.m, self.z, self.y = m, z, y
        return m
    def wK(self, s, k): return sum(self.w(s, a) for a in self.opts[k])
    def solve(self, objective, constraints=(), time=600, workers=2):
        self.build(); m = self.m
        for f in constraints: f(self)
        if objective == "clique":
            terms = [(math.ceil(self.wK(s, k) * SCALE), v) for (s, k), v in self.z.items()]
        else:
            terms = [(math.ceil(sum(self.w(s, a) * (1 - self.b(s, a)) for a in self.opts[k]) * SCALE), v) for (s, k), v in self.z.items()] + \
                    [(math.ceil(self.w(t, a) * self.b(t, a) * SCALE), v) for (t, a), v in self.y.items()]
        m.Maximize(sum(c * v for c, v in terms if c))
        sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = time; sol.parameters.num_workers = workers
        import time as _t; t0=_t.time(); st = sol.Solve(m); print(f'   [{objective}] {sol.StatusName(st)} {sol.ObjectiveValue()/SCALE:.6f} bound {sol.BestObjectiveBound()/SCALE:.6f} ({_t.time()-t0:.0f}s, {len(self.z)} z-vars)', flush=True)
        K = {s: self.opts[k] for (s, k), v in self.z.items() if sol.Value(v)}
        F = {}
        for (t, a), v in self.y.items():
            if sol.Value(v): F.setdefault(t, set()).add(a)
        exact = sum(self.wK(s, k) * (1 if objective == "clique" else 1) for (s, k), v in self.z.items() if sol.Value(v))
        Uexact = sum(self.w(s, a) for s in K for a in K[s]) + sum(self.w(t, a) * self.b(t, a) for t in F for a in F[t] if not (t in K and a in K[t]))
        return dict(status=sol.StatusName(st), bound=sol.BestObjectiveBound() / SCALE, value=sol.ObjectiveValue() / SCALE,
                    K=K, F=F, wK=exact, U=Uexact)
    # constraint helpers
    def require_F_outside(self, inside):            # F(K) contains a type (t,a) with not inside(t,a)
        return lambda G: G.m.AddBoolOr([v for (t, a), v in G.y.items() if not inside(t, a)])
    def require_K_outside(self, inside):            # core contains a type outside
        return lambda G: G.m.AddBoolOr([v for (s, k), v in G.z.items() if not all(inside(s, a) for a in G.opts[k])])
