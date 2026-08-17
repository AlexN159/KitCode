"""Audited Hard data-structure Python curriculum tranche 379--383."""
from __future__ import annotations
STARTER="import sys\n\ndef solve() -> None:\n    pass\n\nif __name__ == '__main__':\n    solve()\n"; ITEMS=[]
def add(n,t,top,desc,con,hints,cx,body,cases,why):
 r=[{"input":x,"expected_output":y} for x,y in cases];ITEMS.append({"id":f"python-curated-{n:03d}","language":"python","title":t,"difficulty":"Hard","topics":top,"practice_frequency":"Common","description":desc,"constraints":con,"hints":hints,"expected_complexity":cx,"starter_code":STARTER,"solution":"import sys\n"+body+"\n\nif __name__ == '__main__':\n    solve()\n","examples":[{"input":r[0]["input"],"output":r[0]["expected_output"],"explanation":why}],"public_tests":r[:2],"hidden_tests":r[2:]})
add(379,"Segment-tree beats range chmin sum",["segment-tree","segment-tree-beats"],"Read n q, initial integers, then CHMIN l r x or SUM l r commands using zero-based inclusive ranges. CHMIN replaces each value in the range by min(value,x); SUM prints the range sum.",["1 <= n,q <= 500; values and x are signed 32-bit integers","At most 500 SUM commands; the complete input is at most 12,000 characters","All ranges satisfy 0 <= l <= r < n"],["Store the largest and second-largest values per node.","A cap affects a whole node only when it stays above its second maximum.","Push pending caps before descending."],"Amortized O((n + q) log n) time and O(n) auxiliary space",'''def solve():
 n,q=map(int,input().split());a=list(map(int,input().split()));seg=[None]*(4*n)
 def build(p,l,r):
  if l==r:seg[p]=[a[l],-10**30,1,a[l]];return
  m=(l+r)//2;build(p*2,l,m);build(p*2+1,m+1,r);pull(p)
 def pull(p):
  x,y=seg[p*2],seg[p*2+1];mx=max(x[0],y[0]);seg[p]=[mx,max(x[1] if x[0]==mx else x[0],y[1] if y[0]==mx else y[0]),(x[2] if x[0]==mx else 0)+(y[2] if y[0]==mx else 0),x[3]+y[3]]
 def cap(p,x):
  z=seg[p]
  if z[0]>x:z[3]-=(z[0]-x)*z[2];z[0]=x
 def push(p):
  cap(p*2,seg[p][0]);cap(p*2+1,seg[p][0])
 def ch(p,l,r,a,b,x):
  if b<l or r<a or seg[p][0]<=x:return
  if a<=l and r<=b and seg[p][1]<x:cap(p,x);return
  push(p);m=(l+r)//2;ch(p*2,l,m,a,b,x);ch(p*2+1,m+1,r,a,b,x);pull(p)
 def sm(p,l,r,a,b):
  if b<l or r<a:return 0
  if a<=l and r<=b:return seg[p][3]
  push(p);m=(l+r)//2;return sm(p*2,l,m,a,b)+sm(p*2+1,m+1,r,a,b)
 build(1,0,n-1)
 for _ in range(q):
  z=input().split()
  if z[0]=='CHMIN':ch(1,0,n-1,*map(int,z[1:]))
  else:print(sm(1,0,n-1,*map(int,z[1:])))''',[("3 3\n5 1 4\nSUM 0 2\nCHMIN 0 2 3\nSUM 0 2\n","10\n7"),("1 2\n9\nCHMIN 0 0 -1\nSUM 0 0\n","-1"),("4 3\n1 8 3 7\nCHMIN 1 3 5\nSUM 1 3\nSUM 0 0\n","13\n1"),("2 2\n2 2\nCHMIN 0 1 9\nSUM 0 1\n","4"),("3 2\n-1 -2 -3\nCHMIN 0 1 -2\nSUM 0 2\n","-7"),("3 2\n10 10 1\nCHMIN 0 1 4\nSUM 0 2\n","9")],"Capping five and four at three leaves 3, 1, 3.")
