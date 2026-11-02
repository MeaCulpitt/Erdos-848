// Exact N_j(x) = #{n <= x : omega(n) = j} at grid points x_i = 10^(i/200) <= X  (j = 0..15)
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
int main(int c,char**v){ long X=atol(v[1]); unsigned char*om=calloc(X+1,1); char*cp=calloc(X+1,1);
  for(long p=2;p<=X;p++) if(!cp[p]) for(long j=p;j<=X;j+=p){ om[j]++; if(j>p) cp[j]=1; }
  long cnt[16]={0}; int i=0; double nxt=1.0;
  for(long n=1;n<=X;n++){ cnt[om[n]]++;
    while(n+1>nxt-1e-9 && (long)floor(nxt+1e-9)==n){ printf("%d %ld",i,n); for(int j=0;j<16;j++) printf(" %ld",cnt[j]); printf("\n"); i++; nxt=pow(10.0,i/200.0);} }
  return 0; }
