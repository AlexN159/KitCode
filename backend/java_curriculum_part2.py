"""Curated Java 17 core drills 81--100.

Every exercise is a standalone stdin/stdout practice contract.  The literal
fixtures are intentionally kept beside their reference program; importing this
module neither runs Java nor computes expected answers.
"""
from __future__ import annotations

STARTER = '''import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        // Read stdin, solve the exercise, and print only the requested result.
    }
}
'''


def program(body: str, helpers: str = "") -> str:
    return f"""import java.io.*;
import java.util.*;

public class Main {{
    public static void main(String[] args) throws Exception {{
        Scanner in = new Scanner(new BufferedInputStream(System.in));
{body}
    }}
{helpers}}}
"""


def case(input_text: str, expected_output: str) -> dict[str, str]:
    return {"input": input_text, "expected_output": expected_output}


def drill(number: int, title: str, difficulty: str, topics: list[str], description: str,
          constraints: list[str], hints: list[str], complexity: str, solution: str,
          public: list[dict[str, str]], hidden: list[dict[str, str]]) -> dict:
    return {"id": f"java-curated-{number:03d}", "title": title, "language": "java",
            "difficulty": difficulty, "topics": topics, "curriculum_family": topics[0],
            "practice_frequency": "Common", "description": description,
            "constraints": constraints, "hints": hints, "expected_complexity": complexity,
            "starter_code": STARTER, "solution": solution, "public_tests": public,
            "hidden_tests": hidden,
            "examples": [{"input": x["input"], "output": x["expected_output"]} for x in public]}


