"""Curated Medium Python exercises 289--353.

Fixture inputs and expected outputs are deliberately stored as literals so the
curriculum catalogue has no import-time reference execution.
"""
from __future__ import annotations

_STARTER = """import sys

def solve() -> None:
    pass

if __name__ == '__main__':
    solve()
"""

def _base_item(number: int) -> dict:
    return {
        "id": f"python-curated-{number:03d}", "concept_token": "",
        "language": "python", "title": "", "difficulty": "Medium",
        "topics": [], "practice_frequency": "Common", "description": "",
        "constraints": [], "hints": [], "expected_complexity": "",
        "starter_code": _STARTER, "solution": "", "examples": [],
        "public_tests": [], "hidden_tests": [],
    }

PYTHON_CURATED_289_353 = [_base_item(number) for number in range(289, 354)]

_FIXTURE_CASES = {'chemical-formula': (('K4(ON(SO3)2)2\n', 'K4 N2 O14 S4'),
                      ('Mg(OH)2\n', 'H2 Mg1 O2'),
                      ('H2O\n', 'H2 O1'),
                      ('Be32\n', 'Be32'),
                      ('(H2O)3\n', 'H6 O3'),
                      ('NaCl\n', 'Cl1 Na1')),
 'brace-expansion': (('a{b,c}d\n', 'abd acd'),
                     ('{a,b}{c,d}\n', 'ac ad bc bd'),
                     ('x{a,b,c}\n', 'xa xb xc'),
                     ('plain\n', 'plain'),
                     ('{red,blue}\n', 'blue red'),
                     ('a{1,2}b\n', 'a1b a2b')),
 'quoted-csv': (('a,"b,c",d\n', 'a|b,c|d'),
                ('"a""b",c\n', 'a"b|c'),
                ('one,two\n', 'one|two'),
                ('"",x\n', '|x'),
                ('"first field",second\n', 'first field|second'),
                ('last,\n', 'last|')),
 'cidr-membership': (('192.168.1.0/24\n192.168.1.99\n', 'YES'),
                     ('10.0.0.0/8\n11.0.0.1\n', 'NO'),
                     ('172.16.0.0/12\n172.31.4.2\n', 'YES'),
                     ('1.2.3.4/32\n1.2.3.4\n', 'YES'),
                     ('1.2.3.4/32\n1.2.3.5\n', 'NO'),
                     ('0.0.0.0/0\n255.255.255.255\n', 'YES')),
 'roman-canonical': (('MCMXCIV\n', 'YES'),
                     ('IIII\n', 'NO'),
                     ('XLII\n', 'YES'),
                     ('IC\n', 'NO'),
                     ('MMXXVI\n', 'YES'),
                     ('VX\n', 'NO')),
 'unique-prefixes': (('3\ndog\ndove\nduck\n', 'dog dov du'),
                     ('3\ncat\ncar\ndog\n', 'cat car d'),
                     ('3\nalpha\nbeta\ngamma\n', 'a b g'),
                     ('2\none\nonly\n', 'one onl'),
                     ('3\nred\nblue\ngreen\n', 'r b g'),
                     ('3\nabc\nabd\nabe\n', 'abc abd abe')),
 'email-normalisation': (('3\na.b+c@x.com\nab@x.com\nA.B@x.com\n', '1'),
                         ('2\nx@y.com\nx+z@y.com\n', '1'),
                         ('1\na@b.com\n', '1'),
                         ('2\na.b@c.com\na.b+d@c.com\n', '1'),
                         ('3\na@x.com\na@y.com\na+q@x.com\n', '2'),
                         ('2\nfoo.bar@z.org\nfoobar@z.org\n', '1')),
 'text-justify': (('16\nThis is an example of text justification\n',
                   'This    is    an\nexample  of text\njustification   '),
                  ('10\na bb ccc\n', 'a bb ccc  '),
                  ('5\nhello\n', 'hello'),
                  ('12\npack my box\n', 'pack my box '),
                  ('8\na b c d\n', 'a b c d '),
                  ('14\nscience is fun\n', 'science is fun')),
 'wildcard-capture': (('a*b\naxxb\n', 'xx'),
                      ('pre*mid*end\npreXmidYend\n', 'X|Y'),
                      ('a*b\nac\n', 'NO'),
                      ('*\nhello\n', 'hello'),
                      ('x*y*z\nx1y2z\n', '1|2'),
                      ('foo*bar\nfoobar\n', '')),
 'escaped-codec': (('E\na\\b\n', 'a\\\\b'),
                   ('E\nline1\nline2\n', 'line1\\nline2'),
                   ('D\na\\tb\n', 'a\tb'),
                   ('D\nline1\\nline2\n', 'line1\nline2'),
                   ('E\nplain\n', 'plain'),
                   ('D\n\\\\\n', '\\')),
 'functional-cycle-data': (('5\n1 2 0 4 3\n', '0 3\n0 3\n0 3\n0 2\n0 2'),
                           ('4\n1 2 3 3\n', '3 1\n2 1\n1 1\n0 1'),
                           ('3\n0 0 1\n', '0 1\n1 1\n2 1'),
                           ('6\n1 2 3 4 5 2\n', '2 4\n1 4\n0 4\n0 4\n0 4\n0 4'),
                           ('2\n1 0\n', '0 2\n0 2'),
                           ('1\n0\n', '0 1')),
 'prufer-encode': (('4\n0 1\n1 2\n1 3\n', '1 1'),
                   ('5\n0 1\n0 2\n0 3\n0 4\n', '0 0 0'),
                   ('3\n0 1\n1 2\n', '1'),
                   ('6\n0 1\n1 2\n2 3\n3 4\n4 5\n', '1 2 3 4'),
                   ('4\n0 3\n1 3\n2 3\n', '3 3'),
                   ('2\n0 1\n', '')),
 'prufer-decode': (('4\n1 1\n', '0-1 1-2 1-3'),
                   ('5\n0 0 0\n', '0-1 0-2 0-3 0-4'),
                   ('3\n1\n', '0-1 1-2'),
                   ('6\n1 2 3 4\n', '0-1 1-2 2-3 3-4 4-5'),
                   ('4\n3 3\n', '0-3 1-3 2-3'),
                   ('2\n\n', '0-1')),
 'triangle-count': (('4 4\n0 1\n1 2\n2 0\n2 3\n', '1'),
                    ('4 6\n0 1\n0 2\n0 3\n1 2\n1 3\n2 3\n', '4'),
                    ('3 2\n0 1\n1 2\n', '0'),
                    ('5 0\n', '0'),
                    ('5 5\n0 1\n1 2\n2 3\n3 4\n4 0\n', '0'),
                    ('3 3\n0 1\n1 2\n0 2\n', '1')),
 'euler-kind': (('3 3\n0 1\n1 2\n2 0\n', 'CIRCUIT'),
                ('3 2\n0 1\n1 2\n', 'TRAIL'),
                ('4 2\n0 1\n2 3\n', 'NONE'),
                ('4 3\n0 1\n0 2\n0 3\n', 'NONE'),
                ('1 0\n', 'CIRCUIT'),
                ('2 1\n0 1\n', 'TRAIL')),
 'complement-components': (('4 2\n0 1\n2 3\n', '1'),
                           ('3 3\n0 1\n1 2\n0 2\n', '3'),
                           ('4 0\n', '1'),
                           ('3 2\n0 1\n1 2\n', '2'),
                           ('5 4\n0 1\n0 2\n0 3\n0 4\n', '2'),
                           ('2 1\n0 1\n', '2')),
 'dag-query-reachability': (('4 3\n0 1\n1 2\n0 3\n3\n0 2\n3 2\n0 3\n', 'YES NO YES'),
                            ('3 2\n0 1\n1 2\n2\n0 2\n2 0\n', 'YES NO'),
                            ('2 0\n1\n0 1\n', 'NO'),
                            ('4 2\n0 2\n1 3\n2\n0 3\n1 3\n', 'NO YES'),
                            ('1 0\n1\n0 0\n', 'YES'),
                            ('3 1\n0 1\n2\n0 1\n1 2\n', 'YES NO')),
 'minimum-reversals': (('4 3\n0 1\n2 1\n2 3\n', '1'),
                       ('3 2\n1 0\n1 2\n', '1'),
                       ('2 1\n0 1\n', '0'),
                       ('3 1\n0 1\n', '-1'),
                       ('4 3\n1 0\n1 2\n3 2\n', '2'),
                       ('1 0\n', '0')),
 'shortest-path-counts': (('4 4\n0 1\n0 2\n1 3\n2 3\n0\n', '1 1 1 2'),
                          ('3 2\n0 1\n1 2\n0\n', '1 1 1'),
                          ('4 1\n0 1\n0\n', '1 1 0 0'),
                          ('3 3\n0 1\n1 2\n0 2\n0\n', '1 1 1'),
                          ('2 1\n0 1\n1\n', '1 1'),
                          ('1 0\n0\n', '1')),
 'leaf-removal-rounds': (('4 3\n0 1\n1 2\n1 3\n', '0 1 0 0'),
                         ('5 4\n0 1\n1 2\n2 3\n3 4\n', '0 1 2 1 0'),
                         ('1 0\n', '0'),
                         ('4 3\n0 1\n0 2\n0 3\n', '1 0 0 0'),
                         ('3 2\n0 1\n0 2\n', '1 0 0'),
                         ('6 5\n0 1\n1 2\n1 3\n3 4\n3 5\n', '0 1 0 1 0 0')),
 'eight-direction-word-count': (('3 3\nABA\nABA\nBAB\nABA\n', '8'),
                                ('2 2\nAA\nAA\nAA\n', '12'),
                                ('1 4\nABC\nABCA\n', '1'),
                                ('3 3\nCAT\nCAT\nAAA\nTTT\n', '3'),
                                ('2 3\nDOG\nDOG\nGOD\n', '2'),
                                ('1 1\nZ\nZ\n', '8')),
 'latin-square-validation': (('3 3\n1 2 3\n2 3 1\n3 1 2\n', 'YES'),
                             ('2 2\n1 1\n2 2\n', 'NO'),
                             ('1 1\n1\n', 'YES'),
                             ('3 3\n1 2 3\n3 1 2\n2 3 1\n', 'YES'),
                             ('2 2\n1 2\n2 1\n', 'YES'),
                             ('3 3\n1 2 3\n2 1 3\n3 3 1\n', 'NO')),
 'largest-plus-arm': (('3 3\n111\n111\n111\n', '2'),
                      ('3 3\n010\n111\n010\n', '2'),
                      ('2 2\n11\n11\n', '1'),
                      ('1 4\n1111\n', '1'),
                      ('3 5\n00100\n11111\n00100\n', '2'),
                      ('2 3\n000\n000\n', '0')),
 'toroidal-shortest-path': (('3 3\n...\n.#.\n...\n0 0\n2 2\n', '2'),
                            ('2 2\n..\n..\n0 0\n1 1\n', '2'),
                            ('2 2\n.#\n##\n0 0\n1 1\n', '-1'),
                            ('1 3\n...\n0 0\n0 2\n', '1'),
                            ('3 1\n.\n.\n.\n0 0\n2 0\n', '1'),
                            ('2 3\n...\n...\n0 1\n1 1\n', '1')),
 'minesweeper-counts': (('2 2\n*.\n..\n', '*1\n11'),
                        ('1 3\n*.*\n', '*2*'),
                        ('3 3\n...\n.*.\n...\n', '111\n1*1\n111'),
                        ('1 1\n.\n', '0'),
                        ('2 3\n..*\n...\n', '01*\n011'),
                        ('2 2\n**\n**\n', '**\n**')),
 'conway-life': (('3 3\n1\n...\n###\n...\n', '.#.\n.#.\n.#.'),
                 ('3 3\n1\n.#.\n.#.\n.#.\n', '...\n###\n...'),
                 ('2 2\n2\n##\n##\n', '##\n##'),
                 ('1 1\n1\n#\n', '.'),
                 ('3 3\n0\n#..\n...\n..#\n', '#..\n...\n..#'),
                 ('3 3\n1\n...\n...\n...\n', '...\n...\n...')),
 'ring-rotation': (('2 2\n1\n1 2\n3 4\n', '3 1\n4 2'),
                   ('3 3\n2\n1 2 3\n4 5 6\n7 8 9\n', '7 4 1\n8 5 2\n9 6 3'),
                   ('1 3\n5\n1 2 3\n', '1 2 3'),
                   ('2 3\n1\n1 2 3\n4 5 6\n', '4 1 2\n5 6 3'),
                   ('4 4\n1\n1 2 3 4\n5 6 7 8\n9 10 11 12\n13 14 15 16\n', '5 1 2 3\n9 10 6 4\n13 11 7 8\n14 15 16 12'),
                   ('1 1\n3\n7\n', '7')),
 'diagonal-zigzag': (('2 3\n1 2 3\n4 5 6\n', '1 2 4 5 3 6'),
                     ('1 1\nx\n', 'x'),
                     ('3 1\na\nb\nc\n', 'a b c'),
                     ('2 2\n1 2\n3 4\n', '1 2 3 4'),
                     ('3 2\na b\nc d\ne f\n', 'a b c e d f'),
                     ('1 4\na b c d\n', 'a b c d')),
 'submatrix-target-count': (('2 2\n0\n1 -1\n-1 1\n', '5'),
                            ('1 3\n3\n1 1 1\n', '1'),
                            ('2 1\n1\n1\n1\n', '2'),
                            ('2 2\n2\n1 1\n1 1\n', '4'),
                            ('1 1\n0\n0\n', '1'),
                            ('2 3\n3\n1 2 0\n0 1 2\n', '5')),
 'knight-blocked-distance': (('3 3\n...\n...\n...\n0 0\n2 1\n', '1'),
                             ('3 3\n...\n.#.\n...\n0 0\n2 2\n', '4'),
                             ('1 1\n.\n0 0\n0 0\n', '0'),
                             ('2 3\n...\n...\n0 0\n1 2\n', '1'),
                             ('3 3\n.##\n###\n##.\n0 0\n2 2\n', '-1'),
                             ('4 4\n....\n....\n....\n....\n0 0\n3 3\n', '2')),
 'exact-coverage-lengths': (('3\n0 4\n1 3\n2 5\n', '2 2 1'),
                            ('2\n0 1\n1 2\n', '2 0'),
                            ('1\n2 7\n', '5'),
                            ('3\n0 10\n2 4\n6 8\n', '6 4 0'),
                            ('2\n0 5\n0 5\n', '0 5'),
                            ('4\n0 2\n1 3\n2 4\n3 5\n', '2 3 0 0')),
 'point-coverage-queries': (('2 3\n0 3\n2 5\n0\n2\n5\n', '1 2 0'),
                            ('1 2\n1 2\n1\n2\n', '1 0'),
                            ('3 1\n0 10\n2 4\n6 8\n3\n', '2'),
                            ('2 2\n-2 0\n0 2\n-1\n0\n', '1 1'),
                            ('1 1\n5 5\n5\n', '0'),
                            ('3 3\n1 4\n1 4\n1 4\n1\n3\n4\n', '3 3 0')),
 'strict-containment-pairs': (('3\n0 5\n1 4\n2 3\n', '3'),
                              ('2\n0 1\n0 1\n', '0'),
                              ('1\n0 2\n', '0'),
                              ('3\n0 10\n1 2\n3 4\n', '2'),
                              ('2\n1 3\n0 4\n', '1'),
                              ('3\n0 3\n1 2\n1 2\n', '2')),
 'weighted-schedule-witness': (('3\n0 2 5\n2 4 5\n0 4 9\n', '10 | 0 1'),
                               ('2\n0 1 3\n1 2 3\n', '6 | 0 1'),
                               ('1\n0 3 7\n', '7 | 0'),
                               ('3\n0 2 4\n1 3 10\n3 4 4\n', '14 | 1 2'),
                               ('2\n0 5 1\n0 5 2\n', '2 | 1'),
                               ('3\n0 1 1\n1 2 1\n2 3 1\n', '3 | 0 1 2')),
 'cleanup-room-count': (('2\n0 2 1\n2 4 1\n', '2'),
                        ('2\n0 2 0\n2 3 0\n', '1'),
                        ('3\n0 5 2\n1 2 0\n4 6 0\n', '2'),
                        ('1\n1 1 2\n', '1'),
                        ('3\n0 1 5\n2 3 0\n4 5 0\n', '2'),
                        ('2\n-1 0 1\n0 1 1\n', '2')),
 'strict-nested-chain': (('3\n0 10\n1 9\n2 8\n', '3'),
                         ('2\n0 1\n1 2\n', '1'),
                         ('1\n0 2\n', '1'),
                         ('4\n0 8\n1 7\n2 6\n3 5\n', '4'),
                         ('3\n0 5\n0 4\n1 3\n', '2'),
                         ('2\n-2 2\n-1 1\n', '2')),
 'union-intersection-length': (('2 2\n0 3\n5 8\n1 6\n7 9\n', '4'),
                               ('1 1\n0 1\n1 2\n', '0'),
                               ('2 1\n0 5\n2 7\n3 4\n', '1'),
                               ('1 2\n0 10\n2 3\n4 5\n', '2'),
                               ('1 1\n0 0\n0 1\n', '0'),
                               ('2 2\n0 2\n4 6\n2 4\n6 8\n', '0')),
 'minimum-target-cover': (('3 0 5\n0 2\n1 4\n4 5\n', '3'),
                          ('2 0 3\n0 1\n2 3\n', '-1'),
                          ('1 1 2\n0 3\n', '1'),
                          ('3 0 10\n0 4\n4 8\n8 10\n', '3'),
                          ('2 -1 1\n-1 0\n0 1\n', '2'),
                          ('2 0 1\n0 1\n0 1\n', '1')),
 'shell-tokenizer': (('one "two words" three\n', 'one|two words|three'),
                     ("a\\ b 'c d'\n", 'a b|c d'),
                     ('"" x\n', '|x'),
                     ('a "b\\"c"\n', 'a|b"c'),
                     ('one\\ two\n', 'one two'),
                     ('\'a b\' "c d"\n', 'a b|c d')),
 'parking-ledger': (('2 3\nENTER A 1\nEXIT A 4\nENTER B 5\n', 'A 6\nACTIVE B'),
                    ('1 2\nENTER X 0\nEXIT X 0\n', 'X 0\nACTIVE '),
                    ('3 3\nENTER B 2\nENTER A 1\nEXIT B 5\n', 'B 9\nACTIVE A'),
                    ('1 1\nEXIT X 4\n', 'ACTIVE '),
                    ('2 4\nENTER A 1\nEXIT A 2\nENTER A 3\nEXIT A 5\n', 'A 2\nA 4\nACTIVE '),
                    ('5 2\nENTER Z 9\nENTER Y 1\n', 'ACTIVE Y Z')),
 'tournament-scoreboard': (('3\nWIN A\nDRAW B C\nWIN B\n', 'B:4 A:3 C:1'),
                           ('2\nDRAW A B\nDRAW A B\n', 'A:2 B:2'),
                           ('1\nWIN Z\n', 'Z:3'),
                           ('3\nWIN C\nWIN B\nWIN A\n', 'A:3 B:3 C:3'),
                           ('2\nWIN A\nWIN A\n', 'A:6'),
                           ('2\nDRAW X Y\nWIN Y\n', 'Y:4 X:1')),
 'undo-redo-buffer': (('4\nAPPEND hi\nAPPEND !\nUNDO\nREDO\n', 'hi!'),
                      ('3\nAPPEND abc\nDELETE 2\nUNDO\n', 'abc'),
                      ('2\nUNDO\nREDO\n', ''),
                      ('4\nAPPEND a\nDELETE 1\nUNDO\nREDO\n', ''),
                      ('1\nAPPEND hello\n', 'hello'),
                      ('3\nAPPEND x\nUNDO\nAPPEND y\n', 'y')),
 'packet-reassembly': (('3 3\n1 B\n0 A\n2 C\n', 'ABC'),
                       ('3 2\n0 a\n2 c\n', 'MISSING 1'),
                       ('1 2\n0 x\n0 y\n', 'x'),
                       ('2 2\n1 b\n0 a\n', 'ab'),
                       ('4 3\n3 d\n1 b\n2 c\n', 'MISSING 0'),
                       ('2 1\n0 z\n', 'MISSING 1')),
 'warehouse-push': (('2 3\n@B.\n...\nRR\n', '0 1 | 0 2'),
                    ('3 3\n@..\n.B#\n...\nDR\n', '1 0 | 1 1'),
                    ('1 3\n@B#\nR\n', '0 0 | 0 1'),
                    ('2 2\n@#\nB.\nD\n', '0 0 | 1 0'),
                    ('2 3\n@..\n.B.\nDRR\n', '1 1 | 1 2'),
                    ('1 2\n@B\nL\n', '0 0 | 0 1')),
 'round-robin-completion': (('2 1\n0 2\n0 1\n', '3 2'),
                            ('2 2\n0 3\n1 2\n', '5 4'),
                            ('1 3\n5 2\n', '7'),
                            ('3 1\n0 1\n0 1\n0 1\n', '1 2 3'),
                            ('2 5\n0 1\n2 1\n', '1 3'),
                            ('3 2\n0 5\n1 1\n4 2\n', '8 3 7')),
 'rail-permutation': (('3 2\n1 2 3\n3 1 2\n', 'YES NO'),
                      ('1 1\n1\n', 'YES'),
                      ('4 2\n4 3 2 1\n2 1 4 3\n', 'YES NO'),
                      ('3 1\n2 3 1\n', 'YES'),
                      ('2 2\n2 1\n1 2\n', 'YES YES'),
                      ('4 1\n3 2 1 4\n', 'NO')),
 'subarray-median-k': (('3\n1 2 3\n2\n', '3'),
                       ('3\n3 1 2\n2\n', '2'),
                       ('1\n5\n5\n', '1'),
                       ('4\n4 1 3 2\n2\n', '4'),
                       ('2\n1 2\n1\n', '2'),
                       ('4\n2 4 1 3\n3\n', '2')),
 'shortest-at-least-k': (('3\n2 -1 2\n3\n', '3'),
                         ('3\n1 2 3\n3\n', '1'),
                         ('2\n1 -1\n2\n', '-1'),
                         ('4\n-1 4 -2 3\n5\n', '3'),
                         ('1\n5\n6\n', '-1'),
                         ('3\n2 -1 2\n2\n', '1')),
 'one-deletion-max-sum': (('4\n1 -2 0 3\n', '4'),
                          ('1\n-1\n', '-1'),
                          ('4\n1 -2 -2 3\n', '3'),
                          ('3\n1 2 3\n', '6'),
                          ('3\n-1 -1 -1\n', '-1'),
                          ('5\n2 1 -2 3 4\n', '10')),
 'reverse-pair-count': (('5\n1 3 2 3 1\n', '2'),
                        ('5\n2 4 3 5 1\n', '3'),
                        ('3\n1 1 1\n', '0'),
                        ('3\n-5 -5 -5\n', '3'),
                        ('1\n9\n', '0'),
                        ('4\n10 4 2 1\n', '4')),
 'next-permutation': (('3\n1 2 3\n', '1 3 2'),
                      ('3\n3 2 1\n', 'NONE'),
                      ('3\n1 1 5\n', '1 5 1'),
                      ('4\n1 3 2 4\n', '1 3 4 2'),
                      ('1\n1\n', 'NONE'),
                      ('4\n2 3 1 3\n', '2 3 3 1')),
 'pancake-flips': (('3\n3 1 2\n', '3 2'),
                   ('3\n1 2 3\n', '-'),
                   ('4\n4 3 2 1\n', '4'),
                   ('1\n5\n', '-'),
                   ('4\n2 4 1 3\n', '2 4 3 2'),
                   ('3\n2 1 3\n', '2')),
 'circular-one-grouping': (('5\n1 0 1 0 1\n', '1'),
                           ('3\n1 1 1\n', '0'),
                           ('4\n0 0 0 0\n', '0'),
                           ('4\n1 0 0 1\n', '0'),
                           ('1\n1\n', '0'),
                           ('6\n1 0 1 1 0 1\n', '1')),
 'exactly-k-distinct': (('5\n1 2 1 2 3\n2\n', '7'),
                        ('3\n1 2 3\n1\n', '3'),
                        ('4\n1 1 1 1\n1\n', '10'),
                        ('3\n1 2 1\n3\n', '0'),
                        ('1\n5\n2\n', '0'),
                        ('4\n1 2 2 3\n2\n', '4')),
 'bounded-range-longest': (('4\n8 2 4 7\n4\n', '2'),
                           ('6\n10 1 2 4 7 2\n5\n', '4'),
                           ('1\n3\n0\n', '1'),
                           ('3\n1 1 1\n0\n', '3'),
                           ('4\n1 5 6 7\n1\n', '2'),
                           ('5\n4 2 2 2 4\n0\n', '3')),
 'online-lower-medians': (('4\n5 1 3 2\n', '5 1 3 2'),
                          ('3\n1 2 3\n', '1 1 2'),
                          ('1\n9\n', '9'),
                          ('5\n5 4 3 2 1\n', '5 4 4 3 3'),
                          ('4\n2 2 2 2\n', '2 2 2 2'),
                          ('3\n-1 0 -2\n', '-1 -1 -1')),
 'k-closest-sorted': (('5\n1 2 3 4 5\n4 3\n', '1 2 3 4'),
                      ('5\n1 2 3 4 5\n4 -1\n', '1 2 3 4'),
                      ('5\n1 2 3 4 5\n4 6\n', '2 3 4 5'),
                      ('4\n1 3 5 7\n2 4\n', '3 5'),
                      ('1\n9\n1 9\n', '9'),
                      ('5\n-2 -1 0 1 2\n3 0\n', '-1 0 1'))}

