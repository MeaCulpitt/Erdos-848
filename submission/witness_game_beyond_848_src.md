# The witness game beyond Erdős Problem 848: higher powers, ab + c, and the third density

Luke Culpitt (AI assisted)

## Abstract

Erdős Problem 848 asks for the largest $A \subseteq \{1, \dots, N\}$ with $ab + 1$ never squarefree. The answer is the class $7 \bmod 25$. In a companion paper [M] we proved this for every $N$ by a finite "witness game" on residue types. That paper also determined the second-best density, $1/50$, attained by a two-class set $F$. Here we test how far the method reaches.

- **Higher powers.** For $ab + 1$ never $k$-free, the maximum is a class $\mathrm{mod}\ 5^k$ for every $k \ge 3$ and all large $N$, with an explicit threshold. For $3 \le k \le 100$ this holds for every $N$, with exactly two small exceptions, at $k = 3$ and $k = 4$. For cubes the maximisers are listed for every $N$.
- **Other forms.** For $ab + c$ never squarefree, the maximum for large $N$ is a root class of $x^2 + c \equiv 0 \pmod{p^2}$. This holds for 49 squarefree $c \le 100$, and for 33 of them the second-best density is also determined. The counting lemmas needed for general $c$ are proved here.
- **The third density for 848.** The densest valid set not inside a class, $F$ or $F$'s mirror has density between $1/25 - 1/(4\pi^2) = 0.014670$ and $0.014910$. The lower bound is one class plus one outsider, and we conjecture that it is sharp.

The computations use exact clique search and CP-SAT with rounded-up objective coefficients. All code is public.

## 1. Introduction

Call $A \subseteq [N]$ *valid* if $ab + 1$ is not squarefree for all $a, b \in A$, including $a = b$. The class $C_7 = \{n \equiv 7 \pmod{25}\}$ is valid, since $7^2 + 1 = 50$. In [M] we proved that it is the largest valid set for every $N$, together with stability and rigidity results and the second-best density.

The method of [M] has three ingredients:

- a *self-forcing class*: a residue class in which $ab + 1$ is always divisible by a fixed square;
- a *positive local gap*: a finite game on residue types showing that any valid set not inside such a class is smaller by a constant factor;
- *control of large primes*: counting lemmas showing that squares $p^2$ with $p$ large contribute $o(N)$, uniformly in the witness.

This paper asks how special these are to $x^2 + 1$ and to squares. Section 2 proves the counting lemmas for $ab + c$ with a general squarefree $c \ge 1$. Section 3 uses them, with $c = 1$, to bracket the third density of 848. Section 4 treats higher powers, and Section 5 the forms $ab + c$.

We use the notation of [M] throughout. A *type* is a set of residue classes modulo a fixed modulus $L$. Type $s$ *forces* type $t$ if some fixed square divides $ab + c$ for every $a \in t$ and $b \in s$. A type is *self-forcing* if it forces itself. For a set $A$, $P$ is the set of types it meets, its *core* $K$ is the set of types in $P$ forced by every type in $P$, and $F(K)$ is the set of types forcing every member of $K$. Forcing is symmetric, so $P \subseteq F(K)$.

## 2. Counting lemmas for $ab + c$

Fix a squarefree $c \ge 1$ and a modulus $L$. The *layer primes* are the primes $p$ whose squares are built into the types, through $L = 36\cdot\prod p^2$ or similar. Every other prime $q$ is a *luck prime*. For a luck prime $q$, the event $q^2 \mid ab + c$ is not decided by the types and is counted directly.

**Lemma 2.1 (large luck primes).** Let $1 \le b \le N$ and $Y \ge c$. Then

$$\#\{a \le N : q^2 \mid ab + c \text{ for some prime } q > Y\} \le c\cdot 2^{\omega(b)+\omega(c)+1}\cdot\left(2(N + c)/Y + (N^2 + c)/Y^2\right).$$

*Proof.* Let $q > Y$ have $q^2 \mid ab + c$. Then $q \nmid c$, since $q > c$, and so $q \nmid b$. Write $ab + c = mq^2$, so that $1 \le m \le M = (bN + c)/Y^2$ and $mq^2 \equiv c \pmod{b}$.

Count the units $s \bmod b$ with $ms^2 \equiv c \pmod{b}$ prime power by prime power. Let $\ell^e \parallel b$.

- If $\ell \nmid c$, then $\ell \nmid m$, and $s^2 \equiv cm^{-1}$ has at most $2$ solutions $\mathrm{mod}\ \ell^e$ (at most $4$ if $\ell = 2$).
- If $\ell \mid c$, then $\ell \parallel c$ because $c$ is squarefree, and $\ell \mid m$. For $e = 1$ every unit works, which gives fewer than $\ell$ solutions. For $e \ge 2$, write $m = \ell m'$ and $c = \ell c'$. Then $m's^2 \equiv c' \pmod{\ell^{e-1}}$ with $c'$ a unit, which has at most $4$ solutions $\mathrm{mod}\ \ell^{e-1}$, so at most $4\ell \bmod \ell^e$.

