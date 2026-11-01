# Numerical evaluation of the closed-form bound of README "Tail N >= 1e60" (Proposition A) at N = 1e60.
# All terms divided by N are nonincreasing in N for N >= 1e60 (see README), so this single check suffices.
import math, json
mc=json.load(open('mconst.json'))['tm']; lam=max(v[0] for v in mc.values()); c=max(v[1] for v in mc.values())
assert lam<=0.5334 and c<=18.94, (lam,c)
G=0.0294059212; delta=0.04-G
lnN=60*math.log(10); L=lnN; N=1e60
expo=0.95933/math.log(L)
IE=2*38*(1+2**3)+38+57*(1+3**2)
medA=6*1.25506*math.sqrt(2)*math.sqrt(N)/(L/2) + 1.25506*N**(2/3)/(2*L/3)
J=(1+(L+math.log(2)+1e-9)/math.log(1+math.sqrt(2)))/2
pell=(1+1e-4)*N**(2/3)*J
medB=38*1.25506*math.sqrt(N)/(L/2) + 1.25506*N**(2/3)/(2*L/3)
lat=N**expo*(1.067*N**(2/3)+20*math.sqrt(N))
E=IE+medA+pell+2*(medB+lat)
print(f"exponent for 2^k: {expo:.5f}; terms/N: IE {IE/N:.2e} medA {medA/N:.2e} pell {pell/N:.2e} medB {medB/N:.2e} lattice {lat/N:.2e}")
print(f"E(1e60)/N = {E/N:.3e}  vs delta - 0.28/N = {delta-0.28/N:.6f}  ->", "OK" if E<=delta*N-0.28 else "FAIL")
