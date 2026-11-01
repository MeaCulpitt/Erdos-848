# Explicit large-prime counting for Erdős 848: lemmas, proofs, N0

Notation. V = {x : x²+1 not squarefree}. C7, C18 = classes 7, 18 mod 25, R = the other 23 classes.
For a witness b let b = b0·b1, with b0 the {2,3,5}-part. ω(b1) = number of distinct primes ≥ 7 dividing b.
"Type" = one of the 63 types of ../margins/typemat.c: (C7 | C18 | R) × (a even | a≡1 mod 4 | a≡3 mod 4) × (3|a | one of the 6 unit classes mod 9).
A "cell" is the mod-36 part of a type. Every type is (set S of residues mod 36) × (set of classes mod 25).

All constants below are computed by the scripts in this directory. Everything marked RIGOROUS is a
theorem (proof given). Everything marked HEURISTIC is not.

## Lemma 1 (discrepancy of type unions). RIGOROUS
Let U = S × {c} (S ⊆ Z/36, c a class mod 25), q ≥ 1 coprime to 30, and r a residue. Then
#{a ≤ N : a ≡ r (q), a ∈ U} = |S|·N/(900q) + θ·19, with |θ| ≤ 1.
For U = S × R25 the error is ≤ 57. For U = all of R (S = Z/36) it is ≤ 3. For C7 ∪ C18 (no mod-36 condition) it is ≤ 2.

Proof. Put a = a0 + 25q·i, i = 0..I, where a0 is the least solution of a ≡ r (q), a ≡ c (25). Then I+1 ≤ N/(25q)+1.
Because 25q is a unit mod 36, a ∈ S (mod 36) holds exactly when i lies in a set S' of the same size mod 36. For
J = I+1 the count #{0 ≤ i < J : i mod 36 ∈ S'} differs from J|S|/36 by at most min(|S|, 36−|S|) ≤ 18.
Using J ≤ N/(25q)+1 adds at most |S|/36 ≤ 1. So the error is ≤ 19.
S × R25 = S×Z25 − S×{7} − S×{18}. The first term is a mod-36 condition with error ≤ 19 (the same argument with
step q), so the total is ≤ 3·19 = 57. For all of R there are three single-class counts, each with error ≤ 1. ∎

## Lemma 1' (small primes by inclusion–exclusion). RIGOROUS
Let U have Lemma-1 constant e, and let P be a finite set of primes p ∤ 30b. Let R_p be a set of r_p residues mod p².
Then #{a ≤ N, a ∈ U : a mod p² ∈ R_p for some p ∈ P} = w_U·N·(1 − Π(1 − r_p/p²)) + θ·e·(1 + Π(1 + r_p)).
Proof. Complement, then Möbius over subsets T ⊆ P. Each term is a union of Π_{T} r_p classes mod Π_T p².
Lemma 1 applies to each class, so each term carries error e. ∎
Used with: B-events (p² | ab+1, r_p = 1, p ∈ [7, zB], p ∤ b) on the C-targets served by one witness (e = 38).
Used with: A-events (p² | a²+1, r_p = 2, p ≡ 1 mod 4, p ∈ [13, zA]) on the R-types of P (e = 57).
If p | b the B-event is empty and can be dropped, so the worst case is b coprime to all p ≤ zB.

## Lemma 2 (medium primes). RIGOROUS
Fix a prime p > z (p ∤ b for B). The number of a ≤ N in U with p² | ab+1 (one class mod p²) exceeds the main term
w_U·N/p² by at most min(e_U, 2N/(25p²)+2, N/p²+1), and by at most 1 if p² > N. For A (two classes ±ι_p mod p², U = R)
the excess is at most min(6, 2(N/p²+1)), and at most 1 if p² > 2N.
Proof. The first option is Lemma 1. The second option counts over the two classes mod 25 without using U.
The third ignores U altogether. All main terms are ≥ 0, so each option bounds the excess. A class mod p² > N meets
[1,N] at most once. ι + (p² − ι) = p², so if p² > 2N at most one of the two roots is ≤ N. ∎