def _literal_fixtures(cases: tuple[tuple[str, str], ...]) -> list[dict[str, str]]:
    return [{"input": source, "expected_output": expected} for source, expected in cases]

# Every script drill has a self-contained learner contract.  Keep these next to
# the literal fixtures: the reference implementations deliberately share small
# dispatchers, but the input and output rules do not.
_CONTRACTS = {
 'chemical-formula': ('Input: one valid formula containing element symbols, parentheses and positive decimal multipliers. Output atom totals as `SymbolCount`, sorted by symbol and separated by one space.', ['Element symbols start with an uppercase letter; nesting is allowed.', 'An omitted multiplier means 1.'], ['Use a stack of count maps.', 'Multiply a completed parenthesised group before merging it.'], 'O(L) time and O(L) space.'),
 'brace-expansion': ('Input: one string with zero or more non-nested `{a,b,...}` groups; each alternative is non-empty and has no braces. Output every expansion once, lexicographically sorted, separated by one space.', ['Groups are not nested.', 'Literal characters and alternatives contain no comma outside a group.'], ['Build a list of prefixes left to right.', 'Sort only the finished expansions.'], 'O(output size) time and space.'),
 'quoted-csv': ('Input: one RFC-4180-style CSV record. A comma separates fields, a quoted field may contain commas, and doubled quotes inside quotes mean one quote. Output decoded fields joined by `|`, preserving empty fields.', ['There is exactly one record.', 'Quotes are balanced and appear only as CSV quoting.'], ['Scan quotes before treating a comma as a delimiter.', 'An empty field still produces an empty output segment.'], 'O(L) time and O(L) space.'),
 'cidr-membership': ('Input line 1 is an IPv4 CIDR block `address/prefix`; line 2 is an IPv4 address. Output `YES` exactly when the address belongs to that block, otherwise `NO`.', ['Prefix is an integer from 0 through 32.', 'The network address need not already be masked.'], ['Turn the prefix into a mask.', 'Compare masked integer addresses.'], 'O(1) time and space.'),
 'roman-canonical': ('Input: one non-empty Roman-numeral string using I,V,X,L,C,D,M. Output `YES` only if it is the canonical Roman spelling of its value (1 through 3999); otherwise output `NO`.', ['Only canonical subtractive pairs are valid.', 'A syntactically invalid string must not be accepted merely because it has a numeric value.'], ['Compute the value, then render it canonically.', 'Compare the rendered string with the input.'], 'O(L) time and O(1) space.'),
 'unique-prefixes': ('Input line 1 is n; the next n lines are distinct lowercase words, with no word a prefix of another. For each word in input order, output its shortest prefix that no other input word starts with; separate prefixes by one space.', ['No input word is a prefix of another input word.', 'Words contain lowercase English letters only.'], ['Count prefixes in a trie or dictionary.', 'Keep the original word order for output.'], 'O(total word length) time and space.'),
 'email-normalisation': ('Input line 1 is n; the next n lines are email addresses. Lowercase every address; in its local part, ignore dots and everything from the first `+` onward. Keep the domain unchanged apart from lowercasing. Output the number of distinct normalised addresses.', ['Each address has exactly one `@`.', 'The normalisation rule applies only to the local part.'], ['Split at `@` first.', 'Put normalised addresses in a set.'], 'O(total input length) time and space.'),
 'text-justify': ('Input line 1 is width W; line 2 contains words separated by single spaces. Greedily pack as many words as fit. Output every line at width W: non-final multiword lines distribute extra spaces left to right; one-word and final lines are left-justified with trailing spaces. The judge ignores whitespace only at the very end of the complete output, not spaces before an output newline.', ['Every word length is at most W.', 'Interior trailing spaces in output lines are significant.'], ['Track word characters separately from gaps.', 'Use divmod to distribute spaces.'], 'O(total text length) time and space.'),
 'wildcard-capture': ('Input line 1 is a pattern containing literal characters and `*`; line 2 is text. Each `*` captures the shortest possible string that allows the complete pattern to match. Output captures in star order separated by `|`, or `NO` if no full match exists.', ['Only `*` is special.', 'A capture may be empty.'], ['Anchor the match at both ends.', 'Make each wildcard non-greedy.'], 'O(L) time for these bounded patterns.'),
 'escaped-codec': ('Input line 1 is `E` or `D`. The payload is every remaining character after that line, excluding exactly one final input-terminator newline when present. `E` replaces backslash, tab, and newline by `\\\\`, `\\t`, and `\\n`; `D` reverses those three forms. Output the transformed payload; the judge ignores whitespace only at the very end of the complete output.', ['The encoded payload uses only the three stated escape forms.', 'A payload may span multiple physical lines; two final newlines represent a payload ending in one newline.'], ['Separate the mode line without splitting the remaining payload into records.', 'Remove at most one final terminator before transforming.'], 'O(L) time and space.'),
 'functional-cycle-data': ('Input line 1 is n; line 2 gives n successors, each in 0..n-1. For every start vertex 0..n-1, output one line: edges before first entering its eventual cycle, then that cycle length.', ['The graph has exactly one outgoing edge per vertex.', 'Output lines are in vertex-number order.'], ['Walk until a vertex repeats.', 'Record the first step at which each visited vertex appeared.'], 'O(n^2) time and O(n) extra space.'),
 'prufer-encode': ('Input line 1 is n; the next n-1 lines are undirected edges of a tree on vertices 0..n-1. Repeatedly remove the smallest numbered leaf and output its neighbour. Print the n-2 values separated by spaces.', ['The input is a tree.', 'The n=2 output is empty.'], ['Maintain every vertex degree.', 'Select the smallest remaining leaf each round.'], 'O(n^2) time and O(n) space.'),
 'prufer-decode': ('Input line 1 is n; line 2 contains n-2 Prüfer values (and is blank when n=2). Decode using the smallest available leaf. Output canonical edges as `u-v`, each endpoint ordered, with edges lexicographically sorted and separated by spaces.', ['All Prüfer values are in 0..n-1.', 'The n=2 sequence is empty.'], ['Start every vertex with degree 1.', 'Select the smallest available leaf each round.'], 'O(n^2) time and O(n) space.'),
 'triangle-count': ('Input line 1 is n m; the next m lines are distinct undirected edges. Output the number of unordered triples of vertices that form a triangle.', ['No self-loops or duplicate edges.', 'Vertices are 0..n-1.'], ['Intersect neighbour sets for an ordered edge.', 'Count each triangle once by vertex order.'], 'O(sum of degree intersections) time.'),
 'euler-kind': ('Input line 1 is n m; the next m lines are undirected edges. Ignore isolated vertices for connectivity. Output `CIRCUIT` if all non-isolated vertices are connected and have even degree, `TRAIL` if exactly two have odd degree, else `NONE`.', ['A graph with no edges is a circuit.', 'No self-loops or duplicate edges.'], ['Check connectivity before counting odd degrees.', 'Isolated vertices do not break connectivity.'], 'O(n+m) time and space.'),
 'complement-components': ('Input line 1 is n m; the next m lines are undirected edges. In the complement graph, two different vertices are adjacent exactly when they are not an input edge. Output its number of connected components.', ['No self-loops or duplicate edges.', 'Vertices are 0..n-1.'], ['Keep an unvisited set.', 'From a vertex, add all remaining non-neighbours.'], 'O(n^2) time and O(n+m) space.'),
 'dag-query-reachability': ('Input line 1 is n m; the next m lines are directed edges of a DAG. Then line `m+2` is q, followed by q ordered queries `s t`. Output `YES` for each query iff a directed path from s to t exists (a zero-edge path means s reaches itself); separate answers by spaces.', ['Edges are directed; do not add reverse edges.', 'The input graph is acyclic.'], ['Build directed adjacency lists.', 'A DFS/BFS per query is sufficient for the stated bounds.'], 'O(q(n+m)) time and O(n+m) space.'),
 'minimum-reversals': ('Input line 1 is n m; the next m lines are directed edges. You may traverse an edge forward at cost 0 or backward at cost 1. Output the minimum cost from vertex 0 to vertex n-1, or `-1` if unreachable.', ['Vertices are 0..n-1.', 'Edges may be traversed in either direction under the stated cost.'], ['Model each edge twice.', 'Use 0-1 BFS.'], 'O(n+m) time and space.'),
 'shortest-path-counts': ('Input line 1 is n m; next m lines are undirected edges; final line is source s. Output, for vertices 0..n-1, the number of shortest paths from s modulo 1,000,000,007, separated by spaces; unreachable vertices output 0.', ['No self-loops or duplicate edges.', 'The source has one empty path to itself.'], ['BFS fixes the shortest distance.', 'Add ways only along the next distance layer.'], 'O(n+m) time and space.'),
 'leaf-removal-rounds': ('Input line 1 is n m and the next m lines form a tree. Simultaneously remove every current leaf in round 0, then repeat. Output each vertex’s removal round in vertex order, separated by spaces.', ['The graph is a tree, including the n=1 case.', 'A degree-0 single vertex is removed in round 0.'], ['Queue all initial leaves.', 'When a neighbour becomes a leaf, assign one more than the current round.'], 'O(n) time and space.'),
 'eight-direction-word-count': ('Input line 1 is rows cols; line 2 is a word; next rows lines are the character grid. Count every start cell and each of the eight compass directions in which the full word fits. Output the count; for a one-letter word, all eight directions count separately.', ['Grid rows have exactly cols characters.', 'Directions are N, NE, E, SE, S, SW, W, NW.'], ['Try every cell and direction.', 'Stop a direction at the first mismatch or boundary.'], 'O(R*C*8*L) time and O(1) extra space.'),
 'latin-square-validation': ('Input line 1 is n n; next n lines each contain n integers. Output `YES` iff every row and every column contains each integer 1..n exactly once; otherwise `NO`.', ['The matrix is square.', 'Values outside 1..n make it invalid.'], ['Compare each row and column set with {1..n}.', 'Check both dimensions.'], 'O(n^2) time and space.'),
 'largest-plus-arm': ('Input line 1 is rows cols; next rows lines are `0`/`1` cells. A plus of arm length k has a `1` centre and k-1 additional `1` cells in each cardinal direction. Output the maximum k, or 0 when there is no `1`.', ['Rows have exactly cols characters.', 'A one-cell plus has arm length 1.'], ['Expand four arms together from each possible centre.', 'The first failed direction limits that centre.'], 'O(R*C*min(R,C)) time and O(1) extra space.'),
 'toroidal-shortest-path': ('Input line 1 is rows cols; next rows lines are `.` open or `#` blocked; final two lines are start and target row/column. Move N/S/E/W, wrapping around opposite grid edges. Output the fewest moves or `-1`.', ['Start and target are open.', 'Coordinates are zero-based.'], ['Use BFS.', 'Apply modulo only after taking a cardinal step.'], 'O(R*C) time and space.'),
 'minesweeper-counts': ('Input line 1 is rows cols; next rows lines are `*` mines or `.` empty cells. Output a same-sized grid: keep `*`; replace each `.` by its number of adjacent mines in the eight surrounding cells.', ['Rows have exactly cols characters.', 'Cells outside the grid are not neighbours.'], ['Inspect the 3-by-3 neighbourhood.', 'Do not replace a mine.'], 'O(R*C) time and O(1) extra space besides output.'),
 'conway-life': ('Input line 1 is rows cols; line 2 is k; next rows lines are `#` live or `.` dead. Simulate exactly k Conway Life generations without wrapping. Output the resulting grid. A live cell survives with 2 or 3 neighbours; a dead cell is born with 3.', ['Rows have exactly cols characters.', 'Only the eight in-bounds neighbours count.'], ['Build a fresh grid per generation.', 'Do not update cells in place.'], 'O(k*R*C) time and O(R*C) space.'),
 'ring-rotation': ('Input line 1 is rows cols; line 2 is nonnegative k; next rows lines are integer matrix rows. Rotate every complete concentric perimeter clockwise by k positions. Leave a central unringed row or column unchanged; print rows with one-space-separated values.', ['A ring has at least two rows and two columns.', 'k may exceed a ring length.'], ['List each ring clockwise once.', 'Reduce k modulo that ring length.'], 'O(R*C) time and space.'),
 'diagonal-zigzag': ('Input line 1 is rows cols; next rows lines contain cols whitespace-separated tokens. Visit anti-diagonals by increasing row+column: reverse diagonals with even sum, keep odd sums forward. Output tokens separated by one space.', ['Tokens contain no whitespace.', 'Coordinates are zero-based for the parity rule.'], ['Enumerate valid rows for each diagonal sum.', 'Reverse only the requested diagonals.'], 'O(R*C) time and space.'),
 'submatrix-target-count': ('Input line 1 is rows cols; line 2 is target T; next rows lines are integers. Output the number of non-empty axis-aligned submatrices whose element sum is exactly T.', ['Values and T are signed integers.', 'Rows have exactly cols values.'], ['Fix a top and bottom row.', 'Count target subarrays of the compressed columns with prefix sums.'], 'O(R^2*C) time and O(C) space.'),
 'knight-blocked-distance': ('Input line 1 is rows cols; next rows lines are `.` open or `#` blocked; final two lines are start and target. A knight uses chess moves (±2,±1) without wrapping. Output fewest moves or `-1`.', ['Start and target are open.', 'Coordinates are zero-based.'], ['Use BFS over the eight knight offsets.', 'Reject blocked and out-of-bounds destinations.'], 'O(R*C) time and space.'),
 'exact-coverage-lengths': ('Input line 1 is n; next n lines are half-open intervals `start end`. For every k from 1 through n, output the total integer-line length covered by exactly k intervals, separated by spaces.', ['Endpoints are integers and start <= end.', 'Touching intervals do not overlap at their shared endpoint.'], ['Sort all distinct endpoints.', 'Coverage is constant between consecutive endpoints.'], 'O(n^3) time and O(n) space.'),
 'point-coverage-queries': ('Input line 1 is n q; next n lines are half-open intervals `start end`; next q lines are query points. Output how many intervals contain each point (`start <= point < end`) in query order, separated by spaces.', ['Endpoints and points are integers.', 'Empty intervals contain no point.'], ['Sort endpoints for faster queries.', 'The right endpoint is excluded.'], 'O(n*q) time and O(n) space.'),
 'strict-containment-pairs': ('Input line 1 is n; next n lines are half-open intervals. Output the number of ordered pairs (outer, inner) with `outer.start < inner.start` and `inner.end < outer.end`.', ['Equal endpoints are not strict containment.', 'Equal intervals contribute zero.'], ['Compare both endpoints strictly.', 'Keep duplicate intervals distinct records.'], 'O(n^2) time and O(n) space.'),
 'weighted-schedule-witness': ('Input line 1 is n; next n lines are `start end reward`. Select pairwise non-overlapping half-open intervals. Output `maximum_reward | i j ...`, where indices are original zero-based indices in increasing order; among equal rewards choose the lexicographically smallest index list.', ['Rewards are positive integers.', 'Intervals that touch may both be selected.'], ['Keep original indices with intervals.', 'Compare candidate index tuples for equal rewards.'], 'O(2^n * n^2) time and O(n) space; n <= 14.'),
 'cleanup-room-count': ('Input line 1 is n; next n lines are `start end cleanup`. A booking occupies `[start, end + cleanup)`. Output the maximum number of simultaneous occupied bookings.', ['All values are integers; start <= end and cleanup >= 0.', 'A booking ending at time t frees its room before one starting at t.'], ['Sweep start and release events.', 'Process releases before starts at the same time.'], 'O(n log n) time and O(n) space.'),
 'strict-nested-chain': ('Input line 1 is n; next n lines are intervals. Output the largest chain in which every later interval has strictly larger start and strictly smaller end than the previous one.', ['Equal starts or ends cannot be consecutive in a chain.', 'Input order is irrelevant.'], ['Sort outer intervals before inner intervals.', 'Use DP over valid strict parents.'], 'O(n^2) time and O(n) space.'),
 'union-intersection-length': ('Input line 1 is n m; next n lines are set-A half-open intervals and next m lines set-B intervals. Merge each set’s overlapping or touching intervals, then output the length of the intersection of the two unions.', ['Endpoints are integers and start <= end.', 'Zero-length intervals add no length.'], ['Merge each collection independently.', 'Walk the two merged lists with two pointers.'], 'O((n+m) log(n+m)) time and O(n+m) space.'),
 'minimum-target-cover': ('Input line 1 is n L R; next n lines are half-open candidate intervals. Output the fewest intervals whose union covers every point of `[L,R)`, or `-1` if impossible.', ['L <= R and endpoints are integers.', 'Touching intervals may extend coverage continuously.'], ['Among intervals starting before current coverage, take the furthest end.', 'Stop if no interval extends the frontier.'], 'O(n log n) time and O(n) space.'),
 'shell-tokenizer': ('Input: one shell-like command line. Whitespace separates tokens except inside single or double quotes; a backslash escapes the next character outside single quotes. Output decoded tokens joined by `|`.', ['Quotes are balanced.', 'There are no shell expansions or comments.'], ['Track quote state while scanning.', 'Do not include surrounding quotes.'], 'O(L) time and space.'),
 'parking-ledger': ('Input line 1 is `rate q`; next q lines are `ENTER id time` or `EXIT id time`. An EXIT for an active id prints `id fee` where fee is `(time-enter_time)*rate`; unmatched EXITs do nothing. Finally output `ACTIVE` followed by active ids in lexicographic order.', ['Times are integers and each id has at most one active entry.', 'Commands are processed in order.'], ['Map each active id to its entry time.', 'Remove an id only on a matched EXIT.'], 'O(q log q) time including final sorting.'),
 'tournament-scoreboard': ('Input line 1 is q; next q lines are `WIN player` or `DRAW player1 player2`. A win gives 3 points; each draw participant gets 1. Output `name:points` entries sorted by descending points then ascending name, separated by spaces.', ['Names are case-sensitive non-whitespace words.', 'Players appear only through commands.'], ['Accumulate points in a map.', 'Sort by the stated two-key order.'], 'O(q + p log p) time and O(p) space.'),
 'undo-redo-buffer': ('Input line 1 is q; next q lines are `APPEND text`, `DELETE k`, `UNDO`, or `REDO`. APPEND and DELETE save the prior buffer and clear redo; DELETE removes the final k characters. UNDO/REDO with an empty relevant history are no-ops. Output final text.', ['0 <= k <= current length.', 'APPEND text is the remainder of its line and may contain spaces.'], ['Store prior states on two stacks.', 'A new edit clears redo history.'], 'O(total edited characters) time and space.'),
 'packet-reassembly': ('Input line 1 is `total m`; next m lines are `index payload`. Keep the first packet seen for each index. If any index 0..total-1 is absent, output `MISSING` followed by missing indices ascending; otherwise concatenate payloads by index.', ['0 <= index < total.', 'Payload is the remainder of the line and may contain spaces.'], ['Use a dictionary with setdefault semantics.', 'Check all required indices after reading.'], 'O(total+m) time and space.'),
 'warehouse-push': ('Input line 1 is rows cols; next rows lines contain walls `#`, floor `.`, one robot `@`, and one box `B`; final line is commands UDLR. A move into a wall/outside fails; entering the box pushes it only if the next square is clear. Output `robot_row robot_col | box_row box_col`.', ['There is exactly one robot and one box.', 'Coordinates are zero-based.'], ['Keep positions separate from the immutable map.', 'Test the square beyond the box before moving either piece.'], 'O(R*C + commands) time and space.'),
 'round-robin-completion': ('Input line 1 is `n quantum`; next n lines give each job’s `arrival burst` in job-index order. Use FIFO round robin: newly arrived jobs join the tail before a pre-empted job; jobs with the same arrival join in input order. Output completion times in job-index order.', ['Arrival and burst are nonnegative; quantum is positive.', 'A job runs for min(quantum, remaining burst).'], ['Sort only by arrival then original index.', 'Enqueue all arrivals at the current clock before requeueing.'], 'O(n log n + number of slices) time and O(n) space.'),
 'rail-permutation': ('Input line 1 is `n q`; each of the next q lines is a permutation of cars 1..n. Incoming cars arrive in increasing order and may go directly out or onto one stack. Output `YES`/`NO` for each requested departure order, separated by spaces.', ['Each query is a permutation of 1..n.', 'The side track is last-in, first-out.'], ['Push arrivals until the required car is available.', 'Only the stack top can leave the side track.'], 'O(n*q) time and O(n) space.'),
 'subarray-median-k': ('Input line 1 is n; line 2 has n distinct integers; line 3 is k. Count non-empty subarrays whose lower median (the element at index `(length-1)//2` after sorting) equals k. Output the count.', ['All array values are distinct.', 'k is one of the array values.'], ['Write out the lower-median rule for even lengths.', 'Enumerate subarrays within the stated bound.'], 'O(n^3 log n) time and O(n) space.'),
 'shortest-at-least-k': ('Input line 1 is n; line 2 has n signed integers; line 3 is K. Output the minimum length of a non-empty subarray with sum at least K, or `-1` if none exists.', ['Values and K are signed 32-bit integers.', 'Negative values are allowed.'], ['Use prefix sums.', 'Maintain increasing prefix sums in a deque.'], 'O(n) time and O(n) space.'),
 'one-deletion-max-sum': ('Input line 1 is n; line 2 has n signed integers. Output the largest sum of a non-empty contiguous subarray after deleting at most one element.', ['The chosen subarray must retain at least one element.', 'Deletion is optional.'], ['Track best sums ending here with and without a deletion.', 'All-negative input still chooses one element.'], 'O(n) time and O(1) space.'),
 'reverse-pair-count': ('Input line 1 is n; line 2 has n signed integers. Output pairs i<j such that a[i] > 2*a[j].', ['Use integer arithmetic; values may be negative.', 'Each qualifying index pair is counted once.'], ['Check ordered index pairs.', 'A merge-sort count is the scalable alternative.'], 'O(n^2) time and O(1) extra space.'),
 'next-permutation': ('Input line 1 is n; line 2 has n integers. Output the lexicographically next larger permutation of this sequence, including duplicates, or `NONE` if it is already largest.', ['Lexicographic order compares values left to right.', 'Duplicate values are allowed.'], ['Find the rightmost increasing pivot.', 'Reverse the suffix after swapping.'], 'O(n) time and O(1) extra space.'),
 'pancake-flips': ('Input line 1 is n; line 2 has n distinct integers. Apply deterministic pancake sort: for each unsorted suffix, choose the leftmost maximum; if needed flip its prefix to front, then flip the suffix. Output flip lengths in order, or `-` when no flips occur.', ['A flip reverses the first k elements.', 'Values are distinct so the selected maximum is unique.'], ['Work from the final position backward.', 'Do not emit a length-1 flip.'], 'O(n^2) time and O(n) space.'),
 'circular-one-grouping': ('Input line 1 is n; line 2 contains n zeros or ones arranged in a circle. Output the minimum number of arbitrary swaps needed to make all ones consecutive; zero or one one needs 0 swaps.', ['Any two positions may be swapped.', 'A consecutive block may cross the end of the input line.'], ['Use a circular window with size equal to the number of ones.', 'Minimise zeros in such a window.'], 'O(n) time and O(n) space.'),
 'exactly-k-distinct': ('Input line 1 is n; line 2 has n integers; line 3 is K. Output the number of non-empty subarrays containing exactly K distinct values.', ['1 <= K <= n.', 'Values may repeat.'], ['Count at most K and at most K-1.', 'Use a frequency map for each sliding window.'], 'O(n) time and O(n) space.'),
 'bounded-range-longest': ('Input line 1 is n; line 2 has n integers; line 3 is limit. Output the maximum length of a contiguous subarray whose maximum minus minimum is at most limit.', ['limit is nonnegative.', 'Values may repeat or be negative.'], ['Maintain monotonic min and max deques.', 'Shrink until the range is valid.'], 'O(n) time and O(n) space.'),
 'online-lower-medians': ('Input line 1 is n; line 2 has n integers. After each prefix, output its lower median (sorted index `(size-1)//2`), separated by spaces.', ['Duplicate values are allowed.', 'Output exactly n medians.'], ['Keep the processed prefix sorted.', 'For a scalable solution use two heaps.'], 'O(n^2) time and O(n) space.'),
 'k-closest-sorted': ('Input line 1 is n; line 2 is sorted ascending; line 3 is `k x`. Choose k values with smallest `(absolute(value-x), value)` order, then output the chosen values sorted ascending, separated by spaces.', ['1 <= k <= n.', 'Values may repeat.'], ['Distance ties choose the smaller value.', 'Sort the selected values before printing.'], 'O(n log n) time and O(n) space.'),
}

