# The second-best density λ* for Erdős 848 (notes, 2026-11-01)

λ* = lim sup over N of max{|A|/N : A ⊆ [N] valid, A not inside C7 and not inside C18}.

We know λ* ≥ 1/50, from F = {n ≡ 7 (mod 25), n ≡ 1 (mod 4)} ∪ {n ≡ 18 (mod 25), n ≡ 3 (mod 4)} (Lean-verified). The question is whether λ* = 1/50.

## Part 1: sets inside C7 ∪ C18 (a human-readable proof)

**Theorem E.** If A ⊆ [N] is valid, A ⊆ C7 ∪ C18 and A meets both classes, then |A| ≤ (1/50 + o(1))N. F shows this is sharp.

**Proof.** Let X = A ∩ C7 and Y = A ∩ C18. Write x and y for their sizes relative to |C7 ∩ [N]| and |C18 ∩ [N]|; both are ≈ N/25. For a ∈ X and b ∈ Y we have ab + 1 ≡ 7·18 + 1 ≡ 2 (mod 25). So 25 never divides ab + 1, and ab + 1 is non-squarefree iff one of these holds:
- (4) a and b are odd with ab ≡ 3 (mod 4);
- (Q) 9 | ab + 1, or p² | ab + 1 for some prime p ≥ 7.

*Key estimate.* Fix b. The set Comp_Q(b) of a ∈ C7 with (Q) has relative density at most c + o(1), uniformly in b ≤ N, where

c = 1/9 + Σ_{p≥7} 1/p² = 0.16225 < 1/6.

The condition 9 | ab + 1 picks out one class mod 9, and p² | ab + 1 one class mod p². Primes p ≤ N^{1/3} are counted by the union bound. Larger p contribute o(N), by Lemma 3.3 (π(Y) terms) and Lemma 3.5 (the lattice count, which is 2^{ω(b)}·N^{2/3+o(1)}). By CRT, Comp_Q(b) meets each class mod 4 in density (1/4)·c (or (1/2)·c for the even class), up to o(1).

Split X = X_E ∪ X_1 ∪ X_3 by a mod 4 (even, 1 or 3), and Y likewise, with relative sizes x_E ≤ 1/2, x_1, x_3 ≤ 1/4, and so on. A pair not forced by 4 must satisfy (Q), so it lies in Comp_Q of its partner. There are four cases.

1. **One side has no odd element**, say Y ⊆ evens. Then every pair is a (Q) pair, so X ⊆ Comp_Q(b) and x ≤ c. If X has an odd element a, then Y ⊆ Comp_Q(a) ∩ evens, so y ≤ c/2. Otherwise y ≤ c/2 as well. In all cases x + y ≤ 2c.
2. **Y has odd elements of both classes.** Then X_1 ⊆ Comp_Q(b₁) for some b₁ ∈ Y_1, X_3 ⊆ Comp_Q(b₃) for some b₃ ∈ Y_3, and X_E ⊆ Comp_Q(b₁). So x ≤ c/4 + c/4 + c/2 = c.
   - If X also has both odd classes, then y ≤ c by symmetry, and x + y ≤ 2c.
   - If X's odd elements are all ≡ 1, then x ≤ 3c/4, and y ≤ 1/4 + 3c/4 because Y_3 is free and Y_1 ∪ Y_E ⊆ Comp_Q(a). So x + y ≤ 1/4 + 3c/2.
   - If X has no odd element, then y ≤ c (case 1).
3. **Each side has exactly one odd class, the same one**, say both ≡ 1. Then X_1 × Y_1 consists of (Q) pairs, so x_1 ≤ c/4 and y_1 ≤ c/4. Also x_E, y_E ≤ c/2. So x + y ≤ 3c/2.
4. **Each side has exactly one odd class, opposite ones** (X_odd = X_1, Y_odd = Y_3, the shape of F).
   - If X_E = Y_E = ∅, then x + y ≤ 1/4 + 1/4 = 1/2.
   - If X_E ≠ ∅ and Y_E = ∅, then Y ⊆ Comp_Q(a_E), so y ≤ c. Also x ≤ 1/4 + x_E ≤ 1/4 + c/2. So x + y ≤ 1/4 + 3c/2.
   - If both are nonempty, then x, y ≤ c, so x + y ≤ 2c.

So x + y ≤ max(1/2, 1/4 + 3c/2, 2c) + o(1). Since c < 1/6, this maximum is 1/2. Hence |A| ≤ (x + y)·N/25 + o(N) ≤ (1/50 + o(1))N. ∎

The whole proof rests on the numerical fact that 1/9 + Σ_{p≥7} p⁻² = 0.16225 < 1/6, with margin 0.0044. A computer check agrees. An exact max-flow over residue types, with the forcing layers 4, 9, 25 and also 49, gives the best two-class configuration as exactly 1/50.

