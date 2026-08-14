"""Final advanced, data-only Python curriculum tranche 181--200."""
from __future__ import annotations

STARTER="import sys\n\ndef solve() -> None:\n    pass\n\nif __name__ == '__main__':\n    solve()\n"; ITEMS=[]
def add(n,t,d,top,desc,con,hints,cx,body,cases,why):
 r=[{"input":x,"expected_output":y} for x,y in cases]; ITEMS.append({"id":f"python-curated-{n:03d}","language":"python","title":t,"difficulty":d,"topics":top,"interview_frequency":"Common","description":desc,"constraints":con,"hints":hints,"expected_complexity":cx,"starter_code":STARTER,"solution":"import sys\n"+body+"\n\nif __name__ == '__main__':\n    solve()\n","examples":[{"input":r[0]["input"],"output":r[0]["expected_output"],"explanation":why}],"public_tests":r[:2],"hidden_tests":r[2:]})

add(181,"Trie autocomplete ranked suggestions","Hard",["trie","strings"],"Read n distinct lowercase words then q nonempty lowercase prefixes. Print up to three matches per prefix, ordered by shorter length then lexicographically, or -.",["1 <= n,q <= 50,000","Every prefix is nonempty; all words and prefixes are lowercase","Total input characters <= 200,000 and total output is at most 60,000 characters"],["Insert ranked words.","Store three candidates per node.","Missing edge means none."],"O(W log n + P + R) time and O(W) auxiliary space, where W is total word length, P is total prefix length, and R is output size","""def solve():
 n=int(input()); root={}
 for w in sorted([input().strip() for _ in range(n)],key=lambda x:(len(x),x)):
  z=root
  for c in w:
   z=z.setdefault(c,{}); z.setdefault('$',[])
   if len(z['$'])<3:z['$'].append(w)
 for _ in range(int(input())):
  z=root
  for c in input().strip():
   if z is None or c not in z:z=None;break
   z=z[c]
  print(' '.join(z.get('$',[])) if z else '-')""",[("4\ncar\ncat\ncart\ndog\n3\nca\ncar\nz\n","car cat cart\ncar cart\n-"),("1\na\n2\na\nb\n","a\n-"),("3\nape\napp\napple\n1\nap\n","ape app apple"),("2\naa\nab\n1\na\n","aa ab"),("3\nzoo\nzone\nz\n1\nz\n","z zoo zone"),("2\nabc\nabd\n1\nabc\n","abc")],"The prefix ca has three ranked completions.")
add(182,"Suffix-array substring positions","Hard",["suffix-array","strings"],"Read a nonempty lowercase text then q nonempty lowercase patterns. Print count and sorted zero-based starts, or 0.",["1 <= text length <= 20,000 and all strings are lowercase","1 <= q <= 4,000 and total pattern length <= 100,000","Across all queries, at most 8,000 occurrence positions are reported"],["Sort suffixes.","Search a contiguous suffix range.","Positions are numeric order."],"O(n log^2 n + P log n + sum(k log k)) time and O(n + max(k)) auxiliary space, where P is total pattern length and k is a query's match count","""def solve():
 s=input().strip();n=len(s);sa=list(range(n));r=[ord(c)for c in s];k=1
 while k<n:
  sa.sort(key=lambda i:(r[i],r[i+k]if i+k<n else -1));nr=[0]*n
  for j in range(1,n):nr[sa[j]]=nr[sa[j-1]]+((r[sa[j]],r[sa[j]+k]if sa[j]+k<n else -1)!=(r[sa[j-1]],r[sa[j-1]+k]if sa[j-1]+k<n else -1))
  r=nr;k*=2
 for _ in range(int(input())):
  p=input().strip();lo=0;hi=n
  while lo<hi:
   md=(lo+hi)//2
   if s[sa[md]:sa[md]+len(p)]<p:lo=md+1
   else:hi=md
  L=lo;lo=0;hi=n
  while lo<hi:
   md=(lo+hi)//2
   if s[sa[md]:sa[md]+len(p)]<=p:lo=md+1
   else:hi=md
  a=sorted(sa[L:lo]);print(len(a),*a) if a else print(0)""",[("banana\n3\nana\nna\nx\n","2 1 3\n2 2 4\n0"),("aaaa\n2\naa\naaaa\n","3 0 1 2\n1 0"),("abc\n2\na\nc\n","1 0\n1 2"),("mississippi\n2\nissi\nss\n","2 1 4\n2 2 5"),("z\n2\nz\nzz\n","1 0\n0"),("ababab\n2\nab\nbab\n","3 0 2 4\n2 1 3")],"Ana occurs at one and three.")
