# Exact V_2 certificate for all 16 (zA, zB) pairs

`bb.c` (exact integer branch-and-bound) was run for every (zA, zB) pair in `../lemma/v2grid.json`. Inputs are ceil(x·10¹⁵) of beta_up(zB), alpha_s = alpha_up(zA) − tailA, and (23/25)·tailA, computed as in `n0lemma.py` and `vk2.py` (primes to 10⁷ plus the Rosser–Schoenfeld tail). Output: `bb_allpairs.out`.

All 16 pairs PROVED V_2 ≤ F, using about 1.3–1.5 million nodes each (57 s in total). Each certified F exceeds the HiGHS value in `v2grid.json` by at most 3.0·10⁻¹⁴, from the upward rounding, which costs at most 3·10⁻¹⁴·N of slack. The grid's smallest slack is above 1.5·10⁻³·N, so every cell of `tmgrid.log` still passes.
