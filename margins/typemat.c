// typemat.c -- exact "type-matrix" counts for Erdos 848 (refined case analysis).
// Types: tau(a) = (kappa,mu,nu): kappa = 7 / 18 / R (a mod 25), mu = even / 1 mod 4 / 3 mod 4,
//        nu = a mod 9 in {0,3,6} (one type) or 1,2,4,5,7,8  -> 3*3*7 = 63 types.
// For b in V and type t:  H_t(b,N) = #{a in V∩t, a<=N : ab+1 not squarefree}.
//   4 | ab+1 and 9 | ab+1 are constant over a in t (given b): if either holds ("forced") H = |V∩t∩[1,N]|;
//   otherwise H = #{a in V∩t : p^2 | ab+1 for some prime p>=5}  (exact; p=2,3 cannot occur).
// Output for each N in the list: M[s][t] = max_{b in V∩s, b<=N} H_t(b,N)  (0 if V∩s∩[1,N] empty), and |V∩t∩[1,N]|.
// Primes p>=5 handled exactly: p<=P by residue stepping a == -b^{-1} (mod p^2); p>P via ab+1 = m p^2 (as fast848.c).
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
typedef unsigned __int128 u128; typedef uint64_t u64; typedef int64_t i64; typedef uint32_t u32;
static u64 mulmod(u64 a,u64 b,u64 m){return (u64)((u128)a*b%m);}
static u64 powmod(u64 a,u64 e,u64 m){u64 r=1%m;a%=m;while(e){if(e&1)r=mulmod(r,a,m);a=mulmod(a,a,m);e>>=1;}return r;}
static u64 invmod(u64 a,u64 m){i64 t=0,nt=1,r=(i64)m,nr=(i64)(a%m);
  while(nr){i64 q=r/nr,tmp;tmp=t-q*nt;t=nt;nt=tmp;tmp=r-q*nr;r=nr;nr=tmp;} if(t<0)t+=(i64)m; return (u64)t;}
static u64 tonelli(u64 x,u64 q,u64 nr){
  if(q%4==3) return powmod(x,(q+1)/4,q);
  u64 Q=q-1; int S=0; while(!(Q&1)){Q>>=1;S++;}
  u64 c=powmod(nr,Q,q), R=powmod(x,(Q+1)/2,q), t=powmod(x,Q,q); int M=S;
  while(t!=1){int i=0; u64 tt=t; while(tt!=1){tt=mulmod(tt,tt,q);i++;}
    u64 bb=c; for(int k=0;k<M-i-1;k++) bb=mulmod(bb,bb,q);
    M=i; c=mulmod(bb,bb,q); t=mulmod(t,c,q); R=mulmod(R,bb,q);} return R;}
static int sqrt_pp(u64 x,u64 q,int e,u64 qe,u64 nr,u64*out){
  if(q==2){ x%=qe; if(e==1){out[0]=1%qe;return 1;}
    if(e==2){ if(x%4!=1)return 0; out[0]=1;out[1]=3;return 2;}
    if(x%8!=1) return 0; u64 r=1; for(int k=3;k<e;k++){ u64 mk=(1ULL<<(k+1)); if((r*r-x)%mk) r+=1ULL<<(k-1);} r%=qe;
    u64 h=qe/2; out[0]=r; out[1]=qe-r; out[2]=(r+h)%qe; out[3]=(qe-r+h)%qe; return 4;}
  u64 xq=x%q; if(xq==0) return 0; if(powmod(xq,(q-1)/2,q)!=1) return 0;
  u64 r=tonelli(xq,q,nr); u64 xm=x%qe;
  for(int it=0;it<e;it++){ u64 f=(mulmod(r,r,qe)+qe-xm)%qe; if(!f)break; r=(r+qe-mulmod(f,invmod((2*r)%qe,qe),qe))%qe; }
  out[0]=r; out[1]=(qe-r)%qe; return (out[0]==out[1])?1:2;}
