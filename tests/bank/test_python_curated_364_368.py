"""Release gates for audited Hard string exercises 364--368."""
from __future__ import annotations

from collections import Counter
import importlib
from pathlib import Path
import re
import subprocess
import sys
import tempfile

from backend.exercise_bank import EXERCISES
from backend.python_curated_364_368 import PYTHON_CURATED_364_368

SOURCE=Path("backend/python_curated_364_368.py")
REQUIRED={"id","language","title","difficulty","topics","practice_frequency","description","constraints","hints","expected_complexity","starter_code","solution","examples","public_tests","hidden_tests"}

def normalise(value):
 return re.sub(r"[^a-z0-9]","",str(value).casefold())

def nearby_items():
 found=[]
 for path in Path("backend").glob("python_curated_*.py"):
  numbers=[int(x) for x in re.findall(r"\d+",path.stem)]
  if not numbers or max(numbers)<354 or min(numbers)>363:continue
  module=importlib.import_module("backend."+path.stem)
  for value in vars(module).values():
   if isinstance(value,list) and value and all(isinstance(x,dict) and "id" in x for x in value):found.extend(value)
 return found

def test_exact_ids_hard_difficulty_and_schema():
 items=PYTHON_CURATED_364_368
 assert [x["id"] for x in items]==[f"python-curated-{n:03d}" for n in range(364,369)]
 assert Counter(x["difficulty"] for x in items)=={"Hard":5}
 assert len({normalise(x["title"]) for x in items})==5
 for item in items:
  assert REQUIRED <= item.keys()
  assert item["language"]=="python" and len(item["hints"])>=3
  assert len(item["public_tests"])==2 and len(item["hidden_tests"])==4
  assert item["description"] and item["constraints"] and item["expected_complexity"]
  fixtures=item["public_tests"]+item["hidden_tests"]
  assert len({(x["input"],x["expected_output"]) for x in fixtures})==6

def test_every_reference_runs_in_an_isolated_subprocess_against_all_thirty_fixtures():
 with tempfile.TemporaryDirectory() as directory:
  script=Path(directory)/"reference.py"
  count=0
  for item in PYTHON_CURATED_364_368:
   script.write_text(item["solution"],encoding="utf-8")
   for fixture in item["public_tests"]+item["hidden_tests"]:
    result=subprocess.run([sys.executable,"-I",str(script)],input=fixture["input"],text=True,capture_output=True,timeout=3)
    assert result.returncode==0,result.stderr
    assert result.stdout.rstrip()==fixture["expected_output"].rstrip()
    count+=1
  assert count==30

def test_normalised_title_description_and_reference_do_not_collide_with_catalogue_or_nearby_modules():
 current=PYTHON_CURATED_364_368;current_ids={x["id"] for x in current}
 prior=[x for x in EXERCISES.values() if x.get("language")=="python"]+nearby_items()
 prior=[x for x in prior if x.get("id") not in current_ids]
 for field in ("title","description","solution"):
  values=[normalise(x[field]) for x in current]
  assert len(values)==len(set(values)),field
  assert not (set(values)&{normalise(x[field]) for x in prior}),field

def test_source_stays_data_only_and_ascii():
 source=SOURCE.read_text(encoding="utf-8")
 assert "PYTHON_CURATED_364_368=ITEMS" in source
 assert "exercise_bank" not in source
 assert all(ord(char)<128 for char in source)
