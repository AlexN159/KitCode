"""Final curated Java 17 core drills 141--150.

Each record is immutable data at import time: fixtures are literal, and the
reference programs are standalone ``public class Main`` submissions.
"""
from __future__ import annotations

STARTER = '''import java.io.*;\nimport java.util.*;\npublic class Main { public static void main(String[] args) throws Exception { } }\n'''


def P(body: str, helpers: str = "") -> str:
    return f"import java.io.*;\nimport java.util.*;\npublic class Main {{ public static void main(String[] args) throws Exception {{ Scanner in=new Scanner(new BufferedInputStream(System.in));{body} }}{helpers}}}\n"


def C(input_text: str, expected_output: str) -> dict[str, str]:
    return {"input": input_text, "expected_output": expected_output}


def D(n: int, title: str, difficulty: str, topic: str, description: str,
      constraints: list[str], hints: list[str], complexity: str, solution: str,
      public: list[dict[str, str]], hidden: list[dict[str, str]]) -> dict:
    return {"id": f"java-curated-{n:03d}", "title": title, "language": "java",
            "difficulty": difficulty, "topics": [topic], "curriculum_family": topic,
            "interview_frequency": "Common", "description": description,
            "constraints": constraints, "hints": hints, "expected_complexity": complexity,
            "starter_code": STARTER, "solution": solution, "public_tests": public,
            "hidden_tests": hidden,
            "examples": [{"input": x["input"], "output": x["expected_output"]} for x in public]}


