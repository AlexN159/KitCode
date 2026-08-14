"""Data-only curated Python exercise tranche 141--160."""
from __future__ import annotations

STARTER = "import sys\n\ndef solve() -> None:\n    pass\n\nif __name__ == '__main__':\n    solve()\n"
ITEMS = []

def add(num, title, difficulty, topics, description, constraints, hints, complexity, body, cases, explanation):
    records = [{"input": source, "expected_output": result} for source, result in cases]
    ITEMS.append({"id": f"python-curated-{num:03d}", "language": "python", "title": title,
        "difficulty": difficulty, "topics": topics, "practice_frequency": "Common",
        "description": description, "constraints": constraints, "hints": hints,
        "expected_complexity": complexity, "starter_code": STARTER,
        "solution": "import sys\n" + body.strip() + "\n\nif __name__ == '__main__':\n    solve()\n",
        "examples": [{"input": records[0]["input"], "output": records[0]["expected_output"], "explanation": explanation}],
        "public_tests": records[:2], "hidden_tests": records[2:]})

add(141, "Linked-list cycle entry", "Medium", ["linked-lists","two-pointers"],
"Line 1 is n; line 2 has n serialized values; line 3 has n next indices (-1 is null). Starting at node 0, print the index where its reachable cycle begins, or -1.",
["1 <= n <= 200,000", "Line 2 has exactly n signed 32-bit values; every next index is -1 or in [0,n).", "Node 0 is the head; nodes not reachable from it do not affect the answer."],
["Move slow one link and fast two links.", "After a meeting, restart slow at the head.", "A null fast link means there is no cycle."], "O(n) time, O(1) auxiliary space",
"""def solve():
    n=int(input()); input(); nxt=list(map(int,input().split())); slow=fast=0
    while fast!=-1 and nxt[fast]!=-1:
        slow=nxt[slow]; fast=nxt[nxt[fast]]
        if slow==fast:
            slow=0
            while slow!=fast: slow=nxt[slow]; fast=nxt[fast]
            print(slow); return
    print(-1)""",
[("4\n8 1 7 3\n1 2 3 1\n","1"),("3\n1 2 3\n1 2 -1\n","-1"),("1\n9\n0\n","0"),("5\n0 0 0 0 0\n1 2 3 4 2\n","2"),("4\n4 5 6 7\n-1 0 1 2\n","-1"),("6\n1 2 3 4 5 6\n1 2 3 4 5 3\n","3")], "Nodes 1, 2, and 3 loop back to node 1.")

add(142, "Middle node in a serialized list", "Easy", ["linked-lists","two-pointers"],
"Line 1 is n; line 2 has the n node values; line 3 has n next indices (-1 is null); line 4 is the head index. All n nodes form one acyclic chain. Print the index and value of its middle node, choosing the second middle when n is even.",
["1 <= n <= 200,000", "Every next index is -1 or in [0,n).", "The head is in [0,n), and following next visits every node exactly once before -1."],
["Move slow one link while fast moves two.", "Stop when fast reaches the end.", "This stopping rule leaves slow at the second middle of an even list."], "O(n) time, O(1) auxiliary space",
"""def solve():
    n=int(input()); values=list(map(int,input().split())); nxt=list(map(int,input().split())); slow=fast=int(input())
    while fast!=-1 and nxt[fast]!=-1:
        slow=nxt[slow]; fast=nxt[nxt[fast]]
    print(slow,values[slow])""",
[("5\n10 20 30 40 50\n1 2 3 4 -1\n0\n","2 30"),("4\n1 2 3 4\n1 2 3 -1\n0\n","2 3"),("1\n9\n-1\n0\n","0 9"),("5\n8 9 10 11 12\n3 -1 1 4 2\n0\n","4 12"),("6\n100 200 300 400 500 600\n3 -1 4 1 0 2\n5\n","0 100"),("2\n-4 7\n-1 0\n1\n","0 -4")], "Slow reaches index 2, the middle of the five-node chain.")

