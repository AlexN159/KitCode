"""Data-only advanced curated Python exercises 161--180."""
from __future__ import annotations

STARTER = "import sys\n\ndef solve() -> None:\n    pass\n\nif __name__ == '__main__':\n    solve()\n"
ITEMS = []

def add(num, title, difficulty, topics, description, constraints, hints, complexity, body, cases, explanation):
    records = [{"input": source, "expected_output": result} for source, result in cases]
    ITEMS.append({"id": f"python-curated-{num:03d}", "language": "python", "title": title,
        "difficulty": difficulty, "topics": topics, "interview_frequency": "Common",
        "description": description, "constraints": constraints, "hints": hints,
        "expected_complexity": complexity, "starter_code": STARTER,
        "solution": "import sys\n" + body.strip() + "\n\nif __name__ == '__main__':\n    solve()\n",
        "examples": [{"input": records[0]["input"], "output": records[0]["expected_output"], "explanation": explanation}],
        "public_tests": records[:2], "hidden_tests": records[2:]})

add(161, "KMP overlapping occurrence count", "Medium", ["strings", "pattern-matching"],
"Read text then pattern. Print the number of starting positions where pattern occurs in text, including overlaps. An empty pattern occurs at every boundary of text.",
["0 <= text length, pattern length <= 200,000", "Both lines use printable ASCII characters."],
["Build a prefix-failure array for the pattern.", "On a mismatch, reuse the longest proper border.", "After a match, fall back so an overlap can start."], "O(text length + pattern length) time, O(pattern length) auxiliary space",
"""def solve():
    text=input().rstrip('\\n'); pat=input().rstrip('\\n')
    if not pat: print(len(text)+1); return
    pi=[0]*len(pat); j=0
    for i in range(1,len(pat)):
        while j and pat[i]!=pat[j]: j=pi[j-1]
        if pat[i]==pat[j]: j+=1
        pi[i]=j
    ans=j=0
    for ch in text:
        while j and ch!=pat[j]: j=pi[j-1]
        if ch==pat[j]: j+=1
        if j==len(pat): ans+=1; j=pi[j-1]
    print(ans)""",
[("ababa\naba\n","2"),("aaaaa\naa\n","4"),("abc\nd\n","0"),("\n\n","1"),("abc\n\n","4"),("abcabcabc\nabc\n","3")], "aba begins at positions 0 and 2.")

add(162, "Z-array prefix match lengths", "Medium", ["strings", "pattern-matching"],
"Read one string s. Print z[0] through z[n-1], where z[0] is n and z[i] is the longest prefix of s matching s starting at i. For an empty string print a blank line.",
["0 <= length <= 8,000", "s uses printable ASCII characters; the bound keeps vector output below the local runner limit."],
["Maintain a matching interval [left, right].", "Reuse z values while i is inside that interval.", "Extend only beyond the interval's current right edge."], "O(n) time, O(n) auxiliary space",
"""def solve():
    s=input().rstrip('\\n'); n=len(s)
    if not n: print(); return
    z=[0]*n; z[0]=n; l=r=0
    for i in range(1,n):
        if i<=r: z[i]=min(r-i+1,z[i-l])
        while i+z[i]<n and s[z[i]]==s[i+z[i]]: z[i]+=1
        if i+z[i]-1>r: l,r=i,i+z[i]-1
    print(*z)""",
[("aabcaabxaaaz\n","12 1 0 0 3 1 0 0 2 2 1 0"),("aaaaa\n","5 4 3 2 1"),("a\n","1"),("\n",""),("ababa\n","5 0 3 0 1"),("abcab\n","5 0 0 2 0")], "At position 4, aab matches the prefix for length 3.")

