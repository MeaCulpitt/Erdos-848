# Third density (paper, Section 8.8)

λ₃ = lim sup of max |A|/N over valid A ⊆ [N] contained in none of C7, C18, F, F′.

| File | What it does |
| --- | --- |
| `lam3_lower.py` | the lower-bound set {x} ∪ {a ∈ C7 : ax + 1 not squarefree}, x prime ≡ 18 (mod 25), ≡ 3 (mod 4); exact count for given N, x |
| `coregame.py` | core game (Lemma 8.5) for types (slab, cell), solved exactly with OR-tools CP-SAT; objective coefficients rounded up |
| `third_cp.py` | the refined game: types split by membership in S_p^± = {a ≡ ±ι_p (mod p²)} for p in a given list |

Results:

- `python3 lam3_lower.py 2e7` gives 0.014671 (N = 2·10⁷, x = 100043); the limit as x → ∞ is 1/25 − 1/(4π²) = 0.0146697.
- `python3 third_cp.py 13 product` gives max U = 0.0149645; `python3 third_cp.py 13,17 product` gives 0.0149093 (OPTIMAL).

So 0.0146697 ≤ λ₃ ≤ 0.014910. The optimum core is the "one class plus one outsider" configuration. Requires `pip install ortools`.
