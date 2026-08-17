"""Audited Hard graph and tree curriculum tranche 384--388."""
from __future__ import annotations
STARTER="import sys\n\ndef solve() -> None:\n    pass\n\nif __name__ == '__main__':\n    solve()\n";ITEMS=[]
def add(n,t,top,d,c,h,x,b,cs,w):
 r=[{'input':i,'expected_output':o}for i,o in cs];ITEMS.append({'id':f'python-curated-{n:03d}','language':'python','title':t,'difficulty':'Hard','topics':top,'practice_frequency':'Common','description':d,'constraints':c,'hints':h,'expected_complexity':x,'starter_code':STARTER,'solution':'import sys\n'+b+"\n\nif __name__ == '__main__':\n    solve()\n",'examples':[{'input':r[0]['input'],'output':r[0]['expected_output'],'explanation':w}],'public_tests':r[:2],'hidden_tests':r[2:]})
add(384,'Hopcroft-Karp bipartite matching size',['graphs','matching'],'Read L R m then m edges u v from left u to right v, all zero-based. Print the maximum matching size.',['1 <= L,R <= 800 and 0 <= m <= 1,200','Parallel edges are allowed; the complete input is at most 12,000 characters.'],['BFS layers all unmatched left vertices.','DFS only along layer-respecting edges.','Repeat until no augmenting path remains.'],'O(m sqrt(L+R)) time and O(L+R+m) space',"""def solve():
 from collections import deque
 L,R,m=map(int,input().split());g=[[]for _ in range(L)]
 for _ in range(m):a,b=map(int,input().split());g[a].append(b)
 a=[-1]*L;b=[-1]*R
 while 1:
  d=[-1]*L;q=deque(i for i in range(L)if a[i]<0)
  for i in q:d[i]=0
  while q:
   u=q.popleft()
   for v in g[u]:
    if b[v]>=0 and d[b[v]]<0:d[b[v]]=d[u]+1;q.append(b[v])
  def go(u):
   for v in g[u]:
    if b[v]<0 or(d[b[v]]==d[u]+1 and go(b[v])):a[u]=v;b[v]=u;return 1
   d[u]=-1;return 0
  z=sum(go(i)for i in range(L)if a[i]<0)
  if not z:break
 print(sum(x>=0 for x in a))""",[("2 2 3\n0 0\n0 1\n1 1\n","2"),("2 2 1\n0 0\n","1"),("1 3 3\n0 0\n0 1\n0 2\n","1"),("3 1 3\n0 0\n1 0\n2 0\n","1"),("2 2 0\n","0"),("3 3 3\n0 2\n1 1\n2 0\n","3")],'Each left vertex can receive a distinct right partner.')
add(385,'DAG minimum vertex path cover',['graphs','dag','matching'],'Read n m then directed DAG edges u v. Print the minimum number of vertex-disjoint directed paths covering every vertex.',['1 <= n <= 800 and 0 <= m <= 1,200','Vertices are zero-based and the graph is acyclic; the complete input is at most 12,000 characters.'],['Split every vertex into left and right copies.','Match an edge u to v when a path continues.','Subtract maximum matching size from n.'],'O(m sqrt(n)) time and O(n+m) space',"""def solve():
 from collections import deque
 n,m=map(int,input().split());g=[[]for _ in range(n)]
 for _ in range(m):a,b=map(int,input().split());g[a].append(b)
 a=[-1]*n;b=[-1]*n
 while 1:
  d=[-1]*n;q=deque(i for i in range(n)if a[i]<0)
  for i in q:d[i]=0
  while q:
   u=q.popleft()
   for v in g[u]:
    if b[v]>=0 and d[b[v]]<0:d[b[v]]=d[u]+1;q.append(b[v])
  def f(u):
   for v in g[u]:
    if b[v]<0 or(d[b[v]]==d[u]+1 and f(b[v])):a[u]=v;b[v]=u;return 1
   d[u]=-1;return 0
  if not sum(f(i)for i in range(n)if a[i]<0):break
 print(n-sum(x>=0 for x in a))""",[("3 2\n0 1\n1 2\n","1"),("3 0\n","3"),("4 2\n0 2\n1 2\n","3"),("4 3\n0 1\n0 2\n2 3\n","2"),("1 0\n","1"),("4 4\n0 1\n1 2\n0 2\n2 3\n","1")],'The chain covers all three vertices with one path.')
