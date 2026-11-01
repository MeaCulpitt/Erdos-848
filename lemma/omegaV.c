// K_k(N) = #{b <= N : b^2+1 not squarefree, omega(b1) >= k},  b1 = part of b coprime to 30.  k = 1..9.
// Output: lines "N K1 K2 ... K9" at N = multiples of STEP up to X.  (b^2+1 non-squarefree iff p^2 | b^2+1 for a
// prime p ≡ 1 mod 4, p=5 included; 4∤b^2+1, 9∤b^2+1 always.)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned long long u64; typedef unsigned __int128 u128;
static u64 mulmod(u64 a,u64 b,u64 m){return (u64)((u128)a*b%m);}
static u64 powmod(u64 a,u64 e,u64 m){u64 r=1%m;a%=m;while(e){if(e&1)r=mulmod(r,a,m);a=mulmod(a,a,m);e>>=1;}return r;}
static u64 invmod(u64 a,u64 m){long long t=0,nt=1,r=(long long)m,nr=(long long)(a%m);
  while(nr){long long q=r/nr,tmp;tmp=t-q*nt;t=nt;nt=tmp;tmp=r-q*nr;r=nr;nr=tmp;} if(t<0)t+=(long long)m; return (u64)t;}
int main(int argc,char**argv){
  u64 X=strtoull(argv[1],0,10), STEP=strtoull(argv[2],0,10);
  uint8_t*om=calloc(X+1,1); uint8_t*comp=calloc(X+1,1); uint8_t*V=calloc(X+1,1);
  for(u64 i=2;i<=X;i++) if(!comp[i]){ for(u64 j=i*i;j<=X&&i<=X/i;j+=i) comp[j]=1;
      if(i>=7) for(u64 j=i;j<=X;j+=i) om[j]++;
      if(i%4==1){ u64 p=i,q=p*p; u64 t=0;
        for(u64 c=2;;c++){t=powmod(c,(p-1)/4,p); if(mulmod(t,t,p)==p-1)break;}
        u64 f=(mulmod(t,t,q)+1)%q; u64 R=(t+q-mulmod(f,invmod((2*t)%q,q),q))%q;
        u64 rr[2]={R,q-R}; for(int s=0;s<2;s++) for(u64 x=rr[s];x<=X;x+=q) V[x]=1; } }
  // primes p ≡ 1 mod 4 with p <= X are needed (p^2 | b^2+1 needs p^2 <= X^2+1): loop above covers p<=X
  u64 K[10]={0};
  for(u64 b=1;b<=X;b++){ if(V[b]) for(int k=1;k<=9;k++) if(om[b]>=k) K[k]++;
    if(b%STEP==0){ printf("%llu",b); for(int k=1;k<=9;k++) printf(" %llu",K[k]); printf("\n"); } }
  return 0; }