add(143, "Reorder list first-last", "Medium", ["linked-lists","two-pointers"],
"Line 1 is n and line 2 is a serialized list. Print values in first, last, second, second-last order.",
["1 <= n <= 5,000", "Values fit signed 32-bit integers."],
["Read from matching ends.", "Stop when the indices cross.", "An odd list has one middle value."], "O(n) time, O(n) output space",
"""def solve():
    n=int(input()); a=list(map(int,input().split())); out=[]; l=0; r=n-1
    while l<=r:
        out.append(a[l]); l+=1
        if l<=r: out.append(a[r]); r-=1
    print(*out)""",
[("5\n1 2 3 4 5\n","1 5 2 4 3"),("4\n10 20 30 40\n","10 40 20 30"),("1\n7\n","7"),("2\n-1 4\n","-1 4"),("6\n1 1 1 1 1 1\n","1 1 1 1 1 1"),("7\n0 1 2 3 4 5 6\n","0 6 1 5 2 4 3")], "Alternating ends turns 1 2 3 4 5 into 1 5 2 4 3.")

add(144, "Height-balanced binary tree", "Medium", ["trees","depth-first-search"],
"Line 1 is n; line 2 is a complete positional-array tree of n integer or # tokens, where children of index i are 2*i+1 and 2*i+2. Print YES iff all child-height differences are at most one.",
["1 <= n <= 200,000", "The root is an integer; # marks a missing position.", "No integer token has a # ancestor."],
["Return a height or failure marker.", "A missing child has height zero.", "Propagate imbalance immediately."], "O(n) time, O(h) auxiliary space",
"""def solve():
    n=int(input()); t=input().split()
    def h(i):
        if i>=n or t[i]=='#': return 0
        a=h(2*i+1); b=h(2*i+2)
        return -1 if a<0 or b<0 or abs(a-b)>1 else max(a,b)+1
    print('YES' if h(0)>=0 else 'NO')""",
[("7\n1 2 3 4 5 # #\n","YES"),("7\n1 2 # 3 # # #\n","NO"),("1\n1\n","YES"),("3\n1 # 2\n","YES"),("15\n1 2 3 4 5 6 7 8 # # # # # # #\n","YES"),("9\n1 2 3 4 # # # 5 #\n","NO")], "The root's subtrees have equal height.")

add(145, "Binary-tree diameter", "Medium", ["trees","depth-first-search"],
"Read n then a complete positional-array tree of n integer or # tokens, where children of index i are 2*i+1 and 2*i+2. Print the largest number of edges on any path between two nodes.",
["1 <= n <= 200,000", "The root is an integer; # marks a missing position.", "No integer token has a # ancestor."],
["Join the two child heights through each node.", "Update the best during postorder.", "An empty child has height zero."], "O(n) time, O(h) auxiliary space",
"""def solve():
    n=int(input()); t=input().split(); best=0
    def h(i):
        nonlocal best
        if i>=n or t[i]=='#': return 0
        a=h(2*i+1); b=h(2*i+2); best=max(best,a+b); return max(a,b)+1
    h(0); print(best)""",
[("7\n1 2 3 4 5 # #\n","3"),("1\n9\n","0"),("7\n1 2 3 # # 4 5\n","3"),("3\n1 # 2\n","1"),("15\n1 2 3 4 5 6 7 # # # # # # # #\n","4"),("7\n1 # 2 # # # 3\n","2")], "The path 4 through 1 to 3 uses three edges.")

