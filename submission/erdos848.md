---
title: |
  Stability, rigidity and exact extremisers for Erd\H{o}s Problem 848
author: Luke Culpitt (AI assisted)
date: November 2026
---

## Abstract

Erdős and Sárközy asked whether the largest $A \subseteq \{1, \dots, N\}$ with $ab + 1$ never squarefree is the residue class $7 \bmod 25$. Sawhney proved this for large $N$, and recent computer-assisted work, notably Li's Lean-verified proof, extends it to every $N$. We give an independent proof for every $N$ by a different method, with explicit threshold $N_0 = 6.7838\cdot 10^{6}$. It rests on a finite "witness game" on 63 residue types modulo $900$, whose value $0.0294059\dots$ is certified by exact integer branch-and-bound.

Our main new results describe valid sets beyond the maximum:

- **Explicit stability.** For $N \ge 6.7838\cdot 10^{6}$, every valid set not inside one class has at most $(N - 7)/25$ elements, and at most $0.0293N$ asymptotically. This makes Sawhney's qualitative $\eta$ explicit: $\eta = 0.0016$ at $N = 10^{7}$, rising to about $0.0107$ as $N \to \infty$.
- **Sharp rigidity.** One element outside $7 \bmod 25$ leaves at most a fraction $0.3667\dots$ of that class. This is the sharp form of the degree estimate in Li's proof.
- **Exact maximisers for every N.** They are the classes $7$ and $18 \bmod 25$, plus four small sets not inside one class when $41 \le N \le 81$.
- **A two-class set of density $1/50$.** It meets both classes, it beats the natural "one class plus one outsider" configuration, and it is optimal. Every valid set not inside one class has at most $N/50 + O(N^{0.81})$ elements, so the second-best density is exactly $1/50$. Near that density $F$ is rigid: for large $N$, a valid set not inside one class with at least $(1/50 - 0.0008)N$ elements lies inside $F$ or its mirror. A companion paper extends the method to $ab + 1$ never $k$-free, to $ab + c$ never squarefree, and to the third density (Section 9).

The constructions and the certificate for the second-best density are verified in Lean 4. Every computation is reproducible and was cross-checked by an independent implementation. This includes a check of the key degree proposition of Li's proof for $5\cdot 10^{6} \le N \le 10^{7}$.

## 1. Introduction

