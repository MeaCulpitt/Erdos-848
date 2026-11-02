# Erdős Problem 848: an independent all-N proof, with stability, rigidity and the second-best density

[Erdős Problem 848](https://www.erdosproblems.com/848) asks whether the largest A ⊆ {1, …, N} with ab + 1 never squarefree (for all a, b ∈ A, including a = b) is the residue class 7 mod 25. Sawhney proved this for all sufficiently large N, with no explicit threshold. Several all-N proofs followed in 2026, among them A. C. Li's, which comes with a Lean formalisation ([SSRN 7230480](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7230480)). None of these, including this one, has yet been refereed.

This repository contains a second, independent proof for every N, together with new structural results, and all the code, certificates and logs needed to check them. The paper is [`paper/erdos848_paper.md`](paper/erdos848_paper.md).

## Results

- **Theorem A** (Li; independent proof here). For every N, every valid A ⊆ [N] has |A| ≤ c7(N) = #{n ≤ N : n ≡ 7 mod 25}. This uses an explicit threshold N₀ = 6.7838·10⁶ and computation below it.
- **Theorem B** (stability). For N ≥ N₀, a valid set not inside one class has at most (N − 7)/25 elements, and at most (0.029289 + o(1))N.
- **Theorem C** (rigidity and extremisers). A valid set with one element outside C7 keeps asymptotically at most a fraction 0.3667… of C7, and this is sharp. The maximisers are exactly C7 (and C18 when it has the same size), plus four small sets for 41 ≤ N ≤ 81.
- **Theorem D / 8.1** (second-best density). The densest valid set not inside one class has size N/50 + O(N^0.81), with an explicit constant: at most N/50 + 30·N^0.81 for every N. It is sharp up to lower-order terms: F has at least N/50 − 2 elements, where F = {7 mod 25, 1 mod 4} ∪ {18 mod 25, 3 mod 4}.

## Status

Every proof step is backed by computation, and the key certificates are cross-checked by independent implementations. The constructions and the certificate for Theorem 8.1 (Proposition 8.6) are verified in Lean 4. **The paper has not yet been refereed or read in full by a human expert.** Reports of errors are welcome as GitHub issues.

## How this was made

The arguments, code and certificates were developed with AI assistance (Anthropic's Claude), directed by the author. Every computational step was re-run, and the main ones were re-implemented independently (see `referee/`). An AI-run consistency review of the paper found and fixed several slips before release. None of this replaces human review, which is the main thing this work still needs.

## Layout

| Folder | What it checks | Main files |
| --- | --- | --- |
| `paper/` | The paper | `erdos848_paper.md` |
| `computation/` | Theorem A for N ≤ 10⁷ (Sawhney's cases S1–S4, exact counts) and exact clique search for N ≤ 3806 | `fast848.c`, `e848cases.c`, `e848b.py`, logs `r1e7_fast.txt`, `r848.txt`; brute-force cross-checks `xcheck.py`, `exhaust.py`, `alledges.py`, `spfcheck.py` |
| `lemma/` | The explicit threshold N₀: error terms, the witness game V₂, and the grid on [10⁷, 10⁶⁰] | `n0lemma.py`, `vk2.py`, `tmgrid.py` + `tmgrid.log` (2525 cells, 0 failures), `tail60.py`, `omegaV.c`; notes `README.md` |
| `referee/` | Independent re-implementation | `bb.c` (exact integer branch-and-bound for V₂, all 16 parameter pairs: `bb_allpairs.out`), `cellsbig.py`/`cellsbig2.py` (grid from N₀ = 6.7838·10⁶), `brute.py`/`brute2.py` (brute-force tests of the Pell and lattice lemmas) |
| `margins/` | Exploration of the type-matrix game | `typemat.c`, `solve.py` |
| `rigidity/` | Theorem C(2): exact maximisers | `nsc.py` (exact cliques not inside one class, N ≤ 1006), `sbrute.py` (independent S1–S4 brute force), `small31.txt`, `strict69.txt` |
| `li_check/` | Independent check of Li's uniform-degree proposition for 5·10⁶ ≤ N ≤ 10⁷ | `fastli.c`, `li1e7.txt`, `li_degree_check.md` |
| `lambda_star/` | Section 8: second-best density 1/50 | `lamcert.c` (exhaustive exact certificate, 51,223 cores), `closed.py` (the 64 closed sets and 439 pairs), `jthr.py` (slack thresholds), `explicitC.py` + `explicitC.out` (explicit constant, C = 170), `explicitC_omega.py` + `explicitC_omega.out` (ω-refinement with Rankin's bound, C ≤ 92.4), `omgrid.c` + `omega_envelope.py` + `omega_envelope_check.py` (rigorous ω-count envelope to 10¹⁸), `explicitC_omega2.py` + `explicitC_omega2.out` (envelope from 10⁹, C ≤ 72.2), `segomega.c` + `seg1e11.txt` (exact ω-counts to 10¹¹, overall and in V), `explicitC_omega4.py` + `explicitC_omega4.out` (final: C ≤ 29.9, so C = 30), `vomega.c` (exact ω-counts in V), `lamgame.py` (525-type MILP), `bipflow2.py`, `wgame4.py` (general local witness game), notes `lambda_star.md` |
| `lean/` | Lean 4 proofs | `Erdos848Constructions.lean` (validity of C7, C18, F and the four small maximisers), `LamCert.lean` (Proposition 8.6 by kernel `decide`, including the equality case) |

## Reproducing the main checks

Requirements: gcc (with OpenMP), Python 3 with numpy, scipy, sympy, networkx and python-igraph. pip may need `--break-system-packages`.

```bash
# Theorem A for N <= 10^7 (can take hours; uses all cores)
cd computation && gcc -O3 -march=native -fopenmp -o fast848 fast848.c -lm && ./fast848 10000000 3806

# Exact clique search, N <= 3806 (about 13 minutes)
python3 e848b.py 3806

# Explicit threshold and grid on [10^7, 10^60]
cd ../lemma && python3 n0lemma.py tm && python3 tmgrid.py

# Independent grid from N0 = 6.7838e6
cd ../referee && python3 cellsbig.py 1e60

# Exact V_2 certificate (one parameter pair; inputs are ceil(x*1e15), see bb_allpairs.out)
gcc -O2 -o bb bb.c

# Exact maximisers not inside one class, N <= 1006
cd ../rigidity && python3 nsc.py 1006

# Li's degree proposition, 5e6 <= N <= 1e7 (about 1 hour on 2 cores)
cd ../li_check && gcc -O3 -fopenmp -o fastli fastli.c -lm && ./fastli 10000000 5000000

# Second-best density certificate (0.02 s) and its slack
cd ../lambda_star && gcc -O2 -o lamcert lamcert.c && ./lamcert 52000 16900 && python3 jthr.py

# Explicit constant: C = 170 without the omega-refinement, 92.4 with Rankin's bound, 30 with exact counts to 1e11 (grids ~30 min each)
gcc -O3 -march=native -fopenmp -o segomega segomega.c -lm && ./segomega 100000000000 100000 > seg1e11.txt   # ~25 min on 2 cores
python3 explicitC.py && python3 explicitC_omega.py && python3 explicitC_omega4.py
```

### Lean

Tested with Lean `v4.36.0-rc2` and Mathlib at commit `a2f96aabcf72be9e18bece4b5c7c54fcc0c029f4` (the toolchain and commit are pinned in `lean/`). Each file was checked from a built Mathlib with

```bash
cd mathlib4 && lake env lean /path/to/lean/LamCert.lean
```

`LamCert.lean` takes about 45 seconds; `Erdos848Constructions.lean` takes a few seconds. Both report only the standard axioms (`propext`, `Classical.choice`, `Quot.sound`). `LamCert.lean` uses `decide` only, never `native_decide`. The `lakefile.toml` in `lean/` follows the usual Mathlib setup (`lake exe cache get`, then `lake build`), but has not itself been test-built.

## Related work

The forum thread for Problem 848 records the earlier steps: van Doorn's bound 0.108N and Weisenberg's improvement to about 0.105N, StijnC's early computations, Sawhney's large-N proof, and the AI-assisted explicit thresholds led by N. Sothanaphan, down to 2.64·10¹⁷.

- T. F. Bloom, [Erdős Problem #848](https://www.erdosproblems.com/848) and the [discussion thread](https://www.erdosproblems.com/forum/thread/848).
- M. Sawhney, [note on Problem 848](https://www.math.columbia.edu/~msawhney/Problem_848.pdf).
- A. C. Li, *The Exact Extremal Bound in Erdős Problem 848* ([SSRN 7230480](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7230480); [code and Lean](https://github.com/crabsatellite/erdos-848-squarefree-product)).
- Other all-N claims: Pitchford ([Zenodo](https://zenodo.org/records/21647629)), Zanghi ([GitHub](https://github.com/bzanghi/erdos-848)), Durfee ([GitHub](https://github.com/AstroCat93/erdos-848-verification)).
- R. Jung et al., [erdos-banger](https://github.com/The-Obstacle-Is-The-Way/erdos-banger): Lean formalisation of Sawhney's stability theorem.

## Licence

Code: MIT (see `LICENSE`). Paper: CC BY 4.0 (see `paper/LICENSE.md`).
