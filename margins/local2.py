import sys; sys.argv=['x']
exec(open('local.py').read().split('if __name__')[0])
def types2(c4,c9):
    R25=tuple(r for r in range(25) if r not in (7,18))
    return [(a,b,c) for a in [(7,),(18,),R25] for b in c4 for c in c9]
P1=[p for p in PR if p%4==1 and p>=13]
ALL9=[tuple(range(9))]; S9=[(0,3,6)]+[(u,) for u in (1,2,4,5,7,8)]
for name,c4,c9 in [("kappa only",[(0,1,2,3)],ALL9),("kappa x parity",[(0,2),(1,3)],ALL9),
                   ("kappa x mod4",[(0,2),(1,),(3,)],ALL9),("kappa x mod9",[(0,1,2,3)],S9),("kappa x mod4 x mod9",[(0,2),(1,),(3,)],S9)]:
    for Sn,S in [("empty",set()),("all",set(P1))]:
        T=types2(c4,c9); b3=big(S)
        M=[[entry(s,t,b3) for t in T] for s in T]
        v,P=solve(T,M,[t[0]==(7,) for t in T],[t[0]==(18,) for t in T])
        print(f"{name:22s} S={Sn:5s} types={len(T):3d} worst={v:.5f}  P={[ (t[0][0] if len(t[0])==1 else 'R', t[1], t[2] if len(t[2])<9 else '*') for t in P][:8]}",flush=True)
