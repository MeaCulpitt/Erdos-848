# The witness game beyond Erdős Problem 848: higher powers, ab + c, and the third density

Luke Culpitt (AI assisted)

## Abstract

Erdős Problem 848 asks for the largest A ⊆ {1, …, N} with ab + 1 never squarefree. The answer is the class 7 mod 25. In a companion paper [M] we proved this for every N by a finite "witness game" on residue types. That paper also determined the second-best density, 1/50, attained by a two-class set F. Here we test how far the method reaches.

- **Higher powers.** For ab + 1 never k-free, the maximum is a class mod 5^k for every k ≥ 3 and all large N, with an explicit threshold. For 3 ≤ k ≤ 100 this holds for every N, with exactly two small exceptions, at k = 3 and k = 4. For cubes the maximisers are listed for every N.
- **Other forms.** For ab + c never squarefree, the maximum for large N is a root class of x² + c ≡ 0 (mod p²). This holds for 49 squarefree c ≤ 100, and for 33 of them the second-best density is also determined. The counting lemmas needed for general c are proved here.
- **The third density for 848.** The densest valid set not inside a class, F or F's mirror has density between 1/25 − 1/(4π²) = 0.014670 and 0.014910. The lower bound is one class plus one outsider, and we conjecture that it is sharp.

The computations use exact clique search and CP-SAT with rounded-up objective coefficients. All code is public.

## 1. Introduction

Call A ⊆ [N] *valid* if ab + 1 is not squarefree for all a, b ∈ A, including a = b. The class C7 = {n ≡ 7 (mod 25)} is valid, since 7² + 1 = 50. In [M] we proved that it is the largest valid set for every N, together with stability and rigidity results and the second-best density.

The method of [M] has three ingredients:

- a *self-forcing class*: a residue class in which ab + 1 is always divisible by a fixed square;
- a *positive local gap*: a finite game on residue types showing that any valid set not inside such a class is smaller by a constant factor;
- *control of large primes*: counting lemmas showing that squares p² with p large contribute o(N), uniformly in the witness.

This paper asks how special these are to x² + 1 and to squares. Section 2 proves the counting lemmas for ab + c with a general squarefree c ≥ 1. Section 3 uses them, with c = 1, to bracket the third density of 848. Section 4 treats higher powers, and Section 5 the forms ab + c.

We use the notation of [M] throughout. A *type* is a set of residue classes modulo a fixed modulus L. Type s *forces* type t if some fixed square divides ab + c for every a ∈ t and b ∈ s. A type is *self-forcing* if it forces itself. For a set A, P is the set of types it meets, its *core* K is the set of types in P forced by every type in P, and F(K) is the set of types forcing every member of K. Forcing is symmetric, so P ⊆ F(K).

## 2. Counting lemmas for ab + c

Fix a squarefree c ≥ 1 and a modulus L. The *layer primes* are the primes p whose squares are built into the types, through L = 36·∏ p² or similar. Every other prime q is a *luck prime*. For a luck prime q, the event q² | ab + c is not decided by the types and is counted directly.

**Lemma 2.1 (large luck primes).** Let 1 ≤ b ≤ N and Y ≥ c. Then

#{a ≤ N : q² | ab + c for some prime q > Y} ≤ c·2^{ω(b)+ω(c)+1}·(2(N + c)/Y + (N² + c)/Y²).

*Proof.* Let q > Y have q² | ab + c. Then q ∤ c, since q > c, and so q ∤ b. Write ab + c = mq², so that 1 ≤ m ≤ M = (bN + c)/Y² and mq² ≡ c (mod b).

Count the units s mod b with ms² ≡ c (mod b) prime power by prime power. Let ℓ^e ∥ b.

- If ℓ ∤ c, then ℓ ∤ m, and s² ≡ cm⁻¹ has at most 2 solutions mod ℓ^e (at most 4 if ℓ = 2).
- If ℓ | c, then ℓ ∥ c because c is squarefree, and ℓ | m. For e = 1 every unit works, which gives fewer than ℓ solutions. For e ≥ 2, write m = ℓm′ and c = ℓc′. Then m′s² ≡ c′ (mod ℓ^{e−1}) with c′ a unit, which has at most 4 solutions mod ℓ^{e−1}, so at most 4ℓ mod ℓ^e.

