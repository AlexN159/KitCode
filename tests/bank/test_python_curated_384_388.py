from __future__ import annotations
from collections import Counter
from pathlib import Path
import re,subprocess,sys,tempfile
from backend.exercise_bank import EXERCISES
from backend.python_curated_384_388 import PYTHON_CURATED_384_388
def norm(x):return re.sub('[^a-z0-9]','',str(x).casefold())
def test_schema_ids_and_collisions():
 x=PYTHON_CURATED_384_388;assert [z['id']for z in x]==[f'python-curated-{i:03d}'for i in range(384,389)];assert Counter(z['difficulty']for z in x)=={'Hard':5}
 current_ids={z['id'] for z in x};old=[z for z in EXERCISES.values()if z.get('language')=='python' and z['id'] not in current_ids]
 for z in x:assert len(z['hints'])>=3 and(len(z['public_tests']),len(z['hidden_tests']))==(2,4)
 for f in ('title','description','solution'):assert not({norm(z[f])for z in x}&{norm(z[f])for z in old})
def test_all_references():
 with tempfile.TemporaryDirectory()as d:
  p=Path(d)/'r.py';k=0
  for z in PYTHON_CURATED_384_388:
   p.write_text(z['solution'])
   for c in z['public_tests']+z['hidden_tests']:
    r=subprocess.run([sys.executable,'-I',str(p)],input=c['input'],text=True,capture_output=True,timeout=3);assert r.returncode==0,r.stderr;assert r.stdout.rstrip()==c['expected_output'].rstrip();k+=1
  assert k==30
