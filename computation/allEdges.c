// Rigorous blockwise verification of Erdős 848 via Sawhney's case analysis with EXACT counts.
//
// V = {x <= X : x^2+1 not squarefree}.  C7, C18 = residue classes 7, 18 mod 25, R = the rest.
// For a valid A (ab+1 non-squarefree for all a,b in A, a=b allowed) not inside C7 or C18:
//  S1: A∩R has an even b:              |A| <= vR(N) + max_{b in R∩V even} [H7(b)+H18(b)]
//  S2: A∩R ≠ ∅ all odd, A∩(C7∪C18) odd: |A| <= vRodd(N) + max_{b in R∩V odd} Hodd(b)
//  S3: A∩R ≠ ∅ all odd, even b' in C7:  |A| <= vRodd + max_{b R odd} H7(b) + max_{b' C7 even} H18(b')
//      (or b' in C18):                  |A| <= vRodd + max_{b R odd} H18(b) + max_{b' C18 even} H7(b')
//  S4: A∩R = ∅, A meets C7 and C18:     |A| <= max_{b' in C18∩V} H7(b') + max_{b in C7∩V} H18(b)
// where H7(b) = #{a in C7∩V, a<=N : ab+1 non-squarefree}, etc., and Hodd counts odd a in C7∪C18.
// All bounds are nondecreasing in N, so F(E_k) <= c7(E_{k-1}+1) certifies every N in (E_{k-1},E_k].
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
typedef unsigned __int128 u128; typedef uint64_t u64; typedef int64_t i64;

static u64 mulmod(u64 a,u64 b,u64 m){return (u64)((u128)a*b%m);}
static u64 powmod(u64 a,u64 e,u64 m){u64 r=1%m;a%=m;while(e){if(e&1)r=mulmod(r,a,m);a=mulmod(a,a,m);e>>=1;}return r;}
static u64 invmod(u64 a,u64 m){ // m>1, gcd(a,m)=1
  i64 t=0,nt=1; i64 r=(i64)m,nr=(i64)(a%m);
  while(nr){i64 q=r/nr,tmp; tmp=t-q*nt;t=nt;nt=tmp; tmp=r-q*nr;r=nr;nr=tmp;}
  if(t<0)t+=(i64)m; return (u64)t;}