add(183,"Rabin-Karp overlapping match starts","Medium",["rolling-hash","strings"],"Read text and pattern. Print all zero-based occurrence starts, including overlaps, or -.",["1 <= pattern length <= 250 and pattern length <= text length <= 200,000","Text and pattern are printable ASCII without leading or trailing whitespace","There are at most 8,000 occurrence starts"],["Slide one position at a time.","Hash windows.","Verify a hash candidate."],"O((n-m+1)m) worst-case time, O(k) space for the reported starts","""def solve():
 s=input().strip();p=input().strip();m=len(p);B=911382323;M=1000000007;hp=hw=0;pw=1
 for i,c in enumerate(p):hp=(hp*B+ord(c))%M;hw=(hw*B+ord(s[i]))%M;pw=pw*B%M
 a=[]
 for i in range(len(s)-m+1):
  if hw==hp and s[i:i+m]==p:a.append(i)
  if i+m<len(s):hw=(hw*B+ord(s[i+m])-ord(s[i])*pw)%M
 print(*a) if a else print('-')""",[("banana\nana\n","1 3"),("aaaaa\naa\n","0 1 2 3"),("abc\nd\n","-"),("abcabc\nabc\n","0 3"),("z\nz\n","0"),("ababa\naba\n","0 2")],"Overlaps count.")
add(184,"Longest palindromic substring length","Hard",["manacher","strings"],"Read a lowercase string and print its longest contiguous palindrome length.",["1 <= length <= 200,000"],["Transform separators.","Reuse the rightmost radius.","Only print the length."],"O(n) time, O(n) space","""def solve():
 s='|'.join('^'+input().strip()+'$');p=[0]*len(s);c=r=0
 for i in range(1,len(s)-1):
  p[i]=min(r-i,p[2*c-i]) if i<r else 0
  while s[i+p[i]+1]==s[i-p[i]-1]:p[i]+=1
  if i+p[i]>r:c,r=i,i+p[i]
 print(max(p))""",[("babad\n","3"),("cbbd\n","2"),("a\n","1"),("aaaa\n","4"),("abacdfgdcaba\n","3"),("racecarx\n","7")],"Either bab or aba has length three.")
add(185,"Dinic maximum flow","Hard",["graphs","max-flow"],"Read n m s t then directed capacity edges. Print maximum s-to-t flow.",["2 <= n <= 200 and 0 <= m <= 3,000","0 <= s,t < n and s != t; parallel directed edges are allowed","Every capacity is an integer from 0 through 1,000,000"],["Add residual reverse edges.","BFS levels.","DFS a blocking flow."],"O(V^2 E) worst-case time, O(V + E) auxiliary space","""def solve():
 from collections import deque
 n,m,s,t=map(int,input().split());g=[[]for _ in range(n)]
 def ad(a,b,c):g[a].append([b,c,len(g[b])]);g[b].append([a,0,len(g[a])-1])
 for _ in range(m):ad(*map(int,input().split()))
 ans=0
 while 1:
  lv=[-1]*n;lv[s]=0;q=deque([s])
  while q:
   v=q.popleft()
   for w,c,_ in g[v]:
    if c and lv[w]<0:lv[w]=lv[v]+1;q.append(w)
  if lv[t]<0:break
  it=[0]*n
  def go(v,f):
   if v==t:return f
   while it[v]<len(g[v]):
    e=g[v][it[v]];w,c,r=e
    if c and lv[v]<lv[w]:
     z=go(w,min(f,c))
     if z:e[1]-=z;g[w][r][1]+=z;return z
    it[v]+=1
   return 0
  while (z:=go(s,10**18)):ans+=z
 print(ans)""",[("4 5 0 3\n0 1 3\n0 2 2\n1 2 1\n1 3 2\n2 3 4\n","5"),("2 1 0 1\n0 1 7\n","7"),("3 1 0 2\n0 1 5\n","0"),("4 4 0 3\n0 1 10\n1 3 1\n0 2 10\n2 3 2\n","3"),("3 3 0 2\n0 1 2\n0 1 3\n1 2 4\n","4"),("3 2 0 2\n0 2 0\n0 1 9\n","0")],"Residual paths carry five units.")