add(163, "Bellman-Ford reachable negative cycle", "Hard", ["graphs", "shortest-path"],
"Line 1 is v e s; the next e lines are directed u v w edges. If a negative cycle is reachable from s, print NEGATIVE CYCLE. Otherwise print distances from s to vertices 0 through v-1, with -1 for unreachable vertices.",
["1 <= v <= 2,000 and 0 <= e <= 10,000", "Vertices are 0 through v-1 and weights are signed 32-bit integers."],
["Relax every edge up to v-1 times.", "Unreachable vertices must not relax outgoing edges.", "A further reachable improvement proves the cycle."], "O(v * e) time, O(v) auxiliary space",
"""def solve():
    v,e,s=map(int,input().split()); edges=[tuple(map(int,input().split())) for _ in range(e)]; inf=10**30; d=[inf]*v; d[s]=0
    for _ in range(v-1):
        changed=False
        for a,b,w in edges:
            if d[a]<inf and d[a]+w<d[b]: d[b]=d[a]+w; changed=True
        if not changed: break
    for a,b,w in edges:
        if d[a]<inf and d[a]+w<d[b]: print('NEGATIVE CYCLE'); return
    print(*[x if x<inf else -1 for x in d])""",
[("4 5 0\n0 1 4\n0 2 5\n1 2 -2\n2 3 3\n1 3 10\n","0 4 2 5"),("3 3 0\n0 1 1\n1 2 -3\n2 1 1\n","NEGATIVE CYCLE"),("3 1 0\n1 2 -5\n","0 -1 -1"),("1 0 0\n","0"),("4 4 0\n0 1 2\n1 2 2\n2 3 2\n3 1 -5\n","NEGATIVE CYCLE"),("4 4 2\n2 1 3\n1 0 -1\n2 3 10\n0 3 2\n","2 3 0 4")], "The route through vertex 1 improves the path to vertex 2.")

add(164, "All-pairs shortest-path queries", "Hard", ["graphs", "dynamic-programming"],
"Line 1 is v e q; next e lines are directed u v w edges with no negative cycles; next q lines are a b queries. Print shortest distance for each query, or -1 if b is unreachable from a.",
["1 <= v <= 180, 0 <= e <= 10,000, and 1 <= q <= 4,500", "Vertices are 0 through v-1; weights fit signed 32-bit integers, and q is output-capped."],
["Initialize diagonal distances to zero.", "Each intermediate vertex may improve every ordered pair.", "Keep unreachable values separate from real distances."], "O(v^3 + q) time, O(v^2 + q) space including buffered output",
"""def solve():
    v,e,q=map(int,input().split()); inf=10**30; d=[[inf]*v for _ in range(v)]
    for i in range(v): d[i][i]=0
    for _ in range(e):
        a,b,w=map(int,input().split()); d[a][b]=min(d[a][b],w)
    for k in range(v):
        for i in range(v):
            if d[i][k]<inf:
                for j in range(v):
                    if d[k][j]<inf and d[i][k]+d[k][j]<d[i][j]: d[i][j]=d[i][k]+d[k][j]
    out=[]
    for _ in range(q):
        a,b=map(int,input().split()); out.append(str(d[a][b] if d[a][b]<inf else -1))
    print('\\n'.join(out))""",
[("3 3 3\n0 1 4\n1 2 3\n0 2 10\n0 2\n2 0\n1 1\n","7\n-1\n0"),("2 2 2\n0 1 5\n0 1 2\n0 1\n1 0\n","2\n-1"),("1 0 2\n0 0\n0 0\n","0\n0"),("4 3 2\n0 1 -2\n1 2 5\n2 3 1\n0 3\n3 0\n","4\n-1"),("3 2 2\n0 1 1\n1 2 1\n0 2\n2 2\n","2\n0"),("3 0 2\n0 1\n2 0\n","-1\n-1")], "The route 0 to 1 to 2 costs 7.")

