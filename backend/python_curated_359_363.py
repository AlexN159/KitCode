"""Five advanced, data-only Python drills: graphs, trees, persistent data structures, and geometry."""
from __future__ import annotations

STARTER = "import sys\n\ndef solve() -> None:\n    pass\n\nif __name__ == '__main__':\n    solve()\n"
ITEMS = []


def add(num, title, topics, description, constraints, hints, complexity, body, cases, explanation):
    records = [{"input": source, "expected_output": result} for source, result in cases]
    ITEMS.append({"id": f"python-curated-{num:03d}", "language": "python", "title": title,
        "difficulty": "Hard", "topics": topics, "practice_frequency": "Common",
        "description": description, "constraints": constraints, "hints": hints,
        "expected_complexity": complexity, "starter_code": STARTER,
        "solution": "import sys\n" + body.strip() + "\n\nif __name__ == '__main__':\n    solve()\n",
        "examples": [{"input": records[0]["input"], "output": records[0]["expected_output"], "explanation": explanation}],
        "public_tests": records[:2], "hidden_tests": records[2:]})


add(359, "Kirchhoff spanning-tree count", ["graphs", "linear-algebra", "matrix-tree-theorem"],
"Line 1 contains n m. The next m lines contain an undirected edge u v; parallel edges are separate choices. Vertices are 0 through n-1. Print the number of spanning trees modulo 1,000,000,007. A graph with one vertex has one spanning tree.",
["1 <= n <= 150 and 0 <= m <= 20,000", "0 <= u,v < n and u != v; parallel edges are allowed", "The answer is computed modulo 1,000,000,007"],
["Build the Laplacian: add one to both endpoint diagonals and subtract one on each off-diagonal.", "Delete one row and one column to form a cofactor.", "Take that determinant with modular Gaussian elimination."],
"O(n^3 + m) time and O(n^2) space",
"""def solve():
    MOD=1_000_000_007
    n,m=map(int,input().split())
    if n==1:
        print(1); return
    a=[[0]*(n-1) for _ in range(n-1)]
    for _ in range(m):
        u,v=map(int,input().split())
        if u<n-1: a[u][u]+=1
        if v<n-1: a[v][v]+=1
        if u<n-1 and v<n-1: a[u][v]-=1; a[v][u]-=1
    ans=1
    for col in range(n-1):
        pivot=next((row for row in range(col,n-1) if a[row][col]%MOD),None)
        if pivot is None:
            print(0); return
        if pivot!=col: a[col],a[pivot]=a[pivot],a[col]; ans=-ans
        value=a[col][col]%MOD; ans=ans*value%MOD; inv=pow(value,MOD-2,MOD)
        for row in range(col+1,n-1):
            factor=a[row][col]%MOD*inv%MOD
            if factor:
                for j in range(col,n-1): a[row][j]=(a[row][j]-factor*a[col][j])%MOD
    print(ans%MOD)""",
[("3 3\n0 1\n1 2\n0 2\n","3"),("2 2\n0 1\n0 1\n","2"),("1 0\n","1"),("3 2\n0 1\n1 2\n","1"),("4 3\n0 1\n1 2\n2 3\n","1"),("3 1\n0 1\n","0")],
"A triangle loses any one of its three edges and remains a spanning tree.")

