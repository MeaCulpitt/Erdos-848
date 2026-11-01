# Independent check of Li's degree proposition

**Claim checked.** Proposition "Uniform mixed degree" in A. C. Li, *The Exact Extremal Bound in Erdős Problem 848*. For N ≥ 5·10⁶, every b ∈ V outside the classes 7 and 18 mod 25 has more than N/50 + N/525 squarefree neighbours (a with ab+1 squarefree) in each of C7 ∩ [1, N] and C18 ∩ [1, N].

**Method.** `fastli.c` is `fast848.c` modified to track the largest H₇(b) and H₁₈(b) over all b ∈ R ∩ V, at the point N = 5·10⁶ and at the ends of 70 blocks of relative width 1% up to 10⁷ (`./fastli 10000000 5000000`; output `li1e7.txt`). Each block (N_lo, N_hi] is checked conservatively: the class size at N_lo minus the largest H at N_hi, against Li's threshold at N_hi. An independent numpy brute force agrees on max H₇ = 300 and max H₁₈ = 299 at N = 20,000. The run took 56 minutes on 2 cores.

**Result.** The proposition holds on every block. The tightest block is (5.10·10⁶, 5.15·10⁶]: minimum degree 128,405 against a threshold of 112,843, a margin of 13.8%. At N = 10⁷ the minimum degree is 250,629 against 217,611.

Note: the `thr` column in `li1e7.txt` is the threshold at the lower end of each block. The conservative comparison uses the threshold at the upper end, which is the `thr` of the next row (or N_hi·(1/50 + 1/525)).

**Remark.** max H₇(b)/N ≈ 0.01468 throughout, matching the sharp rigidity constant g1* = (1/3 + 2/3·β∞)/25 = 0.01467 of Theorem C(1).