add(165, "Prim minimum spanning forest weight", "Medium", ["graphs", "minimum-spanning-tree", "heaps"],
"Line 1 is v e; next e lines are undirected u v w edges. Print the total weight of a minimum spanning forest, including isolated vertices as zero-cost components.",
["1 <= v <= 20,000 and 0 <= e <= 100,000", "Vertices are 0 through v-1 and weights are signed 32-bit integers."],
["Start a heap from every unvisited component.", "Take the cheapest edge entering an unvisited vertex.", "Do not add an edge whose endpoint was already chosen."], "O(e log v) time, O(v + e) auxiliary space",
"""import heapq
def solve():
    v,e=map(int,input().split()); g=[[] for _ in range(v)]
    for _ in range(e):
        a,b,w=map(int,input().split()); g[a].append((w,b)); g[b].append((w,a))
    seen=[False]*v; ans=0
    for s in range(v):
        if seen[s]: continue
        heap=[(0,s)]
        while heap:
            w,u=heapq.heappop(heap)
            if seen[u]: continue
            seen[u]=True; ans+=w
            for edge in g[u]:
                if not seen[edge[1]]: heapq.heappush(heap,edge)
    print(ans)""",
[("4 5\n0 1 1\n1 2 2\n0 2 4\n2 3 1\n1 3 5\n","4"),("3 1\n0 1 7\n","7"),("1 0\n","0"),("3 3\n0 1 -2\n1 2 1\n0 2 4\n","-1"),("4 4\n0 1 10\n0 1 1\n1 2 2\n2 3 3\n","6"),("5 2\n0 1 2\n3 4 3\n","5")], "Edges 0-1, 1-2, and 2-3 give total 4.")


add(166, "Articulation point indices", "Hard", ["graphs", "depth-first-search"],
"Line 1 is v e; next e lines are undirected edges. Print all articulation-point vertex indices in ascending order, or a blank line when none exist.",
["1 <= v <= 8,000 and 0 <= e <= 30,000", "The graph is simple, undirected, and vertices are 0 through v-1; the vertex bound caps output."],
["Track discovery time and lowest reachable ancestor.", "A non-root separates a child when low[child] is at least its time.", "A root needs at least two DFS children."], "O(v + e) time, O(v + e) auxiliary space",
"""def solve():
    v,e=map(int,input().split()); g=[[] for _ in range(v)]
    for _ in range(e):
        a,b=map(int,input().split()); g[a].append(b); g[b].append(a)
    tin=[-1]*v; low=[0]*v; parent=[-1]*v; edge_at=[0]*v; children=[0]*v; cut=[False]*v; timer=0
    for root in range(v):
        if tin[root]>=0: continue
        tin[root]=low[root]=timer; timer+=1; stack=[root]
        while stack:
            u=stack[-1]
            if edge_at[u]<len(g[u]):
                z=g[u][edge_at[u]]; edge_at[u]+=1
                if z==parent[u]: continue
                if tin[z]>=0: low[u]=min(low[u],tin[z])
                else:
                    parent[z]=u; children[u]+=1; tin[z]=low[z]=timer; timer+=1; stack.append(z)
            else:
                stack.pop(); p=parent[u]
                if p<0: cut[u]=children[u]>1
                else:
                    low[p]=min(low[p],low[u])
                    if parent[p]>=0 and low[u]>=tin[p]: cut[p]=True
    print(*[i for i in range(v) if cut[i]])""",
[("5 4\n0 1\n1 2\n1 3\n3 4\n","1 3"),("3 3\n0 1\n1 2\n2 0\n",""),("1 0\n",""),("4 3\n0 1\n0 2\n0 3\n","0"),("6 4\n0 1\n1 2\n3 4\n4 5\n","1 4"),("4 3\n0 1\n1 2\n2 3\n","1 2")], "Removing 1 splits the left branch; removing 3 isolates 4.")