add(186,"Minimum-cost path in a DAG","Medium",["graphs","dynamic-programming"],"Read n m s t then weighted DAG edges. Print cheapest cost or IMPOSSIBLE.",["1 <= n <= 200,000 and 0 <= m <= 200,000","0 <= s,t < n; vertices are 0 through n-1","Weights are signed 32-bit integers and the directed graph is acyclic"],["Topologically order.","Relax once per edge.","Keep infinity for unreachable nodes."],"O(n + m) time, O(n + m) auxiliary space","""def solve():
 from collections import deque
 n,m,s,t=map(int,input().split());g=[[]for _ in range(n)];d=[0]*n
 for _ in range(m):a,b,w=map(int,input().split());g[a].append((b,w));d[b]+=1
 q=deque(i for i in range(n)if not d[i]);x=[10**30]*n;x[s]=0
 while q:
  v=q.popleft()
  for w,c in g[v]:
   if x[v]<10**30:x[w]=min(x[w],x[v]+c)
   d[w]-=1
   if not d[w]:q.append(w)
 print(x[t] if x[t]<10**30 else 'IMPOSSIBLE')""",[("4 4 0 3\n0 1 2\n0 2 5\n1 3 3\n2 3 -1\n","4"),("3 1 0 2\n0 1 1\n","IMPOSSIBLE"),("2 1 0 1\n0 1 -4\n","-4"),("5 5 0 4\n0 1 1\n0 2 2\n1 3 5\n2 3 1\n3 4 2\n","5"),("3 2 1 2\n0 2 1\n1 2 9\n","9"),("3 0 0 2\n","IMPOSSIBLE")],"The route through vertex two costs four.")
add(187,"Condensation graph source count","Hard",["graphs","strongly-connected-components"],"Read n m directed edges. Contract SCCs and print the number with no incoming condensation edge.",["1 <= n <= 100,000 and 0 <= m <= 200,000","Vertices are 0 through n-1; repeated directed edges are allowed"],["Find SCC labels.","Ignore internal edges.","Mark destination components."],"O(n + m) time, O(n + m) auxiliary space","""def solve():
 n,m=map(int,input().split());g=[[]for _ in range(n)];r=[[]for _ in range(n)]
 for _ in range(m):a,b=map(int,input().split());g[a].append(b);r[b].append(a)
 seen=[0]*n;o=[]
 for start in range(n):
  if seen[start]:continue
  seen[start]=1;st=[(start,0)]
  while st:
   v,i=st[-1]
   if i<len(g[v]):
    w=g[v][i];st[-1]=(v,i+1)
    if not seen[w]:seen[w]=1;st.append((w,0))
   else:o.append(v);st.pop()
 c=[-1]*n
 k=0
 for v in o[::-1]:
  if c[v]>=0:continue
  c[v]=k;st=[v]
  while st:
   x=st.pop()
   for w in r[x]:
    if c[w]<0:c[w]=k;st.append(w)
  k+=1
 inn=[0]*k
 for v in range(n):
  for w in g[v]:
   if c[v]!=c[w]:inn[c[w]]=1
 print(inn.count(0))""",[("4 4\n0 1\n1 0\n1 2\n2 3\n","1"),("3 0\n","3"),("3 3\n0 1\n1 2\n2 0\n","1"),("4 2\n0 1\n2 3\n","2"),("5 5\n0 1\n1 0\n2 3\n3 2\n3 4\n","2"),("2 1\n0 1\n","1")],"Only one SCC starts the condensation graph.")
