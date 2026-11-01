import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.GCongr

/-!
# Erdős Problem 848: kernel-checked certificate for λ* = 1/50 (Proposition 8.6)

Cells are the 21 classes mod 36 of Section 8.4 of the paper:
(a mod 4 ∈ {even, 1, 3}) × (a mod 9, with 3 ∣ a merged). Cell index = 7·μ + ν.

* `forced c d`: 4 or 9 divides `a*b + 1` for all `a` in cell `c`, `b` in cell `d`
  (`forced_iff` proves this against the integers).
* `A M`: the cells forced with every cell of `M`.
* A core is a pair `(M7, M18)` of cell sets, every cross pair forced (`M18 ⊆ A M7`).
* `value M7 M18 = 900·D·U(K)` with β = BN/D = 0.052 and j = JN/D = 0.0169:
  `(1-β)(w M7 + w M18) + β(w (A M18) + w (A M7)) + 23·j·w(A M7 ∩ A M18)`,
  weights in residues mod 36.

`lamcert`: `value ≤ 18·D`, i.e. U(K) ≤ 1/50, for every core whose F(K) has a type outside C7
and a type outside C18 (equivalently `A M7` and `A M18` are nonempty).
`lamcert_eq`: equality holds only for the core of F (cells 1 mod 4 in C7, 3 mod 4 in C18)
and its mirror image.

The reduction is a Galois-closure argument: replacing `M` by `A (A M)` keeps every `A`-set and
raises the weight, and there are only 64 sets of the form `A M`. The resulting 64 × 64 check
is done by `decide` in the kernel; no `native_decide`.
-/

namespace LamCert

abbrev Cell := Fin 21

def muOf (c : Cell) : ℕ := [0, 1, 3].getD (c.val / 7) 0
def nuOf (c : Cell) : ℕ := [0, 1, 2, 4, 5, 7, 8].getD (c.val % 7) 0

/-- `forced c d`: 4 or 9 divides `a*b+1` throughout cells `c`, `d`. -/
def forced (c d : Cell) : Bool :=
  (muOf c != 0 && muOf d != 0 && muOf c * muOf d % 4 == 3) ||
  (nuOf c != 0 && nuOf d != 0 && nuOf c * nuOf d % 9 == 8)

def muIdx (n : ℕ) : ℕ := if n % 2 = 0 then 0 else if n % 4 = 1 then 1 else 2
def nuIdx (n : ℕ) : ℕ :=
  match n % 9 with
  | 1 => 1 | 2 => 2 | 4 => 3 | 5 => 4 | 7 => 5 | 8 => 6 | _ => 0

/-- The cell of a natural number. -/
def cellOf (n : ℕ) : Cell := ⟨(muIdx n * 7 + nuIdx n) % 21, Nat.mod_lt _ (by norm_num)⟩

lemma cellOf_mod (n : ℕ) : cellOf (n % 36) = cellOf n := by
  have h4 : n % 36 % 4 = n % 4 := Nat.mod_mod_of_dvd n (by norm_num)
  have h2 : n % 36 % 2 = n % 2 := Nat.mod_mod_of_dvd n (by norm_num)
  have h9 : n % 36 % 9 = n % 9 := Nat.mod_mod_of_dvd n (by norm_num)
  simp only [cellOf, muIdx, nuIdx, h4, h2, h9]

/-- The forcing relation is exactly divisibility of `a*b+1` by 4 or 9. -/
theorem forced_iff (a b : ℕ) :
    (4 ∣ a * b + 1 ∨ 9 ∣ a * b + 1) ↔ forced (cellOf a) (cellOf b) = true := by
  have key : ∀ r s : Fin 36, (((r.val * s.val + 1) % 4 = 0 ∨ (r.val * s.val + 1) % 9 = 0) ↔
      forced (cellOf r.val) (cellOf s.val) = true) := by decide
  have h4 : (a * b + 1) % 4 = ((a % 36) * (b % 36) + 1) % 4 := by
    simp [Nat.add_mod, Nat.mul_mod, Nat.mod_mod_of_dvd _ (by norm_num : 4 ∣ 36)]
  have h9 : (a * b + 1) % 9 = ((a % 36) * (b % 36) + 1) % 9 := by
    simp [Nat.add_mod, Nat.mul_mod, Nat.mod_mod_of_dvd _ (by norm_num : 9 ∣ 36)]
  have := key ⟨a % 36, Nat.mod_lt _ (by norm_num)⟩ ⟨b % 36, Nat.mod_lt _ (by norm_num)⟩
  simp only [cellOf_mod] at this
  rw [Nat.dvd_iff_mod_eq_zero, Nat.dvd_iff_mod_eq_zero, h4, h9]
  exact this

/-- Cell weights, in residues mod 36. -/
def w (c : Cell) : ℕ :=
  [6, 2, 2, 2, 2, 2, 2, 3, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1].getD c.val 0