## Part 2: sets with elements outside C7 ∪ C18 (computer-assisted)

These are the elements in the 23 residue classes R. Each lies in some self-forcing class ±ι_p mod p², for some p ≡ 1 (mod 4) with p ≥ 13.

**Method: the all-witness game.** Use 525 types: (a mod 25) × (even, 1 or 3 mod 4) × (a mod 9, with 3 | a merged). Every element of A serves as a witness, so

|A ∩ t| ≤ min over s ∈ P of M[s][t]·N + o(N), where P is the set of types A meets.

The entries M[s][t] (times w_t) are:
- **forced** by 4, 9 or 25: d_t, where d_t = 1 for C-types and α⁺ for R-types (a ∈ V needs some p ≥ 13 with p² | a² + 1);
- **not forced, C-target:** β⁺ = Σ_{q≥7} 1/q²;
- **not forced, R-target:** j = α⁺β⁺ + κ. This needs both p² | a² + 1 and q² | ab + 1. For p ≠ q, CRT gives (2/p²)(1/q²). For p = q, both conditions hold only if a ≡ ±ι_p and a ≡ −b⁻¹ (mod p²), at most one class, so 1/p². Hence κ = Σ_{p≡1(4), p≥13} 1/p².

Each entry is a rigorous asymptotic upper bound, uniform in the witness; the exact error terms are in Part 3. So λ* ≤ V, where V = max over type sets P not inside one class of Σ_t min_s M[s][t].

**Results (exact MILP, HiGHS):**

| Constants | V | dual bound |
| --- | --- | --- |
| Independent model (j = αβ) | 0.020000 | 0.020000 |
| Worst-case correlation (j = αβ + κ) | 0.020000 | 0.020000 |
| Rigorous union-bound constants (β⁺ = 0.05114, α⁺ = 0.02763, κ = 0.01381, j⁺ = 0.01523) | 0.020000 | 0.020000 |

In every run the optimum is F itself (14 types, all mutually forced), so the large primes never help.

## Part 3: closing the gaps

### Gap 1: an exact certificate (`lamcert.c`)

The MILP has structure that reduces it to a small exact enumeration.

**Core reduction.** For a type set P, let its *core* be K = {t ∈ P : every s ∈ P forces t}. Forcing is symmetric, so P ⊆ F(K), where F(K) is the set of types forcing every member of K. The core contains only C-types. An R-type never forces itself: a² ≡ −1 has no solution mod 4 or mod 9, and mod 25 only in C7 or C18.

Every non-core C-type in P has some s ∈ P that does not force it, so it contributes at most β. Every R-type in P is bounded by its own witness, so it contributes at most j. Hence

value(P) ≤ U(K) = w(K) + β·w(C ∩ F(K) \ K) + j·w(R ∩ F(K)).

**Cells.** A C-type is forced by a type outside its own class only through 4 or 9; 25 never does it, since 7·18 + 1 ≡ 2 and 7r + 1 ≢ 0 for r ∈ R. So forcing depends only on the type's cell mod 36: 21 cells, (even, 1 or 3 mod 4) × (3 | a, or one of 6 unit classes mod 9).

A core is therefore a pair (M₇, M₁₈) of cell sets in which every cross pair is forced. Each half is automatically a clique, since 25 forces all pairs inside a class. U(K) is then a function of (M₇, M₁₈) through:
- the cells forced with all of M₁₈ (the C7 part of F);
- the cells forced with all of M₇ (the C18 part);
- the cells forced with all of M₇ ∪ M₁₈ (the R part, for all 23 classes mod 25).

**The check.** `lamcert.c` enumerates every such pair for which F(K) admits a set not inside one class: 51,223 cores. It evaluates 900·U in exact integer arithmetic, with β = 0.052 and j = 0.016, and was re-run with j = 0.0169 (`./lamcert 52000 16900`, PROVED). These are rational upper bounds with slack over β⁺ = 0.05114 and over j⁺: 0.01523 for the main part alone, and 0.01551 once the p > 500 tail τ is included (Gap 2). It runs in 0.02 s.

**Result.** max U = 1/50 exactly, attained only by F and its mirror. The bound still holds for j up to 0.01721 (with β = 0.052), for β up to 0.0556 (with j = 0.0169), and for β up to 0.066 (with j = 0.016). The check is not vacuous: with β = 0.10 and j = 0.03 it fails. This is independent of HiGHS, and it confirms the MILP value.

### Gap 2: the error terms

Fix N, a valid A not inside one class, and the type set P that A meets. Every bound below is uniform in the witness b ≤ N.