add(188,"Tree lowest common ancestor queries","Hard",["trees","binary-lifting"],"Read n, then the n-1 edges of an undirected tree, then q vertex pairs. Root is zero; print each pair's LCA.",["1 <= n <= 100,000 and 1 <= q <= 5,000","Vertices are 0 through n-1 and the n-1 edges form one tree","The query cap keeps output below the local runner limit"],["Root the tree.","Store powers-of-two ancestors.","Lift deeper node first."],"O((n + q) log n) time, O(n log n) auxiliary space","""def solve():
 n=int(input());g=[[]for _ in range(n)]
 for _ in range(n-1):a,b=map(int,input().split());g[a]+=[b];g[b]+=[a]
 p=[0]*n;d=[0]*n;st=[0]
 for v in st:
  for w in g[v]:
   if w!=p[v]:p[w]=v;d[w]=d[v]+1;st.append(w)
 up=[p]
 while 1<<len(up)<=n:up.append([up[-1][up[-1][i]]for i in range(n)])
 for _ in range(int(input())):
  a,b=map(int,input().split())
  if d[a]<d[b]:a,b=b,a
  z=d[a]-d[b]
  for i in range(len(up)):
   if z>>i&1:a=up[i][a]
  if a!=b:
   for i in range(len(up)-1,-1,-1):
    if up[i][a]!=up[i][b]:a,b=up[i][a],up[i][b]
   a=p[a]
  print(a)""",[("5\n0 1\n0 2\n1 3\n1 4\n3\n3 4\n3 2\n1 4\n","1\n0\n1"),("1\n2\n0 0\n0 0\n","0\n0"),("3\n0 1\n1 2\n2\n2 1\n2 0\n","1\n0"),("4\n0 1\n0 2\n0 3\n1\n1 2\n","0"),("6\n0 1\n1 2\n2 3\n3 4\n4 5\n1\n5 3\n","3"),("2\n0 1\n1\n0 1\n","0")],"Three and four meet at one.")
add(189,"Kth ancestor queries","Medium",["trees","binary-lifting"],"Read n, a parent array (-1 is root), then q node-k queries. Print the kth ancestor or -1.",["1 <= n <= 200,000 and 1 <= q <= 5,000","The parent array describes one rooted tree and contains exactly one -1","0 <= k <= 10^18; the query cap bounds output"],["Use a sentinel above root.","Precompute jumps.","Read bits of k."],"O(n log n + q log k) time, O(n log n) auxiliary space","""def solve():
 n=int(input());p=[n if x<0 else x for x in map(int,input().split())]+[n];u=[p]
 for _ in range(60):u.append([u[-1][u[-1][i]]for i in range(n+1)])
 for _ in range(int(input())):
  v,k=map(int,input().split())
  for i in range(60):
   if k>>i&1:v=u[i][v]
  print(v if v<n else -1)""",[("5\n-1 0 0 1 1\n3\n3 1\n3 2\n3 3\n","1\n0\n-1"),("1\n-1\n2\n0 0\n0 1\n","0\n-1"),("3\n-1 0 1\n1\n2 2\n","0"),("4\n-1 0 1 2\n1\n3 0\n","3"),("2\n-1 0\n1\n1 100\n","-1"),("3\n-1 0 0\n1\n2 1\n","0")],"Two jumps above three reaches root.")