theorem w_spec : ∀ c : Cell, w c = ((Finset.range 36).filter (fun r => cellOf r = c)).card := by
  decide

def W (S : Finset Cell) : ℕ := ∑ c ∈ S, w c

def A (M : Finset Cell) : Finset Cell :=
  Finset.univ.filter (fun c => ∀ m ∈ M, forced m c = true)

def D : ℕ := 1000000
def BN : ℕ := 52000    -- β = 0.052 ≥ β⁺ = 0.05114
def JN : ℕ := 16900    -- j = 0.0169 ≥ j⁺ = 0.01551

def value (M7 M18 : Finset Cell) : ℕ :=
  (D - BN) * (W M7 + W M18) + BN * (W (A M18) + W (A M7)) + 23 * JN * W (A M7 ∩ A M18)

/-! ### The Galois-closure reduction -/

lemma forced_symm : ∀ c d : Cell, forced c d = forced d c := by decide

lemma A_anti {M M' : Finset Cell} (h : M ⊆ M') : A M' ⊆ A M := by
  intro c hc
  simp only [A, Finset.mem_filter, Finset.mem_univ, true_and] at hc ⊢
  exact fun m hm => hc m (h hm)

lemma subset_A_comm {M N : Finset Cell} : M ⊆ A N ↔ N ⊆ A M := by
  have key : ∀ {M N : Finset Cell}, M ⊆ A N → N ⊆ A M := by
    intro M N h c hc
    simp only [A, Finset.mem_filter, Finset.mem_univ, true_and]
    intro m hm
    have := (Finset.mem_filter.mp (h hm)).2 c hc
    rwa [forced_symm]
  exact ⟨key, key⟩

lemma le_AA (M : Finset Cell) : M ⊆ A (A M) := subset_A_comm.mpr (subset_refl _)

lemma AAA (M : Finset Cell) : A (A (A M)) = A M :=
  Finset.Subset.antisymm (A_anti (le_AA M)) (le_AA (A M))

lemma W_mono {S T : Finset Cell} (h : S ⊆ T) : W S ≤ W T :=
  Finset.sum_le_sum_of_subset h

lemma value_le_closure (M7 M18 : Finset Cell) :
    value M7 M18 ≤ value (A (A M7)) (A (A M18)) := by
  unfold value
  rw [AAA, AAA]
  have h1 := W_mono (le_AA M7)
  have h2 := W_mono (le_AA M18)
  gcongr

/-! ### The 64 sets of the form `A M` -/

def L : List (Finset Cell) := [
  ∅ ,
  {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20} ,
  {1, 7, 8, 9, 10, 11, 12, 13, 15} ,
  {1, 8, 14, 15, 16, 17, 18, 19, 20} ,
  {1, 8, 15} ,
  {2, 7, 8, 9, 10, 11, 12, 13, 16} ,
  {2, 9, 14, 15, 16, 17, 18, 19, 20} ,
  {2, 9, 16} ,
  {3, 7, 8, 9, 10, 11, 12, 13, 17} ,
  {3, 10, 14, 15, 16, 17, 18, 19, 20} ,
  {3, 10, 17} ,
  {4, 7, 8, 9, 10, 11, 12, 13, 18} ,
  {4, 11, 14, 15, 16, 17, 18, 19, 20} ,
  {4, 11, 18} ,
  {5, 7, 8, 9, 10, 11, 12, 13, 19} ,
  {5, 12, 14, 15, 16, 17, 18, 19, 20} ,
  {5, 12, 19} ,
  {6, 7, 8, 9, 10, 11, 12, 13, 20} ,
  {6, 13, 14, 15, 16, 17, 18, 19, 20} ,
  {6, 13, 20} ,
  {7, 8, 9, 10, 11, 12, 13} ,
  {8} ,
  {8, 16} ,
  {8, 17} ,
  {8, 18} ,
  {8, 19} ,
  {8, 20} ,
  {9} ,
  {9, 15} ,
  {9, 17} ,
  {9, 18} ,
  {9, 19} ,
  {9, 20} ,
  {10} ,
  {10, 15} ,
  {10, 16} ,
  {10, 18} ,
  {10, 19} ,
  {10, 20} ,
  {11} ,
  {11, 15} ,
  {11, 16} ,
  {11, 17} ,
  {11, 19} ,
  {11, 20} ,
  {12} ,
  {12, 15} ,
  {12, 16} ,
  {12, 17} ,
  {12, 18} ,
  {12, 20} ,
  {13} ,
  {13, 15} ,
  {13, 16} ,
  {13, 17} ,
  {13, 18} ,
  {13, 19} ,
  {14, 15, 16, 17, 18, 19, 20} ,
  {15} ,
  {16} ,
  {17} ,
  {18} ,
  {19} ,
  {20}]

