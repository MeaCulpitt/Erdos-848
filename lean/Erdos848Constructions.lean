import Mathlib.Algebra.Squarefree.Basic
import Mathlib.Tactic.NormNum
import Mathlib.Order.Interval.Finset.Nat

/-!
# Erdős Problem 848: the constructions

A set `A ⊆ ℕ` is *valid* if `a * b + 1` is not squarefree for all `a b ∈ A`, including `a = b`.

This file proves, for every `N` at once (the sets are infinite):

* `valid_C7`, `valid_C18`     : the residue classes 7 and 18 mod 25 are valid.
* `valid_fifty`               : the two-class set
                                `{n ≡ 7 (mod 25), n ≡ 1 (mod 4)} ∪ {n ≡ 18 (mod 25), n ≡ 3 (mod 4)}`
                                is valid (density 1/50), and it meets both classes (`fifty_meets_both`).
* `valid_7_41`, `valid_32_43`, `valid_41_43`, `valid_32_43_57` : the four exceptional maximisers
                                for 41 ≤ N ≤ 81 are valid, with the class counts `c7_56`, `c7_81`
                                showing they tie the maximum c7(N).

It does NOT prove maximality or uniqueness; those rest on the computations in the paper.
-/

namespace Erdos848

/-- `A` is valid: `a * b + 1` is not squarefree for all `a, b ∈ A` (the case `a = b` included). -/
def Valid (A : Set ℕ) : Prop := ∀ a ∈ A, ∀ b ∈ A, ¬ Squarefree (a * b + 1)

/-- A square of some `p ≥ 2` dividing `n` makes `n` non-squarefree. -/
lemma not_squarefree_of_sq_dvd {n p : ℕ} (hp : 2 ≤ p) (h : p * p ∣ n) : ¬ Squarefree n := by
  intro hs
  have hu := hs p h
  rw [Nat.isUnit_iff] at hu
  omega

lemma mul_add_one_mod (a b m : ℕ) :
    (a * b + 1) % m = ((a % m) * (b % m) + 1) % m := by
  rw [Nat.add_mod, Nat.mul_mod, ← Nat.add_mod]

/-- If `a ≡ r`, `b ≡ s (mod p²)` and `p² ∣ r * s + 1`, then `a * b + 1` is not squarefree. -/
lemma not_squarefree_of_mod {a b : ℕ} (p r s : ℕ) (hp : 2 ≤ p)
    (ha : a % (p * p) = r) (hb : b % (p * p) = s) (hrs : (r * s + 1) % (p * p) = 0) :
    ¬ Squarefree (a * b + 1) := by
  apply not_squarefree_of_sq_dvd hp
  apply Nat.dvd_of_mod_eq_zero
  rw [mul_add_one_mod, ha, hb, hrs]

/-- The residue class `c (mod 25)`. -/
def C (c : ℕ) : Set ℕ := {n | n % 25 = c}

theorem valid_C7 : Valid (C 7) := by
  intro a ha b hb
  simp only [C, Set.mem_ofPred_eq] at ha hb
  exact not_squarefree_of_mod 5 7 7 (by norm_num) ha hb (by norm_num)

theorem valid_C18 : Valid (C 18) := by
  intro a ha b hb
  simp only [C, Set.mem_ofPred_eq] at ha hb
  exact not_squarefree_of_mod 5 18 18 (by norm_num) ha hb (by norm_num)

/-- The density-1/50 set meeting both classes. -/
def Fifty : Set ℕ := {n | (n % 25 = 7 ∧ n % 4 = 1) ∨ (n % 25 = 18 ∧ n % 4 = 3)}

theorem valid_fifty : Valid Fifty := by
  intro a ha b hb
  simp only [Fifty, Set.mem_ofPred_eq] at ha hb
  rcases ha with ⟨ha1, ha2⟩ | ⟨ha1, ha2⟩ <;> rcases hb with ⟨hb1, hb2⟩ | ⟨hb1, hb2⟩
  · exact not_squarefree_of_mod 5 7 7 (by norm_num) ha1 hb1 (by norm_num)
  · exact not_squarefree_of_mod 2 1 3 (by norm_num) ha2 hb2 (by norm_num)
  · exact not_squarefree_of_mod 2 3 1 (by norm_num) ha2 hb2 (by norm_num)
  · exact not_squarefree_of_mod 5 18 18 (by norm_num) ha1 hb1 (by norm_num)

/-- `Fifty` is not contained in a single class mod 25. -/
theorem fifty_meets_both : 57 ∈ Fifty ∧ 57 ∈ C 7 ∧ 43 ∈ Fifty ∧ 43 ∈ C 18 := by
  simp only [Fifty, C, Set.mem_ofPred_eq]
  norm_num

/-- Closes `¬ Squarefree (x * y + 1)` for explicit numerals by finding a square divisor. -/
macro "sq_witness" : tactic => `(tactic| first
  | exact not_squarefree_of_sq_dvd (p := 2) (by norm_num) (by decide)
  | exact not_squarefree_of_sq_dvd (p := 3) (by norm_num) (by decide)
  | exact not_squarefree_of_sq_dvd (p := 5) (by norm_num) (by decide)
  | exact not_squarefree_of_sq_dvd (p := 29) (by norm_num) (by decide))

theorem valid_7_41 : Valid {7, 41} := by
  intro a ha b hb
  simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at ha hb
  rcases ha with rfl | rfl <;> rcases hb with rfl | rfl <;> sq_witness

theorem valid_32_43 : Valid {32, 43} := by
  intro a ha b hb
  simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at ha hb
  rcases ha with rfl | rfl <;> rcases hb with rfl | rfl <;> sq_witness

theorem valid_41_43 : Valid {41, 43} := by
  intro a ha b hb
  simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at ha hb
  rcases ha with rfl | rfl <;> rcases hb with rfl | rfl <;> sq_witness

theorem valid_32_43_57 : Valid {32, 43, 57} := by
  intro a ha b hb
  simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at ha hb
  rcases ha with rfl | rfl | rfl <;> rcases hb with rfl | rfl | rfl <;> sq_witness

/-- c7(N) = #{n ≤ N : n ≡ 7 (mod 25)} at the ends of the two exceptional ranges. -/
theorem c7_56 : ((Finset.Icc 1 56).filter (fun n => n % 25 = 7)).card = 2 := by decide
theorem c7_81 : ((Finset.Icc 1 81).filter (fun n => n % 25 = 7)).card = 3 := by decide

#print axioms valid_C7
#print axioms valid_C18
#print axioms valid_fifty
#print axioms fifty_meets_both
#print axioms valid_7_41
#print axioms valid_32_43
#print axioms valid_41_43
#print axioms valid_32_43_57
#print axioms c7_56
#print axioms c7_81

end Erdos848
