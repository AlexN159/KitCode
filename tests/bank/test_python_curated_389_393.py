from collections import Counter
from pathlib import Path
import subprocess,sys,tempfile
from backend.python_curated_389_393 import PYTHON_CURATED_389_393
def test_schema_and_references():
 x=PYTHON_CURATED_389_393;assert [z['id']for z in x]==[f'python-curated-{i:03d}'for i in range(389,394)];assert Counter(z['difficulty']for z in x)=={'Hard':5}
 for z in x:assert len(z['hints'])>=3 and(len(z['public_tests']),len(z['hidden_tests']))==(2,4)
 with tempfile.TemporaryDirectory()as d:
  p=Path(d)/'r.py';k=0
  for z in x:
   p.write_text(z['solution'])
   for c in z['public_tests']+z['hidden_tests']:
    r=subprocess.run([sys.executable,'-I',str(p)],input=c['input'],text=True,capture_output=True,timeout=3);assert r.returncode==0,r.stderr;assert r.stdout.rstrip()==c['expected_output'].rstrip();k+=1
  assert k==30


def test_de_bruijn_maximum_stays_inside_the_local_output_limit():
 item=next(z for z in PYTHON_CURATED_389_393 if z['id']=='python-curated-392')
 assert any('k <= 14' in constraint for constraint in item['constraints'])
 with tempfile.TemporaryDirectory() as directory:
  program=Path(directory)/'solution.py';program.write_text(item['solution'],encoding='utf-8')
  result=subprocess.run([sys.executable,'-I',str(program)],input='14\n',text=True,capture_output=True,timeout=3)
 assert result.returncode==0,result.stderr
 cycle=result.stdout.strip();assert len(cycle)==1<<14 and cycle.startswith('0'*14)