add(167, "Bridge edge list", "Hard", ["graphs", "depth-first-search"],
"Line 1 is v e; next e lines are distinct undirected edges. Print every bridge as min_endpoint max_endpoint, one per line, sorted lexicographically.",
["1 <= v <= 100,000 and 0 <= e <= 200,000", "The graph is simple, undirected, and vertices are 0 through v-1.", "The answer contains at most 4,000 bridges, keeping output below the local runner limit."],
["Use the same low-link values as articulation points.", "A tree edge is a bridge when its child cannot reach an ancestor.", "Normalize and sort the reported endpoints."], "O(v + e) time, O(v + e) auxiliary space",
"""def solve():
    v,e=map(int,input().split()); g=[[] for _ in range(v)]
    for _ in range(e):
        a,b=map(int,input().split()); g[a].append(b); g[b].append(a)
    tin=[-1]*v; low=[0]*v; parent=[-1]*v; edge_at=[0]*v; ans=[]; timer=0
    for root in range(v):
        if tin[root]>=0: continue
        tin[root]=low[root]=timer; timer+=1; stack=[root]
        while stack:
            u=stack[-1]
            if edge_at[u]<len(g[u]):
                z=g[u][edge_at[u]]; edge_at[u]+=1
                if z==parent[u]: continue
                if tin[z]>=0: low[u]=min(low[u],tin[z])
                else: parent[z]=u; tin[z]=low[z]=timer; timer+=1; stack.append(z)
            else:
                stack.pop(); p=parent[u]
                if p>=0:
                    low[p]=min(low[p],low[u])
                    if low[u]>tin[p]: ans.append((min(p,u),max(p,u)))
    print('\\n'.join(f'{a} {b}' for a,b in sorted(ans)))""",
[("5 4\n0 1\n1 2\n1 3\n3 4\n","0 1\n1 2\n1 3\n3 4"),("3 3\n0 1\n1 2\n2 0\n",""),("2 1\n0 1\n","0 1"),("4 4\n0 1\n1 2\n2 0\n2 3\n","2 3"),("4 2\n0 1\n2 3\n","0 1\n2 3"),("1 0\n","")], "Each edge in this tree disconnects the graph when removed.")

add(168, "Undirected Euler trail feasibility", "Medium", ["graphs", "eulerian-path"],
"Line 1 is v e; next e lines are undirected edges. Print YES iff there is a trail using every edge exactly once. Isolated vertices do not affect connectivity.",
["1 <= v <= 200,000 and 0 <= e <= 200,000", "Vertices are 0 through v-1; parallel edges and self-loops may appear."],
["All non-isolated vertices must be in one component.", "Count odd degrees, with a self-loop adding two.", "An Euler trail has zero or two odd-degree vertices."], "O(v + e) time, O(v + e) auxiliary space",
"""from collections import deque
def solve():
    v,e=map(int,input().split()); g=[[] for _ in range(v)]; deg=[0]*v
    for _ in range(e):
        a,b=map(int,input().split()); g[a].append(b); g[b].append(a); deg[a]+=1; deg[b]+=1
    start=next((i for i in range(v) if deg[i]),-1)
    if start<0: print('YES'); return
    seen=[False]*v; seen[start]=True; q=deque([start])
    while q:
        u=q.popleft()
        for z in g[u]:
            if not seen[z]: seen[z]=True; q.append(z)
    print('YES' if all(not deg[i] or seen[i] for i in range(v)) and sum(x%2 for x in deg) in (0,2) else 'NO')""",
[("3 2\n0 1\n1 2\n","YES"),("4 3\n0 1\n0 2\n0 3\n","NO"),("3 0\n","YES"),("4 2\n0 1\n2 3\n","NO"),("2 2\n0 1\n0 1\n","YES"),("1 1\n0 0\n","YES")], "A path already uses each of its two edges exactly once.")