add(386,'Centroid nearest marked-node distance',['trees','centroid-decomposition'],'Read n q, n-1 tree edges, then MARK v or QUERY v. Initially node zero is marked; QUERY prints its distance to the nearest marked node.',['1 <= n,q <= 800; vertices are zero-based','At most 800 QUERY commands; the complete input is at most 12,000 characters.'],['Decompose the tree by centroids.','Record every node distance to its centroid ancestors.','A mark updates all its centroid ancestors.'],'O((n+q) log n) time and O(n log n) space',"""def solve():
 sys.setrecursionlimit(300000);n,q=map(int,input().split());g=[[]for _ in range(n)]
 for _ in range(n-1):a,b=map(int,input().split());g[a].append(b);g[b].append(a)
 dead=[0]*n;sz=[0]*n;paths=[[]for _ in range(n)]
 def size(v,p):sz[v]=1
  # recursion body below
 def dfs(v,p):
  sz[v]=1
  for w in g[v]:
   if w!=p and not dead[w]:sz[v]+=dfs(w,v)
  return sz[v]
 def cen(v,p,tot):
  for w in g[v]:
   if w!=p and not dead[w] and sz[w]*2>tot:return cen(w,v,tot)
  return v
 def dist(v,p,d,c):
  paths[v].append((c,d))
  for w in g[v]:
   if w!=p and not dead[w]:dist(w,v,d+1,c)
 def build(v):
  c=cen(v,-1,dfs(v,-1));dead[c]=1;dist(c,-1,0,c)
  for w in g[c]:
   if not dead[w]:build(w)
 build(0);best=[10**9]*n
 def mark(v):
  for c,d in paths[v]:best[c]=min(best[c],d)
 def ask(v):return min(best[c]+d for c,d in paths[v])
 mark(0)
 for _ in range(q):
  z=input().split();v=int(z[1]);mark(v) if z[0]=='MARK' else print(ask(v))""",[("3 3\n0 1\n1 2\nQUERY 2\nMARK 2\nQUERY 1\n","2\n1"),("1 1\nQUERY 0\n","0"),("4 2\n0 1\n0 2\n0 3\nQUERY 3\nQUERY 2\n","1\n1"),("3 2\n0 1\n1 2\nMARK 1\nQUERY 2\n","1"),("2 1\n0 1\nQUERY 1\n","1"),("4 3\n0 1\n1 2\n2 3\nMARK 3\nQUERY 2\nQUERY 0\n","1\n0")],'Node two is two edges from the initial mark.')
add(387,'All-node tree distance sums',['trees','rerooting'],'Read n then n-1 undirected tree edges. Print, in node order, the sum of distances from each node to every other node.',['1 <= n <= 1,000; vertices are zero-based','The complete input is at most 12,000 characters.'],['Root once to compute subtree sizes.','Find the root distance sum.','Reroot across an edge by moving one subtree.'],'O(n) time and O(n) space',"""def solve():
 n=int(input());g=[[]for _ in range(n)]
 for _ in range(n-1):a,b=map(int,input().split());g[a].append(b);g[b].append(a)
 p=[-1]*n;order=[0]
 for v in order:
  for w in g[v]:
   if w!=p[v]:p[w]=v;order.append(w)
 sz=[1]*n
 for v in order[:0:-1]:sz[p[v]]+=sz[v]
 ans=[0]*n
 dep=[0]*n
 for v in order:
  for w in g[v]:
   if p[w]==v:dep[w]=dep[v]+1
 ans[0]=sum(dep)
 for v in order[1:]:ans[v]=ans[p[v]]+n-2*sz[v]
 print(*ans)""",[("3\n0 1\n1 2\n","3 2 3"),("1\n","0"),("4\n0 1\n0 2\n0 3\n","3 5 5 5"),("4\n0 1\n1 2\n2 3\n","6 4 4 6"),("2\n0 1\n","1 1"),("5\n0 1\n0 2\n2 3\n2 4\n","6 9 5 8 8")],'The middle node has total distance two.')
add(388,'Unrooted tree isomorphism decision',['trees','tree-isomorphism'],'Read n, then n-1 edges of the first tree and n-1 edges of the second tree. Print YES if they are isomorphic as unrooted trees, otherwise NO.',['1 <= n <= 5,000; vertices are zero-based'],['Tree centers are one vertex or one edge.','Root at every center candidate.','Compare sorted child encodings.'],'O(n log n) time and O(n) space',"""def solve():
 sys.setrecursionlimit(30000);n=int(input())
 def read():
  g=[[]for _ in range(n)]
  for _ in range(n-1):a,b=map(int,input().split());g[a].append(b);g[b].append(a)
  return g
 a=read();b=read()
 def code(g):
  deg=list(map(len,g));q=[i for i in range(n)if deg[i]<=1];left=n
  while left>2:
   nq=[];left-=len(q)
   for v in q:
    for w in g[v]:deg[w]-=1
    for w in g[v]:
     if deg[w]==1:nq.append(w)
   q=nq
  def f(v,p):return '('+''.join(sorted(f(w,v)for w in g[v]if w!=p))+')'
  return min(f(c,-1)for c in q)
 print('YES' if code(a)==code(b) else 'NO')""",[("3\n0 1\n1 2\n0 2\n2 1\n","YES"),("4\n0 1\n1 2\n2 3\n0 1\n0 2\n0 3\n","NO"),("1\n","YES"),("4\n0 1\n0 2\n0 3\n1 0\n1 2\n1 3\n","YES"),("5\n0 1\n1 2\n2 3\n3 4\n0 1\n0 2\n0 3\n0 4\n","NO"),("2\n0 1\n0 1\n","YES")],'Both input paths have the same unrooted shape.')
PYTHON_CURATED_384_388=ITEMS
