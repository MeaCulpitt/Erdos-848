// Exact integer certificate: lambda* local game value <= 1/50.
// Cells mod 36: mu in {E,1,3} x nu in {0(3|a),1,2,4,5,7,8}; weight in units of 1/36.
// A core K = (M7 ⊆ C7-cells, M18 ⊆ C18-cells), cross pairs forced (M18 ⊆ A(M7)).
// Cross forcing between a C-cell and any type outside its own class uses only 4 or 9 (never 25),
// so A(M) = cells forced (by 4 or 9) with every cell of M, the same set for C-targets and R-targets.
// Bound:  900*U = (1-b)(W7+W18) + b(W[C7 part of F] + W[C18 part of F]) + 23*j*W[R part of F] <= 18 (= 900/50).
// Feasibility: a mixed P ⊆ F(K) needs F(K) to contain a type outside C7 and a type outside C18.
// Integer arithmetic with b = BN/D, j = JN/D (rational upper bounds for beta+ and j+, with margin).
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
typedef long long ll;
int main(int argc, char **argv) {
  ll D = 1000000, BN = argc > 1 ? atoll(argv[1]) : 52000, JN = argc > 2 ? atoll(argv[2]) : 16000;
  int MU[3] = {0, 1, 3}, NU[7] = {0, 1, 2, 4, 5, 7, 8}, mu[21], nu[21], w[21]; int n = 0;
  for (int a = 0; a < 3; a++) for (int b = 0; b < 7; b++) {
    mu[n] = MU[a]; nu[n] = NU[b]; w[n] = (a == 0 ? (b == 0 ? 6 : 2) : (b == 0 ? 3 : 1)); n++; }
  int tot = 0; for (int i = 0; i < 21; i++) tot += w[i];
  if (tot != 36) { printf("weights bad\n"); return 1; }
  uint32_t Nb[21], ALL = (1u << 21) - 1;
  for (int i = 0; i < 21; i++) { Nb[i] = 0; for (int k = 0; k < 21; k++) {
      int f4 = mu[i] && mu[k] && (mu[i] * mu[k]) % 4 == 3;
      int f9 = nu[i] && nu[k] && (nu[i] * nu[k]) % 9 == 8;
      if (f4 || f9) Nb[i] |= 1u << k; } }
  uint32_t *A = malloc(sizeof(uint32_t) << 21); int *W = malloc(sizeof(int) << 21);
  A[0] = ALL; W[0] = 0;
  for (uint32_t M = 1; M <= ALL; M++) { int lb = __builtin_ctz(M); uint32_t r = M & (M - 1);
    A[M] = A[r] & Nb[lb]; W[M] = W[r] + w[lb]; }
  ll LIM = 18 * D, best = -1, second = -1, nconf = 0, neq = 0; uint32_t b7 = 0, b18 = 0, s7 = 0, s18 = 0;
  for (uint32_t M7 = 0; M7 <= ALL; M7++) {
    uint32_t A7 = A[M7];                      // C18-cells (and R-cells) forced with all of M7
    uint32_t S = A7;                          // M18 ranges over subsets of A7 (biclique)
    for (uint32_t M18 = S;; M18 = (M18 - 1) & S) {
      uint32_t A18 = A[M18], AR = A7 & A18;
      int WC7 = M18 ? W[A18] : 36;            // C7 types in F(K): all if M18 empty, else forced with M18 ...
      int WC18 = M7 ? W[A7] : 36;             // ... but C7 cells of M7 are already counted in K below
      // C7 part of F = (C7 cells forced with all M18) — M7 ⊆ it by the biclique condition. Non-core C7 = WC7 - W7.
      int W7 = W[M7], W18 = W[M18], WR = W[AR];
      // feasibility of a mixed P ⊆ F(K): needs a non-C7 type and a non-C18 type in F(K)
      int nonC7 = (WC18 > 0) || (WR > 0), nonC18 = (WC7 > 0) || (WR > 0);
      if (nonC7 && nonC18) {
        nconf++;
        ll v = (D - BN) * 0 + D * (ll)(W7 + W18) + BN * (ll)((WC7 - W7) + (WC18 - W18)) + 23 * JN * (ll)WR;
        if (v > best) { best = v; b7 = M7; b18 = M18; } if (v < LIM && v > second) { second = v; s7 = M7; s18 = M18; }
        if (v >= LIM) neq++;
      }
      if (M18 == 0) break;
    }
  }
  printf("b=%lld/%lld j=%lld/%lld  configurations checked %lld\n", BN, D, JN, D, nconf);
  printf("max 900*U*D = %lld  vs  18*D = %lld  -> %s;  #configs reaching 1/50: %lld\n", best, LIM,
         best <= LIM ? "PROVED: value <= 1/50 (exact integer arithmetic)" : "FAILS", neq);
  printf("argmax M7 cells:"); for (int i = 0; i < 21; i++) if (b7 >> i & 1) printf(" (%d,%d)", mu[i], nu[i]);
  printf("\nargmax M18 cells:"); for (int i = 0; i < 21; i++) if (b18 >> i & 1) printf(" (%d,%d)", mu[i], nu[i]);
  printf("\nsecond-best value (excluding configurations reaching 1/50): 900*U*D = %lld, gap to 1/50 = %.6f\n", second, (double)(LIM - second) / (900.0 * D));
  printf("second-best M7:"); for (int i = 0; i < 21; i++) if (s7 >> i & 1) printf(" (%d,%d)", mu[i], nu[i]);
  printf("\nsecond-best M18:"); for (int i = 0; i < 21; i++) if (s18 >> i & 1) printf(" (%d,%d)", mu[i], nu[i]);
  printf("\n"); return best <= LIM ? 0 : 1;
}