add(169, "Fenwick range sums with updates", "Medium", ["data-structures", "fenwick-tree"],
"Line 1 is n q; line 2 has n integers. Each next line is either SET i x or SUM l r. SET replaces index i with x. For every SUM print the inclusive range sum.",
["1 <= n, q <= 200,000", "0 <= i, l <= r < n; values fit signed 32-bit integers.", "At most 3,500 commands are SUM queries, keeping output bounded."],
["Store differences between the old and new value.", "A Fenwick prefix sum uses repeated subtraction of the low bit.", "Subtract two prefixes for an inclusive range."], "O((n + q) log n) time, O(n) auxiliary space",
"""def solve():
    n,q=map(int,input().split()); a=list(map(int,input().split())); bit=[0]*(n+1)
    def add(i,x):
        i+=1
        while i<=n: bit[i]+=x; i+=i&-i
    def pref(i):
        total=0; i+=1
        while i: total+=bit[i]; i-=i&-i
        return total
    for i,x in enumerate(a): add(i,x)
    out=[]
    for _ in range(q):
        p=input().split()
        if p[0]=='SET':
            i,x=map(int,p[1:]); add(i,x-a[i]); a[i]=x
        else:
            l,r=map(int,p[1:]); out.append(str(pref(r)-(pref(l-1) if l else 0)))
    print('\\n'.join(out))""",
[("4 4\n1 2 3 4\nSUM 0 3\nSET 1 10\nSUM 1 2\nSUM 0 0\n","10\n13\n1"),("1 3\n5\nSUM 0 0\nSET 0 -2\nSUM 0 0\n","5\n-2"),("3 2\n0 0 0\nSUM 0 2\nSUM 1 1\n","0\n0"),("5 4\n1 -1 1 -1 1\nSUM 1 3\nSET 2 7\nSUM 0 4\nSUM 2 2\n","-1\n7\n7"),("2 3\n9 8\nSET 0 9\nSUM 0 1\nSUM 1 1\n","17\n8"),("4 3\n1 1 1 1\nSET 3 5\nSUM 2 3\nSUM 0 2\n","6\n3")], "After replacing index 1, indices 1 through 2 sum to 13.")

add(170, "Segment tree range minimum", "Medium", ["data-structures", "segment-tree"],
"Line 1 is n q; line 2 has n integers. Each next line is either SET i x or MIN l r. SET replaces index i with x. For every MIN print the inclusive range minimum.",
["1 <= n, q <= 200,000", "0 <= i, l <= r < n; values fit signed 32-bit integers.", "At most 3,500 commands are MIN queries, keeping output bounded."],
["Use an iterative tree with leaves at a power-of-two base.", "After a replacement, repair ancestors to the root.", "Move query endpoints inward while accumulating the answer."], "O((n + q) log n) time, O(n) auxiliary space",
"""def solve():
    n,q=map(int,input().split()); a=list(map(int,input().split())); size=1
    while size<n: size*=2
    t=[10**30]*(2*size); t[size:size+n]=a
    for i in range(size-1,0,-1): t[i]=min(t[2*i],t[2*i+1])
    out=[]
    for _ in range(q):
        p=input().split()
        if p[0]=='SET':
            i,x=map(int,p[1:]); i+=size; t[i]=x
            while i>1: i//=2; t[i]=min(t[2*i],t[2*i+1])
        else:
            l,r=map(int,p[1:]); l+=size; r+=size; ans=10**30
            while l<=r:
                if l%2: ans=min(ans,t[l]); l+=1
                if not r%2: ans=min(ans,t[r]); r-=1
                l//=2; r//=2
            out.append(str(ans))
    print('\\n'.join(out))""",
[("4 4\n5 2 7 3\nMIN 0 3\nSET 1 9\nMIN 0 2\nMIN 2 3\n","2\n5\n3"),("1 3\n4\nMIN 0 0\nSET 0 -1\nMIN 0 0\n","4\n-1"),("3 2\n0 0 0\nMIN 0 2\nMIN 1 1\n","0\n0"),("5 3\n8 6 7 5 3\nMIN 1 3\nSET 3 10\nMIN 0 4\n","5\n3"),("2 2\n-2 -3\nSET 1 1\nMIN 0 1\n","-2"),("4 3\n1 2 3 4\nSET 0 9\nMIN 0 1\nMIN 2 3\n","2\n3")], "The initial minimum is 2; after replacing it, the first three values have minimum 5.")


