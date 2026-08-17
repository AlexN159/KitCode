"""Independent seeded audit for the Hard curated range 354--393."""
from __future__ import annotations
from collections import Counter
import io,random,re,itertools
from contextlib import redirect_stdout
from backend.exercise_bank import EXERCISES
from backend.python_curated_354_358 import PYTHON_CURATED_354_358
from backend.python_curated_359_363 import PYTHON_CURATED_359_363
from backend.python_curated_364_368 import PYTHON_CURATED_364_368
from backend.python_curated_369_373 import PYTHON_CURATED_369_373
from backend.python_curated_374_378 import PYTHON_CURATED_374_378
from backend.python_curated_379_383 import PYTHON_CURATED_379_383
from backend.python_curated_384_388 import PYTHON_CURATED_384_388
from backend.python_curated_389_393 import PYTHON_CURATED_389_393
ALL=PYTHON_CURATED_354_358+PYTHON_CURATED_359_363+PYTHON_CURATED_364_368+PYTHON_CURATED_369_373+PYTHON_CURATED_374_378+PYTHON_CURATED_379_383+PYTHON_CURATED_384_388+PYTHON_CURATED_389_393
def run(i,payload):
 x=ALL[i-354];ns={'__name__':'audit'};exec(compile(x['solution'],x['id'],'exec'),ns);old=__import__('builtins').input;it=iter(payload.split('\n'));__import__('builtins').input=lambda:next(it);o=io.StringIO()
 try:
  with redirect_stdout(o):ns['solve']()
 finally:__import__('builtins').input=old
 return o.getvalue().rstrip()
def norm(x):return re.sub('[^a-z0-9]','',x.casefold())
def test_contiguous_hard_unique_audit():
 assert [x['id']for x in ALL]==[f'python-curated-{i:03d}'for i in range(354,394)] and Counter(x['difficulty']for x in ALL)=={'Hard':40}
 old=[x for x in EXERCISES.values()if x.get('language')=='python' and x['id']<'python-curated-201']
 for f in ('title','description','solution'):
  v=[norm(x[f])for x in ALL];assert len(v)==len(set(v));assert not(set(v)&{norm(x[f])for x in old})
 for x in ALL:assert len(x['hints'])>=3 and len(x['public_tests'])==2 and len(x['hidden_tests'])==4

def test_runner_safe_hard_contract_caps():
 """The desktop runner accepts modest inputs and captures at most about 24 KiB."""
 by_id={int(x['id'].rsplit('-',1)[1]):x for x in ALL}
 expected={
  360:('n,q <= 500','At most 500 commands are SUM'),
  361:('n,q <= 700','12,000 characters'),
  362:('q <= 1,000','At most 1,000 commands are QUERY'),
  364:('length of each string <= 1,000',),367:('length <= 10,000',),
  372:('<= 1,500','12,000 characters'),374:('b <= 17','n,q <= 1,000'),
  377:('n <= 30','12,000 characters'),378:('k <= 60','n <= 500'),
  379:('n,q <= 500','At most 500 SUM commands'),380:('n,q <= 600','At most 600 ASK commands'),
  381:('n,m <= 256','At most 500 SUM commands'),382:('n,q <= 500','At most 500 SUM commands'),
  383:('n,q <= 500','At most 500 PATH commands'),384:('L,R <= 800','m <= 1,200'),
  385:('n <= 800','m <= 1,200'),386:('n,q <= 800','At most 800 QUERY commands'),
  387:('n <= 1,000','12,000 characters'),389:('n <= 300','q <= 300'),
 }
 for number,needles in expected.items():
  text=' '.join(by_id[number]['constraints'])
  assert all(needle in text for needle in needles),(number,text)
  assert number in {364,367,378} or '12,000 characters' in text
