"""Audited Hard graph-algorithm Python curriculum tranche 354--358."""
from __future__ import annotations

STARTER="import sys\n\ndef solve() -> None:\n    pass\n\nif __name__ == '__main__':\n    solve()\n"; ITEMS=[]
def add(n,t,d,top,desc,con,hints,cx,body,cases,why):
 r=[{"input":x,"expected_output":y} for x,y in cases]; ITEMS.append({"id":f"python-curated-{n:03d}","language":"python","title":t,"difficulty":d,"topics":top,"practice_frequency":"Common","description":desc,"constraints":con,"hints":hints,"expected_complexity":cx,"starter_code":STARTER,"solution":"import sys\n"+body+"\n\nif __name__ == '__main__':\n    solve()\n","examples":[{"input":r[0]["input"],"output":r[0]["expected_output"],"explanation":why}],"public_tests":r[:2],"hidden_tests":r[2:]})

add(354,"Exact-demand minimum-cost flow","Hard",["graphs","min-cost-flow"],"Read n m s t f, then m directed edges u v capacity cost. Send exactly f units from s to t at minimum cost and print that cost, or -1 if the network cannot carry f units.",["2 <= n <= 100 and 0 <= m <= 1,000; vertices are 0 through n-1","0 <= f <= 10,000; capacities are 0 through 10,000 and costs are 0 through 1,000,000","s and t are distinct; parallel directed edges are allowed"],["Keep a reverse residual edge for every edge.","Find a cheapest residual s-to-t path each round.","Augment as much as that path permits."],"O(f E V) time with unit augmentations in the worst case and O(V + E) auxiliary space",'''def solve():
 from collections import deque
 n,m,s,t,need=map(int,input().split());g=[[]for _ in range(n)]
 def add(a,b,c,w):
  g[a].append([b,c,w,len(g[b])]);g[b].append([a,0,-w,len(g[a])-1])
 for _ in range(m):add(*map(int,input().split()))
 sent=cost=0
 while sent<need:
  d=[10**30]*n;p=[None]*n;d[s]=0;q=deque([s]);inside=[0]*n;inside[s]=1
  while q:
   v=q.popleft();inside[v]=0
   for i,(u,c,w,_) in enumerate(g[v]):
    if c and d[u]>d[v]+w:
     d[u]=d[v]+w;p[u]=(v,i)
     if not inside[u]:q.append(u);inside[u]=1
  if p[t] is None:print(-1);return
  z=need-sent;v=t
  while v!=s:
   u,i=p[v];z=min(z,g[u][i][1]);v=u
  v=t
  while v!=s:
   u,i=p[v];e=g[u][i];e[1]-=z;g[v][e[3]][1]+=z;v=u
  sent+=z;cost+=z*d[t]
 print(cost)''',[("4 5 0 3 3\n0 1 2 1\n0 2 2 5\n1 2 1 1\n1 3 2 3\n2 3 2 1\n","13"),("2 1 0 1 4\n0 1 3 7\n","-1"),("3 3 0 2 0\n0 1 5 9\n1 2 5 9\n0 2 1 1\n","0"),("3 3 0 2 2\n0 1 2 2\n1 2 2 3\n0 2 1 10\n","10"),("3 3 0 2 3\n0 1 1 1\n0 1 2 4\n1 2 3 2\n","15"),("4 2 0 3 1\n0 1 2 1\n2 3 2 1\n","-1")],"The cheapest three units use all available low-cost routes.")
