# The cube-free analogue (paper, Section 9)

Question: the largest A ⊆ [N] with ab + 1 never cube-free (a = b allowed). Answer (Theorem 9.1): c57(N) = #{n ≤ N : n ≡ 57 mod 125} for every N. The maximisers are the full classes 57 and 68 mod 125, plus {182, 193} for 193 ≤ N ≤ 306 and {57, 239}, {193, 239} for 239 ≤ N ≤ 306.

| File | Covers | Run |
| --- | --- | --- |
| `cube_maxsets.py` | all maximum sets for every N ≤ 700 (exact clique search) | `python3 cube_maxsets.py 700` |
| `cube_small.py` | maximum = c57(N) up to 40,000 (independent clique check at block ends) | `python3 cube_small.py 40000` |
| `cubeM.c` | exact one-witness bound at a given N | `gcc -O2 -o cubeM cubeM.c && ./cubeM 2000000` |
| `cube_cells.py`, `cube_cells.out` | 20 cells covering 700 ≤ N ≤ 2·10⁶, all below c57 | `python3 cube_cells.py` (needs `cubeM`) |
| `cube_analytic.py` | analytic bound, all N ≥ 1.94·10⁶ | `python3 cube_analytic.py` |
