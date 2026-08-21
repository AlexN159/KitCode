"""Focused quality gates for Python curated exercises 289--353."""
from __future__ import annotations
import ast
import hashlib
import io
import json
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

from backend.python_curated_289_353 import PYTHON_CURATED_289_353
from backend.exercise_bank import EXERCISES, _public_view, validate_submission

MODULE_SOURCE = Path(__file__).parents[2] / 'backend' / 'python_curated_289_353.py'

# Maintained independently of titles: these are contracts already offered by
# the historical Python catalogue and therefore may not be reintroduced here.
FORBIDDEN_EXISTING_CONCEPTS={
    'minimum-covering-window','levenshtein-distance','rolling-hash-matches',
    'minimum-spanning-tree','weighted-dag-shortest-path','strong-components',
    'bridge-edges','canonical-topological-order','network-delay','island-count',
    'word-search','merge-intervals','meeting-rooms','minimum-arrows',
    'train-platforms','maximum-subarray','inversion-count','histogram-rectangle',
    'trapped-rainwater','first-missing-positive','circular-house-robber',
    'equal-partition','minimum-jumps','minimum-rotation-index',
}

def _normalise(value: str) -> str:
    return ''.join(value.lower().split())

def test_ids_schema_titles_and_difficulty():
    items=PYTHON_CURATED_289_353
    assert [x['id'] for x in items] == [f'python-curated-{n:03d}' for n in range(289,354)]
    assert len(items)==65
    assert Counter(x['difficulty'] for x in items)=={'Medium':65}
    assert Counter(x['topics'][0] for x in items)=={
        'strings':10,'graphs':10,'grids':10,'intervals':8,'simulation':8,'arrays':11,'oop':8,
    }
    assert len({x['title'].casefold() for x in items})==65
    required={'id','concept_token','language','title','difficulty','topics','description','constraints','hints','expected_complexity','starter_code','solution','examples','public_tests','hidden_tests'}
    for item in items:
        assert required <= item.keys()
        assert item['language']=='python' and len(item['hints'])==3
        assert len(item['public_tests'])==2 and len(item['hidden_tests'])==4
        fixtures=item['public_tests']+item['hidden_tests']
        assert len({case['input'] for case in fixtures})==6
        assert item['description'] and item['constraints'] and item['expected_complexity']
        assert item['concept_token'] not in FORBIDDEN_EXISTING_CONCEPTS