So $q$ lies in at most $c\cdot 2^{\omega(b)+\omega(c)+1}$ classes $\mathrm{mod}\ b$. Since $q \le \sqrt{(bN + c)/m}$, each $m$ contributes at most $c\cdot 2^{\omega(b)+\omega(c)+1}\left(\sqrt{(bN + c)/m}/b + 1\right)$. Summing over $m \le M$ with $\sum m^{-1/2} \le 2\sqrt{M}$ gives $c\cdot 2^{\omega(b)+\omega(c)+1}\left(2(bN + c)/(bY) + M\right)$. This is at most the bound stated, since $1 \le b \le N$. ∎

For $c = 1$ this is Lemma 8.3 of [M]. With $Y = N^{0.6}$ it is $N^{0.8+o(1)}$, uniformly in $b \le N$, because $2^{\omega(b)} = N^{o(1)}$.

**Lemma 2.2 (one witness).** Let $t$ be a type of density $w_t$ and let $b \le N$. For each luck prime $q$, let $d_q(t, b)$ be the relative density in $t$ of the $a$ with $q^2 \mid ab + c$. This density is determined by the classes of $b \bmod L$ and $\mathrm{mod}\ q^2$. Then, uniformly in $b \le N$,

$$\#\{a \in t \cap [N] : q^2 \mid ab + c \text{ for some luck prime } q\} \le w_t\cdot\left(1 - \prod_q (1 - d_q(t, b))\right)\cdot N + o(N),$$

and also $\le w_t\cdot\sum_q d_q(t, b)\cdot N + o(N)$.

The densities $d_q(t, b)$ are as follows.

- For a luck prime $q \nmid cL$:
  - if $q \nmid b$, $a$ must lie in the single class $-cb^{-1} \bmod q^2$, so $d_q = 1/q^2$;
  - if $q \mid b$, then $ab + c \equiv c \not\equiv 0 \pmod{q}$, so $d_q = 0$.
- For a luck prime $q \mid c$, the type records whether $q \mid a$. Then $q^2 \mid ab + c$ needs $q$ to divide exactly one of $a$ and $b$.
  - If $q \mid b$ and $q \nmid a$, then $a$ lies in one nonzero class $\mathrm{mod}\ q$, so $d_q = 1/(q - 1)$.
  - If $q \mid a$ and $q \nmid b$, then $a/q$ lies in one class $\mathrm{mod}\ q$, so $d_q = 1/q$.
  - In the other two cases, $d_q = 0$.
- For a luck prime $q$ whose root classes are recorded in the types (as in Sections 3 and 5):
  - if $a$ lies in a root class $R$ and $b$ does not, then $d_q = 0$, because $ab \equiv -c \pmod{q^2}$ would put $b$ in $R$;
  - if $a$ lies in no root class, then $-cb^{-1}$ is one of the $q^2 - 2$ remaining classes, so $d_q \le 1/(q^2 - 2)$.

*Proof.* Fix $Q$. For the luck primes $q \le Q$, the events are conditions on $a$ modulo $L\cdot\prod_{q\le Q} q^2$. By the Chinese remainder theorem, the count is exact up to $O(1)$ per class, where the implied constant depends on $Q$. This gives the product for $q \le Q$, and the union bound gives the sum.

For $Q < q \le Y$ with $Y = N^{0.6}$, each $q$ contributes at most $N/q^2 + 1$, or $N/q + 1$ when $q \mid c$; but $q \mid c$ means $q \le c \le Q$ once $Q \ge c$. So these primes contribute at most $N/Q + \pi(Y)$. For $q > Y$ use Lemma 2.1. Letting $Q \to \infty$ slowly with $N$, the total error is $o(N)$, uniformly in $b$. ∎

**Lemma 2.3 (large primes in $x^2 + c$).** For every $Q \ge 1$,

$$\#\{x \le N : p^2 \mid x^2 + c \text{ for some prime } p > Q\} \le (2/Q)\cdot N + 2\pi\left(\sqrt{N^2 + c}\right) = (2/Q)\cdot N + O(N/\log N).$$

*Proof.* If $p \mid c$ then $p^2 \nmid x^2 + c$: $p \mid x$ would give $p^2 \mid x^2$, and $c$ is squarefree. So $p \nmid c$, and $x^2 \equiv -c \pmod{p^2}$ has at most two roots. Each root class meets $[N]$ in at most $N/p^2 + 1$ elements, and $p \le \sqrt{N^2 + c}$. Sum over $p > Q$, using $\sum_{p>Q} 1/p^2 \le 1/Q$. ∎

For $c = 1$, [M] used Pell's equation to get a power saving here. For an asymptotic statement this cruder bound suffices, and it holds for every $c$.