add(360, "Heavy-light online tree path sums", ["trees", "heavy-light-decomposition", "fenwick-tree"],
"Line 1 contains n. Line 2 contains n initial vertex values. The next n-1 lines contain undirected tree edges u v. Line n+2 contains q. Each of the next q lines is SET v x, which replaces vertex v's value, or SUM u v, which prints the inclusive sum on the unique u-to-v path. Vertices are 0 through n-1.",
["1 <= n,q <= 500 and the n-1 edges form one tree", "Initial values and SET values are signed 32-bit integers", "At most 500 commands are SUM; the complete input is at most 12,000 characters"],
["Root the tree and find each node's heavy child.", "Put every heavy path in one contiguous base-array interval.", "Use a Fenwick tree for point updates and path segments."],
"O((n + q) log n) time and O(n) space",
"""def solve():
    n=int(input()); value=list(map(int,input().split())); graph=[[] for _ in range(n)]
    for _ in range(n-1):
        a,b=map(int,input().split()); graph[a].append(b); graph[b].append(a)
    parent=[-1]*n; depth=[0]*n; order=[0]
    for v in order:
        for w in graph[v]:
            if w!=parent[v]: parent[w]=v; depth[w]=depth[v]+1; order.append(w)
    size=[1]*n; heavy=[-1]*n
    for v in reversed(order):
        best=0
        for w in graph[v]:
            if parent[w]==v:
                size[v]+=size[w]
                if size[w]>best: best=size[w]; heavy[v]=w
    head=[0]*n; pos=[0]*n; base=[]; stack=[(0,0)]
    while stack:
        start,h=stack.pop(); v=start
        while v!=-1:
            head[v]=h; pos[v]=len(base); base.append(value[v])
            for w in graph[v]:
                if parent[w]==v and w!=heavy[v]: stack.append((w,w))
            v=heavy[v]
    bit=[0]*(n+1)
    def add(i,delta):
        i+=1
        while i<=n: bit[i]+=delta; i+=i&-i
    def prefix(i):
        total=0
        while i: total+=bit[i]; i-=i&-i
        return total
    def segment(left,right): return prefix(right+1)-prefix(left)
    for i,x in enumerate(base): add(i,x)
    for _ in range(int(input())):
        command=input().split()
        if command[0]=='SET':
            v,x=int(command[1]),int(command[2]); add(pos[v],x-value[v]); value[v]=x
        else:
            u,v=map(int,command[1:]); answer=0
            while head[u]!=head[v]:
                if depth[head[u]]<depth[head[v]]: u,v=v,u
                answer+=segment(pos[head[u]],pos[u]); u=parent[head[u]]
            if depth[u]>depth[v]: u,v=v,u
            print(answer+segment(pos[u],pos[v]))""",
[("5\n1 2 3 4 5\n0 1\n0 2\n1 3\n1 4\n4\nSUM 3 2\nSET 1 10\nSUM 3 2\nSUM 4 3\n","10\n18\n19"),("1\n7\n3\nSUM 0 0\nSET 0 -2\nSUM 0 0\n","7\n-2"),("3\n1 2 3\n0 1\n1 2\n2\nSUM 0 2\nSUM 1 1\n","6\n2"),("4\n0 0 0 0\n0 1\n0 2\n0 3\n3\nSET 2 5\nSUM 1 3\nSUM 2 3\n","0\n5"),("2\n-4 9\n0 1\n3\nSUM 0 1\nSET 1 -1\nSUM 0 1\n","5\n-5"),("4\n1 1 1 1\n0 1\n1 2\n2 3\n2\nSET 2 8\nSUM 0 3\n","11")],
"The path 3-1-0-2 initially sums to ten.")

add(361, "Persistent subarray kth smallest", ["persistent-segment-tree", "range-queries", "coordinate-compression"],
"Line 1 contains n q. Line 2 contains n integers. Each of the next q lines contains l r k, using zero-based inclusive l and r. Print the kth smallest value in a[l..r] for each query; k is one-based.",
["1 <= n,q <= 700", "Array values are signed 32-bit integers", "0 <= l <= r < n and 1 <= k <= r-l+1; the complete input is at most 12,000 characters"],
["Coordinate-compress the values.", "Make one persistent root per prefix.", "Subtract the l root from the r+1 root while descending for k."],
"O((n + q) log n) time and O(n log n) space",
"""def solve():
    n,q=map(int,input().split()); a=list(map(int,input().split())); values=sorted(set(a)); rank={x:i for i,x in enumerate(values)}; left=[0]; right=[0]; count=[0]
    def update(old,lo,hi,index):
        node=len(count); left.append(left[old]); right.append(right[old]); count.append(count[old]+1)
        if lo<hi:
            mid=(lo+hi)//2
            if index<=mid: left[node]=update(left[old],lo,mid,index)
            else: right[node]=update(right[old],mid+1,hi,index)
        return node
    roots=[0]
    for x in a: roots.append(update(roots[-1],0,len(values)-1,rank[x]))
    def kth(before,after,lo,hi,k):
        if lo==hi: return lo
        mid=(lo+hi)//2; in_left=count[left[after]]-count[left[before]]
        if k<=in_left: return kth(left[before],left[after],lo,mid,k)
        return kth(right[before],right[after],mid+1,hi,k-in_left)
    for _ in range(q):
        l,r,k=map(int,input().split()); print(values[kth(roots[l],roots[r+1],0,len(values)-1,k)])""",
[("5 3\n5 1 4 2 3\n0 4 3\n1 3 2\n2 2 1\n","3\n2\n4"),("4 2\n2 2 2 2\n0 3 1\n1 2 2\n","2\n2"),("1 2\n-7\n0 0 1\n0 0 1\n","-7\n-7"),("5 2\n-1 9 0 -1 5\n0 3 2\n1 4 4\n","-1\n9"),("6 3\n6 5 4 3 2 1\n0 5 1\n0 5 6\n2 4 2\n","1\n6\n3"),("3 2\n10 -10 0\n0 1 2\n1 2 1\n","10\n-10")],
"The third smallest value in the complete first array is three.")

