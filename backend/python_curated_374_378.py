"""Audited Hard dynamic-programming Python curriculum tranche 374--378."""
from __future__ import annotations

STARTER="import sys\n\ndef solve() -> None:\n    pass\n\nif __name__ == '__main__':\n    solve()\n"; ITEMS=[]
def add(n,t,top,desc,con,hints,cx,body,cases,why):
 r=[{"input":x,"expected_output":y} for x,y in cases]; ITEMS.append({"id":f"python-curated-{n:03d}","language":"python","title":t,"difficulty":"Hard","topics":top,"practice_frequency":"Common","description":desc,"constraints":con,"hints":hints,"expected_complexity":cx,"starter_code":STARTER,"solution":"import sys\n"+body+"\n\nif __name__ == '__main__':\n    solve()\n","examples":[{"input":r[0]["input"],"output":r[0]["expected_output"],"explanation":why}],"public_tests":r[:2],"hidden_tests":r[2:]})

add(374,"SOS-DP submask frequency queries",["dynamic-programming","sum-over-subsets"],"Read b n q, then n masks and q query masks. For each query mask x, print how many listed masks are submasks of x; duplicate listed masks count separately.",["1 <= b <= 17; every mask is in [0, 2^b)","0 <= n,q <= 1,000","The n masks occupy one line when n is positive; each query occupies one line; the complete input is at most 12,000 characters"],["Start with the exact frequency of every mask.","For each bit, add the count without that bit into masks with it.","The completed table at x counts all submasks of x."],"O(b 2^b + n + q) time and O(2^b) auxiliary space",'''def solve():
 b,n,q=map(int,input().split());size=1<<b;f=[0]*size
 if n:
  for x in map(int,input().split()):f[x]+=1
 for bit in range(b):
  step=1<<bit
  for mask in range(size):
   if mask&step:f[mask]+=f[mask^step]
 for _ in range(q):print(f[int(input())])''',[("3 4 3\n0 1 3 7\n3\n4\n7\n","3\n1\n4"),("2 3 2\n1 1 2\n1\n3\n","2\n3"),("1 0 2\n0\n1\n","0\n0"),("3 3 2\n2 4 6\n6\n7\n","3\n3"),("2 1 1\n0\n0\n","1"),("4 4 2\n3 5 9 15\n7\n8\n","2\n0")],"Masks zero, one, and three are all submasks of three.")
add(375,"Small-terminal Steiner tree cost",["dynamic-programming","steiner-tree"],"Read n m t, a line of t distinct terminals, then m weighted undirected edges. Print the minimum cost of a connected subgraph containing every terminal, or -1 if impossible.",["2 <= n <= 100, 2 <= t <= 8, and 0 <= m <= 1,000","Vertices are 0 through n-1; terminals are distinct valid vertices","Edge weights are integers from 0 through 1,000,000; parallel edges are allowed"],["Use one DP mask per subset of terminals.","At a vertex, combine two proper terminal subsets.","Run multi-source Dijkstra after each mask merge."],"O(3^t n + 2^t m log n) time and O(2^t n + m) auxiliary space",'''def solve():
 import heapq
 n,m,t=map(int,input().split());term=list(map(int,input().split()));g=[[]for _ in range(n)]
 for _ in range(m):
  a,b,w=map(int,input().split());g[a].append((b,w));g[b].append((a,w))
 inf=10**30;dp=[[inf]*n for _ in range(1<<t)]
 for i,v in enumerate(term):dp[1<<i][v]=0
 for mask in range(1,1<<t):
  sub=(mask-1)&mask
  while sub:
   other=mask^sub
   if sub<other:
    for v in range(n):dp[mask][v]=min(dp[mask][v],dp[sub][v]+dp[other][v])
   sub=(sub-1)&mask
  q=[(d,v) for v,d in enumerate(dp[mask]) if d<inf];heapq.heapify(q)
  while q:
   d,v=heapq.heappop(q)
   if d!=dp[mask][v]:continue
   for u,w in g[v]:
    if d+w<dp[mask][u]:dp[mask][u]=d+w;heapq.heappush(q,(d+w,u))
 ans=min(dp[-1]);print(ans if ans<inf else -1)''',[("3 3 2\n0 2\n0 1 1\n1 2 2\n0 2 10\n","3"),("4 4 3\n0 2 3\n0 1 1\n1 2 1\n2 3 1\n0 3 10\n","3"),("4 1 2\n0 3\n0 1 2\n","-1"),("5 5 3\n0 2 4\n0 1 2\n1 2 2\n2 3 2\n3 4 2\n0 4 20\n","8"),("3 3 2\n0 2\n0 1 0\n1 2 0\n0 2 5\n","0"),("4 4 2\n1 3\n0 1 4\n1 2 1\n2 3 1\n0 3 9\n","2")],"The path 0-1-2 connects the two terminals for cost three.")