add(146, "Right-side binary-tree view", "Easy", ["trees","breadth-first-search"],
"Read n complete positional-array tree tokens, where # is missing and children of index i are 2*i+1 and 2*i+2. Print the rightmost existing node at each depth.",
["1 <= n <= 200,000", "The root token is an integer.", "No integer token has a # ancestor."],
["Process each depth separately.", "Keep the last existing token in that depth.", "Never print a missing marker."], "O(n) time, O(w) auxiliary space",
"""def solve():
    n=int(input()); t=input().split(); out=[]; start=0; width=1
    while start<n:
        level=[t[i] for i in range(start,min(n,start+width)) if t[i]!='#']
        if level: out.append(level[-1])
        start+=width; width*=2
    print(*out)""",
[("7\n1 2 3 4 # # 5\n","1 3 5"),("1\n8\n","8"),("7\n1 2 # 3 # # #\n","1 2 3"),("7\n1 # 2 # # 3 #\n","1 2 3"),("15\n1 2 3 # 5 6 # # # 7 # # # # #\n","1 3 6 7"),("3\n-1 -2 -3\n","-1 -3")], "At depth two, node 5 is the rightmost existing node.")

add(147, "Root-to-leaf target path", "Medium", ["trees","depth-first-search"],
"Line 1 is n, line 2 is a complete positional-array integer/# tree whose children are at 2*i+1 and 2*i+2, and line 3 is target. Print YES iff a root-to-leaf path sums to target.",
["1 <= n <= 200,000", "The root is an integer and node values fit signed 32-bit integers.", "No integer token has a # ancestor."],
["Carry remaining target downward.", "Compare only at leaves.", "A # token contributes no path."], "O(n) time, O(h) auxiliary space",
"""def solve():
    n=int(input()); t=input().split(); target=int(input())
    def go(i,remain):
        if i>=n or t[i]=='#': return False
        remain-=int(t[i]); l=2*i+1; r=l+1
        if (l>=n or t[l]=='#') and (r>=n or t[r]=='#'): return remain==0
        return go(l,remain) or go(r,remain)
    print('YES' if go(0,target) else 'NO')""",
[("13\n5 4 8 11 # 13 4 7 2 # # # 1\n22\n","YES"),("7\n1 2 3 # # 4 5\n8\n","YES"),("1\n-2\n-2\n","YES"),("3\n1 2 3\n1\n","NO"),("7\n1 -2 3 4 5 # #\n3\n","YES"),("7\n1 2 3 4 # # #\n6\n","NO")], "The path 5, 4, 11, 2 sums to 22.")

add(148, "Lowest common ancestor by node index", "Medium", ["trees","binary-tree"],
"Line 1 is n, line 2 is a complete positional-array integer/# tree, and line 3 gives existing zero-based token indices p q. Print the lowest common ancestor index.",
["1 <= n <= 200,000", "p and q name non-# tokens, and no integer token has a # ancestor.", "Children of index i are 2*i+1 and 2*i+2."],
["A parent index is (i-1)//2.", "Record one node's ancestors.", "Walk the other node upward."], "O(h) time, O(h) auxiliary space",
"""def solve():
    n=int(input()); input(); p,q=map(int,input().split()); seen=set()
    while p>=0: seen.add(p); p=(p-1)//2 if p else -1
    while q not in seen: q=(q-1)//2
    print(q)""",
[("7\n1 2 3 4 5 6 7\n3 4\n","1"),("7\n1 2 3 4 # 6 7\n3 6\n","0"),("1\n9\n0 0\n","0"),("15\n1 2 3 4 5 6 7 8 9 # # # # # #\n7 8\n","3"),("7\n1 2 3 # # 4 5\n5 6\n","2"),("7\n1 2 3 4 5 6 7\n1 4\n","1")], "Indices 3 and 4 first meet at index 1.")

add(149, "Top-k frequent values", "Medium", ["hash-maps","heaps"],
"Line 1 contains n k; line 2 contains n integers. Print the k highest-frequency values, breaking ties by smaller value.",
["1 <= k <= min(distinct count, 5,000) and n <= 200,000", "Values fit signed 32-bit integers."],
["Count values first.", "Sort by negative frequency then value.", "Do not rely on insertion order."], "O(n + d log d) time, O(d) auxiliary space",
"""from collections import Counter
def solve():
    n,k=map(int,input().split()); a=list(map(int,input().split())); c=Counter(a)
    print(*[x for x,_ in sorted(c.items(),key=lambda p:(-p[1],p[0]))[:k]])""",
[("6 2\n1 1 2 2 3 4\n","1 2"),("7 3\n4 4 4 -1 -1 2 2\n","4 -1 2"),("1 1\n9\n","9"),("8 2\n3 3 3 2 2 1 1 1\n","1 3"),("5 3\n-2 -2 0 1 1\n","-2 1 0"),("10 4\n5 4 3 2 1 5 4 3 2 1\n","1 2 3 4")], "Both 1 and 2 occur twice, so 1 comes first.")