#define NT 63
static int COARSE=0;
static int nu_idx(u64 a){if(COARSE)return 0; int r=a%9; static const int m[9]={0,1,2,0,3,4,0,5,6}; return m[r];}
static int type_of(u64 a){int k=a%25==7?0:(a%25==18?1:2); int mu=(a%2==0)?0:(a%4==1?1:2); return (k*3+mu)*7+nu_idx(a);}
// representative residues of type t: a mod 4 class and mod 9 class (nu=0 means 3|a)
static int forced(u64 b,int t){ int mu=(t/7)%3, nu=t%7;
  if(mu&&(b&1)){ int a4=(mu==1)?1:3; if((a4*(b%4)+1)%4==0) return 1; }
  if(!COARSE&&nu&&(b%3)){ static const int r9[7]={0,1,2,4,5,7,8}; if((r9[nu]*(b%9)+1)%9==0) return 1; }
  return 0; }
int main(int argc,char**argv){
  if(argc<3){fprintf(stderr,"usage: typemat X N1 [N2 ...]  (N's increasing, last = X)\n");return 1;}
  u64 X=strtoull(argv[1],0,10); int NE=argc-2; u64 EN[64]; for(int i=0;i<NE;i++) EN[i]=strtoull(argv[2+i],0,10);
  COARSE=getenv("COARSE")!=0; double CP=getenv("CP")?atof(getenv("CP")):1.0;
  u32*spf=calloc(X+2,4); uint8_t*isprime=calloc(X+2,1); u64*pr=malloc(8*(X/2+10)); u64 np=0;
  for(u64 i=2;i<=X+1;i++){ if(!spf[i]){spf[i]=(u32)i; isprime[i]=1; if(i<=X) pr[np++]=i; if(i*i<=X+1) for(u64 j=i*i;j<=X+1;j+=i) if(!spf[j])spf[j]=(u32)i;} }
  char*V=calloc(X+1,1);
  for(u64 k=0;k<np;k++){u64 p=pr[k]; if(p%4!=1)continue; u64 q=p*p; u64 t=0;
    for(u64 c=2;;c++){t=powmod(c,(p-1)/4,p); if(mulmod(t,t,p)==p-1)break;}
    u64 f=(mulmod(t,t,q)+1)%q; u64 R=(t+q-mulmod(f,invmod((2*t)%q,q),q))%q;
    if((mulmod(R,R,q)+1)%q){fprintf(stderr,"hensel fail\n");return 1;}
    u64 rr[2]={R,q-R}; for(int s=0;s<2;s++) for(u64 x=rr[s];x<=X;x+=q) V[x]=1; }
  // edge index of a: smallest e with a<=EN[e]
  uint8_t*eof=malloc(X+1); {int e=0; for(u64 a=0;a<=X;a++){ while(e<NE-1&&a>EN[e]) e++; eof[a]=(uint8_t)e; }}
  uint8_t*tof=malloc(X+1); for(u64 a=1;a<=X;a++) tof[a]=(uint8_t)type_of(a);
  u64 W=(X+64)/64; u64*Vm=calloc(W,8); for(u64 a=1;a<=X;a++) if(V[a]) Vm[a>>6]|=1ULL<<(a&63);
  static u64 vcnt[64][NT]; for(u64 a=1;a<=X;a++) if(V[a]) vcnt[eof[a]][tof[a]]++;
  for(int e=1;e<NE;e++) for(int t=0;t<NT;t++) vcnt[e][t]+=vcnt[e-1][t];
  u32*Mx=calloc((size_t)NE*NT*NT,4);
  u64*hit=malloc(8*W); u32 cnt[64][NT];
  u64 nb=0;
  for(u64 b=1;b<=X;b++){ if(!V[b]) continue; nb++;
    memset(hit,0,8*W);
    u64 bX1=b*X+1; u64 P=(u64)(CP*cbrt((double)bX1)); if(P<7)P=7; if(P*P>bX1) P=(u64)sqrt((double)bX1)+1;
    for(u64 k=(COARSE?1:2);k<np;k++){ u64 p=pr[k]; if(p>P)break; if(b%p==0) continue; u64 q=p*p;
      u64 r=q-invmod(b%q,q); if(r==q) r=0; if(r==0) r=q;
      for(u64 a=r;a<=X;a+=q) hit[a>>6]|=1ULL<<(a&63); }
    { u64 fq[16],fqe[16],fnr[16]; int fe[16],nf=0; u64 y=b; while(y>1){u64 q=spf[y]; int e=0; u64 qe=1; while(y%q==0){y/=q;e++;qe*=q;}
        fq[nf]=q; fe[nf]=e; fqe[nf]=qe; u64 nr=2; if(q>2) while(powmod(nr,(q-1)/2,q)==1) nr++; fnr[nf]=nr; nf++;}
      u64 M=bX1/((P+1)*(P+1)); static u64 roots[1<<13],tmp[1<<13]; u64 pr_r[4];
      for(u64 m=1;m<=M;m++){ int nroots=1; roots[0]=0; u64 mod=1; int okm=1;
        for(int f=0;f<nf&&okm;f++){ u64 qe=fqe[f]; u64 mm=m%qe; if(mm%fq[f]==0){okm=0;break;}
          u64 x=invmod(mm,qe); int c=sqrt_pp(x,fq[f],fe[f],qe,fnr[f],pr_r); if(!c){okm=0;break;}
          u64 i1=invmod(mod%qe,qe); int nn=0;
          for(int i=0;i<nroots;i++) for(int u=0;u<c;u++){ u64 r0=roots[i]; u64 d=(pr_r[u]+qe-(r0%qe))%qe; u64 kq=mulmod(d,i1,qe); tmp[nn++]=r0+mod*kq; }
          mod*=qe; nroots=nn; memcpy(roots,tmp,8*nn); }
        if(!okm) continue;
        u64 smax=(u64)sqrtl((long double)(bX1/m)); while((u128)(smax+1)*(smax+1)*m<=bX1) smax++; while((u128)smax*smax*m>bX1) smax--;
        for(int i=0;i<nroots;i++){ u64 s=roots[i]%b; if(s<=P){ u64 d=(P-s)/b+1; s+=d*b; }
          for(;s<=smax;s+=b){ if(!isprime[s]) continue; u128 v=(u128)m*s*s-1; if(v%b) {fprintf(stderr,"root bug\n");return 1;}
            u64 a=(u64)(v/b); if(a>X||a==0) continue; hit[a>>6]|=1ULL<<(a&63); } } } }
    memset(cnt,0,sizeof cnt);
    for(u64 w=0;w<W;w++){ u64 z=hit[w]&Vm[w]; while(z){ int k=__builtin_ctzll(z); z&=z-1; u64 a=w*64+k; cnt[eof[a]][tof[a]]++; } }
    for(int e=1;e<NE;e++) for(int t=0;t<NT;t++) cnt[e][t]+=cnt[e-1][t];
    int s=tof[b]; int fz[NT]; for(int t=0;t<NT;t++) fz[t]=forced(b,t);
    for(int e=0;e<NE;e++){ if(b>EN[e]) continue; u32*row=Mx+((size_t)e*NT+s)*NT;
      for(int t=0;t<NT;t++){ u32 h= fz[t]? (u32)vcnt[e][t] : cnt[e][t]; if(h>row[t]) row[t]=h; } }
  }
  fprintf(stderr,"X=%lu |V|=%lu\n",X,nb);
  for(int e=0;e<NE;e++){ printf("N %lu\nV",EN[e]); for(int t=0;t<NT;t++) printf(" %lu",vcnt[e][t]); printf("\n");
    for(int s=0;s<NT;s++){ for(int t=0;t<NT;t++) printf("%u ",Mx[((size_t)e*NT+s)*NT+t]); printf("\n"); } }
  return 0; }