## Lemma 3 (Pell, large primes for x²+1). RIGOROUS
#{x ≤ N : p² | x²+1 for some prime p > Y} ≤ Σ_{j ≥ 1} #{2 ≤ m ≤ min(M, m_j) : m admissible}.
Here M = (N²+1)/Y² and m_j = ((T_j + 1/T_j)/2)² with T_j = (2N+1)^{1/(2j−1)}.
Admissible means: m mod 8 ∈ {1,2,5}, 25 ∤ m, and no prime q ∈ {3,7,11,19,23} divides m.
Proof. Write x²+1 = m p², so m < M. Then m ≥ 2, because x²+1 = p² has no solution with x ≥ 1. Also m is not a
square, because x² − (kp)² = −1 is impossible. Every prime q ≡ 3 (mod 4) has q ∤ x²+1. We have x²+1 ≡ 1, 2, 5 (mod 8)
and p² ≡ 1 (mod 8), and 25 ∤ x²+1 for x ∈ R. The positive solutions of X² − mY² = −1 are η^{2j−1}, where η is the
fundamental unit of Z[√m], which has norm −1. From X ≥ 1, Y ≥ 1 and mY² = X²+1 we get η ≥ √(m−1)+√m.
Also η^{2j−1} = X + √(X²+1) ≤ 2N+1. So the j-th solution exists with X ≤ N only if √(m−1)+√m ≤ T_j, that is m ≤ m_j.
The map x ↦ (m, j) is injective. The admissible counts are exact, from a periodic table mod 8·25·3·7·11·19·23. ∎

## Lemma 4 (lattice count for p > Y, witness b). RIGOROUS
Let T_b be the C7∪C18 classes a with 4∤ab+1, 9∤ab+1, 25∤ab+1. Then
#{a ≤ N, a ∈ T_b : p² | ab+1 for a prime p > Y} ≤ 2^{ω(b1)}·[ 2λ(N+1)/Y + c·√(bN+1)/b + λ(bN+1)/Y² + c ].
The constants (λ, c) depend only on the {2,3,5}-profile of b (mconst.json). The worst profile has λ = 0.5333, c ≤ 18.94.
Proof. Write ab+1 = m s² with s = p > Y prime and m < M := (bN+1)/Y². Reducing mod 1800, m lies in
S_b = {(ab+1)·u : a ∈ T_b, u an inverse unit square mod 1800}. Also m s² ≡ 1 (mod b), so s lies in one of
ρ_b(m) = ρ_{b0}(m)·ρ_{b1}(m) classes mod b, with ρ_{b1}(m) ≤ 2^{ω(b1)}. Each prime-power factor of b1 has at most two
square roots. Hence the count for a given m is ≤ ρ_b(m)·(S(m)/b + 1), where S(m) = √((bN+1)/m).
Let g(m) = ρ_{b0}(m)·1[m ∈ S_b]. This g is 1800-periodic, and we computed it exactly. Its partial sums satisfy
G(x) ≤ λx + c. By partial summation Σ_{m≤M} g(m)/√m ≤ 2λ√M + c. Insert this and use b ≥ 1 in the first term. ∎
This bound is taken as a max over all b ≤ N, with ω(b1) = k forcing b ≥ b0·(7·11·…·p_k). Y may depend on b.
For the old (Sawhney) system, T_b = C7∪C18 minus 25 | ab+1, and λ = 0.4 for even b.

## Lemma 5 (forced share). RIGOROUS
If b ∉ C7, the C7-types forced by b (by 4 or by 9; 25 is impossible) make up at most 1/3 of C7. The bound is
1 − (3/4)(8/9) = 1/3.

## Lemma 6 (ω-refinement, using the freedom in choosing b). RIGOROUS
Let K_k(N) = #{b ≤ N : b ∈ V, ω(b1) ≥ k}. This is computed exactly by omegaV.c (for example K_5(10^7) = 672 and
K_5(10^8) = 28841). Split A = A' ⊔ A'', where A'' = {b : ω(b1) ≥ k0}, so |A''| ≤ K_{k0}(N).
- Case I. A' is not inside the C7-types and not inside the C18-types. Apply the type-matrix bound to A' with witnesses
  drawn from A' only, all of which have ω(b1) ≤ k0−1. Then |A| ≤ |A'| + K.