add(190,"Subtree add and point query","Hard",["trees","fenwick-tree"],"Read n, a parent array, n initial values, then q commands ADD v x or GET v. ADD changes every node in v's subtree; GET prints its current value.",["1 <= n,q <= 200,000 and at most 3,500 commands are GET","The parent array describes one rooted tree and contains exactly one -1","Initial values and additions are signed 32-bit integers"],["Flatten subtrees.","Use range-add differences.","Query one Euler position."],"O((n + q) log n) time, O(n) auxiliary space","""def solve():
 n=int(input());p=list(map(int,input().split()));a=list(map(int,input().split()));g=[[]for _ in a];r=p.index(-1)
 for i,x in enumerate(p):
  if x>=0:g[x].append(i)
 ti=[0]*n;to=[0]*n;st=[(r,0)];k=0
 while st:
  v,x=st.pop()
  if not x:ti[v]=k;k+=1;st.append((v,1));st.extend((w,0)for w in g[v])
  else:to[v]=k
 b=[0]*(n+2)
 def ad(i,x):
  while i<len(b):b[i]+=x;i+=i&-i
 def su(i):
  z=0
  while i:z+=b[i];i-=i&-i
  return z
 for _ in range(int(input())):
  x=input().split();v=int(x[1])
  if x[0]=='ADD':ad(ti[v]+1,int(x[2]));ad(to[v]+1,-int(x[2]))
  else:print(a[v]+su(ti[v]+1))""",[("3\n-1 0 0\n1 2 3\n2\nADD 0 5\nGET 2\n","8"),("1\n-1\n7\n2\nADD 0 -2\nGET 0\n","5"),("4\n-1 0 1 1\n0 0 0 0\n3\nADD 1 3\nGET 2\nGET 3\n","3\n3"),("2\n-1 0\n1 9\n2\nADD 1 4\nGET 0\n","1"),("2\n-1 0\n1 9\n2\nADD 0 4\nGET 1\n","13"),("3\n1 -1 1\n4 5 6\n1\nGET 0\n","4")],"Root addition reaches node two.")
add(191,"Rollback connectivity queries","Hard",["union-find","offline"],"Read n then q operations ADD u v, SNAP, ROLL, ASK u v. SNAP saves state and ROLL restores the latest unmatched snapshot; ASK prints YES or NO.",["1 <= n,q <= 100,000 and vertices are 0 through n-1","Every ROLL has a preceding unmatched SNAP","At most 5,000 operations are ASK, keeping output bounded"],["Keep only changed parent sizes.","Do not path-compress.","Rollback to stored stack length."],"O(q log n) worst-case time, O(n + q) auxiliary space","""def solve():
 n=int(input());p=list(range(n));sz=[1]*n;ch=[];sn=[]
 def f(x):
  while p[x]!=x:x=p[x]
  return x
 for _ in range(int(input())):
  z=input().split()
  if z[0]=='ADD':
   a,b=f(int(z[1])),f(int(z[2]));
   if a==b:ch.append((-1,-1,0))
   else:
    if sz[a]<sz[b]:a,b=b,a
    ch.append((b,a,sz[a]));p[b]=a;sz[a]+=sz[b]
  elif z[0]=='SNAP':sn.append(len(ch))
  elif z[0]=='ROLL':
   target=sn.pop()
   while len(ch)>target:
    b,a,s=ch.pop()
    if b>=0:p[b]=b;sz[a]=s
  else:print('YES' if f(int(z[1]))==f(int(z[2])) else 'NO')""",[("2\n3\nASK 0 1\nADD 0 1\nASK 0 1\n","NO\nYES"),("3\n5\nADD 0 1\nSNAP\nADD 1 2\nROLL\nASK 0 2\n","NO"),("3\n4\nSNAP\nADD 0 1\nROLL\nASK 0 1\n","NO"),("3\n3\nADD 0 1\nADD 1 2\nASK 0 2\n","YES"),("2\n4\nADD 0 1\nSNAP\nADD 0 1\nROLL\n",""),("1\n2\nSNAP\nROLL\n","")],"Rollback restores the last saved component state.")
