// fast848.c -- exact recomputation of the same four case bounds as ../e848cases.c, faster and O(N) memory.
// Per b in V, for each needed class t in {7,18}: a bitset over j (a = 25j+t <= X) of a with ab+1 non-squarefree.
//  * p = 2,3 : periodic pattern in j (period 36), tiled.
//  * 7 <= p <= P (p != 5, p | b skipped): a == -b^{-1} (mod p^2), stepped through the class (as before).
//  * p > P : ab+1 = m p^2 with m <= M = (bX+1)/(P+1)^2. For each m (gcd(m,b)=1) solve s^2 == m^{-1} (mod b)
//            (factor b with an spf sieve, sqrt mod prime powers, CRT), walk s = r + kb in (P, sqrt((bX+1)/m)],
//            keep prime s, set bit for a = (m s^2 - 1)/b if a <= X and a == t (mod 25).
//  Bits are OR-ed, so duplicates are harmless; count = popcount = exact H_t(b) (same definition as e848cases).
//  Only running maxima per bin edge are kept (no nv*K arrays).
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
static u32 *spf; static uint8_t *isprime; static u64 X;
static double CP=1.0;
// sqrt of x mod q (odd prime), x a QR, q∤x. nonres = a fixed non-residue mod q.
static u64 tonelli(u64 x,u64 q,u64 nr){
  if(q%4==3) return powmod(x,(q+1)/4,q);
  u64 Q=q-1; int S=0; while(!(Q&1)){Q>>=1;S++;}
  u64 z=powmod(nr,Q,q), c=z, R=powmod(x,(Q+1)/2,q), t=powmod(x,Q,q); int M=S;
  while(t!=1){int i=0; u64 tt=t; while(tt!=1){tt=mulmod(tt,tt,q);i++;}
    u64 bb=c; for(int k=0;k<M-i-1;k++) bb=mulmod(bb,bb,q);
    M=i; c=mulmod(bb,bb,q); t=mulmod(t,c,q); R=mulmod(R,bb,q);} return R;}
// roots of s^2 == x (mod q^e); returns count, writes into out
static int sqrt_pp(u64 x,u64 q,int e,u64 qe,u64 nr,u64*out){
  if(q==2){ x%=qe; if(e==1){out[0]=1%qe;return 1;}
    if(e==2){ if(x%4!=1)return 0; out[0]=1;out[1]=3;return 2;}
    if(x%8!=1) return 0; u64 r=1; for(int k=3;k<e;k++){ u64 mk=(1ULL<<(k+1)); if((r*r-x)%mk) r+=1ULL<<(k-1);} r%=qe;
    u64 h=qe/2; out[0]=r; out[1]=qe-r; out[2]=(r+h)%qe; out[3]=(qe-r+h)%qe; return 4;}
  u64 xq=x%q; if(xq==0) return 0; if(powmod(xq,(q-1)/2,q)!=1) return 0;
  u64 r=tonelli(xq,q,nr); u64 xm=x%qe;
  for(int it=0;it<e;it++){ u64 f=(mulmod(r,r,qe)+qe-xm)%qe; if(!f)break; r=(r+qe-mulmod(f,invmod((2*r)%qe,qe),qe))%qe; }
  out[0]=r; out[1]=(qe-r)%qe; return (out[0]==out[1])?1:2;}