add(355,"Lexicographically smallest Two-SAT assignment","Hard",["graphs","two-sat"],"Read n m then m clauses a b, where each signed literal is in [-n,-1] or [1,n]. Print the lexicographically smallest n-bit satisfying assignment for x1 through xn, comparing x1 first, or IMPOSSIBLE.",["1 <= n <= 250 and 0 <= m <= 1,500","A positive literal i means xi; a negative literal -i means not xi","Bit 0 is smaller than bit 1, so greedily attempt to fix each next variable false"],["A clause a OR b creates implications not-a to b and not-b to a.","An assumption xi = value is a unit clause and therefore one more implication.","For each variable, keep zero exactly when the accumulated formula remains satisfiable."],"O(n(n + m)) time and O(n + m) auxiliary space",'''def solve():
 n,m=map(int,input().split());N=2*n;base=[]
 def node(x):return 2*(abs(x)-1)+(x<0)
 for _ in range(m):
  a,b=map(int,input().split());x=node(a);y=node(b);base.extend(((x^1,y),(y^1,x)))
 def possible(forced):
  g=[[]for _ in range(N)];rg=[[]for _ in range(N)]
  for a,b in base:
   g[a].append(b);rg[b].append(a)
  for literal in forced:
   x=node(literal);g[x^1].append(x);rg[x].append(x^1)
  seen=[0]*N;order=[]
  for start in range(N):
   if seen[start]:continue
   seen[start]=1;stack=[(start,0)]
   while stack:
    v,i=stack[-1]
    if i<len(g[v]):
     w=g[v][i];stack[-1]=(v,i+1)
     if not seen[w]:seen[w]=1;stack.append((w,0))
    else:order.append(v);stack.pop()
  comp=[-1]*N;label=0
  for start in reversed(order):
   if comp[start]>=0:continue
   comp[start]=label;stack=[start]
   while stack:
    v=stack.pop()
    for w in rg[v]:
     if comp[w]<0:comp[w]=label;stack.append(w)
   label+=1
  return all(comp[2*i]!=comp[2*i+1] for i in range(n))
 if not possible([]):print('IMPOSSIBLE');return
 fixed=[];answer=[]
 for variable in range(1,n+1):
  if possible(fixed+[-variable]):fixed.append(-variable);answer.append(0)
  else:fixed.append(variable);answer.append(1)
 print(*answer)''',[("2 2\n1 2\n-1 2\n","0 1"),("1 2\n1 1\n-1 -1\n","IMPOSSIBLE"),("3 0\n","0 0 0"),("2 2\n-1 -2\n1 -2\n","0 0"),("3 3\n1 2\n-1 3\n-2 -3\n","0 1 0"),("1 1\n-1 -1\n","0")],"The assignment 0 1 is the first satisfying two-bit string in lexicographic order.")
add(356,"One discounted-edge shortest path","Hard",["graphs","shortest-path"],"Read n m then m directed weighted edges u v w (vertices are 1 through n). Travel from 1 to n while applying floor(w/2) to exactly one used edge; print the minimum total cost, or -1 if n is unreachable.",["2 <= n <= 200,000 and 0 <= m <= 200,000","1 <= w <= 1,000,000,000; parallel directed edges are allowed","The route may revisit vertices, but all weights are positive"],["Run Dijkstra forward from vertex one.","Run it backward from vertex n.","Try every edge as the discounted edge."],"O((n + m) log n) time and O(n + m) auxiliary space",'''def solve():
 import heapq
 n,m=map(int,input().split());g=[[]for _ in range(n)];rg=[[]for _ in range(n)];edges=[]
 for _ in range(m):
  a,b,w=map(int,input().split());a-=1;b-=1;g[a].append((b,w));rg[b].append((a,w));edges.append((a,b,w))
 def dij(graph,start):
  d=[10**30]*n;d[start]=0;q=[(0,start)]
  while q:
   x,v=heapq.heappop(q)
   if x!=d[v]:continue
   for u,w in graph[v]:
    if x+w<d[u]:d[u]=x+w;heapq.heappush(q,(d[u],u))
  return d
 a=dij(g,0);b=dij(rg,n-1);ans=min((a[u]+w//2+b[v] for u,v,w in edges if a[u]<10**30 and b[v]<10**30),default=10**30)
 print(ans if ans<10**30 else -1)''',[("3 3\n1 2 5\n2 3 5\n1 3 20\n","7"),("3 1\n1 2 4\n","-1"),("2 1\n1 2 9\n","4"),("4 5\n1 2 8\n2 4 8\n1 3 3\n3 4 20\n2 3 1\n","12"),("3 3\n1 2 1\n2 3 1\n1 3 3\n","1"),("4 4\n1 2 100\n2 4 1\n1 3 2\n3 4 100\n","51")],"Discounting either edge on 1-2-3 gives 7.")