JAVA_CURRICULUM_PART2 = [
drill(81, "Integer Cube Root", "Easy", ["binary-search", "numbers"],
 "For nonnegative long n, print floor(cuberoot(n)): the largest long r with r^3 <= n.",
 ["0 <= n <= 9,223,372,036,854,775,807.", "Do not multiply three long values without guarding overflow."],
 ["The answer is at most 2,097,151.", "Compare mid with n / mid / mid when mid is positive.", "Move the lower bound up when mid is feasible."], "O(log n) time, O(1) auxiliary space",
 program('''        long n=in.nextLong(),lo=0,hi=2097152,ans=0;while(lo<=hi){long m=lo+(hi-lo)/2;if(m==0||m<=n/m/m){ans=m;lo=m+1;}else hi=m-1;}System.out.println(ans);'''),
 [case("27\n", "3"), case("28\n", "3")],
 [case("0\n", "0"), case("1\n", "1"), case("9223372036854775807\n", "2097151"), case("64\n", "4")]),

drill(82, "Peak Index In Mountain", "Easy", ["binary-search", "arrays"],
 "Line 1 is n and line 2 is a valid mountain array. Print its unique peak index; a mountain strictly rises then strictly falls.",
 ["3 <= n <= 200,000.", "Values are distinct signed 32-bit integers and the input is guaranteed to be a mountain."],
 ["Compare a[mid] to a[mid + 1].", "If it rises, the peak is to the right.", "Otherwise mid may already be the peak."], "O(log n) time, O(n) auxiliary space for the input array",
 program('''        int n=in.nextInt(),l=0,r=n-1;int[]a=new int[n];for(int i=0;i<n;i++)a[i]=in.nextInt();while(l<r){int m=l+(r-l)/2;if(a[m]<a[m+1])l=m+1;else r=m;}System.out.println(l);'''),
 [case("5\n1 3 5 4 2\n", "2"), case("3\n0 2 1\n", "1")],
 [case("4\n1 4 3 2\n", "1"), case("6\n-5 -2 0 7 3 1\n", "3"), case("7\n1 2 3 4 5 3 1\n", "4"), case("5\n2 9 8 4 0\n", "1")]),

drill(83, "Target Range In Sorted Values", "Medium", ["binary-search", "arrays"],
 "Line 1 contains n and target; line 2 is a nondecreasing array. Print target's first and last zero-based indices, or -1 -1 when absent.",
 ["0 <= n <= 200,000.", "Line 2 contains exactly n values; values and target fit in signed 32-bit integers."],
 ["Find the first value not less than target.", "Find the first value greater than target separately.", "Confirm the first position really holds target."], "O(log n) time, O(n) auxiliary space for the input array",
 program('''        int n=in.nextInt(),t=in.nextInt();int[]a=new int[n];for(int i=0;i<n;i++)a[i]=in.nextInt();int l=lower(a,t),u=upper(a,t);if(l==n||a[l]!=t)System.out.println("-1 -1");else System.out.println(l+" "+(u-1));''', '''    static int lower(int[]a,int x){int l=0,r=a.length;while(l<r){int m=(l+r)/2;if(a[m]<x)l=m+1;else r=m;}return l;}\n    static int upper(int[]a,int x){int l=0,r=a.length;while(l<r){int m=(l+r)/2;if(a[m]<=x)l=m+1;else r=m;}return l;}\n'''),
 [case("6 8\n5 7 7 8 8 10\n", "3 4"), case("4 3\n1 2 4 5\n", "-1 -1")],
 [case("0 1\n", "-1 -1"), case("4 2\n2 2 2 2\n", "0 3"), case("5 -1\n-2 -1 -1 0 3\n", "1 2"), case("1 9\n9\n", "0 0")]),

drill(84, "Best Pair Under Budget", "Medium", ["two-pointers", "sorting"],
 "Line 1 contains n and budget; line 2 contains nonnegative prices. Print the greatest sum of two different items not exceeding the budget, or NONE if no pair fits.",
 ["0 <= n <= 200,000.", "Line 2 contains exactly n prices; prices and budget are nonnegative signed 32-bit integers, so use long for a pair sum."],
 ["Sort the prices.", "A too-expensive pair needs a smaller right value.", "A feasible pair is a candidate before advancing left."], "O(n log n) time, O(n) auxiliary space",
 program('''        int n=in.nextInt();long b=in.nextLong(),best=-1;long[]a=new long[n];for(int i=0;i<n;i++)a[i]=in.nextLong();Arrays.sort(a);for(int l=0,r=n-1;l<r;){long s=a[l]+a[r];if(s<=b){best=Math.max(best,s);l++;}else r--;}System.out.println(best<0?"NONE":best);'''),
 [case("4 10\n2 7 4 8\n", "10"), case("3 3\n4 5 6\n", "NONE")],
 [case("1 20\n10\n", "NONE"), case("4 0\n0 0 1 2\n", "0"), case("5 11\n1 5 5 7 9\n", "10"), case("3 2000000000\n1000000000 1000000000 1\n", "2000000000")]),

drill(85, "Longest Ones With Flip Allowance", "Medium", ["sliding-window", "arrays"],
 "Line 1 contains n and k; line 2 is a binary array. Print the maximum contiguous length obtainable by changing at most k zeroes to one.",
 ["0 <= n <= 200,000 and 0 <= k <= n.", "Line 2 contains exactly n values, each 0 or 1."],
 ["Expand the right endpoint one value at a time.", "Count zeroes currently inside the window.", "Shrink from the left until at most k zeroes remain."], "O(n) time, O(n) auxiliary space for the input array",
 program('''        int n=in.nextInt(),k=in.nextInt(),l=0,z=0,best=0;int[]a=new int[n];for(int i=0;i<n;i++)a[i]=in.nextInt();for(int r=0;r<n;r++){if(a[r]==0)z++;while(z>k)if(a[l++]==0)z--;best=Math.max(best,r-l+1);}System.out.println(best);'''),
 [case("7 1\n1 0 1 1 0 0 1\n", "4"), case("4 0\n1 1 0 1\n", "2")],
 [case("0 0\n", "0"), case("5 5\n0 0 0 0 0\n", "5"), case("5 1\n0 0 1 0 1\n", "3"), case("3 1\n1 1 1\n", "3")]),

drill(86, "Longest Two-Character Window", "Medium", ["sliding-window", "strings"],
 "Print the length of the longest substring containing at most two distinct characters.",
 ["The input is one printable-ASCII line, possibly empty.", "Line length is at most 200,000."],
 ["Store frequencies for the current window.", "When three characters occur, move the left edge.", "Track the widest valid window."], "O(n) time, O(1) auxiliary space",
 program('''        String s=in.nextLine();int[]c=new int[256];int l=0,d=0,b=0;for(int r=0;r<s.length();r++){if(c[s.charAt(r)]++==0)d++;while(d>2)if(--c[s.charAt(l++)]==0)d--;b=Math.max(b,r-l+1);}System.out.println(b);'''),
 [case("eceba\n", "3"), case("ccaabbb\n", "5")],
 [case("\n", "0"), case("a\n", "1"), case("abab\n", "4"), case("abcabc\n", "2")]),

drill(87, "Best Stock Trade With Days", "Medium", ["arrays", "scanning"],
 "Line 1 is n and line 2 contains daily prices. Print buyIndex sellIndex profit for a buy followed by a later sell. Maximize profit; on a tie choose the earlier buy, then earlier sell. Print NONE if no positive-profit trade exists.",
 ["0 <= n <= 200,000.", "Line 2 contains exactly n nonnegative signed 32-bit prices; profit fits in long."],
 ["Keep the cheapest price and its earliest day so far.", "At each day, evaluate selling today.", "Only replace an equal-profit answer if its tie tuple is earlier."], "O(n) time, O(1) auxiliary space",
 program('''        int n=in.nextInt();long min=Long.MAX_VALUE,best=0;int md=-1,bi=-1,si=-1;for(int i=0;i<n;i++){long p=in.nextLong();if(md>=0){long gain=p-min;if(gain>best||(gain==best&&gain>0&&(md<bi||(md==bi&&i<si)))){best=gain;bi=md;si=i;}}if(p<min){min=p;md=i;}}System.out.println(best==0?"NONE":bi+" "+si+" "+best);'''),
 [case("6\n7 1 5 3 6 4\n", "1 4 5"), case("5\n7 6 4 3 1\n", "NONE")],
 [case("4\n1 4 2 5\n", "0 3 4"), case("5\n3 1 4 1 4\n", "1 2 3"), case("1\n9\n", "NONE"), case("4\n2 2 5 5\n", "0 2 3")]),

drill(88, "Circular Next Greater Values", "Medium", ["monotonic-stack", "arrays"],
 "Line 1 is n and line 2 is a circular array. For every value, print the first strictly greater value encountered while moving right, or -1.",
 ["0 <= n <= 1,900.", "Line 2 contains exactly n signed 32-bit values; the bound keeps the required output within the local runner limit."],
 ["Walk two passes from right to left.", "Remove stack values no greater than the current value.", "Only write answers during the first virtual pass."], "O(n) time, O(n) auxiliary space",
 program('''        int n=in.nextInt();int[]a=new int[n],out=new int[n];for(int i=0;i<n;i++)a[i]=in.nextInt();Arrays.fill(out,-1);Deque<Integer>st=new ArrayDeque<>();for(int i=2*n-1;i>=0;i--){int x=a[i%n];while(!st.isEmpty()&&st.peek()<=x)st.pop();if(i<n&&!st.isEmpty())out[i]=st.peek();st.push(x);}for(int i=0;i<n;i++){if(i>0)System.out.print(" ");System.out.print(out[i]);}System.out.println();'''),
 [case("3\n1 2 1\n", "2 -1 2"), case("4\n3 2 1 4\n", "4 4 4 -1")],
 [case("0\n", ""), case("3\n5 5 5\n", "-1 -1 -1"), case("1\n-2\n", "-1"), case("5\n1 5 3 6 8\n", "5 6 6 8 -1")]),

drill(89, "Asteroid Collision", "Medium", ["stacks", "simulation"],
 "Line 1 is n and line 2 contains asteroids: positive values move right and negative values move left. Equal magnitudes both disappear. Print survivors in original order.",
 ["0 <= n <= 1,900.", "Line 2 contains exactly n nonzero signed 32-bit values; Integer.MIN_VALUE is allowed and the bound keeps output within the local runner limit."],
 ["Only a right-moving stack top can meet a new left mover.", "Keep resolving while the new asteroid survives.", "A left mover that survives goes on the stack too."], "O(n) time, O(n) auxiliary space",
 program('''        int n=in.nextInt();Deque<Integer>st=new ArrayDeque<>();for(int i=0;i<n;i++){int x=in.nextInt();boolean alive=true;while(alive&&x<0&&!st.isEmpty()&&st.peekLast()>0){long a=st.peekLast(),b=-(long)x;if(a<b)st.removeLast();else if(a==b){st.removeLast();alive=false;}else alive=false;}if(alive)st.addLast(x);}int i=0;for(int x:st){if(i++>0)System.out.print(" ");System.out.print(x);}System.out.println();'''),
 [case("3\n5 10 -5\n", "5 10"), case("2\n8 -8\n", "")],
 [case("3\n10 2 -5\n", "10"), case("4\n-2 -1 1 2\n", "-2 -1 1 2"), case("2\n1 -2147483648\n", "-2147483648"), case("0\n", "")]),

drill(90, "Decode Bracketed Repetitions", "Medium", ["stacks", "parsing"],
 "Read one encoded line and decode it: k[fragment] repeats fragment k times. Letters are lowercase and nested groups are allowed.",
 ["Input length <= 20,000; each repeat count is 1 through 1,000.", "The decoded output length is at most 20,000 characters and syntax is valid."],
 ["Save the completed prefix when an opening bracket appears.", "Accumulate all digits of a repeat count.", "On ], append the current fragment count times to the saved prefix."], "O(input length * decoded length) worst-case time for nested builders, O(input length + decoded length) auxiliary space",
 program('''        String s=in.nextLine();Deque<Integer>ns=new ArrayDeque<>();Deque<StringBuilder>ss=new ArrayDeque<>();StringBuilder cur=new StringBuilder();int num=0;for(char c:s.toCharArray()){if(Character.isDigit(c))num=num*10+c-'0';else if(c=='['){ns.push(num);ss.push(cur);num=0;cur=new StringBuilder();}else if(c==']'){StringBuilder p=ss.pop();int k=ns.pop();for(int i=0;i<k;i++)p.append(cur);cur=p;}else cur.append(c);}System.out.println(cur);'''),
 [case("3[a2[c]]\n", "accaccacc"), case("2[ab]3[c]\n", "ababccc")],
 [case("10[x]\n", "xxxxxxxxxx"), case("1[a]\n", "a"), case("2[a]3[bc]\n", "aabcbcbc"), case("2[a2[b]c]\n", "abbcabbc")]),

drill(91, "Validate Stack Pop Order", "Medium", ["stacks", "simulation"],
 "Line 1 is n, followed by the push sequence and proposed pop sequence on separate lines. Print true if the pop order is attainable, otherwise false.",
 ["0 <= n <= 200,000.", "The next two lines each contain exactly n values and are permutations of the same distinct signed 32-bit integers."],
 ["Push values in the given order.", "After each push, pop as long as the next requested value is on top.", "All requested pops must be consumed."], "O(n) time, O(n) auxiliary space",
 program('''        int n=in.nextInt();int[]p=new int[n],q=new int[n];for(int i=0;i<n;i++)p[i]=in.nextInt();for(int i=0;i<n;i++)q[i]=in.nextInt();Deque<Integer>st=new ArrayDeque<>();int j=0;for(int x:p){st.push(x);while(!st.isEmpty()&&j<n&&st.peek()==q[j]){st.pop();j++;}}System.out.println(j==n?"true":"false");'''),
 [case("5\n1 2 3 4 5\n4 5 3 2 1\n", "true"), case("5\n1 2 3 4 5\n4 3 5 1 2\n", "false")],
 [case("0\n\n", "true"), case("1\n7\n7\n", "true"), case("3\n1 2 3\n3 1 2\n", "false"), case("4\n9 8 7 6\n6 7 8 9\n", "true")]),

drill(92, "Kth Smallest Matrix Value", "Medium", ["binary-search", "matrices"],
 "Line 1 contains n and 1-based k, followed by an n by n matrix sorted nondecreasingly across rows and columns. Print its kth smallest value.",
 ["1 <= n <= 500 and 1 <= k <= n*n.", "Values fit in signed 32-bit integers and duplicates are allowed."],
 ["Binary-search a value, not a position.", "Count values <= mid by walking from the bottom-left corner.", "Use long for the search bounds and midpoint."], "O(n log(value range)) time, O(n^2) auxiliary space for the matrix",
 program('''        int n=in.nextInt(),k=in.nextInt();int[][]a=new int[n][n];for(int i=0;i<n;i++)for(int j=0;j<n;j++)a[i][j]=in.nextInt();long lo=a[0][0],hi=a[n-1][n-1];while(lo<hi){long m=lo+(hi-lo)/2;int c=0,r=n-1,col=0;while(r>=0&&col<n){if(a[r][col]<=m){c+=r+1;col++;}else r--;}if(c<k)lo=m+1;else hi=m;}System.out.println(lo);'''),
 [case("3 8\n1 5 9\n10 11 13\n12 13 15\n", "13"), case("1 1\n-5\n", "-5")],
 [case("2 3\n1 2\n2 3\n", "2"), case("3 1\n1 1 2\n1 2 3\n2 3 4\n", "1"), case("3 9\n1 1 2\n1 2 3\n2 3 4\n", "4"), case("2 2\n-4 -1\n0 3\n", "-1")]),

drill(93, "Count Array Inversions", "Medium", ["divide-and-conquer", "sorting"],
 "Line 1 is n and line 2 is an integer array. Print the number of pairs i < j for which a[i] > a[j].",
 ["0 <= n <= 200,000.", "Values fit in signed 32-bit integers; the answer fits in long."],
 ["Merge two sorted halves.", "When taking from the right, every remaining left value is an inversion.", "Do not use a quadratic nested loop."], "O(n log n) time, O(n) auxiliary space",
 program('''        int n=in.nextInt();int[]a=new int[n],t=new int[n];for(int i=0;i<n;i++)a[i]=in.nextInt();System.out.println(sort(a,t,0,n));''', '''    static long sort(int[]a,int[]t,int l,int r){if(r-l<2)return 0;int m=(l+r)/2;long ans=sort(a,t,l,m)+sort(a,t,m,r);int i=l,j=m,k=l;while(i<m||j<r){if(j==r||(i<m&&a[i]<=a[j]))t[k++]=a[i++];else{ans+=m-i;t[k++]=a[j++];}}for(i=l;i<r;i++)a[i]=t[i];return ans;}\n'''),
 [case("5\n2 4 1 3 5\n", "3"), case("3\n1 2 3\n", "0")],
 [case("0\n", "0"), case("3\n3 2 1\n", "3"), case("4\n1 1 1 1\n", "0"), case("5\n5 -1 3 2 0\n", "7")]),

drill(94, "Minimum Swaps To Sort", "Medium", ["sorting", "cycles"],
 "Line 1 is n and line 2 contains distinct integers. Print the fewest swaps needed to arrange them in increasing order.",
 ["0 <= n <= 200,000.", "All values are distinct signed 32-bit integers."],
 ["Sort value/index pairs by value.", "Their original indices describe a permutation.", "A cycle of length c costs c - 1 swaps."], "O(n log n) time, O(n) auxiliary space",
 program('''        int n=in.nextInt();int[][]p=new int[n][2];for(int i=0;i<n;i++){p[i][0]=in.nextInt();p[i][1]=i;}Arrays.sort(p,(a,b)->Integer.compare(a[0],b[0]));boolean[]seen=new boolean[n];int ans=0;for(int i=0;i<n;i++)if(!seen[i]){int c=0,j=i;while(!seen[j]){seen[j]=true;c++;j=p[j][1];}ans+=c-1;}System.out.println(ans);'''),
 [case("4\n4 3 2 1\n", "2"), case("5\n1 5 4 3 2\n", "2")],
 [case("0\n", "0"), case("1\n9\n", "0"), case("3\n2 1 3\n", "1"), case("5\n10 -1 7 3 0\n", "3")]),

drill(95, "Weighted Non-Overlapping Jobs", "Hard", ["dynamic-programming", "intervals"],
 "Line 1 is n; each following line is start end profit. Choose non-overlapping jobs with end <= next start and print the maximum total profit; choosing no jobs is allowed.",
 ["0 <= n <= 200,000; start < end and 0 <= profit.", "Times fit in signed 32-bit integers and total profit fits in long."],
 ["Sort jobs by end time.", "Binary-search the last job ending no later than this start.", "Compare taking this job to carrying forward the previous optimum."], "O(n log n) time, O(n) auxiliary space",
 program('''        int n=in.nextInt();long[][]a=new long[n][3];for(int i=0;i<n;i++){a[i][0]=in.nextLong();a[i][1]=in.nextLong();a[i][2]=in.nextLong();}Arrays.sort(a,(x,y)->Long.compare(x[1],y[1]));long[]ends=new long[n],dp=new long[n+1];for(int i=0;i<n;i++)ends[i]=a[i][1];for(int i=1;i<=n;i++){int j=last(ends,i-1,a[i-1][0]);dp[i]=Math.max(dp[i-1],a[i-1][2]+dp[j+1]);}System.out.println(dp[n]);''', '''    static int last(long[]e,int hi,long x){int l=0,r=hi,ans=-1;while(l<r){int m=(l+r)/2;if(e[m]<=x){ans=m;l=m+1;}else r=m;}return ans;}\n'''),
 [case("4\n1 3 50\n3 5 20\n6 19 100\n2 100 200\n", "200"), case("3\n1 2 5\n2 3 6\n3 4 5\n", "16")],
 [case("0\n", "0"), case("3\n1 4 10\n2 3 100\n4 5 10\n", "110"), case("2\n1 5 7\n5 6 8\n", "15"), case("4\n1 2 3\n2 4 4\n1 4 10\n4 5 5\n", "15")]),

drill(96, "Task Cooldown Schedule Length", "Medium", ["greedy", "counting"],
 "Line 1 is cooldown and line 2 is an uppercase A-Z task string. Between identical tasks there must be at least cooldown other positions; print the minimum schedule length including idle slots.",
 ["0 <= task count <= 200,000 and 0 <= cooldown <= 100,000.", "The task line has no spaces; an empty task line is allowed."],
 ["Only the largest frequency determines the unavoidable idle frame.", "Count how many tasks share that largest frequency.", "The schedule cannot be shorter than the number of tasks."], "O(task count + alphabet) time, O(alphabet) auxiliary space",
 program('''        int cool=in.nextInt();String s=in.hasNext()?in.next():"";if(s.isEmpty()){System.out.println(0);return;}int[]c=new int[26];for(char x:s.toCharArray())c[x-'A']++;int max=0,k=0;for(int x:c)max=Math.max(max,x);for(int x:c)if(x==max)k++;long frame=(long)(max-1)*(cool+1)+k;System.out.println(Math.max(s.length(),frame));'''),
 [case("2\nAAABBB\n", "8"), case("0\nAAABBB\n", "6")],
 [case("1\nAAABBB\n", "6"), case("3\nAAAA\n", "13"), case("2\nAAABC\n", "7"), case("5\n\n", "0")]),

drill(97, "Minimum Window Subsequence", "Hard", ["two-pointers", "strings"],
 "Given source s then target t on separate lines, print the shortest contiguous substring of s containing t as a subsequence. For equal lengths print the earliest; print NONE if impossible.",
 ["Both lines contain lowercase ASCII letters; 0 <= |s| <= 20,000 and 1 <= |t| <= 100.", "The target must keep order but need not be contiguous."],
 ["Track the latest start for every target prefix.", "Update those prefix starts from right to left for each source character.", "Keep the first shortest complete window."], "O(|s| * |t|) time, O(|t|) auxiliary space",
 program('''        String s=in.nextLine(),t=in.nextLine();int[]start=new int[t.length()];Arrays.fill(start,-1);int best=Integer.MAX_VALUE,bs=-1;for(int i=0;i<s.length();i++)for(int j=t.length()-1;j>=0;j--)if(s.charAt(i)==t.charAt(j)){if(j==0)start[0]=i;else if(start[j-1]>=0)start[j]=start[j-1];if(j==t.length()-1&&start[j]>=0&&i-start[j]+1<best){best=i-start[j]+1;bs=start[j];}}System.out.println(bs<0?"NONE":s.substring(bs,bs+best));'''),
 [case("abcdebdde\nbde\n", "bcde"), case("jmeqksfrsdcmsiwvaovztaqenprpvnbstl\nv\n", "v")],
 [case("abc\nd\n", "NONE"), case("abcbc\nabc\n", "abc"), case("fgrqsqsnodwmxzkzxwqegkndaa\nkzed\n", "kzxwqegknd"), case("aaaaa\naa\n", "aa")]),

drill(98, "Earliest Longest Palindrome", "Medium", ["strings", "center-expansion"],
 "Print the longest palindromic substring. If several have the same length, print the one with the lowest starting index.",
 ["The input is one printable-ASCII line, possibly empty, of length at most 2,000."],
 ["Each center can have an odd and an even palindrome.", "Expand while the boundary characters match.", "Only replace the answer when a strictly longer palindrome is found."], "O(n^2) time, O(1) auxiliary space",
 program('''        String s=in.nextLine();int bs=0,bl=0;for(int c=0;c<s.length();c++){for(int l=c,r=c;l>=0&&r<s.length()&&s.charAt(l)==s.charAt(r);l--,r++){if(r-l+1>bl){bs=l;bl=r-l+1;}}for(int l=c,r=c+1;l>=0&&r<s.length()&&s.charAt(l)==s.charAt(r);l--,r++){if(r-l+1>bl){bs=l;bl=r-l+1;}}}System.out.println(s.substring(bs,bs+bl));'''),
 [case("babad\n", "bab"), case("cbbd\n", "bb")],
 [case("\n", ""), case("a\n", "a"), case("abacdfgdcaba\n", "aba"), case("forgeeksskeegfor\n", "geeksskeeg")]),

drill(99, "Count Palindromic Substrings", "Medium", ["strings", "center-expansion"],
 "Print the number of nonempty contiguous substrings that are palindromes; equal text at different positions counts separately.",
 ["The input is one printable-ASCII line, possibly empty, of length at most 5,000.", "The answer fits in long."],
 ["Every position is an odd-length center.", "Every gap is an even-length center.", "Count each successful outward expansion."], "O(n^2) time, O(1) auxiliary space",
 program('''        String s=in.nextLine();long ans=0;for(int c=0;c<s.length();c++){for(int l=c,r=c;l>=0&&r<s.length()&&s.charAt(l)==s.charAt(r);l--,r++)ans++;for(int l=c,r=c+1;l>=0&&r<s.length()&&s.charAt(l)==s.charAt(r);l--,r++)ans++;}System.out.println(ans);'''),
 [case("abc\n", "3"), case("aaa\n", "6")],
 [case("\n", "0"), case("a\n", "1"), case("abba\n", "6"), case("ababa\n", "9")]),

drill(100, "Wildcard Whole-String Match", "Hard", ["dynamic-programming", "strings"],
 "Given pattern then text on separate lines, print true when ? matches one character and * matches any sequence (including empty) and the whole text matches.",
 ["Pattern and text contain printable ASCII characters other than newline; each length is at most 2,000.", "Only ? and * have special meaning in the pattern."],
 ["Let dp[j] mean that the processed pattern matches the first j text characters.", "A * can keep the previous-row match or consume one more character.", "Initialize leading stars to match the empty text."], "O(pattern length * text length) time, O(text length) auxiliary space",
 program('''        String p=in.nextLine(),s=in.nextLine();boolean[]dp=new boolean[s.length()+1];dp[0]=true;for(int i=0;i<p.length();i++){char x=p.charAt(i);boolean diag=dp[0];dp[0]=dp[0]&&x=='*';for(int j=1;j<=s.length();j++){boolean old=dp[j];if(x=='*')dp[j]=dp[j]||dp[j-1];else dp[j]=diag&&(x=='?'||x==s.charAt(j-1));diag=old;}}System.out.println(dp[s.length()]?"true":"false");'''),
 [case("a*b?\naaabx\n", "true"), case("a*c\nab\n", "false")],
 [case("*\n\n", "true"), case("?\n\n", "false"), case("**a?\nbaZ\n", "true"), case("a?b\nacb\n", "true")]),
]

assert len(JAVA_CURRICULUM_PART2) == 20
assert [item["id"] for item in JAVA_CURRICULUM_PART2] == [f"java-curated-{n:03d}" for n in range(81, 101)]
assert sum(item["difficulty"] == "Easy" for item in JAVA_CURRICULUM_PART2) == 2
assert sum(item["difficulty"] == "Medium" for item in JAVA_CURRICULUM_PART2) == 15
assert sum(item["difficulty"] == "Hard" for item in JAVA_CURRICULUM_PART2) == 3
