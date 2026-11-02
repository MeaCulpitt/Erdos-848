# Stability, rigidity and exact extremisers for Erdős Problem 848

Nov 1, 2026 · @Luke

## Abstract

Erdős and Sárközy asked whether the largest A ⊆ {1, …, N} with ab + 1 never squarefree is the residue class 7 mod 25. Sawhney proved this for large N, and recent computer-assisted work, notably Li's Lean-verified proof, extends it to every N. We give an independent proof for every N by a different method, with explicit threshold N₀ = 6.7838·10⁶. It rests on a finite "witness game" on 63 residue types modulo 900, whose value 0.0294059… is certified by exact integer branch-and-bound.

Our main new results describe valid sets beyond the maximum:

- **Explicit stability.** For N ≥ 6.7838·10⁶, every valid set not inside one class has at most (N − 7)/25 elements, and at most 0.0293N asymptotically. This makes Sawhney's qualitative η explicit: η = 0.0016 at N = 10⁷, rising to about 0.0107 as N → ∞.
- **Sharp rigidity.** One element outside 7 mod 25 leaves at most a fraction 0.3667… of that class. This is the sharp form of the degree estimate in Li's proof.
- **Exact maximisers for every N.** They are the classes 7 and 18 mod 25, plus four small sets not inside one class when 41 ≤ N ≤ 81.
- **A two-class set of density 1/50.** It meets both classes, it beats the natural "one class plus one outsider" configuration, and it is optimal. Every valid set not inside one class has at most N/50 + O(N^0.81) elements, so the second-best density is exactly 1/50.

The constructions and the certificate for the second-best density are verified in Lean 4. Every computation is reproducible and was cross-checked by an independent implementation. This includes a check of the key degree proposition of Li's proof for 5·10⁶ ≤ N ≤ 10⁷.

## 1. Introduction