JAVA_CURRICULUM_PART5 = [
D(141, "Three Word Autocomplete", "Medium", "tries",
  "Read n distinct lowercase dictionary words then a lowercase prefix. Print the first at most three matching words in lexicographic order, separated by spaces, or NONE.",
  ["0 <= n <= 100,000; total dictionary characters are at most 500,000.", "Every word and the nonempty prefix contain lowercase a-z only; total printed output is at most 24,000 characters."],
  ["Sort the words so candidates arrive in lexicographic order.", "A trie shares common prefixes and each node needs only its first three candidates.", "Walk the prefix, then print that node's saved words."],
  "O(D log n + prefix length + output length) time and O(D) auxiliary space, where D is total dictionary length",
  P("""int n=in.nextInt(),chars=0;String[] words=new String[n];for(int i=0;i<n;i++){words[i]=in.next();chars+=words[i].length();}Arrays.sort(words);int[]nx=new int[(chars+1)*26];String[]one=new String[chars+1],two=new String[chars+1],three=new String[chars+1];int nodes=1;for(String w:words){int u=0;for(int i=0;i<w.length();i++){int c=w.charAt(i)-'a',at=u*26+c;if(nx[at]==0)nx[at]=nodes++;u=nx[at];if(one[u]==null)one[u]=w;else if(two[u]==null)two[u]=w;else if(three[u]==null)three[u]=w;}}String p=in.next();int u=0;for(int i=0;i<p.length()&&u>=0;i++){int v=nx[u*26+p.charAt(i)-'a'];u=v==0?-1:v;}if(u<0||one[u]==null)System.out.println(\"NONE\");else System.out.println(one[u]+(two[u]==null?\"\":\" \"+two[u])+(three[u]==null?\"\":\" \"+three[u]));"""),
  [C("5\nape apple apply bat ball\nap\n", "ape apple apply"), C("3\ncat dog emu\nz\n", "NONE")],
  [C("0\na\n", "NONE"), C("4\na aa aaa aaaa\na\n", "a aa aaa"), C("3\nbe bee been\nbee\n", "bee been"), C("3\ncare car card\ncar\n", "car card care")]),

D(142, "Maximum Closed Interval Overlap", "Medium", "sweep-line",
  "Given closed integer intervals, print the largest number simultaneously covering a coordinate and the earliest coordinate achieving it.",
  ["0 <= n <= 200,000; endpoints are signed 32-bit integers and left <= right.", "For no intervals print 0 NONE."],
  ["Turn starts and ends into sweep events.", "At an equal coordinate, starts count before the maximum is measured and ends leave afterwards.", "Track the first coordinate that improves the answer."],
  "O(n log n) time, O(n) auxiliary space",
  P("""int n=in.nextInt();TreeMap<Long,Integer>e=new TreeMap<>();for(int i=0;i<n;i++){long l=in.nextLong(),r=in.nextLong();e.put(l,e.getOrDefault(l,0)+1);if(r<Long.MAX_VALUE)e.put(r+1,e.getOrDefault(r+1,0)-1);}int cur=0,best=0;long at=0;for(Map.Entry<Long,Integer>x:e.entrySet()){cur+=x.getValue();if(cur>best){best=cur;at=x.getKey();}}System.out.println(best==0?\"0 NONE\":best+\" \"+at);"""),
  [C("3\n1 3\n2 5\n3 4\n", "3 3"), C("0\n", "0 NONE")],
  [C("2\n1 1\n2 2\n", "1 1"), C("3\n-2 2\n-1 1\n0 0\n", "3 0"), C("2\n5 8\n5 5\n", "2 5"), C("4\n1 10\n2 3\n4 5\n6 7\n", "2 2")]),

D(143, "DAG Cheapest Route", "Medium", "graphs",
  "A directed graph has edges u v cost with u < v, so it is a DAG. Print the least cost from s to t, or INF if unreachable.",
  ["1 <= n <= 200,000 and 0 <= m <= 300,000; 0 <= s,t < n and every edge has 0 <= u < v < n.", "Costs are signed 32-bit integers, so every path cost fits signed long."],
  ["Vertex order is already topological.", "Relax outgoing edges only from reachable vertices.", "Use a large long sentinel for unreachable distances."],
  "O(n + m) time, O(n + m) auxiliary space",
  P("""int n=in.nextInt(),m=in.nextInt(),s=in.nextInt(),t=in.nextInt();ArrayList<long[]>[]g=new ArrayList[n];for(int i=0;i<n;i++)g[i]=new ArrayList<>();for(int i=0;i<m;i++){int a=in.nextInt(),b=in.nextInt();long w=in.nextLong();g[a].add(new long[]{b,w});}long[]d=new long[n];Arrays.fill(d,Long.MAX_VALUE/4);d[s]=0;for(int u=s;u<n;u++)if(d[u]<Long.MAX_VALUE/8)for(long[]x:g[u])d[(int)x[0]]=Math.min(d[(int)x[0]],d[u]+x[1]);System.out.println(d[t]>=Long.MAX_VALUE/8?\"INF\":d[t]);"""),
  [C("4 4 0 3\n0 1 5\n0 2 2\n1 3 1\n2 3 10\n", "6"), C("3 1 0 2\n0 1 4\n", "INF")],
  [C("1 0 0 0\n", "0"), C("3 3 0 2\n0 1 -2\n1 2 3\n0 2 5\n", "1"), C("5 5 0 4\n0 1 2\n0 2 1\n1 3 2\n2 3 5\n3 4 1\n", "5"), C("4 2 1 3\n1 2 7\n2 3 8\n", "15")]),

D(144, "KMP Pattern Positions", "Medium", "strings",
  "Read a text line then a nonempty pattern line. Print all zero-based starting positions of overlapping matches, or NONE.",
  ["Text length <= 200,000 and pattern length is 1 through 200,000.", "Both lines contain printable ASCII; there are at most 1,900 matches so output fits the runner cap."],
  ["Build the pattern's failure table.", "On a mismatch, reuse the longest proper matching prefix.", "After a match, continue from its failure link to allow overlap."],
  "O(text length + pattern length) time, O(pattern length) auxiliary space",
  P("""String s=in.nextLine(),p=in.nextLine();int[]f=new int[p.length()];for(int i=1,j=0;i<p.length();i++){while(j>0&&p.charAt(i)!=p.charAt(j))j=f[j-1];if(p.charAt(i)==p.charAt(j))j++;f[i]=j;}ArrayList<Integer>a=new ArrayList<>();for(int i=0,j=0;i<s.length();i++){while(j>0&&s.charAt(i)!=p.charAt(j))j=f[j-1];if(s.charAt(i)==p.charAt(j))j++;if(j==p.length()){a.add(i-j+1);j=f[j-1];}}if(a.isEmpty())System.out.println(\"NONE\");else{for(int i=0;i<a.size();i++){if(i>0)System.out.print(\" \");System.out.print(a.get(i));}System.out.println();}"""),
  [C("ababa\naba\n", "0 2"), C("hello\nll\n", "2")],
  [C("aaaa\naa\n", "0 1 2"), C("abc\nd\n", "NONE"), C("x\nx\n", "0"), C("mississippi\nissi\n", "1 4")]),

D(145, "4x4 Sudoku Completion", "Hard", "backtracking",
  "Read a 4 by 4 Sudoku using 0 for blank. Digits 1..4 must be unique in every row, column, and 2 by 2 box. Print the unique completed grid, rows separated by newlines.",
  ["The input has exactly 16 integers from 0 through 4.", "The puzzle is guaranteed to have exactly one solution."],
  ["Track used digits for each row, column, and box.", "Try a blank cell with its available values.", "Undo a trial when its suffix cannot be completed."],
  "O(4^16) worst-case time, O(16) auxiliary space",
  P("""int[][]a=new int[4][4];for(int i=0;i<4;i++)for(int j=0;j<4;j++)a[i][j]=in.nextInt();solve(a,0);for(int i=0;i<4;i++){for(int j=0;j<4;j++){if(j>0)System.out.print(\" \");System.out.print(a[i][j]);}System.out.println();}""", """static boolean solve(int[][]a,int z){if(z==16)return true;int r=z/4,c=z%4;if(a[r][c]!=0)return solve(a,z+1);for(int v=1;v<=4;v++)if(ok(a,r,c,v)){a[r][c]=v;if(solve(a,z+1))return true;a[r][c]=0;}return false;}static boolean ok(int[][]a,int r,int c,int v){for(int i=0;i<4;i++)if(a[r][i]==v||a[i][c]==v)return false;int R=r/2*2,C=c/2*2;for(int i=R;i<R+2;i++)for(int j=C;j<C+2;j++)if(a[i][j]==v)return false;return true;}"""),
  [C("1 0 0 4\n0 4 1 0\n0 1 4 0\n4 0 0 1\n", "1 2 3 4\n3 4 1 2\n2 1 4 3\n4 3 2 1"), C("0 2 3 4\n3 4 0 2\n2 1 4 0\n4 0 2 1\n", "1 2 3 4\n3 4 1 2\n2 1 4 3\n4 3 2 1")],
  [C("1 2 0 0\n0 4 1 2\n2 1 4 3\n4 3 2 1\n", "1 2 3 4\n3 4 1 2\n2 1 4 3\n4 3 2 1"), C("1 2 3 4\n3 4 1 2\n2 1 4 3\n4 3 2 1\n", "1 2 3 4\n3 4 1 2\n2 1 4 3\n4 3 2 1"), C("0 0 0 4\n3 0 0 2\n2 1 0 0\n0 3 2 0\n", "1 2 3 4\n3 4 1 2\n2 1 4 3\n4 3 2 1"), C("2 0 4 0\n0 3 0 1\n1 0 3 0\n0 4 0 2\n", "2 1 4 3\n4 3 2 1\n1 2 3 4\n3 4 1 2")]),

D(146, "Batch Tree Ancestors", "Medium", "offline-algorithms",
  "Read a rooted tree parent array and q node pairs. Print the lowest common ancestor for every pair using Tarjan's offline algorithm.",
  ["1 <= n <= 200,000 and 1 <= q <= 5,000; the parent array has exactly one -1 root and forms a tree.", "Nodes in every query are 0-based valid indices; the query cap keeps line-oriented output below the local runner limit."],
  ["Attach each query to both of its endpoints.", "When a completed subtree is unioned into its parent, its set ancestor becomes the parent.", "Answer a query when its other endpoint has been completed."],
  "O((n + q) alpha(n)) time, O(n + q) auxiliary space",
  P("""int n=in.nextInt(),q=in.nextInt();ArrayList<Integer>[]g=new ArrayList[n];for(int i=0;i<n;i++)g[i]=new ArrayList<>();int root=0;for(int i=0;i<n;i++){int p=in.nextInt();if(p<0)root=i;else g[p].add(i);}ArrayList<int[]>[]qs=new ArrayList[n];for(int i=0;i<n;i++)qs[i]=new ArrayList<>();for(int i=0;i<q;i++){int a=in.nextInt(),b=in.nextInt();qs[a].add(new int[]{b,i});qs[b].add(new int[]{a,i});}int[]ans=new int[q],par=new int[n],anc=new int[n],it=new int[n],st=new int[n];boolean[]done=new boolean[n];for(int i=0;i<n;i++){par[i]=i;anc[i]=i;}int top=0;st[top++]=root;while(top>0){int u=st[top-1];if(it[u]<g[u].size()){st[top++]=g[u].get(it[u]++);continue;}top--;done[u]=true;for(int[]x:qs[u])if(done[x[0]])ans[x[1]]=anc[find(par,x[0])];if(top>0){int p=st[top-1];par[find(par,u)]=find(par,p);anc[find(par,p)]=p;}}for(int x:ans)System.out.println(x);""", """static int find(int[]p,int x){while(p[x]!=x){p[x]=p[p[x]];x=p[x];}return x;}"""),
  [C("5 3\n-1 0 0 1 1\n3 4\n3 2\n1 4\n", "1\n0\n1"), C("1 2\n-1\n0 0\n0 0\n", "0\n0")],
  [C("4 2\n-1 0 1 2\n3 2\n1 3\n", "2\n1"), C("4 2\n-1 0 0 2\n1 3\n2 3\n", "0\n2"), C("6 3\n-1 0 0 1 1 2\n4 5\n4 2\n3 4\n", "0\n0\n1"), C("3 1\n-1 0 1\n2 2\n", "2")]),

D(147, "Rollback Connectivity Script", "Medium", "disjoint-set",
  "Maintain n isolated vertices. Commands are U a b (union), S (print a snapshot id), R id (restore that snapshot), and C (print connected-component count).",
  ["1 <= n,q <= 200,000; vertices are 0-based; at most 3,000 commands are S or C, keeping output bounded.", "Every restored id is a printed snapshot still on the current history: restoring an earlier id invalidates later snapshots and discarded branches.", "No path compression is used because every union change must be reversible."],
  ["Union by size limits parent-chain depth.", "Record a no-op marker when endpoints already share a set.", "A snapshot is the current change-stack size."],
  "O(q log n) worst-case time, O(n + q) auxiliary space",
  P("""int n=in.nextInt(),q=in.nextInt();int[]p=new int[n],sz=new int[n];for(int i=0;i<n;i++){p[i]=i;sz[i]=1;}ArrayList<int[]>h=new ArrayList<>();int comp=n;while(q-->0){String o=in.next();if(o.equals(\"U\")){int a=find(p,in.nextInt()),b=find(p,in.nextInt());if(a==b)h.add(new int[]{-1});else{if(sz[a]<sz[b]){int t=a;a=b;b=t;}h.add(new int[]{b,sz[a]});p[b]=a;sz[a]+=sz[b];comp--;}}else if(o.equals(\"S\"))System.out.println(h.size());else if(o.equals(\"C\"))System.out.println(comp);else{int k=in.nextInt();while(h.size()>k){int[]x=h.remove(h.size()-1);if(x[0]>=0){int b=x[0],a=p[b];sz[a]=x[1];p[b]=b;comp++;}}}}""", """static int find(int[]p,int x){while(p[x]!=x)x=p[x];return x;}"""),
  [C("3 7\nC\nU 0 1\nS\nU 1 2\nC\nR 1\nC\n", "3\n1\n1\n2"), C("2 5\nU 0 1\nS\nU 0 1\nR 1\nC\n", "1\n1")],
  [C("1 3\nS\nC\nR 0\n", "0\n1"), C("4 6\nU 0 1\nU 2 3\nS\nC\nR 0\nC\n", "2\n2\n4"), C("3 6\nS\nU 0 1\nS\nU 1 2\nR 1\nC\n", "0\n1\n2"), C("3 5\nU 0 1\nU 0 1\nS\nR 2\nC\n", "2\n2")]),

D(148, "Circular Stone Merge Cost", "Hard", "interval-dynamic-programming",
  "n positive piles sit in a circle. Repeatedly merge adjacent piles, paying their combined weight. Print the minimum total cost to make one pile.",
  ["1 <= n <= 300; each pile weight is 1 through 1,000,000,000 and the answer fits signed long.", "In the circular arrangement, the last remaining pile may be any original position."],
  ["Duplicate the array to linearize every possible cut.", "Use interval DP for each segment length up to n.", "The first split of an interval chooses its final merge."],
  "O(n^3) time, O(n^2) auxiliary space",
  P("""int n=in.nextInt(),N=2*n;long[]a=new long[N+1],s=new long[N+1];for(int i=1;i<=n;i++)a[i]=a[i+n]=in.nextLong();for(int i=1;i<=N;i++)s[i]=s[i-1]+a[i];long[][]d=new long[N+1][N+1];for(int len=2;len<=n;len++)for(int l=1;l+len-1<=N;l++){int r=l+len-1;d[l][r]=Long.MAX_VALUE/4;for(int k=l;k<r;k++)d[l][r]=Math.min(d[l][r],d[l][k]+d[k+1][r]+s[r]-s[l-1]);}long ans=Long.MAX_VALUE;for(int l=1;l<=n;l++)ans=Math.min(ans,d[l][l+n-1]);System.out.println(ans);"""),
  [C("3\n1 2 3\n", "9"), C("4\n4 1 1 4\n", "18")],
  [C("1\n7\n", "0"), C("2\n5 8\n", "13"), C("3\n1 1 1\n", "5"), C("4\n1 2 3 4\n", "19")]),

D(149, "Maximum Flow Network", "Hard", "max-flow",
  "Given a directed capacitated network and source s, sink t, print its maximum flow. Parallel edges are allowed.",
  ["2 <= n <= 500 and 0 <= m <= 10,000; vertices are 0-based and s != t.", "Capacities are nonnegative ints; total flow fits signed long."],
  ["Build reverse residual edges.", "A BFS finds one shortest augmenting level graph.", "Send blocking flow through that level graph before rebuilding it."],
  "O(V^2 E) worst-case time with Dinic, O(V + E) auxiliary space",
  P("""int n=in.nextInt(),m=in.nextInt(),s=in.nextInt(),t=in.nextInt();ArrayList<Edge>[]g=new ArrayList[n];for(int i=0;i<n;i++)g[i]=new ArrayList<>();for(int i=0;i<m;i++)add(g,in.nextInt(),in.nextInt(),in.nextLong());long flow=0;int[]lev=new int[n],it=new int[n];while(bfs(g,s,t,lev)){Arrays.fill(it,0);long x;while((x=dfs(g,s,t,Long.MAX_VALUE/4,lev,it))>0)flow+=x;}System.out.println(flow);""", """static class Edge{int v,rev;long c;Edge(int v,int r,long c){this.v=v;rev=r;this.c=c;}}static void add(ArrayList<Edge>[]g,int a,int b,long c){g[a].add(new Edge(b,g[b].size(),c));g[b].add(new Edge(a,g[a].size()-1,0));}static boolean bfs(ArrayList<Edge>[]g,int s,int t,int[]l){Arrays.fill(l,-1);ArrayDeque<Integer>q=new ArrayDeque<>();q.add(s);l[s]=0;while(!q.isEmpty()){int u=q.remove();for(Edge e:g[u])if(e.c>0&&l[e.v]<0){l[e.v]=l[u]+1;q.add(e.v);}}return l[t]>=0;}static long dfs(ArrayList<Edge>[]g,int u,int t,long f,int[]l,int[]it){if(u==t)return f;for(;it[u]<g[u].size();it[u]++){Edge e=g[u].get(it[u]);if(e.c>0&&l[e.v]==l[u]+1){long x=dfs(g,e.v,t,Math.min(f,e.c),l,it);if(x>0){e.c-=x;g[e.v].get(e.rev).c+=x;return x;}}}return 0;}"""),
  [C("4 5 0 3\n0 1 3\n0 2 2\n1 2 1\n1 3 2\n2 3 4\n", "5"), C("3 1 0 2\n0 1 7\n", "0")],
  [C("2 2 0 1\n0 1 3\n0 1 4\n", "7"), C("4 4 0 3\n0 1 10\n1 2 1\n2 3 10\n0 3 2\n", "3"), C("3 3 0 2\n0 1 5\n1 2 5\n0 2 1\n", "6"), C("2 0 0 1\n", "0")]),

D(150, "Multiple Pattern Match Counts", "Hard", "aho-corasick",
  "Read one lowercase text, then m lowercase nonempty patterns. Print, in input order, each pattern's number of occurrences in the text; overlaps count.",
  ["1 <= text length <= 200,000, 1 <= m <= 5,000, and total pattern length <= 200,000.", "Patterns contain a-z only; each count fits signed int; the pattern-count cap keeps output below the local runner limit."],
  ["Trie all patterns and add failure links with BFS.", "Every text character advances through failure links as needed.", "Accumulate visits then propagate them backward through failure links."],
  "O(text length + total pattern length + alphabet * node count) time, O(alphabet * node count) auxiliary space",
  P("""String s=in.next();int m=in.nextInt(),max=200001,nodes=1;int[][]nx=new int[max][26];int[]fail=new int[max],end=new int[m],cnt=new int[max];for(int z=0;z<m;z++){String w=in.next();int u=0;for(char ch:w.toCharArray()){int c=ch-'a';if(nx[u][c]==0)nx[u][c]=nodes++;u=nx[u][c];}end[z]=u;}ArrayDeque<Integer>q=new ArrayDeque<>();ArrayList<Integer>ord=new ArrayList<>();for(int c=0;c<26;c++)if(nx[0][c]>0)q.add(nx[0][c]);while(!q.isEmpty()){int u=q.remove();ord.add(u);for(int c=0;c<26;c++){int v=nx[u][c];if(v>0){fail[v]=nx[fail[u]][c];q.add(v);}else nx[u][c]=nx[fail[u]][c];}}int u=0;for(char ch:s.toCharArray()){u=nx[u][ch-'a'];cnt[u]++;}for(int i=ord.size()-1;i>=0;i--){int v=ord.get(i);cnt[fail[v]]+=cnt[v];}for(int z=0;z<m;z++)System.out.println(cnt[end[z]]);"""),
  [C("ababa 3\na\naba\nba\n", "3\n2\n2"), C("aaaa 2\na\naa\n", "4\n3")],
  [C("abc 3\na\nb\nc\n", "1\n1\n1"), C("mississippi 3\nissi\nss\nppi\n", "2\n2\n1"), C("abcabc 3\nabc\nbc\ncab\n", "2\n2\n1"), C("z 1\nzz\n", "0")]),
]

assert [x["id"] for x in JAVA_CURRICULUM_PART5] == [f"java-curated-{n:03d}" for n in range(141, 151)]
