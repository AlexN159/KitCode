"""Curated Java 17 core drills 61--80.

Each record is declared once.  Test expectations are literal reviewable data;
this module performs no runtime execution or oracle calculation on import.
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
    return {
        "id": f"java-curated-{number:03d}", "title": title, "language": "java",
        "difficulty": difficulty, "topics": topics, "curriculum_family": topics[0],
        "interview_frequency": "Common", "description": description,
        "constraints": constraints, "hints": hints, "expected_complexity": complexity,
        "starter_code": STARTER, "solution": solution,
        "public_tests": public, "hidden_tests": hidden,
        "examples": [{"input": item["input"], "output": item["expected_output"]} for item in public],
    }


JAVA_CURRICULUM_PART1 = [
drill(61, "Sum Positive Values", "Easy", ["arrays", "loops"],
 "Print the sum of the strictly positive integers.",
 ["0 <= n <= 200,000", "Each value is in [-10^9, 10^9]."],
 ["Zero is not positive.", "Accumulate into a long.", "One pass is sufficient."], "O(n) time, O(1) auxiliary space",
 program('''        int n=in.nextInt(); long sum=0; for(int i=0;i<n;i++){long x=in.nextLong(); if(x>0)sum+=x;} System.out.println(sum);'''),
 [case("3\n1 -2 3\n", "4"), case("3\n-4 0 -1\n", "0")],
 [case("0\n", "0"), case("3\n1000000000 1000000000 -1\n", "2000000000"), case("1\n5\n", "5"), case("5\n-1 2 -3 4 0\n", "6")]),

drill(62, "First Reading At Limit", "Easy", ["arrays", "loops"],
 "Given a limit and readings, print the first zero-based index whose reading is at least the limit, or -1.",
 ["0 <= n <= 200,000", "Readings and limit fit in signed 32-bit integers."],
 ["Keep the first matching index.", "The readings are not sorted.", "Continue consuming the input after finding it."], "O(n) time, O(1) auxiliary space",
 program('''        int n=in.nextInt(), limit=in.nextInt(), answer=-1; for(int i=0;i<n;i++){int x=in.nextInt();if(answer<0&&x>=limit)answer=i;}System.out.println(answer);'''),
 [case("4 5\n1 5 7 2\n", "1"), case("3 10\n1 2 3\n", "-1")],
 [case("0 8\n", "-1"), case("3 -2\n-3 -2 8\n", "1"), case("4 4\n4 4 4 4\n", "0"), case("2 9\n8 9\n", "1")]),

drill(63, "Interior Peak Counter", "Medium", ["arrays", "scanning"],
 "Count elements strictly larger than both immediate neighbours. The endpoints are never peaks.",
 ["0 <= n <= 200,000", "Values fit in signed 32-bit integers."],
 ["Only indices 1 through n - 2 can qualify.", "Equal neighbours do not form a peak.", "Keep the array so each value can inspect both neighbours."], "O(n) time, O(n) auxiliary space",
 program('''        int n=in.nextInt();int[]a=new int[n];for(int i=0;i<n;i++)a[i]=in.nextInt();int count=0;for(int i=1;i+1<n;i++)if(a[i]>a[i-1]&&a[i]>a[i+1])count++;System.out.println(count);'''),
 [case("5\n1 3 2 4 1\n", "2"), case("3\n1 2 3\n", "0")],
 [case("3\n5 5 5\n", "0"), case("2\n1 2\n", "0"), case("5\n-2 0 -1 3 1\n", "2"), case("0\n", "0")]),

drill(64, "Move Zeroes Stably", "Easy", ["array-rearrangement"],
 "Move every zero to the end while preserving the original order of non-zero values.",
 ["0 <= n <= 200,000", "Values fit in signed 32-bit integers."],
 ["Write non-zero values from left to right.", "Fill the remaining positions with zeroes.", "Do not sort: the operation must be stable."], "O(n) time, O(n) auxiliary space",
 program('''        int n=in.nextInt(),w=0;int[]a=new int[n];for(int i=0;i<n;i++){int x=in.nextInt();if(x!=0)a[w++]=x;}while(w<n)a[w++]=0;for(int i=0;i<n;i++){if(i>0)System.out.print(" ");System.out.print(a[i]);}System.out.println();'''),
 [case("5\n0 1 0 3 12\n", "1 3 12 0 0"), case("2\n0 0\n", "0 0")],
 [case("3\n1 2 3\n", "1 2 3"), case("3\n-1 0 -2\n", "-1 -2 0"), case("0\n", ""), case("1\n0\n", "0")]),

drill(65, "Rotate Schedule Right", "Medium", ["array-rearrangement"],
 "Given a signed k, rotate the array k positions right. A negative k rotates left.",
 ["0 <= n <= 200,000", "k fits in signed 32-bit range."],
 ["Reduce k modulo n when n is nonzero.", "Normalize a negative remainder.", "Three reversals perform the rotation in place."], "O(n) time, O(1) auxiliary space",
 program('''        int n=in.nextInt(),k=in.nextInt();int[]a=new int[n];for(int i=0;i<n;i++)a[i]=in.nextInt();if(n>0){k=((k%n)+n)%n;reverse(a,0,n-1);reverse(a,0,k-1);reverse(a,k,n-1);}for(int i=0;i<n;i++){if(i>0)System.out.print(" ");System.out.print(a[i]);}System.out.println();''', '''    static void reverse(int[]a,int l,int r){while(l<r){int t=a[l];a[l++]=a[r];a[r--]=t;}}\n'''),
 [case("5 2\n1 2 3 4 5\n", "4 5 1 2 3"), case("4 -1\n1 2 3 4\n", "2 3 4 1")],
 [case("1 99\n7\n", "7"), case("0 3\n", ""), case("3 3\n1 2 3\n", "1 2 3"), case("5 7\n-1 0 2 8 9\n", "8 9 -1 0 2")]),

drill(66, "Stable Parity Partition", "Easy", ["array-rearrangement"],
 "Print even values in original order, followed by odd values in original order.",
 ["0 <= n <= 200,000", "Values fit in signed 32-bit integers."],
 ["Negative even values still divide evenly by two.", "Make one pass for each parity.", "Preserve relative order within both groups."], "O(n) time, O(n) auxiliary space",
 program('''        int n=in.nextInt(),p=0;int[]a=new int[n],out=new int[n];for(int i=0;i<n;i++)a[i]=in.nextInt();for(int x:a)if(x%2==0)out[p++]=x;for(int x:a)if(x%2!=0)out[p++]=x;for(int i=0;i<n;i++){if(i>0)System.out.print(" ");System.out.print(out[i]);}System.out.println();'''),
 [case("4\n3 2 4 1\n", "2 4 3 1"), case("3\n2 4 6\n", "2 4 6")],
 [case("3\n1 3 5\n", "1 3 5"), case("4\n-3 -2 -1 0\n", "-2 0 -3 -1"), case("0\n", ""), case("1\n0\n", "0")]),

drill(67, "Next Lexicographic Arrangement", "Hard", ["array-rearrangement", "permutations"],
 "Print the next lexicographic permutation. If none exists, print the ascending permutation.",
 ["1 <= n <= 200,000", "Values fit in signed 32-bit integers and may repeat."],
 ["Find the rightmost increasing pivot.", "Swap it with the rightmost larger suffix value.", "Reverse the suffix after the swap."], "O(n) time, O(1) auxiliary space",
 program('''        int n=in.nextInt();int[]a=new int[n];for(int i=0;i<n;i++)a[i]=in.nextInt();int i=n-2;while(i>=0&&a[i]>=a[i+1])i--;if(i>=0){int j=n-1;while(a[j]<=a[i])j--;int t=a[i];a[i]=a[j];a[j]=t;}reverse(a,i+1,n-1);for(i=0;i<n;i++){if(i>0)System.out.print(" ");System.out.print(a[i]);}System.out.println();''', '''    static void reverse(int[]a,int l,int r){while(l<r){int t=a[l];a[l++]=a[r];a[r--]=t;}}\n'''),
 [case("3\n1 2 3\n", "1 3 2"), case("3\n3 2 1\n", "1 2 3")],
 [case("3\n1 1 5\n", "1 5 1"), case("4\n1 3 2 3\n", "1 3 3 2"), case("1\n9\n", "9"), case("4\n2 2 1 2\n", "2 2 2 1")]),

drill(68, "First Vowel Position", "Easy", ["strings", "scanning"],
 "Print the zero-based position of the first English vowel in one line, or -1.",
 ["The input line may be empty.", "The line contains printable ASCII characters."],
 ["Check both lower- and uppercase vowels.", "Scan from left to right.", "Stop when the first vowel is found."], "O(n) time, O(1) auxiliary space",
 program('''        String s=in.nextLine();for(int i=0;i<s.length();i++)if("aeiouAEIOU".indexOf(s.charAt(i))>=0){System.out.println(i);return;}System.out.println(-1);'''),
 [case("sky\n", "-1"), case("Apple\n", "0")],
 [case("bCdE\n", "3"), case("\n", "-1"), case("rhythm\n", "-1"), case("123u\n", "3")]),

drill(69, "Longest Repeated Character Run", "Medium", ["strings", "scanning"],
 "Print the length of the longest contiguous run of a single repeated character.",
 ["The input line may be empty.", "The line contains printable ASCII characters."],
 ["Start a new run when the character changes.", "Track both the current and best run length.", "Handle the empty line before reading s.charAt(0)."], "O(n) time, O(1) auxiliary space",
 program('''        String s=in.nextLine();if(s.isEmpty()){System.out.println(0);return;}int best=1,run=1;for(int i=1;i<s.length();i++){run=s.charAt(i)==s.charAt(i-1)?run+1:1;best=Math.max(best,run);}System.out.println(best);'''),
 [case("aaabbc\n", "3"), case("z\n", "1")],
 [case("\n", "0"), case("abab\n", "1"), case("aaaa\n", "4"), case("  \n", "2")]),

drill(70, "Word Initials", "Medium", ["strings", "tokenization"],
 "Print the uppercase first character of every whitespace-separated word.",
 ["The input line may be empty and may contain tabs or repeated spaces.", "Words are printable ASCII tokens."],
 ["Trim outer whitespace first.", "Split on one-or-more whitespace characters.", "Take exactly one character per word."], "O(n) time, O(n) auxiliary space",
 program('''        String s=in.nextLine().trim();if(s.isEmpty()){System.out.println();return;}String[]w=s.split("\\\\s+");StringBuilder out=new StringBuilder();for(String x:w)out.append(Character.toUpperCase(x.charAt(0)));System.out.println(out);'''),
 [case("pair programming interview\n", "PPI"), case("  red   blue\n", "RB")],
 [case("\n", ""), case("x\n", "X"), case("one\ttwo\n", "OT"), case("99 bottles\n", "9B")]),

drill(71, "Reverse Word Order", "Medium", ["strings", "tokenization"],
 "Reverse whitespace-separated words and print one space between output words.",
 ["The input line may be empty and may contain tabs or repeated spaces.", "Words are printable ASCII tokens."],
 ["Ignore outer whitespace.", "Split into words before printing.", "Walk the word array from right to left."], "O(n) time, O(n) auxiliary space",
 program('''        String s=in.nextLine().trim();if(s.isEmpty()){System.out.println();return;}String[]w=s.split("\\\\s+");for(int i=w.length-1;i>=0;i--){if(i<w.length-1)System.out.print(" ");System.out.print(w[i]);}System.out.println();'''),
 [case("one two three\n", "three two one"), case("  hello   world \n", "world hello")],
 [case("\n", ""), case("solo\n", "solo"), case("a b\n", "b a"), case("tabs\there\n", "here tabs")]),

drill(72, "Run-Length Encode", "Medium", ["strings", "two-pointers"],
 "Encode every maximal run as its character followed by its decimal count.",
 ["The line contains printable ASCII characters.", "0 <= line length <= 200,000."],
 ["Advance a second index across each run.", "Append once per maximal run.", "Counts can have more than one digit."], "O(n) time, O(n) auxiliary space",
 program('''        String s=in.nextLine();StringBuilder out=new StringBuilder();for(int i=0;i<s.length();){int j=i;while(j<s.length()&&s.charAt(j)==s.charAt(i))j++;out.append(s.charAt(i)).append(j-i);i=j;}System.out.println(out);'''),
 [case("aaabbc\n", "a3b2c1"), case("x\n", "x1")],
 [case("\n", ""), case("aaaaaaaaaa\n", "a10"), case("ababa\n", "a1b1a1b1a1"), case("  \n", " 2")]),

drill(73, "Camel Or Pascal To Snake", "Medium", ["strings", "transforms"],
 "Convert a camelCase or PascalCase identifier to lowercase snake_case. Put an underscore before every uppercase character except the first, so HTTPRequest becomes h_t_t_p_request.",
 ["The identifier is nonempty, contains only ASCII letters and digits, and has no underscores."],
 ["A non-first uppercase character starts a new segment.", "Lowercase every letter before appending.", "Digits remain in place and never add an underscore."], "O(n) time, O(n) auxiliary space",
 program('''        String s=in.nextLine();StringBuilder out=new StringBuilder();for(int i=0;i<s.length();i++){char c=s.charAt(i);if(i>0&&Character.isUpperCase(c))out.append('_');out.append(Character.toLowerCase(c));}System.out.println(out);'''),
 [case("camelCase\n", "camel_case"), case("HTTPRequest\n", "h_t_t_p_request")],
 [case("x\n", "x"), case("Version2Number\n", "version2_number"), case("ABC\n", "a_b_c"), case("already\n", "already")]),

drill(74, "Cancel Adjacent Pairs", "Hard", ["strings", "stacks"],
 "Repeatedly remove adjacent equal-character pairs until none remain, then print the remaining string.",
 ["The line contains printable ASCII characters.", "0 <= line length <= 200,000."],
 ["A stack represents the unreduced prefix.", "Pop when the next character equals the top.", "Read the stack from bottom to top for the answer."], "O(n) time, O(n) auxiliary space",
 program('''        String s=in.nextLine();Deque<Character>st=new ArrayDeque<>();for(char c:s.toCharArray()){if(!st.isEmpty()&&st.peek()==c)st.pop();else st.push(c);}StringBuilder out=new StringBuilder();while(!st.isEmpty())out.append(st.removeLast());System.out.println(out);'''),
 [case("abbaca\n", "ca"), case("azxxzy\n", "ay")],
 [case("aaaa\n", ""), case("abc\n", "abc"), case("\n", ""), case("aabccba\n", "a")]),

drill(75, "Unique Sorted Intersection", "Medium", ["sets", "sorting"],
 "Given two integer lists, print shared values once each in increasing order.",
 ["0 <= n, m <= 200,000", "Values fit in signed 32-bit integers."],
 ["Put the first list in a hash set.", "A sorted set removes duplicates and orders the answer.", "Print nothing for an empty intersection."], "O(n + m log m) time, O(n + m) auxiliary space",
 program('''        int n=in.nextInt(),m=in.nextInt();Set<Integer>left=new HashSet<>(),out=new TreeSet<>();for(int i=0;i<n;i++)left.add(in.nextInt());for(int i=0;i<m;i++){int x=in.nextInt();if(left.contains(x))out.add(x);}int i=0;for(int x:out){if(i++>0)System.out.print(" ");System.out.print(x);}System.out.println();'''),
 [case("3 3\n1 2 2\n2 2 3\n", "2"), case("2 2\n1 4\n2 3\n", "")],
 [case("0 2\n1 2\n", ""), case("3 4\n-1 0 1\n1 0 0 -1\n", "-1 0 1"), case("1 1\n7\n7\n", "7"), case("3 2\n5 4 3\n3 5\n", "3 5")]),

drill(76, "First Non-Repeating Character", "Medium", ["strings", "hash-counting"],
 "Print the zero-based position of the first character occurring exactly once in a line, or -1.",
 ["The line contains ASCII characters.", "0 <= line length <= 200,000."],
 ["Count every character first.", "Scan again from the beginning.", "The first frequency of one is the answer."], "O(n) time, O(1) auxiliary space",
 program('''        String s=in.nextLine();int[]count=new int[256];for(char c:s.toCharArray())count[c]++;for(int i=0;i<s.length();i++)if(count[s.charAt(i)]==1){System.out.println(i);return;}System.out.println(-1);'''),
 [case("leetcode\n", "0"), case("aabb\n", "-1")],
 [case("loveleetcode\n", "2"), case("\n", "-1"), case("a\n", "0"), case("aabbccd\n", "6")]),

drill(77, "Evaluate Postfix Expression", "Medium", ["stacks", "parsing"],
 "Given a token count followed by a valid postfix expression of integer literals and +, -, *, /, print its value. Division truncates toward zero.",
 ["1 <= token count <= 200,000", "Every expression is valid and all intermediate results fit signed 32-bit integers.", "No division by zero occurs."],
 ["Numbers go on the stack.", "An operator pops its right operand first.", "Push each computed result back."], "O(n) time, O(n) auxiliary space",
 program('''        int n=in.nextInt();Deque<Integer>st=new ArrayDeque<>();for(int i=0;i<n;i++){String t=in.next();if(t.matches("-?\\\\d+"))st.push(Integer.parseInt(t));else{int b=st.pop(),a=st.pop();if(t.equals("+"))st.push(a+b);else if(t.equals("-"))st.push(a-b);else if(t.equals("*"))st.push(a*b);else st.push(a/b);}}System.out.println(st.pop());'''),
 [case("5\n2 3 + 4 *\n", "20"), case("7\n5 1 2 + 4 * +\n", "17")],
 [case("3\n7 3 /\n", "2"), case("5\n-4 2 * 3 +\n", "-5"), case("1\n9\n", "9"), case("13\n10 6 9 3 + -11 * / * 17 + 5 +\n", "22")]),

drill(78, "Stock Span Lengths", "Medium", ["monotonic-stack"],
 "For each price, print the count of consecutive days ending today whose price is at most today's price.",
 ["0 <= n <= 200,000", "Prices fit in signed 32-bit integers."],
 ["Keep indices with strictly decreasing prices.", "Pop prices no greater than today.", "The remaining top bounds today's span."], "O(n) time, O(n) auxiliary space",
 program('''        int n=in.nextInt();int[]a=new int[n];for(int i=0;i<n;i++)a[i]=in.nextInt();Deque<Integer>st=new ArrayDeque<>();for(int i=0;i<n;i++){while(!st.isEmpty()&&a[st.peek()]<=a[i])st.pop();int span=st.isEmpty()?i+1:i-st.peek();st.push(i);if(i>0)System.out.print(" ");System.out.print(span);}System.out.println();'''),
 [case("7\n100 80 60 70 60 75 85\n", "1 1 1 2 1 4 6"), case("4\n1 2 3 4\n", "1 2 3 4")],
 [case("3\n5 5 5\n", "1 2 3"), case("1\n9\n", "1"), case("4\n4 3 2 1\n", "1 1 1 1"), case("0\n", "")]),

drill(79, "Sliding Window Maximums", "Hard", ["deque", "sliding-window"],
 "Given n, k, and an array, print the maximum value of each contiguous window of length k.",
 ["1 <= k <= n <= 200,000", "Values fit in signed 32-bit integers."],
 ["Keep indices in decreasing value order.", "Discard an index once it leaves the window.", "The deque front holds the current maximum."], "O(n) time, O(k) auxiliary space",
 program('''        int n=in.nextInt(),k=in.nextInt();int[]a=new int[n];for(int i=0;i<n;i++)a[i]=in.nextInt();Deque<Integer>d=new ArrayDeque<>();for(int i=0;i<n;i++){while(!d.isEmpty()&&d.peekFirst()<=i-k)d.removeFirst();while(!d.isEmpty()&&a[d.peekLast()]<=a[i])d.removeLast();d.addLast(i);if(i>=k-1){if(i>k-1)System.out.print(" ");System.out.print(a[d.peekFirst()]);}}System.out.println();'''),
 [case("8 3\n1 3 -1 -3 5 3 6 7\n", "3 3 5 5 6 7"), case("4 1\n4 2 7 1\n", "4 2 7 1")],
 [case("3 3\n2 2 2\n", "2"), case("5 2\n9 8 7 6 5\n", "9 8 7 6"), case("5 2\n1 1 1 1 1\n", "1 1 1 1"), case("4 4\n-1 -2 -3 -4\n", "-1")]),

drill(80, "Canonical Unix Path", "Medium", ["stacks", "strings"],
 "Simplify an absolute Unix path: ignore . and empty segments, process .., and print the canonical absolute path.",
 ["The input path begins with /.", "Path length <= 200,000 and segments contain no slash."],
 ["Split on slash.", "Push ordinary segments.", "Never pop above the root."], "O(n) time, O(n) auxiliary space",
 program('''        String[]parts=in.nextLine().split("/");Deque<String>st=new ArrayDeque<>();for(String x:parts){if(x.equals("")||x.equals("."))continue;if(x.equals("..")){if(!st.isEmpty())st.pop();}else st.push(x);}StringBuilder out=new StringBuilder();while(!st.isEmpty())out.append('/').append(st.removeLast());System.out.println(out.length()==0?"/":out);'''),
 [case("/home/\n", "/home"), case("/a/./b/../../c/\n", "/c")],
 [case("/../\n", "/"), case("/a//b////c/d//././/..\n", "/a/b/c"), case("/\n", "/"), case("/x/../../y\n", "/y")]),
]

assert len(JAVA_CURRICULUM_PART1) == 20
assert [item["id"] for item in JAVA_CURRICULUM_PART1] == [f"java-curated-{n:03d}" for n in range(61, 81)]
assert sum(item["difficulty"] == "Easy" for item in JAVA_CURRICULUM_PART1) == 5
assert sum(item["difficulty"] == "Medium" for item in JAVA_CURRICULUM_PART1) == 12
assert sum(item["difficulty"] == "Hard" for item in JAVA_CURRICULUM_PART1) == 3