**Lemma 2.4 (joint estimate with the own witness).** Let $t$ be a type that is not self-forcing, and let $b \in t$. Write $V_c = \{x : x^2 + c \text{ not squarefree}\}$, and $\rho_p$ for the number of roots of $x^2 \equiv -c \pmod{p^2}$. Suppose $t$ records, for each luck prime $q \mid c$, whether $q \mid a$. Then, uniformly in $b \le N$,

$$\#\{a \in t \cap [N] : a \in V_c,\ ab + c \text{ not squarefree}\} \le w_t\cdot(\alpha_t\cdot\beta^0_t + \kappa_t)\cdot N + o(N),$$

where

- $\alpha_t$ is the relative density in $t$ of the $a$ that have $p^2 \mid a^2 + c$ for some luck prime $p$, bounded by the union bound $\sum \rho_p/p^2$ (a luck prime whose root classes are recorded contributes nothing here, since $t$ is not self-forcing and so lies outside them);
- $\beta^0_t = \sum d_q(t, b)$ over luck primes $q \nmid c$;
- $\kappa_t = \sum 1/p^2$ over the luck primes $p$ with $\rho_p = 2$.

*Proof.* Since $t$ is not self-forcing and $b \in t$, the layer primes force nothing between $a$ and $b$. So $a \in V_c$ needs $p^2 \mid a^2 + c$ for some luck prime $p$, and $ab + c$ not squarefree needs $q^2 \mid ab + c$ for some luck prime $q$.

A luck prime $q \mid c$ contributes nothing. The elements $a$ and $b$ lie in the same type, so $q$ divides both or neither. If $q$ divides both, $ab + c \equiv c \pmod{q^2}$ and $q \parallel c$. If $q$ divides neither, $ab + c \equiv ab \not\equiv 0 \pmod{q}$.

Fix $Q$ and consider $p, q \le Q$. For $p \ne q$, the Chinese remainder theorem gives the product of the densities. For $p = q$, $a$ must lie in a root class $\mathrm{mod}\ p^2$ and in the class $-cb^{-1} \bmod p^2$. The two root classes are distinct, so this leaves at most one class, and contributes $1/p^2$. Up to the CRT errors, this gives $w_t(\alpha_t \beta^0_t + \kappa_t)N$.

For $p > Q$, drop the condition on $q$ and use Lemma 2.3. For $q > Q$, drop the condition on $p$ and use the tail of Lemma 2.2. Let $Q \to \infty$. ∎

**Lemma 2.5 (core reduction).** Let $A \subseteq [N]$ be $c$-valid, meaning $ab + c$ is not squarefree for all $a, b \in A$. Let $P$ be the set of types $A$ meets, with core $K$. Suppose that for each type $t$ there is a constant $b_t$ with these properties:

- if $t$ is self-forcing, $b_t$ is at least the luck density of Lemma 2.2 for every witness that does not force $t$;
- otherwise, $b_t$ is at least the constant of Lemma 2.4.

Then

$$|A| \le U(K)\cdot N + o(N), \quad \text{where } U(K) = w(K) + \sum_{t \in F(K) \setminus K} b_t\cdot w_t.$$

*Proof.* As in [M, Lemma 8.5]. Every element of $A$ is compatible with every other. A self-forcing type $t \in P \setminus K$ is not forced by some $s \in P$, so any element of $A \cap s$ is a witness for Lemma 2.2. A type that is not self-forcing uses an element of itself as the witness for Lemma 2.4. Core types count in full. Since $P \subseteq F(K)$, summing over $t \in P$ gives the bound. The number of types is fixed, so the $o(N)$ terms add up to $o(N)$. ∎

Maximising $U(K)$ over the cores that a given family of sets can have is a finite problem. We solve it with CP-SAT [OR-tools], with every objective coefficient rounded up to a multiple of $10^{-9}$, so the reported optimum is an upper bound.

The variables are as follows. A *slab* is a residue class for the layers other than $4$ and $9$, together with the root-class memberships described below. A *cell* is a residue mod 36, together with the divisibility flags. Then $K$ is given by a closed set of cells in each slab, and $F(K)$ by its intersections, exactly as in [M, Section 8.4]. The code is `coregame.py`.

## 3. The third density of Problem 848

Let $F = \{7 \bmod 25, 1 \bmod 4\} \cup \{18 \bmod 25, 3 \bmod 4\}$ and let $F'$ be its mirror image. In [M] we showed that every valid set not inside $C_7$ or $C_{18}$ has at most $N/50 + O(N^{0.81})$ elements, and that $F$ and $F'$ attain this. We also showed that for $N \ge 10^{23.6}$, a valid set not inside a class with at least $(1/50 - 0.0008)N$ elements lies in $F$ or $F'$. Let $\lambda_3(N)$ be the largest size of a valid $A \subseteq [N]$ contained in none of $C_7$, $C_{18}$, $F$ and $F'$.

