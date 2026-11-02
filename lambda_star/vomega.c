// exact counts of n <= X in V (n^2+1 not squarefree) by omega(n), at checkpoints 10^6..10^9
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
int main(int c,char**v){ long X=atol(v[1]); unsigned char*om=calloc(X+1,1); char*inV=calloc(X+1,1);
  char*comp=calloc(X+1,1);
  for(long p=2;p<=X;p++) if(!comp[p]){ for(long j=p;j<=X;j+=p){om[j]++; if(j>p) comp[j]=1;} }
  // V: p^2 | n^2+1 for some p = 5 or p = 1 mod 4 (p^2 <= X^2+1); roots of n^2 = -1 mod p^2 via Hensel
  for(long p=5;p*p<=X*X+1 && p<=X;p++){ if(comp[p]||p%4!=1) continue; unsigned long long q=(unsigned long long)p*p;
    unsigned long long t=0; for(unsigned long long a=2;;a++){ unsigned long long e=(p-1)/4, r=1, b=a%p; while(e){ if(e&1) r=r*b%p; b=b*b%p; e>>=1;} if(r*r%p==p-1){t=r;break;} }
    // lift t to mod p^2: t' = t - (t^2+1)/(2t) mod p^2
    unsigned long long f=((__uint128_t)t*t+1)%q; unsigned long long inv=0; { // inverse of 2t mod p^2
      long long a0=(2*t)%q, m=q, x0=1,x1=0; long long aa=a0, mm=m; while(mm){ long long qq=aa/mm, tmp=aa-qq*mm; aa=mm; mm=tmp; tmp=x0-qq*x1; x0=x1; x1=tmp;} inv=(x0%(long long)q+q)%q; }
    unsigned long long R=(t+q-(unsigned long long)((__uint128_t)f*inv%q))%q; unsigned long long rr[2]={R,q-R};
    for(int s=0;s<2;s++) for(unsigned long long n=rr[s];n<=(unsigned long long)X;n+=q) if(n) inV[n]=1; }
  long cnt[2][40]; memset(cnt,0,sizeof cnt); long chk=1000000;
  for(long n=1;n<=X;n++){ cnt[0][om[n]]++; if(inV[n]) cnt[1][om[n]]++;
    if(n==chk){ printf("X=%ld",n); for(int w=0;w<2;w++){ long tail=0; printf(w?"  V:":"  all:"); for(int k=12;k>=1;k--){ tail+=cnt[w][k]; if(k<=9) printf(" >=%d:%.4g",k,(double)tail/n);} } printf("\n"); fflush(stdout); chk*=10; } }
  return 0; }