_SIZE_BOUNDS = {
 'chemical-formula': '1 <= formula length <= 2,000 characters; serialized CLI input is at most 12,000 characters.',
 'brace-expansion': 'Input length is at most 1,000; expanded output is at most 20,000 characters; serialized CLI input is at most 12,000 characters.',
 'quoted-csv': 'The input record and serialized CLI input are each at most 12,000 characters.',
 'cidr-membership': 'Each IPv4 address has exactly 4 octets, each from 0 through 255.',
 'roman-canonical': '1 <= input length <= 15 characters.',
 'unique-prefixes': '1 <= n <= 1,000, total word length <= 10,000, and serialized CLI input is at most 12,000 characters.',
 'email-normalisation': '1 <= n <= 1,000, total address length <= 10,000, and serialized CLI input is at most 12,000 characters.',
 'text-justify': '1 <= W <= 8,000, text length <= 10,000, serialized CLI input <= 12,000 characters, and output <= 22,000 characters.',
 'wildcard-capture': 'Pattern and text lengths are each at most 2,000, with at most 20 stars.',
 'escaped-codec': 'The payload is at most 10,000 characters; serialized CLI input is at most 12,000 characters and output is at most 20,000 characters.',
 'functional-cycle-data': '1 <= n <= 2,000.',
 'prufer-encode': '2 <= n <= 2,000.',
 'prufer-decode': '2 <= n <= 2,000.',
 'triangle-count': '1 <= n <= 2,000 and 0 <= m <= 20,000.',
 'euler-kind': '1 <= n <= 100,000 and 0 <= m <= 200,000.',
 'complement-components': '1 <= n <= 2,000 and 0 <= m <= 20,000.',
 'dag-query-reachability': '1 <= n <= 2,000; 0 <= m <= 10,000; 1 <= q <= 2,000.',
 'minimum-reversals': '1 <= n <= 100,000 and 0 <= m <= 200,000.',
 'shortest-path-counts': '1 <= n <= 100,000 and 0 <= m <= 200,000.',
 'leaf-removal-rounds': '1 <= n <= 1,500 and m = n - 1; serialized CLI input is at most 12,000 characters and output is at most 22,000 characters.',
 'eight-direction-word-count': '1 <= rows, cols <= 100, rows*cols <= 10,000, word length <= 100, and serialized CLI input is at most 12,000 characters.',
 'latin-square-validation': '1 <= n <= 500, with rows = cols = n.',
 'largest-plus-arm': '1 <= rows, cols <= 100.',
 'toroidal-shortest-path': '1 <= rows, cols <= 500 and rows*cols <= 200,000.',
 'minesweeper-counts': '1 <= rows, cols <= 100, rows*cols <= 10,000, and serialized CLI input is at most 12,000 characters.',
 'conway-life': '1 <= rows, cols <= 200 and 0 <= k <= 500, with k*rows*cols <= 2,000,000.',
 'ring-rotation': '1 <= rows, cols <= 500 and 0 <= k <= 10^9.',
 'diagonal-zigzag': '1 <= rows, cols <= 100, total token characters <= 10,000, and serialized CLI input is at most 12,000 characters.',
 'submatrix-target-count': '1 <= rows, cols <= 40, each integer has at most 9 digits, and serialized CLI input is at most 12,000 characters.',
 'knight-blocked-distance': '1 <= rows, cols <= 500 and rows*cols <= 200,000.',
 'exact-coverage-lengths': '1 <= n <= 150.',
 'point-coverage-queries': '1 <= n, q <= 2,000.',
 'strict-containment-pairs': '1 <= n <= 2,000.',
 'weighted-schedule-witness': '1 <= n <= 14 and serialized CLI input is at most 12,000 characters.',
 'cleanup-room-count': '1 <= n <= 200,000.',
 'strict-nested-chain': '1 <= n <= 2,000.',
 'union-intersection-length': '0 <= n, m <= 100,000 and n+m >= 1.',
 'minimum-target-cover': '1 <= n <= 200,000.',
 'shell-tokenizer': 'The command line and serialized CLI input are each at most 12,000 characters.',
 'parking-ledger': '0 <= q <= 500, each id has at most 20 characters, and serialized CLI input/output are at most 12,000/22,000 characters.',
 'tournament-scoreboard': '0 <= q <= 500, each name has at most 20 characters, and serialized CLI input/output are at most 12,000/22,000 characters.',
 'undo-redo-buffer': '0 <= q <= 100, every APPEND payload is at most 100 characters, and serialized CLI input/output are at most 12,000/22,000 characters.',
 'packet-reassembly': '1 <= total <= 1,000, 0 <= m <= 1,000, each payload is at most 10 characters, and serialized CLI input/output are at most 12,000/22,000 characters.',
 'warehouse-push': '1 <= rows, cols <= 100; rows*cols <= 10,000; commands <= 1,000; serialized CLI input is at most 12,000 characters.',
 'round-robin-completion': '1 <= n <= 1,500, total slices <= 20,000, and serialized CLI input/output are at most 12,000/22,000 characters.',
 'rail-permutation': '1 <= n, q, n*q <= 1,500; serialized CLI input/output are at most 12,000/22,000 characters.',
 'subarray-median-k': '1 <= n <= 200.',
 'shortest-at-least-k': '1 <= n <= 200,000.',
 'one-deletion-max-sum': '1 <= n <= 200,000.',
 'reverse-pair-count': '1 <= n <= 2,000.',
 'next-permutation': '1 <= n <= 1,500, each integer has at most 9 digits, and serialized CLI input/output are at most 12,000/22,000 characters.',
 'pancake-flips': '1 <= n <= 2,000.',
 'circular-one-grouping': '1 <= n <= 200,000.',
 'exactly-k-distinct': '1 <= n <= 200,000.',
 'bounded-range-longest': '1 <= n <= 200,000.',
 'online-lower-medians': '1 <= n <= 1,500, each integer has at most 9 digits, and serialized CLI input/output are at most 12,000/22,000 characters.',
 'k-closest-sorted': '1 <= n <= 1,500, each integer has at most 9 digits, and serialized CLI input/output are at most 12,000/22,000 characters.',
}