So q lies in at most c·2^{ω(b)+ω(c)+1} classes mod b. Since q ≤ √((bN + c)/m), each m contributes at most c·2^{ω(b)+ω(c)+1}(√((bN + c)/m)/b + 1). Summing over m ≤ M with Σ m^{−1/2} ≤ 2√M gives c·2^{ω(b)+ω(c)+1}(2(bN + c)/(bY) + M). This is at most the bound stated, since 1 ≤ b ≤ N. ∎

For c = 1 this is Lemma 8.3 of [M]. With Y = N^{0.6} it is N^{0.8+o(1)}, uniformly in b ≤ N, because 2^{ω(b)} = N^{o(1)}.

**Lemma 2.2 (one witness).** Let t be a type of density w_t and let b ≤ N. For each luck prime q, let d_q(t, b) be the relative density in t of the a with q² | ab + c. This density is determined by the classes of b mod L and mod q². Then, uniformly in b ≤ N,

#{a ∈ t ∩ [N] : q² | ab + c for some luck prime q} ≤ w_t·(1 − ∏_q (1 − d_q(t, b)))·N + o(N),

and also ≤ w_t·Σ_q d_q(t, b)·N + o(N).

The densities d_q(t, b) are as follows.

- For a luck prime q ∤ cL:
  - if q ∤ b, a must lie in the single class −cb⁻¹ mod q², so d_q = 1/q²;
  - if q | b, then ab + c ≡ c ≢ 0 (mod q), so d_q = 0.
- For a luck prime q | c, the type records whether q | a. Then q² | ab + c needs q to divide exactly one of a and b.
  - If q | b and q ∤ a, then a lies in one nonzero class mod q, so d_q = 1/(q − 1).
  - If q | a and q ∤ b, then a/q lies in one class mod q, so d_q = 1/q.
  - In the other two cases, d_q = 0.
- For a luck prime q whose root classes are recorded in the types (as in Sections 3 and 5):
  - if a lies in a root class R and b does not, then d_q = 0, because ab ≡ −c (mod q²) would put b in R;
  - if a lies in no root class, then −cb⁻¹ is one of the q² − 2 remaining classes, so d_q ≤ 1/(q² − 2).

*Proof.* Fix Q. For the luck primes q ≤ Q, the events are conditions on a modulo L·∏_{q≤Q} q². By the Chinese remainder theorem, the count is exact up to O(1) per class, where the implied constant depends on Q. This gives the product for q ≤ Q, and the union bound gives the sum.

For Q < q ≤ Y with Y = N^{0.6}, each q contributes at most N/q² + 1, or N/q + 1 when q | c; but q | c means q ≤ c ≤ Q once Q ≥ c. So these primes contribute at most N/Q + π(Y). For q > Y use Lemma 2.1. Letting Q → ∞ slowly with N, the total error is o(N), uniformly in b. ∎

**Lemma 2.3 (large primes in x² + c).** For every Q ≥ 1,

#{x ≤ N : p² | x² + c for some prime p > Q} ≤ (2/Q)·N + 2π(√(N² + c)) = (2/Q)·N + O(N/log N).

*Proof.* If p | c then p² ∤ x² + c: p | x would give p² | x², and c is squarefree. So p ∤ c, and x² ≡ −c (mod p²) has at most two roots. Each root class meets [N] in at most N/p² + 1 elements, and p ≤ √(N² + c). Sum over p > Q, using Σ_{p>Q} 1/p² ≤ 1/Q. ∎

For c = 1, [M] used Pell's equation to get a power saving here. For an asymptotic statement this cruder bound suffices, and it holds for every c.

**Lemma 2.4 (joint estimate with the own witness).** Let t be a type that is not self-forcing, and let b ∈ t. Write V_c = {x : x² + c not squarefree}, and ρ_p for the number of roots of x² ≡ −c (mod p²). Suppose t records, for each luck prime q | c, whether q | a. Then, uniformly in b ≤ N,