def test_seeded_small_oracles():
 r=random.Random(354393)
 for _ in range(12):
  a,b,m=r.randrange(6),r.randrange(6),r.choice([3,4,5]);exp=next((x for x in range(60)if x%m==a%m and x%(m+1)==b%(m+1)),None);got=run(369,f'2\n{a} {m}\n{b} {m+1}\n');assert got==(str(exp)if exp is not None else 'IMPOSSIBLE')
 for _ in range(12):
  p=r.choice([5,7,11,13]);a=r.randrange(1,p);b=r.randrange(1,p);exp=next((x for x in range(p)if pow(a,x,p)==b),-1);assert run(370,f'{p} {a} {b}\n')==str(exp)
 for _ in range(12):
  p=r.choice([3,5,7,11,13]);a=r.randrange(p);roots=[x for x in range(p)if x*x%p==a];assert run(371,f'{p} {a}\n')==str(min(roots)if roots else -1)
 for _ in range(10):
  n=4;a=[r.randrange(6)for _ in range(n)];ops=[];cur=a[:];out=[]
  for z in range(6):
   l=r.randrange(n);rr=r.randrange(l,n)
   if r.random()<.5:x=r.randrange(6);ops.append(f'CHMIN {l} {rr} {x}');cur[l:rr+1]=[min(v,x)for v in cur[l:rr+1]]
   else:ops.append(f'SUM {l} {rr}');out.append(sum(cur[l:rr+1]))
  assert run(379,f'{n} 6\n'+ ' '.join(map(str,a))+'\n'+'\n'.join(ops)+'\n')=='\n'.join(map(str,out))
def test_next_five_seeded_oracles():
 r=random.Random(354358361)
 for _ in range(20):
  n=3;edges=[(u,v,r.randrange(3),r.randrange(5))for u in range(n)for v in range(n)if u!=v and r.random()<.45];need=r.randrange(3);best=None
  import itertools
  for f in itertools.product(*[range(c+1)for _,_,c,_ in edges]):
   bal=[0]*n
   for (u,v,_,w),z in zip(edges,f):bal[u]-=z;bal[v]+=z
   if bal[0]==-need and bal[-1]==need and all(bal[i]==0 for i in range(1,n-1)):
    cost=sum(z*e[3]for z,e in zip(f,edges));best=cost if best is None else min(best,cost)
  payload=f'{n} {len(edges)} 0 2 {need}\n'+''.join(f'{u} {v} {c} {w}\n'for u,v,c,w in edges);assert run(354,payload)==str(best if best is not None else -1)
 for _ in range(20):
  n=4;clauses=[(r.choice([-1,1])*r.randrange(1,n+1),r.choice([-1,1])*r.randrange(1,n+1))for __ in range(5)]
  valid=[]
  for bits in itertools.product((0,1),repeat=n):
   if all((bits[abs(a)-1] if a>0 else not bits[-a-1]) or (bits[abs(b)-1] if b>0 else not bits[-b-1])for a,b in clauses):valid.append(bits)
  got=run(355,f'{n} {len(clauses)}\n'+''.join(f'{a} {b}\n'for a,b in clauses))
  assert got==('IMPOSSIBLE'if not valid else ' '.join(map(str,min(valid))))
 for _ in range(20):
  n=4;edges=[(u,v,r.randrange(6))for u in range(n)for v in range(n)if u!=v and r.random()<.45];best=None
  incoming=[[e for e in edges if e[1]==v]for v in range(1,n)]
  for pick in itertools.product(*incoming) if all(incoming) else []:
   parent={v:e[0]for v,e in zip(range(1,n),pick)}
   if all((lambda x: (lambda seen: 0 in seen)(set()))(v) for v in []):pass
   ok=True
   for v in range(1,n):
    seen=set();x=v
    while x and x not in seen:seen.add(x);x=parent.get(x,-1)
    if x!=0:ok=False
   if ok:best=min(best or 10**9,sum(e[2]for e in pick))
  assert run(358,f'{n} {len(edges)} 0\n'+''.join(f'{u} {v} {w}\n'for u,v,w in edges))==str(best if best is not None else -1)
 for _ in range(20):
  n=4;edges=[(u,v)for u in range(n)for v in range(u+1,n)if r.random()<.55];count=0
  for sub in itertools.combinations(range(len(edges)),n-1):
   seen={0};changed=1
   while changed:
    changed=0
    for i in sub:
     a,b=edges[i]
     if (a in seen)^(b in seen):seen|={a,b};changed=1
   count+=len(seen)==n
  assert run(359,f'{n} {len(edges)}\n'+''.join(f'{a} {b}\n'for a,b in edges))==str(count)
 for _ in range(20):
  a=[r.randrange(-4,5)for __ in range(7)];qs=[];out=[]
  for __ in range(5):
   l=r.randrange(7);rr=r.randrange(l,7);k=r.randrange(1,rr-l+2);qs.append((l,rr,k));out.append(sorted(a[l:rr+1])[k-1])
  assert run(361,f'7 5\n'+ ' '.join(map(str,a))+'\n'+''.join(f'{l} {rr} {k}\n'for l,rr,k in qs))=='\n'.join(map(str,out))