# IDs 289--298 are intentionally standalone parsing contracts.  Keep this
# small reference separate so each solution is
# readable when copied into the judge.
_STRING_289_CORE = r'''def answer(mode, text):
 import csv,io,ipaddress,re
 lines=text.splitlines()
 if mode=='chemical-formula':
  s=lines[0];st=[{}];i=0
  while i<len(s):
   if s[i]=='(':st.append({});i+=1
   elif s[i]==')':
    i+=1;j=i
    while j<len(s) and s[j].isdigit():j+=1
    k=int(s[i:j] or 1)
    for a,n in st.pop().items():st[-1][a]=st[-1].get(a,0)+n*k
    i=j
   else:
    j=i+1
    while j<len(s) and s[j].islower():j+=1
    a=s[i:j];k=j
    while k<len(s) and s[k].isdigit():k+=1
    st[-1][a]=st[-1].get(a,0)+int(s[j:k] or 1);i=k
  return ' '.join(a+str(st[0][a]) for a in sorted(st[0]))
 if mode=='brace-expansion':
  s=lines[0];out=[''];i=0
  while i<len(s):
   if s[i]=='{':
    j=s.index('}',i);choices=s[i+1:j].split(',');out=[p+c for p in out for c in choices];i=j+1
   else:out=[p+s[i] for p in out];i+=1
  return ' '.join(sorted(out))
 if mode=='quoted-csv':return '|'.join(next(csv.reader([lines[0]])))
 if mode=='cidr-membership':return 'YES' if ipaddress.ip_address(lines[1]) in ipaddress.ip_network(lines[0],strict=False) else 'NO'
 if mode=='roman-canonical':
  s=lines[0];v={'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000};n=sum((-v[c] if i+1<len(s) and v[c]<v[s[i+1]] else v[c]) for i,c in enumerate(s));pairs=[(1000,'M'),(900,'CM'),(500,'D'),(400,'CD'),(100,'C'),(90,'XC'),(50,'L'),(40,'XL'),(10,'X'),(9,'IX'),(5,'V'),(4,'IV'),(1,'I')];z=''
  for q,c in pairs:z+=c*(n//q);n%=q
  return 'YES' if z==s else 'NO'
 if mode=='unique-prefixes':
  n=int(lines[0]);w=lines[1:1+n];return ' '.join(next(x[:k] for k in range(1,len(x)+1) if sum(y.startswith(x[:k]) for y in w)==1) for x in w)
 if mode=='email-normalisation':
  z=set()
  for x in lines[1:]:
   a,b=x.lower().split('@');z.add(a.split('+')[0].replace('.','')+'@'+b)
  return str(len(z))
 if mode=='text-justify':
  width=int(lines[0]);words=lines[1].split();out=[];row=[];size=0
  for w in words:
   if row and size+len(w)+len(row)>width:
    gaps=max(1,len(row)-1);spaces=width-size;base,extra=divmod(spaces,gaps);out.append(''.join(x+(' '*(base+(i<extra))) for i,x in enumerate(row[:-1]))+row[-1] if len(row)>1 else row[0]+' '*spaces);row=[];size=0
   row.append(w);size+=len(w)
  out.append(' '.join(row)+' '*(width-size-len(row)+1));return '\n'.join(out)
 if mode=='wildcard-capture':
  pattern=lines[0];text=lines[1];parts=pattern.split('*');m=re.fullmatch('(.*?)'.join(re.escape(x) for x in parts),text)
  return '|'.join(m.groups()) if m else 'NO'
 if mode=='escaped-codec':
  action,separator,s=text.partition('\n')
  if action.endswith('\r'):action=action[:-1]
  if not separator:raise ValueError('missing payload separator')
  if s.endswith('\r\n'):s=s[:-2]
  elif s.endswith('\n'):s=s[:-1]
  if action=='E':return s.replace('\\','\\\\').replace('\n','\\n').replace('\t','\\t')
  out='';i=0
  while i<len(s):
   if s[i]=='\\' and i+1<len(s):out+= {'n':'\n','t':'\t','\\':'\\'}[s[i+1]];i+=2
   else:out+=s[i];i+=1
  return out
'''

_STRING_289_SPECS=[
 ('chemical-formula','Canonical chemical formula atom counts',['K4(ON(SO3)2)2','Mg(OH)2','H2O','Be32','(H2O)3','NaCl']),
 ('brace-expansion','Sorted single-level brace expansion',['a{b,c}d','{a,b}{c,d}','x{a,b,c}','plain','{red,blue}','a{1,2}b']),
 ('quoted-csv','Quoted CSV field parser',['a,"b,c",d','"a""b",c','one,two','"",x','"first field",second','last,']),
 ('cidr-membership','IPv4 CIDR range membership',['192.168.1.0/24\n192.168.1.99','10.0.0.0/8\n11.0.0.1','172.16.0.0/12\n172.31.4.2','1.2.3.4/32\n1.2.3.4','1.2.3.4/32\n1.2.3.5','0.0.0.0/0\n255.255.255.255']),
 ('roman-canonical','Canonical Roman numeral validation',['MCMXCIV','IIII','XLII','IC','MMXXVI','VX']),
 ('unique-prefixes','Shortest unique word prefixes',['3\ndog\ndove\nduck','3\ncat\ncar\ndog','3\nalpha\nbeta\ngamma','2\none\nonly','3\nred\nblue\ngreen','3\nabc\nabd\nabe']),
 ('email-normalisation','Normalised email address count',['3\na.b+c@x.com\nab@x.com\nA.B@x.com','2\nx@y.com\nx+z@y.com','1\na@b.com','2\na.b@c.com\na.b+d@c.com','3\na@x.com\na@y.com\na+q@x.com','2\nfoo.bar@z.org\nfoobar@z.org']),
 ('text-justify','Exact-width text justification',['16\nThis is an example of text justification','10\na bb ccc','5\nhello','12\npack my box','8\na b c d','14\nscience is fun']),
 ('wildcard-capture','Wildcard capture extraction',['a*b\naxxb','pre*mid*end\npreXmidYend','a*b\nac','*\nhello','x*y*z\nx1y2z','foo*bar\nfoobar']),
 ('escaped-codec','Reversible escaped-string codec',['E\na\\b','E\nline1\nline2','D\na\\tb','D\nline1\\nline2','E\nplain','D\n\\\\']),]