add(376,"Blocked-board domino tiling count",["dynamic-programming","profile-dp"],"Read n m then n rows of . and #. Count tilings of all unblocked cells by 1-by-2 dominoes and print the result modulo 1000000007.",["1 <= n <= 200 and 1 <= m <= 10","Each row has exactly m characters; # is blocked and . is unblocked","Dominoes cover two orthogonally adjacent unblocked cells"],["A state records vertical dominoes arriving from the previous row.","For an empty cell, either place a horizontal domino or start a vertical one.","Blocked cells cannot have an incoming vertical domino."],"O(n m 2^m) time and O(2^m) auxiliary space",'''def solve():
 mod=1000000007;n,m=map(int,input().split());rows=[input().strip() for _ in range(n)];dp={0:1}
 for row in rows:
  block=sum((c=='#')<<i for i,c in enumerate(row));nd={}
  for incoming,ways in dp.items():
   if incoming&block:continue
   used=incoming|block
   def fill(pos,out):
    nonlocal used
    while pos<m and used>>pos&1:pos+=1
    if pos==m:nd[out]=(nd.get(out,0)+ways)%mod;return
    if pos+1<m and not(used>>(pos+1)&1):
     old=used;used|=(1<<pos)|(1<<(pos+1));fill(pos+1,out);used=old
    old=used;used|=1<<pos;fill(pos+1,out|(1<<pos));used=old
   fill(0,0)
  dp=nd
 print(dp.get(0,0))''',[("2 2\n..\n..\n","2"),("1 3\n...\n","0"),("2 3\n...\n...\n","3"),("2 2\n.#\n..\n","0"),("2 2\n##\n##\n","1"),("1 2\n##\n","1")],"A clear two-by-two board has two domino tilings.")
add(377,"Hungarian minimum square assignment",["optimization","hungarian-algorithm"],"Read n then an n by n integer cost matrix. Assign every row to a different column and print the minimum total cost.",["1 <= n <= 30","Every cost is a signed 32-bit integer","Rows and columns are both numbered only by their input order; the complete input is at most 12,000 characters"],["Maintain row and column potentials.","Grow one augmenting path for each new row.","Update the minimum slack values while searching for that path."],"O(n^3) time and O(n) auxiliary space",'''def solve():
 n=int(input());a=[list(map(int,input().split()))for _ in range(n)];u=[0]*(n+1);v=[0]*(n+1);p=[0]*(n+1);way=[0]*(n+1)
 for i in range(1,n+1):
  p[0]=i;j0=0;mn=[10**30]*(n+1);used=[0]*(n+1)
  while 1:
   used[j0]=1;i0=p[j0];delta=10**30;j1=0
   for j in range(1,n+1):
    if not used[j]:
     cur=a[i0-1][j-1]-u[i0]-v[j]
     if cur<mn[j]:mn[j]=cur;way[j]=j0
     if mn[j]<delta:delta=mn[j];j1=j
   for j in range(n+1):
    if used[j]:u[p[j]]+=delta;v[j]-=delta
    else:mn[j]-=delta
   j0=j1
   if not p[j0]:break
  while 1:
   j1=way[j0];p[j0]=p[j1];j0=j1
   if not j0:break
 print(-v[0])''',[("2\n1 2\n2 1\n","2"),("3\n4 1 3\n2 0 5\n3 2 2\n","5"),("1\n-7\n","-7"),("3\n0 10 10\n10 0 10\n10 10 0\n","0"),("2\n-1 5\n2 -3\n","-4"),("3\n1 100 100\n100 1 100\n100 100 1\n","3")],"Assigning the diagonal pairs costs two.")
add(378,"Monge-optimized squared-sum partition",["dynamic-programming","divide-and-conquer-optimization"],"Read n k then n nonnegative integers. Partition the array into exactly k nonempty contiguous groups, minimizing the sum of squared group sums; print that minimum.",["1 <= k <= 60 and k <= n <= 500","Each array value is an integer from 0 through 1,000,000","The values are nonnegative, which gives the squared-prefix-sum cost the required monotone optima"],["Precompute prefix sums for O(1) group costs.","Let dp[g][i] end the gth group at i.","Compute one DP layer with divide-and-conquer over its optimal split range."],"O(k n log n) time and O(n) auxiliary space",'''def solve():
 n,k=map(int,input().split());a=list(map(int,input().split()));pre=[0]
 for x in a:pre.append(pre[-1]+x)
 inf=10**40;old=[inf]*(n+1);old[0]=0
 for groups in range(1,k+1):
  cur=[inf]*(n+1)
  def go(left,right,lo,hi):
   if left>right:return
   mid=(left+right)//2;best=inf;at=lo
   for j in range(lo,min(hi,mid-1)+1):
    value=old[j]+(pre[mid]-pre[j])**2
    if value<best:best=value;at=j
   cur[mid]=best;go(left,mid-1,lo,at);go(mid+1,right,at,hi)
  go(groups,n,groups-1,n-1);old=cur
 print(old[n])''',[("3 2\n1 2 3\n","18"),("4 2\n1 1 1 1\n","8"),("3 3\n2 0 3\n","13"),("1 1\n5\n","25"),("4 3\n1 2 3 4\n","34"),("4 2\n1 0 1 0\n","2")],"Splitting after the first two values gives group sums three and three.")
PYTHON_CURATED_374_378=ITEMS
