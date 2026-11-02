"""Lower bound lambda_3 >= 1/25 - 1/(4 pi^2): A = {a <= N : a = 7 mod 25, ax+1 not squarefree} u {x}, x = 18 mod 25.
Exact count for given N, x (sieve over q^2 | ax+1)."""
import sys, math, numpy as np
from sympy import primerange, nextprime
N=int(float(sys.argv[1])); x=int(sys.argv[2]) if len(sys.argv)>2 else None
if x is None:
    x=nextprime(10**5)
    while not (x%25==18 and x%4==3): x=nextprime(x)
mark=np.zeros(N+1,bool)
for q in primerange(2, math.isqrt(N*x+1)+1):
    m=q*q
    if x%q==0: continue
    a0=(-pow(x,-1,m))%m
    if a0==0: a0=m
    mark[a0::m]=True
a=np.arange(N+1); A=mark&(a%25==7)
cnt=int(A.sum())+1
# validity spot-check: a, a' in C7 forced by 25; x self: x^2+1
assert (x*x+1)%25==0
print(f"N={N}, x={x}: |A|={cnt}, |A|/N={cnt/N:.6f}, target 1/25-1/(4pi^2)={1/25-1/(4*math.pi**2):.6f}, d(x)={(1-(2/3)*75/(8*math.pi**2)/(1-1/x**2))/25:.6f}")
