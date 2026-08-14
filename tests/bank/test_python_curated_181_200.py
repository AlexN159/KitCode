"""Release gates for the final Python curriculum tranche."""
from __future__ import annotations
import ast
from collections import Counter
from contextlib import redirect_stdout
from functools import lru_cache
import io
import itertools
from pathlib import Path
import random
import re
import subprocess
import sys
import tempfile
import unittest

from backend.python_curated_181_200 import PYTHON_CURATED_181_200
from backend.exercise_bank import EXERCISES

SOURCE=Path("backend/python_curated_181_200.py")
CONCEPTS={
181:"trie-autocomplete",182:"suffix-array-occurrences",183:"rabin-karp-overlaps",
184:"longest-palindrome-length",185:"dinic-flow",186:"dag-shortest-path",
187:"condensation-sources",188:"tree-lca-queries",189:"kth-ancestor",
190:"subtree-range-add",191:"rollback-connectivity",192:"strict-convex-hull",
193:"closest-pair-squared",194:"interval-overlap",195:"meet-middle-closest-sum",
196:"lexicographic-lcs",197:"optimal-bst",198:"circular-stone-merge",
199:"four-by-four-sudoku",200:"minimum-interval-stabbing"}

def run_reference(number,input_text):
 exercise=PYTHON_CURATED_181_200[number-181]
 namespace={"__name__":"audit_reference"};exec(compile(exercise["solution"],exercise["id"],"exec"),namespace)
 lines=iter(input_text.split("\n"));out=io.StringIO()
 import builtins
 original=builtins.input;builtins.input=lambda prompt="":next(lines)
 try:
  with redirect_stdout(out):namespace["solve"]()
 finally:builtins.input=original
 return out.getvalue().rstrip()