add(380,"Mo-with-time dynamic distinct queries",["mo-algorithm","offline-queries"],"Read n q, initial integers, then SET i x or ASK l r commands with zero-based inclusive ranges. Print the number of distinct values for every ASK in command order.",["1 <= n,q <= 600; values are signed 32-bit integers","At most 600 ASK commands; all indices and ranges are valid; the complete input is at most 12,000 characters"],["Record every update with its old value.","Sort queries by left block, right block, and update time.","Move the three pointers while maintaining frequencies."],"O((n + q)^(5/3)) time and O(n + q) auxiliary space",'''def solve():
 n,q=map(int,input().split());a=list(map(int,input().split()));now=a[:];ups=[];qs=[];ans=[]
 for _ in range(q):
  z=input().split()
  if z[0]=='SET':i,x=map(int,z[1:]);ups.append((i,now[i],x));now[i]=x
  else:l,r=map(int,z[1:]);qs.append((l,r,len(ups),len(ans)));ans.append(0)
 vals={x for x in a}
 for _,x,y in ups:vals|={x,y}
 mp={x:i for i,x in enumerate(sorted(vals))};a=[mp[x] for x in a];ups=[(i,mp[x],mp[y]) for i,x,y in ups];B=max(1,int(n**(2/3)));qs.sort(key=lambda z:(z[0]//B,z[1]//B,z[2]));f=[0]*len(mp);L=0;R=-1;T=0;d=0
 def add(i):
  nonlocal d;f[a[i]]+=1;d+=f[a[i]]==1
 def rem(i):
  nonlocal d;f[a[i]]-=1;d-=f[a[i]]==0
 def change(k,forward):
  i,old,new=ups[k];x=new if forward else old
  if L<=i<=R:rem(i);a[i]=x;add(i)
  else:a[i]=x
 for l,r,t,ix in qs:
  while T<t:change(T,1);T+=1
  while T>t:T-=1;change(T,0)
  while L>l:L-=1;add(L)
  while R<r:R+=1;add(R)
  while L<l:rem(L);L+=1
  while R>r:rem(R);R-=1
  ans[ix]=d
 print(*ans,sep=chr(10))''',[("3 4\n1 2 1\nASK 0 2\nSET 1 1\nASK 0 2\nASK 1 1\n","2\n1\n1"),("1 2\n5\nSET 0 7\nASK 0 0\n","1"),("4 3\n1 2 3 4\nASK 1 3\nSET 2 2\nASK 0 3\n","3\n3"),("2 1\n1 1\nASK 0 1\n","1"),("3 3\n1 1 2\nSET 2 1\nASK 0 2\nASK 1 2\n","1\n1"),("3 2\n-1 0 -1\nASK 0 1\nASK 0 2\n","2\n2")],"After setting index one to one, the full range has one distinct value.")
add(381,"Two-dimensional Fenwick commands",["fenwick-tree","range-queries"],"Read n m q, then ADD x y v and SUM x1 y1 x2 y2 commands on a zero-initialized grid. ADD adds v at one cell; SUM prints the inclusive rectangle sum.",["1 <= n,m <= 256 and 1 <= q <= 500","Coordinates are zero-based and valid; rectangle corners satisfy x1 <= x2 and y1 <= y2","At most 500 SUM commands; the complete input is at most 12,000 characters"],["A rectangle is four prefix sums.","Make the Fenwick structure one-indexed internally.","Update all ancestors of one point."],"O(q log n log m) time and O(nm) auxiliary space",'''def solve():
 n,m,q=map(int,input().split());b=[[0]*(m+1)for _ in range(n+1)]
 def add(x,y,v):
  x+=1;y+=1
  while x<=n:
   j=y
   while j<=m:b[x][j]+=v;j+=j&-j
   x+=x&-x
 def get(x,y):
  x+=1;y+=1;s=0
  while x:
   j=y
   while j:s+=b[x][j];j-=j&-j
   x-=x&-x
  return s
 for _ in range(q):
  z=input().split()
  if z[0]=='ADD':add(*map(int,z[1:]))
  else:
   a,c,d,e=map(int,z[1:]);print(get(d,e)-get(a-1,e)-get(d,c-1)+get(a-1,c-1))''',[("2 2 3\nADD 0 0 5\nADD 1 1 3\nSUM 0 0 1 1\n","8"),("1 3 2\nADD 0 1 -2\nSUM 0 1 0 2\n","-2"),("2 3 3\nADD 0 2 4\nADD 1 0 7\nSUM 0 1 1 2\n","4"),("1 1 1\nSUM 0 0 0 0\n","0"),("2 2 2\nADD 1 0 9\nSUM 1 0 1 0\n","9"),("2 2 3\nADD 0 0 1\nADD 0 1 2\nSUM 0 0 0 1\n","3")],"Both updated cells lie in the full rectangle.")
