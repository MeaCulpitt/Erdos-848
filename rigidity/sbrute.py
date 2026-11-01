# Independent brute force of Sawhney case bounds S1..S4 at given N (direct non-squarefree table, no prime stepping).
# nsq[x] = True iff x has a square factor > 1, by a direct sieve over all d^2 (d >= 2, not just primes).
import sys, numpy as np
for N in map(int, sys.argv[1:]):
    M = N*N + 2
    nsq = np.zeros(M, bool)
    d = 2
    while d*d < M:
        nsq[d*d::d*d] = True; d += 1
    a = np.arange(N+1)
    V = nsq[a*a+1]; V[0] = False
    r = a % 25
    C7 = V & (r == 7); C18 = V & (r == 18); R = V & (r != 7) & (r != 18); odd = a % 2 == 1
    m = dict.fromkeys(["1", "2", "3a", "3b", "3c", "3d", "4a", "4b"], 0)
    for b in np.nonzero(V)[0]:
        b = int(b); hit = nsq[a*b+1]
        h7 = int((hit & C7).sum()); h18 = int((hit & C18).sum()); ho = int((hit & (C7 | C18) & odd).sum())
        if R[b]:
            if b % 2 == 0: m["1"] = max(m["1"], h7 + h18)
            else: m["2"] = max(m["2"], ho); m["3a"] = max(m["3a"], h7); m["3c"] = max(m["3c"], h18)
        elif C7[b]:
            m["4b"] = max(m["4b"], h18)
            if b % 2 == 0: m["3b"] = max(m["3b"], h18)
        else:
            m["4a"] = max(m["4a"], h7)
            if b % 2 == 0: m["3d"] = max(m["3d"], h7)
    vR = int(R.sum()); vRo = int((R & odd).sum())
    S1 = vR + m["1"]; S2 = vRo + m["2"]; S3 = vRo + max(m["3a"] + m["3b"], m["3c"] + m["3d"]); S4 = m["4a"] + m["4b"]
    print(f"N={N} S1={S1} S2={S2} S3={S3} S4={S4} F={max(S1,S2,S3,S4)} c7={(N-7)//25+1}", flush=True)
