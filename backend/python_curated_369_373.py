"""Audited Hard number-theory Python curriculum tranche 369--373."""
from __future__ import annotations

STARTER="import sys\n\ndef solve() -> None:\n    pass\n\nif __name__ == '__main__':\n    solve()\n"; ITEMS=[]
def add(n,t,top,desc,con,hints,cx,body,cases,why):
 r=[{"input":x,"expected_output":y} for x,y in cases]; ITEMS.append({"id":f"python-curated-{n:03d}","language":"python","title":t,"difficulty":"Hard","topics":top,"practice_frequency":"Common","description":desc,"constraints":con,"hints":hints,"expected_complexity":cx,"starter_code":STARTER,"solution":"import sys\n"+body+"\n\nif __name__ == '__main__':\n    solve()\n","examples":[{"input":r[0]["input"],"output":r[0]["expected_output"],"explanation":why}],"public_tests":r[:2],"hidden_tests":r[2:]})

add(369,"Generalized Chinese remainder solution",["number-theory","chinese-remainder-theorem"],"Read k, then k lines a m. Solve x congruent to a modulo m for every line and print the smallest nonnegative solution, or IMPOSSIBLE.",["1 <= k <= 100 and 1 <= m <= 1,000,000,000; a is a signed 64-bit integer","Moduli need not be coprime","The least common multiple of all input moduli is at most 10^18"],["Merge one congruence into the current solution at a time.","A merge is possible only when residues agree modulo the gcd.","Use a modular inverse after dividing both moduli by that gcd."],"O(k log M) time and O(1) auxiliary space, where M is the largest modulus",'''def solve():
 from math import gcd
 k=int(input());x=0;mod=1
 for _ in range(k):
  a,m=map(int,input().split());a%=m;g=gcd(mod,m)
  if (a-x)%g:print('IMPOSSIBLE');return
  q=m//g;t=0 if q==1 else ((a-x)//g*pow(mod//g,-1,q))%q
  x=(x+mod*t)%(mod*q);mod*=q
 print(x)''',[("2\n2 3\n3 5\n","8"),("2\n1 4\n3 6\n","9"),("2\n0 2\n1 2\n","IMPOSSIBLE"),("2\n-1 5\n2 3\n","14"),("1\n0 1\n","0"),("2\n2 4\n6 8\n","6")],"Eight leaves remainder two modulo three and three modulo five.")
add(370,"Prime-modulus discrete logarithm",["number-theory","baby-step-giant-step"],"Read prime p and integers a b with 1 <= a,b < p. Print the smallest nonnegative x such that a^x is congruent to b modulo p, or -1 if no such x exists.",["2 <= p <= 1,000,000,007 and p is prime","1 <= a,b < p","The square root table has at most 31,624 entries"],["Store powers a^j for a short baby-step range.","Multiply b by repeated inverse giant steps.","Keep the first exponent for each stored power."],"O(sqrt(p) log p) time and O(sqrt(p)) auxiliary space",'''def solve():
 from math import isqrt
 p,a,b=map(int,input().split());n=isqrt(p-1)+1;baby={};v=1
 for j in range(n):
  if v not in baby:baby[v]=j
  v=v*a%p
 step=pow(pow(a,n,p),p-2,p);v=b
 for i in range(n+1):
  if v in baby:
   x=i*n+baby[v]
   if x<p:print(x);return
  v=v*step%p
 print(-1)''',[("17 3 13\n","4"),("7 3 2\n","2"),("5 2 3\n","3"),("7 2 3\n","-1"),("11 10 10\n","1"),("2 1 1\n","0")],"Three to the fourth power is thirteen modulo seventeen.")
add(371,"Tonelli-Shanks least modular root",["number-theory","tonelli-shanks"],"Read odd prime p and integer a. Print the smallest r in [0,p) with r squared congruent to a modulo p, or -1 if no root exists.",["3 <= p <= 1,000,000,007 and p is prime","0 <= a < p"],["Euler's criterion detects a non-residue.","Factor p-1 into an odd part times a power of two.","Choose the smaller of the two roots at the end."],"O(log^2 p) time and O(1) auxiliary space",'''def solve():
 p,a=map(int,input().split());a%=p
 if a==0:print(0);return
 if pow(a,(p-1)//2,p)!=1:print(-1);return
 if p%4==3:r=pow(a,(p+1)//4,p);print(min(r,p-r));return
 q=p-1;s=0
 while q%2==0:q//=2;s+=1
 z=2
 while pow(z,(p-1)//2,p)!=p-1:z+=1
 c=pow(z,q,p);r=pow(a,(q+1)//2,p);t=pow(a,q,p);m=s
 while t!=1:
  i=1;v=t*t%p
  while v!=1:v=v*v%p;i+=1
  b=pow(c,1<<(m-i-1),p);r=r*b%p;t=t*b*b%p;c=b*b%p;m=i
 print(min(r,p-r))''',[("13 10\n","6"),("7 2\n","3"),("7 5\n","-1"),("11 0\n","0"),("17 4\n","2"),("41 9\n","3")],"Six squared is ten modulo thirteen.")
