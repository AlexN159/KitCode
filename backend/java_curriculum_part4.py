"""Curated Java 17 drills 121--140.  This module is deliberately data-only."""

from __future__ import annotations

S = """import java.io.*;\nimport java.util.*;\npublic class Main { public static void main(String[] args) throws Exception { } }\n"""


def P(b, h=""):
    return f"import java.io.*;\nimport java.util.*;\npublic class Main {{ public static void main(String[] args) throws Exception {{ Scanner in=new Scanner(new BufferedInputStream(System.in));{b} }}{h}}}\n"


def C(i, o):
    return {"input": i, "expected_output": o}


def D(n, t, d, topic, desc, con, hints, cx, sol, p, q):
    return {
        "id": f"java-curated-{n:03d}",
        "title": t,
        "language": "java",
        "difficulty": d,
        "topics": [topic],
        "curriculum_family": topic,
        "interview_frequency": "Common",
        "description": desc,
        "constraints": con,
        "hints": hints,
        "expected_complexity": cx,
        "starter_code": S,
        "solution": sol,
        "public_tests": p,
        "hidden_tests": q,
        "examples": [{"input": x["input"], "output": x["expected_output"]} for x in p],
    }


JAVA_CURRICULUM_PART4 = [
    D(
        121,
        "Articulation Point Count",
        "Hard",
        "graphs",
        "For an undirected graph, print how many vertices are articulation points: deleting one increases the number of connected components.",
        [
            "1 <= n <= 100000 and 0 <= m <= 200000.",
            "Vertices are 0-based; parallel edges and self-loops may occur.",
        ],
        [
            "Track discovery and low-link times.",
            "A non-root is critical when a child cannot reach an earlier ancestor.",
            "A DFS root needs at least two DFS children.",
        ],
        "O(n+m) time, O(n+m) auxiliary space",
        P(
            """int n=in.nextInt(),m=in.nextInt();ArrayList<int[]>[]g=new ArrayList[n];for(int i=0;i<n;i++)g[i]=new ArrayList<>();for(int i=0;i<m;i++){int a=in.nextInt(),b=in.nextInt();g[a].add(new int[]{b,i});g[b].add(new int[]{a,i});}int[]d=new int[n],low=new int[n],par=new int[n],pe=new int[n],it=new int[n],kids=new int[n],st=new int[n];Arrays.fill(par,-1);Arrays.fill(pe,-1);boolean[]cut=new boolean[n];int time=0;for(int root=0;root<n;root++){if(d[root]!=0)continue;int top=0;st[top++]=root;d[root]=low[root]=++time;while(top>0){int u=st[top-1];if(it[u]<g[u].size()){int[]e=g[u].get(it[u]++);int v=e[0];if(e[1]==pe[u])continue;if(d[v]==0){par[v]=u;pe[v]=e[1];kids[u]++;d[v]=low[v]=++time;st[top++]=v;}else low[u]=Math.min(low[u],d[v]);}else{top--;if(par[u]<0)cut[u]=kids[u]>1;else{int p=par[u];low[p]=Math.min(low[p],low[u]);if(par[p]>=0&&low[u]>=d[p])cut[p]=true;}}}}int ans=0;for(boolean x:cut)if(x)ans++;System.out.println(ans);"""
        ),
        [C("3 2\n0 1\n1 2\n", "1"), C("3 3\n0 1\n1 2\n2 0\n", "0")],
        [
            C("1 0\n", "0"),
            C("5 3\n0 1\n0 2\n0 3\n", "1"),
            C("4 1\n0 1\n", "0"),
            C("4 3\n0 1\n1 2\n1 3\n", "1"),
        ],
    ),
    D(
        122,
        "SCC Condensation Sources",
        "Hard",
        "graphs",
        "Given a directed graph, contract every strongly connected component. Print the number of components having no incoming edge from another component.",
        [
            "1 <= n <= 100000 and 0 <= m <= 200000.",
            "Vertices are 0-based; repeated edges are allowed.",
        ],
        [
            "Find SCC labels with two graph traversals.",
            "Reverse finishing order is useful.",
            "Count distinct component labels on cross-component edges.",
        ],
        "O(n+m) time, O(n+m) auxiliary space",
        P(
            """int n=in.nextInt(),m=in.nextInt();ArrayList<Integer>[]g=new ArrayList[n],r=new ArrayList[n];for(int i=0;i<n;i++){g[i]=new ArrayList<>();r[i]=new ArrayList<>();}for(int i=0;i<m;i++){int a=in.nextInt(),b=in.nextInt();g[a].add(b);r[b].add(a);}boolean[]vis=new boolean[n];int[]it=new int[n],st=new int[n],ord=new int[n];int count=0;for(int root=0;root<n;root++){if(vis[root])continue;int top=0;st[top++]=root;vis[root]=true;while(top>0){int u=st[top-1];if(it[u]<g[u].size()){int v=g[u].get(it[u]++);if(!vis[v]){vis[v]=true;st[top++]=v;}}else{top--;ord[count++]=u;}}}int[]co=new int[n];Arrays.fill(co,-1);int k=0;for(int z=n-1;z>=0;z--){int root=ord[z];if(co[root]>=0)continue;int top=0;st[top++]=root;co[root]=k;while(top>0){int u=st[--top];for(int v:r[u])if(co[v]<0){co[v]=k;st[top++]=v;}}k++;}boolean[]inEdge=new boolean[k];for(int u=0;u<n;u++)for(int v:g[u])if(co[u]!=co[v])inEdge[co[v]]=true;int ans=0;for(boolean x:inEdge)if(!x)ans++;System.out.println(ans);"""
        ),
        [C("3 2\n0 1\n1 2\n", "1"), C("3 2\n0 1\n2 1\n", "2")],
        [
            C("1 0\n", "1"),
            C("3 3\n0 1\n1 0\n1 2\n", "1"),
            C("4 4\n0 1\n1 0\n2 3\n3 2\n", "2"),
            C("3 3\n0 1\n1 2\n2 0\n", "1"),
        ],
    ),
    D(
        123,
        "Negative-Cycle-Affected Vertices",
        "Medium",
        "graphs",
        "For a weighted directed graph and source s, print the count of vertices whose shortest-path value is unbounded below because a reachable negative cycle can reach them.",
        [
            "1 <= n <= 5000 and 0 <= m <= 20000; weights fit int.",
            "Vertices are 0-based; only cycles reachable from s count.",
        ],
        [
            "Relax edges n-1 times.",
            "A further relaxation marks an affected seed.",
            "Propagate marks along outgoing edges.",
        ],
        "O(nm) time, O(n+m) auxiliary space",
        P(
            """int n=in.nextInt(),m=in.nextInt(),s=in.nextInt();int[]a=new int[m],b=new int[m],w=new int[m];ArrayList<Integer>[]g=new ArrayList[n];for(int i=0;i<n;i++)g[i]=new ArrayList<>();for(int i=0;i<m;i++){a[i]=in.nextInt();b[i]=in.nextInt();w[i]=in.nextInt();g[a[i]].add(b[i]);}long[]d=new long[n];Arrays.fill(d,Long.MAX_VALUE/4);d[s]=0;for(int z=1;z<n;z++)for(int i=0;i<m;i++)if(d[a[i]]<Long.MAX_VALUE/8&&d[b[i]]>d[a[i]]+w[i])d[b[i]]=d[a[i]]+w[i];boolean[]bad=new boolean[n];ArrayDeque<Integer>q=new ArrayDeque<>();for(int i=0;i<m;i++)if(d[a[i]]<Long.MAX_VALUE/8&&d[b[i]]>d[a[i]]+w[i]&&!bad[b[i]]){bad[b[i]]=true;q.add(b[i]);}while(!q.isEmpty())for(int v:g[q.remove()])if(!bad[v]){bad[v]=true;q.add(v);}int z=0;for(boolean x:bad)if(x)z++;System.out.println(z);"""
        ),
        [C("3 3 0\n0 1 1\n1 2 -2\n2 1 -2\n", "2"), C("3 2 0\n0 1 2\n1 2 3\n", "0")],
        [
            C("4 4 0\n0 1 1\n1 2 -3\n2 1 1\n2 3 2\n", "3"),
            C("3 1 0\n1 2 -1\n", "0"),
            C("1 1 0\n0 0 -1\n", "1"),
            C("4 3 0\n0 1 1\n2 3 -2\n3 2 -2\n", "0"),
        ],
    ),
    D(
        124,
        "All-Pairs Distance Queries",
        "Medium",
        "graphs",
        "Line 1 has n m q. Edges are directed weighted edges. For each query u v, print the shortest distance or INF when unreachable.",
        [
            "1 <= n <= 350, 0 <= m <= n(n-1), 1 <= q <= 1800; the query cap keeps worst-case output below the local 24,000-character ceiling.",
            "Weights are nonnegative ints; parallel edges may occur.",
        ],
        [
            "Initialize diagonal distances to zero.",
            "Keep the lightest parallel edge.",
            "Use each vertex as a permitted intermediate.",
        ],
        "O(n^3+q) time, O(n^2) auxiliary space",
        P(
            """int n=in.nextInt(),m=in.nextInt(),q=in.nextInt();long[][]d=new long[n][n];for(int i=0;i<n;i++){Arrays.fill(d[i],Long.MAX_VALUE/4);d[i][i]=0;}for(int i=0;i<m;i++){int a=in.nextInt(),b=in.nextInt(),w=in.nextInt();d[a][b]=Math.min(d[a][b],w);}for(int k=0;k<n;k++)for(int i=0;i<n;i++)for(int j=0;j<n;j++)if(d[i][k]+d[k][j]<d[i][j])d[i][j]=d[i][k]+d[k][j];while(q-->0){long x=d[in.nextInt()][in.nextInt()];System.out.println(x>=Long.MAX_VALUE/8?\"INF\":x);}"""
        ),
        [
            C("3 3 2\n0 1 4\n1 2 5\n0 2 20\n0 2\n2 0\n", "9\nINF"),
            C("2 0 2\n0 0\n1 1\n", "0\n0"),
        ],
        [
            C("3 2 1\n0 1 7\n0 1 3\n0 1\n", "3"),
            C("3 3 1\n0 1 1\n1 2 1\n2 0 1\n2 1\n", "2"),
            C("1 0 1\n0 0\n", "0"),
            C("4 2 2\n0 1 2\n2 3 4\n0 3\n2 3\n", "INF\n4"),
        ],
    ),
    D(
        125,
        "Euler Trail Start",
        "Easy",
        "graphs",
        "For an undirected multigraph, print the smallest valid starting vertex of an Euler trail, or NONE if no Euler trail exists. An isolated-only graph starts at 0.",
        [
            "1 <= n <= 200000 and 0 <= m <= 200000.",
            "Vertices are 0-based; loops contribute degree two.",
        ],
        [
            "Ignore isolated vertices when checking connectivity.",
            "There must be zero or two odd degrees.",
            "With two odd degrees, a trail must start at an odd vertex.",
        ],
        "O(n+m) time, O(n+m) auxiliary space",
        P(
            """int n=in.nextInt(),m=in.nextInt();ArrayList<Integer>[]g=new ArrayList[n];for(int i=0;i<n;i++)g[i]=new ArrayList<>();int[]deg=new int[n];for(int i=0;i<m;i++){int a=in.nextInt(),b=in.nextInt();g[a].add(b);g[b].add(a);deg[a]++;deg[b]++;}int first=0;while(first<n&&deg[first]==0)first++;if(first==n){System.out.println(0);return;}boolean[]v=new boolean[n];ArrayDeque<Integer>q=new ArrayDeque<>();q.add(first);v[first]=true;while(!q.isEmpty())for(int x:g[q.remove()])if(!v[x]){v[x]=true;q.add(x);}for(int i=0;i<n;i++)if(deg[i]>0&&!v[i]){System.out.println(\"NONE\");return;}int odd=0,start=n;for(int i=0;i<n;i++)if((deg[i]&1)==1){odd++;start=Math.min(start,i);}System.out.println(odd==0?first:odd==2?start:\"NONE\");"""
        ),
        [C("3 2\n0 1\n1 2\n", "0"), C("3 3\n0 1\n1 2\n2 0\n", "0")],
        [
            C("4 2\n0 1\n2 3\n", "NONE"),
            C("3 3\n0 1\n0 1\n1 2\n", "1"),
            C("2 0\n", "0"),
            C("3 4\n0 1\n0 1\n0 2\n0 2\n", "0"),
        ],
    ),
    D(
        126,
        "Tree Vertical Order",
        "Easy",
        "trees",
        "A binary tree is serialized as value left right rows, root 0. Print its values by increasing column; within a column use top-to-bottom then node index order.",
        [
            "0 <= n <= 1900; node values are signed 32-bit integers and children form a tree rooted at 0. This cap keeps worst-case output below the local 24,000-character ceiling.",
            "Child index -1 means absent.",
        ],
        [
            "Left decreases a column and right increases it.",
            "Record row and column while traversing.",
            "Sort by column, row, then index.",
        ],
        "O(n log n) time, O(n) auxiliary space",
        P(
            """int n=in.nextInt();int[]v=new int[n],l=new int[n],r=new int[n];for(int i=0;i<n;i++){v[i]=in.nextInt();l[i]=in.nextInt();r[i]=in.nextInt();}if(n==0){System.out.println();return;}ArrayList<int[]>a=new ArrayList<>();ArrayDeque<int[]>q=new ArrayDeque<>();q.add(new int[]{0,0,0});while(!q.isEmpty()){int[]x=q.remove();a.add(new int[]{x[1],x[2],x[0]});if(l[x[0]]>=0)q.add(new int[]{l[x[0]],x[1]-1,x[2]+1});if(r[x[0]]>=0)q.add(new int[]{r[x[0]],x[1]+1,x[2]+1});}a.sort((x,y)->x[0]!=y[0]?x[0]-y[0]:x[1]!=y[1]?x[1]-y[1]:x[2]-y[2]);for(int i=0;i<a.size();i++){if(i>0)System.out.print(\" \");System.out.print(v[a.get(i)[2]]);}System.out.println();"""
        ),
        [C("3\n1 1 2\n2 -1 -1\n3 -1 -1\n", "2 1 3"), C("0\n", "")],
        [
            C("1\n7 -1 -1\n", "7"),
            C("5\n1 1 2\n2 3 4\n3 -1 -1\n4 -1 -1\n5 -1 -1\n", "4 2 1 5 3"),
            C("4\n1 1 -1\n2 2 -1\n3 3 -1\n4 -1 -1\n", "4 3 2 1"),
            C("3\n1 -1 1\n2 2 -1\n3 -1 -1\n", "1 3 2"),
        ],
    ),
    D(
        127,
        "Tree Boundary Order",
        "Medium",
        "trees",
        "Print a binary tree boundary anticlockwise: root, left boundary excluding leaves, leaves left-to-right, then right boundary bottom-up excluding leaves. Print an empty line for no nodes.",
        [
            "0 <= n <= 1900; rows are signed-32-bit value, left, right and root is 0. This cap keeps worst-case output below the local 24,000-character ceiling.",
            "The input is an acyclic tree; -1 denotes absent child.",
        ],
        [
            "Do not duplicate leaves.",
            "Walk each side preferring its outer child.",
            "A DFS naturally lists leaves left-to-right.",
        ],
        "O(n) time, O(n) auxiliary space",
        P(
            """int n=in.nextInt();int[]v=new int[n],l=new int[n],r=new int[n];for(int i=0;i<n;i++){v[i]=in.nextInt();l[i]=in.nextInt();r[i]=in.nextInt();}if(n==0){System.out.println();return;}ArrayList<Integer>a=new ArrayList<>();a.add(0);int x=l[0];while(x>=0){if(l[x]>=0||r[x]>=0)a.add(x);x=l[x]>=0?l[x]:r[x];}ArrayDeque<Integer>st=new ArrayDeque<>();st.push(0);while(!st.isEmpty()){x=st.pop();if(l[x]<0&&r[x]<0){if(x!=0)a.add(x);}else{if(r[x]>=0)st.push(r[x]);if(l[x]>=0)st.push(l[x]);}}ArrayList<Integer>b=new ArrayList<>();x=r[0];while(x>=0){if(l[x]>=0||r[x]>=0)b.add(x);x=r[x]>=0?r[x]:l[x];}for(int i=b.size()-1;i>=0;i--)a.add(b.get(i));for(int i=0;i<a.size();i++){if(i>0)System.out.print(\" \");System.out.print(v[a.get(i)]);}System.out.println();"""
        ),
        [C("3\n1 1 2\n2 -1 -1\n3 -1 -1\n", "1 2 3"), C("0\n", "")],
        [
            C("1\n9 -1 -1\n", "9"),
            C("4\n1 1 -1\n2 2 -1\n3 3 -1\n4 -1 -1\n", "1 2 3 4"),
            C("4\n1 -1 1\n2 -1 2\n3 -1 3\n4 -1 -1\n", "1 4 3 2"),
            C("5\n1 1 2\n2 3 4\n3 -1 -1\n4 -1 -1\n5 -1 -1\n", "1 2 4 5 3"),
        ],
    ),
    D(
        128,
        "Maximum Positional Tree Width",
        "Medium",
        "trees",
        "For a binary tree, width of a level is last positional slot minus first plus one, where left/right children occupy 2p and 2p+1. Print the maximum width.",
        [
            "0 <= n <= 100000; rows are left right child indices.",
            "The tree is rooted at 0 and indices form an acyclic tree; its maximum root depth is at most 62, so every positional index fits signed long.",
        ],
        [
            "A queue can carry a node and its positional slot.",
            "Normalize positions at each level to avoid growth.",
            "Width includes null gaps between end nodes.",
        ],
        "O(n) time, O(n) auxiliary space",
        P(
            """int n=in.nextInt();int[]l=new int[n],r=new int[n];for(int i=0;i<n;i++){l[i]=in.nextInt();r[i]=in.nextInt();}if(n==0){System.out.println(0);return;}ArrayDeque<long[]>q=new ArrayDeque<>();q.add(new long[]{0,0});long ans=1;while(!q.isEmpty()){int z=q.size();long base=q.peek()[1],last=0;for(int i=0;i<z;i++){long[]x=q.remove();long p=x[1]-base;last=p;int u=(int)x[0];if(l[u]>=0)q.add(new long[]{l[u],2*p});if(r[u]>=0)q.add(new long[]{r[u],2*p+1});}ans=Math.max(ans,last+1);}System.out.println(ans);"""
        ),
        [C("3\n1 2\n-1 -1\n-1 -1\n", "2"), C("0\n", "0")],
        [
            C("1\n-1 -1\n", "1"),
            C("4\n1 -1\n-1 2\n3 -1\n-1 -1\n", "1"),
            C("5\n1 2\n3 -1\n-1 4\n-1 -1\n-1 -1\n", "4"),
            C("3\n-1 1\n-1 2\n-1 -1\n", "1"),
        ],
    ),
    D(
        129,
        "Subtree Sum Updates",
        "Medium",
        "trees",
        "A rooted tree has initial node values. Process Q operations: `U v x` assigns value x; `Q v` prints the sum of v's subtree.",
        [
            "1 <= n <= 100000 and 1 <= q <= 1100. Exactly one parent is -1 and all other parent links form one rooted tree; the query cap keeps worst-case output below the local 24,000-character ceiling.",
            "Values and sums fit signed long.",
        ],
        [
            "Flatten each subtree into a contiguous DFS interval.",
            "A point assignment changes one flattened position.",
            "Use a Fenwick tree for interval sums.",
        ],
        "O((n+q) log n) time, O(n) auxiliary space",
        P(
            """int n=in.nextInt(),q=in.nextInt();long[]val=new long[n];for(int i=0;i<n;i++)val[i]=in.nextLong();ArrayList<Integer>[]g=new ArrayList[n];for(int i=0;i<n;i++)g[i]=new ArrayList<>();int root=0;for(int i=0;i<n;i++){int p=in.nextInt();if(p<0)root=i;else g[p].add(i);}int[]tin=new int[n],tout=new int[n],ord=new int[n],it=new int[n];int[]st=new int[n];int top=0,t=0;st[top++]=root;while(top>0){int u=st[top-1];if(it[u]==0){tin[u]=t;ord[t++]=u;}if(it[u]<g[u].size())st[top++]=g[u].get(it[u]++);else{tout[u]=t-1;top--;}}long[]bit=new long[n+1];for(int i=0;i<n;i++)add(bit,tin[i]+1,val[i]);while(q-->0){String op=in.next();int v=in.nextInt();if(op.equals(\"U\")){long x=in.nextLong();add(bit,tin[v]+1,x-val[v]);val[v]=x;}else System.out.println(sum(bit,tout[v]+1)-sum(bit,tin[v]));}""",
            """static void add(long[]b,int i,long x){for(;i<b.length;i+=i&-i)b[i]+=x;}static long sum(long[]b,int i){long s=0;for(;i>0;i-=i&-i)s+=b[i];return s;}""",
        ),
        [
            C("3 3\n1 2 3\n-1 0 0\nQ 0\nU 1 5\nQ 0\n", "6\n9"),
            C("1 2\n7\n-1\nQ 0\nU 0 -2\n", "7"),
        ],
        [
            C("2 2\n1 2\n-1 0\nQ 1\nQ 0\n", "2\n3"),
            C("4 3\n1 1 1 1\n-1 0 0 1\nQ 1\nU 3 9\nQ 0\n", "2\n12"),
            C("3 1\n-1 0 1\n-1 0 1\nQ 1\n", "1"),
            C("2 3\n0 0\n-1 0\nU 0 2\nU 1 3\nQ 0\n", "5"),
        ],
    ),
    D(
        130,
        "Kth Ancestor Queries",
        "Medium",
        "trees",
        "Given parent pointers, answer q queries `v k` by printing the k-th ancestor of v, or -1 if it does not exist.",
        [
            "1 <= n <= 200000, 1 <= q <= 3000, and 0 <= k <= 10^18; the query cap keeps worst-case output below the local 24,000-character ceiling.",
            "The parent pointers form a rooted forest; parent is -1 or a valid index.",
        ],
        [
            "Precompute jumps of powers of two.",
            "For each set bit in k, take that jump.",
            "Keep -1 as an absorbing missing ancestor.",
        ],
        "O((n+q) log n) time, O(n log n) auxiliary space",
        P(
            """int n=in.nextInt(),q=in.nextInt(),L=61;int[][]up=new int[L][n];for(int i=0;i<n;i++)up[0][i]=in.nextInt();for(int z=1;z<L;z++)for(int i=0;i<n;i++)up[z][i]=up[z-1][i]<0?-1:up[z-1][up[z-1][i]];while(q-->0){int v=in.nextInt();long k=in.nextLong();for(int z=0;z<L&&v>=0;z++)if(((k>>z)&1)==1)v=up[z][v];System.out.println(v);}"""
        ),
        [C("3 2\n-1 0 1\n2 2\n2 3\n", "0\n-1"), C("1 2\n-1\n0 0\n0 1\n", "0\n-1")],
        [
            C("4 2\n-1 0 0 2\n3 1\n3 2\n", "2\n0"),
            C("3 1\n-1 0 1\n2 0\n", "2"),
            C("2 1\n-1 0\n1 100\n", "-1"),
            C("4 2\n-1 -1 0 1\n3 2\n2 1\n", "-1\n0"),
        ],
    ),
    D(
        131,
        "Range Minimum Updates",
        "Medium",
        "segment-trees",
        "An array receives `U i x` point assignments and `Q l r` inclusive range-minimum queries. Print each query answer.",
        [
            "1 <= n <= 100000, 1 <= q <= 1900, and 0 <= l <= r < n; the query cap keeps worst-case output below the local 24,000-character ceiling.",
            "All values fit signed 32-bit integers.",
        ],
        [
            "Build leaves at a power-of-two base.",
            "Update one leaf then repair ancestors.",
            "Fold the covered segments for a query.",
        ],
        "O((n+q) log n) time, O(n) auxiliary space",
        P(
            """int n=in.nextInt(),q=in.nextInt(),z=1;while(z<n)z<<=1;int[]t=new int[2*z];Arrays.fill(t,Integer.MAX_VALUE);for(int i=0;i<n;i++)t[z+i]=in.nextInt();for(int i=z-1;i>0;i--)t[i]=Math.min(t[2*i],t[2*i+1]);while(q-->0){String o=in.next();int a=in.nextInt(),b=in.nextInt();if(o.equals(\"U\")){int p=z+a;t[p]=b;for(p>>=1;p>0;p>>=1)t[p]=Math.min(t[2*p],t[2*p+1]);}else{int ans=Integer.MAX_VALUE;for(int l=z+a,r=z+b;l<=r;l>>=1,r>>=1){if((l&1)==1)ans=Math.min(ans,t[l++]);if((r&1)==0)ans=Math.min(ans,t[r--]);}System.out.println(ans);}}"""
        ),
        [
            C("3 3\n5 2 7\nQ 0 2\nU 1 9\nQ 0 2\n", "2\n5"),
            C("1 2\n4\nQ 0 0\nU 0 -1\n", "4"),
        ],
        [
            C("4 2\n3 3 3 3\nQ 1 2\nQ 0 3\n", "3\n3"),
            C("2 3\n9 1\nU 0 0\nQ 0 1\nQ 1 1\n", "0\n1"),
            C("5 1\n5 4 3 2 1\nQ 2 4\n", "1"),
            C("3 2\n-1 -2 -3\nQ 0 1\nQ 2 2\n", "-2\n-3"),
        ],
    ),
    D(
        132,
        "Static Range Minimum",
        "Medium",
        "sparse-tables",
        "Given an immutable array, answer inclusive minimum queries `l r`.",
        [
            "1 <= n <= 200000, 1 <= q <= 1900, and 0 <= l <= r < n; the query cap keeps worst-case output below the local 24,000-character ceiling.",
            "Values fit signed 32-bit integers.",
        ],
        [
            "Store minima for power-of-two blocks.",
            "Any interval is covered by two overlapping blocks.",
            "Compute floor log lengths once.",
        ],
        "O(n log n+q) time, O(n log n) auxiliary space",
        P(
            """int n=in.nextInt(),q=in.nextInt(),L=1;while((1<<L)<=n)L++;int[][]s=new int[L][n];for(int i=0;i<n;i++)s[0][i]=in.nextInt();for(int z=1;z<L;z++)for(int i=0;i+(1<<z)<=n;i++)s[z][i]=Math.min(s[z-1][i],s[z-1][i+(1<<(z-1))]);while(q-->0){int l=in.nextInt(),r=in.nextInt(),z=31-Integer.numberOfLeadingZeros(r-l+1);System.out.println(Math.min(s[z][l],s[z][r-(1<<z)+1]));}"""
        ),
        [C("4 2\n5 1 4 2\n0 2\n2 3\n", "1\n2"), C("1 1\n-3\n0 0\n", "-3")],
        [
            C("3 2\n2 2 2\n0 1\n1 2\n", "2\n2"),
            C("5 1\n9 8 7 6 5\n0 4\n", "5"),
            C("5 2\n1 3 -1 4 2\n0 0\n1 3\n", "1\n-1"),
            C("2 1\n0 -2\n0 1\n", "-2"),
        ],
    ),
    D(
        133,
        "Matrix Chain Minimum Cost",
        "Medium",
        "dynamic-programming",
        "Line 1 is n matrix count; line 2 gives n+1 dimensions. Print the least scalar multiplications to multiply matrices in order.",
        [
            "1 <= n <= 500; the next line contains exactly n+1 dimensions, each from 1 through 200000.",
            "These bounds keep every candidate multiplication-chain cost within signed long.",
        ],
        [
            "The last multiplication chooses a split.",
            "Try every split of each interval.",
            "Build by increasing chain length.",
        ],
        "O(n^3) time, O(n^2) auxiliary space",
        P(
            """int n=in.nextInt();long[]p=new long[n+1];for(int i=0;i<=n;i++)p[i]=in.nextLong();long[][]d=new long[n][n];for(int len=2;len<=n;len++)for(int i=0;i+len<=n;i++){int j=i+len-1;d[i][j]=Long.MAX_VALUE;for(int k=i;k<j;k++)d[i][j]=Math.min(d[i][j],d[i][k]+d[k+1][j]+p[i]*p[k+1]*p[j+1]);}System.out.println(d[0][n-1]);"""
        ),
        [C("3\n10 30 5 60\n", "4500"), C("1\n7 9\n", "0")],
        [
            C("2\n10 20 30\n", "6000"),
            C("4\n40 20 30 10 30\n", "26000"),
            C("3\n5 4 6 2\n", "88"),
            C("2\n1 1 1\n", "1"),
        ],
    ),
    D(
        134,
        "Subset Sum Count",
        "Medium",
        "dynamic-programming",
        "Print the number of subsets whose values sum exactly target, modulo 1,000,000,007. Values are nonnegative.",
        [
            "0 <= n <= 2000 and 0 <= target <= 20000.",
            "The next line contains exactly n nonnegative 32-bit integers; each array position is a distinct choice, including repeated values.",
        ],
        [
            "dp[s] counts ways to reach s.",
            "Process sums downward so a value is used once.",
            "Zero doubles every existing count.",
        ],
        "O(n target) time, O(target) auxiliary space",
        P(
            """int n=in.nextInt(),T=in.nextInt(),M=1000000007;long[]d=new long[T+1];d[0]=1;for(int i=0;i<n;i++){int x=in.nextInt();for(int s=T;s>=x;s--)d[s]=(d[s]+d[s-x])%M;}System.out.println(d[T]);"""
        ),
        [C("3 3\n1 2 3\n", "2"), C("3 0\n0 0 1\n", "4")],
        [
            C("0 0\n", "1"),
            C("4 2\n1 1 1 1\n", "6"),
            C("3 7\n2 4 6\n", "0"),
            C("2 1\n0 1\n", "2"),
        ],
    ),
    D(
        135,
        "Weighted Edit Distance",
        "Medium",
        "dynamic-programming",
        "Line 1 is string a, line 2 is string b, and line 3 gives positive insertion, deletion, and replacement costs. Print the minimum cost to convert a to b.",
        [
            "Each of the first two lines contains only lowercase ASCII and may be empty; each length is at most 2000.",
            "All three costs are integers from 1 to 100000.",
        ],
        [
            "One prefix row depends only on the previous row.",
            "Equal characters may be kept for zero cost.",
            "Otherwise consider insert, delete, and replace.",
        ],
        "O(|a||b|) time, O(|b|) auxiliary space",
        P(
            """String a=in.nextLine(),b=in.nextLine();long ci=in.nextLong(),cd=in.nextLong(),cr=in.nextLong();long[]d=new long[b.length()+1];for(int j=0;j<=b.length();j++)d[j]=j*ci;for(int i=1;i<=a.length();i++){long prev=d[0];d[0]=i*cd;for(int j=1;j<=b.length();j++){long old=d[j];d[j]=a.charAt(i-1)==b.charAt(j-1)?prev:Math.min(prev+cr,Math.min(d[j]+cd,d[j-1]+ci));prev=old;}}System.out.println(d[b.length()]);"""
        ),
        [C("cat\ncut\n1 1 1\n", "1"), C("a\nb\n5 2 10\n", "7")],
        [
            C("abc\nabc\n2 3 4\n", "0"),
            C("ab\nc\n1 1 5\n", "3"),
            C("abc\nx\n10 1 100\n", "13"),
            C("\nbb\n2 3 1\n", "4"),
        ],
    ),
    D(
        136,
        "Closest Subset Sum",
        "Hard",
        "meet-in-the-middle",
        "Given up to 40 signed values and target T, print the smallest absolute difference between T and any subset sum.",
        [
            "0 <= n <= 40; every value and target is between -10^12 and 10^12 inclusive.",
            "Therefore every subset sum, complement, and absolute difference fits signed long.",
        ],
        [
            "Split the array in half.",
            "Enumerate every sum of each half.",
            "Sort one side and binary-search complements.",
        ],
        "O(2^(n/2) log 2^(n/2)) time, O(2^(n/2)) auxiliary space",
        P(
            """int n=in.nextInt();long T=in.nextLong();long[]a=new long[n];for(int i=0;i<n;i++)a[i]=in.nextLong();int k=n/2;long[]x=sums(a,0,k),y=sums(a,k,n);Arrays.sort(y);long ans=Math.abs(T);for(long u:x){long want=T-u;int z=Arrays.binarySearch(y,want);if(z<0)z=-z-1;for(int j=Math.max(0,z-1);j<=Math.min(y.length-1,z);j++)ans=Math.min(ans,Math.abs(want-y[j]));}System.out.println(ans);""",
            """static long[]sums(long[]a,int l,int r){long[]z=new long[1<<(r-l)];for(int m=0;m<z.length;m++)for(int i=0;i<r-l;i++)if((m&(1<<i))!=0)z[m]+=a[l+i];return z;}""",
        ),
        [C("3 6\n1 2 4\n", "0"), C("2 5\n1 1\n", "3")],
        [
            C("0 -7\n", "7"),
            C("4 0\n-3 1 2 9\n", "0"),
            C("3 -4\n-1 -2 5\n", "1"),
            C("4 100\n20 30 40 50\n", "0"),
        ],
    ),
    D(
        137,
        "Segmented Prime Count",
        "Medium",
        "number-theory",
        "Print how many primes lie in the inclusive interval [L,R].",
        ["0 <= L <= R <= 10^12 and R-L <= 2,000,000."],
        [
            "Sieve primes only up to sqrt(R).",
            "Mark their multiples in the requested interval.",
            "Remember that 0 and 1 are not prime.",
        ],
        "O((R-L+sqrt(R)) log log R) time, O(R-L+sqrt(R)) auxiliary space",
        P(
            """long L=in.nextLong(),R=in.nextLong();int z=(int)Math.sqrt(R);boolean[]p=new boolean[z+1];ArrayList<Integer>ps=new ArrayList<>();for(int i=2;i<=z;i++)if(!p[i]){ps.add(i);if((long)i*i<=z)for(int j=i*i;j<=z;j+=i)p[j]=true;}boolean[]bad=new boolean[(int)(R-L+1)];for(int x:ps){long st=Math.max((long)x*x,((L+x-1)/x)*x);for(long j=st;j<=R;j+=x)bad[(int)(j-L)]=true;}long ans=0;for(int i=0;i<bad.length;i++)if(!bad[i]&&L+i>=2)ans++;System.out.println(ans);"""
        ),
        [C("1 10\n", "4"), C("14 16\n", "0")],
        [C("2 2\n", "1"), C("0 1\n", "0"), C("17 19\n", "2"), C("100 110\n", "4")],
    ),
    D(
        138,
        "Convex Hull Perimeter",
        "Hard",
        "geometry",
        "Given distinct planar integer points, print the perimeter of their convex hull with exactly six decimal places. A one-point hull has perimeter 0; two points return twice their distance.",
        [
            "1 <= n <= 100000; each coordinate is between -10^9 and 10^9 inclusive, keeping every long cross product exact.",
            "All input points are distinct.",
        ],
        [
            "Sort points lexicographically.",
            "Discard clockwise and collinear turns while building each chain.",
            "Join lower and upper chains without duplicate endpoints.",
        ],
        "O(n log n) time, O(n) auxiliary space",
        P(
            """int n=in.nextInt();long[][]a=new long[n][2];for(int i=0;i<n;i++){a[i][0]=in.nextLong();a[i][1]=in.nextLong();}Arrays.sort(a,(x,y)->x[0]==y[0]?Long.compare(x[1],y[1]):Long.compare(x[0],y[0]));ArrayList<long[]>h=new ArrayList<>();for(long[]p:a){while(h.size()>1&&cross(h.get(h.size()-2),h.get(h.size()-1),p)<=0)h.remove(h.size()-1);h.add(p);}int low=h.size();for(int i=n-2;i>=0;i--){long[]p=a[i];while(h.size()>low&&cross(h.get(h.size()-2),h.get(h.size()-1),p)<=0)h.remove(h.size()-1);h.add(p);}if(n>1)h.remove(h.size()-1);double ans=0;for(int i=0;i<h.size();i++){long[]u=h.get(i),v=h.get((i+1)%h.size());ans+=Math.hypot(u[0]-v[0],u[1]-v[1]);}System.out.printf(Locale.US,\"%.6f%n\",ans);""",
            """static long cross(long[]a,long[]b,long[]c){return(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]);}""",
        ),
        [C("3\n0 0\n1 0\n0 1\n", "3.414214"), C("1\n2 3\n", "0.000000")],
        [
            C("2\n0 0\n3 4\n", "10.000000"),
            C("4\n0 0\n1 0\n1 1\n0 1\n", "4.000000"),
            C("3\n0 0\n2 0\n1 0\n", "4.000000"),
            C("5\n0 0\n2 0\n2 2\n0 2\n1 1\n", "8.000000"),
        ],
    ),
    D(
        139,
        "Closest Pair Squared Distance",
        "Hard",
        "geometry",
        "Given n distinct points, print the squared Euclidean distance of the closest pair.",
        [
            "2 <= n <= 5000; each coordinate is between -10^9 and 10^9 inclusive.",
            "Thus each squared distance is at most 8*10^18 and fits signed long.",
        ],
        [
            "Compare each pair while tracking the best distance.",
            "Use long for coordinate differences and squaring.",
            "The stated bound makes the quadratic scan practical.",
        ],
        "O(n^2) time, O(1) auxiliary space besides input",
        P(
            """int n=in.nextInt();long[][]a=new long[n][2];for(int i=0;i<n;i++){a[i][0]=in.nextLong();a[i][1]=in.nextLong();}long best=Long.MAX_VALUE;for(int i=0;i<n;i++)for(int j=i+1;j<n;j++){long dx=a[i][0]-a[j][0],dy=a[i][1]-a[j][1];best=Math.min(best,dx*dx+dy*dy);}System.out.println(best);"""
        ),
        [C("3\n0 0\n3 4\n1 1\n", "2"), C("2\n0 0\n5 0\n", "25")],
        [
            C("3\n-1 -1\n-1 0\n9 9\n", "1"),
            C("4\n0 0\n10 10\n3 4\n4 3\n", "2"),
            C("2\n-100000 0\n100000 0\n", "40000000000"),
            C("5\n0 0\n2 0\n4 0\n6 0\n8 0\n", "4"),
        ],
    ),
    D(
        140,
        "Minimum Interval Stabbing Points",
        "Easy",
        "greedy",
        "Given closed intervals, print the minimum number of integer points that hit every interval.",
        [
            "0 <= n <= 200000; endpoints are signed 32-bit and l <= r.",
            "A point at an interval endpoint counts as inside.",
        ],
        [
            "Sort by increasing right endpoint.",
            "When an interval is uncovered, choose its right endpoint.",
            "That choice reaches as far right as possible.",
        ],
        "O(n log n) time, O(n) auxiliary space",
        P(
            """int n=in.nextInt();int[][]a=new int[n][2];for(int i=0;i<n;i++){a[i][0]=in.nextInt();a[i][1]=in.nextInt();}Arrays.sort(a,(x,y)->Integer.compare(x[1],y[1]));int ans=0,p=0;boolean have=false;for(int[]x:a)if(!have||p<x[0]){p=x[1];have=true;ans++;}System.out.println(ans);"""
        ),
        [C("3\n1 3\n2 5\n3 6\n", "1"), C("3\n1 2\n3 4\n5 6\n", "3")],
        [
            C("0\n", "0"),
            C("2\n1 1\n1 1\n", "1"),
            C("4\n-3 -1\n-2 0\n0 2\n2 2\n", "2"),
            C("4\n1 10\n2 3\n4 5\n6 7\n", "3"),
        ],
    ),
]