def _string_289_solution(mode):
    return "import sys\n"+_STRING_289_CORE+"\n\ndef solve():\n print(answer("+repr(mode)+",sys.stdin.read()))\n\nif __name__=='__main__':\n solve()\n"

for _i,(_mode,_title,_cases) in enumerate(_STRING_289_SPECS):
    _fixtures=_literal_fixtures(_FIXTURE_CASES[_mode])
    _description,_constraints,_hints,_complexity=_CONTRACTS[_mode]
    _item=PYTHON_CURATED_289_353[_i]
    _item.update({'title':_title,'concept_token':_mode,'topics':['strings','parsing'],'description':_description,'constraints':_constraints+[_SIZE_BOUNDS[_mode]],'hints':_hints+['Use the public example to check formatting.'],'expected_complexity':_complexity,'solution':_string_289_solution(_mode),'examples':[{'input':_fixtures[0]['input'],'output':_fixtures[0]['expected_output'],'explanation':'The input and output use the stated contract.'}],'public_tests':_fixtures[:2],'hidden_tests':_fixtures[2:]})

_GRAPH_299_CORE = r'''def answer(mode,text):
 from collections import deque
 lines=text.splitlines();n,*rest=map(int,lines[0].split());m=rest[0] if rest else 0
 if mode=='functional-cycle-data':
  nxt=list(map(int,lines[1].split()));out=[]
  for s in range(n):
   seen={};u=s;step=0
   while u not in seen:seen[u]=step;step+=1;u=nxt[u]
   out.append(str(seen[u])+' '+str(step-seen[u]))
  return '\n'.join(out)
 if mode=='prufer-encode':
  g=[set()for _ in range(n)]
  for x in lines[1:]:u,v=map(int,x.split());g[u].add(v);g[v].add(u)
  z=[]
  for _ in range(n-2):
   leaf=min(i for i in range(n) if len(g[i])==1);v=g[leaf].pop();g[v].remove(leaf);z.append(v)
  return ' '.join(map(str,z))
 if mode=='prufer-decode':
  p=list(map(int,lines[1].split())) if n>2 else [];deg=[1]*n
  for x in p:deg[x]+=1
  e=[]
  for x in p:
   leaf=min(i for i in range(n) if deg[i]==1);e.append(tuple(sorted((leaf,x))));deg[leaf]-=1;deg[x]-=1
  a=[i for i in range(n) if deg[i]==1];e.append(tuple(a));return ' '.join(f'{u}-{v}' for u,v in sorted(e))
 es=[tuple(map(int,x.split())) for x in lines[1:1+m]]
 g=[set()for _ in range(n)]
 for u,v in es:
  g[u].add(v)
  if mode!='dag-query-reachability':g[v].add(u)
 if mode=='triangle-count':return str(sum(1 for u in range(n) for v in g[u] if u<v for w in g[u]&g[v] if v<w))
 if mode=='euler-kind':
  active=[i for i in range(n) if g[i]]
  if active:
   seen={active[0]};q=[active[0]]
   for u in q:
    for v in g[u]:
     if v not in seen:seen.add(v);q.append(v)
   if any(x not in seen for x in active):return 'NONE'
  odd=sum(len(x)%2 for x in g);return 'CIRCUIT' if odd==0 else 'TRAIL' if odd==2 else 'NONE'
 if mode=='complement-components':
  unseen=set(range(n));count=0
  while unseen:
   count+=1;q=[unseen.pop()]
   for u in q:
    add=unseen-g[u];unseen-=add;q+=list(add)
  return str(count)
 if mode=='dag-query-reachability':
  q=int(lines[1+m]);queries=[tuple(map(int,x.split())) for x in lines[2+m:]];out=[]
  for s,t in queries:
   seen={s};stack=[s]
   for u in stack:
    for v in g[u]:
     if v not in seen:seen.add(v);stack.append(v)
   out.append('YES' if t in seen else 'NO')
  return ' '.join(out)
 if mode=='minimum-reversals':
  h=[[]for _ in range(n)]
  for u,v in es:h[u].append((v,0));h[v].append((u,1))
  d=[10**9]*n;d[0]=0;q=deque([0])
  while q:
   u=q.popleft()
   for v,w in h[u]:
    if d[u]+w<d[v]:d[v]=d[u]+w;(q.appendleft(v) if w==0 else q.append(v))
  return str(d[-1] if d[-1]<10**9 else -1)
 if mode=='shortest-path-counts':
  s=int(lines[1+m]);d=[-1]*n;ways=[0]*n;d[s]=0;ways[s]=1;q=deque([s])
  while q:
   u=q.popleft()
   for v in g[u]:
    if d[v]<0:d[v]=d[u]+1;q.append(v)
    if d[v]==d[u]+1:ways[v]=(ways[v]+ways[u])%1000000007
  return ' '.join(map(str,ways))
 # tree leaf-removal layers
 deg=[len(x) for x in g];rounds=[0]*n;q=deque(i for i in range(n) if deg[i]<=1)
 while q:
  u=q.popleft()
  for v in g[u]:
   if deg[v]>1:
    deg[v]-=1;rounds[v]=max(rounds[v],rounds[u]+1)
    if deg[v]==1:q.append(v)
  deg[u]=0
 return ' '.join(map(str,rounds))
'''
_GRAPH_299_SPECS=[
 ('functional-cycle-data','Functional graph cycle distance and length',['5\n1 2 0 4 3','4\n1 2 3 3','3\n0 0 1','6\n1 2 3 4 5 2','2\n1 0','1\n0']),
 ('prufer-encode','Encode labelled tree as Prufer sequence',['4\n0 1\n1 2\n1 3','5\n0 1\n0 2\n0 3\n0 4','3\n0 1\n1 2','6\n0 1\n1 2\n2 3\n3 4\n4 5','4\n0 3\n1 3\n2 3','2\n0 1']),
 ('prufer-decode','Decode Prufer sequence to canonical edges',['4\n1 1','5\n0 0 0','3\n1','6\n1 2 3 4','4\n3 3','2\n']),
 ('triangle-count','Count undirected triangles',['4 4\n0 1\n1 2\n2 0\n2 3','4 6\n0 1\n0 2\n0 3\n1 2\n1 3\n2 3','3 2\n0 1\n1 2','5 0','5 5\n0 1\n1 2\n2 3\n3 4\n4 0','3 3\n0 1\n1 2\n0 2']),
 ('euler-kind','Euler trail or circuit classification',['3 3\n0 1\n1 2\n2 0','3 2\n0 1\n1 2','4 2\n0 1\n2 3','4 3\n0 1\n0 2\n0 3','1 0','2 1\n0 1']),
 ('complement-components','Connected components in graph complement',['4 2\n0 1\n2 3','3 3\n0 1\n1 2\n0 2','4 0','3 2\n0 1\n1 2','5 4\n0 1\n0 2\n0 3\n0 4','2 1\n0 1']),
 ('dag-query-reachability','DAG reachability query answers',['4 3\n0 1\n1 2\n0 3\n3\n0 2\n3 2\n0 3','3 2\n0 1\n1 2\n2\n0 2\n2 0','2 0\n1\n0 1','4 2\n0 2\n1 3\n2\n0 3\n1 3','1 0\n1\n0 0','3 1\n0 1\n2\n0 1\n1 2']),
 ('minimum-reversals','Minimum edge reversals from first to last vertex',['4 3\n0 1\n2 1\n2 3','3 2\n1 0\n1 2','2 1\n0 1','3 1\n0 1','4 3\n1 0\n1 2\n3 2','1 0']),
 ('shortest-path-counts','Count shortest paths to every vertex',['4 4\n0 1\n0 2\n1 3\n2 3\n0','3 2\n0 1\n1 2\n0','4 1\n0 1\n0','3 3\n0 1\n1 2\n0 2\n0','2 1\n0 1\n1','1 0\n0']),
 ('leaf-removal-rounds','Leaf-removal round for every tree vertex',['4 3\n0 1\n1 2\n1 3','5 4\n0 1\n1 2\n2 3\n3 4','1 0','4 3\n0 1\n0 2\n0 3','3 2\n0 1\n0 2','6 5\n0 1\n1 2\n1 3\n3 4\n3 5'])]
def _graph_299_solution(mode):return "import sys\n"+_GRAPH_299_CORE+"\n\ndef solve():\n print(answer("+repr(mode)+",sys.stdin.read()))\n\nif __name__=='__main__':\n solve()\n"
for _i,(_mode,_title,_cases) in enumerate(_GRAPH_299_SPECS,10):
 _fixtures=_literal_fixtures(_FIXTURE_CASES[_mode]);_description,_constraints,_hints,_complexity=_CONTRACTS[_mode];_item=PYTHON_CURATED_289_353[_i];_item.update({'title':_title,'concept_token':_mode,'topics':['graphs','graph-theory'],'description':_description,'constraints':_constraints+[_SIZE_BOUNDS[_mode]],'hints':_hints+['Use the public example to check formatting.'],'expected_complexity':_complexity,'solution':_graph_299_solution(_mode),'examples':[{'input':_fixtures[0]['input'],'output':_fixtures[0]['expected_output'],'explanation':'The input and output use the stated contract.'}],'public_tests':_fixtures[:2],'hidden_tests':_fixtures[2:]})


# The final eight Medium drills deliberately teach object-oriented APIs rather
# than another variation of the array-style command exercises above.
def _replace_oop(number, title, topics, description, constraints, hints, complexity, starter, solution, cases, harness, required_class):
    fixtures = [{"input": source, "expected_output": output, "harness": harness} for source, output in cases]
    item = PYTHON_CURATED_289_353[number - 289]
    item.update({"concept_token": f"oop-{number}", "title": title, "topics": ["oop"] + topics,
        "description": description, "constraints": constraints, "hints": hints, "expected_complexity": complexity,
        "starter_code": starter.strip()+"\n", "solution": solution.strip()+"\n",
        "examples": [{"input": fixtures[0]["input"], "output": fixtures[0]["expected_output"], "explanation": "The commands exercise the class API in order."}],
        "public_tests": fixtures[:2], "hidden_tests": fixtures[2:], "submission_mode": "python_class", "required_class": required_class})


_replace_oop(346, "Validated bank account", ["properties", "exceptions"], "Implement BankAccount(initial). Its balance property returns the current nonnegative balance; assigning a negative balance raises ValueError. deposit(amount) and withdraw(amount) reject negative amounts with ValueError, and withdraw also raises ValueError when funds are insufficient. CLI input: line 1 is the initial balance; line 2 is q, the number of commands; the next q lines are exactly `deposit amount`, `withdraw amount`, or `balance`. Each failed deposit or withdrawal prints `ERROR`; each `balance` prints the current balance.", ["Amounts are integers from 0 to 10^9", "At most 100,000 commands"], ["Keep the stored balance private.", "Put validation in the property setter.", "Check a withdrawal before subtracting."], "O(1) per operation and O(1) space", '''class BankAccount:
 def __init__(self, initial): pass
 @property
 def balance(self): pass
 @balance.setter
 def balance(self, value): pass
 def deposit(self, amount): pass
 def withdraw(self, amount): pass
def solve():
 a=BankAccount(int(input()))
 for _ in range(int(input())):
  p=input().split()
  try:
   if p[0]=='deposit':a.deposit(int(p[1]))
   elif p[0]=='withdraw':a.withdraw(int(p[1]))
   else:print(a.balance)
  except ValueError:print('ERROR')
if __name__=='__main__':solve()''', '''class BankAccount:
 def __init__(self, initial): self.balance=initial
 @property
 def balance(self): return self._balance
 @balance.setter
 def balance(self,value):
  if value<0:raise ValueError('negative balance')
  self._balance=value
 def deposit(self,amount):
  if amount<0:raise ValueError('negative deposit')
  self.balance+=amount
 def withdraw(self,amount):
  if amount<0 or amount>self.balance:raise ValueError('invalid withdrawal')
  self.balance-=amount
def solve():
 a=BankAccount(int(input()))
 for _ in range(int(input())):
  p=input().split()
  try:
   if p[0]=='deposit':a.deposit(int(p[1]))
   elif p[0]=='withdraw':a.withdraw(int(p[1]))
   else:print(a.balance)
  except ValueError:print('ERROR')
if __name__=='__main__':solve()''', [("10\n3\ndeposit 5\nwithdraw 8\nbalance\n","7"),("2\n2\nwithdraw 3\nbalance\n","ERROR\n2"),("0\n2\ndeposit 0\nbalance\n","0"),("5\n2\ndeposit -1\nbalance\n","ERROR\n5"),("9\n2\nwithdraw 9\nbalance\n","0"),("1\n2\nwithdraw -1\nbalance\n","ERROR\n1")], '''lines=sys.stdin.read().splitlines();a=submission_class(int(lines[0]))
for line in lines[2:]:
 p=line.split()
 try:
  if p[0]=='deposit':a.deposit(int(p[1]))
  elif p[0]=='withdraw':a.withdraw(int(p[1]))
  else:print(a.balance)
 except ValueError:print('ERROR')''', {"name":"BankAccount","methods":["__init__","balance","deposit","withdraw"]})

_replace_oop(347, "Shopping cart composition", ["composition", "collections"], "Implement LineItem(name, price, quantity) and ShoppingCart(). add(item) stores a LineItem, total() returns the total cost, and item_count() returns the total quantities. CLI input: line 1 is q, the number of commands; the next q lines are exactly `add name price quantity`, `total`, or `count`. Each `total` prints total cost and each `count` prints total quantity.", ["Prices and quantities are nonnegative integers", "At most 100,000 items"], ["LineItem stores one purchase line.", "The cart owns a list of LineItems.", "Multiply price by quantity for each line."], "O(n) total, O(1) item_count after maintaining a count, and O(n) space", '''class LineItem:
 def __init__(self,name,price,quantity):pass
class ShoppingCart:
 def __init__(self):pass
 def add(self,item):pass
 def total(self):pass
 def item_count(self):pass
def solve():
 c=ShoppingCart()
 for _ in range(int(input())):
  p=input().split()
  if p[0]=='add':c.add(LineItem(p[1],int(p[2]),int(p[3])))
  elif p[0]=='total':print(c.total())
  else:print(c.item_count())
if __name__=='__main__':solve()''', '''class LineItem:
 def __init__(self,name,price,quantity):self.name=name;self.price=price;self.quantity=quantity
class ShoppingCart:
 def __init__(self):self.items=[];self.count=0
 def add(self,item):self.items.append(item);self.count+=item.quantity
 def total(self):return sum(item.price*item.quantity for item in self.items)
 def item_count(self):return self.count
def solve():
 c=ShoppingCart()
 for _ in range(int(input())):
  p=input().split()
  if p[0]=='add':c.add(LineItem(p[1],int(p[2]),int(p[3])))
  elif p[0]=='total':print(c.total())
  else:print(c.item_count())
if __name__=='__main__':solve()''', [("4\nadd pen 2 3\nadd book 5 1\ntotal\ncount\n","11\n4"),("2\nadd free 0 4\ntotal\n","0"),("3\nadd apple 3 2\ncount\ntotal\n","2\n6"),("3\nadd x 1 0\ncount\ntotal\n","0\n0"),("4\nadd a 1 1\nadd b 2 2\nadd c 3 3\ntotal\n","14"),("2\nadd z 9 1\ncount\n","1")], '''lines=sys.stdin.read().splitlines();c=submission_class();Item=submission_module.LineItem
for line in lines[1:]:
 p=line.split()
 if p[0]=='add':c.add(Item(p[1],int(p[2]),int(p[3])))
 elif p[0]=='total':print(c.total())
 else:print(c.item_count())''', {"name":"ShoppingCart","methods":["__init__","add","total","item_count"]})