#{a ∈ t ∩ [N] : a ∈ V_c, ab + c not squarefree} ≤ w_t·(α_t·β⁰_t + κ_t)·N + o(N),

where

- α_t is the relative density in t of the a that have p² | a² + c for some luck prime p, bounded by the union bound Σ ρ_p/p² (a luck prime whose root classes are recorded contributes nothing here, since t is not self-forcing and so lies outside them);
- β⁰_t = Σ d_q(t, b) over luck primes q ∤ c;
- κ_t = Σ 1/p² over the luck primes p with ρ_p = 2.

*Proof.* Since t is not self-forcing and b ∈ t, the layer primes force nothing between a and b. So a ∈ V_c needs p² | a² + c for some luck prime p, and ab + c not squarefree needs q² | ab + c for some luck prime q.

A luck prime q | c contributes nothing. The elements a and b lie in the same type, so q divides both or neither. If q divides both, ab + c ≡ c (mod q²) and q ∥ c. If q divides neither, ab + c ≡ ab ≢ 0 (mod q).

Fix Q and consider p, q ≤ Q. For p ≠ q, the Chinese remainder theorem gives the product of the densities. For p = q, a must lie in a root class mod p² and in the class −cb⁻¹ mod p². The two root classes are distinct, so this leaves at most one class, and contributes 1/p². Up to the CRT errors, this gives w_t(α_t β⁰_t + κ_t)N.

For p > Q, drop the condition on q and use Lemma 2.3. For q > Q, drop the condition on p and use the tail of Lemma 2.2. Let Q → ∞. ∎

**Lemma 2.5 (core reduction).** Let A ⊆ [N] be c-valid, meaning ab + c is not squarefree for all a, b ∈ A. Let P be the set of types A meets, with core K. Suppose that for each type t there is a constant b_t with these properties:

- if t is self-forcing, b_t is at least the luck density of Lemma 2.2 for every witness that does not force t;
- otherwise, b_t is at least the constant of Lemma 2.4.

Then

|A| ≤ U(K)·N + o(N),  where U(K) = w(K) + Σ_{t ∈ F(K) ∖ K} b_t·w_t.

*Proof.* As in [M, Lemma 8.5]. Every element of A is compatible with every other. A self-forcing type t ∈ P ∖ K is not forced by some s ∈ P, so any element of A ∩ s is a witness for Lemma 2.2. A type that is not self-forcing uses an element of itself as the witness for Lemma 2.4. Core types count in full. Since P ⊆ F(K), summing over t ∈ P gives the bound. The number of types is fixed, so the o(N) terms add up to o(N). ∎

Maximising U(K) over the cores that a given family of sets can have is a finite problem. We solve it with CP-SAT [OR-tools], with every objective coefficient rounded up to a multiple of 10⁻⁹, so the reported optimum is an upper bound.

The variables are as follows. A *slab* is a residue class for the layers other than 4 and 9, together with the root-class memberships described below. A *cell* is a residue mod 36, together with the divisibility flags. Then K is given by a closed set of cells in each slab, and F(K) by its intersections, exactly as in [M, Section 8.4]. The code is `coregame.py`.

## 3. The third density of Problem 848

Let F = {7 mod 25, 1 mod 4} ∪ {18 mod 25, 3 mod 4} and let F′ be its mirror image. In [M] we showed that every valid set not inside C7 or C18 has at most N/50 + O(N^{0.81}) elements, and that F and F′ attain this. We also showed that for N ≥ 10^{23.6}, a valid set not inside a class with at least (1/50 − 0.0008)N elements lies in F or F′. Let λ₃(N) be the largest size of a valid A ⊆ [N] contained in none of C7, C18, F and F′.

**Theorem 3.1.**
1. lim inf λ₃(N)/N ≥ 1/25 − 1/(4π²) = 0.0146697….
2. lim sup λ₃(N)/N ≤ 0.014910.