1. **Forced C-target.** |A ∩ t| ≤ |t ∩ [N]| = w_t·N + O(1).
2. **Non-forced C-target.** |A ∩ t| ≤ #{a ∈ t ∩ [N] : q² | ab + 1 for some q ≥ 7}. By Lemmas 3.2, 3.3 and 3.5 (the E_B estimate of Theorem 4.1) this is at most w_t·β⁺·N + O(N^{2/3+o(1)}), with β⁺ = Σ_{q≥7} q⁻² + tail ≤ 0.05114.
3. **R-target, with its own witness or any non-forcing witness.** We need a ∈ V and q² | ab + 1 for some q ≥ 7. Fix P₀ = Q₀ = 500 and Y = N^{0.6}, and split the event into three parts:
   - **Main part, p ≤ P₀ and q ≤ Q₀.** By CRT (p, q are coprime to 900), the pairs with p ≠ q contribute at most Σ (2w_t·N/(p²q²) + 2). The pairs with p = q contribute at most Σ (w_t·N/p² + 1), because a ≡ ±ι_p and a ≡ −b⁻¹ (mod p²) leave at most one class. Total: w_t·N(α⁺β⁺ + κ) + O(1).
   - **p-tail, p > P₀.** Only primes p ≡ 1 (mod 4) occur. By Lemma 3.3, primes P₀ < p ≤ Y give at most w_t·N·τ + 2π(Y), with τ = 2Σ_{p>P₀, p≡1(4)} p⁻². By Lemma 3.4, p > Y gives O((N/Y)² log N) = O(N^{0.8} log N). Numerically τ ≈ 0.00027 (summed to 10⁷, with an explicit tail beyond), so τ ≤ 0.00028 and this part is at most 0.00028·w_t·N + O(N^{0.8} log N). (An earlier draft used the cruder 2Σ_{p>500} p⁻² ≤ 0.0016 over all primes; it also suffices.)
   - **q-tail, q > Q₀, with the p ≤ P₀ event.** This is at most w_t·N·α⁺·Σ_{q>Q₀} q⁻², which together with the main part stays below w_t·N·α⁺β⁺. The rest is O(P₀·Y) "+2" terms plus P₀ times the large-prime count beyond Y. That count uses the crude lattice lemma for an arbitrary target (paper, Lemma 8.3): #{a ≤ N : q² | ab+1, q > Y} ≤ N^{o(1)}(4N/Y + 2N²/Y²), which needs no information about the target class and is N^{0.8+o(1)} at Y = N^{0.6}.

   So |A ∩ t| ≤ w_t·N·j⁺ + O(N^{0.8+o(1)}), where j⁺ = α⁺β⁺ + κ + τ ≤ 0.01551 with the split above. (Final version, 2026-11-02: for q > 500 the p-condition is dropped, so j⁺ = α⁺β₅₀₀ + κ + τ + τ_B ≤ 0.01577, still below j = 0.0169. This removes the 1656·43·π(Y) bookkeeping term, which was two-thirds of the explicit error.) This is below j = 0.0169 used in the certificate, and below the certified slack 0.01717.

Summing over the at most 525 types, and applying Gap 1 with constants β = 0.052 and j = 0.0169, both inside the certified slack:

**Theorem F (second-best density).** There is a constant C such that every valid A ⊆ [N] not contained in C7 or C18 satisfies |A| ≤ N/50 + C·N^{0.81}. The set F shows the constant 1/50 is sharp. Hence λ* = 1/50, and the limit exists.

**Reduced, kernel-checked certificate (`LamCert.lean`).** Write A(M) for the cells forced with all of M. Replacing M by A(A(M)) keeps A(M) and does not lower U, so both halves of a core may be taken closed. Only 64 sets have the form A(M), giving 439 admissible pairs. `LamCert.lean` proves the closure reduction, the 64×64 check, the equality case (only F and its mirror) and that cell forcing is exactly 4 | ab+1 or 9 | ab+1, all by kernel `decide` (no `native_decide`), in about 45 s with Lean 4.36.0-rc2 and Mathlib. The same file fails, as it should, with β = 0.10 and j = 0.03.

**Explicit constant (`explicitC.py`).** With every error term written out (paper, Section 8.5), E(N) = N^{2/3+o(1)}, E(N) < N from about N = 10^11.7, and |A| ≤ N/50 + 170·N^0.81 for every N (grid maximum 167.5 near 10^11.75; Robin's ω bound beyond 10^601). An earlier accounting, charging one residue error per prime pair p ≤ 500 < q ≤ Y, gave C = 680; dropping the p-condition for q > 500 cut E(N) by 8–12×. The large-prime lemma for any target is used in the explicit form #{a ≤ N : q² | ab+1, q > Y} ≤ 2^{ω(b)+1}(2(N+1)/Y + (N²+1)/Y²).

This is written up as Section 8 (Theorem 8.1, Proposition 8.2, Lemmas 8.3–8.5, Proposition 8.6) of the paper. Remaining work is presentational. Both former loose ends, the explicit constant and a Lean version of the certificate, are now done (above).
