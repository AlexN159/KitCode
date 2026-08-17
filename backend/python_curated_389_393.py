"""Final audited Hard non-OOP curriculum tranche 389--393."""
from __future__ import annotations
STARTER="import sys\n\ndef solve() -> None:\n    pass\n\nif __name__ == '__main__':\n    solve()\n";ITEMS=[]
def add(n,t,top,d,c,h,x,b,cs,w):
 r=[{'input':i,'expected_output':o}for i,o in cs];ITEMS.append({'id':f'python-curated-{n:03d}','language':'python','title':t,'difficulty':'Hard','topics':top,'practice_frequency':'Common','description':d,'constraints':c,'hints':h,'expected_complexity':x,'starter_code':STARTER,'solution':'import sys\n'+b+"\n\nif __name__ == '__main__':\n    solve()\n",'examples':[{'input':r[0]['input'],'output':r[0]['expected_output'],'explanation':w}],'public_tests':r[:2],'hidden_tests':r[2:]})
add(389,'Convex polygon point classification',['geometry','binary-search'],'Read n CCW strictly convex polygon vertices, then q points. Print INSIDE, BOUNDARY, or OUTSIDE per point.',['3 <= n <= 300; 1 <= q <= 300','Coordinates are signed 32-bit integers; the complete input is at most 12,000 characters.'],['Use vertex zero as a fan apex.','Reject points outside the first and last fan rays.','Binary-search the containing fan triangle.'],'O((n+q log n)) time and O(n) space',"""def solve():
 n=int(input());p=[tuple(map(int,input().split()))for _ in range(n)];q=int(input())
 def cr(a,b,c):return(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 for _ in range(q):
  x=tuple(map(int,input().split()));a=cr(p[0],p[1],x);b=cr(p[0],p[-1],x)
  if a<0 or b>0:print('OUTSIDE');continue
  if a==0 or b==0:
   u=p[1] if a==0 else p[-1];print('BOUNDARY' if min(p[0][0],u[0])<=x[0]<=max(p[0][0],u[0]) and min(p[0][1],u[1])<=x[1]<=max(p[0][1],u[1]) else 'OUTSIDE');continue
  l=1;r=n-1
  while r-l>1:
   m=(l+r)//2
   if cr(p[0],p[m],x)>=0:l=m
   else:r=m
  z=cr(p[l],p[(l+1)%n],x)
  print('INSIDE' if z>0 else 'BOUNDARY' if z==0 else 'OUTSIDE')""",[("4\n0 0\n2 0\n2 2\n0 2\n3\n1 1\n2 1\n3 1\n","INSIDE\nBOUNDARY\nOUTSIDE"),("3\n0 0\n4 0\n0 4\n2\n0 0\n2 2\n","BOUNDARY\nBOUNDARY"),("3\n0 0\n3 0\n0 3\n1\n1 1\n","INSIDE"),("4\n0 0\n3 0\n3 3\n0 3\n1\n0 2\n","BOUNDARY"),("4\n0 0\n2 0\n2 2\n0 2\n1\n-1 0\n","OUTSIDE"),("3\n0 0\n2 0\n0 2\n1\n3 0\n","OUTSIDE")],'The center lies strictly inside the square.')
add(390,'Quadratic farthest-pair squared distance',['geometry','brute-force'],'Read n distinct integer points and print the largest squared Euclidean distance over every unordered pair.',['2 <= n <= 2000; coordinates are signed 32-bit integers'],['Try every pair whose first index is smaller than its second.','Use (x1-x2)^2 + (y1-y2)^2.','Squared distances avoid floating-point arithmetic.'],'O(n^2) time and O(1) auxiliary space',"""def solve():
 n=int(input());a=[tuple(map(int,input().split()))for _ in range(n)];print(max((x-u)**2+(y-v)**2 for i,(x,y)in enumerate(a)for u,v in a[i+1:]))""",[("2\n0 0\n3 4\n","25"),("3\n0 0\n1 0\n0 1\n","2"),("3\n0 0\n2 0\n1 1\n","4"),("2\n-1 -1\n1 1\n","8"),("4\n0 0\n0 3\n4 0\n4 3\n","25"),("3\n0 0\n5 0\n2 1\n","25")],'The only pair is five units apart.')