So for all large N, a valid set with more than 0.01491N elements lies inside C7, C18, F or F′. This sharpens the density 1/50 − 0.0008 = 0.0192 of [M, Theorem 8.9] to 0.01491, though without an explicit threshold for N.

*Proof of (1).* Take a prime x > 3 with x ≡ 18 (mod 25) and x ≡ 3 (mod 4), and let

A = {x} ∪ {a ∈ C7 ∩ [N] : ax + 1 not squarefree}.

Pairs inside C7 are forced by 25. Also x² + 1 ≡ 0 (mod 25), and pairs with x hold by definition, so A is valid. It contains x ∈ C18 and elements of C7 that are ≡ 1 and ≡ 3 (mod 4), so it lies in none of the four sets.

For a ∈ C7 we have ax + 1 ≡ 2 (mod 25), so 25 never divides ax + 1. Among the a ∈ C7:

- 4 divides ax + 1 for one class of a mod 4;
- 9 divides it for one class mod 9;
- p² divides it for one class mod p², when p ≥ 7 and p ≠ x;
- x² never divides it.

So the a ∈ C7 with ax + 1 squarefree have density

(1/25)·(3/4)·(8/9)·∏_{p≥7, p≠x}(1 − p⁻²) = (1/(4π²))·(1 − x⁻²)⁻¹,

using ∏_{p≥7}(1 − p⁻²) = (6/π²)·(4/3)·(9/8)·(25/24) = 75/(8π²). Hence |A|/N → 1/25 − (1/(4π²))(1 − x⁻²)⁻¹ as N → ∞, and letting x → ∞ gives (1). The script `lam3_lower.py` checks the count: 0.014671 at N = 2·10⁷ with x = 100043. ∎

This is the "one class plus one outsider" configuration. The outsider forces exactly a third of C7, through 4 and 9 [M, Lemma 2.2]. The other two thirds survive only where ax + 1 picks up a square factor by chance. Its density is the sharp constant g₁* of [M, Theorem C(1)].

*Proof of (2).* Apply Lemma 2.5 with c = 1 and the following types:

- the class mod 25;
- the cell mod 36;
- membership in the classes S_p^± = {a ≡ ±ι_p (mod p²)} for p = 13 and 17, where ι_p² ≡ −1.

Two elements of the same S_p^σ are forced. An element of S_p^σ and one outside it never have p² | ab + 1, since ab ≡ −1 (mod p²) would put the second element in S_p^σ too. Inside the complement of S_p^±, the prime p acts as a luck prime with density 1/(p² − 2). So the luck primes are q ≥ 7, and the types outside C7 ∪ C18 ∪ S₁₃^± ∪ S₁₇^± are in V only through primes p ≥ 29.

The constants are as follows.

- For self-forcing types, b_t = 1 − ∏(1 − q⁻²), with the product over 7 ≤ q ≤ 10⁷ and the factor for p = 13, 17 replaced by 1 − 1/(p² − 2), plus Σ_{q>10⁷} q⁻². This is 0.0502.
- For the remaining types, b_t is the Lemma 2.4 constant, 0.0050. It was 0.0158 for the unrefined R-types of [M].

The admissible cores are those whose F(K) has a type outside each of C7, C18, F and F′. Maximising U over them is a problem on 225 slabs × 21 cells. `third_cp.py` solves it to optimality and finds 0.0149093. ∎

The optimal core is the class-plus-outsider core: twelve cells of one class, all forced by a single cell. So the game identifies the right configuration, and the gap of 0.00024 to the construction has two sources.

- Most of it comes from elements of the outsider's cell, in the other classes mod 25, that lie in V through primes p ≥ 29. This part shrinks as more classes S_p are split off: the bound is 0.0149645 with S₁₃ alone.
- The rest, β/900 ≈ 0.000056, is the outsider cell itself. The game charges it at rate β, although the construction has a single element there.

Closing the second part needs a bound for pairs of sets X, Y with xy + 1 never squarefree that is better than one witness on each side.

The unrefined enumeration of [M, Section 8.4] gives only 0.0186 here (`third.py`). In that version the R-types carry the full constant κ = Σ_{p≡1(4), p≥13} p⁻² = 0.0138 from the coincidence p = q, which the refinement removes.