Call $A \subseteq [N] = \{1, \dots, N\}$ **valid** if $ab + 1$ is not squarefree for all $a, b \in A$, including $a = b$. Erdős and Sárközy asked whether the maximum of $|A|$ over valid sets is attained by $\{n \le N : n \equiv 7 \pmod{25}\}$ ([Erdős Problem #848](https://www.erdosproblems.com/848)). This class is valid because $7^2 + 1 = 50$, so $25 \mid ab + 1$ whenever $a \equiv b \equiv 7 \pmod{25}$. The class $18 \equiv -7$ works for the same reason.

Van Doorn gave $|A| \le (0.108\dots + o(1))N$, and Weisenberg improved the constant to about $0.105$ by inclusion–exclusion. Early computations posted by StijnC already pointed to stability, and found small valid sets avoiding both classes, such as $\{41, 70, 239, 437\}$ at $N = 606$. Sawhney ([note](https://www.math.columbia.edu/~msawhney/Problem_848.pdf)) proved the conjecture for $N \ge N_0$, with $N_0$ not computed, and noted a qualitative stability property. Sawhney and Sellke discuss the problem in Section IV.1 of arXiv:2511.16072, and Alexeev, Mixon and Sawin treat the companion problem where $ab$ is never squarefree (arXiv:2507.01928). As Alexeev pointed out, Erdős's original question has no restriction to large $N$. Later AI-assisted work on the forum, led by Sothanaphan, made $N_0$ explicit, reaching $\exp(1420)$ ([forum](https://www.erdosproblems.com/forum/thread/848)). That is far beyond the range of computation.

Since mid-2026 several unrefereed, AI-assisted all-N claims have appeared. Sothanaphan reached $N_0 = 2.64\cdot 10^{17}$, and full claims came from Pitchford with Codex ([Zenodo](https://zenodo.org/records/21647629)), A. C. Li (SSRN, with Lean; analytic range reportedly from $5\cdot 10^{6}$), Zanghi ([GitHub](https://github.com/bzanghi/erdos-848), $N_0 = 5\cdot 10^{8}$) and Durfee ([GitHub](https://github.com/AstroCat93/erdos-848-verification), $N_0 = 4.2\cdot 10^{7}$). All of these follow Sawhney's case split, and most cover small $N$ with colouring certificates. The argument here is independent of them. Its new ingredients are the type-matrix witness game, which gives $N_0 = 6.78\cdot 10^{6}$, and Theorems B and C, which none of those claims state.

Write $c_7(N) = \#\{n \le N : n \equiv 7 \pmod{25}\} = \lfloor (N - 7)/25\rfloor + 1$, and $C_7$, $C_{18}$ for the classes $7$ and $18 \bmod 25$.

**Theorem A (Li; independent proof here).** For every $N \ge 1$, every valid $A \subseteq [N]$ has $|A| \le c_7(N)$.

**Theorem B (stability).** Let $N \ge 6.7838\cdot 10^{6}$. If $A \subseteq [N]$ is valid and not contained in $C_7$ or $C_{18}$, then $|A| \le (N - 7)/25 < c_7(N)$. Moreover $|A| \le (0.029289 + o(1))N$. Equivalently, every valid set with more than about $0.0293N$ elements lies in one class.

**Theorem C (rigidity and extremisers).**

1. If $A$ is valid and $A \not\subseteq C_7$, then $|A \cap C_7| \le (g_1^* + o(1))N$, where $g_1^* = (1/3 + 2/3\cdot \beta_\infty)/25 = 0.0146697\dots$ and $\beta_\infty = 1 - \prod_{p\ge 7}(1 - p^{-2})$. This constant is sharp.
2. For $N \notin [41, 81]$, the maximisers in Theorem A are exactly $C_7 \cap [N]$, together with $C_{18} \cap [N]$ when $c_{18}(N) = c_7(N)$. For $41 \le N \le 81$ there are also the maximisers $\{7, 41\}$, $\{32, 43\}$, $\{41, 43\}$ and $\{32, 43, 57\}$, each in its own range of $N$.

**Theorem D (a dense two-class set).** The set $F = \{n \equiv 7 \pmod{25},\ n \equiv 1 \pmod{4}\} \cup \{n \equiv 18 \pmod{25},\ n \equiv 3 \pmod{4}\}$ is valid. It has density $1/50$ and meets both classes. Among sets defined by congruences mod $900$, it is the densest valid set not inside one class. Moreover $F$ is optimal: every valid $A \subseteq [N]$ not inside $C_7$ or $C_{18}$ has $|A| \le N/50 + 30\cdot N^{0.81}$, so the second-best density $\lambda^*$ equals $1/50$ (Section 8). For $N \ge 10^{23.6}$, every valid set not inside one class with at least $(1/50 - 0.0008)N$ elements lies inside $F$ or its mirror (Theorem 8.9).

Theorems B, C and D are new. Sawhney's note gives stability with an unspecified $\eta$ and leaves open whether $18 \bmod 25$ also attains the maximum. Li's proof of Theorem A, and the other all-N claims, give no stability constant and no description of the maximisers. The Lean formalisation in erdos-banger proves stability with $\eta = 1/2000$ beyond an ineffective $N_0$.

**Method.** Each $a$ lies in one of 63 *types*, given by its class mod $25$ ($C_7$, $C_{18}$ or the rest $R$), mod $4$ and mod $9$. Whether $p^2 \mid ab + 1$ is forced for $p \in \{2, 3, 5\}$ depends only on the types of $a$ and $b$. Fix a valid $A$ and pick one or two "witnesses" $b \in A$. Every other $a \in A$ must make $ab + 1$ non-squarefree. Optimising the witness choice against every possible set of types gives a finite min–max problem with value $V_2 = 0.0294059\dots < 1/25$.

Sections 3–5 bound the error terms explicitly, giving Theorem A for $N \ge 6.7838\cdot 10^{6}$. Section 6 covers smaller $N$ by one computation, which also gives the exact maximisers. Section 7 proves Theorems B and C and the first part of Theorem D, and Section 8 proves that $F$ is optimal and, near $1/50$, essentially unique. Section 9 summarises further results from a companion paper, and Section 10 lists open problems.

The arguments and code were developed with AI assistance and independently re-run (Appendix). They have not yet been reviewed by a human expert.

## 2. Local structure

Let $V = \{x \ge 1 : x^2 + 1 \text{ is not squarefree}\}$. Taking $a = b$ shows that every valid set lies in $V$.

**Lemma 2.1.** $x \in V$ if and only if $p^2 \mid x^2 + 1$ for some prime $p \equiv 1 \pmod{4}$. For $p = 5$ this means $x \equiv 7$ or $18 \pmod{25}$. Hence $C_7 \cup C_{18} \subseteq V$, and $x \in R$ lies in $V$ iff $p^2 \mid x^2 + 1$ for some prime $p \equiv 1 \pmod{4}$ with $p \ge 13$.

*Proof.* $x^2 + 1 \equiv 1$ or $2 \pmod{4}$ and is never divisible by $3$. An odd prime $p$ divides $x^2 + 1$ only if $-1$ is a square mod $p$, that is, $p \equiv 1 \pmod{4}$. The roots of $x^2 \equiv -1 \pmod{25}$ are $7$ and $18$. ∎

**Types.** The *type* of $a$ is the triple $(\kappa, \mu, \nu)$ where:

- $\kappa \in \{C_7, C_{18}, R\}$ is the class of $a$ mod $25$;
- $\mu \in \{E, 1, 3\}$ records $a$ even, $a \equiv 1 \pmod{4}$ or $a \equiv 3 \pmod{4}$;
- $\nu \in \{0, 1, 2, 4, 5, 7, 8\}$ records $3 \mid a$, or the unit class of $a$ mod $9$.

This gives $3\cdot 3\cdot 7 = 63$ types. Each is a union of residue classes mod $900$. Type $t$ has density $w_t = w(\kappa)\cdot w(\mu)\cdot w(\nu)$, where $w(C_7) = w(C_{18}) = 1/25$, $w(R) = 23/25$, $w(E) = 1/2$, $w(1) = w(3) = 1/4$, $w(0) = 1/3$, and $w(\nu) = 1/9$ otherwise.

**Forcing.** For $q^2 \in \{4, 9, 25\}$, say a witness type $s$ *forces* a target type $t$ if $q^2 \mid ab + 1$ for every $a$ of type $t$ and $b$ of type $s$, for some such $q$. This happens exactly when one of the following holds:

| Modulus | Forced when |
| --- | --- |
| $25$ | $a, b$ both in $C_7$, or both in $C_{18}$ |
| $4$ | $a, b$ both odd, in different classes mod $4$ |
| $9$ | $a, b$ both units mod $9$, with $ab \equiv 8 \pmod{9}$ |

When $t$ is a $C$-type and $s$ does not force $t$, no $a$ of type $t$ and $b$ of type $s$ has $4 \mid ab + 1$, $9 \mid ab + 1$ or $25 \mid ab + 1$. For $25$, note that $a \equiv 7$ and $25 \mid ab + 1$ force $b \equiv 7$, and similarly for $18$. So non-squarefreeness must then come from $p^2$ with $p \ge 7$.

**Lemma 2.2 (forced share).** If $b \notin C_7$, the $C_7$-types forced by $b$ have total density at most $(1/25)(1 - (3/4)(8/9)) = (1/3)(1/25)$.

*Proof.* Forcing by $25$ is impossible. Forcing by $4$ removes at most one of the four classes mod $4$, and forcing by $9$ at most one of the nine classes mod $9$. These conditions are independent. ∎

The class $7 \bmod 25$ is special because a single modulus ($25$) forces every pair inside it. Every other source of non-squarefreeness has density well below $1$.

## 3. Counting lemmas

Throughout, $U$ is a union of types and $w_U$ its density. Two kinds of event are counted:

- the *B-event* $p^2 \mid ab + 1$, for a fixed witness $b$ and a prime $p \ge 7$ with $p \nmid b$;
- the *A-event* $p^2 \mid a^2 + 1$, for a prime $p \equiv 1 \pmod{4}$ with $p \ge 13$.

The B-event fixes $a$ in one class mod $p^2$, namely $a \equiv -b^{-1}$. The A-event fixes $a$ in two classes, $\pm\iota_p$.

**Lemma 3.1 (discrepancy).** Let $U = S \times \{c\}$, with $S$ a set of residues mod $36$ and $c$ a class mod $25$. Let $q \ge 1$ be coprime to $30$. Then for any residue $r$,

$$\#\{a \le N : a \in U,\ a \equiv r \ (q)\} = \frac{|S|\,N}{900\,q} + \theta \cdot 19, \qquad |\theta| \le 1.$$

The error is at most $38$ for a union over $C_7$ and $C_{18}$, at most $57$ for $S \times R$, and at most $3$ for all of $R$. Write $e_U$ for the bound that applies to $U$.

*Proof.* Write $a = a_0 + 25q\cdot i$. Since $25q$ is a unit mod $36$, the condition $a \in S \pmod{36}$ holds for $i$ in a set of $|S|$ classes mod $36$. A run of $J$ consecutive $i$ hits it $J|S|/36 + O(18)$ times, and $J \le N/(25q) + 1$. For $R$, write it as $\mathbb{Z}/25$ minus the two $C$ classes. ∎

**Lemma 3.2 (small primes).** Let $\mathcal{P}$ be a finite set of primes not dividing $30b$, and let event $p$ take $r_p$ classes mod $p^2$. Then

$$\#\{a \le N,\ a\in U : \text{some event } p\in\mathcal P \text{ holds}\} = w_U N\Big(1-\prod_{p\in\mathcal P}\big(1-\tfrac{r_p}{p^2}\big)\Big) + \theta\, e_U \Big(1+\prod_{p\in\mathcal P}(1+r_p)\Big).$$

*Proof.* Take the complement and apply Möbius inversion over subsets of $\mathcal{P}$. Each term is a union of $\prod r_p$ classes, each counted by Lemma 3.1. ∎

**Lemma 3.3 (medium primes).** For a single prime $p$, the count of $a \in U$ with the B-event exceeds $w_U N/p^2$ by at most $\min(e_U, 2N/(25p^2) + 2, N/p^2 + 1)$. It exceeds it by at most $1$ if $p^2 > N$. For the A-event on $R$ the excess is at most $\min(6, 2(N/p^2 + 1))$, and at most $1$ if $p^2 > 2N$.

*Proof.* These are Lemma 3.1, then the count ignoring the mod-36 condition, then the count ignoring $U$. A class mod $p^2 > N$ meets $[N]$ at most once. The roots satisfy $\iota + (p^2 - \iota) = p^2$, so at most one of them is $\le N$ when $p^2 > 2N$. ∎

**Lemma 3.4 (Pell bound for large primes in $x^2 + 1$).** Let $M = (N^2 + 1)/Y^2$ and $m_j = ((T_j + T_j^{-1})/2)^2$, where $T_j = (2N + 1)^{1/(2j-1)}$. Then

$$\#\{x \le N,\ x\in R : p^2 \mid x^2+1 \text{ for a prime } p>Y\} \le \sum_{j\ge1} \#\{2\le m\le \min(M,m_j) : m \text{ admissible}\}.$$

Here $m$ is *admissible* if $m \bmod 8 \in \{1, 2, 5\}$, $25 \nmid m$, and $m$ has no prime factor in $\{3, 7, 11, 19, 23\}$.

*Proof.* Write $x^2 + 1 = mp^2$. Then $m < M$, and $m \ge 2$. The number $m$ is not a square, since $X^2 - Z^2 = -1$ has no solution with $X \ge 1$. Primes $q \equiv 3 \pmod{4}$ never divide $x^2 + 1$. Also $x^2 + 1 \equiv 1, 2, 5 \pmod{8}$ and $p^2 \equiv 1 \pmod{8}$, and $25 \nmid x^2 + 1$ for $x \in R$.

The positive solutions of $X^2 - mZ^2 = -1$ are $\eta^{2j-1}$, where $\eta$ is the fundamental unit of $\mathbb{Z}[\sqrt{m}]$. From $mZ^2 = X^2 + 1$ with $Z \ge 1$ we get $\eta \ge \sqrt{m-1} + \sqrt{m}$. Also $\eta^{2j-1} = x + \sqrt{x^2+1} \le 2N + 1$. So a $j$-th solution with $x \le N$ needs $\sqrt{m-1} + \sqrt{m} \le T_j$, that is, $m \le m_j$. The map $x \mapsto (m, j)$ is injective. ∎

**Lemma 3.5 (lattice bound for large primes in $ab + 1$).** Fix $b$, and let $T_b$ be the $C_7 \cup C_{18}$ classes $a$ with $4 \nmid ab + 1$, $9 \nmid ab + 1$ and $25 \nmid ab + 1$. Let $\omega_1(b)$ be the number of distinct primes $\ge 7$ dividing $b$. Then

$$\#\{a\le N,\ a\in T_b : p^2\mid ab+1,\ p>Y\} \le 2^{\omega_1(b)}\Big[\frac{2\lambda(N+1)}{Y} + \frac{c\sqrt{bN+1}}{b} + \frac{\lambda(bN+1)}{Y^2} + c\Big].$$

The constants $(\lambda, c)$ depend only on the $\{2, 3, 5\}$-part of $b$; in all cases $\lambda \le 0.5334$ and $c \le 18.94$.

*Proof.* Write $ab + 1 = ms^2$ with $s = p > Y$. Then $m < (bN + 1)/Y^2$. Since $s$ is coprime to $30$, $m \bmod 1800$ lies in a set $S_b$ determined by $b \bmod 1800$. Also $ms^2 \equiv 1 \pmod{b}$, so $s$ lies in one of $\rho_b(m)$ classes mod $b$. Here $\rho_b(m) \le \rho_{b_0}(m)\cdot 2^{\omega_1(b)}$, with $b_0$ the $\{2, 3, 5\}$-part of $b$. So the count for a given $m$ is at most $\rho_b(m)(\sqrt{(bN+1)/m}/b + 1)$.

The weight $g(m) = \rho_{b_0}(m)\cdot \mathbf{1}[m \in S_b]$ is $1800$-periodic. Computed exactly, its partial sums satisfy $\sum_{m\le x} g(m) \le \lambda x + c$. Partial summation then gives $\sum g(m)/\sqrt{m} \le 2\lambda\sqrt{M} + c$. ∎

## 4. The type-matrix bound

Fix truncation points $z_A$, $z_B$ and put

$$\beta^{+} = 1-\prod_{7\le p\le z_B}\Big(1-\frac1{p^2}\Big) + \sum_{p>z_B}\frac1{p^2}, \qquad \alpha_s = 1-\prod_{\substack{13\le p\le z_A\\ p\equiv1\,(4)}}\Big(1-\frac2{p^2}\Big), \qquad \tau_A = 2\sum_{\substack{p>z_A\\ p\equiv1\,(4)}}\frac1{p^2}.$$

The tails are evaluated exactly up to $10^{7}$, and beyond that by the bound $\sum_{p>x} p^{-2} \le 2.51012/(x \ln x)$, which follows from Rosser–Schoenfeld.

**The witness game.** Let $P$ be a set of types, and $W \subseteq P$ with $1 \le |W| \le 2$. Define

$$\mathrm{val}(P,W) = \sum_{\substack{t\in P\\ t \text{ a C-type}}} w_t\cdot\begin{cases}1 & \text{every } s\in W \text{ forces } t\\ \beta^{+} & \text{otherwise}\end{cases} \;+\; \sum_{\substack{t\in P\\ t\subseteq R}} w_t\,\alpha_s \;+\; \mathbf 1[P\cap R\neq\varnothing]\,\tfrac{23}{25}\tau_A,$$

$$V_2 = \max_{P}\ \min_{W\subseteq P,\ 1\le|W|\le 2} \mathrm{val}(P,W),$$

with the maximum over type sets $P$ not contained in the $C_7$-types and not contained in the $C_{18}$-types.

**Theorem 4.1.** If $A \subseteq [N]$ is valid and not contained in $C_7$ or $C_{18}$, then $|A| \le V_2\cdot N + E_I(N)$, where $E_I$ is the explicit error of Section 5.

*Proof.* Let $P$ be the set of types met by $A$. $P$ is not contained in one class, because the type determines the class. Choose $W$ attaining the minimum, and for each $s \in W$ pick $b_s \in A$ of type $s$. Each type $t \in P$ is bounded as follows.

1. **$C$-types forced by every witness.** Use $|A \cap t| \le |t \cap [N]| = w_t N + O(1)$, by Lemma 3.1.
2. **Other $C$-types.** Assign each one to a witness $s \in W$ that does not force it, and let $U_s$ be the union of the types assigned to $s$. By Section 2, every $a \in A \cap U_s$ has $p^2 \mid ab_s + 1$ for some prime $p \ge 7$. Lemma 3.2 handles $p \le z_B$, Lemma 3.3 handles $z_B < p \le Y$ and Lemma 3.5 handles $p > Y$. Together they give $|A \cap U_s| \le w_{U_s}\cdot \beta^{+}\cdot N + E_B(N)$.
3. **$R$-types.** Use $A \cap t \subseteq V \cap t$. By Lemma 2.1 the count is bounded by A-events for primes $p \ge 13$. Lemma 3.2 on the union of the $R$-types in $P$ handles $p \le z_A$. Lemmas 3.3 and 3.4, applied over all of $R$, handle $p > z_A$.

Summing gives $\mathrm{val}(P, W)\cdot N$ plus the error terms. ∎

**Value of the game.** The game is a 0–1 problem over $2^{63}$ type sets. At $(z_A, z_B) = (17, 13)$ we solved it by an exact branch-and-bound in integer arithmetic, with inputs scaled by $10^{15}$ and rounded up, so the certified value is an upper bound. A mixed-integer program (HiGHS; Q. Huangfu and J. A. J. Hall, Math. Prog. Comp. 10 (2018), 119–142) gives the same optimum. The worst $P$ is the set of all 63 types, so

$$V_2 = \tfrac{2}{25}\beta^{+} + \tfrac{23}{25}(\alpha_s+\tau_A) \le 0.0294059212,$$

certified with 1,339,011 branch-and-bound nodes. The same formula holds at every pair $(z_A, z_B) \in \{17, 29, 37, 41\} \times \{13, 17, 19, 23\}$; only $(41, 23)$, where $V_2 \le 0.0292884$, is used again (Theorem B).

The value is easy to see for $P = \text{all types}$. Take one witness of type $(C_7, E, 0)$ and one of type $(C_{18}, E, 0)$. A witness that is even and divisible by $3$ never forces by $4$ or $9$, so each $C$-class gets density $\beta^{+}$, from the witness in the other class. The content of the certificate is that no adversarial choice of $P$ does better than this.

Since $1/25 - 0.0294059 = 0.0105941 > 0$, Theorem A follows for every $N$ with $E_I(N) \le 0.0105941N - 0.28$. Section 5 makes this explicit.

## 5. The explicit threshold

**The error term.** Let $k_A$ and $k_B$ be the numbers of primes in the small-prime ranges of Lemma 3.2: primes $p \equiv 1 \pmod{4}$ with $13 \le p \le z_A$, and primes with $7 \le p \le z_B$. Then

$$E_I(N) = 2\cdot 38\,(1+2^{k_B}) + 38 + 57\,(1+3^{k_A}) + E_A(N) + 2E_B(N),$$

$$E_A(N)=\min_Y\Big[\sum_{z_A<p\le Y}\text{(Lemma 3.3 excess)} + \text{(Lemma 3.4)}\Big],$$

$$E_B(N)=\max_{b\le N}\min_Y\Big[\sum_{z_B<p\le Y}\text{(Lemma 3.3 excess)} + \text{(Lemma 3.5)}\Big].$$

The maximum over $b$ runs over the 2-, 3- and 5-profile of $b$ and over $k = \omega_1(b)$. Here $\omega_1(b) = k$ forces $b \ge b_0\cdot 7\cdot 11\cdots p_k$, which tames the factor $2^k$.

**The $\omega$-refinement.** Near $N_0$ the factor $2^{\omega_1(b)}$ is the bottleneck, so witnesses with many prime factors are avoided. Let $K_k(N) = \#\{b \le N : b \in V, \omega_1(b) \ge k\}$, computed exactly ($K_5(10^{7}) = 672$). Split $A = A' \sqcup A''$, where $A''$ is the elements with $\omega_1 \ge k_0$.

- If $A'$ is not inside one class, apply Theorem 4.1 to $A'$ with witnesses from $A'$. Then $|A| \le V_2N + E_I(N; \omega_1 < k_0) + K_{k_0}(N)$.
- Otherwise, say $A' \subseteq C_7$ and $A \not\subseteq C_7$. Use one witness $b \in A'' \setminus C_7$. Lemma 2.2 gives $|A \cap C_7| \le g_1N + E_{II}(N)$, with $g_1 = (1/3 + (2/3)\beta^{+})/25 \approx 0.01469$, and $|A \setminus C_7| \le K_{k_0}(N)$.

The second case has much smaller density, so it never binds.

**Grid certification.** Fix $(z_A, z_B) = (17, 13)$. For fixed $(k_0, Y)$, every term of $E$ is nondecreasing in $N$. So it suffices to cover $[N_0, 10^{60}]$ by cells $[N_{lo}, N_{hi}]$, of ratio $1.01$ below $10^{13}$ and $1.1$ above, and to check for each cell that

$$E(N_{hi}) \le \big(\tfrac1{25}-V_2\big)N_{lo} - 0.28 .$$

This gives $|A| \le N/25 - 0.28 = (N - 7)/25 < c_7(N)$ throughout the cell. The $\omega$-refinement ($k_0 = 5$) is needed only below $10^{8}$. Prime counts up to $10^{7}$ are exact, and beyond that come from the Rosser–Schoenfeld and Dusart bounds. Every cell passes. The smallest slack is $+329.8$, in the first cell $[6.7838\cdot 10^{6}, 6.85\cdot 10^{6}]$. As a fraction of $N$ the slack is $0.0016$ at $10^{7}$, $0.0053$ at $10^{8}$ and $0.0106$ at $10^{60}$, approaching $1/25 - V_2 = 0.010594$. A second implementation, which optimises the parameters in each cell, agrees on $[10^{7}, 10^{60}]$.

**Proposition 5.1 (tail).** For $N \ge 10^{60}$, Theorem 4.1 holds with $E_I(N) \le 1.02\cdot 10^{-8}\cdot N$.

*Proof.* Take $(z_A, z_B) = (17, 13)$, $Y = N^{2/3}$ and no $\omega$-refinement. Let $L = \ln N$. The terms are bounded as follows:

- the inclusion–exclusion constant is $1292$;
- Lemma 3.3 on the $A$ side is at most $6\pi(\sqrt{2N}) + \pi(N^{2/3})$;
- Lemma 3.4 is at most $(1 + 10^{-4})N^{2/3}\cdot J$, where $J = (1 + \ln(2N+1)/\ln(1+\sqrt{2}))/2 = O(L)$;
- Lemma 3.3 on the $B$ side is at most $38\pi(\sqrt{N}) + \pi(N^{2/3})$;
- Lemma 3.5 is at most $2^k\cdot(1.067N^{2/3} + 20\sqrt{N})$.

Robin's bound $\omega(n) \le 1.38402\cdot\ln n/\ln\ln n$ gives $2^k \le N^{0.95933/\ln L} \le N^{0.1947}$. The prime counts use $\pi(x) < 1.25506x/\ln x$. Each term divided by $N$ decreases for $N \ge 10^{60}$, and the total at $N = 10^{60}$ is $1.02\cdot 10^{-8}\cdot N$. ∎

**Corollary 5.2.** Theorem A holds for all $N \ge 6.7838\cdot 10^{6}$, and every valid set not inside one class has $|A| \le (N - 7)/25$. (Sawhney suggested on the forum that large-sieve methods should bring $N_0$ down to about $10^{6}$. The witness game reaches the same order by a different route.)

## 6. Small N

Let $m(N)$ be the largest size of a valid $A \subseteq [N]$ not inside $C_7$ or $C_{18}$. A valid set inside one class has at most $c_7(N)$ elements, so Theorem A at $N$ says $m(N) \le c_7(N)$. The function $m$ is nondecreasing, and $c_7$ is constant on each block $(6 + 25k, 31 + 25k]$. One computation serves both Theorem A and Theorem C(2).

**$N \le 1006$: exact cliques.** Valid sets are exactly the cliques in the graph on $V \cap [N]$ with edges $\{a, b\}$ where $ab + 1$ is not squarefree. We compute $m(N)$ at each $N \equiv 6 \pmod{25}$ as a maximum over cliques that contain an $R$-vertex or meet both $C_7$ and $C_{18}$. Then $m(N) \le c_7(N)$ throughout, with equality only for $41 \le N \le 81$.

**$1006 < N \le 6.9\cdot 10^{6}$: case bounds.** Let $H_t(b, N) = \#\{a \in V \cap C_t, a \le N : ab + 1 \text{ not squarefree}\}$ for $t \in \{7, 18\}$, and let $H_{\text{odd}}(b, N)$ count the odd such $a$ in $C_7 \cup C_{18}$. Let $v_R(N) = |V \cap R \cap [N]|$, and $v_R^{\text{odd}}(N)$ its odd part. Every valid $A$ not inside $C_7$ or $C_{18}$ falls into one of four cases.

| Case | Condition on A | Bound on \|A\| |
| --- | --- | --- |
| S1 | $A \cap R$ contains an even $b$ | $v_R$ + max over even $b \in V \cap R$ of $[H_7(b) + H_{18}(b)]$ |
| S2 | $A \cap R \ne \emptyset$ and all odd; $A \cap (C_7 \cup C_{18})$ all odd | $v_R^{\text{odd}}$ + max over odd $b \in V \cap R$ of $H_{\text{odd}}(b)$ |
| S3 | $A \cap R \ne \emptyset$ and all odd; an even $b' \in C_7 \cup C_{18}$ | $v_R^{\text{odd}}$ + max of $H_7(b)$ over odd $b \in R$, plus max of $H_{18}(b')$ over even $b' \in C_7$ (or the same with 7 and 18 swapped) |
| S4 | $A \cap R = \emptyset$, $A$ meets $C_7$ and $C_{18}$ | max of $H_7(b')$ over $b' \in C_{18}$, plus max of $H_{18}(b)$ over $b \in C_7$ |

Each bound is correct because every element of $A \cap C_t$ is compatible with the chosen witness. In S2 an odd $R$-witness and odd $C$-elements remain. In S3 an even $C$-element of one class witnesses the other class.

All four bounds are nondecreasing in $N$. So $S(N) = \max S_i$ at the end $E_k$ of a block bounds $m(N)$ for every $N \in (E_{k-1}, E_k]$, and it suffices that $S(E_k) < c_7(E_{k-1} + 1)$. We use blocks of width $\max(25, E_{k-1}/100)$. The check holds on all 859 blocks from 1006 to $6.9\cdot 10^{6}$. For example, $S(10^{6}) = 37{,}637 < c_7 = 40{,}000$. The counts $H_t(b, N)$ are computed exactly:

- primes $p \le (bN)^{1/3}$ by stepping through the class $a \equiv -b^{-1} \pmod{p^2}$;
- larger primes by enumerating $ab + 1 = mp^2$ over $m$, solving $s^2 \equiv m^{-1} \pmod{b}$ by CRT.

**Proof of Theorem A.** For $N \le 6.9\cdot 10^{6}$ this is the computation above, and for $N \ge 6.7838\cdot 10^{6}$ it is Corollary 5.2. ∎

## 7. Stability, rigidity and the extremisers

**Proof of Theorem B.** The first bound is Corollary 5.2. For the asymptotic bound, apply Theorem 4.1 with $(z_A, z_B) = (41, 23)$, where $V_2 \le 0.0292884$. The argument of Proposition 5.1 gives $E_I(N) = o(N)$ for any fixed parameters. ∎

Theorem B implies a robust form. If $N \ge 6.7838\cdot 10^{6}$ and $|A| > (N - 7)/25$, then $A \subseteq C_7$ or $A \subseteq C_{18}$, so $A$ is one full class with some elements removed. Nothing outside the class can be added. Sawhney's note gives this with an unspecified $\eta$. Here $\eta$ can be taken to be $0.0016$ at $N = 10^{7}$, rising to about $0.0107$ as $N \to \infty$.

**Proof of Theorem C(1), upper bound.** Pick $b \in A \setminus C_7$. Then $A \cap C_7$ is contained in $\{a \in C_7 : ab + 1 \text{ not squarefree}\}$. By Lemma 2.2 the forced share $s$ satisfies $s \le 1/3$. On the remaining types only primes $p \ge 7$ contribute, and Lemmas 3.2, 3.3 and 3.5 bound them by $(1 - s)\beta^{+}N/25$ plus an error. The bound $s + (1 - s)\beta^{+}$ increases with $s$, so

$$|A\cap C_7| \le \tfrac1{25}\big(\tfrac13+\tfrac23\beta^{+}\big)N + 38\,(1+2^{k_B}) + 38 + E_B(N).$$

This holds for every $N$. Letting $z_B \to \infty$ gives the limsup bound $g_1^*$. ∎

**Sharpness.** Let $q$ be a prime with $q \equiv 18 \pmod{25}$, $q \equiv 1 \pmod{4}$ and $q \equiv 1 \pmod{9}$. Put $A_q(N) = \{q\} \cup \{a \in C_7 \cap [N] : aq + 1 \text{ not squarefree}\}$. This set is valid:

- pairs inside $C_7$ have $25 \mid ab + 1$;
- the pair $(q, q)$ has $25 \mid q^2 + 1$;
- the pairs $(a, q)$ are valid by definition.

The forced share is exactly $1/3$, from $a \equiv 3 \pmod{4}$ or $a \equiv 8 \pmod{9}$. On the other cells, the events $p^2 \mid aq + 1$ for $p \ge 7$, $p \ne q$ are independent of the cell by CRT. The squarefree sieve for a linear form gives density $\beta(q) = 1 - \prod_{p\ge 7, p\ne q}(1 - p^{-2})$. So $|A_q(N)|/N \to (1/3 + (2/3)\beta(q))/25$, which tends to $g_1^*$ as $q \to \infty$. ∎

**Relation to Li's proof.** Li's "uniform mixed degree" proposition says that for $N \ge 5\cdot 10^{6}$, every $b \in V$ outside $C_7 \cup C_{18}$ has more than $N/50 + N/525 \approx 0.0219N$ squarefree neighbours in $C_7 \cap [N]$, and likewise in $C_{18} \cap [N]$. Theorem C(1) is the sharp form of this. The squarefree degree is $c_7(N) - H_7(b)$, so the worst case is asymptotically $(1/25 - g_1^*)N \approx 0.0253N$, and no constant above $1/25 - g_1^*$ is possible. Computing $H_7$ and $H_{18}$ exactly for every $b \le 10^{7}$ confirms Li's proposition on all of $5\cdot 10^{6} \le N \le 10^{7}$, with a margin of at least 13.8%. Each 1% block is checked conservatively: the largest $H$ at the top of the block, against the class size at the bottom and Li's threshold at the top. There $\max H_7(b)/N$ stays at $0.01468$, matching $g_1^*$.

**Proof of Theorem C(2).** A valid set inside $C_7$ has at most $c_7(N)$ elements, with equality only for $C_7 \cap [N]$, and the same holds for $C_{18}$. So it suffices to show $m(N) < c_7(N)$ for $N \notin [41, 81]$, and to list the sets attaining $m = c_7$ inside $[41, 81]$. Section 6 gives $m(N) < c_7(N)$ for every $N \le 6.9\cdot 10^{6}$ outside $[41, 81]$, and Theorem B gives it for $N \ge 6.7838\cdot 10^{6}$. Enumerating all maximal cliques for $7 \le N \le 106$ gives exactly the sets in the table below.

| $N$ | $c_7(N)$ | Extra maximisers |
| --- | --- | --- |
| 41–42 | 2 | $\{7, 41\}$ |
| 43–56 | 2 | $\{7, 41\}$, $\{32, 43\}$, $\{41, 43\}$ |
| 57–81 | 3 | $\{32, 43, 57\}$ |

For instance, $32\cdot 43 + 1 = 3^4\cdot 17$, $32\cdot 57 + 1 = 5^2\cdot 73$ and $43\cdot 57 + 1 = 2^2\cdot 613$, and 25 divides $32^2 + 1$, $43^2 + 1$ and $57^2 + 1$. ∎

**Proof of Theorem D.** If $a, b \in F$ lie in the same class mod 25, then $25 \mid ab + 1$. If $a \equiv 7$ and $b \equiv 18 \pmod{25}$, then $a \equiv 1$ and $b \equiv 3 \pmod{4}$, so $ab + 1 \equiv 0 \pmod{4}$. The case $a = b$ is covered by the first case. $F$ meets both classes, for example $57 \in C_7$ and $43 \in C_{18}$, and has density $2\cdot(1/25)(1/4) = 1/50$. Maximality among congruence-defined sets comes from an exact maximum-clique computation on the forcing graph mod 900. Its value is $1/50$, attained by $F$ up to symmetry. The upper bound for $\lambda^*$ is Theorem 8.1. Validity of $F$, of $C_7$ and $C_{18}$, and of the four exceptional maximisers is checked in Lean 4 (`Erdos848Constructions.lean`). ∎

## 8. The second-best density

Let $\lambda^*(N)$ be the largest size of a valid $A \subseteq [N]$ contained neither in $C_7$ nor in $C_{18}$.

**Theorem 8.1.** For every $N$, $\lambda^*(N) \le N/50 + E(N)$, where $E(N) = N^{2/3+o(1)}$ is the explicit function of Section 8.5. Moreover, by the refinement of Section 8.6, $\lambda^*(N) \le N/50 + 30\cdot N^{0.81}$ for every $N$. The set $F$ of Theorem D gives $\lambda^*(N) \ge N/50 - 2$. Hence $\lambda^*(N)/N \to 1/50$.

Section 8.1 proves the theorem for sets inside $C_7 \cup C_{18}$ by a short argument. Sections 8.2–8.4 prove the general case: a counting lemma, then an all-witness version of the game of Section 4, then an exact certificate. Section 8.5 makes every constant explicit, Section 8.6 lowers the constant to 30, and Section 8.7 proves the third-order Theorem 8.9.

### 8.1 Sets inside $C_7 \cup C_{18}$

**Proposition 8.2.** Let $A \subseteq [N]$ be valid, $A \subseteq C_7 \cup C_{18}$, and suppose $A$ meets both classes. Then $|A| \le N/50 + O(N^{0.81})$.

*Proof.* Put $X = A \cap C_7$ and $Y = A \cap C_{18}$, and let $x, y$ be their sizes relative to $N/25$. For $a \in X$ and $b \in Y$ we have $ab + 1 \equiv 7\cdot 18 + 1 \equiv 2 \pmod{25}$. So $ab + 1$ is non-squarefree only if:

- (4) $a$ and $b$ are odd with $ab \equiv 3 \pmod{4}$, or
- (Q) $9 \mid ab + 1$, or $p^2 \mid ab + 1$ for some prime $p \ge 7$.

For fixed $b$, let $\mathrm{Comp}_Q(b)$ be the set of $a \in C_7 \cap [N]$ satisfying (Q). The condition $9 \mid ab + 1$ picks out one class mod 9, and $p^2 \mid ab + 1$ one class mod $p^2$. Lemma 8.3 handles $p > N^{0.6}$. So $\mathrm{Comp}_Q(b)$ has relative size at most

$$c = \frac19 + \sum_{p\ge 7}\frac1{p^2} = 0.16225\ldots < \frac16,$$

up to $O(N^{0.8+o(1)})$, and by CRT it meets each class mod 4 proportionally. Split $X$ and $Y$ by residue mod 4 into even, 1 and 3 parts. A pair not forced by 4 lies in $\mathrm{Comp}_Q$ of its partner. A case analysis on which odd classes each side meets gives:

- one side has no odd element: $x + y \le 2c$;
- one side meets both odd classes: $x + y \le \max(2c, 1/4 + 3c/2)$;
- both sides meet the same single odd class: $x + y \le 3c/2$;
- they meet opposite single odd classes (the shape of $F$): $x + y \le 1/2$ if neither side has an even element, and otherwise $x + y \le \max(1/4 + 3c/2, 2c)$.

Since $c < 1/6$, every case gives $x + y \le 1/2$. ∎

### 8.2 Counting with an arbitrary target

**Lemma 8.3 (large primes, any target).** For $1 \le b \le N$ and $Y \ge 1$,

$$\#\{a\le N : q^2\mid ab+1 \text{ for some prime } q>Y\} \le 2^{\omega(b)+1}\Big(\frac{2(N+1)}{Y}+\frac{N^2+1}{Y^2}\Big).$$

*Proof.* Write $ab + 1 = mq^2$. Then $1 \le m < (bN + 1)/Y^2$, and $ms^2 \equiv 1 \pmod{b}$ with $s = q$. So $s$ is a square root of $m^{-1} \bmod b$. There are at most $2^{\omega(b)+1}$ of these: two for each odd prime power, at most four for a power of 2. Also $s \le \sqrt{(bN + 1)/m}$. So each $m$ contributes at most $2^{\omega(b)+1}(\sqrt{(bN + 1)/m}/b + 1)$. Summing over $m < M = (bN + 1)/Y^2$, and using $\sum m^{-1/2} \le 2\sqrt{M}$, gives $2^{\omega(b)+1}(2(bN + 1)/(bY) + M)$. This is at most the bound stated, since $1 \le b \le N$. ∎

This is a cruder form of Lemma 3.5 that needs no information about the target. Since $2^{\omega(b)} = N^{o(1)}$, with $Y = N^{0.6}$ it is $N^{0.8+o(1)}$.

**Lemma 8.4 (joint estimate for R-targets).** Let $t$ be a residue class mod 900 inside $R$, of density $w_t$ (for a type made of $r_t$ such classes, add the bounds; each additive error term is then multiplied by $r_t$, as in Section 8.5), and let $b \le N$ be a witness that does not force $t$. Then

$$\#\{a\in t\cap[N] : a\in V,\ ab+1 \text{ not squarefree}\} \le w_t\, j^{+} N + O(N^{0.8+o(1)}),$$

$$j^{+} = \alpha^{+}\beta_{500} + \kappa + \tau + \tau_B \le 0.01577,$$

where

- $\alpha^{+} = \sum 2/p^2$ over primes $p \equiv 1 \pmod{4}$, $p \ge 13$;
- $\beta^{+} = \sum_{q\ge 7} 1/q^2 = 0.051136$ (in this section; it is at least the truncated $\beta^{+}$ of Section 4), and $\beta_{500} = \sum_{7\le q\le 500} 1/q^2 = 0.050863$;
- $\kappa = \sum 1/p^2$ over primes $p \equiv 1 \pmod{4}$, $p \ge 13$;
- $\tau = 2\sum 1/p^2$ over primes $p \equiv 1 \pmod{4}$, $p > 500$, which is at most $0.00028$; and $\tau_B = \sum 1/q^2$ over all primes $q > 500$, which is also at most $0.00028$.

*Proof.* Membership $a \in V$ needs $p^2 \mid a^2 + 1$ for some $p \equiv 1 \pmod{4}$, $p \ge 13$ (Lemma 2.1). Because $b$ does not force $t$, non-squarefreeness of $ab + 1$ needs $q^2 \mid ab + 1$ for some $q \ge 7$. Split into three parts.

1. **$p, q \le 500$.** By CRT with mod 900, a pair $p \ne q$ fixes 2 classes mod $900p^2q^2$, contributing at most $2(w_t N/(p^2q^2) + 1)$. A pair $p = q$ needs $a \equiv \pm\iota_p$ and $a \equiv -b^{-1} \pmod{p^2}$, at most one class, contributing $w_t N/p^2 + 1$. Together these give at most $w_t(\alpha^{+}\beta_{500} + \kappa)N + O(1)$.
2. **$p > 500$.** Lemma 3.3 for $500 < p \le N^{0.6}$ and Lemma 3.4 for $p > N^{0.6}$ give at most $w_t \tau N + O(N^{0.8} \log N)$.
3. **$q > 500$.** Drop the condition on $p$. For $500 < q \le N^{0.6}$ each prime fixes one class, contributing at most $w_t N/q^2 + 1$, so these give at most $w_t \tau_B N + \pi(N^{0.6})$. For $q > N^{0.6}$ use Lemma 8.3. ∎

For a C-type target that $b$ does not force, the same argument without the condition $a \in V$ gives at most $w_t \beta^{+} N + O(N^{0.8+o(1)})$, with $\beta^{+} \le 0.05114$.

### 8.3 The all-witness game and its core

Use 525 types $t$: $a \bmod 25$, $a \bmod 4$ (even, 1 or 3), and $a \bmod 9$ with $3 \mid a$ merged. Let $P$ be the set of types met by a valid $A$ not inside one class, and choose a witness $b_s \in A$ of each type $s \in P$. Every $a \in A \cap t$ is compatible with every witness, so $|A \cap t| \le$ min over $s \in P$ of the bound for witness $b_s$. The possible bounds are:

- **Forced C-target:** $w_t N + O(1)$.
- **Non-forced C-target:** $w_t \beta^{+} N + O(N^{0.8+o(1)})$.
- **R-target:** $w_t j^{+} N + O(N^{0.8+o(1)})$. An R-type never forces itself: $a^2 \equiv -1$ has no solution mod 4 or mod 9, and mod 25 only in $C_7$ or $C_{18}$. So each R-type in $P$ can use its own witness.

**Lemma 8.5 (core reduction).** Let $K$ be the set of types in $P$ forced by every type in $P$, and let $F(K)$ be the set of types forcing every member of $K$. Then $K$ consists of C-types, $P \subseteq F(K)$, and

$$|A| \le \Big(w(K) + \beta\, w\big(\mathcal C\cap F(K)\setminus K\big) + j\, w\big(\mathcal R\cap F(K)\big)\Big)N + O(N^{0.8+o(1)}) =: U(K)\,N + O(N^{0.8+o(1)}),$$

for any $\beta \ge \beta^{+}$ and $j \ge j^{+}$. Here $\mathcal{C}$ and $\mathcal{R}$ are the C-types and the R-types.

*Proof.* Forcing is symmetric, so every $s \in P$ forces every member of $K$, giving $P \subseteq F(K)$. A non-core C-type in $P$ is not forced by some $s \in P$, and an R-type in $P$ uses its own witness. Sum the bounds above over $t \in P$. ∎

### 8.4 The certificate

A $C$-type is forced by a type outside its own class only through $4$ or $9$, never $25$, since $7\cdot 18 + 1 \equiv 2 \pmod{25}$ and $7r + 1 \not\equiv 0$ for $r \in R$. So forcing between a core and the rest depends only on cells $\mathrm{mod}\ 36$: 21 cells per class.

A core is a pair $(M_7, M_{18})$ of cell sets with every cross pair forced. Each half is automatically internally forced, by $25$. $U(K)$ is then a function of three sets of cells:

- the cells forced with all of $M_{18}$ (the $C_7$ part of $F(K)$);
- the cells forced with all of $M_7$ (the $C_{18}$ part);
- the cells forced with all of $M_7 \cup M_{18}$ (the $R$ part, in each of the 23 classes of $R$).

**Proposition 8.6.** With $\beta = 0.052$ and $j = 0.0169$, $U(K) \le 1/50$ for every core $K$ for which $F(K)$ contains a type outside $C_7$ and a type outside $C_{18}$. Equality holds only for the core of $F$ and its mirror image.

*Proof.* Write $A(M)$ for the set of cells forced with every cell of $M$. The program `lamcert.c` enumerates all 51,223 such cores and evaluates $900\cdot U$ in exact integer arithmetic.

A much smaller check suffices. Replacing $M$ by its closure $A(A(M))$ does not change $A(M)$, because $A(A(A(M))) = A(M)$, and it does not lower $U$, because the closure contains $M$. So both halves of the core may be taken closed. Only 64 sets of cells have the form $A(M)$, and they give 439 admissible pairs.

This reduced check is formalised in `LamCert.lean` and checked by the Lean kernel (`decide`, with no `native_decide`). The file also proves the closure argument, the equality case, and that the forcing relation on cells is exactly divisibility of $ab + 1$ by $4$ or $9$.

The check fails with $\beta = 0.10$ and $j = 0.03$, so it is not vacuous. The bound survives up to $j = 0.01721$ (with $\beta = 0.052$) or $\beta = 0.0556$ (with $j = 0.0169$). A floating-point MILP over all $2^{525}$ type sets, run independently, gives the same value $1/50$ with a matching dual bound. ∎

**Proof of Theorem 8.1.** Since $\beta^{+} \le 0.05114 < 0.052$ and $j^{+} \le 0.01577 < 0.0169$, Lemma 8.5 and Proposition 8.6 give $|A| \le N/50 + O(N^{0.8+o(1)})$, taking $Y = N^{0.6}$. Section 8.5 chooses $Y$ better and makes every term explicit. ∎

### 8.5 The explicit error term

Let $r_t$ be the number of residues $\mathrm{mod}\ 900$ in the type $t$. These sum to $72$ over the 42 $C$-types, and to $828$ over the 483 $R$-types. Fix a cut-off $Y$ for the primes $q$ in $ab + 1$, and $Y'$ for the primes $p$ in $a^2 + 1$. Going through the proofs of Lemmas 8.3–8.5, the error is at most the sum of these terms:

- **Core $C$-types:** $|t \cap [N]| \le w_t N + r_t$, so $72$ in total.
- **Other $C$-types, $7 \le q \le Y$:** one class $\mathrm{mod}\ q^2$ for each prime, so at most $72\pi(Y)$.
- **Other $C$-types, $q > Y$:** a non-forced $C$-target lies in $T_b$, so Lemma 3.5 applies. This gives $42\cdot L_C$, where $L_C$ is the bound of Lemma 3.5 with $b \le N$.
- **$R$-types, $p, q \le 500$:** $828(2n_1n_2 + n_1)$, where $n_1 = 43$ and $n_2 = 92$ count the primes in the two ranges.
- **$R$-types, $500 < q \le Y$:** at most $828\cdot\pi(Y)$, one residue error per prime $q$ (the condition on $p$ is dropped, as in Lemma 8.4).
- **$R$-types, $q > Y$:** $483\cdot L$, where $L = 2^{\omega^*(N)+1}(2(N+1)/Y + (N^2+1)/Y^2)$ comes from Lemma 8.3, and $\omega^*(N)$ is the largest number of distinct prime factors of an integer $\le N$.
- **$R$-types, $500 < p \le Y'$:** at most $1656\cdot\pi(Y')$.
- **$R$-types, $p > Y'$:** the bound of Lemma 3.4, counted once for all of $R$, because the types are disjoint.

Let $E(N)$ be the minimum of this sum over $Y$ and $Y'$. The script `explicitC.py` evaluates $E$ on cells of ratio $10^{0.1}$ up to $N = 10^{601}$, refined to ratio $10^{0.01}$ between $10^{10}$ and $10^{25}$. It uses exact prime counts below $10^{7}$ and $\pi(x) < 1.25506x/\ln x$ above. For fixed $Y$ and $Y'$ every term is nondecreasing in $N$, so each cell is checked at its upper end. Some values:

| $N$ | $10^{7}$ | $10^{13}$ | $10^{20}$ | $10^{30}$ | $10^{60}$ | $10^{100}$ |
| --- | --- | --- | --- | --- | --- | --- |
| $E(N)/N$ | $27$ | $0.31$ | $0.0030$ | $2.4\cdot 10^{-6}$ | $4.1\cdot 10^{-15}$ | $1.1\cdot 10^{-26}$ |

The best $Y$ lies between about $N^{0.72}$ and $N^{0.85}$, and $E(N) = N^{2/3+o(1)}$. The bound beats the trivial bound $|A| \le N$ from about $N = 10^{11.7}$.

So $|A| \le N/50 + C\cdot N^{0.81}$ holds for every $N$, with $C$ the largest value of $\min((49/50)N^{0.19}, E(N)/N^{0.81})$. The grid gives $C \le 167.5$, attained near $N = 10^{11.75}$. Beyond $10^{601}$, take $Y = Y' = N^{2/3}$ and use Robin's bound $\omega(n) \le 1.38402 \ln n/\ln\ln n$. This gives $E(N) \le 1001\cdot 2^{\omega^*(N)}N^{2/3}$, so $E(N)/N^{0.81}$ is at most $4\cdot 10^{-4}$ and decreasing there. This gives $C = 170$. Section 8.6 lowers it to $30$.

The constant is large because the witness may have many prime factors, and because the large-prime count is crude. The exponent $0.81$ can be replaced by any number above $2/3$, at the cost of a larger $C$.

### 8.6 Witnesses with many prime factors

The factor $2^{\omega(b)}$ in Lemmas 3.5 and 8.3 is paid for the worst possible witness. As in the $\omega$-refinement of Section 5, it can be avoided by setting aside the elements with many prime factors. Fix $k \ge 1$, let $A''$ be the elements of $A$ with at least $k$ distinct prime factors, and let $A' = A \setminus A''$.

**Lemma 8.7 (Rankin).** For every $z \ge 1$, $\#\{n \le N : \omega(n) \ge k\} \le z^{-k}\cdot N\cdot \exp((z - 1)S(N))$, where $S(N) = \sum_{p\le N} 1/p < \log\log N + B + 1/\log^2 N$ and $B = 0.26150\dots$ is the Meissel–Mertens constant.

*Proof.* Since $z^{\omega(n)} = \sum_{d \mid n,\ d \text{ squarefree}} (z - 1)^{\omega(d)}$, we get $\sum_{n\le N} z^{\omega(n)} \le N\cdot\prod_{p\le N}(1 + (z - 1)/p) \le N\cdot \exp((z - 1)S(N))$. Divide by $z^k$. The bound on $S(N)$ is Rosser and Schoenfeld's. ∎

For $N \le 10^{18}$ a sharper bound comes from Hardy and Ramanujan's induction, run numerically. Write $N_j(x) = \#\{n \le x : \omega(n) = j\}$ and $P(y)$ for the number of prime powers up to $y$.

**Lemma 8.8.** For $x \ge 1$ and $k \ge 1$,

$$N_{k+1}(x) \le \sum_{\substack{m\le\sqrt{x}\\ \omega(m)=k}} P(x/m) + \frac{1}{k+1}\sum_{\substack{q\le\sqrt{x}\\ q \text{ a prime power}}} N_k(x/q).$$

*Proof.* Let $n \le x$ have $k + 1$ prime-power factors. If the largest of them, $q$, exceeds $\sqrt{x}$, then $n = qm$ with $m < \sqrt{x}$ and $\omega(m) = k$, and this representation is unique. Otherwise each of the $k + 1$ prime-power factors $q$ is at most $\sqrt{x}$, and $n/q$ has $k$ prime factors and is at most $x/q$, so $n$ is counted $k + 1$ times in the second sum. ∎

The script `omega_envelope.py` (in its final form inside `explicitC_omega3.py`) starts from exact counts of $N_j$ at the points $10^{i/200}$ up to $10^{11}$. These come from a segmented sieve, `segomega.c`, which reproduces the direct counts of `omgrid.c` up to $10^{9}$ exactly. Above that it uses $P(y) \le \pi(y) + 2\sqrt{y}$ with Dusart's bound for $\pi$. It evaluates Lemma 8.8 on the same grid up to $10^{18}$, binning both sums and rounding every argument up to the next grid point. Since each $N_j$ is nondecreasing, this gives upper envelopes. As a check, the same computation started from exact counts at $10^{7}$ stays above the exact counts at every grid point up to $10^{9}$.

Write $K_k(N)$ for the smaller of the Rankin and envelope bounds on $\#\{n \le N : \omega(n) \ge k\}$, with $K_k(N) = 0$ when $k > \omega^*(N)$. There are two cases.

- **Case I: $A'$ is inside neither $C_7$ nor $C_{18}$.** Run the argument of Sections 8.2–8.4 on $A'$, choosing every witness in $A'$. Then $\omega(b) \le k - 1$, so in Section 8.5 the factors $2^{\omega^*(N)+1}$ and $2^{\omega_1^*(N)}$ become $2^{k}$ and $2^{k-1}$. Call the resulting error $E_k(N)$. Then $|A| \le N/50 + E_k(N) + K_k(N)$.
- **Case II: $A' \subseteq C_7$, say.** Since $A \not\subseteq C_7$, some $b \in A''$ lies outside $C_7$, and $A \setminus C_7 \subseteq A''$. A single cell outside $C_7$ forces at most 12 of the 36 residues of $C_7 \bmod 36$: one row of weight $9$ and one column of weight $4$, which overlap in one cell. So, as in Lemma 2.2, $|A \cap C_7| \le g_1N + E_{II}(N)$. Here $g_1 = (1/3 + (2/3)\beta^{+})/25 = 0.014697 < 1/50$, and $E_{II}(N) = 36 + 36\pi(Y) + L_C$, where $L_C$ is Lemma 3.5's bound with the worst-case factor $2^{\omega_1^*(N)}$. Then $|A| \le N/50 + E_{II}(N) + K_k(N) - (1/50 - g_1)N$.

Two further facts help at moderate $N$, both because every element of $A$ lies in $V$.

- **Counting inside $V$.** Let $V_P$ be the part of $V$ that comes from primes $p \le P = 10^{5}$, that is, the $n$ with $p^2 \mid n^2 + 1$ for some such $p$. The sieve also counts the $n \in V_P$ with $\omega(n) \ge k$ exactly, up to $10^{11}$. The rest of $V$ comes from primes $p > P$ with $p \equiv 1 \pmod{4}$, and has at most $2N\sum_{p>P} p^{-2} + 2\pi(Y')$ elements up to $Y'$, plus the bound of Lemma 3.4 beyond $Y'$. Inside $V$ the count of elements with many prime factors is about fourteen times smaller than over all integers.
- **The bound $|A| \le |V \cap [N]|$.** This replaces the trivial bound $|A| \le N$. Up to $10^{11}$ the sieve gives $|V \cap [N]|$ directly. Beyond that, inclusion–exclusion over the eleven primes $p \le 100$ with $p = 5$ or $p \equiv 1 \pmod{4}$ gives at most $0.10359N + 3^{11}$; Lemma 3.3 covers $100 < p \le Y'$, and Lemma 3.4 the primes beyond. At $10^{11}$ this formula gives $1.0549\cdot 10^{10}$, against an exact count of $1.0531\cdot 10^{10}$.

Taking $k = \omega^*(N) + 1$ recovers Section 8.5. The script `explicitC_omega4.py` uses the grid of Section 8.5, refined to ratio $10^{0.01}$ from $10^{5}$ to $10^{25}$. For each cell it takes the better of two bounds. One is $|A| \le |V \cap [N]|$. The other, for the best $k$, is the two cases above, using the smallest available bound on the elements with $\omega \ge k$. It gives $C \le 29.9$, attained near $N = 10^{13.33}$ with $k = 8$. Hence $C = 30$ works in Theorem 8.1. For comparison, Rankin's bound alone gives $C \le 92.4$ (`explicitC_omega.py`).

The bound $|A| \le |V \cap [N]|$ decides $C$ up to about $10^{13}$. Beyond that the refined argument decides it; where $C$ is decided, about $10^{13}$ to $10^{18}$, $k$ is between $8$ and $11$. The worst cell lies just past the range where the bound $|A| \le |V \cap [N]|$ decides $C$. So extending the sieve, or an explicit bound for integers with many prime factors in the classes $\pm\iota_p \bmod p^2$, would lower $C$ further.

### 8.7 Third-order structure

Write $F' = \{n \equiv 7 \pmod{25},\ n \equiv 3 \pmod{4}\} \cup \{n \equiv 18 \pmod{25},\ n \equiv 1 \pmod{4}\}$ for the mirror image of $F$.

**Theorem 8.9.** Let $N \ge 10^{23.6}$. If $A \subseteq [N]$ is valid, not contained in $C_7$ or $C_{18}$, and $|A| \ge (1/50 - 0.0008)N$, then $A \subseteq F$ or $A \subseteq F'$. The same holds with $0.0005$ in place of $0.0008$ for $N \ge 10^{22.3}$.

So near the second-best density there is no room to move. A near-extremal set is $F$ or $F'$ with some elements removed; nothing can be added.

**Lemma 8.10 (strict gap).** With $\beta = 0.05114$ and $j = 0.01577$, every admissible core $K$ other than those of $F$ and $F'$ has $U(K) \le 1/50 - 0.0010542$. The runner-up is the core of $F$ with one cell of weight $1$ removed, which costs exactly $(1 - \beta)/900$.

*Proof.* `lamgap.c`, a variant of `lamcert.c`, finds this by enumerating all 51,223 admissible cores in exact integer arithmetic. `LamGap.lean` proves the statement in the Lean kernel, again with `decide` only. The argument is the closure argument of Proposition 8.6. If a core's closure is not the core of $F$ or $F'$, the $64 \times 64$ check bounds it. If the closure is $F$'s but the core is smaller, the core misses a cell of weight at least $1$. ∎

*Proof of Theorem 8.9.* The constants of Lemma 8.10 are at least $\beta^{+}$ and $j^{+}$ (Lemma 8.4). So Lemma 8.5 gives $|A| \le U(K)N + E(N)$, where $K$ is the core of $A$ and $E(N)$ is the error of Section 8.5. The script `thirdorder.py` checks on the grid of Section 8.5 that $E(N) < (0.0010542 - \delta)N$ for every $N \ge N_2(\delta)$. It finds $N_2 = 10^{23.56}$ for $\delta = 0.0008$ and $N_2 = 10^{22.27}$ for $\delta = 0.0005$, with the tail beyond $10^{601}$ handled as in Section 8.5. Then $U(K) > 1/50 - 0.0010542$, so $K$ is the core of $F$ or of $F'$; say $F$.

Every type of $A$ is forced by every type of this core. A $C_7$ cell forced with every $C_{18}$ cell $\equiv 3 \pmod{4}$ must be $\equiv 1 \pmod{4}$, because the cell with $3 \mid a$ forces nothing through $9$. Symmetrically, a $C_{18}$ cell must be $\equiv 3 \pmod{4}$. An $R$-type would have to be forced with the cells $\equiv 1$ and $\equiv 3 \pmod{4}$ that have $3 \mid a$, through $4$ alone, which no residue $\mathrm{mod}\ 4$ allows. So every type of $A$ is a type of $F$, and $A \subseteq F$. ∎

The threshold is large for two reasons: the gap is small, and the error of Section 8.5 decays only like $N^{-1/3+o(1)}$. The $\omega$-refinement of Section 8.6 does not transfer directly. It would only show that $A$ lies in $F$ apart from at most $K_k(N)$ exceptional elements.

## 9. Further results

A companion paper \[14\] tests how far the method reaches. It proves counting lemmas for $ab + c$ with any squarefree $c$, and uses them in three directions:

- **Higher powers.** For $ab + 1$ never $k$-free, the maximum is a class $\mathrm{mod}\ 5^k$ for every $k \ge 3$ and large $N$, with an explicit threshold. For $3 \le k \le 100$ this holds for every $N$, with two small exceptions; for cubes the maximisers are listed for every $N$.
- **Other forms.** For $ab + c$ never squarefree, the maximum for large $N$ is a root class of $x^2 + c \equiv 0 \pmod{p^2}$, for 49 squarefree $c \le 100$.
- **The third density.** The densest valid set not inside $C_7$, $C_{18}$, $F$ or $F'$ has density between $1/25 - 1/(4\pi^2) = 0.01467$ and $0.01491$, so for large $N$, Theorem 8.9 holds with $0.0192$ replaced by $0.01491$.

## 10. Open problems

1. **Third-order structure.** Theorem 8.9 settles this for $N \ge 10^{23.6}$: a valid set not inside one class with at least $(1/50 - 0.0008)N$ elements lies inside $F$ or its mirror. Does this hold for much smaller $N$, with an explicit $\delta$? The exact maximisers for $N \le 1006$ (Section 7, proof of Theorem C(2)) are small sets unrelated to $F$, so some lower bound on $N$ is needed.
2. **Sharper large-prime counts.** Brute force shows that Lemmas 3.4 and 3.5 overestimate by a factor of about 38 or more (worst ratio $0.026$). Averaging $\rho_b(m)$ over short ranges of $m$, using explicit Burgess- or Weil-type bounds, should lower $N_0$ substantially, make the $\omega$-refinement unnecessary, and shrink the constant $C$ of Theorem 8.1.
3. **A general witness-game theorem.** The companion paper \[14\] carries the method to higher powers and to $ab + c$ for many $c$, each by a separate computation. Is there a single theorem: a self-forcing class plus a positive local gap implies extremality for all large $N$, with an effective threshold? The companion paper also asks for the exact third density, conjectured to be $1/25 - 1/(4\pi^2)$.
4. **Formalisation.** The constructions (`Erdos848Constructions.lean`), the certificate of Proposition 8.6 (`LamCert.lean`) and the strict gap of Lemma 8.10 (`LamGap.lean`) are verified in Lean. Natural next targets are Proposition 8.2, which is short, and the counting lemmas of Section 3.

## Appendix: verification and reproducibility

All code is plain C (gcc -O3, optionally -fopenmp) or Python 3 with numpy, sympy, networkx and scipy. Each computational claim for Theorems A–D has at least two independent checks.

| Claim | Primary computation | Independent check |
| --- | --- | --- |
| Theorem A and C(2), $N \le 1006$ | `nsc.py` (exact cliques by case) | maximum clique at $N \equiv 6 \pmod{25}$ up to 3806, `e848b.py`; maximal-clique enumeration for $N \le 106$ |
| Theorem A and C(2), $1006 < N \le 6.9\cdot 10^{6}$ | `fast848.c` with `STRICT=1`, 859 blocks | `e848cases.c` (different algorithm) to $10^{6}$; numpy brute force `alledges.py`; `sbrute.py` (direct $d^2$ sieve) matches $S_1$–$S_4$ at all 168 edges $\le 20{,}000$ and on the tightest block one $N$ at a time; non-strict run to $10^{7}$ (794 blocks) |
| $V_2$ values | exact integer branch-and-bound, `bb.c`, all 16 parameter pairs | MILP, `vk2.py` (HiGHS) |
| Lemma 3.5 constants $\lambda$, $c$ | `mconst2.py` | `mc.py` (brute-force $\rho$) |
| Lemmas 3.4 and 3.5 | proofs above | brute force at $N \le 3\cdot 10^{5}$, `brute.py` / `brute2.py`: no violations, worst ratio actual/bound $0.026$ |
| Grid, $N \ge 6.7838\cdot 10^{6}$ | `cellsbig.py` / `cellsbig2.py`, $(17, 13)$, $[6.7838\cdot 10^{6}, 10^{60}]$ | `tmgrid.py`, parameters optimised per cell, 2525 cells on $[10^{7}, 10^{60}]$ |
| $\omega$-counts $K_k(N)$ | `omegaV.c` | `kom.c` |
| Proposition 5.1 | closed form above | `tail60.py` |

Further independent checks:

| Claim | Computation | Result |
| --- | --- | --- |
| Li's uniform-degree proposition, $5\cdot 10^{6} \le N \le 10^{7}$ | `fastli.c` (exact $H_7$, $H_{18}$ for all $b$; 70 blocks of 1%, 56 min) | holds on every block; minimum margin 13.8% (threshold taken at the top of each block); brute-force cross-check at $N = 20{,}000$ |
| Theorem D and the constructions | `Erdos848Constructions.lean`, Lean 4.36.0-rc2 with Mathlib | compiles; no `sorry`; only the standard axioms |
| Densest congruence-defined set not inside one class | `wgame4.py` (exact cliques mod 900) | $1/50$, attained by $F$; exact integer certificate of the full game: lamcert.c (51,223 cores); kernel-checked reduced certificate: LamCert.lean (64 closed sets, 439 pairs); third-order gap: lamgap.c, LamGap.lean, thirdorder.py; explicit $C = 30$: explicitC\_omega4.py, with exact counts to $10^{11}$ from segomega.c ($C = 92.4$ with Rankin's bound alone: explicitC\_omega.py; $C = 170$ without the $\omega$-refinement: explicitC.py) |

The full package (code, logs and certificates) accompanies this paper.

## References

1. T. F. Bloom, [Erdős Problem #848](https://www.erdosproblems.com/848), erdosproblems.com, and the [discussion thread](https://www.erdosproblems.com/forum/thread/848).
2. M. Sawhney, [Problem 848](https://www.math.columbia.edu/~msawhney/Problem_848.pdf), note.
3. W. van Doorn, upper bound $(0.108\dots + o(1))N$, as recorded at reference 1.
4. J. B. Rosser and L. Schoenfeld, Approximate formulas for some functions of prime numbers, Illinois J. Math. 6 (1962), 64–94.
5. G. Robin, Estimation de la fonction de Tchebychef $\theta$ sur le $k$-ième nombre premier et grandes valeurs de la fonction $\omega(n)$ nombre de diviseurs premiers de $n$, Acta Arith. 42 (1983), no. 4, 367–389, doi:10.4064/aa-42-4-367-389.
6. P. Dusart, Inégalités explicites pour $\psi(X)$, $\theta(X)$, $\pi(X)$ et les nombres premiers, C. R. Math. Rep. Acad. Sci. Canada 21 (1999), no. 2, 53–59. This is the source of $\pi(x) \le (x/\ln x)(1 + 1/\ln x + 2.51/\ln^2 x)$ for $x \ge 355991$.
7. B. Alexeev, D. G. Mixon and W. Sawin, [The independence and clique cover numbers of the squarefree graph](https://arxiv.org/abs/2507.01928) (2025), for the companion problem where $ab$ is never squarefree.

8) A. C. Li, *The Exact Extremal Bound in Erdős Problem 848*, August 2026 ([SSRN 7230480](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7230480); [code and Lean](https://github.com/crabsatellite/erdos-848-squarefree-product)). Uses a Hall-matching reformulation relative to $C_7$, a prefix colouring for $N \le 5\cdot 10^{6}$, and case-wise pivot estimates beyond that. Claims a complete Lean 4 verification.
9) N. Sothanaphan, explicit threshold $N_0 = 2.64\cdot 10^{17}$ for Sawhney's theorem (2026), as cited in reference 8.
10) I. Pitchford (with OpenAI Codex), [Candidate certificate-backed all-N determination for Erdős Problem 848](https://zenodo.org/records/21647629), Zenodo, July 2026.
11) B. Zanghi, [erdos-848](https://github.com/bzanghi/erdos-848), and N. Durfee, [erdos-848-verification](https://github.com/AstroCat93/erdos-848-verification), GitHub, 2026.

12. R. Jung et al., [erdos-banger](https://github.com/The-Obstacle-Is-The-Way/erdos-banger), Lean 4 formalisation of Sawhney's stability theorem for Problem 848 ($\eta = 1/2000$, ineffective $N_0$), January 2026.
13. M. Sawhney and M. Sellke, in *Early science acceleration experiments with GPT-5*, [arXiv:2511.16072](https://arxiv.org/abs/2511.16072), Section IV.1 (Problem 848).

14) L. Culpitt, *The witness game beyond Erdős Problem 848: higher powers, $ab + c$, and the third density*, companion paper (2026); code in the repository [Erdos-848](https://github.com/MeaCulpitt/Erdos-848).

## Acknowledgements

The argument, code and certificates were developed with AI assistance (Claude) and checked by independent re-implementation. Every computation above can be re-run from the accompanying package. We thank the contributors to the forum thread for Problem 848, especially W. van Doorn, D. Weisenberg, StijnC, B. Alexeev, M. Sawhney and N. Sothanaphan, whose comments shaped this work. We welcome expert review, especially of Sections 3–5 and 8.