**Theorem 3.1.**
1. $\liminf \lambda_3(N)/N \ge 1/25 - 1/(4\pi^2) = 0.0146697\dots$.
2. $\limsup \lambda_3(N)/N \le 0.014910$.

So for all large $N$, a valid set with more than $0.01491N$ elements lies inside $C_7$, $C_{18}$, $F$ or $F'$. This sharpens the density $1/50 - 0.0008 = 0.0192$ of [M, Theorem 8.9] to $0.01491$, though without an explicit threshold for $N$.

*Proof of (1).* Take a prime $x > 3$ with $x \equiv 18 \pmod{25}$ and $x \equiv 3 \pmod{4}$, and let

$$A = \{x\} \cup \{a \in C_7 \cap [N] : ax + 1 \text{ not squarefree}\}.$$

Pairs inside $C_7$ are forced by $25$. Also $x^2 + 1 \equiv 0 \pmod{25}$, and pairs with $x$ hold by definition, so $A$ is valid. It contains $x \in C_{18}$ and elements of $C_7$ that are $\equiv 1$ and $\equiv 3 \pmod{4}$, so it lies in none of the four sets.

For $a \in C_7$ we have $ax + 1 \equiv 2 \pmod{25}$, so $25$ never divides $ax + 1$. Among the $a \in C_7$:

- $4$ divides $ax + 1$ for one class of $a \bmod 4$;
- $9$ divides it for one class $\mathrm{mod}\ 9$;
- $p^2$ divides it for one class $\mathrm{mod}\ p^2$, when $p \ge 7$ and $p \ne x$;
- $x^2$ never divides it.

So the $a \in C_7$ with $ax + 1$ squarefree have density

$$(1/25)\cdot(3/4)\cdot(8/9)\cdot\prod_{p\ge 7,\, p\ne x}(1 - p^{-2}) = (1/(4\pi^2))\cdot(1 - x^{-2})^{-1},$$

using $\prod_{p\ge 7}(1 - p^{-2}) = (6/\pi^2)\cdot(4/3)\cdot(9/8)\cdot(25/24) = 75/(8\pi^2)$. Hence $|A|/N \to 1/25 - (1/(4\pi^2))(1 - x^{-2})^{-1}$ as $N \to \infty$, and letting $x \to \infty$ gives (1). The script `lam3_lower.py` checks the count: $0.014671$ at $N = 2\cdot 10^{7}$ with $x = 100043$. ∎

This is the "one class plus one outsider" configuration. The outsider forces exactly a third of $C_7$, through $4$ and $9$ [M, Lemma 2.2]. The other two thirds survive only where $ax + 1$ picks up a square factor by chance. Its density is the sharp constant $g_1^*$ of [M, Theorem C(1)].

*Proof of (2).* Apply Lemma 2.5 with $c = 1$ and the following types:

- the class mod 25;
- the cell mod 36;
- membership in the classes $S_p^\pm = \{a \equiv \pm\iota_p \pmod{p^2}\}$ for $p = 13$ and $17$, where $\iota_p^2 \equiv -1$.

Two elements of the same $S_p^\sigma$ are forced. An element of $S_p^\sigma$ and one outside it never have $p^2 \mid ab + 1$, since $ab \equiv -1 \pmod{p^2}$ would put the second element in $S_p^\sigma$ too. Inside the complement of $S_p^\pm$, the prime $p$ acts as a luck prime with density $1/(p^2 - 2)$. So the luck primes are $q \ge 7$, and the types outside $C_7 \cup C_{18} \cup S_{13}^\pm \cup S_{17}^\pm$ are in $V$ only through primes $p \ge 29$.

The constants are as follows.

- For self-forcing types, $b_t = 1 - \prod(1 - q^{-2})$, with the product over $7 \le q \le 10^{7}$ and the factor for $p = 13, 17$ replaced by $1 - 1/(p^2 - 2)$, plus $\sum_{q>10^{7}} q^{-2}$. This is $0.0502$.
- For the remaining types, $b_t$ is the Lemma 2.4 constant, $0.0050$. It was $0.0158$ for the unrefined $R$-types of [M].

The admissible cores are those whose $F(K)$ has a type outside each of $C_7$, $C_{18}$, $F$ and $F'$. Maximising $U$ over them is a problem on 225 slabs × 21 cells. `third_cp.py` solves it to optimality and finds $0.0149093$. ∎

The optimal core is the class-plus-outsider core: twelve cells of one class, all forced by a single cell. So the game identifies the right configuration, and the gap of $0.00024$ to the construction has two sources.

- Most of it comes from elements of the outsider's cell, in the other classes mod 25, that lie in $V$ through primes $p \ge 29$. This part shrinks as more classes $S_p$ are split off: the bound is $0.0149645$ with $S_{13}$ alone.
- The rest, $\beta/900 \approx 0.000056$, is the outsider cell itself. The game charges it at rate $\beta$, although the construction has a single element there.