**Conjecture 3.2.** λ₃(N)/N → 1/25 − 1/(4π²).

## 4. Higher powers

### 4.1 Cubes

Call A ⊆ [N] *cube-valid* if ab + 1 is not cube-free for all a, b ∈ A, including a = b. Write V₃ = {x : x² + 1 not cube-free}. Since 57² + 1 = 2·5³·13, the classes 57 and 68 mod 125 are cube-valid, playing the role of 7 and 18 mod 25. Write c57(N) = #{n ≤ N : n ≡ 57 (mod 125)}.

**Theorem 4.1.** For every N, every cube-valid A ⊆ [N] has |A| ≤ c57(N). Equality holds exactly in the following cases:

- A = C57 ∩ [N];
- A = C68 ∩ [N], when c68(N) = c57(N);
- for 193 ≤ N ≤ 306, also A = {182, 193};
- for 239 ≤ N ≤ 306, also A = {57, 239} and A = {193, 239}.

The exceptional sets work through 8 and 27: 182·193 + 1 = 3³·1301, 57·239 + 1 = 2³·13·131 and 193·239 + 1 = 2⁴·3·31². Locally the picture is the same as for 848. The densest congruence-defined cube-valid set not inside one class is {57 mod 125, 1 mod 8} ∪ {68 mod 125, 7 mod 8}, of density 1/500 (`wgame4.py`).

The proof is much shorter than for 848, for two reasons. The local gap is far larger, so a single witness suffices and the full game is not needed. And a cube q³ > N² + 1 can never divide ab + 1, so no lattice lemma is needed either.

**Lemma 4.2 (one witness).** Let A be cube-valid, and suppose some b ∈ A lies outside C57. Then

|A ∩ C57| ≤ (N/125)·(1/8 + 1/27 + β₃) + 2 + π((N² + 1)^{1/3}),  where β₃ = Σ_{q≥7} q⁻³ ≤ 0.004726,

and the same holds for C68.

*Proof.* Since b ∉ C57, 125 never divides ab + 1 for a ∈ C57. So some prime q ≠ 5 has q³ | ab + 1, which puts a in one class mod q³ (if q ∤ b). For q = 2 and q = 3 this is at most a fraction 1/8 or 1/27 of C57, at a cost of 1 each. For q ≥ 7, the class mod 125q³ contains at most N/(125q³) + 1 elements up to N. Also q³ ≤ ab + 1 ≤ N² + 1. ∎

*Proof of Theorem 4.1.* Let A be cube-valid and inside neither C57 nor C68. Then A has elements outside each class, so Lemma 4.2 applies to both. The remaining elements lie in V₃ outside C57 ∪ C68, so each has p³ | x² + 1 for some p ≡ 1 (mod 4) with p ≥ 13. There are at most 2Nσ₃ + 2π((N² + 1)^{1/3}) of them, where σ₃ = Σ p⁻³ over primes p ≡ 1 (mod 4) with p ≥ 13, so σ₃ ≤ 0.000756.

- **Large N.** The total main term is 0.004178N against c57(N) > (N − 57)/125 ≈ 0.008N. Checking cells of ratio 1.01 with exact prime counts to 10⁸ and Rosser–Schoenfeld above (`cube_analytic.py`) gives |A| < c57(N) for 1.94·10⁶ ≤ N ≤ 10⁴⁰. Beyond 10⁴⁰ the error term 4π((N² + 1)^{1/3}) + 4 is far below (0.008 − 0.004178)N.
- **700 ≤ N ≤ 2·10⁶.** Here `cubeM.c` computes the bound exactly. It finds the maximum over witnesses b ∈ V₃ ∖ C57 of #{a ∈ C57 ∩ [N] : ab + 1 not cube-free}, likewise for C68, and adds |V₃ ∩ [N]| − c57(N) − c68(N). All three are nondecreasing in N. On 20 cells of ratio 1.5, the bound at the top of each cell stays below c57 at the bottom of the cell. At its closest it reaches 89% of c57 (17 against 19 on [2362, 3543]). A brute-force recomputation by factorisation agrees at N = 3000.
- **N ≤ 700.** `cube_maxsets.py` lists all maximum cube-valid sets for every N by an exact clique search. An independent clique computation confirms the maximum c57(N) up to N = 40,000. ∎