add(192,"Convex hull vertex count","Hard",["geometry","convex-hull"],"Read n distinct integer points and print the number of vertices of their strict convex hull; collinear boundary points are excluded. An all-collinear set has two hull vertices.",["3 <= n <= 100,000","Coordinates are signed 32-bit integers and all points are distinct"],["Sort points.","Build lower and upper chains.","Pop non-left turns."],"O(n log n) time, O(n) auxiliary space","""def solve():
 p=sorted({tuple(map(int,input().split()))for _ in range(int(input()))})
 def cr(a,b,c):return(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 def half(q):
  h=[]
  for x in q:
   while len(h)>1 and cr(h[-2],h[-1],x)<=0:h.pop()
   h.append(x)
  return h
 print(len(half(p)[:-1]+half(p[::-1])[:-1]))""",[("4\n0 0\n1 0\n1 1\n0 1\n","4"),("3\n0 0\n1 0\n0 1\n","3"),("3\n0 0\n1 0\n2 0\n","2"),("5\n0 0\n2 0\n2 2\n0 2\n1 1\n","4"),("4\n-1 -1\n1 -1\n1 1\n-1 1\n","4"),("4\n0 0\n2 0\n1 1\n1 -1\n","4")],"A square has four hull vertices.")
add(193,"Closest pair squared distance","Hard",["geometry","divide-and-conquer"],"Read n distinct integer points; print the minimum squared Euclidean distance.",["2 <= n <= 100,000","Coordinates are signed 32-bit integers and all points are distinct"],["Split by x.","Return points sorted by y.","Compare only the y-strip."],"O(n log n) time, O(n) auxiliary space","""def solve():
 p=sorted(tuple(map(int,input().split()))for _ in range(int(input())));INF=10**100
 def go(a):
  if len(a)<=3:
   d=min(((x-u)**2+(y-v)**2 for i,(x,y) in enumerate(a) for u,v in a[i+1:]),default=INF);return d,sorted(a,key=lambda z:z[1])
  m=len(a)//2;x=a[m][0];d,l=go(a[:m]);e,r=go(a[m:]);d=min(d,e);q=[];i=j=0
  while i<len(l) or j<len(r):
   if j==len(r)or(i<len(l)and l[i][1]<=r[j][1]):q.append(l[i]);i+=1
   else:q.append(r[j]);j+=1
  z=[v for v in q if (v[0]-x)**2<d]
  for i in range(len(z)):
   for j in range(i+1,len(z)):
    if (z[j][1]-z[i][1])**2>=d:break
    d=min(d,(z[i][0]-z[j][0])**2+(z[i][1]-z[j][1])**2)
  return d,q
 print(go(p)[0])""",[("2\n0 0\n3 4\n","25"),("3\n0 0\n1 1\n9 9\n","2"),("4\n0 0\n0 3\n4 0\n4 3\n","9"),("3\n-2 -2\n-1 -2\n5 5\n","1"),("2\n7 8\n7 9\n","1"),("4\n0 0\n2 2\n3 3\n10 1\n","2")],"The only pair has squared distance 25.")
add(194,"Maximum interval overlap","Medium",["sweep-line","intervals"],"Read n half-open intervals l r. Print the greatest number simultaneously active.",["1 <= n <= 200,000","Endpoints are signed 32-bit integers and l < r"],["Create start and end events.","Process ends before starts at same point.","Track a running count."],"O(n log n) time, O(n) auxiliary space","""def solve():
 e=[]
 for _ in range(int(input())):a,b=map(int,input().split());e += [(a,1),(b,-1)]
 x=best=0
 for _,d in sorted(e,key=lambda z:(z[0],z[1])):x+=d;best=max(best,x)
 print(best)""",[("3\n1 3\n2 4\n3 5\n","2"),("1\n0 1\n","1"),("3\n0 5\n1 4\n2 3\n","3"),("2\n1 2\n2 3\n","1"),("4\n-2 2\n-1 1\n0 3\n2 4\n","3"),("3\n1 10\n2 3\n4 5\n","2")],"The endpoint at three is not overlapping.")