- Case II. A' lies inside C7 (or C18), possibly empty, and A ⊄ C7. Take any b ∈ A \ C7 (so b ∈ A''). Then
  |A ∩ C7| ≤ (1/25)(1/3 + (2/3)β⁺)N + errors(b, any ω), and |A \ C7| ≤ K.
∎

## Theorem T (type-matrix system). RIGOROUS (the V_2 value is certified by ../referee/bb.c, see below)
For every A ⊆ [1,N] with ab+1 non-squarefree for all a,b ∈ A, and A not inside one class 7 or 18 mod 25:
|A| ≤ max( G·N + E_I(N), g1·N + E_II(N) ).
- G = V_2(α_s, tail_A, β⁺) = (2/25)β⁺ + (23/25)α⁺. This is the vk2.py MILP. Its worst P is all 63 types, with two
  witnesses. Example: G = 0.029406 at (zA,zB) = (17,13).
- β⁺ = 1 − Π_{7≤p≤zB}(1−1/p²) + Σ_{p>zB} 1/p².
- α⁺ = 1 − Π_{13≤p≤zA, p≡1(4)}(1−2/p²) + 2Σ_{p>zA, p≡1(4)} 1/p². The tails are rigorous: exact sums to 10^7, plus
  2.51/(x ln x) beyond.
- R-types are bounded only through V. Their primes > zA are counted over all of R, with a constant (23/25)·tail_A
  whenever P meets R. The MILP shows this does not change V_2.
- E_I = 2·38(1+2^{kB}) + 38 + 57(1+3^{kA}) + E_A + 2·E_B(ω ≤ k0−1) + K_{k0}(N).
- E_II = 38(1+2^{kB}) + 38 + E_B(all ω) + K_{k0}(N).
- g1 = (1/3 + (2/3)β⁺)/25 ≈ 0.01468.
- E_A = min_Y [Lemma 2 sum over zA < p ≤ Y + Lemma 3].
- E_B = max over b of min_Y [Lemma 2 sum over zB < p ≤ Y + Lemma 4].
Proof. This is the type-matrix argument: |A∩t| ≤ H_t(b_s) for each t ∈ P and its assigned witness s ∈ W.
Sum the counts over the union of targets that share a witness. Then apply Lemmas 1–6. ∎

## Old (Sawhney) system: E(N) for one or two witness counts H over C7∪C18 plus vR
E = 3(1+3^{kA}) + nw·2(1+2^{kB+2}) + E_A + nw·E_B(old). Here the primes 2 and 3 are included in the inclusion–exclusion.
δ is the margin against the main density computed with the SAME truncations (zA = 17, zB = 23). Those truncated upper
densities exceed the exact Euler products by less than 10^{-4}.

## Proposition A (tail N ≥ 10^60). RIGOROUS
Claim: for all N ≥ 10^60, Theorem T holds with (zA, zB) = (17, 13), no ω-refinement (K = 0), and
Y = N^{2/3} on both sides. That is, E_I(N) ≤ δN − 0.28 with δ = 0.04 − 0.0294059212 = 0.0105940788.
Case II follows as well, because E_II ≤ E_I and 0.04 − g1 ≥ 0.0253 > δ.

Throughout, L = ln N ≥ 138.155, and the cited facts are:
- (RS) Rosser–Schoenfeld 1962, eq. (3.6): π(x) < 1.25506·x/ln x for all x > 1.
- (Ro) Robin 1983: ω(n) ≤ 1.38402·ln n/ln ln n for all n ≥ 3.
The function f(x) = ln x/ln ln x is increasing for x > e^e.

Bounds on each term:
(a) Inclusion–exclusion: kB = 3 (the primes 7, 11, 13) and kA = 2 (13, 17). So 2·38·(1+2³) + 38 + 57·(1+3²) = 1292.
(b) Lemma 2, A side: the excess is ≤ 6 for each p ≤ √(2N) and ≤ 1 for each p ∈ (√(2N), Y]. So it is
    ≤ 6π(√(2N)) + π(N^{2/3}). By (RS) this is ≤ 21.3·√N/L + 1.883·N^{2/3}/L.