add(391,'Dynamic bipartiteness by rebuilding',['graphs','breadth-first-search'],'Read n q then ADD u v, REMOVE u v, ASK. Valid removals match an active edge; ASK prints YES if the current graph is bipartite.',['1 <= n,q <= 2000; vertices are zero-based','At most 500 ASK commands.'],['Keep the currently active undirected edges.','On ASK, two-colour every connected component.','A same-colour edge proves an odd cycle.'],'O(q(n+q)) time and O(n+q) space',"""def solve():
 from collections import deque
 n,q=map(int,input().split());e=set()
 for _ in range(q):
  z=input().split()
  if z[0]!='ASK':
   a,b=sorted(map(int,z[1:]));e.remove((a,b)) if z[0]=='REMOVE' else e.add((a,b))
  else:
   g=[[]for _ in range(n)]
   for a,b in e:g[a].append(b);g[b].append(a)
   c=[-1]*n;ok=1
   for s in range(n):
    if c[s]>=0:continue
    c[s]=0;d=deque([s])
    while d:
     v=d.popleft()
     for w in g[v]:
      if c[w]<0:c[w]=c[v]^1;d.append(w)
      elif c[w]==c[v]:ok=0
   print('YES' if ok else 'NO')""",[("3 4\nADD 0 1\nADD 1 2\nASK\nADD 2 0\n","YES"),("3 4\nADD 0 1\nADD 1 2\nADD 2 0\nASK\n","NO"),("2 2\nASK\nADD 0 1\n","YES"),("3 5\nADD 0 1\nADD 1 2\nADD 2 0\nREMOVE 2 0\nASK\n","YES"),("1 2\nADD 0 0\nASK\n","NO"),("4 3\nADD 0 1\nADD 2 3\nASK\n","YES")],'A path has no odd cycle.')
add(392,'Lexicographic binary De Bruijn cycle',['graphs','combinatorics'],'Read k and print the lexicographically smallest length 2^k binary De Bruijn cycle, represented by the cycle starting with k zeroes.',['1 <= k <= 14, keeping the cycle within the local output limit'],['Vertices are binary strings of length k-1.','Use an iterative deterministic Euler tour.','Append an edge bit on backtracking.'],'O(2^k) time and space',"""def solve():
 k=int(input());vertices=1<<(k-1);next_bit=[0]*vertices;stack=[(0,-1)];out=[];mask=vertices-1
 while stack:
  vertex,bit=stack[-1]
  if next_bit[vertex]<2:
   bit=next_bit[vertex];next_bit[vertex]+=1;stack.append((((vertex<<1)|bit)&mask,bit))
  else:
   _,bit=stack.pop()
   if bit>=0:out.append(str(bit))
 s=''.join(reversed(out));d=s+s;i=d.find('0'*k);print(d[i:i+len(s)])""",[("2\n","0011"),("3\n","00010111"),("1\n","01"),("4\n","0000100110101111"),("2\n","0011"),("1\n","01")],'Every binary length-two word appears once cyclically.')
add(393,'Prime-field Lagrange evaluation',['number-theory','polynomials'],'Read prime p, n, n distinct xi yi pairs, then x. Print the value at x of the unique degree<n polynomial modulo p.',['2 <= p <= 1000000007 is prime; 1 <= n <= 2000','All xi are distinct modulo p and every input value is in [0,p).'],['Build each Lagrange numerator at the query point.','Multiply its denominator differences.','Use Fermat inversion modulo p.'],'O(n^2 + n log p) time and O(1) auxiliary space',"""def solve():
 p=int(input());n=int(input());a=[tuple(map(int,input().split()))for _ in range(n)];x=int(input());ans=0
 for i,(u,y) in enumerate(a):
  num=den=1
  for j,(v,_) in enumerate(a):
   if i!=j:num=num*(x-v)%p;den=den*(u-v)%p
  ans=(ans+y*num*pow(den,p-2,p))%p
 print(ans)""",[("17\n2\n0 1\n1 3\n2\n","5"),("7\n3\n0 0\n1 1\n2 4\n3\n","2"),("5\n1\n3 4\n0\n","4"),("11\n2\n2 5\n4 9\n3\n","7"),("13\n3\n0 1\n1 2\n2 5\n3\n","10"),("3\n2\n0 2\n1 0\n2\n","1")],'The line through one and three evaluates to five at two.')
PYTHON_CURATED_389_393=ITEMS
