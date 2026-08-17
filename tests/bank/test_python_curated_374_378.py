"""Release gates for audited Hard DP and optimization exercises 374--378."""
from __future__ import annotations

from collections import Counter
import importlib
from pathlib import Path
import re
import subprocess
import sys
import tempfile

from backend.exercise_bank import EXERCISES
from backend.python_curated_374_378 import PYTHON_CURATED_374_378

SOURCE=Path("backend/python_curated_374_378.py")
REQUIRED={"id","language","title","difficulty","topics","practice_frequency","description","constraints","hints","expected_complexity","starter_code","solution","examples","public_tests","hidden_tests"}

def normalise(value):return re.sub(r"[^a-z0-9]","",str(value).casefold())
def external_items():
 result=[]
 for name in ("python_curated_354_358","python_curated_364_368","python_curated_369_373"):
  try:module=importlib.import_module("backend."+name)
  except Exception:continue
  for value in vars(module).values():
   if isinstance(value,list) and value and all(isinstance(x,dict) and "id" in x for x in value):result.extend(value)
 return result

def test_exact_ids_schema_and_hard_difficulty():
 items=PYTHON_CURATED_374_378
 assert [x["id"] for x in items]==[f"python-curated-{n:03d}" for n in range(374,379)]
 assert Counter(x["difficulty"] for x in items)=={"Hard":5}
 assert len({normalise(x["title"]) for x in items})==5
 for item in items:
  assert REQUIRED <= item.keys() and item["language"]=="python"
  assert len(item["hints"])>=3 and len(item["public_tests"])==2 and len(item["hidden_tests"])==4
  assert item["description"] and item["constraints"] and item["expected_complexity"]
  assert len({(x["input"],x["expected_output"]) for x in item["public_tests"]+item["hidden_tests"]})==6

def test_every_reference_runs_in_isolation_for_all_thirty_cases():
 with tempfile.TemporaryDirectory() as directory:
  path=Path(directory)/"reference.py";count=0
  for item in PYTHON_CURATED_374_378:
   path.write_text(item["solution"],encoding="utf-8")
   for fixture in item["public_tests"]+item["hidden_tests"]:
    result=subprocess.run([sys.executable,"-I",str(path)],input=fixture["input"],text=True,capture_output=True,timeout=3)
    assert result.returncode==0,result.stderr
    assert result.stdout.rstrip()==fixture["expected_output"].rstrip()
    count+=1
  assert count==30

def test_normalised_titles_descriptions_and_references_do_not_collide_across_modules():
 current=PYTHON_CURATED_374_378;ids={x["id"] for x in current}
 prior=[x for x in EXERCISES.values() if x.get("language")=="python"]+external_items()
 for field in ("title","description","solution"):
  values=[normalise(x[field]) for x in current]
  assert len(values)==len(set(values)),field
  assert not (set(values)&{normalise(x[field]) for x in prior if x.get("id") not in ids}),field

def test_source_is_ascii_data_only():
 source=SOURCE.read_text(encoding="utf-8")
 assert "PYTHON_CURATED_374_378=ITEMS" in source and "exercise_bank" not in source
 assert all(ord(char)<128 for char in source)