def test_geometry_dp_and_query_oracles():
 r=random.Random(363374375377380)
 import itertools
 for _ in range(20):
  rect=[]
  for __ in range(4):
   x=r.randrange(3);y=r.randrange(3);rect.append((x,y,r.randrange(x+1,5),r.randrange(y+1,5)))
  cells={(i,j)for x,y,X,Y in rect for i in range(x,X)for j in range(y,Y)}
  assert run(363,'4\n'+''.join('%s %s %s %s\n'%z for z in rect))==str(len(cells))
 for _ in range(20):
  b=4;vals=[r.randrange(16)for __ in range(8)];qs=[r.randrange(16)for __ in range(5)]
  assert run(374,f'4 8 5\n'+ ' '.join(map(str,vals))+'\n'+''.join(f'{x}\n'for x in qs))=='\n'.join(str(sum(v&x==v for v in vals))for x in qs)
 for _ in range(20):
  n=4;edges=[(u,v,r.randrange(1,6))for u in range(n)for v in range(u+1,n)if r.random()<.55];terms=[0,2];best=None
  for mask in range(1<<len(edges)):
   g=[[]for __ in range(n)];cost=0
   for i,(u,v,w)in enumerate(edges):
    if mask>>i&1:g[u].append(v);g[v].append(u);cost+=w
   seen={terms[0]};st=[terms[0]]
   while st:
    u=st.pop()
    for v in g[u]:
     if v not in seen:seen.add(v);st.append(v)
   if all(x in seen for x in terms):best=min(best,cost)if best is not None else cost
  assert run(375,f'{n} {len(edges)} 2\n0 2\n'+''.join(f'{u} {v} {w}\n'for u,v,w in edges))==str(best if best is not None else -1)
 for _ in range(20):
  n=4;a=[[r.randrange(-5,6)for _ in range(n)]for __ in range(n)];exp=min(sum(a[i][p[i]]for i in range(n))for p in itertools.permutations(range(n)))
  assert run(377,'4\n'+'\n'.join(' '.join(map(str,z))for z in a)+'\n')==str(exp)
 for _ in range(20):
  a=[r.randrange(4)for __ in range(6)];cur=a[:];ops=[];out=[]
  for __ in range(8):
   if r.random()<.5:
    i=r.randrange(6);x=r.randrange(4);ops.append(f'SET {i} {x}');cur[i]=x
   else:
    l=r.randrange(6);rr=r.randrange(l,6);ops.append(f'ASK {l} {rr}');out.append(len(set(cur[l:rr+1])))
  assert run(380,'6 8\n'+' '.join(map(str,a))+'\n'+'\n'.join(ops)+'\n')=='\n'.join(map(str,out))