For squares the large-prime events were the main difficulty. For cubes all three ingredients are easy.

### 4.2 General k

Call A ⊆ [N] *k-valid* if ab + 1 is never k-free, for all a, b ∈ A including a = b. Let q = 5^k, let r_k be the smaller root of x² ≡ −1 (mod q), and write c_k(N) = #{n ≤ N : n ≡ r_k (mod q)}. For example, r₃ = 57, r₄ = 182, r₅ = r₆ = 1068 and r₇ = 32318.

**Theorem 4.3.**
1. For every k ≥ 3 there is an explicit N_k such that for N ≥ N_k, every k-valid A ⊆ [N] not inside one of the classes ±r_k (mod q) has fewer than c_k(N) elements. So for N ≥ N_k the maximum is c_k(N), and only the full classes attain it. Here N_k/5^k is about 15,400 for k = 3, 555 for k = 4, at most 214 for k ≥ 5, and at most 60 for k ≥ 40.
2. For 3 ≤ k ≤ 100 the maximum is c_k(N) for every N, and only the full classes attain it, with exactly two exceptions. For k = 3 and 193 ≤ N ≤ 306, the mixed sets of Theorem 4.1 also attain it. For k = 4 and 239 ≤ N ≤ 806, the set {239} also attains the maximum 1, because 239² + 1 = 2·13⁴.

*Proof of part 1.* Lemma 4.2 holds with 2^k, 3^k and p^k in place of 8, 27 and p³. A witness outside C_{r_k} forces at most a fraction Z_k = 2^{−k} + 3^{−k} + Σ_{p≥7} p^{−k} of that class, plus one element for each prime p with p^k ≤ N² + 1. The rest of V_k has at most 2Nσ_k + 2π((N² + 1)^{1/k}) elements, where σ_k = Σ p^{−k} over primes p ≡ 1 (mod 4) with p ≥ 13. The main term 2Z_k + 2qσ_k is largest at k = 3, where it is 0.52, and it falls to 0.21 at k = 4 and 0.09 at k = 5.

For 3 ≤ k ≤ 40, `kfree_analytic.py` finds N_k by checking cells of ratio 1.01. For k > 40 and N = λq with λ ≥ 60, the requirement reduces to λ(1 − 10⁻¹¹) − 1 > 4π(25.01·λ^{0.05}) + 4. This holds because the right side is at most 52 for λ ≤ 10⁴, and grows only like λ^{0.05}. ∎

*Proof of part 2.* Below N_k the vertex set V_k ∩ [N_k] can be listed directly, as the roots of x² ≡ −1 (mod p^k) for the few primes with p^k ≤ N_k² + 1. Testing an edge only needs those same primes. The vertex set is small: 1,143 vertices for k = 4, 432 for k = 5, and between 90 and 155 for 9 ≤ k ≤ 100. Above k = 30 there are no vertices outside the two classes at all.

For 5 ≤ k ≤ 100, `kfree_exact.py` enumerates all maximum cliques at every vertex value up to N_k; the graph is constant between consecutive vertices. For k = 4 it does this up to 30,000 and then checks the one-witness bound on 14 cells up to N₄, where the bound is at most a third of c₄. The case k = 3 is Theorem 4.1.

The graphs are not trivial: for k = 5 there are 844 edges between the two classes and 5 extra vertices. An independent brute force, factorising x² + 1 and ab + 1 directly, reproduces every maximum set for k = 4 up to 3000 and k = 5 up to 20,000. ∎

So the extremal answer is the same for every k ≥ 3: the class r_k mod 5^k, with occasional small exceptions at the start. Part 2 cannot be checked for all k at once. Whether a stray vertex such as 239 falls below the second element of the class depends on the particular roots.