add(357,"First k shortest walk costs","Hard",["graphs","k-shortest-paths"],"Read n m k then m directed positive-weight edges u v w (vertices are 1 through n). Print the costs of the first k shortest walks from 1 to n in nondecreasing order.",["2 <= n <= 200,000, 0 <= m <= 200,000, and 1 <= k <= 10","1 <= w <= 1,000,000,000; walks may repeat vertices and edges","The input guarantees at least k walks from 1 to n"],["A vertex can be removed from the heap more than once.","The kth removal of a vertex cannot improve future answers.","Record removals of n, including duplicates."],"O(k m log(k n)) time and O(k n + m) auxiliary space",'''def solve():
 import heapq
 n,m,k=map(int,input().split());g=[[]for _ in range(n)]
 for _ in range(m):
  a,b,w=map(int,input().split());g[a-1].append((b-1,w))
 used=[0]*n;q=[(0,0)];out=[]
 while q and len(out)<k:
  d,v=heapq.heappop(q)
  if used[v]>=k:continue
  used[v]+=1
  if v==n-1:out.append(d)
  for u,w in g[v]:
   if used[u]<k:heapq.heappush(q,(d+w,u))
 print(*out)''',[("4 5 3\n1 2 1\n2 4 1\n1 3 2\n3 4 1\n2 2 1\n","2 3 3"),("2 2 4\n1 2 5\n2 2 1\n","5 6 7 8"),("3 4 3\n1 2 1\n2 3 1\n3 3 1\n1 3 5\n","2 3 4"),("3 4 5\n1 2 1\n2 2 2\n2 3 1\n1 3 10\n","2 4 6 8 10"),("2 1 1\n1 2 7\n","7"),("4 5 3\n1 2 1\n2 4 4\n1 3 2\n3 4 2\n2 3 1\n","4 4 5")],"The cycle at vertex two produces the third walk of cost three.")
add(358,"Rooted directed minimum arborescence","Hard",["graphs","arborescence"],"Read n m r, then m directed weighted edges u v w. Print the minimum cost of a directed arborescence rooted at r that reaches every vertex, or -1 if none exists.",["2 <= n <= 200 and 0 <= m <= 3,000; vertices are 0 through n-1","0 <= r < n; edge costs are signed 32-bit integers and parallel edges are allowed","An arborescence has one incoming edge for every non-root vertex and a directed root-to-vertex path"],["Choose each vertex's cheapest incoming edge.","A chosen directed cycle must be contracted.","Subtract selected incoming costs when rebuilding edges."],"O(V E) time and O(V + E) auxiliary space",'''def solve():
 n,m,r=map(int,input().split());edges=[tuple(map(int,input().split()))for _ in range(m)];ans=0
 while 1:
  inf=10**30;inc=[inf]*n;pre=[-1]*n
  for u,v,w in edges:
   if u!=v and w<inc[v]:inc[v]=w;pre[v]=u
  inc[r]=0
  if any(x==inf for x in inc):print(-1);return
  ans+=sum(inc);group=[-1]*n;seen=[-1]*n;count=0
  for i in range(n):
   v=i
   while seen[v]!=i and group[v]<0 and v!=r:seen[v]=i;v=pre[v]
   if v!=r and group[v]<0:
    group[v]=count;u=pre[v]
    while u!=v:group[u]=count;u=pre[u]
    count+=1
  if count==0:print(ans);return
  for i in range(n):
   if group[i]<0:group[i]=count;count+=1
  edges=[(group[u],group[v],w-inc[v]) for u,v,w in edges];r=group[r];n=count''',[("3 4 0\n0 1 5\n0 2 4\n1 2 1\n2 1 1\n","5"),("3 1 0\n0 1 2\n","-1"),("2 2 0\n0 1 -5\n1 0 9\n","-5"),("4 5 0\n0 1 10\n0 2 10\n1 2 1\n2 1 1\n2 3 2\n","13"),("3 4 1\n1 0 3\n1 2 4\n0 2 1\n2 0 1\n","4"),("2 0 0\n","-1")],"The cheapest incoming cycle is entered from the root once.")
PYTHON_CURATED_354_358=ITEMS
