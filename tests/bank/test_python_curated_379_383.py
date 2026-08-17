"""Release gates for Hard data-structure exercises 379--383."""
from __future__ import annotations
from collections import Counter
from pathlib import Path
import re,subprocess,sys,tempfile
from backend.exercise_bank import EXERCISES
from backend.python_curated_379_383 import PYTHON_CURATED_379_383
SOURCE=Path('backend/python_curated_379_383.py')
REQ={'id','language','title','difficulty','topics','practice_frequency','description','constraints','hints','expected_complexity','starter_code','solution','examples','public_tests','hidden_tests'}
def norm(x):return re.sub('[^a-z0-9]','',str(x).casefold())
def test_ids_schema_and_difficulty():
 x=PYTHON_CURATED_379_383;assert [a['id'] for a in x]==[f'python-curated-{i:03d}'for i in range(379,384)]
 assert Counter(a['difficulty']for a in x)=={'Hard':5} and len({norm(a['title'])for a in x})==5
 for a in x:assert REQ<=a.keys() and a['language']=='python' and len(a['hints'])>=3 and (len(a['public_tests']),len(a['hidden_tests']))==(2,4) and len({(z['input'],z['expected_output'])for z in a['public_tests']+a['hidden_tests']})==6
def test_all_thirty_isolated_fixtures():
 with tempfile.TemporaryDirectory()as d:
  p=Path(d)/'r.py';total=0
  for a in PYTHON_CURATED_379_383:
   p.write_text(a['solution'])
   for z in a['public_tests']+a['hidden_tests']:
    r=subprocess.run([sys.executable,'-I',str(p)],input=z['input'],text=True,capture_output=True,timeout=3);assert r.returncode==0,r.stderr;assert r.stdout.rstrip()==z['expected_output'].rstrip();total+=1
  assert total==30
def test_normalised_collision_audit_and_source():
 cur=PYTHON_CURATED_379_383;current_ids={a['id'] for a in cur};old=[a for a in EXERCISES.values()if a.get('language')=='python' and a['id'] not in current_ids]
 for field in ('title','description','solution'):
  v=[norm(a[field])for a in cur];assert len(v)==len(set(v));assert not(set(v)&{norm(a[field])for a in old})
 s=SOURCE.read_text();assert 'PYTHON_CURATED_379_383=ITEMS'in s and 'exercise_bank'not in s and all(ord(c)<128 for c in s)