Closing the second part needs a bound for pairs of sets $X, Y$ with $xy + 1$ never squarefree that is better than one witness on each side.

The unrefined enumeration of [M, Section 8.4] gives only $0.0186$ here (`third.py`). In that version the $R$-types carry the full constant $\kappa = \sum_{p\equiv 1 (4),\, p\ge 13} p^{-2} = 0.0138$ from the coincidence $p = q$, which the refinement removes.

**Conjecture 3.2.** $\lambda_3(N)/N \to 1/25 - 1/(4\pi^2)$.

## 4. Higher powers

### 4.1 Cubes

Call $A \subseteq [N]$ *cube-valid* if $ab + 1$ is not cube-free for all $a, b \in A$, including $a = b$. Write $V_3 = \{x : x^2 + 1 \text{ not cube-free}\}$. Since $57^2 + 1 = 2\cdot 5^{3}\cdot 13$, the classes $57$ and $68 \bmod 125$ are cube-valid, playing the role of $7$ and $18 \bmod 25$. Write $c_{57}(N) = \#\{n \le N : n \equiv 57 \pmod{125}\}$.

**Theorem 4.1.** For every $N$, every cube-valid $A \subseteq [N]$ has $|A| \le c_{57}(N)$. Equality holds exactly in the following cases:

- $A = C_{57} \cap [N]$;
- $A = C_{68} \cap [N]$, when $c_{68}(N) = c_{57}(N)$;
- for $193 \le N \le 306$, also $A = \{182, 193\}$;
- for $239 \le N \le 306$, also $A = \{57, 239\}$ and $A = \{193, 239\}$.

The exceptional sets work through $8$ and $27$: $182\cdot 193 + 1 = 3^{3}\cdot 1301$, $57\cdot 239 + 1 = 2^{3}\cdot 13\cdot 131$ and $193\cdot 239 + 1 = 2^{4}\cdot 3\cdot 31^{2}$. Locally the picture is the same as for 848. The densest congruence-defined cube-valid set not inside one class is $\{57 \bmod 125, 1 \bmod 8\} \cup \{68 \bmod 125, 7 \bmod 8\}$, of density $1/500$ (`wgame4.py`).

The proof is much shorter than for 848, for two reasons. The local gap is far larger, so a single witness suffices and the full game is not needed. And a cube $q^3 > N^2 + 1$ can never divide $ab + 1$, so no lattice lemma is needed either.

**Lemma 4.2 (one witness).** Let $A$ be cube-valid, and suppose some $b \in A$ lies outside $C_{57}$. Then

$$|A \cap C_{57}| \le (N/125)\cdot(1/8 + 1/27 + \beta_3) + 2 + \pi((N^2 + 1)^{1/3}), \quad \text{where } \beta_3 = \sum_{q\ge 7} q^{-3} \le 0.004726,$$

and the same holds for $C_{68}$.

*Proof.* Since $b \notin C_{57}$, $125$ never divides $ab + 1$ for $a \in C_{57}$. So some prime $q \ne 5$ has $q^3 \mid ab + 1$, which puts $a$ in one class $\mathrm{mod}\ q^3$ (if $q \nmid b$). For $q = 2$ and $q = 3$ this is at most a fraction $1/8$ or $1/27$ of $C_{57}$, at a cost of 1 each. For $q \ge 7$, the class $\mathrm{mod}\ 125q^3$ contains at most $N/(125q^3) + 1$ elements up to $N$. Also $q^3 \le ab + 1 \le N^2 + 1$. ∎

*Proof of Theorem 4.1.* Let $A$ be cube-valid and inside neither $C_{57}$ nor $C_{68}$. Then $A$ has elements outside each class, so Lemma 4.2 applies to both. The remaining elements lie in $V_3$ outside $C_{57} \cup C_{68}$, so each has $p^3 \mid x^2 + 1$ for some $p \equiv 1 \pmod{4}$ with $p \ge 13$. There are at most $2N\sigma_3 + 2\pi((N^2 + 1)^{1/3})$ of them, where $\sigma_3 = \sum p^{-3}$ over primes $p \equiv 1 \pmod{4}$ with $p \ge 13$, so $\sigma_3 \le 0.000756$.

