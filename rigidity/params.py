# Exact-rational parameters for bb.c, mirroring n0lemma.py alpha_up/beta_up and vk2.py's split.
import math, json, sys
from fractions import Fraction as Fr
import numpy as np
P1 = 10**7
s = np.ones(P1+1, bool); s[:2] = False
for i in range(2, int(P1**.5)+1):
    if s[i]: s[i*i::i] = False
PR = np.nonzero(s)[0]
PR1 = PR[PR % 4 == 1]
Tsq = 2.51012/(P1*math.log(P1))
def sum_gt(z, cls1):
    arr = PR1 if cls1 else PR
    return float(np.sum(1.0/arr[arr > z].astype(float)**2)) + Tsq
D = 10**15
v2 = json.load(open(sys.argv[1]))
for zA in (17, 29, 37, 41):
    for zB in (13, 17, 19, 23):
        tA = 2*sum_gt(zA, True)
        alpha_s = 1 - math.prod(1-2/p**2 for p in PR1 if 13 <= p <= zA)
        beta = 1 - math.prod(1-1/p**2 for p in PR if 7 <= p <= zB) + sum_gt(zB, False)
        # small safety margin for float error in the sums (rounds up)
        bI = math.ceil(beta*D*(1+1e-12)); aI = math.ceil(alpha_s*D*(1+1e-12)); cI = math.ceil(23/25*tA*D*(1+1e-12))
        print(zA, zB, bI, aI, cI, v2[f"{zA},{zB}"])