add(150, "Running median", "Medium", ["heaps","streaming"],
"Line 1 is n and line 2 is a stream. After every insertion print the lower median of values seen so far.",
["1 <= n <= 5,000", "Line 2 contains exactly n signed 32-bit integers."],
["Use a max heap for the lower half.", "Balance heaps after every insertion.", "Read the median from the lower heap top."], "O(n log n) time, O(n) auxiliary space",
"""import heapq
def solve():
    n=int(input()); lo=[]; hi=[]; out=[]
    for x in map(int,input().split()):
        heapq.heappush(lo,-x); heapq.heappush(hi,-heapq.heappop(lo))
        if len(hi)>len(lo): heapq.heappush(lo,-heapq.heappop(hi))
        out.append(str(-lo[0]))
    print(*out)""",
[("4\n5 2 10 1\n","5 2 5 2"),("5\n1 2 3 4 5\n","1 1 2 2 3"),("1\n-7\n","-7"),("6\n2 2 2 2 2 2\n","2 2 2 2 2 2"),("5\n10 -1 7 -3 4\n","10 -1 7 -1 4"),("7\n9 8 7 6 5 4 3\n","9 8 8 7 7 6 6")], "After 5, 2, 10, 1 the lower medians are 5, 2, 5, 2.")

add(151, "Dijkstra shortest distances", "Hard", ["graphs","shortest-path","heaps"],
"Line 1 contains v e s. The next e lines are directed edges u v w with nonnegative weights. Print distances from s to 0 through v-1, using -1 if unreachable.",
["1 <= v <= 5,000", "0 <= e <= 200,000", "0 <= w <= 1,000,000 and labels are in [0,v)."],
["Heap entries are tentative distance and vertex.", "Skip stale heap entries.", "Relax an edge only when it improves a distance."], "O((v+e) log v) time, O(v+e) auxiliary space",
"""import heapq
def solve():
    v,e,s=map(int,input().split()); g=[[] for _ in range(v)]
    for _ in range(e):
        a,b,w=map(int,input().split()); g[a].append((b,w))
    d=[10**30]*v; d[s]=0; q=[(0,s)]
    while q:
        x,u=heapq.heappop(q)
        if x!=d[u]: continue
        for z,w in g[u]:
            if x+w<d[z]: d[z]=x+w; heapq.heappush(q,(d[z],z))
    print(*[x if x<10**30 else -1 for x in d])""",
[("4 5 0\n0 1 4\n0 2 1\n2 1 2\n1 3 1\n2 3 5\n","0 3 1 4"),("3 1 1\n1 2 7\n","-1 0 7"),("1 0 0\n","0"),("4 5 0\n0 1 0\n1 2 0\n0 2 5\n2 3 1\n1 3 9\n","0 0 0 1"),("5 4 4\n4 3 2\n3 2 2\n2 1 2\n1 0 2\n","8 6 4 2 0"),("4 4 0\n0 1 10\n0 2 3\n2 1 1\n1 3 2\n","0 4 3 6")], "Going through vertex 2 improves the direct route.")