int main(int argc,char**argv){
  u64 X=strtoull(argv[1],0,10); u64 E0=argc>2?strtoull(argv[2],0,10):3806;
  // primes up to X
  char*comp=calloc(X+1,1); u64*pr=malloc(sizeof(u64)*(X/2+10)); u64 np=0;
  for(u64 i=2;i<=X;i++){if(!comp[i]){pr[np++]=i; for(u64 j=i*i;j<=X;j+=i)comp[j]=1;}}
  free(comp);
  // V
  char*V=calloc(X+1,1);
  for(u64 k=0;k<np;k++){u64 p=pr[k]; if(p%4!=1)continue; u64 q=p*p;
    u64 t=0; for(u64 c=2;;c++){t=powmod(c,(p-1)/4,p); if(mulmod(t,t,p)==p-1)break;}
    // Hensel lift t to root mod p^2
    u64 f=(mulmod(t,t,q)+1)%q; u64 R=(t+q-mulmod(f,invmod((2*t)%q,q),q))%q;
    if((mulmod(R,R,q)+1)%q){fprintf(stderr,"hensel fail %lu\n",p);return 1;}
    u64 rr[2]={R,q-R}; for(int s=0;s<2;s++) for(u64 x=rr[s];x<=X;x+=q)V[x]=1; }
  // bin edges
  u64 *E=malloc(sizeof(u64)*100000); int K=0; E[K++]=E0;
  while(E[K-1]<X){u64 w=E[K-1]/100; if(w<25)w=25; u64 n=E[K-1]+w; if(n>X)n=X; E[K++]=n;}
  uint16_t*binof=malloc(sizeof(uint16_t)*(X+1));
  {int k=0; for(u64 a=0;a<=X;a++){while(a>E[k])k++; binof[a]=(uint16_t)k;}}
  // list of V elements
  u64 nv=0; for(u64 x=1;x<=X;x++) if(V[x]) nv++;
  u64*vl=malloc(sizeof(u64)*nv); {u64 j=0; for(u64 x=1;x<=X;x++) if(V[x]) vl[j++]=x;}
  fprintf(stderr,"X=%lu primes=%lu |V|=%lu bins=%d\n",X,np,nv,K);
  // per-b histograms: h7, h18, hodd
  uint32_t*h7=calloc((size_t)nv*K,4),*h18=calloc((size_t)nv*K,4),*ho=calloc((size_t)nv*K,4);
  if(!h7||!h18||!ho){fprintf(stderr,"oom\n");return 1;}
  #pragma omp parallel
  {
    uint32_t*stamp=calloc(X+1,4);
    #pragma omp for schedule(dynamic,64)
    for(u64 j=0;j<nv;j++){
      u64 b=vl[j]; int cb=b%25; int needC7 = (cb!=7), needC18=(cb!=18); // b in C7: only C18; b in C18: only C7
      uint32_t tag=(uint32_t)(j+1);
      u128 lim=(u128)b*X+1;
      for(u64 k=0;k<np;k++){u64 p=pr[k]; u64 q=p*p; if((u128)q>lim)break; if(b%p==0||p==5)continue;
        u64 r=q-invmod(b%q,q); if(r==q)r=0;      // a ≡ -b^{-1} (mod p^2)
        u64 qi=invmod(q%25,25);
        for(int s=0;s<2;s++){ int t=s?18:7; if(t==7&&!needC7)continue; if(t==18&&!needC18)continue;
          u64 kk=mulmod(( (t+25-(r%25))%25 ),qi,25); u64 a=r+q*kk; u64 step=25*q;
          for(;a<=X;a+=step){ if(a==0)continue; if(!V[a]||stamp[a]==tag)continue; stamp[a]=tag;
            size_t idx=(size_t)j*K+binof[a]; if(t==7)h7[idx]++; else h18[idx]++; if(a&1)ho[idx]++; } } }
      // prefix sums over bins
      for(int k=1;k<K;k++){size_t i=(size_t)j*K+k; h7[i]+=h7[i-1]; h18[i]+=h18[i-1]; ho[i]+=ho[i-1];}
    }
    free(stamp);
  }
  // evaluate case bounds at each edge
  u64 vR=0,vRo=0; u64 x=0; int ok=1; u64 firstfail=0;
  u64 prevc7=0; // c7(E_{k-1}+1)
  for(int k=0;k<K;k++){
    u64 N=E[k];
    for(;x<N;){x++; if(V[x]&&x%25!=7&&x%25!=18){vR++; if(x&1)vRo++;}}
    u64 m1=0,m2=0,m3a=0,m3b=0,m3c=0,m3d=0,m4a=0,m4b=0;
    for(u64 j=0;j<nv&&vl[j]<=N;j++){u64 b=vl[j]; int cb=b%25; size_t i=(size_t)j*K+k;
      if(cb!=7&&cb!=18){ if(!(b&1)){u64 s=h7[i]+h18[i]; if(s>m1)m1=s;}
        else { if(ho[i]>m2)m2=ho[i]; if(h7[i]>m3a)m3a=h7[i]; if(h18[i]>m3c)m3c=h18[i]; } }
      else if(cb==7){ if(h18[i]>m4b)m4b=h18[i]; if(!(b&1)&&h18[i]>m3b)m3b=h18[i]; }
      else { if(h7[i]>m4a)m4a=h7[i]; if(!(b&1)&&h7[i]>m3d)m3d=h7[i]; } }
    u64 S1=vR+m1, S2=vRo+m2, S3=vRo+((m3a+m3b)>(m3c+m3d)?(m3a+m3b):(m3c+m3d)), S4=m4a+m4b;
    u64 F=S1; if(S2>F)F=S2; if(S3>F)F=S3; if(S4>F)F=S4;
    u64 c7N = N>=7? (N-7)/25+1 : 0;
    u64 lo = (k==0)? N : E[k-1]+1; u64 c7lo = lo>=7?(lo-7)/25+1:0;
    int good = (F<=c7lo);
    if(1)
      printf("N=%lu c7(N)=%lu c7(lo)=%lu  S1=%lu S2=%lu S3=%lu S4=%lu  F=%lu  %s\n",N,c7N,c7lo,S1,S2,S3,S4,F,good?"ok":"FAIL");
    if(k>0&&!good&&ok){ok=0;firstfail=N;}
    (void)prevc7;
  }
  if(ok) printf("CERTIFIED: case bounds <= c7 on every block up to N=%lu\n",X);
  else printf("first failing block ends at N=%lu\n",firstfail);
  return 0;
}