add(171,"Sparse table range minimum","Medium",["data-structures","sparse-table"],"Read n q, n integers, then q inclusive l r queries. Print each static range minimum.",["1 <= n <= 200,000 and 1 <= q <= 5,000","0 <= l <= r < n; values fit signed 32-bit integers, and q is output-capped."],["Precompute power-of-two blocks.","Use two overlapping blocks.","No updates occur."],"O(n log n + q) time, O(n log n) auxiliary space", """def solve():
 n,q=map(int,input().split()); a=list(map(int,input().split())); st=[a]
 while 2**len(st)<=n:
  b=st[-1]; h=2**(len(st)-1); st.append([min(b[i],b[i+h]) for i in range(len(b)-h)])
 print('\\n'.join(str(min(st[(r-l+1).bit_length()-1][l],st[(r-l+1).bit_length()-1][r-2**((r-l+1).bit_length()-1)+1])) for l,r in (map(int,input().split()) for _ in range(q))))""",
[("5 2\n5 2 7 1 3\n0 4\n1 2\n","1\n2"),("1 1\n-4\n0 0\n","-4"),("4 1\n1 1 1 1\n2 3\n","1"),("3 1\n3 1 2\n0 1\n","1"),("4 1\n-1 -5 2 0\n0 2\n","-5"),("6 1\n9 8 7 6 5 4\n3 5\n","4")],"The whole range reaches 1.")

add(172,"Weighted edit distance","Hard",["dynamic-programming","strings"],"Read source and target as printable-ASCII lines, then insert delete replace costs. Print the least transform cost; replacing equal characters costs zero.",["Lengths are at most 2,000.","Costs are nonnegative integers."],["Initialize empty prefixes.","Compare insertion, deletion, replacement.","Keep one DP row."],"O(mn) time, O(n) auxiliary space", """def solve():
 a=input(); b=input(); ins,de,rep=map(int,input().split()); d=[j*ins for j in range(len(b)+1)]
 for i,x in enumerate(a,1):
  z=[i*de]+[0]*len(b)
  for j,y in enumerate(b,1): z[j]=min(d[j]+de,z[j-1]+ins,d[j-1]+(0 if x==y else rep))
  d=z
 print(d[-1])""",
[("kitten\nsitting\n1 1 1\n","3"),("a\nb\n5 5 20\n","10"),("\nabc\n2 3 4\n","6"),("abc\n\n2 3 4\n","9"),("abc\nabc\n7 8 9\n","0"),("ab\nba\n1 1 3\n","2")],"Three unit edits transform kitten.")

add(173,"Regex whole-string match","Hard",["dynamic-programming","strings"],"Read text then a valid pattern using lowercase literals, . and x*. Print YES only for a complete match.",["Both lengths are at most 1,000.","A star has one preceding atom."],["A star skips or consumes its atom.","Initialize empty matches.","Match the full prefixes."],"O(mn) time, O(n) space", """def solve():
 s=input().rstrip(); p=input().rstrip(); d=[False]*(len(p)+1); d[0]=True
 for j in range(2,len(p)+1):
  if p[j-1]=='*': d[j]=d[j-2]
 for x in s:
  z=[False]*(len(p)+1)
  for j in range(1,len(p)+1): z[j]=z[j-2] or ((p[j-2]=='.' or p[j-2]==x) and d[j]) if p[j-1]=='*' else (p[j-1]=='.' or p[j-1]==x) and d[j-1]
  d=z
 print('YES' if d[-1] else 'NO')""",
[("aab\nc*a*b\n","YES"),("mississippi\nmis*is*p*.\n","NO"),("\na*b*c*\n","YES"),("ab\n.*\n","YES"),("aaa\na*a\n","YES"),("abcd\nd*\n","NO")],"c* can consume nothing.")

add(174,"Digit count with no equal neighbors","Hard",["dynamic-programming","digit-dp"],"Read N. Count integers from 0 through N whose usual decimal form has no equal adjacent digits; 0 qualifies.",["0 <= N <= 10^18"],["Use tight and started states.","Do not compare leading zeroes.","Include zero at the end."],"O(digits * 100) time, O(digits * 100) space", """from functools import lru_cache
def solve():
 a=list(map(int,input().strip()))
 @lru_cache(None)
 def f(i,last,tight,started):
  if i==len(a): return 1
  return sum(f(i+1,d if started or d else 10,tight and d==a[i],started or d>0) for d in range((a[i] if tight else 9)+1) if not(started and d==last))
 print(f(0,10,True,False))""",
[("20\n","20"),("0\n","1"),("9\n","10"),("11\n","11"),("100\n","91"),("101\n","92")],"Only 11 fails through 20.")