add(152, "Graph bipartite check", "Medium", ["graphs","breadth-first-search"],
"Line 1 contains v e; the next e lines are undirected edges. Print YES iff every edge crosses a two-color split.",
["1 <= v <= 200,000", "0 <= e <= 200,000", "Vertices are numbered 0 through v-1."],
["Color a vertex when visited first.", "Equal endpoint colors fail.", "Start each uncolored component."], "O(v+e) time, O(v) auxiliary space",
"""from collections import deque
def solve():
    v,e=map(int,input().split()); g=[[] for _ in range(v)]
    for _ in range(e):
        a,b=map(int,input().split()); g[a].append(b); g[b].append(a)
    c=[-1]*v
    for s in range(v):
        if c[s]>=0: continue
        c[s]=0; q=deque([s])
        while q:
            u=q.popleft()
            for z in g[u]:
                if c[z]<0: c[z]=c[u]^1; q.append(z)
                elif c[z]==c[u]: print('NO'); return
    print('YES')""",
[("4 4\n0 1\n1 2\n2 3\n3 0\n","YES"),("3 3\n0 1\n1 2\n2 0\n","NO"),("1 0\n","YES"),("2 1\n0 0\n","NO"),("5 2\n0 1\n3 4\n","YES"),("6 6\n0 1\n1 2\n2 3\n3 4\n4 5\n5 0\n","YES")], "A four-cycle alternates colors.")

add(153, "Strongly connected component count", "Hard", ["graphs","depth-first-search"],
"Line 1 contains v e; the next e lines are directed edges. Print the number of strongly connected components.",
["1 <= v <= 100,000", "0 <= e <= 200,000", "Vertices are numbered 0 through v-1."],
["Record finish order.", "Build reverse edges while reading.", "Explore reverse graph in reverse finish order."], "O(v+e) time, O(v+e) auxiliary space",
"""def solve():
    v,e=map(int,input().split()); g=[[] for _ in range(v)]; r=[[] for _ in range(v)]
    for _ in range(e):
        a,b=map(int,input().split()); g[a].append(b); r[b].append(a)
    seen=[False]*v; order=[]
    for start in range(v):
        if seen[start]: continue
        seen[start]=True; stack=[(start,0)]
        while stack:
            u,i=stack[-1]
            if i<len(g[u]):
                z=g[u][i]; stack[-1]=(u,i+1)
                if not seen[z]: seen[z]=True; stack.append((z,0))
            else: order.append(u); stack.pop()
    seen=[False]*v; ans=0
    for start in reversed(order):
        if seen[start]: continue
        ans+=1; seen[start]=True; stack=[start]
        while stack:
            u=stack.pop()
            for z in r[u]:
                if not seen[z]: seen[z]=True; stack.append(z)
    print(ans)""",
[("4 4\n0 1\n1 2\n2 0\n2 3\n","2"),("3 2\n0 1\n1 2\n","3"),("1 1\n0 0\n","1"),("5 6\n0 1\n1 0\n2 3\n3 2\n3 4\n4 4\n","3"),("4 4\n0 1\n1 0\n2 3\n3 2\n","2"),("6 7\n0 1\n1 2\n2 0\n2 3\n3 4\n4 5\n5 3\n","2")], "Vertices 0, 1, and 2 form one component; 3 forms another.")

add(154, "Redundant undirected edge", "Medium", ["graphs","union-find"],
"Line 1 contains v e; next e lines are undirected edges in insertion order. Print the first edge that creates a cycle, or NONE.",
["1 <= v <= 200,000", "0 <= e <= 200,000", "Vertices are numbered 0 through v-1."],
["Roots represent connected components.", "Equal roots mean a cycle.", "Compress paths and attach the smaller tree under the larger root."], "O(v + e * alpha(v)) time, O(v) auxiliary space",
"""def solve():
    v,e=map(int,input().split()); p=list(range(v)); size=[1]*v
    def f(x):
        while p[x]!=x: p[x]=p[p[x]]; x=p[x]
        return x
    for _ in range(e):
        a,b=map(int,input().split()); x,y=f(a),f(b)
        if x==y: print(a,b); return
        if size[x]<size[y]: x,y=y,x
        p[y]=x; size[x]+=size[y]
    print('NONE')""",
[("3 3\n0 1\n1 2\n2 0\n","2 0"),("4 3\n0 1\n1 2\n2 3\n","NONE"),("2 1\n0 0\n","0 0"),("5 5\n0 1\n2 3\n1 2\n3 4\n4 0\n","4 0"),("4 4\n0 1\n0 1\n2 3\n1 2\n","0 1"),("1 0\n","NONE")], "The third edge completes a triangle.")

