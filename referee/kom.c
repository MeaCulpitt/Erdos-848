// referee: K_k(N) = #{b<=N : b^2+1 not squarefree, #distinct primes>=7 dividing b >= k}
// V via: for each prime p<=X, p%4==1, find i with i^2=-1 mod p^2 by brute force mod p then Newton lift in __int128.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned long long u64; typedef __int128 i128;
static u64 pw(u64 a,u64 e,u64 m){u64 r=1;a%=m;while(e){if(e&1)r=(i128)r*a%m;a=(i128)a*a%m;e>>=1;}return r;}
int main(int c,char**v){u64 X=strtoull(v[1],0,10); int ns=c-2; u64 Q[512]; for(int i=0;i<ns;i++)Q[i]=strtoull(v[2+i],0,10);
 uint32_t*spf=calloc(X+1,4); char*V=calloc(X+1,1);
 for(u64 i=2;i<=X;i++) if(!spf[i]){ for(u64 j=i;j<=X;j+=i) if(!spf[j]) spf[j]=i;
   if(i%4==1){ u64 p=i,q=p*p,t=0; for(u64 g=2;;g++){t=pw(g,(p-1)/4,p); if((i128)t*t%p==p-1)break;}
     // lift: t' = t - (t^2+1)/(2t) mod q
     i128 f=((i128)t*t+1)%q; i128 inv=pw(2*t%q,p*(p-1)-1,q); i128 r=((i128)t - f*inv%q + q)%q;
     if(((i128)r*r+1)%q){fprintf(stderr,"lift fail %llu\n",p);return 1;}
     for(u64 x=(u64)r;x<=X;x+=q)V[x]=1; for(u64 x=q-(u64)r;x<=X;x+=q)V[x]=1; } }
 u64 K[12]={0}; int qi=0;
 for(u64 b=1;b<=X;b++){ if(V[b]){ int w=0; u64 y=b,last=0; while(y>1){u64 p=spf[y]; if(p!=last&&p>=7)w++; last=p; y/=p;} for(int k=1;k<=w&&k<12;k++)K[k]++; }
   while(qi<ns&&Q[qi]==b){ printf("%llu",b); for(int k=1;k<=8;k++)printf(" %llu",K[k]); printf("\n"); qi++; } }
 return 0;}
