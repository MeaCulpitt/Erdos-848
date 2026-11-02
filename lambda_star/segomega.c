// Segmented exact counts, for grid bins (x_{i-1}, x_i], x_i = 10^(i/200), of
//   N_j      = #{n : omega(n) = j}                         (all integers)
//   NV_j     = #{n : omega(n) = j, n in V_P}               V_P: p^2 | n^2+1 for some prime p <= P, p = 5 or p = 1 mod 4
// omega via sum of log p over prime powers p^a | n with p <= sqrt(X); a shortfall >= log 2 means one more prime > sqrt(X).
// Usage: ./segomega X P  -> prints cumulative counts at every grid point <= X.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#include <omp.h>
#define S (1<<24)
#define NG 2401
#define NJ 16
typedef unsigned long long u64;
static u64 pw(u64 a,u64 e,u64 m){u64 r=1;a%=m;while(e){if(e&1)r=(unsigned __int128)r*a%m;a=(unsigned __int128)a*a%m;e>>=1;}return r;}
int main(int c,char**v){ u64 X=strtoull(v[1],0,10), P=strtoull(v[2],0,10); u64 R=(u64)sqrtl((long double)X)+1;
  char*cp=calloc(R+1,1); u64*pr=malloc(sizeof(u64)*R); int np=0;
  for(u64 i=2;i<=R;i++) if(!cp[i]){pr[np++]=i; for(u64 j=i*i;j<=R;j+=i) cp[j]=1;}
  // roots of x^2 = -1 mod p^2 for p <= P (p = 5 or 1 mod 4)
  u64 *vq=malloc(8*np), *vr=malloc(16*np); int nv=0;
  for(int k=0;k<np && pr[k]<=P;k++){ u64 p=pr[k]; if(!(p==5||p%4==1)) continue; u64 q=p*p,t=0;
    for(u64 a=2;;a++){t=pw(a,(p-1)/4,p); if(t*t%p==p-1) break;}
    // Hensel: R = t - (t^2+1)/(2t) mod q
    u64 f=(t*t+1)%q; long long a0=(2*t)%q,m=q,x0=1,x1=0; while(m){long long qq=a0/m,tm=a0-qq*m;a0=m;m=tm;tm=x0-qq*x1;x0=x1;x1=tm;}
    u64 inv=((x0%(long long)q)+q)%q; u64 Rt=(t+q-(u64)((unsigned __int128)f*inv%q))%q;
    if(((unsigned __int128)Rt*Rt+1)%q){fprintf(stderr,"hensel %llu\n",p);return 1;}
    vq[nv]=q; vr[2*nv]=Rt; vr[2*nv+1]=q-Rt; nv++; }
  double g[NG]; for(int i=0;i<NG;i++) g[i]=pow(10.0,i/200.0);
  int imax=0; while(imax+1<NG && floor(g[imax+1]+1e-9)<=X) imax++;
  static u64 bins[2][2][NG][NJ];  // [thread][all/V][bin][j]
  memset(bins,0,sizeof bins);
  u64 nseg=(X+S-1)/S;
  #pragma omp parallel num_threads(2)
  { int th=omp_get_thread_num(); float*acc=malloc(4*S); unsigned char*om=malloc(S); unsigned char*inV=malloc(S);
    #pragma omp for schedule(dynamic,1)
    for(u64 sg=0;sg<nseg;sg++){ u64 L=sg*S+1, H=L+S-1; if(H>X) H=X; u64 len=H-L+1;
      memset(acc,0,4*len); memset(om,0,len); memset(inV,0,len);
      for(int k=0;k<np;k++){ u64 p=pr[k]; if(p>H) break; float lp=logf((float)p);
        u64 st=((L+p-1)/p)*p; for(u64 n=st;n<=H;n+=p){ om[n-L]++; acc[n-L]+=lp; }
        for(u64 pa=p*p; pa<=H; pa*=p){ u64 s2=((L+pa-1)/pa)*pa; for(u64 n=s2;n<=H;n+=pa) acc[n-L]+=lp; if(pa>H/p) break; } }
      for(int k=0;k<nv;k++){ u64 q=vq[k]; for(int s=0;s<2;s++){ u64 r=vr[2*k+s]; u64 st=L+((r+q-(L%q))%q); for(u64 n=st;n<=H;n+=q) inV[n-L]=1; } }
      // bin index: smallest i with floor(g[i]) >= n
      int bi=0; while(bi<=imax && floor(g[bi]+1e-9)<L) bi++;
      for(u64 n=L;n<=H;n++){ int w=om[n-L]; if(acc[n-L] < logf((float)n)-0.5f) w++;
        while(bi<=imax && floor(g[bi]+1e-9)<n) bi++;
        if(bi>imax) break;
        bins[th][0][bi][w]++; if(inV[n-L]) bins[th][1][bi][w]++; } }
  }
  u64 cum[2][NJ]={{0}};
  for(int i=0;i<=imax;i++){ for(int t=0;t<2;t++) for(int j=0;j<NJ;j++){ cum[t][j]+=bins[0][t][i][j]+bins[1][t][i][j]; }
    printf("%d %llu",i,(u64)floor(g[i]+1e-9)); for(int t=0;t<2;t++) for(int j=0;j<NJ;j++) printf(" %llu",cum[t][j]); printf("\n"); }
  return 0; }