Call A ⊆ \[N\] = {1, …, N} **valid** if ab + 1 is not squarefree for all a, b ∈ A, including a = b. Erdős and Sárközy asked whether the maximum of |A| over valid sets is attained by {n ≤ N : n ≡ 7 (mod 25)} ([Erdős Problem #848](https://www.erdosproblems.com/848)). This class is valid because 7² + 1 = 50, so 25 | ab + 1 whenever a ≡ b ≡ 7 (mod 25). The class 18 ≡ −7 works for the same reason.

Van Doorn gave |A| ≤ (0.108… + o(1))N, and Weisenberg improved the constant to about 0.105 by inclusion–exclusion. Early computations posted by StijnC already pointed to stability, and found small valid sets avoiding both classes, such as {41, 70, 239, 437} at N = 606. Sawhney ([note](https://www.math.columbia.edu/~msawhney/Problem_848.pdf)) proved the conjecture for N ≥ N₀, with N₀ not computed, and noted a qualitative stability property. Sawhney and Sellke discuss the problem in Section IV.1 of arXiv:2511.16072, and Alexeev, Mixon and Sawin treat the companion problem where ab is never squarefree (arXiv:2507.01928). As Alexeev pointed out, Erdős's original question has no restriction to large N. Later AI-assisted work on the forum, led by Sothanaphan, made N₀ explicit, reaching exp(1420) ([forum](https://www.erdosproblems.com/forum/thread/848)). That is far beyond the range of computation.

Since mid-2026 several unrefereed, AI-assisted all-N claims have appeared. Sothanaphan reached N₀ = 2.64·10¹⁷, and full claims came from Pitchford with Codex ([Zenodo](https://zenodo.org/records/21647629)), A. C. Li (SSRN, with Lean; analytic range reportedly from 5·10⁶), Zanghi ([GitHub](https://github.com/bzanghi/erdos-848), N₀ = 5·10⁸) and Durfee ([GitHub](https://github.com/AstroCat93/erdos-848-verification), N₀ = 4.2·10⁷). All of these follow Sawhney's case split, and most cover small N with colouring certificates. The argument here is independent of them. Its new ingredients are the type-matrix witness game, which gives N₀ = 6.78·10⁶, and Theorems B and C, which none of those claims state.

Write c7(N) = #{n ≤ N : n ≡ 7 (mod 25)} = ⌊(N − 7)/25⌋ + 1, and C7, C18 for the classes 7 and 18 mod 25.

**Theorem A (Li; independent proof here).** For every N ≥ 1, every valid A ⊆ \[N\] has |A| ≤ c7(N).

**Theorem B (stability).** Let N ≥ 6.7838·10⁶. If A ⊆ \[N\] is valid and not contained in C7 or C18, then |A| ≤ (N − 7)/25 < c7(N). Moreover |A| ≤ (0.029289 + o(1))N. Equivalently, every valid set with more than about 0.0293N elements lies in one class.

**Theorem C (rigidity and extremisers).**

1. If A is valid and A ⊄ C7, then |A ∩ C7| ≤ (g1\* + o(1))N, where g1\* = (1/3 + 2/3·β∞)/25 = 0.0146697… and β∞ = 1 − ∏\_{p≥7}(1 − p⁻²). This constant is sharp.
2. For N ∉ \[41, 81\], the maximisers in Theorem A are exactly C7 ∩ \[N\], together with C18 ∩ \[N\] when c18(N) = c7(N). For 41 ≤ N ≤ 81 there are also the maximisers {7, 41}, {32, 43}, {41, 43} and {32, 43, 57}, each in its own range of N.

**Theorem D (a dense two-class set).** The set F = {n ≡ 7 (mod 25), n ≡ 1 (mod 4)} ∪ {n ≡ 18 (mod 25), n ≡ 3 (mod 4)} is valid. It has density 1/50 and meets both classes. Among sets defined by congruences mod 900, it is the densest valid set not inside one class. Moreover F is optimal: every valid A ⊆ \[N\] not inside C7 or C18 has |A| ≤ N/50 + 75·N^0.81, so the second-best density λ\* equals 1/50 (Section 8).

Theorems B, C and D are new. Sawhney's note gives stability with an unspecified η and leaves open whether 18 mod 25 also attains the maximum. Li's proof of Theorem A, and the other all-N claims, give no stability constant and no description of the maximisers. The Lean formalisation in erdos-banger proves stability with η = 1/2000 beyond an ineffective N₀.

**Method.** Each a lies in one of 63 *types*, given by its class mod 25 (C7, C18 or the rest R), mod 4 and mod 9. Whether p² | ab + 1 is forced for p ∈ {2, 3, 5} depends only on the types of a and b. Fix a valid A and pick one or two "witnesses" b ∈ A. Every other a ∈ A must make ab + 1 non-squarefree. Optimising the witness choice against every possible set of types gives a finite min–max problem with value V₂ = 0.0294059… < 1/25.

Sections 3–5 bound the error terms explicitly, giving Theorem A for N ≥ 6.7838·10⁶. Section 6 covers smaller N by computation. Section 7 proves Theorems B and C and the first part of Theorem D, and Section 8 proves that F is optimal.

The arguments and code were developed with AI assistance and independently re-run (Appendix). They have not yet been reviewed by a human expert.

## 2. Local structure

Let V = {x ≥ 1 : x² + 1 is not squarefree}. Taking a = b shows that every valid set lies in V.

**Lemma 2.1.** x ∈ V if and only if p² | x² + 1 for some prime p ≡ 1 (mod 4). For p = 5 this means x ≡ 7 or 18 (mod 25). Hence C7 ∪ C18 ⊆ V, and x ∈ R lies in V iff p² | x² + 1 for some prime p ≡ 1 (mod 4) with p ≥ 13.

*Proof.* x² + 1 ≡ 1 or 2 (mod 4) and is never divisible by 3. An odd prime p divides x² + 1 only if −1 is a square mod p, that is, p ≡ 1 (mod 4). The roots of x² ≡ −1 (mod 25) are 7 and 18. ∎

**Types.** The *type* of a is the triple (κ, μ, ν) where:

- κ ∈ {C7, C18, R} is the class of a mod 25;
- μ ∈ {E, 1, 3} records a even, a ≡ 1 (mod 4) or a ≡ 3 (mod 4);
- ν ∈ {0, 1, 2, 4, 5, 7, 8} records 3 | a, or the unit class of a mod 9.

This gives 3·3·7 = 63 types. Each is a union of residue classes mod 900. Type t has density w\_t = w(κ)·w(μ)·w(ν), where w(C7) = w(C18) = 1/25, w(R) = 23/25, w(E) = 1/2, w(1) = w(3) = 1/4, w(0) = 1/3, and w(ν) = 1/9 otherwise.

**Forcing.** For q² ∈ {4, 9, 25}, say a witness type s *forces* a target type t if q² | ab + 1 for every a of type t and b of type s, for some such q. This happens exactly when one of the following holds:

| Modulus | Forced when |
| --- | --- |
| 25 | a, b both in C7, or both in C18 |
| 4 | a, b both odd, in different classes mod 4 |
| 9 | a, b both units mod 9, with ab ≡ 8 (mod 9) |

When t is a C-type and s does not force t, no a of type t and b of type s has 4 | ab + 1, 9 | ab + 1 or 25 | ab + 1. For 25, note that a ≡ 7 and 25 | ab + 1 force b ≡ 7, and similarly for 18. So non-squarefreeness must then come from p² with p ≥ 7.

**Lemma 2.2 (forced share).** If b ∉ C7, the C7-types forced by b have total density at most (1/25)(1 − (3/4)(8/9)) = (1/3)(1/25).

*Proof.* Forcing by 25 is impossible. Forcing by 4 removes at most one of the four classes mod 4, and forcing by 9 at most one of the nine classes mod 9. These conditions are independent. ∎

The class 7 mod 25 is special because a single modulus (25) forces every pair inside it. Every other source of non-squarefreeness has density well below 1.

## 3. Counting lemmas

Throughout, U is a union of types and w\_U its density. Two kinds of event are counted:

- the *B-event* p² | ab + 1, for a fixed witness b and a prime p ≥ 7 with p ∤ b;
- the *A-event* p² | a² + 1, for a prime p ≡ 1 (mod 4) with p ≥ 13.

The B-event fixes a in one class mod p², namely a ≡ −b⁻¹. The A-event fixes a in two classes, ±ι\_p.

**Lemma 3.1 (discrepancy).** Let U = S × {c}, with S a set of residues mod 36 and c a class mod 25. Let q ≥ 1 be coprime to 30. Then for any residue r,

```latex
\#\{a \le N : a \in U,\ a \equiv r \ (q)\} = \frac{|S|\,N}{900\,q} + \theta \cdot 19, \qquad |\theta| \le 1.
```

The error is at most 38 for a union over C7 and C18, at most 57 for S × R, and at most 3 for all of R. Write e\_U for the bound that applies to U.

*Proof.* Write a = a₀ + 25q·i. Since 25q is a unit mod 36, the condition a ∈ S (mod 36) holds for i in a set of |S| classes mod 36. A run of J consecutive i hits it J|S|/36 + O(18) times, and J ≤ N/(25q) + 1. For R, write it as Z/25 minus the two C classes. ∎

**Lemma 3.2 (small primes).** Let 𝒫 be a finite set of primes not dividing 30b, and let event p take r\_p classes mod p². Then

```latex
\#\{a \le N,\ a\in U : \text{some event } p\in\mathcal P \text{ holds}\} = w_U N\Big(1-\prod_{p\in\mathcal P}\big(1-\tfrac{r_p}{p^2}\big)\Big) + \theta\, e_U \Big(1+\prod_{p\in\mathcal P}(1+r_p)\Big).
```

*Proof.* Take the complement and apply Möbius inversion over subsets of 𝒫. Each term is a union of ∏ r\_p classes, each counted by Lemma 3.1. ∎

**Lemma 3.3 (medium primes).** For a single prime p, the count of a ∈ U with the B-event exceeds w\_U N/p² by at most min(e\_U, 2N/(25p²) + 2, N/p² + 1). It exceeds it by at most 1 if p² > N. For the A-event on R the excess is at most min(6, 2(N/p² + 1)), and at most 1 if p² > 2N.

*Proof.* These are Lemma 3.1, then the count ignoring the mod-36 condition, then the count ignoring U. A class mod p² > N meets \[N\] at most once. The roots satisfy ι + (p² − ι) = p², so at most one of them is ≤ N when p² > 2N. ∎

**Lemma 3.4 (Pell bound for large primes in x² + 1).** Let M = (N² + 1)/Y² and m\_j = ((T\_j + T\_j⁻¹)/2)², where T\_j = (2N + 1)^{1/(2j−1)}. Then

```latex
\#\{x \le N,\ x\in R : p^2 \mid x^2+1 \text{ for a prime } p>Y\} \le \sum_{j\ge1} \#\{2\le m\le \min(M,m_j) : m \text{ admissible}\}.
```

Here m is *admissible* if m mod 8 ∈ {1, 2, 5}, 25 ∤ m, and m has no prime factor in {3, 7, 11, 19, 23}.

*Proof.* Write x² + 1 = mp². Then m < M, and m ≥ 2. The number m is not a square, since X² − Z² = −1 has no solution with X ≥ 1. Primes q ≡ 3 (mod 4) never divide x² + 1. Also x² + 1 ≡ 1, 2, 5 (mod 8) and p² ≡ 1 (mod 8), and 25 ∤ x² + 1 for x ∈ R.

The positive solutions of X² − mZ² = −1 are η^{2j−1}, where η is the fundamental unit of Z\[√m\]. From mZ² = X² + 1 with Z ≥ 1 we get η ≥ √(m−1) + √m. Also η^{2j−1} = x + √(x²+1) ≤ 2N + 1. So a j-th solution with x ≤ N needs √(m−1) + √m ≤ T\_j, that is, m ≤ m\_j. The map x ↦ (m, j) is injective. ∎

**Lemma 3.5 (lattice bound for large primes in ab + 1).** Fix b, and let T\_b be the C7 ∪ C18 classes a with 4 ∤ ab + 1, 9 ∤ ab + 1 and 25 ∤ ab + 1. Let ω₁(b) be the number of distinct primes ≥ 7 dividing b. Then

```latex
\#\{a\le N,\ a\in T_b : p^2\mid ab+1,\ p>Y\} \le 2^{\omega_1(b)}\Big[\frac{2\lambda(N+1)}{Y} + \frac{c\sqrt{bN+1}}{b} + \frac{\lambda(bN+1)}{Y^2} + c\Big].
```

The constants (λ, c) depend only on the {2, 3, 5}-part of b; in all cases λ ≤ 0.5334 and c ≤ 18.94.

*Proof.* Write ab + 1 = ms² with s = p > Y. Then m < (bN + 1)/Y². Since s is coprime to 30, m mod 1800 lies in a set S\_b determined by b mod 1800. Also ms² ≡ 1 (mod b), so s lies in one of ρ\_b(m) classes mod b. Here ρ\_b(m) ≤ ρ\_{b₀}(m)·2^{ω₁(b)}, with b₀ the {2, 3, 5}-part of b. So the count for a given m is at most ρ\_b(m)(√((bN+1)/m)/b + 1).

The weight g(m) = ρ\_{b₀}(m)·1\[m ∈ S\_b\] is 1800-periodic. Computed exactly, its partial sums satisfy Σ\_{m≤x} g(m) ≤ λx + c. Partial summation then gives Σ g(m)/√m ≤ 2λ√M + c. ∎

## 4. The type-matrix bound

Fix truncation points z\_A, z\_B and put

```latex
\beta^{+} = 1-\prod_{7\le p\le z_B}\Big(1-\frac1{p^2}\Big) + \sum_{p>z_B}\frac1{p^2}, \qquad \alpha_s = 1-\prod_{\substack{13\le p\le z_A\\ p\equiv1\,(4)}}\Big(1-\frac2{p^2}\Big), \qquad \tau_A = 2\sum_{\substack{p>z_A\\ p\equiv1\,(4)}}\frac1{p^2}.
```

The tails are evaluated exactly up to 10⁷, and beyond that by the bound Σ\_{p>x} p⁻² ≤ 2.51012/(x ln x), which follows from Rosser–Schoenfeld.

**The witness game.** Let P be a set of types, and W ⊆ P with 1 ≤ |W| ≤ 2. Define

```latex
\mathrm{val}(P,W) = \sum_{\substack{t\in P\\ t \text{ a C-type}}} w_t\cdot\begin{cases}1 & \text{every } s\in W \text{ forces } t\\ \beta^{+} & \text{otherwise}\end{cases} \;+\; \sum_{\substack{t\in P\\ t\subseteq R}} w_t\,\alpha_s \;+\; \mathbf 1[P\cap R\neq\varnothing]\,\tfrac{23}{25}\tau_A,
```

```latex
V_2 = \max_{P}\ \min_{W\subseteq P,\ 1\le|W|\le 2} \mathrm{val}(P,W),
```

with the maximum over type sets P not contained in the C7-types and not contained in the C18-types.

**Theorem 4.1.** If A ⊆ \[N\] is valid and not contained in C7 or C18, then |A| ≤ V₂·N + E\_I(N), where E\_I is the explicit error of Section 5.

*Proof.* Let P be the set of types met by A. P is not contained in one class, because the type determines the class. Choose W attaining the minimum, and for each s ∈ W pick b\_s ∈ A of type s. Each type t ∈ P is bounded as follows.

1. **C-types forced by every witness.** Use |A ∩ t| ≤ |t ∩ \[N\]| = w\_t N + O(1), by Lemma 3.1.
2. **Other C-types.** Assign each one to a witness s ∈ W that does not force it, and let U\_s be the union of the types assigned to s. By Section 2, every a ∈ A ∩ U\_s has p² | ab\_s + 1 for some prime p ≥ 7. Lemma 3.2 handles p ≤ z\_B, Lemma 3.3 handles z\_B < p ≤ Y and Lemma 3.5 handles p > Y. Together they give |A ∩ U\_s| ≤ w\_{U\_s}·β⁺·N + E\_B(N).
3. **R-types.** Use A ∩ t ⊆ V ∩ t. By Lemma 2.1 the count is bounded by A-events for primes p ≥ 13. Lemma 3.2 on the union of the R-types in P handles p ≤ z\_A. Lemmas 3.3 and 3.4, applied over all of R, handle p > z\_A.

Summing gives val(P, W)·N plus the error terms. ∎

**Value of the game.** The game is a 0–1 problem over 2⁶³ type sets. It was solved by a mixed-integer program (HiGHS; Q. Huangfu and J. A. J. Hall, Math. Prog. Comp. 10 (2018), 119–142), and independently by an exact branch-and-bound in integer arithmetic. The inputs were scaled by 10¹⁵ and rounded up, so the certified value is an upper bound. For every one of the 16 pairs (z\_A, z\_B) ∈ {17, 29, 37, 41} × {13, 17, 19, 23}, the worst P is the set of all 63 types, and

```latex
V_2 = \tfrac{2}{25}\beta^{+} + \tfrac{23}{25}(\alpha_s+\tau_A).
```

At (z\_A, z\_B) = (17, 13) this is V₂ ≤ 0.0294059212, certified with 1,339,011 branch-and-bound nodes. The smallest of the 16 values is V₂(41, 23) ≤ 0.0292884.

The value is easy to see for P = all types. Take one witness of type (C7, E, 0) and one of type (C18, E, 0). A witness that is even and divisible by 3 never forces by 4 or 9, so each C-class gets density β⁺, from the witness in the other class. The content of the certificate is that no adversarial choice of P does better than this.

Since 1/25 − 0.0294059 = 0.0105941 > 0, Theorem A follows for every N with E\_I(N) ≤ 0.0105941N − 0.28. Section 5 makes this explicit.

## 5. The explicit threshold

**The error term.** Let k\_A and k\_B be the numbers of primes in the small-prime ranges of Lemma 3.2: primes p ≡ 1 (mod 4) with 13 ≤ p ≤ z\_A, and primes with 7 ≤ p ≤ z\_B. Then

```latex
E_I(N) = 2\cdot 38\,(1+2^{k_B}) + 38 + 57\,(1+3^{k_A}) + E_A(N) + 2E_B(N),
```

```latex
E_A(N)=\min_Y\Big[\sum_{z_A<p\le Y}\text{(Lemma 3.3 excess)} + \text{(Lemma 3.4)}\Big],\qquad E_B(N)=\max_{b\le N}\min_Y\Big[\sum_{z_B<p\le Y}\text{(Lemma 3.3 excess)} + \text{(Lemma 3.5)}\Big].
```

The maximum over b runs over the 2-, 3- and 5-profile of b and over k = ω₁(b). Here ω₁(b) = k forces b ≥ b₀·7·11···p\_k, which tames the factor 2^k.

**The ω-refinement.** Near N₀ the factor 2^{ω₁(b)} is the bottleneck, so witnesses with many prime factors are avoided. Let K\_k(N) = #{b ≤ N : b ∈ V, ω₁(b) ≥ k}, computed exactly (K₅(10⁷) = 672). Split A = A′ ⊔ A″, where A″ is the elements with ω₁ ≥ k₀.

- If A′ is not inside one class, apply Theorem 4.1 to A′ with witnesses from A′. Then |A| ≤ V₂N + E\_I(N; ω₁ < k₀) + K\_{k₀}(N).
- Otherwise, say A′ ⊆ C7 and A ⊄ C7. Use one witness b ∈ A″ \\ C7. Lemma 2.2 gives |A ∩ C7| ≤ g₁N + E\_II(N), with g₁ = (1/3 + (2/3)β⁺)/25 ≈ 0.01469, and |A \\ C7| ≤ K\_{k₀}(N).

The second case has much smaller density, so it never binds.

**Grid certification.** For fixed parameters (z\_A, z\_B, k₀, Y), every term of E is nondecreasing in N. So it suffices to cover \[N₀, 10⁶⁰\] by cells \[N\_lo, N\_hi\] with ratio 1.01 below 10¹³ and 1.1 above, and to check for each cell that

```latex
E(N_{hi}) \le \big(\tfrac1{25}-V_2\big)N_{lo} - 0.28 .
```

This gives |A| ≤ N/25 − 0.28 = (N − 7)/25 < c7(N) throughout the cell. Prime counts up to 4·10⁹ are exact, and beyond that come from Rosser–Schoenfeld and Dusart bounds.

Two independent implementations agree. The referee grid uses only (z\_A, z\_B) = (17, 13), and its smallest slack is +329.8, in the first cell \[6.7838·10⁶, 6.85·10⁶\]. The original grid covers \[10⁷, 10⁶⁰\]. It optimises the parameters per cell and has 2525 cells with no failures. Its slack, as a fraction of N, rises from 0.0016 at 10⁷ to 0.0106.

**Proposition 5.1 (tail).** For N ≥ 10⁶⁰, Theorem 4.1 holds with E\_I(N) ≤ 1.02·10⁻⁸·N.

*Proof.* Take (z\_A, z\_B) = (17, 13), Y = N^{2/3} and no ω-refinement. Let L = ln N. The terms are bounded as follows:

- the inclusion–exclusion constant is 1292;
- Lemma 3.3 on the A side is at most 6π(√(2N)) + π(N^{2/3});
- Lemma 3.4 is at most (1 + 10⁻⁴)N^{2/3}·J, where J = (1 + ln(2N+1)/ln(1+√2))/2 = O(L);
- Lemma 3.3 on the B side is at most 38π(√N) + π(N^{2/3});
- Lemma 3.5 is at most 2^k·(1.067N^{2/3} + 20√N).

Robin's bound ω(n) ≤ 1.38402·ln n/ln ln n gives 2^k ≤ N^{0.95933/ln L} ≤ N^{0.1947}. The prime counts use π(x) < 1.25506x/ln x. Each term divided by N decreases for N ≥ 10⁶⁰, and the total at N = 10⁶⁰ is 1.02·10⁻⁸·N. ∎

**Corollary 5.2.** Theorem A holds for all N ≥ 6.7838·10⁶, and every valid set not inside one class has |A| ≤ (N − 7)/25. (Sawhney suggested on the forum that large-sieve methods should bring N₀ down to about 10⁶. The witness game reaches the same order by a different route.)

## 6. Small N

**N ≤ 3806: exact clique search.** Valid sets are exactly the cliques in the graph on V ∩ \[N\] with edges {a, b} where ab + 1 is not squarefree. At N = 3806 this graph has 397 vertices and 36,248 edges. The clique number is nondecreasing in N, and c7 is constant on each block (6 + 25k, 31 + 25k\]. So it suffices to compute the clique number at N ≡ 6 (mod 25). It equals c7(N) at every such N ≤ 3806.

**3806 ≤ N ≤ 10⁷: case bounds.** Let H\_t(b, N) = #{a ∈ V ∩ C\_t, a ≤ N : ab + 1 not squarefree} for t ∈ {7, 18}, and let H\_odd(b, N) count the odd such a in C7 ∪ C18. Let v\_R(N) = |V ∩ R ∩ \[N\]|, and v\_R^odd(N) its odd part. Every valid A not inside C7 or C18 falls into exactly one of four cases.

| Case | Condition on A | Bound on \|A\| |
| --- | --- | --- |
| S1 | A ∩ R contains an even b | v\_R + max over even b ∈ V ∩ R of \[H₇(b) + H₁₈(b)\] |
| S2 | A ∩ R ≠ ∅ and all odd; A ∩ (C7 ∪ C18) all odd | v\_R^odd + max over odd b ∈ V ∩ R of H\_odd(b) |
| S3 | A ∩ R ≠ ∅ and all odd; an even b′ ∈ C7 ∪ C18 | v\_R^odd + max of H₇(b) over odd b ∈ R, plus max of H₁₈(b′) over even b′ ∈ C7 (or the same with 7 and 18 swapped) |
| S4 | A ∩ R = ∅, A meets C7 and C18 | max of H₇(b′) over b′ ∈ C18, plus max of H₁₈(b) over b ∈ C7 |

Each bound is correct because every element of A ∩ C\_t is compatible with the chosen witness. In S2 an odd R-witness and odd C-elements remain. In S3 an even C-element of one class witnesses the other class.

All four bounds are nondecreasing in N. So S(N) = max S\_i at a block end E\_k bounds every N ∈ (E\_{k−1}, E\_k\]. The check is S(E\_k) ≤ c7(E\_{k−1} + 1).

With blocks of relative width 1%, this holds on all 794 blocks from 3806 to 10⁷. For example, F(10⁶) = 37,637 < c7 = 40,000, and F(10⁷) = 376,171 < 400,000. The counts H\_t(b, N) are computed exactly:

- primes p ≤ (bN)^{1/3} by stepping through the class a ≡ −b⁻¹ (mod p²);
- larger primes by enumerating ab + 1 = mp² over m, solving s² ≡ m⁻¹ (mod b) by CRT.

Together with Corollary 5.2, whose range starts at 6.7838·10⁶ < 10⁷, this proves Theorem A for every N.

## 7. Stability, rigidity and the extremisers

**Proof of Theorem B.** The first bound is Corollary 5.2. For the asymptotic bound, apply Theorem 4.1 with (z\_A, z\_B) = (41, 23), where V₂ ≤ 0.0292884. The argument of Proposition 5.1 gives E\_I(N) = o(N) for any fixed parameters. ∎

Theorem B implies a robust form. If N ≥ 6.7838·10⁶ and |A| > (N − 7)/25, then A ⊆ C7 or A ⊆ C18, so A is one full class with some elements removed. Nothing outside the class can be added. Sawhney's note gives this with an unspecified η. Here η can be taken to be 0.0016 at N = 10⁷, rising to about 0.0107 as N → ∞.

**Proof of Theorem C(1), upper bound.** Pick b ∈ A \\ C7. Then A ∩ C7 is contained in {a ∈ C7 : ab + 1 not squarefree}. By Lemma 2.2 the forced share s satisfies s ≤ 1/3. On the remaining types only primes p ≥ 7 contribute, and Lemmas 3.2, 3.3 and 3.5 bound them by (1 − s)β⁺N/25 plus an error. The bound s + (1 − s)β⁺ increases with s, so

```latex
|A\cap C_7| \le \tfrac1{25}\big(\tfrac13+\tfrac23\beta^{+}\big)N + 38\,(1+2^{k_B}) + 38 + E_B(N).
```

This holds for every N. Letting z\_B → ∞ gives the limsup bound g1\*. ∎

**Sharpness.** Let q be a prime with q ≡ 18 (mod 25), q ≡ 1 (mod 4) and q ≡ 1 (mod 9). Put A\_q(N) = {q} ∪ {a ∈ C7 ∩ \[N\] : aq + 1 not squarefree}. This set is valid:

- pairs inside C7 have 25 | ab + 1;
- the pair (q, q) has 25 | q² + 1;
- the pairs (a, q) are valid by definition.

The forced share is exactly 1/3, from a ≡ 3 (mod 4) or a ≡ 8 (mod 9). On the other cells, the events p² | aq + 1 for p ≥ 7, p ≠ q are independent of the cell by CRT. The squarefree sieve for a linear form gives density β(q) = 1 − ∏\_{p≥7, p≠q}(1 − p⁻²). So |A\_q(N)|/N → (1/3 + (2/3)β(q))/25, which tends to g1\* as q → ∞. ∎

**Relation to Li's proof.** Li's "uniform mixed degree" proposition says that for N ≥ 5·10⁶, every b ∈ V outside C7 ∪ C18 has more than N/50 + N/525 ≈ 0.0219N squarefree neighbours in C7 ∩ \[N\], and likewise in C18 ∩ \[N\]. Theorem C(1) is the sharp form of this. The squarefree degree is c7(N) − H₇(b), so the worst case is asymptotically (1/25 − g1\*)N ≈ 0.0253N, and no constant above 1/25 − g1\* is possible. Computing H₇ and H₁₈ exactly for every b ≤ 10⁷ confirms Li's proposition on all of 5·10⁶ ≤ N ≤ 10⁷, with a margin of at least 13.8%. Each 1% block is checked conservatively: the largest H at the top of the block, against the class size at the bottom and Li's threshold at the top. There max H₇(b)/N stays at 0.01468, matching g1\*.

**Proof of Theorem C(2).** A valid set inside C7 has at most c7(N) elements, with equality only for C7 ∩ \[N\]. The same holds for C18. So it suffices to compare c7(N) with m(N), the largest size of a valid set not inside one class. The function m is nondecreasing and c7 is constant on blocks.

1. **N ≤ 1006.** Compute m(N) exactly as a maximum over cliques that contain an R-vertex or meet both C7 and C18. Then m(N) < c7(N) except for 41 ≤ N ≤ 81, where m = c7. Enumerating all maximal cliques for 7 ≤ N ≤ 106 gives exactly the sets in the table below.
2. **1006 < N ≤ 3806.** The case bounds S1–S4 are strictly below c7 on every block.
3. **3806 < N ≤ 6.9·10⁶.** The case bounds are strictly below c7 on all 757 blocks. The smallest block margin is 1, on (4282, 4324\]. Checked one N at a time, the margin there is at least 2.
4. **N ≥ 6.7838·10⁶.** This is Theorem B.

| N | c7(N) | Extra maximisers |
| --- | --- | --- |
| 41–42 | 2 | {7, 41} |
| 43–56 | 2 | {7, 41}, {32, 43}, {41, 43} |
| 57–81 | 3 | {32, 43, 57} |

For instance, 32·43 + 1 = 3⁴·17, 32·57 + 1 = 5²·73 and 43·57 + 1 = 2²·613, and 25 divides 32² + 1, 43² + 1 and 57² + 1. ∎

**Proof of Theorem D.** If a, b ∈ F lie in the same class mod 25, then 25 | ab + 1. If a ≡ 7 and b ≡ 18 (mod 25), then a ≡ 1 and b ≡ 3 (mod 4), so ab + 1 ≡ 0 (mod 4). The case a = b is covered by the first case. F meets both classes, for example 57 ∈ C7 and 43 ∈ C18, and has density 2·(1/25)(1/4) = 1/50. Maximality among congruence-defined sets comes from an exact maximum-clique computation on the forcing graph mod 900. Its value is 1/50, attained by F up to symmetry. The upper bound for λ\* is Theorem 8.1. Validity of F, of C7 and C18, and of the four exceptional maximisers is checked in Lean 4 (`Erdos848Constructions.lean`). ∎

## 8. The second-best density

Let λ\*(N) be the largest size of a valid A ⊆ \[N\] contained neither in C7 nor in C18.

**Theorem 8.1.** For every N, λ\*(N) ≤ N/50 + E(N), where E(N) = N^{2/3+o(1)} is the explicit function of Section 8.5. In particular λ\*(N) ≤ N/50 + 75·N^0.81 for every N (Section 8.6). The set F of Theorem D gives λ\*(N) ≥ N/50 − 2. Hence λ\*(N)/N → 1/50.

Section 8.1 proves the theorem for sets inside C7 ∪ C18 by a short argument. Sections 8.2–8.4 prove the general case: a counting lemma, then an all-witness version of the game of Section 4, then an exact certificate. Section 8.5 makes every constant explicit.

### 8.1 Sets inside C7 ∪ C18

**Proposition 8.2.** Let A ⊆ \[N\] be valid, A ⊆ C7 ∪ C18, and suppose A meets both classes. Then |A| ≤ N/50 + O(N^0.81).

*Proof.* Put X = A ∩ C7 and Y = A ∩ C18, and let x, y be their sizes relative to N/25. For a ∈ X and b ∈ Y we have ab + 1 ≡ 7·18 + 1 ≡ 2 (mod 25). So ab + 1 is non-squarefree only if:

- (4) a and b are odd with ab ≡ 3 (mod 4), or
- (Q) 9 | ab + 1, or p² | ab + 1 for some prime p ≥ 7.

For fixed b, let Comp\_Q(b) be the set of a ∈ C7 ∩ \[N\] satisfying (Q). The condition 9 | ab + 1 picks out one class mod 9, and p² | ab + 1 one class mod p². Lemma 8.3 handles p > N^0.6. So Comp\_Q(b) has relative size at most

```latex
c = \frac19 + \sum_{p\ge 7}\frac1{p^2} = 0.16225\ldots < \frac16,
```

up to O(N^{0.8+o(1)}), and by CRT it meets each class mod 4 proportionally. Split X and Y by residue mod 4 into even, 1 and 3 parts. A pair not forced by 4 lies in Comp\_Q of its partner. A case analysis on which odd classes each side meets gives:

- one side has no odd element: x + y ≤ 2c;
- one side meets both odd classes: x + y ≤ max(2c, 1/4 + 3c/2);
- both sides meet the same single odd class: x + y ≤ 3c/2;
- they meet opposite single odd classes (the shape of F): x + y ≤ 1/2 if neither side has an even element, and otherwise x + y ≤ max(1/4 + 3c/2, 2c).

Since c < 1/6, every case gives x + y ≤ 1/2. ∎

### 8.2 Counting with an arbitrary target

**Lemma 8.3 (large primes, any target).** For 1 ≤ b ≤ N and Y ≥ 1,

```latex
\#\{a\le N : q^2\mid ab+1 \text{ for some prime } q>Y\} \le 2^{\omega(b)+1}\Big(\frac{2(N+1)}{Y}+\frac{N^2+1}{Y^2}\Big).
```

*Proof.* Write ab + 1 = mq². Then 1 ≤ m < (bN + 1)/Y², and ms² ≡ 1 (mod b) with s = q. So s is a square root of m⁻¹ mod b. There are at most 2^{ω(b)+1} of these: two for each odd prime power, at most four for a power of 2. Also s ≤ √((bN + 1)/m). So each m contributes at most 2^{ω(b)+1}(√((bN + 1)/m)/b + 1). Summing over m < M = (bN + 1)/Y², and using Σ m^{−1/2} ≤ 2√M, gives 2^{ω(b)+1}(2(bN + 1)/(bY) + M). This is at most the bound stated, since 1 ≤ b ≤ N. ∎

This is a cruder form of Lemma 3.5 that needs no information about the target. Since 2^{ω(b)} = N^{o(1)}, with Y = N^0.6 it is N^{0.8+o(1)}.

**Lemma 8.4 (joint estimate for R-targets).** Let t be a residue class mod 900 inside R, of density w\_t, and let b ≤ N be a witness that does not force t. Then

```latex
\#\{a\in t\cap[N] : a\in V,\ ab+1 \text{ not squarefree}\} \le w_t\, j^{+} N + O(N^{0.8+o(1)}),\qquad j^{+} = \alpha^{+}\beta_{500} + \kappa + \tau + \tau_B \le 0.01577,
```

where

- α⁺ = Σ 2/p² over primes p ≡ 1 (mod 4), p ≥ 13;
- β⁺ = Σ\_{q≥7} 1/q² = 0.051136 (in this section; it is at least the truncated β⁺ of Section 4), and β\_500 = Σ\_{7≤q≤500} 1/q² = 0.050863;
- κ = Σ 1/p² over primes p ≡ 1 (mod 4), p ≥ 13;
- τ = 2Σ 1/p² over primes p ≡ 1 (mod 4), p > 500, which is at most 0.00028; and τ\_B = Σ 1/q² over all primes q > 500, which is also at most 0.00028.

*Proof.* Membership a ∈ V needs p² | a² + 1 for some p ≡ 1 (mod 4), p ≥ 13 (Lemma 2.1). Because b does not force t, non-squarefreeness of ab + 1 needs q² | ab + 1 for some q ≥ 7. Split into three parts.

1. **p, q ≤ 500.** By CRT with mod 900, a pair p ≠ q fixes 2 classes mod 900p²q², contributing at most 2(w\_t N/(p²q²) + 1). A pair p = q needs a ≡ ±ι\_p and a ≡ −b⁻¹ (mod p²), at most one class, contributing w\_t N/p² + 1. Together these give at most w\_t(α⁺β\_500 + κ)N + O(1).
2. **p > 500.** Lemma 3.3 for 500 < p ≤ N^0.6 and Lemma 3.4 for p > N^0.6 give at most w\_t τ N + O(N^0.8 log N).
3. **q > 500.** Drop the condition on p. For 500 < q ≤ N^0.6 each prime fixes one class, contributing at most w\_t N/q² + 1, so these give at most w\_t τ\_B N + π(N^0.6). For q > N^0.6 use Lemma 8.3. ∎

For a C-type target that b does not force, the same argument without the condition a ∈ V gives at most w\_t β⁺ N + O(N^{0.8+o(1)}), with β⁺ ≤ 0.05114.

### 8.3 The all-witness game and its core

Use 525 types t: a mod 25, a mod 4 (even, 1 or 3), and a mod 9 with 3 | a merged. Let P be the set of types met by a valid A not inside one class, and choose a witness b\_s ∈ A of each type s ∈ P. Every a ∈ A ∩ t is compatible with every witness, so |A ∩ t| ≤ min over s ∈ P of the bound for witness b\_s. The possible bounds are:

- **Forced C-target:** w\_t N + O(1).
- **Non-forced C-target:** w\_t β⁺ N + O(N^{0.8+o(1)}).
- **R-target:** w\_t j⁺ N + O(N^{0.8+o(1)}). An R-type never forces itself: a² ≡ −1 has no solution mod 4 or mod 9, and mod 25 only in C7 or C18. So each R-type in P can use its own witness.

**Lemma 8.5 (core reduction).** Let K be the set of types in P forced by every type in P, and let F(K) be the set of types forcing every member of K. Then K consists of C-types, P ⊆ F(K), and

```latex
|A| \le \Big(w(K) + \beta\, w\big(\mathcal C\cap F(K)\setminus K\big) + j\, w\big(\mathcal R\cap F(K)\big)\Big)N + O(N^{0.8+o(1)}) =: U(K)\,N + O(N^{0.8+o(1)}),
```

for any β ≥ β⁺ and j ≥ j⁺. Here 𝒞 and ℛ are the C-types and the R-types.

*Proof.* Forcing is symmetric, so every s ∈ P forces every member of K, giving P ⊆ F(K). A non-core C-type in P is not forced by some s ∈ P, and an R-type in P uses its own witness. Sum the bounds above over t ∈ P. ∎

### 8.4 The certificate

A C-type is forced by a type outside its own class only through 4 or 9, never 25, since 7·18 + 1 ≡ 2 (mod 25) and 7r + 1 ≢ 0 for r ∈ R. So forcing between a core and the rest depends only on cells mod 36: 21 cells per class.

A core is a pair (M₇, M₁₈) of cell sets with every cross pair forced. Each half is automatically internally forced, by 25. U(K) is then a function of three sets of cells:

- the cells forced with all of M₁₈ (the C7 part of F(K));
- the cells forced with all of M₇ (the C18 part);
- the cells forced with all of M₇ ∪ M₁₈ (the R part, in each of the 23 classes of R).

**Proposition 8.6.** With β = 0.052 and j = 0.0169, U(K) ≤ 1/50 for every core K for which F(K) contains a type outside C7 and a type outside C18. Equality holds only for the core of F and its mirror image.

*Proof.* Write A(M) for the set of cells forced with every cell of M. The program `lamcert.c` enumerates all 51,223 such cores and evaluates 900·U in exact integer arithmetic.

A much smaller check suffices. Replacing M by its closure A(A(M)) does not change A(M), because A(A(A(M))) = A(M), and it does not lower U, because the closure contains M. So both halves of the core may be taken closed. Only 64 sets of cells have the form A(M), and they give 439 admissible pairs.

This reduced check is formalised in `LamCert.lean` and checked by the Lean kernel (`decide`, with no `native_decide`). The file also proves the closure argument, the equality case, and that the forcing relation on cells is exactly divisibility of ab + 1 by 4 or 9.

The check fails with β = 0.10 and j = 0.03, so it is not vacuous. The bound survives up to j = 0.01721 (with β = 0.052) or β = 0.0556 (with j = 0.0169). A floating-point MILP over all 2⁵²⁵ type sets, run independently, gives the same value 1/50 with a matching dual bound. ∎

**Proof of Theorem 8.1.** Since β⁺ ≤ 0.05114 < 0.052 and j⁺ ≤ 0.01577 < 0.0169, Lemma 8.5 and Proposition 8.6 give |A| ≤ N/50 + O(N^{0.8+o(1)}), taking Y = N^0.6. Section 8.5 chooses Y better and makes every term explicit. ∎

### 8.5 The explicit error term

Let r\_t be the number of residues mod 900 in the type t. These sum to 72 over the 42 C-types, and to 828 over the 483 R-types. Fix a cut-off Y for the primes q in ab + 1, and Y′ for the primes p in a² + 1. Going through the proofs of Lemmas 8.3–8.5, the error is at most the sum of these terms:

- **Core C-types:** |t ∩ \[N\]| ≤ w\_t N + r\_t, so 72 in total.
- **Other C-types, 7 ≤ q ≤ Y:** one class mod q² for each prime, so at most 72π(Y).
- **Other C-types, q > Y:** a non-forced C-target lies in T\_b, so Lemma 3.5 applies. This gives 42·L\_C, where L\_C is the bound of Lemma 3.5 with b ≤ N.
- **R-types, p, q ≤ 500:** 828(2n₁n₂ + n₁), where n₁ = 43 and n₂ = 92 count the primes in the two ranges.
- **R-types, 500 < q ≤ Y:** at most 828·π(Y), one residue error per prime q (the condition on p is dropped, as in Lemma 8.4).
- **R-types, q > Y:** 483·L, where L = 2^{ω\*(N)+1}(2(N+1)/Y + (N²+1)/Y²) comes from Lemma 8.3, and ω\*(N) is the largest number of distinct prime factors of an integer ≤ N.
- **R-types, 500 < p ≤ Y′:** at most 1656·π(Y′).
- **R-types, p > Y′:** the bound of Lemma 3.4, counted once for all of R, because the types are disjoint.

Let E(N) be the minimum of this sum over Y and Y′. The script `explicitC.py` evaluates E on cells of ratio 10^0.1 up to N = 10⁶⁰¹, refined to ratio 10^0.01 between 10¹⁰ and 10²⁵. It uses exact prime counts below 10⁷ and π(x) < 1.25506x/ln x above. For fixed Y and Y′ every term is nondecreasing in N, so each cell is checked at its upper end. Some values:

| N | 10⁷ | 10¹³ | 10²⁰ | 10³⁰ | 10⁶⁰ | 10¹⁰⁰ |
| --- | --- | --- | --- | --- | --- | --- |
| E(N)/N | 27 | 0.31 | 0.0030 | 2.4·10⁻⁶ | 4.1·10⁻¹⁵ | 1.1·10⁻²⁶ |

The best Y lies between about N^0.72 and N^0.85, and E(N) = N^{2/3+o(1)}. The bound beats the trivial bound |A| ≤ N from about N = 10^11.7.

So |A| ≤ N/50 + C·N^0.81 holds for every N, with C the largest value of min((49/50)N^0.19, E(N)/N^0.81). The grid gives C ≤ 167.5, attained near N = 10^11.75. Beyond 10⁶⁰¹, take Y = Y′ = N^{2/3} and use Robin's bound ω(n) ≤ 1.38402 ln n/ln ln n. This gives E(N) ≤ 1001·2^{ω\*(N)}N^{2/3}, so E(N)/N^0.81 is at most 4·10⁻⁴ and decreasing there. This gives C = 170. Section 8.6 lowers it to 75.

The constant is large because the witness may have many prime factors, and because the large-prime count is crude. The exponent 0.81 can be replaced by any number above 2/3, at the cost of a larger C.

### 8.6 Witnesses with many prime factors

The factor 2^{ω(b)} in Lemmas 3.5 and 8.3 is paid for the worst possible witness. As in the ω-refinement of Section 5, it can be avoided by setting aside the elements with many prime factors. Fix k ≥ 1, let A″ be the elements of A with at least k distinct prime factors, and let A′ = A \\ A″.

**Lemma 8.7 (Rankin).** For every z ≥ 1, #{n ≤ N : ω(n) ≥ k} ≤ z^{−k}·N·exp((z − 1)S(N)), where S(N) = Σ\_{p≤N} 1/p < log log N + B + 1/log² N and B = 0.26150… is the Meissel–Mertens constant.

*Proof.* Since z^{ω(n)} = Σ\_{d | n, d squarefree} (z − 1)^{ω(d)}, we get Σ\_{n≤N} z^{ω(n)} ≤ N·∏\_{p≤N}(1 + (z − 1)/p) ≤ N·exp((z − 1)S(N)). Divide by z^k. The bound on S(N) is Rosser and Schoenfeld's. ∎

For N ≤ 10¹⁸ a sharper bound comes from Hardy and Ramanujan's induction, run numerically. Write N\_j(x) = #{n ≤ x : ω(n) = j} and P(y) for the number of prime powers up to y.

**Lemma 8.8.** For x ≥ 1 and k ≥ 1,

```latex
N_{k+1}(x) \le \sum_{\substack{m\le\sqrt{x}\\ \omega(m)=k}} P(x/m) + \frac{1}{k+1}\sum_{\substack{q\le\sqrt{x}\\ q \text{ a prime power}}} N_k(x/q).
```

*Proof.* Let n ≤ x have k + 1 prime-power factors. If the largest of them, q, exceeds √x, then n = qm with m < √x and ω(m) = k, and this representation is unique. Otherwise each of the k + 1 prime-power factors q is at most √x, and n/q has k prime factors and is at most x/q, so n is counted k + 1 times in the second sum. ∎

The script `omega_envelope.py` starts from exact counts of N\_j at the points 10^{i/200} up to 10⁹ (`omgrid.c`), and uses P(y) ≤ π(y) + 2√y with Dusart's bound for π above that. It evaluates Lemma 8.8 on the same grid up to 10¹⁸, binning both sums and rounding every argument up to the next grid point. Since each N\_j is nondecreasing, this gives upper envelopes. As a check, the same computation started from exact counts at 10⁷ stays above the exact counts at every grid point up to 10⁹.

Write K\_k(N) for the smaller of the Rankin and envelope bounds on #{n ≤ N : ω(n) ≥ k}, with K\_k(N) = 0 when k > ω\*(N). There are two cases.

- **Case I: A′ is inside neither C7 nor C18.** Run the argument of Sections 8.2–8.4 on A′, choosing every witness in A′. Then ω(b) ≤ k − 1, so in Section 8.5 the factors 2^{ω\*(N)+1} and 2^{ω₁\*(N)} become 2^{k} and 2^{k−1}. Call the resulting error E\_k(N). Then |A| ≤ N/50 + E\_k(N) + K\_k(N).
- **Case II: A′ ⊆ C7, say.** Since A ⊄ C7, some b ∈ A″ lies outside C7, and A \\ C7 ⊆ A″. A single cell outside C7 forces at most 12 of the 36 residues of C7 mod 36: one row of weight 9 and one column of weight 4, which overlap in one cell. So, as in Lemma 2.2, |A ∩ C7| ≤ g₁N + E\_II(N). Here g₁ = (1/3 + (2/3)β⁺)/25 = 0.014697 < 1/50, and E\_II(N) = 36 + 36π(Y) + L\_C, where L\_C is Lemma 3.5's bound with the worst-case factor 2^{ω₁\*(N)}. Then |A| ≤ N/50 + E\_II(N) + K\_k(N) − (1/50 − g₁)N.

Taking k = ω\*(N) + 1 recovers Section 8.5. The script `explicitC_omega2.py` uses the grid of Section 8.5, refined to ratio 10^0.01 from 10⁵ to 10²⁵. For each cell it chooses k, Y and Y′ and checks both cases. It gives C ≤ 72.2, attained near N = 10^9.82 with k = 6. Hence C = 75 works in Theorem 8.1. Rankin's bound alone gives C ≤ 92.4 (`explicitC_omega.py`).

The envelope is still a few times the true count; started at 10⁷, it is 3–12 times too large at 10⁹ for the relevant k. The larger remaining gain would come from counting only the elements of V, which are the only elements a valid set can contain. Exact counts up to 10⁹ show that this makes the count about ten times smaller. Our estimate is that it would bring C to about 40, but it needs an explicit bound for integers with many prime factors in the classes ±ι\_p mod p².

## 9. Open problems

1. **Third-order structure.** Describe the valid sets of size close to N/50 that are not inside one class. Is F, with its mirror and finite modifications, the only one? Proposition 8.6 suggests yes, since only those cores attain 1/50.
2. **Sharper large-prime counts.** Brute force shows that Lemmas 3.4 and 3.5 overestimate by a factor of 40 or more (worst ratio 0.026). Averaging ρ\_b(m) over short ranges of m, using explicit Burgess- or Weil-type bounds, should lower N₀ substantially, make the ω-refinement unnecessary, and shrink the constant C of Theorem 8.1.
3. **A general witness-game theorem.** The method seems to apply whenever "f(a, b) has a square factor" admits a self-forcing residue class and the local game has a positive gap. A local survey suggests ab + 1 never cube-free (extremal class 57 or 68 mod 125) as the cleanest next case.
4. **Formalisation.** The constructions (`Erdos848Constructions.lean`) and the certificate of Proposition 8.6 (`LamCert.lean`) are verified in Lean. Natural next targets are Proposition 8.2, which is short, and the counting lemmas of Section 3.

## Appendix: verification and reproducibility

All code is plain C (gcc -O3, optionally -fopenmp) or Python 3 with numpy, sympy, networkx and scipy. Each computational claim has at least two independent checks.

| Claim | Primary computation | Independent check |
| --- | --- | --- |
| Theorem A, N ≤ 3806 | max clique at N ≡ 6 (mod 25), `e848b.py` (776 s) | `nsc.py exact cliques for N ≤ 1006, plus case bounds S1–S4 strictly below c7 for 1006 < N ≤ 3806 (fast848.c started at N = 31)` |
| Theorem A, 3806 ≤ N ≤ 10⁷ | `fast848.c`, 794 blocks (47 min) | `e848cases.c` (different algorithm) to 10⁶; numpy brute force `alledges.py`; `sbrute.py` (direct d² sieve) matches S1–S4 at all 168 edges ≤ 20,000 |
| V₂ values | MILP, `vk2.py` (HiGHS) | exact integer branch-and-bound, `bb.c`, all 16 parameter pairs |
| Lemma 3.5 constants λ, c | `mconst2.py` | `mc.py` (brute-force ρ) |
| Lemmas 3.4 and 3.5 | proofs above | brute force at N ≤ 3·10⁵, `brute.py` / `brute2.py`: no violations, worst ratio actual/bound 0.026 |
| Grid, N ≥ 6.7838·10⁶ | `tmgrid.py`, 2525 cells on \[10⁷, 10⁶⁰\]; the referee grid alone covers \[6.7838·10⁶, 10⁷\] | referee `cellsbig.py` / `cellsbig2.py`, (17, 13) only, to 10⁶⁰ |
| ω-counts K\_k(N) | `omegaV.c` | `kom.c` |
| Proposition 5.1 | closed form above | `tail60.py` |
| Theorem C(2), N ≤ 1006 | `nsc.py` (exact cliques by case) | maximal-clique enumeration for N ≤ 106 |
| Theorem C(2), 3806 < N ≤ 6.9·10⁶ | `fast848.c`, strict comparison (29 min, 2 cores) | `sbrute.py` on the tightest block, one N at a time |

Further independent checks:

| Claim | Computation | Result |
| --- | --- | --- |
| Li's uniform-degree proposition, 5·10⁶ ≤ N ≤ 10⁷ | `fastli.c` (exact H₇, H₁₈ for all b; 70 blocks of 1%, 56 min) | holds on every block; minimum margin 13.8% (threshold taken at the top of each block); brute-force cross-check at N = 20,000 |
| Theorem D and the constructions | `Erdos848Constructions.lean`, Lean 4.36.0-rc2 with Mathlib | compiles; no `sorry`; only the standard axioms |
| Densest congruence-defined set not inside one class | `wgame4.py` (exact cliques mod 900) | 1/50, attained by F; exact integer certificate of the full game: lamcert.c (51,223 cores); kernel-checked reduced certificate: LamCert.lean (64 closed sets, 439 pairs); explicit C = 75: explicitC\_omega2.py with omega\_envelope.py (C = 92.4 with Rankin's bound alone: explicitC\_omega.py; C = 170 without the ω-refinement: explicitC.py) |

The full package (code, logs and certificates) accompanies this paper.

## References

1. T. F. Bloom, [Erdős Problem #848](https://www.erdosproblems.com/848), erdosproblems.com, and the [discussion thread](https://www.erdosproblems.com/forum/thread/848).
2. M. Sawhney, [Problem 848](https://www.math.columbia.edu/~msawhney/Problem_848.pdf), note.
3. W. van Doorn, upper bound (0.108… + o(1))N, as recorded at reference 1.
4. J. B. Rosser and L. Schoenfeld, Approximate formulas for some functions of prime numbers, Illinois J. Math. 6 (1962), 64–94.
5. G. Robin, Estimation de la fonction de Tchebychef θ sur le k-ième nombre premier et grandes valeurs de la fonction ω(n) nombre de diviseurs premiers de n, Acta Arith. 42 (1983), no. 4, 367–389, doi:10.4064/aa-42-4-367-389.
6. P. Dusart, Inégalités explicites pour ψ(X), θ(X), π(X) et les nombres premiers, C. R. Math. Rep. Acad. Sci. Canada 21 (1999), no. 2, 53–59. This is the source of π(x) ≤ (x/ln x)(1 + 1/ln x + 2.51/ln² x) for x ≥ 355991.
7. B. Alexeev, D. G. Mixon and W. Sawin, [The independence and clique cover numbers of the squarefree graph](https://arxiv.org/abs/2507.01928) (2025), for the companion problem where ab is never squarefree.

8) A. C. Li, *The Exact Extremal Bound in Erdős Problem 848*, August 2026 ([SSRN 7230480](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7230480); [code and Lean](https://github.com/crabsatellite/erdos-848-squarefree-product)). Uses a Hall-matching reformulation relative to C7, a prefix colouring for N ≤ 5·10⁶, and case-wise pivot estimates beyond that. Claims a complete Lean 4 verification.
9) N. Sothanaphan, explicit threshold N₀ = 2.64·10¹⁷ for Sawhney's theorem (2026), as cited in reference 8.
10) I. Pitchford (with OpenAI Codex), [Candidate certificate-backed all-N determination for Erdős Problem 848](https://zenodo.org/records/21647629), Zenodo, July 2026.
11) B. Zanghi, [erdos-848](https://github.com/bzanghi/erdos-848), and N. Durfee, [erdos-848-verification](https://github.com/AstroCat93/erdos-848-verification), GitHub, 2026.

12. R. Jung et al., [erdos-banger](https://github.com/The-Obstacle-Is-The-Way/erdos-banger), Lean 4 formalisation of Sawhney's stability theorem for Problem 848 (η = 1/2000, ineffective N₀), January 2026.
13. M. Sawhney and M. Sellke, in *Early science acceleration experiments with GPT-5*, [arXiv:2511.16072](https://arxiv.org/abs/2511.16072), Section IV.1 (Problem 848).

## Acknowledgements

The argument, code and certificates were developed with AI assistance (Claude) and checked by independent re-implementation. Every computation above can be re-run from the accompanying package. We thank the contributors to the forum thread for Problem 848, especially W. van Doorn, D. Weisenberg, StijnC, B. Alexeev, M. Sawhney and N. Sothanaphan, whose comments shaped this work. We welcome expert review, especially of Sections 3–5 and 8.