- **Large $N$.** The total main term is $0.004178N$ against $c_{57}(N) > (N - 57)/125 \approx 0.008N$. Checking cells of ratio $1.01$ with exact prime counts to $10^{8}$ and Rosser–Schoenfeld above (`cube_analytic.py`) gives $|A| < c_{57}(N)$ for $1.94\cdot 10^{6} \le N \le 10^{40}$. Beyond $10^{40}$ the error term $4\pi((N^2 + 1)^{1/3}) + 4$ is far below $(0.008 - 0.004178)N$.
- **$700 \le N \le 2\cdot 10^{6}$.** Here `cubeM.c` computes the bound exactly. It finds the maximum over witnesses $b \in V_3 \setminus C_{57}$ of $\#\{a \in C_{57} \cap [N] : ab + 1 \text{ not cube-free}\}$, likewise for $C_{68}$, and adds $|V_3 \cap [N]| - c_{57}(N) - c_{68}(N)$. All three are nondecreasing in $N$. On 20 cells of ratio $1.5$, the bound at the top of each cell stays below $c_{57}$ at the bottom of the cell. At its closest it reaches 89% of $c_{57}$ ($17$ against $19$ on $[2362, 3543]$). A brute-force recomputation by factorisation agrees at $N = 3000$.
- **$N \le 700$.** `cube_maxsets.py` lists all maximum cube-valid sets for every $N$ by an exact clique search. An independent clique computation confirms the maximum $c_{57}(N)$ up to $N = 40{,}000$. ∎

For squares the large-prime events were the main difficulty. For cubes all three ingredients are easy.

### 4.2 General k

Call $A \subseteq [N]$ *$k$-valid* if $ab + 1$ is never $k$-free, for all $a, b \in A$ including $a = b$. Let $q = 5^k$, let $r_k$ be the smaller root of $x^2 \equiv -1 \pmod{q}$, and write $c_k(N) = \#\{n \le N : n \equiv r_k \pmod{q}\}$. For example, $r_3 = 57$, $r_4 = 182$, $r_5 = r_6 = 1068$ and $r_7 = 32318$.

**Theorem 4.3.**
1. For every $k \ge 3$ there is an explicit $N_k$ such that for $N \ge N_k$, every $k$-valid $A \subseteq [N]$ not inside one of the classes $\pm r_k \pmod{q}$ has fewer than $c_k(N)$ elements. So for $N \ge N_k$ the maximum is $c_k(N)$, and only the full classes attain it. Here $N_k/5^k$ is about $15{,}400$ for $k = 3$, $555$ for $k = 4$, at most $214$ for $k \ge 5$, and at most $60$ for $k \ge 40$.
2. For $3 \le k \le 100$ the maximum is $c_k(N)$ for every $N$, and only the full classes attain it, with exactly two exceptions. For $k = 3$ and $193 \le N \le 306$, the mixed sets of Theorem 4.1 also attain it. For $k = 4$ and $239 \le N \le 806$, the set $\{239\}$ also attains the maximum $1$, because $239^2 + 1 = 2\cdot 13^{4}$.

*Proof of part 1.* Lemma 4.2 holds with $2^k$, $3^k$ and $p^k$ in place of $8$, $27$ and $p^3$. A witness outside $C_{r_k}$ forces at most a fraction $Z_k = 2^{-k} + 3^{-k} + \sum_{p\ge 7} p^{-k}$ of that class, plus one element for each prime $p$ with $p^k \le N^2 + 1$. The rest of $V_k$ has at most $2N\sigma_k + 2\pi((N^2 + 1)^{1/k})$ elements, where $\sigma_k = \sum p^{-k}$ over primes $p \equiv 1 \pmod{4}$ with $p \ge 13$. The main term $2Z_k + 2q\sigma_k$ is largest at $k = 3$, where it is $0.52$, and it falls to $0.21$ at $k = 4$ and $0.09$ at $k = 5$.

For $3 \le k \le 40$, `kfree_analytic.py` finds $N_k$ by checking cells of ratio $1.01$. For $k > 40$ and $N = \lambda q$ with $\lambda \ge 60$, the requirement reduces to $\lambda(1 - 10^{-11}) - 1 > 4\pi(25.01\cdot\lambda^{0.05}) + 4$. This holds because the right side is at most $52$ for $\lambda \le 10^{4}$, and grows only like $\lambda^{0.05}$. ∎

*Proof of part 2.* Below $N_k$ the vertex set $V_k \cap [N_k]$ can be listed directly, as the roots of $x^2 \equiv -1 \pmod{p^k}$ for the few primes with $p^k \le N_k^2 + 1$. Testing an edge only needs those same primes. The vertex set is small: 1,143 vertices for $k = 4$, 432 for $k = 5$, and between 90 and 155 for $9 \le k \le 100$. Above $k = 30$ there are no vertices outside the two classes at all.

For $5 \le k \le 100$, `kfree_exact.py` enumerates all maximum cliques at every vertex value up to $N_k$; the graph is constant between consecutive vertices. For $k = 4$ it does this up to $30{,}000$ and then checks the one-witness bound on 14 cells up to $N_4$, where the bound is at most a third of $c_4$. The case $k = 3$ is Theorem 4.1.

The graphs are not trivial: for $k = 5$ there are 844 edges between the two classes and 5 extra vertices. An independent brute force, factorising $x^2 + 1$ and $ab + 1$ directly, reproduces every maximum set for $k = 4$ up to $3000$ and $k = 5$ up to $20{,}000$. ∎

