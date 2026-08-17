"""Release gates for audited Hard Python graph exercises 354--358."""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import re
import subprocess
import sys
import tempfile

from backend.exercise_bank import EXERCISES
from backend.python_curated_354_358 import PYTHON_CURATED_354_358

SOURCE=Path("backend/python_curated_354_358.py")
REQUIRED={"id","language","title","difficulty","topics","practice_frequency","description","constraints","hints","expected_complexity","starter_code","solution","examples","public_tests","hidden_tests"}

def normalise(value):
 return re.sub(r"[^a-z0-9]","",str(value).casefold())

def test_exact_ids_hard_difficulty_and_schema():
 items=PYTHON_CURATED_354_358
 assert [x["id"] for x in items]==[f"python-curated-{n:03d}" for n in range(354,359)]
 assert Counter(x["difficulty"] for x in items)=={"Hard":5}
 assert len({normalise(x["title"]) for x in items})==5
 for item in items:
  assert REQUIRED <= item.keys()
  assert item["language"]=="python"
  assert len(item["hints"])>=3
  assert len(item["public_tests"])==2 and len(item["hidden_tests"])==4
  assert item["description"] and item["constraints"] and item["expected_complexity"]
  fixtures=item["public_tests"]+item["hidden_tests"]
  assert len({(x["input"],x["expected_output"]) for x in fixtures})==6
  assert item["examples"]==[{"input":fixtures[0]["input"],"output":fixtures[0]["expected_output"],"explanation":item["examples"][0]["explanation"]}]

def test_every_reference_runs_in_an_isolated_subprocess_against_every_fixture():
 with tempfile.TemporaryDirectory() as directory:
  script=Path(directory)/"reference.py"
  for item in PYTHON_CURATED_354_358:
   script.write_text(item["solution"],encoding="utf-8")
   for fixture in item["public_tests"]+item["hidden_tests"]:
    result=subprocess.run([sys.executable,"-I",str(script)],input=fixture["input"],text=True,capture_output=True,timeout=3)
    assert result.returncode==0,result.stderr
    assert result.stdout.rstrip()==fixture["expected_output"].rstrip()

def test_normalised_title_description_and_reference_do_not_collide_with_catalogue():
 current=PYTHON_CURATED_354_358
 prior=[x for x in EXERCISES.values() if x.get("language")=="python" and x.get("id") not in {y["id"] for y in current}]
 for field in ("title","description","solution"):
  values=[normalise(x[field]) for x in current]
  assert len(values)==len(set(values)),field
  assert not (set(values)&{normalise(x[field]) for x in prior}),field

def test_source_stays_a_small_data_only_module():
 source=SOURCE.read_text(encoding="utf-8")
 assert "PYTHON_CURATED_354_358=ITEMS" in source
 assert "exercise_bank" not in source
 assert all(ord(char)<128 for char in source)