add(362, "Li Chao online minimum lines", ["li-chao-tree", "dynamic-programming", "geometry"],
"Line 1 contains q. Each following command is ADD m b, adding the line y = m*x + b, or QUERY x, which prints the minimum y among all added lines at x. Every QUERY follows at least one ADD. All queried x values are in the fixed inclusive range -1,000,000 through 1,000,000.",
["1 <= q <= 1,000", "-1,000,000 <= x <= 1,000,000 and m,b are signed 32-bit integers", "At most 1,000 commands are QUERY; the complete input is at most 12,000 characters"],
["Each node stores the currently best line around its midpoint.", "Swap lines when the new one is better at the midpoint.", "Recurse only into the side where the displaced line can still win."],
"O(q log X) time and O(q log X) worst-case space, where X = 2,000,001",
"""def solve():
    LO=-1_000_000; HI=1_000_000; lines=[None]; left=[0]; right=[0]
    def value(line,x): return line[0]*x+line[1]
    def insert(node,line,lo,hi):
        if not lines[node]: lines[node]=line; return
        mid=(lo+hi)//2; current=lines[node]
        if value(line,mid)<value(current,mid): lines[node],line=line,current
        if lo==hi: return
        if value(line,lo)<value(lines[node],lo):
            if not left[node]: left[node]=len(lines); lines.append(None); left.append(0); right.append(0)
            insert(left[node],line,lo,mid)
        elif value(line,hi)<value(lines[node],hi):
            if not right[node]: right[node]=len(lines); lines.append(None); left.append(0); right.append(0)
            insert(right[node],line,mid+1,hi)
    def query(node,x,lo,hi):
        answer=value(lines[node],x)
        if lo==hi: return answer
        mid=(lo+hi)//2
        child=left[node] if x<=mid else right[node]
        return min(answer,query(child,x,lo,mid) if child and x<=mid else query(child,x,mid+1,hi) if child else answer)
    for _ in range(int(input())):
        command=input().split()
        if command[0]=='ADD': insert(0,(int(command[1]),int(command[2])),LO,HI)
        else: print(query(0,int(command[1]),LO,HI))""",
[("5\nADD 1 0\nQUERY 3\nADD -1 10\nQUERY 3\nQUERY 10\n","3\n3\n0"),("4\nADD 0 5\nQUERY -1000000\nADD 2 -1\nQUERY -2\n","5\n-5"),("3\nADD 3 4\nQUERY 0\nQUERY 1\n","4\n7"),("6\nADD 1 1\nADD -1 1\nQUERY -5\nQUERY 0\nQUERY 5\nQUERY 1000000\n","-4\n1\n-4\n-999999"),("5\nADD 0 0\nADD 0 -3\nQUERY 7\nADD 2 -100\nQUERY 50\n","-3\n-3"),("4\nADD -2 4\nQUERY -3\nADD 1 -10\nQUERY -3\n","10\n-13")],
"At x=3, both y=x and y=-x+10 evaluate to three.")

add(363, "Rectangle union area", ["computational-geometry", "sweep-line", "segment-tree"],
"Line 1 contains n. Each of the next n lines contains x1 y1 x2 y2 for one axis-aligned rectangle with x1 < x2 and y1 < y2. Rectangles may overlap or touch. Print the area covered by at least one rectangle.",
["1 <= n <= 50,000", "All coordinates are signed 32-bit integers", "The union area fits in a signed 64-bit integer"],
["Sweep from left to right over rectangle sides.", "Coordinate-compress y endpoints.", "A segment tree stores covered y length and a cover count for each interval."],
"O(n log n) time and O(n) space",
"""def solve():
    n=int(input()); events=[]; ys=[]
    for _ in range(n):
        x1,y1,x2,y2=map(int,input().split()); events.append((x1,1,y1,y2)); events.append((x2,-1,y1,y2)); ys.extend((y1,y2))
    ys=sorted(set(ys)); index={y:i for i,y in enumerate(ys)}; size=len(ys)-1; cover=[0]*(size*4); length=[0]*(size*4)
    def update(node,lo,hi,left,right,delta):
        if left<=lo and hi<=right: cover[node]+=delta
        else:
            mid=(lo+hi)//2
            if left<=mid: update(node*2,lo,mid,left,right,delta)
            if right>mid: update(node*2+1,mid+1,hi,left,right,delta)
        if cover[node]: length[node]=ys[hi+1]-ys[lo]
        elif lo==hi: length[node]=0
        else: length[node]=length[node*2]+length[node*2+1]
    events.sort(); area=0; previous=events[0][0]; i=0
    while i<len(events):
        x=events[i][0]; area+=(x-previous)*length[1]
        while i<len(events) and events[i][0]==x:
            _,delta,y1,y2=events[i]; update(1,0,size-1,index[y1],index[y2]-1,delta); i+=1
        previous=x
    print(area)""",
[("2\n0 0 2 2\n1 1 3 3\n","7"),("1\n-1 -2 2 3\n","15"),("2\n0 0 1 1\n1 0 2 1\n","2"),("3\n0 0 4 4\n1 1 2 2\n2 2 3 3\n","16"),("2\n-2 -2 0 0\n0 0 2 2\n","8"),("3\n0 0 3 1\n1 -1 2 2\n4 0 5 5\n","10")],
"The two 2-by-2 squares overlap in one unit square, so 4 + 4 - 1 = 7.")

PYTHON_CURATED_359_363 = ITEMS