def test_final_source_has_literal_fixtures_and_no_retired_generator_layers():
    source = MODULE_SOURCE.read_text(encoding='utf-8')
    for forbidden in ('exec(', 'retired draft', 'superseded', 'fallback',
                      'standard polynomial-time algorithm', '_NEW_CORE', '_FAMILY_SPECS'):
        assert forbidden not in source

    tree = ast.parse(source)
    literal_cases = next(
        ast.literal_eval(node.value)
        for node in tree.body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == '_FIXTURE_CASES'
                for target in node.targets)
    )
    assert len(literal_cases) == 57
    assert sum(len(cases) for cases in literal_cases.values()) == 342
    assert all(isinstance(source, str) and isinstance(output, str)
               for cases in literal_cases.values() for source, output in cases)

    fixtures = [case for item in PYTHON_CURATED_289_353
                for case in item['public_tests'] + item['hidden_tests']]
    assert len(fixtures) == 390
    assert all(isinstance(case['input'], str) and isinstance(case['expected_output'], str)
               for case in fixtures)
    assert len({(item['id'], case['input']) for item in PYTHON_CURATED_289_353
                for case in item['public_tests'] + item['hidden_tests']}) == 390

    metadata = [{key: item.get(key) for key in (
        'id', 'concept_token', 'title', 'difficulty', 'topics', 'description',
        'constraints', 'hints', 'expected_complexity', 'submission_mode', 'required_class',
    )} for item in PYTHON_CURATED_289_353]
    digest = hashlib.sha256(json.dumps(metadata, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    assert digest == '22f7cb10711aa3dcf9b31ba065724c412b1a828fe6103c67e09006e02d507137'


def test_script_contracts_are_specific_and_cover_formatting_ties_and_edge_rules():
    script_items = PYTHON_CURATED_289_353[:57]
    vague = (
        'Read the line records exactly as specified',
        'Read the graph in the exact line format',
        'Print the deterministic result',
        'uses the stated tie and output rules',
        'No implicit expansion or unstated recovery',
        'prints its canonical result',
    )
    assert all(not any(phrase in item['description'] for phrase in vague)
               for item in script_items)
    by_token = {item['concept_token']: item for item in script_items}
    required_phrases = {
        'unique-prefixes': ('line 1 is n', 'input order'),
        'escaped-codec': ('Input line 1', 'every remaining character'),
        'dag-query-reachability': ('directed edges', 'zero-edge path'),
        'weighted-schedule-witness': ('lexicographically smallest', 'zero-based indices'),
        'round-robin-completion': ('same arrival', 'input order'),
        'pancake-flips': ('leftmost maximum', 'flip lengths'),
        'k-closest-sorted': ('absolute(value-x)', 'sorted ascending'),
    }
    for token, phrases in required_phrases.items():
        description = by_token[token]['description']
        assert all(phrase in description for phrase in phrases)
        assert len(by_token[token]['constraints']) == 3
        assert len(by_token[token]['hints']) == 3


def test_every_script_contract_states_a_quantitative_input_bound():
    for item in PYTHON_CURATED_289_353[:57]:
        numeric_constraints = [constraint for constraint in item['constraints']
                               if any(character.isdigit() for character in constraint)]
        assert numeric_constraints, item['id']
        assert 'for this reference' not in ' '.join(item['constraints']).casefold()
    weighted = next(item for item in PYTHON_CURATED_289_353
                    if item['concept_token'] == 'weighted-schedule-witness')
    assert any('1 <= n <= 14' in constraint for constraint in weighted['constraints'])


def test_reviewed_complexities_state_time_and_space_and_wildcards_are_deterministic():
    by_token = {item['concept_token']: item for item in PYTHON_CURATED_289_353}
    assert by_token['wildcard-capture']['expected_complexity'] == (
        'O(P*T) time and O(S*T) space, where P is pattern length, T is text length, '
        'and S is the number of stars.'
    )
    assert by_token['triangle-count']['expected_complexity'] == (
        'O(n + m + sum of degree intersections) time and O(n + m) space.'
    )
    assert by_token['parking-ledger']['expected_complexity'] == (
        'O(q log q) time including final sorting and O(q) space.'
    )
    wildcard = by_token['wildcard-capture']['solution']
    assert 'import re' not in wildcard
    assert 'possible = [[False]' in wildcard


def test_repaired_medium_contract_edge_cases_have_the_documented_answers():
    by_token = {item['concept_token']: item for item in PYTHON_CURATED_289_353}
    checks = {
        'unique-prefixes': ('3\ndog\ndove\nduck\n', 'dog dov du'),
        'escaped-codec': ('D\nx\\ny\n', 'x\ny'),
        'dag-query-reachability': ('3 2\n0 1\n1 2\n2\n0 2\n2 0\n', 'YES NO'),
        'strict-nested-chain': ('3\n2 3\n1 4\n0 5\n', '3'),
        'round-robin-completion': ('2 1\n0 2\n0 1\n', '3 2'),
    }
    for token, (source, expected) in checks.items():
        namespace = {'__name__': 'audit'}
        exec(compile(by_token[token]['solution'], token, 'exec'), namespace)
        old_stdin, old_stdout = sys.stdin, sys.stdout
        try:
            sys.stdin = io.StringIO(source)
            output = io.StringIO()
            sys.stdout = output
            namespace['solve']()
        finally:
            sys.stdin, sys.stdout = old_stdin, old_stdout
        assert output.getvalue().rstrip() == expected.rstrip()


def test_escaped_codec_has_a_real_multiline_round_trip_fixture():
    codec = next(item for item in PYTHON_CURATED_289_353
                 if item['concept_token'] == 'escaped-codec')
    encoded = codec['public_tests'][1]
    decoded = codec['hidden_tests'][1]
    assert encoded == {
        'input': 'E\nline1\nline2\n',
        'expected_output': 'line1\\nline2',
    }
    assert decoded == {
        'input': 'D\nline1\\nline2\n',
        'expected_output': 'line1\nline2',
    }
    assert 'every remaining character' in codec['description']
    assert 'excluding exactly one final input-terminator newline' in codec['description']


def test_final_eight_are_medium_oop_class_contracts_with_private_harnesses():
    class_items = PYTHON_CURATED_289_353[-8:]
    assert [item['id'] for item in class_items] == [f'python-curated-{number:03d}' for number in range(346,354)]
    cli_forms = {
        'python-curated-346': ('line 1 is the initial balance', 'line 2 is q', '`deposit amount`', '`withdraw amount`', '`balance`'),
        'python-curated-347': ('line 1 is q', '`add name price quantity`', '`total`', '`count`'),
        'python-curated-348': ('line 1 is q', '`append text`', '`undo`', '`length`', '`text`'),
        'python-curated-349': ('line 1 is q', '`add song`', '`list`', '`has song`'),
        'python-curated-350': ('line 1 is q', '`circle radius`', '`rectangle width height`'),
        'python-curated-351': ('line 1 is q', '`name priority`'),
        'python-curated-352': ('line 1 is q', '`sub event double`', '`sub event label`', '`emit event value`'),
        'python-curated-353': ('line 1 is q', '`add title`', '`borrow title`', '`return title`', '`available`'),
    }
    for item in class_items:
        assert item['submission_mode'] == 'python_class'
        assert item['concept_token'] == f"oop-{int(item['id'][-3:])}"
        assert 'the next q lines' in item['description'] or 'each of the next q lines' in item['description']
        assert all(form in item['description'] for form in cli_forms[item['id']])
        assert 'def solve()' in item['starter_code'] and 'def solve()' in item['solution']
        assert item['required_class']['methods']
        for case in item['public_tests'] + item['hidden_tests']:
            assert set(case) == {'input','expected_output','harness'}
            assert 'submission_class' in case['harness']


def test_oop_class_references_pass_all_48_fixtures_through_real_runner():
    class_items = PYTHON_CURATED_289_353[-8:]
    prior = {item['id']: EXERCISES.get(item['id']) for item in class_items}
    try:
        EXERCISES.update({item['id']: item for item in class_items})
        for item in class_items:
            assert 'harness' not in repr(_public_view(item, include_hidden=True))
            result = validate_submission(item['id'], item['solution'], timeout_seconds=4)
            assert result['status'] == 'passed', (item['id'], result)
            assert result['passed'] == result['total'] == 6
    finally:
        for exercise_id, old in prior.items():
            if old is None: EXERCISES.pop(exercise_id, None)
            else: EXERCISES[exercise_id] = old

def test_every_reference_is_self_contained_and_handles_every_fixture():
    with tempfile.TemporaryDirectory() as directory:
        path=Path(directory)/'solution.py'
        for item in PYTHON_CURATED_289_353:
            path.write_text(item['solution'],encoding='utf-8')
            for case in item['public_tests']+item['hidden_tests']:
                result=subprocess.run([sys.executable,'-I',str(path)],input=case['input'],text=True,capture_output=True,timeout=3)
                assert result.returncode==0, result.stderr
                assert result.stdout.rstrip()==case['expected_output'].rstrip()


def test_reviewed_script_references_are_direct_and_not_semicolon_packed():
    """Best answers must remain teachable rather than gaming a line count."""
    for item in PYTHON_CURATED_289_353[:57]:
        solution = item['solution']
        assert 'def answer(mode' not in solution, item['id']
        assert ';' not in solution, item['id']

def test_no_normalised_title_description_or_solution_collides_with_catalogue():
    current_ids = {item['id'] for item in PYTHON_CURATED_289_353}
    prior=[item for item in EXERCISES.values() if item.get('language')=='python' and item['id'] not in current_ids]
    for field in ('title','description','solution'):
        old={_normalise(str(item[field])) for item in prior}
        current=[_normalise(str(item[field])) for item in PYTHON_CURATED_289_353]
        assert not (set(current)&old), field
        assert len(current)==len(set(current)), field

def test_every_reference_handles_its_public_examples():
    for item in PYTHON_CURATED_289_353:
        namespace={'__name__':'audit'}
        exec(compile(item['solution'],item['id'],'exec'),namespace)
        for case in item['public_tests']:
            old_stdin,old_stdout=sys.stdin,sys.stdout
            try:
                sys.stdin=io.StringIO(case['input']); output=io.StringIO();sys.stdout=output
                namespace['solve']()
            finally:
                sys.stdin,sys.stdout=old_stdin,old_stdout
            assert output.getvalue().rstrip()==case['expected_output'].rstrip()
