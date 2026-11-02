// Exact bound for valid A (ab+1 never cube-free) inside neither C57 nor C68, at a given N:
//   |A| <= M57(N) + M68(N) + r(N),  Mc(N) = max over b in V3 cap [N] outside Cc of #{a in Cc cap [N] : ab+1 not cube-free},
//   r(N) = |V3 cap [N]| - c57(N) - c68(N)   (V3 = {x : x^2+1 not cube-free}; Cc = {n = c mod 125}, both inside V3).
// ab+1 not cube-free  <=>  some prime q has q^3 | ab+1; q = 2, 3, 5 and q >= 7 all handled by marking residue classes.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef long long ll; typedef unsigned long long u64; typedef __int128 i128;
static ll inv(ll a, ll m){ ll g=m,x=0,x1=1,a1=((a%m)+m)%m; while(a1){ ll q=g/a1,t=g-q*a1; g=a1; a1=t; t=x-q*x1; x=x1; x1=t; } return g==1?((x%m)+m)%m:-1; }
static u64 pw(u64 a,u64 e,u64 m){u64 r=1;a%=m;while(e){if(e&1)r=(i128)r*a%m;a=(i128)a*a%m;e>>=1;}return r;}
int main(int argc,char**argv){ ll N=atoll(argv[1]); ll Q=1; while((i128)(Q+1)*(Q+1)*(Q+1) <= (i128)N*N+1) Q++;
  char*cp=calloc(Q+2,1); ll*pr=malloc(sizeof(ll)*(Q+2)); int np=0;
  for(ll i=2;i<=Q;i++) if(!cp[i]){ pr[np++]=i; for(ll j=i*i;j<=Q;j+=i) cp[j]=1; }
  // V3 via roots of x^2 = -1 mod p^3
  char*inV=calloc(N+1,1);
  for(int k=0;k<np;k++){ ll p=pr[k]; if(p%4!=1) continue; ll p3=p*p*p; ll t=0;
    for(ll a=2;;a++){ t=pw(a,(p-1)/4,p); if((i128)t*t%p==p-1) break; }
    ll m=p; for(int s=0;s<2;s++){ ll m2=m*p; ll f=(ll)(((i128)t*t+1)%m2); ll iv=inv((2*t)%m2,m2); t=(ll)(((i128)t - (i128)f*iv%m2 + 2*m2)%m2); m=m2; }
    if(((i128)t*t+1)%p3){ fprintf(stderr,"hensel fail %lld\n",p); return 1; }
    ll r[2]={t,p3-t}; for(int s=0;s<2;s++) for(ll x=r[s];x<=N;x+=p3) if(x>0) inV[x]=1; }
  ll nV=0; for(ll x=1;x<=N;x++) nV+=inV[x];
  ll c57=N>=57?(N-57)/125+1:0, c68=N>=68?(N-68)/125+1:0;
  ll best[2]={0,0}, arg[2]={0,0}; int cls[2]={57,68};
  ll L=N/125+2; char*mk=malloc(L);
  for(int ci=0;ci<2;ci++){ ll c=cls[ci];
    for(ll b=1;b<=N;b++){ if(!inV[b] || b%125==c) continue;
      memset(mk,0,L); ll na=(N>=c)?(N-c)/125+1:0;   // a = c + 125 i, i = 0..na-1
      for(int k=-3;k<np;k++){ ll q = k==-3?2: k==-2?3: k==-1?5 : pr[k]; if(k>=0 && pr[k]<=5) continue;
        ll q3=q*q*q; if(b%q==0) continue; if((i128)q3 > (i128)N*b+1) continue;
        ll r=((-inv(b%q3,q3))%q3+q3)%q3;           // a = r mod q^3
        if(q==5){ if((c - r)%125!=0) continue;     // a = c mod 125 must agree with r mod 125
          for(ll i=0;i<na;i++) mk[i]=1; continue; }
        // a = c + 125 i = r mod q3  ->  i = (r - c) * inv(125) mod q3
        ll i0=(ll)(((i128)(((r-c)%q3+q3)%q3) * inv(125%q3,q3)) % q3);
        for(ll i=i0;i<na;i+=q3) mk[i]=1; }
      ll h=0; for(ll i=0;i<na;i++) h+=mk[i];
      if(h>best[ci]){best[ci]=h; arg[ci]=b;} } }
  ll r=nV-c57-c68;
  printf("N=%lld  |V3|=%lld  c57=%lld c68=%lld  M57=%lld (b=%lld)  M68=%lld (b=%lld)  r=%lld  bound=%lld\n",
         N,nV,c57,c68,best[0],arg[0],best[1],arg[1],r,best[0]+best[1]+r);
  return 0; }