(c) Lemma 3: m < M = (N²+1)/N^{4/3} ≤ (1+10^{-4})·N^{2/3}, so there are at most M values of m. For m ≥ 2,
    η ≥ √(m−1)+√m ≥ 1+√2, and η^{2j−1} ≤ 2N+1. So the number of j is ≤ J := (1 + ln(2N+1)/ln(1+√2))/2.
    The Pell term is ≤ M·J ≤ 0.581·N^{2/3}·L.
(d) Lemma 2, B side: the excess is ≤ 38 for each p ≤ √N and ≤ 1 for each p ∈ (√N, Y]. So it is
    ≤ 38π(√N) + π(N^{2/3}) ≤ 95.4·√N/L + 1.883·N^{2/3}/L by (RS).
(e) Lemma 4, where k = ω(b1): we have λ ≤ 0.5334 and c ≤ 18.94 (mconst.json; asserted in tail60.py), and b ≥ 7.
    Hence √(bN+1)/b ≤ √N. The bracket is then ≤ 1.0668(N+1)N^{-2/3} + 18.94√N + 1.0668(1+10^{-4})N^{2/3} + 18.94,
    which is ≤ 1.067·N^{2/3} + 20√N.
    Bounding 2^k: if k ≥ 2, then P_k ≥ 77 > e^e and P_k ≤ N. By (Ro) and the monotonicity of f,
    k = ω(P_k) ≤ 1.38402·f(N). So 2^k ≤ N^{0.95933/ln L} ≤ N^{0.19466}. If k ≤ 1, then 2^k ≤ 2.
    The lattice term is therefore ≤ N^{0.95933/ln L}·(1.067·N^{2/3} + 20√N).

E_I ≤ (a) + (b) + (c) + 2[(d) + (e)].

Monotonicity: each summand divided by N has the form C·N^{−a}·L^{b} with a ≥ 1/6 and b ∈ {−1, 0, 1}. It is
decreasing once L > b/a, and that holds here. The exception is the lattice term, whose exponent
0.95933/ln L + 2/3 − 1 (or + 1/2 − 1) is negative and decreasing in N. Also 0.28/N is decreasing.
So it suffices to check E_I(10^60)/N + 0.28/10^60 ≤ δ.
tail60.py evaluates this: E_I(10^60)/N ≤ 1.02·10^{-8}, which is less than δ = 0.0106. ∎

## V_2 certificate
V_2 ≤ 0.0294059212 at (17,13). This is certified by an exact integer branch-and-bound
(../referee/bb.c, independent referee). vk2.py (HiGHS) gives the same value for all 16 (zA,zB) pairs.

## Certified ranges (Theorem T, type-matrix system)
- [6.7838e6, 1e7]: `n0lemma.py tm` run (N0 = 6.7838e6), independently re-certified by the referee (worst cell slack +329).
- [1e7, 1e60]: every cell logged by tmgrid.py in tmgrid.log; the last line gives CELLS, FAILURES and MIN_SLACK.
- [1e60, ∞): Proposition A.
- [1, 1e7]: computation (../margins).

## N0 table, old (Sawhney) system (`n0lemma.py old-table`, grid 1e4..1e60; RIGOROUS given the margin δ)
| δ | 1 witness (S1, b even) | 2 witnesses (any b) |
|---|---|---|
| 0.0016 | 5.96e8 | 1.10e10 |
| 0.0024 | 1.20e8 | 1.97e9 |
| 0.005  | 1.74e7 | 2.69e8 |
| 0.01   | 1.95e6 | 2.44e7 |
| 0.015  | 7.43e5 | 8.51e6 |
| 0.02   | 2.89e5 | (not run) |
Type-matrix system without the ω-refinement: N0 is between 1.5e7 and 2e7 (sampled slack −5.0e3 at 1.5e7, +1.65e4 at 2e7;
the full grid run was stopped to stay on one core).

## What is heuristic / loose
- The 0.0171 type-matrix figure (R targets using witnesses) needs a joint (x²+1, ab+1) large-prime bound. It is not
  covered here. With union-bound tails it gives no gain.
- Brute-force checks at N = 2·10^4 (sanity.py) show Lemmas 3 and 4 overestimate by about 100× or more. The 2^{ω(b1)}
  factor and the "+1 per prime" in (√N, Y] dominate. Averaging ρ_b(m) over short m-ranges, M < b, would need
  Burgess/Weil-type explicit bounds and was not done.