add(155, "House robber", "Medium", ["dynamic-programming"],
"Line 1 is n; line 2 contains nonnegative house amounts. Print the greatest sum without choosing adjacent houses.",
["1 <= n <= 200,000", "0 <= amount <= 1,000,000."],
["Compare taking this house with skipping it.", "Keep only two previous values.", "The optimum may skip the last house."], "O(n) time, O(1) auxiliary space",
"""def solve():
    n=int(input()); prev2=prev=0
    for x in map(int,input().split()): prev2,prev=prev,max(prev,prev2+x)
    print(prev)""",
[("4\n2 7 9 3\n","11"),("1\n8\n","8"),("5\n0 0 0 0 0\n","0"),("5\n2 1 1 2 9\n","12"),("6\n10 1 1 10 1 1\n","21"),("4\n1 2 3 1\n","4")], "Taking 2 and 9 gives 11.")

add(156, "Zero-one knapsack", "Hard", ["dynamic-programming","knapsack"],
"Line 1 contains n capacity; line 2 has n values; line 3 has n positive weights. Print the best value using each item at most once.",
["1 <= n <= 200", "0 <= capacity <= 20,000", "0 <= value <= 1,000,000 and weights are positive."],
["Let dp[c] be best under capacity c.", "Scan capacities downward.", "Leaving capacity unused is valid."], "O(n * capacity) time, O(capacity) auxiliary space",
"""def solve():
    n,c=map(int,input().split()); val=list(map(int,input().split())); wt=list(map(int,input().split())); dp=[0]*(c+1)
    for x,w in zip(val,wt):
        for j in range(c,w-1,-1): dp[j]=max(dp[j],dp[j-w]+x)
    print(dp[c])""",
[("3 5\n3 4 5\n2 3 4\n","7"),("1 2\n10\n3\n","0"),("4 7\n1 4 5 7\n1 3 4 5\n","9"),("3 0\n5 6 7\n1 2 3\n","0"),("5 10\n6 3 5 4 6\n2 2 6 5 4\n","15"),("2 5\n10 9\n5 5\n","10")], "Weights 2 and 3 exactly fill capacity 5.")

add(157, "Word break decision", "Medium", ["dynamic-programming","strings"],
"Line 1 is lowercase string s. Line 2 is m, followed by m lowercase dictionary words. Print YES iff s can be segmented.",
["0 <= len(s) <= 5,000", "0 <= m <= 10,000; dictionary words are nonempty lowercase strings.", "Total dictionary length is at most 200,000."],
["Store dictionary prefixes in a trie.", "Start a trie walk only from a reachable string position.", "Mark the endpoint whenever the trie reaches a complete word."], "O(D + n * L) time, O(D + n) auxiliary space, where D is total dictionary length and L is the longest word",
"""def solve():
    s=input().strip(); m=int(input()); root={}; longest=0
    for _ in range(m):
        word=input().strip(); longest=max(longest,len(word)); node=root
        for char in word: node=node.setdefault(char,{})
        node['']=True
    dp=[False]*(len(s)+1); dp[0]=True
    for i in range(len(s)):
        if not dp[i]: continue
        node=root
        for j in range(i,min(len(s),i+longest)):
            node=node.get(s[j])
            if node is None: break
            if '' in node: dp[j+1]=True
    print('YES' if dp[-1] else 'NO')""",
[("leetcode\n2\nleet\ncode\n","YES"),("catsandog\n5\ncats\ndog\nsand\nand\ncat\n","NO"),("\n0\n","YES"),("aaaaaaa\n2\naaaa\naaa\n","YES"),("applepenapple\n2\napple\npen\n","YES"),("aaaaab\n2\naaa\naa\n","NO")], "The words leet and code cover the string.")

