# ab + c never squarefree (paper, Theorem 9.4)

| File | What it does |
| --- | --- |
| `coregame.py` | the core game (Lemma 8.5) over types (slab, cell), solved exactly with OR-tools CP-SAT; objective coefficients rounded up |
| `game_c2.py` | first version: forcing layers 4, 9, 25, no refinement (c = 1 gives 1/25 and V = 1/50) |
| `game_gen.py` | final version: layers 4, 9, p_c² (25 if p_c ≤ 5); types split by q \| a for luck primes q \| c and by membership in the root classes of the first luck prime with roots |
| `gen_k1.jsonl` | output of `python3 game_gen.py 1 <c>` for the squarefree c ≤ 100 with p_c ≤ 7: d = maximum clique density, V = game value, second_clique = best congruence set not inside a maximum clique |
| `brute_c.py` | exact maximum c-valid sets at small N by clique search |

Results: V_c < d_c for 49 of the 51 squarefree c ≤ 100 with p_c ≤ 7 (all but 10 and 13); V_c equals the best congruence set for 33 of them.
`brute_c.py` agrees with the root class for c = 2, 3 (N ≤ 400), 6, 21, 34 (N ≤ 600), 10, 13 (N ≤ 800).
Not run: c with p_c ≥ 11 (22, 30, 37, 42, 57, 58, 70, 78, 85, 93). Requires `pip install ortools`.
