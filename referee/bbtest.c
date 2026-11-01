// referee: exact integer B&B proof that max_P min_{W subset P,|W|<=2} value <= F  (see milpexact.py)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned long long u64; typedef __int128 i128;
int cat[63],mu[63],nu[63],W9[63]; u64 FM[63],Cm=0,Rm=0,C7=0,C18=0,ALL;
long long bI,aI,cI,D=1000000000000000LL; i128 Ft; long long nodes=0; int ord[63];
u64 wm[4][2]; int wv[4]={6,2,3,1};
static int wsum(u64 m){int s=0; for(int k=0;k<4;k++) s+=wv[k]*(__builtin_popcountll(m&wm[k][0])+23*__builtin_popcountll(m&wm[k][1])); return s;}
static i128 val(u64 F,u64 T){ int nC=wsum(T&Cm), nF=wsum(T&Cm&F), nR=wsum(T&Rm);
  return (i128)bI*nC+(i128)(D-bI)*nF+(i128)aI*nR+((T&Rm)?(i128)cI*900:0);}
static int forced(int s,int t){ if(cat[t]==2) return 0; if(cat[s]==cat[t]) return 1;
  if(mu[s]&&mu[t]&&(mu[s]*mu[t])%4==3) return 1; if(nu[s]%3&&nu[t]%3&&(nu[s]*nu[t])%9==8) return 1; return 0;}
i128 best_leaf=0; int ce=0;
static void rec(int k,u64 In,u64 Out){ nodes++; if((nodes&((1LL<<26)-1))==0){fprintf(stderr,"nodes %lld k=%d\n",nodes,k);}
  u64 T=ALL&~Out; if(!(T&~C7)||!(T&~C18)) return;
  if(In){ i128 b=-1; int L[63],nl=0; for(int j=0;j<63;j++) if(In>>j&1) L[nl++]=j;
    for(int a=0;a<nl;a++){ i128 v=val(FM[L[a]],T); if(b<0||v<b) b=v; if(b<=Ft) return;
      for(int c=a+1;c<nl;c++){ v=val(FM[L[a]]&FM[L[c]],T); if(v<b){b=v; if(b<=Ft) return;} } }
    if(k==63){ ce=1; if(b>best_leaf) best_leaf=b; printf("COUNTEREXAMPLE In=%llx\n",In); return; } }
  if(k==63) return;
  int j=ord[k]; rec(k+1,In|(1ULL<<j),Out); rec(k+1,In,Out|(1ULL<<j)); }
int main(int argc,char**argv){
  bI=atoll(argv[1]); aI=atoll(argv[2]); cI=atoll(argv[3]);  // ceil(x*1e15)
  int MU[3]={0,1,3}, NU[7]={0,1,2,4,5,7,8}; int n=0;
  for(int c=0;c<3;c++) for(int m=0;m<3;m++) for(int v=0;v<7;v++){cat[n]=c;mu[n]=MU[m];nu[n]=NU[v];
    int w=(m==0?(v==0?6:2):(v==0?3:1)); W9[n]=w*(c==2?23:1); int wi=(w==6?0:w==2?1:w==3?2:3); wm[wi][c==2]|=1ULL<<n;
    if(c<2)Cm|=1ULL<<n; else Rm|=1ULL<<n; if(c==0)C7|=1ULL<<n; if(c==1)C18|=1ULL<<n; n++;}
  ALL=(1ULL<<63)-1; int tot=0; for(int i=0;i<63;i++) tot+=W9[i]; if(tot!=900){printf("weights bad\n");return 1;}
  for(int i=0;i<63;i++){FM[i]=0; for(int j=0;j<63;j++) if(forced(i,j)) FM[i]|=1ULL<<j;}
  // order: fewest forced targets first, R before C on ties
  for(int i=0;i<63;i++) ord[i]=i;
  for(int i=0;i<63;i++) for(int j=i+1;j<63;j++){ int a=ord[i],b=ord[j];
    int ka=__builtin_popcountll(FM[a]&Cm)*2-(cat[a]==2), kb=__builtin_popcountll(FM[b]&Cm)*2-(cat[b]==2);
    if(kb<ka){ord[i]=b;ord[j]=a;} }
  Ft=(i128)bI*72+(i128)aI*828+(i128)cI*900-(argc>4?atoll(argv[4]):0);
  rec(0,0,0);
  printf("nodes %lld %s\n",nodes, ce?"COUNTEREXAMPLE FOUND":"PROVED: V_2 <= F (exact integer arithmetic)");
  printf("F = %.10f\n",(double)Ft/900/1e15); return 0; }
