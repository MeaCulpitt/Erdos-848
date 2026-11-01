exec(open('closed.py').read().split("best=[]")[0])
def mx(b,j):
  m=0
  for M7 in closed:
    A7=A(M7) 
    for M18 in closed:
      if not M18<=A7: continue
      A18=A(M18); AR=A7&A18
      if not (W(A7)>0 and W(A18)>0): continue
      m=max(m,(1-b)*(W(M7)+W(M18))+b*(W(A18)+W(A7))+23*j*W(AR))
  return m
lo,hi=0.0169,0.03
for _ in range(40):
  mid=(lo+hi)/2
  if mx(0.052,mid)<=18+1e-12: lo=mid
  else: hi=mid
print("j threshold at beta=0.052:",lo)
lo,hi=0.052,0.2
for _ in range(40):
  mid=(lo+hi)/2
  if mx(mid,0.0169)<=18+1e-12: lo=mid
  else: hi=mid
print("beta threshold at j=0.0169:",lo)