def test_line_tiling_and_dynamic_structure_oracles():
 r=random.Random(362376381382383)
 for _ in range(20):
  lines=[];ops=[];out=[]
  for j in range(8):
   if not lines or r.random()<.55:m=r.randrange(-4,5);b=r.randrange(-5,6);lines.append((m,b));ops.append(f'ADD {m} {b}')
   else:x=r.randrange(-6,7);ops.append(f'QUERY {x}');out.append(min(m*x+b for m,b in lines))
  assert run(362,'8\n'+'\n'.join(ops)+'\n')=='\n'.join(map(str,out))
 for _ in range(20):
  n=m=3;grid=[''.join('#' if r.random()<.3 else '.'for _ in range(m))for __ in range(n)]
  def f(state):
   try:i=next(i for i,x in enumerate(state)if x=='.')
   except StopIteration:return 1
   x,y=divmod(i,m);z=list(state);z[i]='#';ans=0
   for dx,dy in ((1,0),(0,1)):
    X=x+dx;Y=y+dy
    if X<n and Y<m and z[X*m+Y]=='.':w=z[:];w[X*m+Y]='#';ans+=f(tuple(w))
   return ans
  assert run(376,'3 3\n'+'\n'.join(grid)+'\n')==str(f(tuple(''.join(grid))))
 for _ in range(20):
  a=[[0]*3 for __ in range(3)];ops=[];out=[]
  for __ in range(8):
   if r.random()<.55:x=r.randrange(3);y=r.randrange(3);v=r.randrange(-3,4);a[x][y]+=v;ops.append(f'ADD {x} {y} {v}')
   else:x=r.randrange(3);X=r.randrange(x,3);y=r.randrange(3);Y=r.randrange(y,3);ops.append(f'SUM {x} {y} {X} {Y}');out.append(sum(a[i][j]for i in range(x,X+1)for j in range(y,Y+1)))
  assert run(381,'3 3 8\n'+'\n'.join(ops)+'\n')=='\n'.join(map(str,out))
 for _ in range(20):
  a=[r.randrange(-3,4)for __ in range(6)];cur=a[:];ops=[];out=[]
  for __ in range(8):
   l=r.randrange(6);rr=r.randrange(l,6)
   if r.random()<.5:ops.append(f'REVERSE {l} {rr}');cur[l:rr+1]=cur[l:rr+1][::-1]
   else:ops.append(f'SUM {l} {rr}');out.append(sum(cur[l:rr+1]))
  assert run(382,'6 8\n'+' '.join(map(str,a))+'\n'+'\n'.join(ops)+'\n')=='\n'.join(map(str,out+ [' '.join(map(str,cur))]))
 for _ in range(20):
  val=[r.randrange(-3,4)for __ in range(4)];cur=val[:];ops=['LINK 0 1','LINK 1 2','LINK 2 3'];out=[]
  for __ in range(5):
   if r.random()<.5:i=r.randrange(4);x=r.randrange(-3,4);cur[i]=x;ops.append(f'SET {i} {x}')
   else:u=r.randrange(4);v=r.randrange(4);ops.append(f'PATH {u} {v}');out.append(sum(cur[min(u,v):max(u,v)+1]))
  assert run(383,'4 8\n'+' '.join(map(str,val))+'\n'+'\n'.join(ops)+'\n')=='\n'.join(map(str,out))
def test_final_tree_geometry_and_field_oracles():
 r=random.Random(384393)
 for _ in range(15):
  L=R=3;ed=[(i,j)for i in range(3)for j in range(3)if r.random()<.5];best=max((sum((i,j)in ed for i,j in enumerate(p))for p in itertools.permutations(range(3))),default=0)
  assert run(384,f'3 3 {len(ed)}\n'+''.join(f'{a} {b}\n'for a,b in ed))==str(best)
  # DAG path cover equals n minus the same bipartite matching on forward edges.
  dag=[(i,j)for i in range(4)for j in range(i+1,4)if r.random()<.5];best=max((sum((i,j)in dag for i,j in enumerate(p))for p in itertools.permutations(range(4))),default=0)
  assert run(385,f'4 {len(dag)}\n'+''.join(f'{a} {b}\n'for a,b in dag))==str(4-best)
  pts=[(r.randrange(-4,5),r.randrange(-4,5))for __ in range(5)];pts=list(dict.fromkeys(pts));
  if len(pts)>1:assert run(390,str(len(pts))+'\n'+''.join(f'{x} {y}\n'for x,y in pts))==str(max((x-u)**2+(y-v)**2 for i,(x,y)in enumerate(pts)for u,v in pts[i+1:]))
 for k in range(1,6):
  s=run(392,f'{k}\n');assert len(s)==1<<k and len({(s+s)[i:i+k]for i in range(1<<k)})==1<<k and s.startswith('0'*k)
 # This specifically protects the iterative Euler tour against a recursion-limit
 # regression; a length-1024 cycle is large enough to expose the old failure.
 s=run(392,'10\n');assert len(s)==1<<10 and len({(s+s)[i:i+10]for i in range(1<<10)})==1<<10 and s.startswith('0'*10)
 for _ in range(15):
  p=17;n=3;c=[r.randrange(p)for __ in range(n)];xs=list(range(n));ys=[sum(c[j]*x**j for j in range(n))%p for x in xs];x=r.randrange(p);exp=sum(c[j]*x**j for j in range(n))%p
  assert run(393,f'{p}\n{n}\n'+''.join(f'{u} {v}\n'for u,v in zip(xs,ys))+f'{x}\n')==str(exp)