The exceptions are not confined to c_k(N) ≤ 1: for k = 3 they occur where c₃(N) = 2. But they do not recur. Let μ_k(N) be the size of the largest k-valid set in [N] not inside one class. For every 5 ≤ k ≤ 300 and every N ≤ N_k, μ_k(N) ≤ c_k(N) − 3. The closest approach is k = 5 and N = 13,568, where a mixed pair faces a class of 5 (`margin.py`). For 12 ≤ k ≤ 300 there is no mixed set at all below N_k: V_k ∩ [N_k] consists of the two classes, with no edge between them.

## 5. The forms ab + c

Fix a squarefree c ≥ 1, and call A ⊆ [N] *c-valid* if ab + c is not squarefree for all a, b ∈ A, including a = b. A *root class* is a class x mod p² with x² + c ≡ 0 (mod p²). It is self-forcing, because aa′ + c ≡ x² + c ≡ 0 for a, a′ in the class.

For p = 2, root classes exist exactly when c ≡ 3 (mod 4): they are 1 and 3 mod 4. For odd p ∤ c, they exist exactly when −c is a square mod p, and then there are two classes mod p². For p | c there are none. Let p_c be the least prime with root classes; for c = 1 it is 5. The root classes mod p_c² are the natural candidates for the maximum. They have density 1/4 if p_c = 2 and 1/p_c² otherwise.

**The game for c.** The types are built as follows.

- The layer primes are 2, 3 and P, where P = p_c if p_c ≥ 7 and P = 5 otherwise. A type records a mod 36 and a mod P².
- Every other prime is a luck prime. For each luck prime q | c, the type records whether q | a, as Lemmas 2.2 and 2.4 require.
- The type records membership in the root classes of the least luck prime p with ρ_p = 2, as in Section 3.

The constants b_t are those of Lemmas 2.2 and 2.4: union bounds over all luck primes, with the q | c terms at their worst case for self-forcing types. Lemma 2.5 then reduces the problem to a finite maximisation, which `game_gen.py` solves with CP-SAT in two steps.

1. It finds the maximum-weight cliques among the types. These are the largest congruence-defined c-valid sets.
2. It maximises U(K) over the cores whose F(K) is not inside any maximum clique. Call this maximum V_c.

**Theorem 5.1 (computer-assisted).** Let c ≤ 100 be squarefree with p_c ≤ 7 and c ∉ {10, 13}; there are 49 such c. Then:

1. The maximum cliques of the game are exactly the two root classes mod p_c² (mod 4 if p_c = 2).
2. V_c < 1/p_c² (V_c < 1/4 if p_c = 2).
3. For all sufficiently large N, the largest c-valid sets in [N] are the root classes mod p_c² of largest size, and only these.

*Proof.* Parts 1 and 2 are the computation. For part 3, let A be c-valid and not inside a root class mod p_c². Then the type set of A is not inside a maximum clique, so neither is F(K). By Lemma 2.5, |A| ≤ (V_c + o(1))N. Since V_c is strictly below the density of the root classes, this is smaller than the root classes once N is large. A c-valid set inside a root class has at most its size, with equality only for the full class. ∎

For 33 of these c, the best congruence-defined c-valid set not inside a root class has density exactly V_c. So V_c is the second-best density.

| max density | second-best density | c |
| --- | --- | --- |
| 1/4 (classes mod 4) | 1/9 | 3, 11, 23, 47, 51, 59, 71, 83, 87, 95 |
| 1/4 | 1/18 | 43, 67, 79 |
| 1/9 (classes mod 9) | 1/12 | 2, 14, 26, 38, 62, 74, 86 |
| 1/9 | 1/18 | 5, 17, 29, 41, 53, 65, 89 |
| 1/25 (classes mod 25) | 1/50 | 1 |
| 1/25 | 3/100 | 6, 34, 46 |
| 1/49 (classes mod 49) | 3/196 | 82 |
| 1/49 | 1/98 | 97 |

For the other 16 values of c (7, 15, 19, 21, 31, 33, 35, 39, 55, 61, 66, 69, 73, 77, 91, 94), the best congruence set and V_c still differ, so the second-best density is only bracketed (`gen_k1.jsonl`).