add(158, "Equal subset partition", "Medium", ["dynamic-programming","sets"],
"Line 1 is n and line 2 contains nonnegative integers. Print YES iff they can be split into equal-sum subsets.",
["1 <= n <= 200", "0 <= value <= 10,000", "Total sum is at most 200,000."],
["An odd total fails immediately.", "Track reachable sums to half the total.", "Update downward to avoid reuse."], "O(n * sum) time, O(sum) auxiliary space",
"""def solve():
    n=int(input()); a=list(map(int,input().split())); total=sum(a)
    if total%2: print('NO'); return
    target=total//2; dp=[True]+[False]*target
    for x in a:
        for s in range(target,x-1,-1): dp[s]|=dp[s-x]
    print('YES' if dp[target] else 'NO')""",
[("4\n1 5 11 5\n","YES"),("4\n1 2 3 5\n","NO"),("1\n0\n","YES"),("3\n2 2 2\n","NO"),("5\n3 3 3 4 5\n","YES"),("6\n100 100 100 100 100 100\n","YES")], "The subset 1, 5, 5 equals the remaining 11.")

add(159, "Distinct permutations in lexicographic order", "Hard", ["backtracking","sorting"],
"Line 1 is n and line 2 has n integers. Print every distinct permutation, one per line, in lexicographic order.",
["1 <= n <= 6", "Values fit signed 32-bit integers.", "The complete output is capped below the local runner's 64 KiB limit."],
["Sort before backtracking.", "Skip a duplicate with an unused identical predecessor.", "Emit only complete paths."], "O(p * n) time, O(p * n) output space, and O(n) auxiliary stack space",
"""def solve():
    n=int(input()); a=sorted(map(int,input().split())); used=[False]*n; path=[]; out=[]
    def go():
        if len(path)==n: out.append(' '.join(map(str,path))); return
        for i,x in enumerate(a):
            if used[i] or (i and a[i]==a[i-1] and not used[i-1]): continue
            used[i]=True; path.append(x); go(); path.pop(); used[i]=False
    go(); print('\\n'.join(out))""",
[("3\n1 1 2\n","1 1 2\n1 2 1\n2 1 1"),("2\n2 1\n","1 2\n2 1"),("1\n5\n","5"),("3\n0 0 0\n","0 0 0"),("3\n-1 0 1\n","-1 0 1\n-1 1 0\n0 -1 1\n0 1 -1\n1 -1 0\n1 0 -1"),("4\n1 2 2 3\n","1 2 2 3\n1 2 3 2\n1 3 2 2\n2 1 2 3\n2 1 3 2\n2 2 1 3\n2 2 3 1\n2 3 1 2\n2 3 2 1\n3 1 2 2\n3 2 1 2\n3 2 2 1")], "The repeated 1 produces only three unique arrangements.")

add(160, "Palindrome partition count", "Hard", ["dynamic-programming","strings"],
"Line 1 is lowercase string s. Print how many ways it can be divided into nonempty palindromic substrings.",
["0 <= len(s) <= 500", "s contains lowercase English letters.", "The empty string has one empty partition."],
["Precompute palindromic substrings.", "A partition ending at i may follow any palindromic suffix.", "Fill short palindrome lengths first."], "O(n^2) time, O(n^2) auxiliary space",
"""def solve():
    s=input().strip(); n=len(s); pal=[[False]*n for _ in range(n)]; dp=[0]*(n+1); dp[0]=1
    for end in range(n):
        for start in range(end,-1,-1):
            if s[start]==s[end] and (end-start<2 or pal[start+1][end-1]): pal[start][end]=True; dp[end+1]+=dp[start]
    print(dp[n])""",
[("aab\n","2"),("aaa\n","4"),("\n","1"),("abc\n","1"),("abba\n","3"),("aaaa\n","8")], "aab has partitions a|a|b and aa|b.")

PYTHON_CURATED_141_160 = ITEMS
if len(PYTHON_CURATED_141_160) != 20:
    raise RuntimeError("expected exactly 20 exercises")