add(372,"NTT polynomial convolution",["number-theory","number-theoretic-transform"],"Read n m, then n and m coefficient lines. Multiply the two polynomials modulo 998244353 and print coefficients from degree zero upward.",["1 <= n,m and n + m - 1 <= 1,500","Every coefficient is an integer from 0 through 998244352; the complete input is at most 12,000 characters","All arithmetic uses modulus 998244353"],["Pad both coefficient lists to a power of two.","Use primitive root three for the transform.","Invert the transform and trim to n+m-1 coefficients."],"O((n + m) log(n + m)) time and O(n + m) auxiliary space",'''def solve():
 mod=998244353;root=3;n,m=map(int,input().split());a=list(map(int,input().split()));b=list(map(int,input().split()));size=1
 while size<n+m-1:size*=2
 a+= [0]*(size-n);b+= [0]*(size-m)
 def ntt(v,invert):
  j=0
  for i in range(1,len(v)):
   bit=len(v)>>1
   while j&bit:j^=bit;bit>>=1
   j^=bit
   if i<j:v[i],v[j]=v[j],v[i]
  length=2
  while length<=len(v):
   wlen=pow(root,(mod-1)//length,mod)
   if invert:wlen=pow(wlen,mod-2,mod)
   for i in range(0,len(v),length):
    w=1
    for j in range(i,i+length//2):
     u=v[j];z=v[j+length//2]*w%mod;v[j]=(u+z)%mod;v[j+length//2]=(u-z)%mod;w=w*wlen%mod
   length*=2
  if invert:
   inv=pow(len(v),mod-2,mod)
   for i in range(len(v)):v[i]=v[i]*inv%mod
 ntt(a,False);ntt(b,False)
 for i in range(size):a[i]=a[i]*b[i]%mod
 ntt(a,True);print(*a[:n+m-1])''',[("2 2\n1 2\n3 4\n","3 10 8"),("1 3\n0\n5 6 7\n","0 0 0"),("3 3\n1 1 1\n1 1 1\n","1 2 3 2 1"),("1 1\n998244352\n2\n","998244351"),("3 2\n2 0 1\n3 4\n","6 8 3 4"),("2 2\n1 998244352\n1 1\n","1 0 998244352")],"The constant, linear, and quadratic coefficients are 3, 10, and 8.")
add(373,"Mobius coprime index-pair count",["number-theory","mobius-function"],"Read n then n positive integers. Count unordered index pairs whose two values have gcd exactly one and print the count.",["1 <= n <= 200,000","1 <= each value <= 200,000","Equal values at different indices are separate elements"],["Count how many input values are divisible by every d.","Use the Mobius coefficient for each d.","A divisor contributes mu(d) times the number of pairs of its multiples."],"O(A log A) time and O(A) auxiliary space, where A is the maximum input value",'''def solve():
 n=int(input());a=list(map(int,input().split()));mx=max(a);freq=[0]*(mx+1)
 for x in a:freq[x]+=1
 mu=[0]*(mx+1);mu[1]=1;pr=[];comp=[0]*(mx+1)
 for i in range(2,mx+1):
  if not comp[i]:pr.append(i);mu[i]=-1
  for p in pr:
   if i*p>mx:break
   comp[i*p]=1
   if i%p==0:mu[i*p]=0;break
   mu[i*p]=-mu[i]
 ans=0
 for d in range(1,mx+1):
  count=sum(freq[j] for j in range(d,mx+1,d));ans+=mu[d]*count*(count-1)//2
 print(ans)''',[("4\n1 2 3 4\n","5"),("3\n2 4 6\n","0"),("1\n1\n","0"),("4\n2 3 5 7\n","6"),("3\n6 10 15\n","0"),("4\n2 3 4 9\n","4")],"All pairs except the pair 2 and 4 are coprime.")
PYTHON_CURATED_369_373=ITEMS