The refinements matter. Without the root-class split and the divisibility flags, the game fails for c = 34, 61, 66, 69 and 94: for c = 34 it gives V = 0.0427 against 1/25. Each of these has a luck prime dividing c, such as 17 | 34, or many small primes p with ρ_p = 2. With the refinements all five pass. With c = 1 the computation reproduces V = 1/50 of [M].

Exact clique computations (`brute_c.py`) agree with the root class for every N up to 400–800 for c = 2, 3, 6, 10, 13, 21 and 34.

Two groups of c ≤ 100 are left open.

- **c = 10 and 13.** The class is mod 49, and the game with one split prime falls just short: V₁₃ = 0.020465 against 1/49 = 0.020408. A second split prime should settle them, but it exceeds our computing budget.
- **The ten c ≤ 100 with p_c ≥ 11:** 22, 30, 37, 42, 57, 58, 70, 78, 85 and 93. The model has p_c² slabs, and we have not run it.

Theorem 5.1 gives no explicit threshold for N, since the o(N) terms of Section 2 are not made explicit.

## 6. Open problems

1. **The third density.** Prove Conjecture 3.2. This needs a two-sided bound for pairs X, Y with xy + 1 never squarefree that improves on one witness per side.
2. **All k.** Does Theorem 4.3(2) hold for every k? For large k, a mixed set below N_k needs 13^k or 17^k to divide x² + 1 or ab + 1 with x, a, b below about 60·5^k. Heuristically this happens for only finitely many k.
3. **All c.** Is the root class mod p_c² extremal for every squarefree c, including c = 10, 13 and those with p_c ≥ 11? Is there a proof that does not need a computation for each c? Non-squarefree c brings new self-forcing classes, such as 0 mod q when q² | c, and is not covered here.
4. **Effective thresholds** for Theorems 3.1 and 5.1.

## Appendix: reproducibility

All code is in the repository [R], in the folders `third_density/`, `cubefree/`, `kfree/` and `general_c/`. The CP-SAT computations use OR-tools 9.15.

| Claim | Computation | Result |
| --- | --- | --- |
| Theorem 3.1(1) | `lam3_lower.py`, exact count | 0.014671 at N = 2·10⁷ |
| Theorem 3.1(2) | `third_cp.py 13,17 product` | max U = 0.0149093, OPTIMAL; 0.0149645 with S₁₃ only; 0.0186 unrefined (`third.py`) |
| Theorem 4.1 | `cube_maxsets.py` (N ≤ 700), `cube_small.py` (to 40,000), `cubeM.c` (700 ≤ N ≤ 2·10⁶), `cube_analytic.py` (N ≥ 1.94·10⁶) | as stated |
| Theorem 4.3 | `kfree_analytic.py`, `kfree_exact.py`, `run_all.py`, `run_big.py`, `margin.py` | no exceptions for 5 ≤ k ≤ 100; margin at least 3 for 5 ≤ k ≤ 300 |
| Theorem 5.1 | `game_gen.py 1 c` for each c; output `gen_k1.jsonl` | V_c < 1/p_c² for 49 values; V_1 = 1/50 |
| Small-N checks for ab + c | `brute_c.py` | root class maximal for c = 2, 3, 6, 10, 13, 21, 34 up to N = 400–800 |

## References

[M] L. Culpitt, Stability, rigidity and exact extremisers for Erdős Problem 848, companion paper (2026).

[R] L. Culpitt, Erdos-848, https://github.com/MeaCulpitt/Erdos-848 (2026).

[B] T. F. Bloom, Erdős Problem #848, https://www.erdosproblems.com/848.

[OR-tools] L. Perron and F. Didier, CP-SAT, Google OR-Tools, https://developers.google.com/optimization.

[RS] J. B. Rosser and L. Schoenfeld, Approximate formulas for some functions of prime numbers, Illinois J. Math. 6 (1962), 64–94.

## Acknowledgements

The arguments and code were developed with AI assistance (Claude) and independently re-run. They have not yet been reviewed by a human expert.