add(175,"Bitmask travelling-salesperson cycle","Hard",["dynamic-programming","bitmask"],"Read n then a directed cost matrix; -1 means no edge. Start at 0, visit each vertex once, and return to 0. Print the minimum cost or -1; for n=1 the empty tour costs zero.",["1 <= n <= 15","Costs are -1 or in [0, 10^9]."],["State is visited mask and endpoint.","Extend to unvisited vertices.","Add the final return edge."],"O(2^n n^2) time, O(2^n n) auxiliary space", """def solve():
 n=int(input()); w=[list(map(int,input().split())) for _ in range(n)]
 if n==1: print(0); return
 I=10**30; d=[[I]*n for _ in range(1<<n)]; d[1][0]=0
 for m in range(1<<n):
  for u in range(n):
   for v in range(n):
    if d[m][u]<I and not m>>v&1 and w[u][v]>=0:d[m|1<<v][v]=min(d[m|1<<v][v],d[m][u]+w[u][v])
 x=min([d[-1][u]+w[u][0] for u in range(n) if w[u][0]>=0]or[I]); print(x if x<I else -1)""",
[("3\n0 1 10\n10 0 2\n3 10 0\n","6"),("2\n0 5\n7 0\n","12"),("1\n0\n","0"),("3\n0 1 -1\n-1 0 1\n-1 -1 0\n","-1"),("3\n0 0 5\n2 0 1\n1 4 0\n","2"),("2\n0 -1\n-1 0\n","-1")],"0-1-2-0 costs 6.")

add(176,"Matrix-chain minimum cost","Hard",["dynamic-programming","interval-dp"],"Read n then n+1 dimensions. Print the smallest scalar multiplication count for the matrix chain.",["1 <= n <= 150","The next line contains exactly n+1 positive dimensions."],["Choose the final split.","Single matrices cost zero.","Use interval DP."],"O(n^3) time, O(n^2) auxiliary space", """def solve():
 n=int(input()); a=list(map(int,input().split())); d=[[0]*n for _ in range(n)]
 for z in range(2,n+1):
  for i in range(n-z+1):
   j=i+z-1; d[i][j]=min(d[i][k]+d[k+1][j]+a[i]*a[k+1]*a[j+1] for k in range(i,j))
 print(d[0][-1])""",
[("3\n10 30 5 60\n","4500"),("1\n5 7\n","0"),("2\n10 20 30\n","6000"),("4\n40 20 30 10 30\n","26000"),("3\n1 2 3 4\n","18"),("3\n10 10 10 10\n","2000")],"The best parenthesization costs 4500.")

add(177,"Huffman weighted code length","Medium",["greedy","heaps"],"Read n and n frequencies. Print the minimum weighted binary prefix-code length; a single symbol costs zero.",["1 <= n <= 200,000","Frequencies are nonnegative."],["Merge the two smallest weights.","Each merge contributes cost.","Use a heap."],"O(n log n) time, O(n) space", """import heapq
def solve():
 n=int(input()); h=list(map(int,input().split()))
 if len(h)==1:print(0);return
 heapq.heapify(h);s=0
 while len(h)>1:x=heapq.heappop(h)+heapq.heappop(h);s+=x;heapq.heappush(h,x)
 print(s)""",
[("4\n5 9 12 13\n","78"),("1\n10\n","0"),("2\n1 1\n","2"),("3\n1 1 1\n","5"),("4\n0 0 1 1\n","3"),("5\n2 3 7 9 18\n","77")],"Merge costs sum to 78.")