lemma A_insert (c : Cell) (M : Finset Cell) : A (insert c M) = A {c} ∩ A M := by
  ext d; simp [A, Finset.mem_filter]

lemma L_closed : ∀ S ∈ L, ∀ c : Cell, A {c} ∩ S ∈ L := by decide +kernel

lemma univ_mem : (Finset.univ : Finset Cell) ∈ L := by decide +kernel

lemma A_mem (M : Finset Cell) : A M ∈ L := by
  induction M using Finset.induction_on with
  | empty =>
    have : A ∅ = Finset.univ := by ext; simp [A]
    rw [this]; exact univ_mem
  | insert c M _ ih => rw [A_insert]; exact L_closed _ ih c

/-- The finite check over the 64 × 64 pairs of sets of the form `A M`. -/
lemma check : ∀ S ∈ L, ∀ T ∈ L, T ⊆ A S → (A S).Nonempty → (A T).Nonempty →
    value S T ≤ 18 * D := by decide +kernel

/-- **Proposition 8.6.** Every core whose F(K) has a type outside C7 and one outside C18
has U(K) ≤ 1/50, with β = 0.052 and j = 0.0169. -/
theorem lamcert (M7 M18 : Finset Cell) (h : M18 ⊆ A M7)
    (h7 : (A M7).Nonempty) (h18 : (A M18).Nonempty) : value M7 M18 ≤ 18 * D := by
  have h' : A (A M18) ⊆ A (A (A M7)) := by
    rw [AAA]; exact A_anti (subset_A_comm.mp h)
  have e7 : (A (A (A M7))).Nonempty := by rw [AAA]; exact h7
  have e18 : (A (A (A M18))).Nonempty := by rw [AAA]; exact h18
  have hc := check (A (A M7)) (A_mem (A M7)) (A (A M18)) (A_mem (A M18)) h' e7 e18
  exact le_trans (value_le_closure M7 M18) hc

/-! ### Equality: only the core of F and its mirror -/

/-- The cells ≡ 1 (mod 4) and ≡ 3 (mod 4). -/
def row1 : Finset Cell := {7, 8, 9, 10, 11, 12, 13}
def row3 : Finset Cell := {14, 15, 16, 17, 18, 19, 20}

lemma w_pos : ∀ c : Cell, 0 < w c := by decide

lemma eq_of_W_eq {S T : Finset Cell} (h : S ⊆ T) (he : W S = W T) : S = T := by
  by_contra hne
  obtain ⟨x, hxT, hxS⟩ := Finset.exists_of_ssubset (Finset.ssubset_iff_subset_ne.mpr ⟨h, hne⟩)
  have := Finset.sum_lt_sum_of_subset h hxT hxS (w_pos x) (fun _ _ _ => Nat.zero_le _)
  unfold W at he
  omega

lemma check_eq : ∀ S ∈ L, ∀ T ∈ L, T ⊆ A S → (A S).Nonempty → (A T).Nonempty →
    value S T = 18 * D → (S = row1 ∧ T = row3) ∨ (S = row3 ∧ T = row1) := by decide +kernel

/-- **Equality case of Proposition 8.6.** Only the core of F and its mirror reach 1/50. -/
theorem lamcert_eq (M7 M18 : Finset Cell) (h : M18 ⊆ A M7)
    (h7 : (A M7).Nonempty) (h18 : (A M18).Nonempty) (hv : value M7 M18 = 18 * D) :
    (M7 = row1 ∧ M18 = row3) ∨ (M7 = row3 ∧ M18 = row1) := by
  have h' : A (A M18) ⊆ A (A (A M7)) := by
    rw [AAA]; exact A_anti (subset_A_comm.mp h)
  have e7 : (A (A (A M7))).Nonempty := by rw [AAA]; exact h7
  have e18 : (A (A (A M18))).Nonempty := by rw [AAA]; exact h18
  have hc := check (A (A M7)) (A_mem (A M7)) (A (A M18)) (A_mem (A M18)) h' e7 e18
  have hcl := value_le_closure M7 M18
  have hv' : value (A (A M7)) (A (A M18)) = 18 * D := by omega
  have w7 := W_mono (le_AA M7)
  have w18 := W_mono (le_AA M18)
  have hsum : W M7 + W M18 = W (A (A M7)) + W (A (A M18)) := by
    simp only [value, AAA, D, BN, JN] at hv hv'
    omega
  have c7 : M7 = A (A M7) := eq_of_W_eq (le_AA M7) (by omega)
  have c18 : M18 = A (A M18) := eq_of_W_eq (le_AA M18) (by omega)
  rw [c7, c18]
  exact check_eq _ (A_mem (A M7)) _ (A_mem (A M18)) h' e7 e18 hv'

end LamCert

#print axioms LamCert.forced_iff
#print axioms LamCert.w_spec
#print axioms LamCert.lamcert
#print axioms LamCert.lamcert_eq
