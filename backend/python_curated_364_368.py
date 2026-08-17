"""Audited Hard string-algorithm Python curriculum tranche 364--368."""
from __future__ import annotations

STARTER="import sys\n\ndef solve() -> None:\n    pass\n\nif __name__ == '__main__':\n    solve()\n"; ITEMS=[]
def add(n,t,top,desc,con,hints,cx,body,cases,why):
 r=[{"input":x,"expected_output":y} for x,y in cases]; ITEMS.append({"id":f"python-curated-{n:03d}","language":"python","title":t,"difficulty":"Hard","topics":top,"practice_frequency":"Common","description":desc,"constraints":con,"hints":hints,"expected_complexity":cx,"starter_code":STARTER,"solution":"import sys\n"+body+"\n\nif __name__ == '__main__':\n    solve()\n","examples":[{"input":r[0]["input"],"output":r[0]["expected_output"],"explanation":why}],"public_tests":r[:2],"hidden_tests":r[2:]})

add(364,"Suffix-automaton longest common substring",["strings","suffix-automaton"],"Read two possibly empty lowercase strings. Print the maximum common substring length, then the lexicographically smallest common substring with that length.",["0 <= length of each string <= 1,000","Both strings contain only lowercase English letters","A substring is contiguous; the second output line is empty when the maximum length is zero"],["Build states for every prefix of the first string.","Follow suffix links while scanning the second string.","For equal best lengths, compare the candidate substrings."],"O((n + m)L) worst-case time and O(n) auxiliary space, where L is the longest common substring length",'''def solve():
 a=input().strip();b=input().strip();n=len(a);link=[-1];length=[0];go=[{}];last=0
 for ch in a:
  cur=len(go);go.append({});length.append(length[last]+1);link.append(0);p=last
  while p>=0 and ch not in go[p]:go[p][ch]=cur;p=link[p]
  if p<0:link[cur]=0
  else:
   q=go[p][ch]
   if length[p]+1==length[q]:link[cur]=q
   else:
    clone=len(go);go.append(go[q].copy());length.append(length[p]+1);link.append(link[q])
    while p>=0 and go[p].get(ch)==q:go[p][ch]=clone;p=link[p]
    link[q]=link[cur]=clone
  last=cur
 state=run=best=0;answer=''
 for i,ch in enumerate(b):
  while state and ch not in go[state]:state=link[state];run=length[state]
  if ch in go[state]:state=go[state][ch];run+=1
  else:state=0;run=0
  if run>=best:
   candidate=b[i-run+1:i+1]
   if run>best or candidate<answer:best=run;answer=candidate
 print(best);print(answer)''',[("ababc\nbabca\n","4\nbabc"),("aaaa\nbaaa\n","3\naaa"),("abc\ndef\n","0\n"),("banana\nananas\n","5\nanana"),("ababa\nbabab\n","4\nabab"),("z\nz\n","1\nz")],"The shared substring babc has length four.")
add(365,"Palindromic-tree distinct substring count",["strings","palindromic-tree"],"Read one nonempty lowercase string and print its number of distinct palindromic substrings.",["1 <= length <= 200,000","The string contains only lowercase English letters"],["Start with the two imaginary roots of lengths -1 and 0.","Follow suffix links until the new character can extend a palindrome.","Each newly created non-root node is one distinct palindrome."],"O(n) expected time and O(n) auxiliary space",'''def solve():
 s=input().strip();nxt=[{},{}];size=[-1,0];link=[0,0];last=1
 for i,ch in enumerate(s):
  cur=last
  while i-1-size[cur]<0 or s[i-1-size[cur]]!=ch:cur=link[cur]
  if ch in nxt[cur]:last=nxt[cur][ch];continue
  last=len(nxt);nxt.append({});size.append(size[cur]+2);link.append(0);nxt[cur][ch]=last
  if size[last]==1:link[last]=1;continue
  p=link[cur]
  while i-1-size[p]<0 or s[i-1-size[p]]!=ch:p=link[p]
  link[last]=nxt[p][ch]
 print(len(nxt)-2)''',[("ababa\n","5"),("aaaa\n","4"),("abc\n","3"),("a\n","1"),("abacaba\n","7"),("abba\n","4")],"The palindromes are a, b, aba, bab, and ababa.")
