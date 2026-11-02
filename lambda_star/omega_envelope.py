"""Rigorous upper envelopes U_j(x) >= N_j(x) = #{n <= x : omega(n) = j} on the grid x_i = 10^(i/200), up to 10^18.

  x_i <= 10^9 : exact counts (omgrid.c).
  x_i > 10^9  : N_1(x) = #{prime powers <= x} <= piU(x) + 2 sqrt(x)        (Dusart 2010: pi(x) <= x/ln x (1 + 1/ln x + 2.51/ln^2 x), x >= 355991)
                N_{k+1}(x) <= A + B, splitting n by whether its largest prime-power factor q exceeds sqrt(x):
                  A = #{n : q > sqrt x} <= sum_{m <= sqrt x, omega(m) = k} #{prime powers <= x/m}       (n = q m uniquely)
                  B = #{n : all prime-power factors <= sqrt x} <= (1/(k+1)) sum_{q <= sqrt x} N_k(x/q)   (each n counted k+1 times)
                Both sums are binned on the grid: in A, m in (g_{j-1}, g_j] is charged U_1(x/g_{j-1}) (exact N_k counts, m <= 10^9);
                in B, prime powers q in (g_{j-1}, g_j] (exact counts, q <= 10^9) are charged U_k(x/g_{j-1}), rounded up to the grid.
All envelopes are nondecreasing in x, so U_j at the next grid point bounds N_j on the whole interval."""
import math, numpy as np

D = 200; IMAX = 3600                       # grid up to 10^18
rows = np.loadtxt('omgrid.txt', dtype=np.int64)
I9 = 1800
ex = np.zeros((I9 + 1, 16)); ex[rows[:, 0]] = rows[:, 2:]
assert np.all(ex[I9].sum() == 10**9), "counts do not sum to 10^9"
g = 10.0 ** (np.arange(IMAX + 1) / D)

def piU(x):
    if x < 355991: raise ValueError
    L = math.log(x); return x / L * (1 + 1 / L + 2.51 / L**2)

KMAX = 15
U = np.zeros((KMAX + 1, IMAX + 1))
U[:, :I9 + 1] = ex[:, :KMAX + 1].T
for i in range(I9 + 1, IMAX + 1):
    U[1, i] = piU(g[i]) + 2 * math.sqrt(g[i])
U[0, :] = 1
pp = np.diff(ex[:, 1], prepend=0)          # prime powers in (g_{j-1}, g_j], j <= 1800
def Uat(k, logidx):
    """U_k at the smallest grid point >= 10^(logidx/D) (logidx real)."""
    j = int(math.ceil(logidx - 1e-9))
    return U[k, min(j, IMAX)] if j <= IMAX else None

for k in range(1, KMAX):
    for i in range(I9 + 1, IMAX + 1):
        half = i / 2.0                      # sqrt(x_i) = 10^(half/D)
        jmax = int(math.floor(half + 1e-9))  # grid points <= sqrt(x_i)
        # A: m <= sqrt x with omega(m) = k, binned; charge prime powers up to x/g_{j-1}
        A = 0.0
        Nk = ex[:, k]
        for j in range(1, jmax + 1):
            dm = Nk[j] - Nk[j - 1]
            if dm: A += dm * Uat(1, i - (j - 1))
        # the part of the last bin above sqrt(x) only adds (upper bound), fine; plus m in (g_jmax, sqrt x]
        if jmax < half:
            dm = Nk[jmax + 1] - Nk[jmax]
            if dm: A += dm * Uat(1, i - jmax)
        # B: prime powers q <= sqrt x, binned
        Bs = 0.0
        for j in range(1, min(jmax + 1, I9) + 1):
            if pp[j]: Bs += pp[j] * Uat(k, i - (j - 1))
        U[k + 1, i] = (A + Bs / (k + 1)) * (1 + 1e-9)

np.save('omega_envelope.npy', U)
def tail_density(i, k): return U[k:, i].sum() / g[i]
if __name__ == "__main__":
    for d10 in (9, 10, 12, 15, 18):
        i = d10 * D
        print(f"x=1e{d10}: " + " ".join(f">={k}:{tail_density(i, k):.3g}" for k in (3, 5, 7, 9, 11)))
