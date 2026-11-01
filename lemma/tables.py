# Precompute: primes <= 1e7 (with mod-4 class), Pell admissible-m table mod L, rigorous prime-square tails.
import numpy as np
P1=10**7
s=np.ones(P1+1,bool); s[:2]=False
for i in range(2,int(P1**0.5)+1):
    if s[i]: s[i*i::i]=False
pr=np.nonzero(s)[0].astype(np.int64)
np.save('primes1e7.npy',pr)
# Pell admissible m (Lemma 3): m = (x^2+1)/p^2 with p>=7 prime: m mod 8 in {1,2,5}; 25∤m; no prime q≡3 mod 4 divides m.
L=8*25*3*7*11*19*23
m=np.arange(L)
ok=np.isin(m%8,[1,2,5])&(m%25!=0)
for q in (3,7,11,19,23): ok&=(m%q!=0)
cum=np.cumsum(ok).astype(np.int64)   # cum[r] = #{0<=m<=r admissible}
np.save('pellcum.npy',cum); print("L",L,"density",ok.mean())