add(366,"Booth minimum cyclic rotation index",["strings","cyclic-strings"],"Read a nonempty printable-ASCII string and print the smallest zero-based start index of a lexicographically smallest cyclic rotation.",["1 <= length <= 200,000","Characters are printable ASCII (code points 32 through 126); leading and internal spaces are allowed","If several rotations are equal, print the smallest start index"],["Compare two candidate starts in the doubled string.","Discard the start with the larger mismatching character.","Reset the matched length after discarding a candidate."],"O(n) time and O(n) auxiliary space",'''def solve():
 s=input();n=len(s);d=s+s;i=0;j=1;k=0
 while i<n and j<n and k<n:
  if d[i+k]==d[j+k]:k+=1;continue
  if d[i+k]>d[j+k]:i+=k+1
  else:j+=k+1
  if i==j:j+=1
  k=0
 print(min(i,j))''',[("baca\n","3"),("aaaa\n","0"),("cba\n","2"),("abab\n","0"),("zxy\n","1"),("bba\n","2")],"The rotations are baca, acab, caba, and abac; abac starts at three.")
add(367,"Stable Burrows-Wheeler transform",["strings","burrows-wheeler-transform"],"Read a nonempty printable-ASCII string without a sentinel. Stably sort its cyclic rotations, breaking equal rotations by their start index. Print the original rotation's zero-based rank, then the last column.",["1 <= length <= 10,000","Characters are printable ASCII (code points 32 through 126); the input has no trailing-space data","No sentinel is appended; duplicate rotations use ascending start indices as their tie-breaker"],["Sort cyclic shifts by doubling their compared length.","Assign equal pairs the same rank.","The last column character for start i is s[(i-1) mod n]."],"O(n log^2 n) time and O(n) auxiliary space",'''def solve():
 s=input();n=len(s);rank=[ord(c) for c in s];order=sorted(range(n),key=lambda i:(rank[i],i));step=1
 while step<n:
  order.sort(key=lambda i:(rank[i],rank[(i+step)%n],i));new=[0]*n
  for j in range(1,n):new[order[j]]=new[order[j-1]]+((rank[order[j]],rank[(order[j]+step)%n])!=(rank[order[j-1]],rank[(order[j-1]+step)%n]))
  rank=new;step*=2
 primary=order.index(0);print(primary);print(''.join(s[(i-1)%n] for i in order))''',[("banana\n","3\nnnbaaa"),("aaaa\n","0\naaaa"),("aba\n","1\nbaa"),("z\n","0\nz"),("baba\n","2\nbbaa"),("abcd\n","0\ndabc")],"The original banana rotation has rank three and contributes the last column nnbaaa.")
add(368,"Linear greedy wildcard glob match",["strings","wildcards"],"Read text then pattern on separate lines. In the pattern, ? matches one character and * matches any sequence (including empty); all other characters match themselves. Print YES or NO.",["0 <= text length, pattern length <= 200,000","Text characters are printable ASCII; pattern characters are printable ASCII plus wildcard meanings for ? and *","The two input lines may be empty; only ? and * are wildcards"],["Advance on equal literal characters or ?.","Remember the latest * and the text position it first covers.","On a mismatch, extend that remembered * by one character."],"O(n + m) time and O(1) auxiliary space",'''def solve():
 text=input();pattern=input();i=j=0;star=-1;mark=0
 while i<len(text):
  if j<len(pattern) and (pattern[j]=='?' or pattern[j]==text[i]):i+=1;j+=1
  elif j<len(pattern) and pattern[j]=='*':star=j;j+=1;mark=i
  elif star>=0:j=star+1;mark+=1;i=mark
  else:print('NO');return
 while j<len(pattern) and pattern[j]=='*':j+=1
 print('YES' if j==len(pattern) else 'NO')''',[("adceb\n*a*b\n","YES"),("acdcb\na*c?b\n","NO"),("\n*\n","YES"),("abc\na?c\n","YES"),("abc\n***\n","YES"),("abc\na*d\n","NO")],"The star can cover dce, leaving a and b as literals.")
PYTHON_CURATED_364_368=ITEMS