def test_remaining_final_range_oracles():
 r=random.Random(386387388389391)
 for _ in range(15):
  n=6;edges=[(i,r.randrange(i))for i in range(1,n)];g=[[]for __ in range(n)]
  for a,b in edges:g[a].append(b);g[b].append(a)
  marked={0};ops=[];out=[]
  for __ in range(7):
   v=r.randrange(n)
   if r.random()<.45:marked.add(v);ops.append(f'MARK {v}')
   else:
    d=[-1]*n;d[v]=0;st=[v]
    for x in st:
     for y in g[x]:
      if d[y]<0:d[y]=d[x]+1;st.append(y)
    out.append(min(d[x]for x in marked));ops.append(f'QUERY {v}')
  assert run(386,f'{n} 7\n'+''.join(f'{a} {b}\n'for a,b in edges)+'\n'.join(ops)+'\n')=='\n'.join(map(str,out))
  sums=[]
  for s in range(n):
   d=[-1]*n;d[s]=0;st=[s]
   for x in st:
    for y in g[x]:
     if d[y]<0:d[y]=d[x]+1;st.append(y)
   sums.append(sum(d))
  assert run(387,f'{n}\n'+''.join(f'{a} {b}\n'for a,b in edges))==' '.join(map(str,sums))
  # direct replay bipartite oracle
  active=set();ops=[];out=[]
  for __ in range(8):
   if not active or r.random()<.5:
    a,b=sorted((r.randrange(4),r.randrange(4)));active.add((a,b));ops.append(f'ADD {a} {b}')
   elif r.random()<.5:
    e=next(iter(active));active.remove(e);ops.append(f'REMOVE {e[0]} {e[1]}')
   else:
    col=[-1]*4;ok=1
    for s in range(4):
     if col[s]<0:
      col[s]=0;st=[s]
      for x in st:
       for a,b in active:
        y=b if a==x else a if b==x else None
        if y is not None:
         if col[y]<0:col[y]=col[x]^1;st.append(y)
         elif col[y]==col[x]:ok=0
    ops.append('ASK');out.append('YES'if ok else'NO')
  assert run(391,'4 8\n'+'\n'.join(ops)+'\n')=='\n'.join(out)
def test_isomorphism_and_convex_ray_oracles():
 r=random.Random(388389)
 for _ in range(15):
  n=5;e=[(i,r.randrange(i))for i in range(1,n)];perm=list(range(n));r.shuffle(perm);f=[(perm[a],perm[b])for a,b in e]
  assert run(388,str(n)+'\n'+''.join(f'{a} {b}\n'for a,b in e+f))=='YES'
 for _ in range(15):
  p=[(0,0),(4,0),(4,4),(0,4)];qs=[(r.randrange(-1,6),r.randrange(-1,6))for __ in range(4)];out=[]
  for x,y in qs:
   boundary=(x in (0,4) and 0<=y<=4)or(y in (0,4)and 0<=x<=4)
   out.append('BOUNDARY'if boundary else'INSIDE'if 0<x<4 and 0<y<4 else'OUTSIDE')
  assert run(389,'4\n'+'\n'.join(f'{a} {b}'for a,b in p)+f'\n4\n'+''.join(f'{a} {b}\n'for a,b in qs))=='\n'.join(out)
