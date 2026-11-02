import json, sys, time
import kfree_analytic as KA, kfree_exact as K
ks = [int(a) for a in sys.argv[1].split(",")]
for k in ks:
    t = time.time(); Nk, Z, sig = KA.Nk(k); Nk = int(Nk) + 1
    q, r, ps, V, adj = K.setup(k, Nk)
    ex = K.run_clique(k, Nk, V, adj, q, r)
    print(json.dumps(dict(k=k, r=r, N_k=Nk, vertices=len(V), exceptions=ex, seconds=round(time.time() - t))), flush=True)