_replace_oop(348, "Undoable text buffer", ["dunder-methods", "state"], "Implement TextBuffer(). append(text) adds text, undo() removes the most recently appended whole text and returns it or an empty string, len(buffer) returns the character count, and str(buffer) returns all text. CLI input: line 1 is q, the number of commands; the next q lines are exactly `append text`, `undo`, `length`, or `text`. `undo`, `length`, and `text` each print their returned value.", ["At most 100,000 append commands and 1,000,000 total characters", "Appended text has no spaces"], ["Keep appended pieces in a stack.", "undo pops one piece only.", "__str__ can join the stored pieces."], "O(1) undo and length, O(total characters) str, and O(total characters) space", '''class TextBuffer:
 def __init__(self):pass
 def append(self,text):pass
 def undo(self):pass
 def __len__(self):pass
 def __str__(self):pass
def solve():
 b=TextBuffer()
 for _ in range(int(input())):
  p=input().split()
  if p[0]=='append':b.append(p[1])
  elif p[0]=='undo':print(b.undo())
  elif p[0]=='length':print(len(b))
  else:print(str(b))
if __name__=='__main__':solve()''', '''class TextBuffer:
 def __init__(self):self.parts=[];self.length=0
 def append(self,text):self.parts.append(text);self.length+=len(text)
 def undo(self):
  if not self.parts:return ''
  text=self.parts.pop();self.length-=len(text);return text
 def __len__(self):return self.length
 def __str__(self):return ''.join(self.parts)
def solve():
 b=TextBuffer()
 for _ in range(int(input())):
  p=input().split()
  if p[0]=='append':b.append(p[1])
  elif p[0]=='undo':print(b.undo())
  elif p[0]=='length':print(len(b))
  else:print(str(b))
if __name__=='__main__':solve()''', [("4\nappend hi\nappend there\nlength\ntext\n","7\nhithere"),("3\nappend x\nundo\ntext\n","x"),("2\nundo\nlength\n","\n0"),("4\nappend a\nappend bc\nundo\ntext\n","bc\na"),("3\nappend hello\nlength\nundo\n","5\nhello"),("3\nappend a\nappend b\nlength\n","2")], '''b=submission_class()
for line in sys.stdin.read().splitlines()[1:]:
 p=line.split()
 if p[0]=='append':b.append(p[1])
 elif p[0]=='undo':print(b.undo())
 elif p[0]=='length':print(len(b))
 else:print(str(b))''', {"name":"TextBuffer","methods":["__init__","append","undo","__len__","__str__"]})

_replace_oop(349, "Iterable playlist", ["dunder-methods", "collections"], "Implement Playlist(). add(song) appends a song, iter(playlist) yields songs in added order, and song in playlist checks membership. CLI input: line 1 is q, the number of commands; the next q lines are exactly `add song`, `list`, or `has song`. `list` prints songs in added order and `has` prints `True` or `False`.", ["At most 100,000 songs", "Song names are lowercase words"], ["Store songs in a list.", "__iter__ returns an iterator over the list.", "__contains__ can use membership in the list."], "O(1) add, O(n) membership, and O(n) space", '''class Playlist:
 def __init__(self):pass
 def add(self,song):pass
 def __iter__(self):pass
 def __contains__(self,song):pass
def solve():
 p=Playlist()
 for _ in range(int(input())):
  x=input().split()
  if x[0]=='add':p.add(x[1])
  elif x[0]=='list':print(' '.join(p))
  else:print(x[1] in p)
if __name__=='__main__':solve()''', '''class Playlist:
 def __init__(self):self.songs=[]
 def add(self,song):self.songs.append(song)
 def __iter__(self):return iter(self.songs)
 def __contains__(self,song):return song in self.songs
def solve():
 p=Playlist()
 for _ in range(int(input())):
  x=input().split()
  if x[0]=='add':p.add(x[1])
  elif x[0]=='list':print(' '.join(p))
  else:print(x[1] in p)
if __name__=='__main__':solve()''', [("4\nadd one\nadd two\nlist\nhas two\n","one two\nTrue"),("2\nhas none\nlist\n","False"),("3\nadd a\nhas b\nlist\n","False\na"),("3\nadd x\nadd x\nlist\n","x x"),("2\nadd jazz\nhas jazz\n","True"),("3\nadd first\nadd last\nhas first\n","True")], '''p=submission_class()
for line in sys.stdin.read().splitlines()[1:]:
 x=line.split()
 if x[0]=='add':p.add(x[1])
 elif x[0]=='list':print(' '.join(p))
 else:print(x[1] in p)''', {"name":"Playlist","methods":["__init__","add","__iter__","__contains__"]})

_replace_oop(350, "Polymorphic shape areas", ["inheritance", "polymorphism"], "Implement Shape with area(), plus Circle(radius) and Rectangle(width, height) subclasses that override area(). CLI input: line 1 is q, the number of shapes; the next q lines are exactly `circle radius` or `rectangle width height`. Print one integer area per shape in input order; for this exercise a circle uses pi = 3.", ["Dimensions are nonnegative integers no greater than 10^6", "At most 100,000 shapes"], ["Both subclasses inherit from Shape.", "Override area in each subclass.", "A list of Shape values can call area polymorphically."], "O(1) per area and O(n) space for the CLI list", '''class Shape:
 def area(self):pass
class Circle(Shape):
 def __init__(self,radius):pass
 def area(self):pass
class Rectangle(Shape):
 def __init__(self,width,height):pass
 def area(self):pass
def solve():
 for _ in range(int(input())):
  p=input().split();s=Circle(int(p[1])) if p[0]=='circle' else Rectangle(int(p[1]),int(p[2]));print(s.area())
if __name__=='__main__':solve()''', '''class Shape:
 def area(self):raise NotImplementedError
class Circle(Shape):
 def __init__(self,radius):self.radius=radius
 def area(self):return 3*self.radius*self.radius
class Rectangle(Shape):
 def __init__(self,width,height):self.width=width;self.height=height
 def area(self):return self.width*self.height
def solve():
 for _ in range(int(input())):
  p=input().split();s=Circle(int(p[1])) if p[0]=='circle' else Rectangle(int(p[1]),int(p[2]));print(s.area())
if __name__=='__main__':solve()''', [("2\ncircle 2\nrectangle 3 4\n","12\n12"),("1\nrectangle 0 8\n","0"),("1\ncircle 0\n","0"),("2\nrectangle 5 1\ncircle 3\n","5\n27"),("1\nrectangle 9 9\n","81"),("2\ncircle 1\nrectangle 2 7\n","3\n14")], '''for line in sys.stdin.read().splitlines()[1:]:
 assert issubclass(submission_module.Circle,submission_class) and issubclass(submission_module.Rectangle,submission_class)
 p=line.split();shape=submission_module.Circle(int(p[1])) if p[0]=='circle' else submission_module.Rectangle(int(p[1]),int(p[2]));print(shape.area())''', {"name":"Shape","methods":["area"]})

_replace_oop(351, "Priority task ordering", ["dunder-methods", "ordering"], "Implement Task(name, priority). Lower priority numbers come first; ties use name alphabetically. __lt__ supplies that ordering and __eq__ compares both fields. CLI input: line 1 is q, the number of tasks; each of the next q lines is exactly `name priority`. Print all task names on one line in sorted order, separated by spaces.", ["At most 100,000 tasks", "Priorities are signed integers and names are lowercase words"], ["Compare priority before name.", "__eq__ should compare both stored fields.", "sorted calls __lt__."], "O(n log n) time for sorting and O(n) space", '''class Task:
 def __init__(self,name,priority):pass
 def __lt__(self,other):pass
 def __eq__(self,other):pass
def solve():
 tasks=[Task(*((lambda p:(p[0],int(p[1])))(input().split()))) for _ in range(int(input()))]
 print(' '.join(t.name for t in sorted(tasks)))
if __name__=='__main__':solve()''', '''class Task:
 def __init__(self,name,priority):self.name=name;self.priority=priority
 def __lt__(self,other):return (self.priority,self.name)<(other.priority,other.name)
 def __eq__(self,other):return isinstance(other,Task) and (self.priority,self.name)==(other.priority,other.name)
def solve():
 tasks=[Task(*((lambda p:(p[0],int(p[1])))(input().split()))) for _ in range(int(input()))]
 print(' '.join(t.name for t in sorted(tasks)))
if __name__=='__main__':solve()''', [("3\nwrite 2\nread 1\ncall 2\n","read call write"),("1\none 0\n","one"),("2\na 1\nb 1\n","a b"),("3\nx -1\ny -2\nz 0\n","y x z"),("2\nsame 3\nsame 3\n","same same"),("3\nc 5\nb 5\na 5\n","a b c")], '''tasks=[]
for line in sys.stdin.read().splitlines()[1:]:
 name,priority=line.split();tasks.append(submission_class(name,int(priority)))
print(' '.join(task.name for task in sorted(tasks)))
if len(tasks)>1: assert (tasks[0]==tasks[1]) == (tasks[0].name==tasks[1].name and tasks[0].priority==tasks[1].priority)''', {"name":"Task","methods":["__init__","__lt__","__eq__"]})

_replace_oop(352, "Ordered event emitter", ["callbacks", "state"], "Implement EventEmitter(). subscribe(event, callback) registers a callback and emit(event, value) calls registered callbacks in subscription order, returning their results as a list. CLI input: line 1 is q, the number of commands; the next q lines are exactly `sub event double`, `sub event label`, or `emit event value`. `double` returns value*2, `label` returns `tag` followed by value, and every `emit` prints its results in subscription order separated by spaces.", ["At most 100,000 subscriptions and emissions", "Event names are lowercase words"], ["Map each event to a callback list.", "append preserves subscription order.", "emit uses an empty list for an unknown event."], "O(k) per emit with k callbacks for that event and O(subscriptions) space", '''class EventEmitter:
 def __init__(self):pass
 def subscribe(self,event,callback):pass
 def emit(self,event,value):pass
def solve():
 e=EventEmitter()
 for _ in range(int(input())):
  p=input().split()
  if p[0]=='sub':e.subscribe(p[1],(lambda x:x*2) if p[2]=='double' else (lambda x:'tag'+str(x)))
  else:print(' '.join(map(str,e.emit(p[1],int(p[2])))))
if __name__=='__main__':solve()''', '''class EventEmitter:
 def __init__(self):self.listeners={}
 def subscribe(self,event,callback):self.listeners.setdefault(event,[]).append(callback)
 def emit(self,event,value):return [callback(value) for callback in self.listeners.get(event,[])]
def solve():
 e=EventEmitter()
 for _ in range(int(input())):
  p=input().split()
  if p[0]=='sub':e.subscribe(p[1],(lambda x:x*2) if p[2]=='double' else (lambda x:'tag'+str(x)))
  else:print(' '.join(map(str,e.emit(p[1],int(p[2])))))
if __name__=='__main__':solve()''', [("3\nsub go double\nsub go label\nemit go 4\n","8 tag4"),("1\nemit none 2\n",""),("3\nsub a label\nsub a double\nemit a 3\n","tag3 6"),("2\nsub a double\nemit a 0\n","0"),("3\nsub x double\nemit x 5\nemit x 1\n","10\n2"),("2\nsub z label\nemit z 7\n","tag7")], '''e=submission_class()
for line in sys.stdin.read().splitlines()[1:]:
 p=line.split()
 if p[0]=='sub':e.subscribe(p[1],(lambda x:x*2) if p[2]=='double' else (lambda x:'tag'+str(x)))
 else:print(' '.join(map(str,e.emit(p[1],int(p[2])))))''', {"name":"EventEmitter","methods":["__init__","subscribe","emit"]})

_replace_oop(353, "Library book composition", ["composition", "state"], "Implement Book(title) and Library(). add(book) stores a Book, borrow(title) returns True and makes an available book unavailable or returns False, return_book(title) makes a stored book available, and available() returns available titles in added order. CLI input: line 1 is q, the number of commands; the next q lines are exactly `add title`, `borrow title`, `return title`, or `available`. Each `borrow` prints `True` or `False`; each `available` prints available titles in added order separated by spaces.", ["At most 100,000 books and commands", "Titles are lowercase words"], ["A Library owns Book instances.", "A Book needs an availability state.", "Borrow changes only the first matching available book."], "O(n) borrow/return/available and O(n) space", '''class Book:
 def __init__(self,title):pass
class Library:
 def __init__(self):pass
 def add(self,book):pass
 def borrow(self,title):pass
 def return_book(self,title):pass
 def available(self):pass
def solve():
 l=Library()
 for _ in range(int(input())):
  p=input().split()
  if p[0]=='add':l.add(Book(p[1]))
  elif p[0]=='borrow':print(l.borrow(p[1]))
  elif p[0]=='return':l.return_book(p[1])
  else:print(' '.join(l.available()))
if __name__=='__main__':solve()''', '''class Book:
 def __init__(self,title):self.title=title;self.is_available=True
class Library:
 def __init__(self):self.books=[]
 def add(self,book):self.books.append(book)
 def borrow(self,title):
  for book in self.books:
   if book.title==title and book.is_available:book.is_available=False;return True
  return False
 def return_book(self,title):
  for book in self.books:
   if book.title==title:book.is_available=True;return
 def available(self):return [book.title for book in self.books if book.is_available]
def solve():
 l=Library()
 for _ in range(int(input())):
  p=input().split()
  if p[0]=='add':l.add(Book(p[1]))
  elif p[0]=='borrow':print(l.borrow(p[1]))
  elif p[0]=='return':l.return_book(p[1])
  else:print(' '.join(l.available()))
if __name__=='__main__':solve()''', [("4\nadd dune\nborrow dune\navailable\nreturn dune\n","True"),("3\nadd a\nborrow b\navailable\n","False\na"),("4\nadd a\nadd b\nborrow a\navailable\n","True\nb"),("4\nadd x\nborrow x\nreturn x\navailable\n","True\nx"),("3\nadd a\nadd a\nborrow a\n","True"),("2\nadd z\navailable\n","z")], '''l=submission_class();Book=submission_module.Book
for line in sys.stdin.read().splitlines()[1:]:
 p=line.split()
 if p[0]=='add':l.add(Book(p[1]))
 elif p[0]=='borrow':print(l.borrow(p[1]))
 elif p[0]=='return':l.return_book(p[1])
 else:print(' '.join(l.available()))''', {"name":"Library","methods":["__init__","add","borrow","return_book","available"]})