class FinalPythonTrancheTests(unittest.TestCase):
 def test_metadata_contract(self):
  x=PYTHON_CURATED_181_200
  self.assertEqual([a['id'] for a in x],[f'python-curated-{i:03d}' for i in range(181,201)])
  self.assertEqual(len(CONCEPTS),20);self.assertEqual(len(set(CONCEPTS.values())),20)
  self.assertEqual(len({re.sub(r'[^a-z0-9]','',a['title'].lower()) for a in x}),20)
  self.assertEqual(Counter(a['difficulty'] for a in x),{'Medium':5,'Hard':15})
  for a in x:
   self.assertEqual((len(a['public_tests']),len(a['hidden_tests'])),(2,4));self.assertEqual(len(a['hints']),3)
   self.assertTrue(a['description'] and a['constraints'] and a['expected_complexity'])
   self.assertEqual(len({(z['input'],z['expected_output']) for z in a['public_tests']+a['hidden_tests']}),6)
 def test_source_is_literal_data(self):
  s=SOURCE.read_text(encoding='utf-8');self.assertFalse(any(ord(c)>127 for c in s));tree=ast.parse(s)
  self.assertNotIn("setrecursionlimit",s);self.assertNotIn(".replace(",s)
  calls=[x.value for x in tree.body if isinstance(x,ast.Expr) and isinstance(x.value,ast.Call) and isinstance(x.value.func,ast.Name) and x.value.func.id=='add']
  self.assertEqual(len(calls),20)
  for c in calls:
   self.assertIsInstance(c.args[9],ast.List);self.assertEqual(len(c.args[9].elts),6)

 def test_no_exact_title_or_source_reuse_from_python_1_through_180(self):
  prior=[x for x in EXERCISES.values() if x.get('language')=='python' and x['id'] not in {a['id'] for a in PYTHON_CURATED_181_200}]
  current_titles={re.sub(r'[^a-z0-9]','',x['title'].casefold()) for x in PYTHON_CURATED_181_200}
  prior_titles={re.sub(r'[^a-z0-9]','',x['title'].casefold()) for x in prior}
  self.assertFalse(current_titles & prior_titles)
  normalize=lambda source:re.sub(r'\s+','',source)
  self.assertFalse({normalize(x['solution']) for x in PYTHON_CURATED_181_200} & {normalize(x['solution']) for x in prior})
 def test_all_120_isolated_references(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'reference.py'
   for a in PYTHON_CURATED_181_200:
    p.write_text(a['solution'],encoding='utf-8')
    for case in a['public_tests']+a['hidden_tests']:
     r=subprocess.run([sys.executable,'-I',str(p)],input=case['input'],text=True,capture_output=True,timeout=3)
     self.assertEqual(r.returncode,0,r.stderr);self.assertEqual(r.stdout.rstrip(),case['expected_output'].rstrip())

 def test_output_contracts_are_bounded(self):
  by={x['id']:x for x in PYTHON_CURATED_181_200}
  for number in (181,182,183,188,189,190,191):
   text=' '.join(by[f'python-curated-{number:03d}']['constraints']).lower()
   self.assertTrue(any(token in text for token in ('output','reported','occurrence','get','ask','query cap')),number)

 def test_condensation_source_uses_iterative_traversal_at_max_depth(self):
  n=100_000
  payload=f'{n} {n-1}\n'+''.join(f'{i} {i+1}\n' for i in range(n-1))
  self.assertEqual(run_reference(187,payload),'1')

 def test_random_graph_algorithms_against_small_independent_oracles(self):
  rng=random.Random(181200)
  for _ in range(35):
   n=rng.randint(2,6);edges=[]
   for a in range(n):
    for b in range(n):
     if a!=b and rng.random()<.25:edges.append((a,b,rng.randint(0,8)))
   payload=f'{n} {len(edges)} 0 {n-1}\n'+''.join(f'{a} {b} {c}\n' for a,b,c in edges)
   expected=min((sum(c for a,b,c in edges if (mask>>a)&1 and not((mask>>b)&1))
                 for mask in range(1<<n) if mask&1 and not(mask>>(n-1)&1)),default=0)
   self.assertEqual(run_reference(185,payload),str(expected))

   dag=[(a,b,rng.randint(-8,8)) for a in range(n) for b in range(a+1,n) if rng.random()<.35]
   dist=[None]*n;dist[0]=0
   for a in range(n):
    if dist[a] is not None:
     for u,v,w in dag:
      if u==a and (dist[v] is None or dist[a]+w<dist[v]):dist[v]=dist[a]+w
   payload=f'{n} {len(dag)} 0 {n-1}\n'+''.join(f'{a} {b} {w}\n' for a,b,w in dag)
   self.assertEqual(run_reference(186,payload),str(dist[-1]) if dist[-1] is not None else 'IMPOSSIBLE')

   directed=[(a,b) for a in range(n) for b in range(n) if rng.random()<.2]
   reach=[[i==j for j in range(n)]for i in range(n)]
   for a,b in directed:reach[a][b]=True
   for k in range(n):
    for i in range(n):
     if reach[i][k]:
      for j in range(n):reach[i][j]|=reach[k][j]
   comp=[-1]*n;k=0
   for i in range(n):
    if comp[i]>=0:continue
    for j in range(n):
     if reach[i][j] and reach[j][i]:comp[j]=k
    k+=1
   incoming=[False]*k
   for a,b in directed:
    if comp[a]!=comp[b]:incoming[comp[b]]=True
   payload=f'{n} {len(directed)}\n'+''.join(f'{a} {b}\n' for a,b in directed)
   self.assertEqual(run_reference(187,payload),str(incoming.count(False)))

 def test_random_tree_structures_against_naive_models(self):
  rng=random.Random(188191)
  for _ in range(30):
   n=rng.randint(1,18);parent=[-1]+[rng.randrange(i) for i in range(1,n)]
   pairs=[(rng.randrange(n),rng.randrange(n))for _ in range(20)]
   def lca(a,b):
    ancestors=set()
    while a>=0:ancestors.add(a);a=parent[a]
    while b not in ancestors:b=parent[b]
    return b
   payload=f'{n}\n'+''.join(f'{parent[i]} {i}\n' for i in range(1,n))+f'{len(pairs)}\n'+''.join(f'{a} {b}\n' for a,b in pairs)
   self.assertEqual(run_reference(188,payload),'\n'.join(map(str,(lca(a,b)for a,b in pairs))))
   queries=[(rng.randrange(n),rng.randrange(n+3))for _ in range(20)]
   expected=[]
   for v,k in queries:
    for _ in range(k):v=parent[v] if v>=0 else -1
    expected.append(v)
   payload=f'{n}\n'+ ' '.join(map(str,parent))+f'\n{len(queries)}\n'+''.join(f'{v} {k}\n' for v,k in queries)
   self.assertEqual(run_reference(189,payload),'\n'.join(map(str,expected)))

   values=[rng.randint(-5,5)for _ in range(n)];current=values[:];ops=[];answers=[]
   for _ in range(35):
    v=rng.randrange(n)
    if rng.random()<.6:
     delta=rng.randint(-4,4);ops.append(f'ADD {v} {delta}')
     for u in range(n):
      x=u
      while x>=0 and x!=v:x=parent[x]
      if x==v:current[u]+=delta
    else:ops.append(f'GET {v}');answers.append(current[v])
   payload=f'{n}\n'+ ' '.join(map(str,parent))+'\n'+' '.join(map(str,values))+f'\n{len(ops)}\n'+'\n'.join(ops)+'\n'
   self.assertEqual(run_reference(190,payload),'\n'.join(map(str,answers)))

 def test_random_rollback_geometry_subset_and_dp_oracles(self):
  rng=random.Random(192198)
  for _ in range(35):
   n=rng.randint(2,10);edges=[];snapshots=[];ops=[];answers=[]
   for __ in range(30):
    choice=rng.random()
    if choice<.45:
     a,b=rng.randrange(n),rng.randrange(n);edges.append((a,b));ops.append(f'ADD {a} {b}')
    elif choice<.58:
     snapshots.append(len(edges));ops.append('SNAP')
    elif choice<.70 and snapshots:
     edges=edges[:snapshots.pop()];ops.append('ROLL')
    else:
     a,b=rng.randrange(n),rng.randrange(n);seen={a};stack=[a]
     while stack:
      u=stack.pop()
      for x,y in edges:
       if x==u and y not in seen:seen.add(y);stack.append(y)
       if y==u and x not in seen:seen.add(x);stack.append(x)
     ops.append(f'ASK {a} {b}');answers.append('YES' if b in seen else 'NO')
   payload=f'{n}\n{len(ops)}\n'+'\n'.join(ops)+'\n'
   self.assertEqual(run_reference(191,payload),'\n'.join(answers))

   points=[]
   while len(points)<rng.randint(2,10):
    p=(rng.randint(-8,8),rng.randint(-8,8))
    if p not in points:points.append(p)
   brute=min((a-c)**2+(b-d)**2 for i,(a,b) in enumerate(points) for c,d in points[i+1:])
   payload=f'{len(points)}\n'+''.join(f'{a} {b}\n' for a,b in points)
   self.assertEqual(run_reference(193,payload),str(brute))

   vals=[rng.randint(-9,9)for _ in range(rng.randint(1,14))];target=rng.randint(-20,20)
   sums=[sum(vals[i]for i in range(len(vals))if mask>>i&1)for mask in range(1<<len(vals))]
   best=min(sums,key=lambda x:(abs(x-target),x))
   payload=f'{len(vals)} {target}\n'+' '.join(map(str,vals))+'\n'
   self.assertEqual(run_reference(195,payload),str(best))

   a=''.join(rng.choice('abc')for _ in range(rng.randint(0,8)));b=''.join(rng.choice('abc')for _ in range(rng.randint(0,8)))
   candidates={''.join(a[i]for i in range(len(a))if mask>>i&1)for mask in range(1<<len(a))}
   common=[s for s in candidates if iter_subsequence(s,b)]
   expected=min(common,key=lambda s:(-len(s),s))
   self.assertEqual(run_reference(196,f'{a}\n{b}\n'),expected)

   stones=tuple(rng.randint(0,7)for _ in range(rng.randint(2,7)))
   @lru_cache(None)
   def merge(state):
    if len(state)==1:return 0
    options=[]
    for i in range(len(state)):
     j=(i+1)%len(state);cost=state[i]+state[j]
     nxt=(cost,)+state[1:-1] if j==0 else state[:i]+(cost,)+state[j+1:]
     options.append(cost+merge(nxt))
    return min(options)
   payload=f'{len(stones)}\n'+' '.join(map(str,stones))+'\n'
   self.assertEqual(run_reference(198,payload),str(merge(stones)))

 def test_random_string_hull_and_interval_algorithms_against_naive_oracles(self):
  rng=random.Random(181184200)
  for _ in range(30):
   words=set()
   while len(words)<rng.randint(1,12):words.add(''.join(rng.choice('abc')for _ in range(rng.randint(1,6))))
   words=list(words);prefixes=[''.join(rng.choice('abc')for _ in range(rng.randint(1,4)))for __ in range(8)]
   expected=[]
   for prefix in prefixes:
    matches=sorted((w for w in words if w.startswith(prefix)),key=lambda w:(len(w),w))[:3]
    expected.append(' '.join(matches) if matches else '-')
   payload=f'{len(words)}\n'+'\n'.join(words)+f'\n{len(prefixes)}\n'+'\n'.join(prefixes)+'\n'
   self.assertEqual(run_reference(181,payload),'\n'.join(expected))

   text=''.join(rng.choice('abc')for _ in range(rng.randint(1,28)))
   patterns=[''.join(rng.choice('abc')for _ in range(rng.randint(1,7)))for __ in range(8)]
   lines=[]
   for pattern in patterns:
    starts=[i for i in range(len(text)-len(pattern)+1)if text.startswith(pattern,i)]
    lines.append((str(len(starts))+' '+' '.join(map(str,starts))).rstrip() if starts else '0')
   payload=text+f'\n{len(patterns)}\n'+'\n'.join(patterns)+'\n'
   self.assertEqual(run_reference(182,payload),'\n'.join(lines))
   pattern=rng.choice(patterns)
   if len(pattern)>len(text):pattern=text[:rng.randint(1,len(text))]
   starts=[i for i in range(len(text)-len(pattern)+1)if text.startswith(pattern,i)]
   expected=' '.join(map(str,starts)) if starts else '-'
   self.assertEqual(run_reference(183,f'{text}\n{pattern}\n'),expected)
   best=max((j-i for i in range(len(text))for j in range(i+1,len(text)+1)if text[i:j]==text[i:j][::-1]),default=0)
   self.assertEqual(run_reference(184,text+'\n'),str(best))

   points=[]
   while len(points)<rng.randint(3,11):
    point=(rng.randint(-7,7),rng.randint(-7,7))
    if point not in points:points.append(point)
   start=min(points);hull=[];current=start
   while True:
    hull.append(current);candidate=next(p for p in points if p!=current)
    for point in points:
     if point==current:continue
     cross=(candidate[0]-current[0])*(point[1]-current[1])-(candidate[1]-current[1])*(point[0]-current[0])
     dc=(candidate[0]-current[0])**2+(candidate[1]-current[1])**2
     dp=(point[0]-current[0])**2+(point[1]-current[1])**2
     if cross>0 or cross==0 and dp>dc:candidate=point
    current=candidate
    if current==start:break
   payload=f'{len(points)}\n'+''.join(f'{x} {y}\n' for x,y in points)
   self.assertEqual(run_reference(192,payload),str(len(hull)))

   intervals=[]
   for __ in range(rng.randint(1,8)):
    left=rng.randint(-5,4);right=rng.randint(left+1,6);intervals.append((left,right))
   overlap=max(sum(left<=x<right for left,right in intervals)for x in range(-5,7))
   payload=f'{len(intervals)}\n'+''.join(f'{a} {b}\n' for a,b in intervals)
   self.assertEqual(run_reference(194,payload),str(overlap))

   closed=[]
   for __ in range(rng.randint(1,8)):
    left=rng.randint(-4,4);right=rng.randint(left,5);closed.append((left,right))
   candidates=sorted({right for _,right in closed});opt=len(closed)
   for size in range(len(candidates)+1):
    if any(all(any(left<=point<=right for point in chosen)for left,right in closed)
           for chosen in itertools.combinations(candidates,size)):
     opt=size;break
   payload=f'{len(closed)}\n'+''.join(f'{a} {b}\n' for a,b in closed)
   self.assertEqual(run_reference(200,payload),str(opt))

 def test_random_optimal_bst_against_interval_oracle(self):
  rng=random.Random(197)
  for _ in range(40):
   frequencies=tuple(rng.randint(1,9)for __ in range(rng.randint(1,8)))
   prefix=[0]
   for value in frequencies:prefix.append(prefix[-1]+value)
   @lru_cache(None)
   def oracle(left,right):
    if left>right:return 0
    weight=prefix[right+1]-prefix[left]
    return weight+min(oracle(left,root-1)+oracle(root+1,right)for root in range(left,right+1))
   payload=f'{len(frequencies)}\n'+' '.join(map(str,frequencies))+'\n'
   self.assertEqual(run_reference(197,payload),str(oracle(0,len(frequencies)-1)))

def iter_subsequence(needle,haystack):
 it=iter(haystack)
 return all(any(c==x for x in it) for c in needle)
