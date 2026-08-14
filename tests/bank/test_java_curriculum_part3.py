"""Release gates for Java curriculum records 101--120."""
from __future__ import annotations
import ast
from pathlib import Path
import pytest
from backend import main
from backend.java_curriculum_part1 import JAVA_CURRICULUM_PART1
from backend.java_curriculum_part2 import JAVA_CURRICULUM_PART2
from backend.java_curriculum_part3 import JAVA_CURRICULUM_PART3
from backend.java_practice_bank import JAVA_PRACTICE_EXERCISES
from backend.multilang_bank import MULTILANG_EXERCISES

SOURCE=Path("backend/java_curriculum_part3.py")
CONCEPTS={"majority-vote","missing-number-xor","gcd-lcm","modular-power","list-middle","merge-two-lists","remove-nth-end","cycle-entry","zigzag-level-order","tree-diameter","tree-lca","matrix-membership","running-median","kth-pair-distance","n-queens-count","catalan-count","minimum-word-break","edit-distance","palindrome-cuts","maximal-rectangle"}
PRIOR_CONCEPTS={
 "two-sum","valid-parentheses","longest-unique-substring","minimum-target-window","binary-search-first-target","rotated-search","product-except-self","max-subarray","merge-intervals","meeting-rooms","min-stack","next-greater","daily-warmer","flood-fill","islands","course-schedule","unweighted-shortest-path","tree-height","validate-bst","climb-stairs","coin-change","house-robber","lis","jump-game","gas-station","anagram","group-anagrams","top-k-frequent","kth-largest","queue","spiral-matrix","set-matrix-zeroes","rotate-matrix","word-search","container-water","three-sum","longest-consecutive","rotated-minimum","integer-square-root","decode-ways","partition-labels","reorganize-string","reverse-linked-list","lru","array-sum","array-maximum","array-minimum","count-even","sum-odd","count-positive","array-range","first-plus-last","reverse-array","nondecreasing-array","reverse-text","count-vowels","palindrome-decision","count-words","first-uppercase","count-distinct-integers",
 "sum-positive-values","first-threshold-index","interior-peak-count","stable-move-zeroes","signed-array-rotation","stable-parity-partition","next-permutation","first-vowel-index","longest-repeated-run","word-initials","reverse-word-order","run-length-encode","camel-to-snake","adjacent-pair-cancellation","unique-sorted-intersection","first-nonrepeating-index","postfix-evaluation","stock-span","sliding-window-maximum","canonical-unix-path",
 "integer-cube-root","mountain-peak-index","first-last-occurrence","best-price-pair","longest-ones-with-flips","longest-two-distinct","stock-trade-with-days","circular-next-greater","asteroid-collision","bracket-decoder","stack-pop-sequence","kth-smallest-sorted-matrix","inversion-count","minimum-swaps-distinct-sort","weighted-interval-scheduling","task-cooldown","minimum-window-subsequence","longest-palindromic-substring","palindromic-substring-count","wildcard-match",
}
def _normalise(source: str) -> str: return ''.join(source.split()).casefold()
def test_shape_literal_fixtures_and_manifest():
 assert [x['id'] for x in JAVA_CURRICULUM_PART3]==[f'java-curated-{i:03d}' for i in range(101,121)]
 assert len(CONCEPTS)==len(JAVA_CURRICULUM_PART3)
 assert CONCEPTS.isdisjoint(PRIOR_CONCEPTS)
 assert all(len(x['public_tests'])==2 and len(x['hidden_tests'])==4 and len(x['hints'])==3 for x in JAVA_CURRICULUM_PART3)
 assert sum(x['difficulty']=='Easy' for x in JAVA_CURRICULUM_PART3)==4
 assert sum(x['difficulty']=='Medium' for x in JAVA_CURRICULUM_PART3)==10
 assert sum(x['difficulty']=='Hard' for x in JAVA_CURRICULUM_PART3)==6
def test_title_and_source_uniqueness_against_registered_java_1_100():
 prior=[x for x in JAVA_PRACTICE_EXERCISES+MULTILANG_EXERCISES if x.get('language')=='java']+JAVA_CURRICULUM_PART1+JAVA_CURRICULUM_PART2
 titles=[x['title'].casefold() for x in JAVA_CURRICULUM_PART3]; sources=[_normalise(x['solution']) for x in JAVA_CURRICULUM_PART3]
 assert not set(titles)&{x['title'].casefold() for x in prior}
 assert not set(sources)&{_normalise(x['solution']) for x in prior}
 assert len(set(titles))==20 and len(set(sources))==20
def test_import_pure_and_fixtures_literal():
 s=SOURCE.read_text(encoding='utf-8'); assert not any(x in s for x in ('subprocess','sqlite','requests','Exit code:','\ufffd','\u00c2','lambda'))
 calls=[x for x in ast.walk(ast.parse(s)) if isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id=='C']
 assert len(calls)==120 and all(len(x.args)==2 and all(isinstance(a,ast.Constant) and isinstance(a.value,str) for a in x.args) for x in calls)
 assert not any(ord(char)>127 or (ord(char)<32 and char not in '\r\n\t') for char in s)
def test_serialization_and_resource_contracts_cover_fixed_failures():
 by_id={x['id']:x for x in JAVA_CURRICULUM_PART3}
 cycle=by_id['java-curated-108']; assert 'next index' in cycle['description'] and 'cycleEntryIndex' not in cycle['description']
 assert all(len(c['input'].splitlines())>=4 for c in cycle['public_tests']+cycle['hidden_tests'])
 diameter=by_id['java-curated-110']; assert any('need not have larger' in c for c in diameter['constraints'])
 assert diameter['hidden_tests'][2]['input'].startswith('4\n2 1\n')
 distance=by_id['java-curated-114']; assert 'long' in distance['constraints'][1]
 assert distance['hidden_tests'][-1]['expected_output']=='4294967295'
 for exercise_id in ('java-curated-106','java-curated-107','java-curated-109','java-curated-113'):
  assert any('1900' in c for c in by_id[exercise_id]['constraints'])
 assert 'O(rows*cols) auxiliary space' in by_id['java-curated-112']['expected_complexity']
@pytest.mark.skipif(not all(main._java_tools()),reason='JDK required')
@pytest.mark.parametrize('exercise',JAVA_CURRICULUM_PART3,ids=lambda x:x['id'])
def test_reference_fixtures(exercise):
 r=main._validate_java_submission([('public',x) for x in exercise['public_tests']]+[('hidden',x) for x in exercise['hidden_tests']],exercise['solution'],4)
 assert r['status']=='passed',r