So the extremal answer is the same for every $k \ge 3$: the class $r_k \bmod 5^k$, with occasional small exceptions at the start. Part 2 cannot be checked for all $k$ at once. Whether a stray vertex such as $239$ falls below the second element of the class depends on the particular roots.

The exceptions are not confined to $c_k(N) \le 1$: for $k = 3$ they occur where $c_3(N) = 2$. But they do not recur. Let $\mu_k(N)$ be the size of the largest $k$-valid set in $[N]$ not inside one class. For every $5 \le k \le 300$ and every $N \le N_k$, $\mu_k(N) \le c_k(N) - 3$. The closest approach is $k = 5$ and $N = 13{,}568$, where a mixed pair faces a class of 5 (`margin.py`). For $12 \le k \le 300$ there is no mixed set at all below $N_k$: $V_k \cap [N_k]$ consists of the two classes, with no edge between them.

## 5. The forms ab + c

Fix a squarefree $c \ge 1$, and call $A \subseteq [N]$ *$c$-valid* if $ab + c$ is not squarefree for all $a, b \in A$, including $a = b$. A *root class* is a class $x \bmod p^2$ with $x^2 + c \equiv 0 \pmod{p^2}$. It is self-forcing, because $aa' + c \equiv x^2 + c \equiv 0$ for $a, a'$ in the class.

For $p = 2$, root classes exist exactly when $c \equiv 3 \pmod{4}$: they are $1$ and $3 \bmod 4$. For odd $p \nmid c$, they exist exactly when $-c$ is a square $\mathrm{mod}\ p$, and then there are two classes $\mathrm{mod}\ p^2$. For $p \mid c$ there are none. Let $p_c$ be the least prime with root classes; for $c = 1$ it is $5$. The root classes $\mathrm{mod}\ p_c^2$ are the natural candidates for the maximum. They have density $1/4$ if $p_c = 2$ and $1/p_c^2$ otherwise.

**The game for $c$.** The types are built as follows.

- The layer primes are $2$, $3$ and $P$, where $P = p_c$ if $p_c \ge 7$ and $P = 5$ otherwise. A type records $a \bmod 36$ and $a \bmod P^2$.
- Every other prime is a luck prime. For each luck prime $q \mid c$, the type records whether $q \mid a$, as Lemmas 2.2 and 2.4 require.
- The type records membership in the root classes of the least luck prime $p$ with $\rho_p = 2$, as in Section 3.

The constants $b_t$ are those of Lemmas 2.2 and 2.4: union bounds over all luck primes, with the $q \mid c$ terms at their worst case for self-forcing types. Lemma 2.5 then reduces the problem to a finite maximisation, which `game_gen.py` solves with CP-SAT in two steps.

1. It finds the maximum-weight cliques among the types. These are the largest congruence-defined $c$-valid sets.
2. It maximises $U(K)$ over the cores whose $F(K)$ is not inside any maximum clique. Call this maximum $V_c$.

**Theorem 5.1 (computer-assisted).** Let $c \le 100$ be squarefree with $p_c \le 7$ and $c \notin \{10, 13\}$; there are 49 such $c$. Then:

1. The maximum cliques of the game are exactly the two root classes $\mathrm{mod}\ p_c^2$ ($\mathrm{mod}\ 4$ if $p_c = 2$).
2. $V_c < 1/p_c^2$ ($V_c < 1/4$ if $p_c = 2$).
3. For all sufficiently large $N$, the largest $c$-valid sets in $[N]$ are the root classes $\mathrm{mod}\ p_c^2$ of largest size, and only these.

*Proof.* Parts 1 and 2 are the computation. For part 3, let $A$ be $c$-valid and not inside a root class $\mathrm{mod}\ p_c^2$. Then the type set of $A$ is not inside a maximum clique, so neither is $F(K)$. By Lemma 2.5, $|A| \le (V_c + o(1))N$. Since $V_c$ is strictly below the density of the root classes, this is smaller than the root classes once $N$ is large. A $c$-valid set inside a root class has at most its size, with equality only for the full class. ∎

For 33 of these $c$, the best congruence-defined $c$-valid set not inside a root class has density exactly $V_c$. So $V_c$ is the second-best density.

| max density | second-best density | c |
| --- | --- | --- |
| $1/4$ (classes $\mathrm{mod}\ 4$) | $1/9$ | $3, 11, 23, 47, 51, 59, 71, 83, 87, 95$ |
| $1/4$ | $1/18$ | $43, 67, 79$ |
| $1/9$ (classes $\mathrm{mod}\ 9$) | $1/12$ | $2, 14, 26, 38, 62, 74, 86$ |
| $1/9$ | $1/18$ | $5, 17, 29, 41, 53, 65, 89$ |
| $1/25$ (classes $\mathrm{mod}\ 25$) | $1/50$ | $1$ |
| $1/25$ | $3/100$ | $6, 34, 46$ |
| $1/49$ (classes $\mathrm{mod}\ 49$) | $3/196$ | $82$ |
| $1/49$ | $1/98$ | $97$ |