add(195,"Closest subset sum","Hard",["meet-in-the-middle","subsets"],"Read n and target, then exactly n integers. Print the subset sum closest to target; a tie chooses the smaller sum. The empty subset is allowed.",["1 <= n <= 36","Values and target are signed 32-bit integers"],["Split the array.","Enumerate each half.","Binary search complementary sums."],"O(2^(n/2) log 2^(n/2)) time, O(2^(n/2)) auxiliary space","""def solve():
 n,t=map(int,input().split());a=list(map(int,input().split()));m=n//2;L=[0];R=[0]
 for x in a[:m]:L += [v+x for v in L]
 for x in a[m:]:R += [v+x for v in R]
 R.sort();from bisect import bisect_left
 ans=None
 for x in L:
  k=bisect_left(R,t-x)
  for j in (k-1,k):
   if 0<=j<len(R):
    v=x+R[j]
    if ans is None or(abs(v-t),v)<(abs(ans-t),ans):ans=v
 print(ans)""",[("3 10\n3 7 20\n","10"),("2 5\n2 4\n","4"),("3 0\n-5 2 9\n","0"),("1 8\n9\n","9"),("3 6\n1 2 10\n","3"),("2 -3\n-1 -2\n","-3")],"Three plus seven hits the target.")
add(196,"Deterministic LCS reconstruction","Hard",["dynamic-programming","strings"],"Read lowercase strings a and b on separate lines. Print the lexicographically smallest longest common subsequence; print a blank line if none exists.",["0 <= both lengths <= 500","Both strings contain only lowercase English letters"],["Build suffix DP lengths.","At ties consider both next letters.","Keep lexicographic choice."],"O(nm + 26L(n + m)) time and O(nm) auxiliary space, where L is the reported subsequence length","""def solve():
 a=input().strip();b=input().strip();n=len(a);m=len(b);d=[[0]*(m+1)for _ in range(n+1)]
 for i in range(n-1,-1,-1):
  for j in range(m-1,-1,-1):d[i][j]=1+d[i+1][j+1]if a[i]==b[j]else max(d[i+1][j],d[i][j+1])
 out=[];i=j=0
 while d[i][j]:
  for c in 'abcdefghijklmnopqrstuvwxyz':
   ii=next((x for x in range(i,n)if a[x]==c),n);jj=next((x for x in range(j,m)if b[x]==c),m)
   if ii<n and jj<m and d[ii][jj]==d[i][j] and d[ii+1][jj+1]==d[i][j]-1:out.append(c);i=ii+1;j=jj+1;break
 print(''.join(out))""",[("abc\nac\n","ac"),("abc\nbac\n","ac"),("aaaa\naa\n","aa"),("abc\ndef\n",""),("axbxc\nabc\n","abc"),("ab\nba\n","a")],"Ac is the longest shared sequence.")
add(197,"Optimal binary-search-tree cost","Hard",["dynamic-programming","interval-dp"],"Read n positive search frequencies in sorted-key order. Print the minimum successful-search cost, with the root at depth one.",["1 <= n <= 300","The next line contains exactly n integer frequencies from 1 through 1,000,000"],["Choose each root.","Add interval frequency sum.","Use increasing interval length."],"O(n^3) time, O(n^2) auxiliary space","""def solve():
 n=int(input());a=list(map(int,input().split()));d=[[0]*n for _ in a]
 for L in range(1,n+1):
  for i in range(n-L+1):
   j=i+L-1;d[i][j]=sum(a[i:j+1])+min((d[i][k-1]if k>i else 0)+(d[k+1][j]if k<j else 0)for k in range(i,j+1))
 print(d[0][-1])""",[("3\n34 8 50\n","142"),("1\n7\n","7"),("2\n1 1\n","3"),("2\n10 1\n","12"),("3\n1 2 3\n","10"),("3\n3 3 3\n","15")],"Choosing the last key as root costs 142.")
add(198,"Circular stone merge minimum cost","Hard",["dynamic-programming","interval-dp"],"Read n nonnegative stone weights in a circle. Repeatedly merge adjacent piles, paying their sum; print the minimum total cost.",["2 <= n <= 200","The next line contains exactly n integers from 0 through 1,000,000"],["Duplicate the circle.","Use interval DP.","Take the best length-n interval."],"O(n^3) time, O(n^2) auxiliary space","""def solve():
 n=int(input());a=list(map(int,input().split()))*2;p=[0]
 for x in a:p.append(p[-1]+x)
 d=[[0]*(2*n)for _ in a]
 for L in range(2,n+1):
  for i in range(2*n-L+1):d[i][i+L-1]=p[i+L]-p[i]+min(d[i][k]+d[k+1][i+L-1]for k in range(i,i+L-1))
 print(min(d[i][i+n-1]for i in range(n)))""",[("3\n1 2 3\n","9"),("2\n4 5\n","9"),("3\n1 1 1\n","5"),("4\n1 2 3 4\n","19"),("3\n10 1 1\n","14"),("2\n1 100\n","101")],"Merge one and two first.")