add(382,"Implicit-treap reverse and sum sequence",["treap","sequence-queries"],"Read n q, initial integers, then REVERSE l r or SUM l r commands using zero-based inclusive ranges. Print every sum, then print the final sequence.",["1 <= n,q <= 500; values are signed 32-bit integers","At most 500 SUM commands; all ranges are valid; the complete input is at most 12,000 characters"],["Split before l and after r.","Store subtree sizes and sums.","Lazy reverse swaps children and toggles a flag."],"Expected O((n + q) log n) time and O(n) auxiliary space",'''def solve():
 import random
 n,q=map(int,input().split());root=None
 def node(x):return [x,random.randrange(1<<30),None,None,1,x,0]
 def sz(t):return t[4] if t else 0
 def su(t):return t[5] if t else 0
 def push(t):
  if t and t[6]:t[2],t[3]=t[3],t[2];t[2] and t[2].__setitem__(6,t[2][6]^1);t[3] and t[3].__setitem__(6,t[3][6]^1);t[6]=0
 def pull(t):t[4]=1+sz(t[2])+sz(t[3]);t[5]=t[0]+su(t[2])+su(t[3])
 def split(t,k):
  if not t:return None,None
  push(t)
  if sz(t[2])>=k:a,b=split(t[2],k);t[2]=b;pull(t);return a,t
  a,b=split(t[3],k-sz(t[2])-1);t[3]=a;pull(t);return t,b
 def merge(a,b):
  if not a or not b:return a or b
  if a[1]>b[1]:push(a);a[3]=merge(a[3],b);pull(a);return a
  push(b);b[2]=merge(a,b[2]);pull(b);return b
 for x in map(int,input().split()):root=merge(root,node(x))
 for _ in range(q):
  z=input().split();l,r=map(int,z[1:]);a,b=split(root,l);b,c=split(b,r-l+1)
  if z[0]=='REVERSE':b[6]^=1
  else:print(su(b))
  root=merge(a,merge(b,c))
 out=[]
 def walk(t):
  if t:push(t);walk(t[2]);out.append(t[0]);walk(t[3])
 walk(root);print(*out)''',[("3 3\n1 2 3\nSUM 0 2\nREVERSE 0 2\nSUM 0 1\n","6\n5\n3 2 1"),("1 1\n7\nREVERSE 0 0\n","7"),("4 2\n1 2 3 4\nREVERSE 1 2\nSUM 1 3\n","9\n1 3 2 4"),("2 1\n5 6\nSUM 0 0\n","5\n5 6"),("3 2\n1 -2 3\nREVERSE 0 1\nSUM 0 2\n","2\n-2 1 3"),("3 1\n1 1 1\nREVERSE 0 2\n","1 1 1")],"Reversing the sequence makes its first two values three and two.")
add(383,"Link-cut dynamic forest path sums",["link-cut-tree","dynamic-trees"],"Read n q and node values, then LINK u v, CUT u v, SET u x, or PATH u v commands. Print the inclusive node-value sum on each PATH.",["1 <= n,q <= 500; vertices are zero-based","LINK joins different trees, CUT names an existing edge, and PATH endpoints are connected","At most 500 PATH commands; the complete input is at most 12,000 characters"],["Splay nodes represent preferred paths.","Expose a path with makeroot(u) then access(v).","Maintain subtree sums and propagate reversal flags."],"Amortized O(q log n) time and O(n) auxiliary space",'''def solve():
 n,q=map(int,input().split());val=[0]+list(map(int,input().split()));l=[0]*(n+1);r=[0]*(n+1);fa=[0]*(n+1);rev=[0]*(n+1);sm=val[:]
 def root(x):return not fa[x] or (l[fa[x]]!=x and r[fa[x]]!=x)
 def pull(x):sm[x]=val[x]+sm[l[x]]+sm[r[x]]
 def push(x):
  if rev[x]:l[x],r[x]=r[x],l[x];rev[l[x]]^=1;rev[r[x]]^=1;rev[x]=0
 def allpush(x):
  if not root(x):allpush(fa[x])
  push(x)
 def rot(x):
  y=fa[x];z=fa[y];d=(r[y]==x);b=l[x] if d else r[x]
  if not root(y):(r[z] if r[z]==y else l[z])
  if not root(y):
   if r[z]==y:r[z]=x
   else:l[z]=x
  fa[x]=z
  if d:l[x]=y;r[y]=b
  else:r[x]=y;l[y]=b
  if b:fa[b]=y
  fa[y]=x;pull(y);pull(x)
 def splay(x):
  allpush(x)
  while not root(x):
   y=fa[x]
   if not root(y):rot(x if (r[y]==x)==(r[fa[y]]==y) else y)
   rot(x)
 def access(x):
  last=0
  while x:splay(x);r[x]=last;pull(x);last=x;x=fa[x]
  return last
 def make(x):access(x);splay(x);rev[x]^=1
 def find(x):
  access(x);splay(x)
  while l[x]:push(x);x=l[x]
  splay(x);return x
 for _ in range(q):
  z=input().split();op=z[0];u=int(z[1])+1
  if op=='SET':access(u);splay(u);val[u]=int(z[2]);pull(u)
  else:
   v=int(z[2])+1
   if op=='LINK':make(u);fa[u]=v
   elif op=='CUT':make(u);access(v);splay(v);l[v]=0;fa[u]=0;pull(v)
   else:make(u);access(v);splay(v);print(sm[v])''',[("3 5\n1 2 3\nLINK 0 1\nLINK 1 2\nPATH 0 2\nSET 1 5\nPATH 0 2\n","6\n9"),("2 4\n4 7\nLINK 0 1\nPATH 0 1\nCUT 0 1\nSET 0 2\n","11"),("4 5\n1 1 1 1\nLINK 0 1\nLINK 1 2\nLINK 2 3\nPATH 1 3\nPATH 0 0\n","3\n1"),("2 3\n-1 2\nLINK 0 1\nSET 0 3\nPATH 0 1\n","5"),("3 5\n2 3 4\nLINK 0 1\nLINK 1 2\nCUT 1 2\nLINK 0 2\nPATH 1 2\n","9"),("1 1\n8\nPATH 0 0\n","8")],"The initial path contains values one, two, and three.")
PYTHON_CURATED_379_383=ITEMS