add(178,"Minimum prerequisite semesters","Medium",["graphs","topological-sort"],"Read n m then pairs a b meaning a must precede b. Unlimited available courses fit in one semester. Print minimum semesters or -1 for a cycle.",["1 <= n <= 200,000 and 0 <= m <= 200,000","Courses are 0 through n-1."],["Process one indegree-zero layer per semester.","Decrease indegrees.","Unprocessed courses imply a cycle."],"O(n+m) time, O(n+m) auxiliary space", """from collections import deque
def solve():
 n,m=map(int,input().split());g=[[]for _ in range(n)];d=[0]*n
 for _ in range(m):a,b=map(int,input().split());g[a].append(b);d[b]+=1
 q=deque(i for i in range(n)if not d[i]);done=s=0
 while q:
  s+=1
  for _ in range(len(q)):
   u=q.popleft();done+=1
   for v in g[u]:d[v]-=1;q.append(v) if not d[v] else None
 print(s if done==n else -1)""",
[("4 3\n0 1\n1 2\n0 3\n","3"),("3 3\n0 1\n1 2\n2 0\n","-1"),("3 0\n","1"),("5 4\n0 2\n1 2\n2 3\n2 4\n","3"),("1 0\n","1"),("4 2\n0 2\n1 3\n","2")],"A chain requires three semesters.")

add(179,"Aho-Corasick multi-pattern counts","Hard",["strings","trie","pattern-matching"],"Read m, m nonempty lowercase patterns, then lowercase text. Print one overlapping count per pattern in input order.",["1 <= m <= 8,000 and total pattern length D <= 20,000","Text length T <= 200,000; all input strings are lowercase, and m is output-capped."],["Build failure links.","Complete missing lowercase transitions through failure states.","Propagate visit counts back along failure links."],"O(26*D + T + m) time, O(26*D + m) auxiliary space", """from collections import deque
def solve():
 m=int(input()); patterns=[input().strip() for _ in range(m)]; go=[[0]*26]; fail=[0]; terminal=[]
 for word in patterns:
  u=0
  for char in word:
   c=ord(char)-97
   if not go[u][c]: go[u][c]=len(go); go.append([0]*26); fail.append(0)
   u=go[u][c]
  terminal.append(u)
 q=deque(); order=[]
 for c in range(26):
  if go[0][c]: q.append(go[0][c])
 while q:
  u=q.popleft(); order.append(u)
  for c in range(26):
   v=go[u][c]
   if v: fail[v]=go[fail[u]][c]; q.append(v)
   else: go[u][c]=go[fail[u]][c]
 count=[0]*len(go); u=0
 for char in input().strip(): u=go[u][ord(char)-97]; count[u]+=1
 for u in reversed(order): count[fail[u]]+=count[u]
 print('\\n'.join(str(count[u]) for u in terminal))""",
[("3\nhe\nshe\nhers\nushers\n","1\n1\n1"),("2\na\naa\naaaa\n","4\n3"),("1\nabc\nabc\n","1"),("2\nab\nb\nabab\n","2\n2"),("3\na\na\naa\naa\n","2\n2\n1"),("2\nabc\ndef\nzzzz\n","0\n0")],"All three patterns appear once.")

add(180,"Burst balloons maximum coins","Hard",["dynamic-programming","interval-dp"],"Read n then balloon values. A burst earns current nearest-left times value times nearest-right; outside values are 1. Print maximum coins.",["0 <= n <= 150","The next line contains exactly n values from 0 through 100."],["Choose the last balloon in each interval.","Pad boundaries with 1.","Combine two subintervals."],"O(n^3) time, O(n^2) auxiliary space", """def solve():
 n=int(input());a=[1]+list(map(int,input().split()))+[1];d=[[0]*(n+2)for _ in range(n+2)]
 for z in range(1,n+1):
  for l in range(1,n-z+2):
   r=l+z-1
   for k in range(l,r+1):d[l][r]=max(d[l][r],d[l][k-1]+d[k+1][r]+a[l-1]*a[k]*a[r+1])
 print(d[1][n]if n else 0)""",
[("4\n3 1 5 8\n","167"),("1\n7\n","7"),("0\n\n","0"),("2\n1 5\n","10"),("3\n1 1 1\n","3"),("4\n0 2 0 3\n","9")],"Choosing the last burst yields 167.")

PYTHON_CURATED_161_180 = ITEMS
if len(PYTHON_CURATED_161_180) != 20:
    raise RuntimeError("expected exactly 20 exercises")
