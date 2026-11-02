# Higher powers: ab + 1 never k-free (paper, Section 9, Theorem 9.3)

For k ≥ 3, let q = 5^k and r_k the smaller root of x² ≡ −1 (mod q). The largest A ⊆ [N] with ab + 1 never k-free is the class r_k mod q:
- for every k ≥ 3 and N ≥ N_k (explicit; N_k/5^k ≤ 15,400, ≤ 214 for k ≥ 5, ≤ 60 for k ≥ 40), with only the full classes attaining it;
- for 3 ≤ k ≤ 100 and every N, except k = 3, 193 ≤ N ≤ 306 (see `../cubefree`) and k = 4, 239 ≤ N ≤ 806 (where {239} also attains the maximum 1).

| File | What it does |
| --- | --- |
| `kfree_analytic.py` | N_k for 3 ≤ k ≤ 40 (one-witness bound, cells of ratio 1.01) |
| `kfree_exact.py` | explicit vertex set below N_k; all maximum cliques at every vertex value (`clique` mode), or cliques to M₀ plus one-witness cells (`cells` mode) |
| `margin.py` | for each N ≤ N_k, the largest valid set not inside one class, μ_k(N), against c_k(N); output `margin_5_300.jsonl` (no exception for 5 ≤ k ≤ 300, closest margin 3 at k = 5) |
| `run_all.py`, `run_big.py` | drivers for k = 5..30 and k = 31..100 (k > 40 uses N_k ≤ 60·5^k) |
| `kfree_5_30.jsonl`, `kfree_21_29.jsonl`, `kfree_31_100.jsonl` | results: no exceptions for 5 ≤ k ≤ 100 |
| `kfree_4_cells.out` | k = 4: window 239..806, then 14 cells to N_4, all passing |

Run: `python3 kfree_exact.py 4 346700 cells 30000`, `python3 run_all.py 5,6,7,8,9,10`, `python3 run_big.py 31 100`, `python3 margin.py 5 300`.
