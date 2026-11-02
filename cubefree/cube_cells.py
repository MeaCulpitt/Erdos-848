# Cells of ratio 1.5 covering 700 <= N <= 2*10^6: the exact bound at the top of each cell must stay below c57 at its bottom.
import subprocess
c57 = lambda N: (N - 57) // 125 + 1
lo = 700; fails = 0; rows = 0
while lo < 2_000_000:
    hi = min(int(lo * 1.5), 2_000_000)
    out = subprocess.run(["./cubeM", str(hi)], capture_output=True, text=True).stdout
    bound = int(out.split("bound=")[1])
    ok = bound < c57(lo); fails += (not ok); rows += 1
    print(f"[{lo}, {hi}]: bound {bound} vs c57(N_lo) = {c57(lo)}  {'ok' if ok else 'FAIL'}", flush=True)
    lo = hi
print(f"{rows} cells, {fails} failures; covers 700 <= N <= 2,000,000")
