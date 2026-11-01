# Brute-force sanity checks of Lemma 3 and Lemma 4 bounds at small N (not part of the proof).
import sys, math, random
sys.argv=['x']; exec(open('n0lemma.py').read().split('if __name__')[0])
from sympy import primerange, factorint
N=20000; worst4=0
for Y in (150,300,600):
    pl=list(primerange(int(Y)+1, int(math.isqrt(N*N+1))+2))
    # Lemma 3: count x<=N in R with p^2 | x^2+1, p>Y
    cnt=sum(1 for x in range(1,N+1) if x%25 not in (7,18) and any((x*x+1)%(p*p)==0 for p in pl if p*p<=x*x+1))
    print("Lemma3 N=",N,"Y=",Y,"actual",cnt,"bound",pell(N,Y))
    for b in random.sample(range(7,N),60)+[7436429%N or 7]:
        lat=lattice(N,Y,'tm')
        act=0
        for a in range(1,N+1):
            if a%25 not in (7,18): continue
            v=a*b+1
            if v%4==0 or v%9==0 or v%25==0: continue
            if any(v%(p*p)==0 for p in pl if p*p<=v): act+=1
        worst4=max(worst4,act/lat)
    print("  Lemma4 max actual/bound over sampled b:",round(worst4,4))
