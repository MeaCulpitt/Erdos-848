# k = 31..KMAX: N_k from kfree_analytic for k <= 40, and the closed-form bound N_k <= 60*5^k for k > 40.
import json, sys, time
import kfree_analytic as KA, kfree_exact as K
for k in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    t = time.time()
    Nk = int(KA.Nk(k)[0]) + 1 if k <= 40 else 60 * 5**k
    q, r, ps, V, adj = K.setup(k, Nk)
    ex = K.run_clique(k, Nk, V, adj, q, r)
    print(json.dumps(dict(k=k, N_k_over_q=round(Nk / q, 1), vertices=len(V), sporadic=sum(1 for v in V if v % q not in (r, q - r)), exceptions=ex, seconds=round(time.time() - t))), flush=True)