_GRID_309_CORE=r'''def answer(mode,text):
 from collections import deque,Counter
 lines=text.splitlines();r,c=map(int,lines[0].split())
 if mode=='eight-direction-word-count':word=lines[1];a=lines[2:2+r];return str(sum(all(0<=i+d*x<r and 0<=j+e*x<c and a[i+d*x][j+e*x]==word[x] for x in range(len(word))) for i in range(r) for j in range(c) for d,e in ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))))
 if mode=='latin-square-validation':
  a=[list(map(int,x.split())) for x in lines[1:1+r]];want=set(range(1,r+1));return 'YES' if all(set(x)==want for x in a) and all({a[i][j] for i in range(r)}==want for j in range(r)) else 'NO'
 if mode=='largest-plus-arm':
  a=lines[1:1+r];best=0
  for i in range(r):
   for j in range(c):
    k=0
    while i-k>=0 and i+k<r and j-k>=0 and j+k<c and all(a[x][y]=='1' for x,y in ((i-k,j),(i+k,j),(i,j-k),(i,j+k))):best=max(best,k+1);k+=1
  return str(best)
 if mode in {'toroidal-shortest-path','knight-blocked-distance'}:
  a=lines[1:1+r];s=tuple(map(int,lines[1+r].split()));t=tuple(map(int,lines[2+r].split()));q=deque([s]);d={s:0};steps=((-1,0),(1,0),(0,-1),(0,1)) if mode[0]=='t' else ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
  while q:
   x,y=q.popleft()
   for dx,dy in steps:
    u,v=((x+dx)%r,(y+dy)%c) if mode[0]=='t' else (x+dx,y+dy)
    if 0<=u<r and 0<=v<c and a[u][v]!='#' and (u,v) not in d:d[u,v]=d[x,y]+1;q.append((u,v))
  return str(d.get(t,-1))
 if mode=='minesweeper-counts':
  a=lines[1:1+r];return '\n'.join(''.join('*' if a[i][j]=='*' else str(sum(0<=i+x<r and 0<=j+y<c and a[i+x][j+y]=='*' for x in (-1,0,1) for y in (-1,0,1))) for j in range(c)) for i in range(r))
 if mode=='conway-life':
  k=int(lines[1]);a=[list(x) for x in lines[2:2+r]]
  for _ in range(k):a=[['#' if (sum(0<=i+x<r and 0<=j+y<c and a[i+x][j+y]=='#' for x in (-1,0,1) for y in (-1,0,1) if (x,y)!=(0,0))==3 or a[i][j]=='#' and sum(0<=i+x<r and 0<=j+y<c and a[i+x][j+y]=='#' for x in (-1,0,1) for y in (-1,0,1) if (x,y)!=(0,0))==2) else '.' for j in range(c)] for i in range(r)]
  return '\n'.join(''.join(x) for x in a)
 if mode=='ring-rotation':
  k=int(lines[1]);a=[list(map(int,x.split())) for x in lines[2:2+r]]
  for z in range(min(r,c)//2):
   p=[(z,j) for j in range(z,c-z)]+[(i,c-z-1) for i in range(z+1,r-z)]+[(r-z-1,j) for j in range(c-z-2,z-1,-1)]+[(i,z) for i in range(r-z-2,z,-1)];v=[a[i][j] for i,j in p];v=v[-k%len(v):]+v[:-k%len(v)]
   for (i,j),x in zip(p,v):a[i][j]=x
  return '\n'.join(' '.join(map(str,x)) for x in a)
 if mode=='diagonal-zigzag':
  a=[x.split() for x in lines[1:1+r]];z=[]
  for s in range(r+c-1):
   q=[a[i][s-i] for i in range(max(0,s-c+1),min(r-1,s)+1)];z+=q[::-1] if s%2==0 else q
  return ' '.join(z)
 a=[list(map(int,x.split())) for x in lines[2:2+r]];target=int(lines[1]);out=0
 for top in range(r):
  col=[0]*c
  for bot in range(top,r):
   for j in range(c):col[j]+=a[bot][j]
   seen=Counter({0:1});s=0
   for x in col:s+=x;out+=seen[s-target];seen[s]+=1
 return str(out)
'''
_GRID_309_SPECS=[
('eight-direction-word-count','Count word occurrences in eight directions',['3 3\nABA\nABA\nBAB\nABA','2 2\nAA\nAA\nAA','1 4\nABC\nABCA','3 3\nCAT\nCAT\nAAA\nTTT','2 3\nDOG\nDOG\nGOD','1 1\nZ\nZ']),
('latin-square-validation','Validate a Latin square',['3 3\n1 2 3\n2 3 1\n3 1 2','2 2\n1 1\n2 2','1 1\n1','3 3\n1 2 3\n3 1 2\n2 3 1','2 2\n1 2\n2 1','3 3\n1 2 3\n2 1 3\n3 3 1']),
('largest-plus-arm','Largest all-one plus-sign arm length',['3 3\n111\n111\n111','3 3\n010\n111\n010','2 2\n11\n11','1 4\n1111','3 5\n00100\n11111\n00100','2 3\n000\n000']),
('toroidal-shortest-path','Toroidal blocked-grid shortest path',['3 3\n...\n.#.\n...\n0 0\n2 2','2 2\n..\n..\n0 0\n1 1','2 2\n.#\n##\n0 0\n1 1','1 3\n...\n0 0\n0 2','3 1\n.\n.\n.\n0 0\n2 0','2 3\n...\n...\n0 1\n1 1']),
('minesweeper-counts','Generate Minesweeper neighbour counts',['2 2\n*.\n..','1 3\n*.*','3 3\n...\n.*.\n...','1 1\n.','2 3\n..*\n...','2 2\n**\n**']),
('conway-life','Conway Life after k steps',['3 3\n1\n...\n###\n...','3 3\n1\n.#.\n.#.\n.#.','2 2\n2\n##\n##','1 1\n1\n#','3 3\n0\n#..\n...\n..#','3 3\n1\n...\n...\n...']),
('ring-rotation','Rotate concentric matrix rings',['2 2\n1\n1 2\n3 4','3 3\n2\n1 2 3\n4 5 6\n7 8 9','1 3\n5\n1 2 3','2 3\n1\n1 2 3\n4 5 6','4 4\n1\n1 2 3 4\n5 6 7 8\n9 10 11 12\n13 14 15 16','1 1\n3\n7']),
('diagonal-zigzag','Diagonal zigzag matrix traversal',['2 3\n1 2 3\n4 5 6','1 1\nx','3 1\na\nb\nc','2 2\n1 2\n3 4','3 2\na b\nc d\ne f','1 4\na b c d']),
('submatrix-target-count','Count target-sum submatrices',['2 2\n0\n1 -1\n-1 1','1 3\n3\n1 1 1','2 1\n1\n1\n1','2 2\n2\n1 1\n1 1','1 1\n0\n0','2 3\n3\n1 2 0\n0 1 2']),
('knight-blocked-distance','Minimum knight moves on blocked board',['3 3\n...\n...\n...\n0 0\n2 1','3 3\n...\n.#.\n...\n0 0\n2 2','1 1\n.\n0 0\n0 0','2 3\n...\n...\n0 0\n1 2','3 3\n.##\n###\n##.\n0 0\n2 2','4 4\n....\n....\n....\n....\n0 0\n3 3'])]
def _grid_309_solution(mode):return "import sys\n"+_GRID_309_CORE+"\n\ndef solve():\n print(answer("+repr(mode)+",sys.stdin.read()))\n\nif __name__=='__main__':\n solve()\n"
for _i,(_mode,_title,_cases) in enumerate(_GRID_309_SPECS,20):
 _fixtures=_literal_fixtures(_FIXTURE_CASES[_mode]);_description,_constraints,_hints,_complexity=_CONTRACTS[_mode];_item=PYTHON_CURATED_289_353[_i];_item.update({'title':_title,'concept_token':_mode,'topics':['grids','matrix'],'description':_description,'constraints':_constraints+[_SIZE_BOUNDS[_mode]],'hints':_hints+['Use the public example to check formatting.'],'expected_complexity':_complexity,'solution':_grid_309_solution(_mode),'examples':[{'input':_fixtures[0]['input'],'output':_fixtures[0]['expected_output'],'explanation':'The input and output use the stated contract.'}],'public_tests':_fixtures[:2],'hidden_tests':_fixtures[2:]})

_INTERVAL_319_CORE=r'''def answer(mode,text):
 import itertools
 lines=text.splitlines();head=list(map(int,lines[0].split()));n=head[0]
 if mode=='point-coverage-queries':
  q=head[1];a=[tuple(map(int,x.split())) for x in lines[1:1+n]];return ' '.join(str(sum(l<=int(x)<r for l,r in a)) for x in lines[1+n:1+n+q])
 if mode=='union-intersection-length':
  m=head[1];a=[tuple(map(int,x.split())) for x in lines[1:1+n]];b=[tuple(map(int,x.split())) for x in lines[1+n:1+n+m]]
  def merge(x):
   z=[]
   for l,r in sorted(x):
    if z and l<=z[-1][1]:z[-1]=(z[-1][0],max(r,z[-1][1]))
    else:z.append((l,r))
   return z
  a,b=merge(a),merge(b);i=j=out=0
  while i<len(a) and j<len(b):
   out+=max(0,min(a[i][1],b[j][1])-max(a[i][0],b[j][0]))
   if a[i][1]<b[j][1]:i+=1
   else:j+=1
  return str(out)
 if mode=='minimum-target-cover':
  L,R=head[1:];a=sorted(tuple(map(int,x.split())) for x in lines[1:]);cur=L;i=used=0
  while cur<R:
   far=cur
   while i<len(a) and a[i][0]<=cur:far=max(far,a[i][1]);i+=1
   if far==cur:return '-1'
   cur=far;used+=1
  return str(used)
 a=[tuple(map(int,x.split())) for x in lines[1:1+n]]
 if mode=='exact-coverage-lengths':
  e=sorted({x for p in a for x in p});out=[]
  for k in range(1,n+1):out.append(sum(e[i+1]-e[i] for i in range(len(e)-1) if sum(l<=e[i] and e[i+1]<=r for l,r in a)==k))
  return ' '.join(map(str,out))
 if mode=='strict-containment-pairs':return str(sum(a[i][0]<a[j][0] and a[j][1]<a[i][1] for i in range(n) for j in range(n) if i!=j))
 if mode=='weighted-schedule-witness':
  best=(0,())
  for mask in range(1<<n):
   z=tuple(i for i in range(n) if mask>>i&1)
   if all(a[i][1]<=a[j][0] or a[j][1]<=a[i][0] for i,j in itertools.combinations(z,2)):
    q=(sum(a[i][2] for i in z),z)
    if q[0]>best[0] or q[0]==best[0] and q[1]<best[1]:best=q
  return str(best[0])+' | '+' '.join(map(str,best[1]))
 if mode=='cleanup-room-count':
  e=[]
  for s,t,c in a:e.extend(((s,1),(t+c,-1)))
  cur=best=0
  for _,d in sorted(e,key=lambda x:(x[0],x[1])):cur+=d;best=max(best,cur)
  return str(best)
 # strict nesting chain
 a=sorted(a,key=lambda x:(x[0],-x[1]));d=[1]*n
 for i in range(n):d[i]=1+max((d[j] for j in range(n) if a[j][0]<a[i][0] and a[i][1]<a[j][1]),default=0)
 return str(max(d,default=0))
'''
_INTERVAL_319_SPECS=[
('exact-coverage-lengths','Exact half-open coverage lengths',['3\n0 4\n1 3\n2 5','2\n0 1\n1 2','1\n2 7','3\n0 10\n2 4\n6 8','2\n0 5\n0 5','4\n0 2\n1 3\n2 4\n3 5']),
('point-coverage-queries','Half-open interval point coverage queries',['2 3\n0 3\n2 5\n0\n2\n5','1 2\n1 2\n1\n2','3 1\n0 10\n2 4\n6 8\n3','2 2\n-2 0\n0 2\n-1\n0','1 1\n5 5\n5','3 3\n1 4\n1 4\n1 4\n1\n3\n4']),
('strict-containment-pairs','Count strict interval containment pairs',['3\n0 5\n1 4\n2 3','2\n0 1\n0 1','1\n0 2','3\n0 10\n1 2\n3 4','2\n1 3\n0 4','3\n0 3\n1 2\n1 2']),
('weighted-schedule-witness','Weighted half-open schedule with witness',['3\n0 2 5\n2 4 5\n0 4 9','2\n0 1 3\n1 2 3','1\n0 3 7','3\n0 2 4\n1 3 10\n3 4 4','2\n0 5 1\n0 5 2','3\n0 1 1\n1 2 1\n2 3 1']),
('cleanup-room-count','Meeting rooms with cleanup',['2\n0 2 1\n2 4 1','2\n0 2 0\n2 3 0','3\n0 5 2\n1 2 0\n4 6 0','1\n1 1 2','3\n0 1 5\n2 3 0\n4 5 0','2\n-1 0 1\n0 1 1']),
('strict-nested-chain','Longest strictly nested interval chain',['3\n0 10\n1 9\n2 8','2\n0 1\n1 2','1\n0 2','4\n0 8\n1 7\n2 6\n3 5','3\n0 5\n0 4\n1 3','2\n-2 2\n-1 1']),
('union-intersection-length','Intersection length of two unions',['2 2\n0 3\n5 8\n1 6\n7 9','1 1\n0 1\n1 2','2 1\n0 5\n2 7\n3 4','1 2\n0 10\n2 3\n4 5','1 1\n0 0\n0 1','2 2\n0 2\n4 6\n2 4\n6 8']),
('minimum-target-cover','Minimum continuous target cover',['3 0 5\n0 2\n1 4\n4 5','2 0 3\n0 1\n2 3','1 1 2\n0 3','3 0 10\n0 4\n4 8\n8 10','2 -1 1\n-1 0\n0 1','2 0 1\n0 1\n0 1'])]
def _interval_319_solution(mode):return "import sys\n"+_INTERVAL_319_CORE+"\n\ndef solve():\n print(answer("+repr(mode)+",sys.stdin.read()))\n\nif __name__=='__main__':\n solve()\n"
for _i,(_mode,_title,_cases) in enumerate(_INTERVAL_319_SPECS,30):
 _fixtures=_literal_fixtures(_FIXTURE_CASES[_mode]);_description,_constraints,_hints,_complexity=_CONTRACTS[_mode];_item=PYTHON_CURATED_289_353[_i];_item.update({'title':_title,'concept_token':_mode,'topics':['intervals','sweep-line'],'description':_description,'constraints':_constraints+[_SIZE_BOUNDS[_mode]],'hints':_hints+['Use the public example to check formatting.'],'expected_complexity':_complexity,'solution':_interval_319_solution(_mode),'examples':[{'input':_fixtures[0]['input'],'output':_fixtures[0]['expected_output'],'explanation':'The input and output use the stated contract.'}],'public_tests':_fixtures[:2],'hidden_tests':_fixtures[2:]})