add(199,"Bounded Sudoku solve","Hard",["backtracking","constraint-propagation"],"Read a 4 by 4 Sudoku using 0 for blank. Print the lexicographically smallest solved row-major grid, or IMPOSSIBLE when no completion exists.",["Input has exactly four rows of four integers from 0 through 4","Every completed row, column, and 2 by 2 box must contain digits 1 through 4"],["Track row, column and box choices.","Try blanks in row-major order and digits in ascending order.","Backtrack after conflicts."],"O(4^16) bounded time, O(1) auxiliary space","""def solve():
 a=[list(map(int,input().split()))for _ in range(4)]
 def ok(r,c,x):return 1<=x<=4 and x not in a[r]and all(a[k][c]!=x for k in range(4))and all(a[k][l]!=x for k in range(r//2*2,r//2*2+2)for l in range(c//2*2,c//2*2+2))
 for r in range(4):
  for c in range(4):
   x=a[r][c]
   if x:
    a[r][c]=0
    if not ok(r,c,x):print('IMPOSSIBLE');return
    a[r][c]=x
 def f():
  for i in range(16):
   r,c=divmod(i,4)
   if not a[r][c]:
    for x in range(1,5):
     if ok(r,c,x):
      a[r][c]=x
      if f():return 1
      a[r][c]=0
    return 0
  return 1
 if f():[print(*r)for r in a]
 else:print('IMPOSSIBLE')""",[("1 0 0 4\n0 4 1 0\n2 0 4 3\n4 3 0 1\n","1 2 3 4\n3 4 1 2\n2 1 4 3\n4 3 2 1"),("0 2 3 4\n3 4 0 2\n2 1 4 3\n4 3 2 1\n","1 2 3 4\n3 4 1 2\n2 1 4 3\n4 3 2 1"),("1 2 3 4\n3 4 1 2\n2 1 4 3\n4 3 2 1\n","1 2 3 4\n3 4 1 2\n2 1 4 3\n4 3 2 1"),("1 2 0 4\n3 4 1 2\n2 1 4 3\n4 3 2 0\n","1 2 3 4\n3 4 1 2\n2 1 4 3\n4 3 2 1"),("0 0 0 0\n0 0 0 0\n0 0 0 0\n0 0 0 0\n","1 2 3 4\n3 4 1 2\n2 1 4 3\n4 3 2 1"),("1 1 0 0\n0 0 0 0\n0 0 0 0\n0 0 0 0\n","IMPOSSIBLE")],"Ascending choices produce the lexicographically smallest valid grid.")
add(200,"Minimum interval stabbing points","Medium",["greedy","intervals"],"Read n closed intervals. Print the minimum number of integer points that hit every interval.",["1 <= n <= 200,000","Endpoints are signed 32-bit integers and l <= r"],["Sort by right endpoint.","Place a point at the earliest finishing uncovered interval.","That point covers later overlaps."],"O(n log n) time, O(n) auxiliary space","""def solve():
 a=sorted(tuple(map(int,input().split()))for _ in range(int(input())));p=None;c=0
 for l,r in sorted(a,key=lambda x:x[1]):
  if p is None or p<l:p=r;c+=1
 print(c)""",[("3\n1 3\n2 5\n6 7\n","2"),("1\n0 0\n","1"),("3\n1 2\n2 3\n3 4\n","2"),("3\n1 10\n2 3\n4 5\n","2"),("2\n-3 -1\n0 2\n","2"),("4\n1 2\n1 2\n2 2\n3 3\n","2")],"A point at three hits the first two intervals.")
PYTHON_CURATED_181_200=ITEMS