For the other 16 values of $c$ ($7, 15, 19, 21, 31, 33, 35, 39, 55, 61, 66, 69, 73, 77, 91, 94$), the best congruence set and $V_c$ still differ, so the second-best density is only bracketed (`gen_k1.jsonl`).

The refinements matter. Without the root-class split and the divisibility flags, the game fails for $c = 34, 61, 66, 69$ and $94$: for $c = 34$ it gives $V = 0.0427$ against $1/25$. Each of these has a luck prime dividing $c$, such as $17 \mid 34$, or many small primes $p$ with $\rho_p = 2$. With the refinements all five pass. With $c = 1$ the computation reproduces $V = 1/50$ of [M].

Exact clique computations (`brute_c.py`) agree with the root class for every $N$ up to $400$–$800$ for $c = 2, 3, 6, 10, 13, 21$ and $34$.

Two groups of $c \le 100$ are left open.

- **$c = 10$ and $13$.** The class is $\mathrm{mod}\ 49$, and the game with one split prime falls just short: $V_{13} = 0.020465$ against $1/49 = 0.020408$. A second split prime should settle them, but it exceeds our computing budget.
- **The ten $c \le 100$ with $p_c \ge 11$:** $22, 30, 37, 42, 57, 58, 70, 78, 85$ and $93$. The model has $p_c^2$ slabs, and we have not run it.

Theorem 5.1 gives no explicit threshold for $N$, since the $o(N)$ terms of Section 2 are not made explicit.

## 6. Open problems

1. **The third density.** Prove Conjecture 3.2. This needs a two-sided bound for pairs $X, Y$ with $xy + 1$ never squarefree that improves on one witness per side.
2. **All $k$.** Does Theorem 4.3(2) hold for every $k$? For large $k$, a mixed set below $N_k$ needs $13^k$ or $17^k$ to divide $x^2 + 1$ or $ab + 1$ with $x, a, b$ below about $60\cdot 5^k$. Heuristically this happens for only finitely many $k$.
3. **All $c$.** Is the root class $\mathrm{mod}\ p_c^2$ extremal for every squarefree $c$, including $c = 10$, $13$ and those with $p_c \ge 11$? Is there a proof that does not need a computation for each $c$? Non-squarefree $c$ brings new self-forcing classes, such as $0 \bmod q$ when $q^2 \mid c$, and is not covered here.
4. **Effective thresholds** for Theorems 3.1 and 5.1.

## Appendix: reproducibility

All code is in the repository [R], in the folders `third_density/`, `cubefree/`, `kfree/` and `general_c/`. The CP-SAT computations use OR-tools 9.15.

| Claim | Computation | Result |
| --- | --- | --- |
| Theorem 3.1(1) | `lam3_lower.py`, exact count | $0.014671$ at $N = 2\cdot 10^{7}$ |
| Theorem 3.1(2) | `third_cp.py 13,17 product` | $\max U = 0.0149093$, OPTIMAL; $0.0149645$ with $S_{13}$ only; $0.0186$ unrefined (`third.py`) |
| Theorem 4.1 | `cube_maxsets.py` ($N \le 700$), `cube_small.py` (to $40{,}000$), `cubeM.c` ($700 \le N \le 2\cdot 10^{6}$), `cube_analytic.py` ($N \ge 1.94\cdot 10^{6}$) | as stated |
| Theorem 4.3 | `kfree_analytic.py`, `kfree_exact.py`, `run_all.py`, `run_big.py`, `margin.py` | no exceptions for $5 \le k \le 100$; margin at least $3$ for $5 \le k \le 300$ |
| Theorem 5.1 | `game_gen.py 1 c` for each $c$; output `gen_k1.jsonl` | $V_c < 1/p_c^2$ for 49 values; $V_1 = 1/50$ |
| Small-N checks for $ab + c$ | `brute_c.py` | root class maximal for $c = 2, 3, 6, 10, 13, 21, 34$ up to $N = 400$–$800$ |

## References

[M] L. Culpitt, Stability, rigidity and exact extremisers for Erdős Problem 848, companion paper (2026).

[R] L. Culpitt, Erdos-848, https://github.com/MeaCulpitt/Erdos-848 (2026).

[B] T. F. Bloom, Erdős Problem #848, https://www.erdosproblems.com/848.

[OR-tools] L. Perron and F. Didier, CP-SAT, Google OR-Tools, https://developers.google.com/optimization.

[RS] J. B. Rosser and L. Schoenfeld, Approximate formulas for some functions of prime numbers, Illinois J. Math. 6 (1962), 64–94.

## Acknowledgements

The arguments and code were developed with AI assistance (Claude) and independently re-run. They have not yet been reviewed by a human expert.