_SIM_327_CORE=r'''def answer(mode,text):
 import shlex
 from collections import deque,defaultdict
 lines=text.splitlines()
 if mode=='shell-tokenizer':return '|'.join(shlex.split(lines[0]))
 if mode=='parking-ledger':
  rate,q=map(int,lines[0].split());active={};out=[]
  for x in lines[1:1+q]:
   op,i,t=x.split();t=int(t)
   if op=='ENTER':active[i]=t
   elif i in active:out.append(i+' '+str((t-active.pop(i))*rate))
  return '\n'.join(out+['ACTIVE '+' '.join(sorted(active))])
 if mode=='tournament-scoreboard':
  d=defaultdict(int)
  for x in lines[1:]:
   p=x.split()
   if p[0]=='WIN':d[p[1]]+=3
   else:d[p[1]]+=1;d[p[2]]+=1
  return ' '.join(k+':'+str(v) for k,v in sorted(d.items(),key=lambda x:(-x[1],x[0])))
 if mode=='undo-redo-buffer':
  s='';undo=[];redo=[]
  for x in lines[1:]:
   p=x.split(' ',1);op=p[0]
   if op=='APPEND':undo.append(s);s+=p[1];redo=[]
   elif op=='DELETE':undo.append(s);s=s[:-int(p[1])];redo=[]
   elif op=='UNDO' and undo:redo.append(s);s=undo.pop()
   elif op=='REDO' and redo:undo.append(s);s=redo.pop()
  return s
 if mode=='packet-reassembly':
  total,m=map(int,lines[0].split());d={}
  for x in lines[1:1+m]:i,p=x.split(' ',1);d.setdefault(int(i),p)
  miss=[str(i) for i in range(total) if i not in d];return 'MISSING '+' '.join(miss) if miss else ''.join(d[i] for i in range(total))
 if mode=='warehouse-push':
  r,c=map(int,lines[0].split());a=lines[1:1+r];cmd=lines[1+r];robot=next((i,j) for i in range(r) for j in range(c) if a[i][j]=='@');box=next((i,j) for i in range(r) for j in range(c) if a[i][j]=='B');ds={'U':(-1,0),'D':(1,0),'L':(0,-1),'R':(0,1)}
  for z in cmd:
   x,y=robot[0]+ds[z][0],robot[1]+ds[z][1]
   if not(0<=x<r and 0<=y<c) or a[x][y]=='#':continue
   if (x,y)==box:
    q=(x+ds[z][0],y+ds[z][1])
    if not(0<=q[0]<r and 0<=q[1]<c) or a[q[0]][q[1]]=='#':continue
    box=q
   robot=(x,y)
  return f'{robot[0]} {robot[1]} | {box[0]} {box[1]}'
 if mode=='round-robin-completion':
  n,q=map(int,lines[0].split());jobs=[tuple(map(int,x.split()))+(i,) for i,x in enumerate(lines[1:1+n])];jobs.sort(key=lambda job:(job[0],job[2]));clock=0;i=0;ready=deque();done=[0]*n
  while i<n or ready:
   if not ready:clock=max(clock,jobs[i][0])
   while i<n and jobs[i][0]<=clock:ready.append(jobs[i]);i+=1
   at,left,idx=ready.popleft();run=min(q,left);clock+=run;left-=run
   while i<n and jobs[i][0]<=clock:ready.append(jobs[i]);i+=1
   if left:ready.append((at,left,idx))
   else:done[idx]=clock
  return ' '.join(map(str,done))
 n,q=map(int,lines[0].split());out=[]
 for x in lines[1:1+q]:
  st=[];want=list(map(int,x.split()));nextcar=1
  for v in want:
   while nextcar<=n and nextcar!=v:st.append(nextcar);nextcar+=1
   if nextcar==v:nextcar+=1
   elif st and st[-1]==v:st.pop()
   else:break
  else:out.append('YES');continue
  out.append('NO')
 return ' '.join(out)
'''
_SIM_327_SPECS=[
('shell-tokenizer','Shell-like quoted tokenizer',['one "two words" three','a\\ b \'c d\'','"" x','a "b\\"c"','one\\ two','\'a b\' "c d"']),
('parking-ledger','Parking ENTER EXIT fee ledger',['2 3\nENTER A 1\nEXIT A 4\nENTER B 5','1 2\nENTER X 0\nEXIT X 0','3 3\nENTER B 2\nENTER A 1\nEXIT B 5','1 1\nEXIT X 4','2 4\nENTER A 1\nEXIT A 2\nENTER A 3\nEXIT A 5','5 2\nENTER Z 9\nENTER Y 1']),
('tournament-scoreboard','Tournament command scoreboard',['3\nWIN A\nDRAW B C\nWIN B','2\nDRAW A B\nDRAW A B','1\nWIN Z','3\nWIN C\nWIN B\nWIN A','2\nWIN A\nWIN A','2\nDRAW X Y\nWIN Y']),
('undo-redo-buffer','Undo redo text buffer',['4\nAPPEND hi\nAPPEND !\nUNDO\nREDO','3\nAPPEND abc\nDELETE 2\nUNDO','2\nUNDO\nREDO','4\nAPPEND a\nDELETE 1\nUNDO\nREDO','1\nAPPEND hello','3\nAPPEND x\nUNDO\nAPPEND y']),
('packet-reassembly','Out-of-order packet reassembly',['3 3\n1 B\n0 A\n2 C','3 2\n0 a\n2 c','1 2\n0 x\n0 y','2 2\n1 b\n0 a','4 3\n3 d\n1 b\n2 c','2 1\n0 z']),
('warehouse-push','Warehouse robot single-box simulation',['2 3\n@B.\n...\nRR','3 3\n@..\n.B#\n...\nDR','1 3\n@B#\nR','2 2\n@#\nB.\nD','2 3\n@..\n.B.\nDRR','1 2\n@B\nL']),
('round-robin-completion','Round-robin CPU completion times',['2 1\n0 2\n0 1','2 2\n0 3\n1 2','1 3\n5 2','3 1\n0 1\n0 1\n0 1','2 5\n0 1\n2 1','3 2\n0 5\n1 1\n4 2']),
('rail-permutation','Stack rail-car permutation feasibility',['3 2\n1 2 3\n3 1 2','1 1\n1','4 2\n4 3 2 1\n2 1 4 3','3 1\n2 3 1','2 2\n2 1\n1 2','4 1\n3 2 1 4'])]
def _sim_327_solution(mode):return "import sys\n"+_SIM_327_CORE+"\n\ndef solve():\n print(answer("+repr(mode)+",sys.stdin.read()))\n\nif __name__=='__main__':\n solve()\n"
for _i,(_mode,_title,_cases) in enumerate(_SIM_327_SPECS,38):
 _fixtures=_literal_fixtures(_FIXTURE_CASES[_mode]);_description,_constraints,_hints,_complexity=_CONTRACTS[_mode];_item=PYTHON_CURATED_289_353[_i];_item.update({'title':_title,'concept_token':_mode,'topics':['simulation','parsing'],'description':_description,'constraints':_constraints+[_SIZE_BOUNDS[_mode]],'hints':_hints+['Use the public example to check formatting.'],'expected_complexity':_complexity,'solution':_sim_327_solution(_mode),'examples':[{'input':_fixtures[0]['input'],'output':_fixtures[0]['expected_output'],'explanation':'The input and output use the stated contract.'}],'public_tests':_fixtures[:2],'hidden_tests':_fixtures[2:]})

_ARRAY_335_CORE=r'''def answer(mode,text):
 from collections import deque,Counter
 from bisect import insort
 data=list(map(int,text.split()));n=data[0];a=data[1:1+n];tail=data[1+n:]
 if mode=='subarray-median-k':
  k=tail[0];return str(sum(sorted(a[i:j])[(j-i-1)//2]==k for i in range(n) for j in range(i+1,n+1)))
 if mode=='shortest-at-least-k':
  K=tail[0];p=[0]
  for x in a:p.append(p[-1]+x)
  q=deque();best=n+1
  for i,x in enumerate(p):
   while q and x-p[q[0]]>=K:best=min(best,i-q.popleft())
   while q and p[q[-1]]>=x:q.pop()
   q.append(i)
  return str(best if best<=n else -1)
 if mode=='one-deletion-max-sum':
  keep=drop=best=a[0]
  for x in a[1:]:drop=max(keep,drop+x);keep=max(x,keep+x);best=max(best,keep,drop)
  return str(best)
 if mode=='reverse-pair-count':return str(sum(a[i]>2*a[j] for i in range(n) for j in range(i+1,n)))
 if mode=='next-permutation':
  b=a[:];i=n-2
  while i>=0 and b[i]>=b[i+1]:i-=1
  if i<0:return 'NONE'
  j=n-1
  while b[j]<=b[i]:j-=1
  b[i],b[j]=b[j],b[i];b[i+1:]=b[i+1:][::-1];return ' '.join(map(str,b))
 if mode=='pancake-flips':
  b=a[:];z=[]
  for end in range(n-1,0,-1):
   i=max(range(end+1),key=b.__getitem__)
   if i!=end:
    if i:z.append(i+1);b[:i+1]=b[:i+1][::-1]
    z.append(end+1);b[:end+1]=b[:end+1][::-1]
  return ' '.join(map(str,z)) or '-'
 if mode=='circular-one-grouping':
  ones=sum(a)
  if ones<=1:return '0'
  b=a*2;zero=sum(x==0 for x in b[:ones]);best=zero
  for i in range(ones,len(b)):zero+=(b[i]==0)-(b[i-ones]==0);best=min(best,zero)
  return str(best)
 if mode=='exactly-k-distinct':
  K=tail[0]
  def f(k):
   c=Counter();l=out=0
   for r,x in enumerate(a):
    c[x]+=1
    while len(c)>k:c[a[l]]-=1;c.pop(a[l],None) if not c[a[l]] else None;l+=1
    out+=r-l+1
   return out
  return str(f(K)-f(K-1))
 if mode=='bounded-range-longest':
  lim=tail[0];lo=deque();hi=deque();l=best=0
  for r,x in enumerate(a):
   while lo and a[lo[-1]]>x:lo.pop()
   while hi and a[hi[-1]]<x:hi.pop()
   lo.append(r);hi.append(r)
   while a[hi[0]]-a[lo[0]]>lim:
    l+=1
    if lo[0]<l:lo.popleft()
    if hi[0]<l:hi.popleft()
   best=max(best,r-l+1)
  return str(best)
 if mode=='online-lower-medians':
  b=[];z=[]
  for x in a:insort(b,x);z.append(b[(len(b)-1)//2])
  return ' '.join(map(str,z))
 k,x=tail;b=sorted(a,key=lambda v:(abs(v-x),v))[:k];return ' '.join(map(str,sorted(b)))
'''
_ARRAY_335_SPECS=[
('subarray-median-k','Count subarrays with lower median k',['3\n1 2 3\n2','3\n3 1 2\n2','1\n5\n5','4\n4 1 3 2\n2','2\n1 2\n1','4\n2 4 1 3\n3']),
('shortest-at-least-k','Shortest subarray reaching K with negatives',['3\n2 -1 2\n3','3\n1 2 3\n3','2\n1 -1\n2','4\n-1 4 -2 3\n5','1\n5\n6','3\n2 -1 2\n2']),
('one-deletion-max-sum','Maximum subarray sum with one deletion',['4\n1 -2 0 3','1\n-1','4\n1 -2 -2 3','3\n1 2 3','3\n-1 -1 -1','5\n2 1 -2 3 4']),
('reverse-pair-count','Count reverse pairs',['5\n1 3 2 3 1','5\n2 4 3 5 1','3\n1 1 1','3\n-5 -5 -5','1\n9','4\n10 4 2 1']),
('next-permutation','Next lexicographic permutation',['3\n1 2 3','3\n3 2 1','3\n1 1 5','4\n1 3 2 4','1\n1','4\n2 3 1 3']),
('pancake-flips','Deterministic pancake-sort flips',['3\n3 1 2','3\n1 2 3','4\n4 3 2 1','1\n5','4\n2 4 1 3','3\n2 1 3']),
('circular-one-grouping','Minimum circular swaps to group ones',['5\n1 0 1 0 1','3\n1 1 1','4\n0 0 0 0','4\n1 0 0 1','1\n1','6\n1 0 1 1 0 1']),
('exactly-k-distinct','Count subarrays with exactly k distinct values',['5\n1 2 1 2 3\n2','3\n1 2 3\n1','4\n1 1 1 1\n1','3\n1 2 1\n3','1\n5\n2','4\n1 2 2 3\n2']),
('bounded-range-longest','Longest subarray within value range',['4\n8 2 4 7\n4','6\n10 1 2 4 7 2\n5','1\n3\n0','3\n1 1 1\n0','4\n1 5 6 7\n1','5\n4 2 2 2 4\n0']),
('online-lower-medians','Online lower medians',['4\n5 1 3 2','3\n1 2 3','1\n9','5\n5 4 3 2 1','4\n2 2 2 2','3\n-1 0 -2']),
('k-closest-sorted','K closest sorted values',['5\n1 2 3 4 5\n4 3','5\n1 2 3 4 5\n4 -1','5\n1 2 3 4 5\n4 6','4\n1 3 5 7\n2 4','1\n9\n1 9','5\n-2 -1 0 1 2\n3 0'])]
def _array_335_solution(mode):return "import sys\n"+_ARRAY_335_CORE+"\n\ndef solve():\n print(answer("+repr(mode)+",sys.stdin.read()))\n\nif __name__=='__main__':\n solve()\n"
for _i,(_mode,_title,_cases) in enumerate(_ARRAY_335_SPECS,46):
 _fixtures=_literal_fixtures(_FIXTURE_CASES[_mode]);_description,_constraints,_hints,_complexity=_CONTRACTS[_mode];_item=PYTHON_CURATED_289_353[_i];_item.update({'title':_title,'concept_token':_mode,'topics':['arrays','advanced-scanning'],'description':_description,'constraints':_constraints+[_SIZE_BOUNDS[_mode]],'hints':_hints+['Use the public example to check formatting.'],'expected_complexity':_complexity,'solution':_array_335_solution(_mode),'examples':[{'input':_fixtures[0]['input'],'output':_fixtures[0]['expected_output'],'explanation':'The input and output use the stated contract.'}],'public_tests':_fixtures[:2],'hidden_tests':_fixtures[2:]})

# The class harness invokes real methods, so keep command streams and their
# materialised output safely inside the interactive runner's limits too.
_OOP_RUNNER_BOUNDS = {
    346: ["Amounts are integers from 0 to 10^9.", "0 <= q <= 1,000; serialized CLI input/output are at most 12,000/22,000 characters."],
    347: ["Prices and quantities are nonnegative integers.", "0 <= q <= 500, names have at most 20 characters, and serialized CLI input/output are at most 12,000/22,000 characters."],
    348: ["0 <= q <= 200, appended text has no spaces, and total appended text is at most 5,000 characters.", "The combined characters printed by `undo` and `text` commands are at most 10,000; serialized CLI input/output are at most 12,000/22,000 characters."],
    349: ["0 <= q <= 500 and song names are lowercase words of at most 20 characters.", "Combined characters printed by `list` commands are at most 10,000; serialized CLI input/output are at most 12,000/22,000 characters."],
    350: ["Dimensions are nonnegative integers no greater than 10^6.", "0 <= q <= 1,500; serialized CLI input/output are at most 12,000/22,000 characters."],
    351: ["0 <= q <= 1,000, priorities are signed integers, and names are lowercase words of at most 20 characters.", "Serialized CLI input/output are at most 12,000/22,000 characters."],
    352: ["0 <= q <= 500, event names are lowercase words of at most 20 characters, and each event has at most 20 subscriptions.", "At most 1,000 callback results are printed across all emits; serialized CLI input/output are at most 12,000/22,000 characters."],
    353: ["0 <= q <= 500 and titles are lowercase words of at most 20 characters.", "Combined characters printed by `available` commands are at most 10,000; serialized CLI input/output are at most 12,000/22,000 characters."],
}
for _number, _bounds in _OOP_RUNNER_BOUNDS.items():
    PYTHON_CURATED_289_353[_number - 289]["constraints"] = _bounds

# This catalogue is designed for the in-app runner.  The individual numeric
# bounds above describe the problem; this common cap makes the runner limits
# part of every script exercise's actual input/output contract.
for _item in PYTHON_CURATED_289_353[:57]:
    _item["constraints"][-1] += " Valid serialized CLI input is at most 12,000 characters and serialized output is at most 22,000 characters."