int main(int argc,char**argv){
  X=strtoull(argv[1],0,10); u64 E0=argc>2?strtoull(argv[2],0,10):3806; if(argc>3) CP=atof(argv[3]);
  spf=calloc(X+2,4); isprime=calloc(X+2,1);
  u64*pr=malloc(sizeof(u64)*(X/2+10)); u64 np=0;
  for(u64 i=2;i<=X+1;i++){ if(!spf[i]){spf[i]=(u32)i; isprime[i]=1; if(i<=X) pr[np++]=i; if(i*i<=X+1) for(u64 j=i*i;j<=X+1;j+=i) if(!spf[j])spf[j]=(u32)i;} }
  char*V=calloc(X+1,1);
  for(u64 k=0;k<np;k++){u64 p=pr[k]; if(p%4!=1)continue; u64 q=p*p; u64 t=0;
    for(u64 c=2;;c++){t=powmod(c,(p-1)/4,p); if(mulmod(t,t,p)==p-1)break;}
    u64 f=(mulmod(t,t,q)+1)%q; u64 R=(t+q-mulmod(f,invmod((2*t)%q,q),q))%q;
    if((mulmod(R,R,q)+1)%q){fprintf(stderr,"hensel fail\n");return 1;}
    u64 rr[2]={R,q-R}; for(int s=0;s<2;s++) for(u64 x=rr[s];x<=X;x+=q) V[x]=1; }
  u64*E=malloc(sizeof(u64)*200000); int K=0; E[K++]=E0;
  while(E[K-1]<X){u64 w=E[K-1]/100; if(w<25)w=25; u64 n=E[K-1]+w; if(n>X)n=X; E[K++]=n;}
  u64 nv=0; for(u64 x=1;x<=X;x++) if(V[x]) nv++;
  u64*vl=malloc(8*nv); {u64 j=0; for(u64 x=1;x<=X;x++) if(V[x]) vl[j++]=x;}
  fprintf(stderr,"X=%lu primes=%lu |V|=%lu bins=%d\n",X,np,nv,K);
  // 8 running maxima per edge: 0:m1 1:m2 2:m3a 3:m3b 4:m3c 5:m3d 6:m4a 7:m4b
  u32*GM=calloc((size_t)8*K,4);
  u64 nj[2]; nj[0]=(X>=7)?(X-7)/25+1:0; nj[1]=(X>=18)?(X-18)/25+1:0;
  u64 inv25[200]; // not used
  (void)inv25;
  #pragma omp parallel
  {
    u32*LM=calloc((size_t)8*K,4);
    u64 W=(nj[0]+63)/64+40; u64*bs[2]; bs[0]=malloc(8*W); bs[1]=malloc(8*W);
    u32*c7=malloc(4*K),*c18=malloc(4*K),*codd=malloc(4*K);
    #pragma omp for schedule(dynamic,16)
    for(u64 jb=0;jb<nv;jb++){
      u64 b=vl[jb]; int cb=b%25; int need[2]={cb!=7, cb!=18}; int tv[2]={7,18};
      u64 bX1=b*X+1; // <= 1e16 for X<=1e8
      u64 P=(u64)(CP*cbrt((double)bX1)); if(P<7)P=7; if(P*P>bX1) P=(u64)sqrt((double)bX1)+1;
      // factor b
      u64 fq[16],fqe[16],fnr[16]; int fe[16],nf=0; {u64 y=b; while(y>1){u64 q=spf[y]; int e=0; u64 qe=1; while(y%q==0){y/=q;e++;qe*=q;}
        fq[nf]=q; fe[nf]=e; fqe[nf]=qe; u64 nr=2; if(q>2) while(powmod(nr,(q-1)/2,q)==1) nr++; fnr[nf]=nr; nf++;}}
      for(int ci=0;ci<2;ci++){ if(!need[ci]) continue; int t=tv[ci]; u64 n=nj[ci]; u64 nw=(n+63)/64; u64*B=bs[ci];
        // pattern for p=2,3 over j mod 36 : a=25j+t
        u64 pat[36]; memset(pat,0,sizeof pat);
        int bad[36]; for(int j=0;j<36;j++){ u64 a=25*j+t; bad[j]= ((a*b+1)%4==0) || ((a*b+1)%9==0); }
        // bits g in 0..2303, word w=g/64 ; j==g mod 36
        for(int g=0;g<2304;g++) if(bad[g%36]) pat[g/64]|=1ULL<<(g%64);
        for(u64 w=0;w<nw;w++) B[w]=pat[w%36];
        if(n%64) B[nw-1]&=(1ULL<<(n%64))-1;
        // medium primes
        for(u64 k=3;k<np;k++){ u64 p=pr[k]; if(p>P)break; if(p==5||b%p==0) continue; u64 q=p*p;
          u64 r=q-invmod(b%q,q); if(r==q)r=0;
          // a = r + q*kk == t mod 25 ; j=(a-t)/25 ; step in j is q
          u64 kk=mulmod((t+25-(r%25))%25, invmod(q%25,25),25); u64 a=r+q*kk; if(a<(u64)t) a+=25*q; // a>=t
          for(u64 j=(a-t)/25;j<n;j+=q) B[j>>6]|=1ULL<<(j&63); }
      }
      // large primes p>P via m
      if(need[0]||need[1]){
        u64 M=bX1/((P+1)*(P+1));
        u64 roots[1<<12], tmp[1<<12], pr_r[4];
        for(u64 m=1;m<=M;m++){
          int nroots=1; roots[0]=0; u64 mod=1; int okm=1;
          if(b==1){ roots[0]=0; }
          for(int f=0;f<nf&&okm;f++){ u64 qe=fqe[f]; u64 mm=m%qe; if(mm%fq[f]==0){okm=0;break;}
            u64 x=invmod(mm,qe); int c=sqrt_pp(x,fq[f],fe[f],qe,fnr[f],pr_r); if(!c){okm=0;break;}
            // CRT combine roots (mod mod) with pr_r (mod qe)
            u64 i1=invmod(mod%qe,qe); int nn=0;
            for(int i=0;i<nroots;i++) for(int u=0;u<c;u++){ u64 r0=roots[i]; u64 d=(pr_r[u]+qe-(r0%qe))%qe; u64 kq=mulmod(d,i1,qe); tmp[nn++]=r0+mod*kq; }
            mod*=qe; nroots=nn; memcpy(roots,tmp,8*nn); }
          if(!okm) continue;
          u64 smax=(u64)sqrtl((long double)(bX1/m)); while((u128)(smax+1)*(smax+1)*m<=bX1) smax++; while((u128)smax*smax*m>bX1) smax--;
          for(int i=0;i<nroots;i++){ u64 s=roots[i]%b; if(b==1) s=0;
            if(s<=P){ u64 d=(P-s)/b+1; s+=d*b; }
            for(;s<=smax;s+=b){ if(!isprime[s]) continue; u64 v=m*s*s-1; u64 a=v/b; if(a>X||a==0) continue; int ar=a%25;
              if(ar==7&&need[0]){u64 j=(a-7)/25; bs[0][j>>6]|=1ULL<<(j&63);} else if(ar==18&&need[1]){u64 j=(a-18)/25; bs[1][j>>6]|=1ULL<<(j&63);} } }
        }
      }
      // cumulative counts at edges (only k with E_k >= b matter)
      int k0=0; while(E[k0]<b) k0++;
      memset(codd,0,4*K);
      for(int ci=0;ci<2;ci++){ u32*dst=ci?c18:c7; if(!need[ci]){ memset(dst,0,4*K); continue; }
        int t=tv[ci]; u64*B=bs[ci]; u64 n=nj[ci]; u64 cnt=0,codd_c=0; u64 j=0;
        // odd a = 25j+t odd <=> j odd (t=7) / j even? 25j+7 odd <=> j even ; 25j+18 odd <=> j odd
        u64 oddmask = (t==7)?0x5555555555555555ULL:0xAAAAAAAAAAAAAAAAULL;
        for(int k=0;k<K;k++){ u64 jm = (E[k]>=(u64)t)? (E[k]-t)/25+1 : 0; if(jm>n) jm=n;
          while(j+64<=jm){ u64 w=B[j>>6]; cnt+=__builtin_popcountll(w); codd_c+=__builtin_popcountll(w&oddmask); j+=64; }
          u64 extra=0,extrao=0; if(jm>j){ u64 w=B[j>>6]&((1ULL<<(jm-j))-1); extra=__builtin_popcountll(w); extrao=__builtin_popcountll(w&oddmask);} // j multiple of 64
          dst[k]=(u32)(cnt+extra);
          codd[k]+=(u32)(codd_c+extrao);
        }
      }
      if(!need[0]) { /* codd from C18 only, handled */ }
      for(int k=k0;k<K;k++){ u32*L=LM+8*k; u32 h7=c7[k],h18=c18[k],ho=codd[k];
        if(cb!=7&&cb!=18){ if(!(b&1)){ if(h7+h18>L[0])L[0]=h7+h18; } else { if(ho>L[1])L[1]=ho; if(h7>L[2])L[2]=h7; if(h18>L[4])L[4]=h18; } }
        else if(cb==7){ if(h18>L[7])L[7]=h18; if(!(b&1)&&h18>L[3])L[3]=h18; }
        else { if(h7>L[6])L[6]=h7; if(!(b&1)&&h7>L[5])L[5]=h7; } }
    }
    #pragma omp critical
    { for(size_t i=0;i<(size_t)8*K;i++) if(LM[i]>GM[i]) GM[i]=LM[i]; }
  }
  u64 vR=0,vRo=0,x=0; int ok=1; u64 firstfail=0; int verbose=getenv("ALL")!=0;
  for(int k=0;k<K;k++){ u64 N=E[k];
    for(;x<N;){x++; if(V[x]&&x%25!=7&&x%25!=18){vR++; if(x&1)vRo++;}}
    u32*L=GM+8*k;
    u64 S1=vR+L[0],S2=vRo+L[1],S3=vRo+((L[2]+L[3])>(L[4]+L[5])?(L[2]+L[3]):(L[4]+L[5])),S4=L[6]+L[7];
    u64 F=S1; if(S2>F)F=S2; if(S3>F)F=S3; if(S4>F)F=S4;
    u64 c7N=N>=7?(N-7)/25+1:0; u64 lo=(k==0)?N:E[k-1]+1; u64 c7lo=lo>=7?(lo-7)/25+1:0; int good=F<=c7lo;
    if(verbose||k==0||k==K-1||!good||k%40==0)
      printf("N=%lu c7(N)=%lu c7(lo)=%lu  S1=%lu S2=%lu S3=%lu S4=%lu  F=%lu  %s\n",N,c7N,c7lo,S1,S2,S3,S4,F,good?"ok":"FAIL");
    if(!good&&ok){ok=0;firstfail=N;} }
  if(ok) printf("CERTIFIED: case bounds <= c7 on every block up to N=%lu\n",X); else printf("first failing block ends at N=%lu\n",firstfail);
  return 0;
}
