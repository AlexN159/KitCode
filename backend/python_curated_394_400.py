"""Hard object-oriented Python drills 394--400.

Each drill has a small command-line demo for Run, while Submit imports the
learner's class through the private harness attached to each fixture.
"""
from __future__ import annotations

ITEMS = []


def add(number, title, topics, description, constraints, hints, complexity, starter, solution, cases, explanation, required_class):
    records = [{"input": source, "expected_output": output, "harness": harness}
               for source, output, harness in cases]
    ITEMS.append({"id": f"python-curated-{number:03d}", "language": "python", "title": title,
        "difficulty": "Hard", "topics": topics, "practice_frequency": "Less common",
        "description": description, "constraints": constraints, "hints": hints,
        "expected_complexity": complexity, "starter_code": starter.strip() + "\n",
        "solution": solution.strip() + "\n", "examples": [{"input": records[0]["input"],
        "output": records[0]["expected_output"], "explanation": explanation}],
        "public_tests": records[:2], "hidden_tests": records[2:],
        "submission_mode": "python_class", "required_class": required_class})


LRU_STARTER = '''class LRUCache:
    def __init__(self, capacity):
        pass
    def get(self, key):
        pass
    def put(self, key, value):
        pass

def solve():
    cache = LRUCache(int(input()))
    for _ in range(int(input())):
        command = input().split()
        if command[0] == "put": cache.put(command[1], int(command[2]))
        else: print(cache.get(command[1]))

if __name__ == "__main__":
    solve()'''
LRU_SOLUTION = '''from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = OrderedDict()
    def get(self, key):
        if key not in self.items: return -1
        self.items.move_to_end(key)
        return self.items[key]
    def put(self, key, value):
        if key in self.items: self.items.move_to_end(key)
        self.items[key] = value
        if len(self.items) > self.capacity: self.items.popitem(last=False)

def solve():
    cache = LRUCache(int(input()))
    for _ in range(int(input())):
        command = input().split()
        if command[0] == "put": cache.put(command[1], int(command[2]))
        else: print(cache.get(command[1]))

if __name__ == "__main__":
    solve()'''
LRU_HARNESS = '''lines = sys.stdin.read().splitlines()
cache = submission_class(int(lines[0]))
for line in lines[2:]:
    command = line.split()
    if command[0] == "put": cache.put(command[1], int(command[2]))
    else: print(cache.get(command[1]))'''
add(394, "LRU cache class", ["classes", "hashing", "linked-lists"],
    "Implement LRUCache(capacity). put(key, value) inserts or updates a key and evicts the least recently used key over capacity. get(key) returns its value and marks it recent, or -1 when absent. CLI input is: line 1 capacity, line 2 command count q, then q lines of put KEY VALUE or get KEY.",
    ["0 <= capacity <= 500 and there are at most 500 commands", "Keys are lowercase words and values are signed 32-bit integers", "The complete CLI input is at most 12,000 characters and its output is at most 22,000 characters"],
    ["A dictionary gives direct lookup.", "Track recency separately from values.", "Both get and updating put make a key most recent."], "O(1) average time per get or put and O(capacity) space",
    LRU_STARTER, LRU_SOLUTION,
    [("2\n6\nput a 1\nput b 2\nget a\nput c 3\nget b\nget c\n", "1\n-1\n3", LRU_HARNESS),
     ("1\n4\nput x 7\nput x 8\nget x\nget y\n", "8\n-1", LRU_HARNESS),
     ("0\n2\nput a 1\nget a\n", "-1", LRU_HARNESS),
     ("2\n5\nput a 1\nput b 2\nget a\nput c 3\nget a\n", "1\n1", LRU_HARNESS),
     ("3\n5\nput a -2\nput b 4\nput c 6\nput d 8\nget a\n", "-1", LRU_HARNESS),
     ("2\n5\nput a 1\nput b 2\nget b\nput c 3\nget a\n", "2\n-1", LRU_HARNESS)],
    "Reading a makes a recent, so adding c evicts b.", {"name": "LRUCache", "methods": ["__init__", "get", "put"]})

DSU_STARTER = '''class RollbackDisjointSet:
    def __init__(self, n):
        pass
    def union(self, left, right):
        pass
    def connected(self, left, right):
        pass
    def snapshot(self):
        pass
    def rollback(self, snapshot):
        pass

def solve():
    dsu = RollbackDisjointSet(int(input()))
    snapshots = []
    for _ in range(int(input())):
        p = input().split()
        if p[0] == "union": print(dsu.union(int(p[1]), int(p[2])))
        elif p[0] == "connected": print(dsu.connected(int(p[1]), int(p[2])))
        elif p[0] == "snapshot": snapshots.append(dsu.snapshot()); print(len(snapshots) - 1)
        else: dsu.rollback(snapshots[int(p[1])])

if __name__ == "__main__": solve()'''
DSU_SOLUTION = '''class RollbackDisjointSet:
    def __init__(self, n):
        self.parent = list(range(n)); self.size = [1] * n; self.history = []
    def find(self, value):
        while value != self.parent[value]: value = self.parent[value]
        return value
    def union(self, left, right):
        left, right = self.find(left), self.find(right)
        if left == right:
            self.history.append(None); return False
        if self.size[left] < self.size[right]: left, right = right, left
        self.history.append((right, self.size[left]))
        self.parent[right] = left; self.size[left] += self.size[right]
        return True
    def connected(self, left, right): return self.find(left) == self.find(right)
    def snapshot(self): return len(self.history)
    def rollback(self, snapshot):
        while len(self.history) > snapshot:
            change = self.history.pop()
            if change is not None:
                child, old_size = change; root = self.parent[child]
                self.parent[child] = child; self.size[root] = old_size

def solve():
    dsu = RollbackDisjointSet(int(input())); snapshots = []
    for _ in range(int(input())):
        p = input().split()
        if p[0] == "union": print(dsu.union(int(p[1]), int(p[2])))
        elif p[0] == "connected": print(dsu.connected(int(p[1]), int(p[2])))
        elif p[0] == "snapshot": snapshots.append(dsu.snapshot()); print(len(snapshots)-1)
        else: dsu.rollback(snapshots[int(p[1])])

if __name__ == "__main__": solve()'''
DSU_HARNESS = '''lines = sys.stdin.read().splitlines()
dsu = submission_class(int(lines[0])); snapshots = []
for line in lines[2:]:
    p = line.split()
    if p[0] == "union": print(dsu.union(int(p[1]), int(p[2])))
    elif p[0] == "connected": print(dsu.connected(int(p[1]), int(p[2])))
    elif p[0] == "snapshot": snapshots.append(dsu.snapshot()); print(len(snapshots) - 1)
    else: dsu.rollback(snapshots[int(p[1])])'''
add(395, "Rollback disjoint-set class", ["classes", "disjoint-set", "rollback"],
    "Implement RollbackDisjointSet(n) for vertices 0 through n-1. union(a,b) joins components and returns whether they were different, connected(a,b) checks a component, snapshot() returns a rollback token, and rollback(token) restores exactly that state. Do not use path compression. CLI input is: line 1 n, line 2 command count q, then q union A B, connected A B, snapshot, or rollback INDEX commands; snapshot indices are assigned in creation order from zero.",
    ["1 <= n <= 800 and at most 800 operations", "rollback receives a token returned by this same instance", "The complete CLI input is at most 12,000 characters and its output is at most 22,000 characters"],
    ["Use union by size to keep trees shallow.", "Record enough information to undo every union.", "A repeated union still needs a history marker."], "O(log n) per union/connected, O(1) snapshot, and O(changes undone) rollback with O(n + operations) space",
    DSU_STARTER, DSU_SOLUTION,
    [("4\n6\nunion 0 1\nsnapshot\nunion 1 2\nconnected 0 2\nrollback 0\nconnected 0 2\n", "True\n0\nTrue\nTrue\nFalse", DSU_HARNESS),
     ("3\n4\nunion 0 1\nunion 0 1\nsnapshot\nconnected 1 2\n", "True\nFalse\n0\nFalse", DSU_HARNESS),
     ("2\n4\nsnapshot\nunion 0 1\nrollback 0\nconnected 0 1\n", "0\nTrue\nFalse", DSU_HARNESS),
     ("5\n6\nunion 0 1\nunion 2 3\nsnapshot\nunion 1 3\nrollback 0\nconnected 0 3\n", "True\nTrue\n0\nTrue\nFalse", DSU_HARNESS),
     ("1\n3\nconnected 0 0\nsnapshot\nrollback 0\n", "True\n0", DSU_HARNESS),
     ("4\n5\nunion 0 1\nsnapshot\nunion 2 3\nrollback 0\nconnected 2 3\n", "True\n0\nTrue\nFalse", DSU_HARNESS)],
    "The snapshot before joining 1 and 2 restores the earlier two components.", {"name": "RollbackDisjointSet", "methods": ["__init__", "union", "connected", "snapshot", "rollback"]})

VECTOR_STARTER = '''from ast import literal_eval

class SparseVector:
    def __init__(self, size, entries):
        pass
    def __len__(self):
        pass
    def __add__(self, other):
        pass
    def __matmul__(self, other):
        pass
    def __eq__(self, other):
        pass

def solve():
    size = int(input()); left = literal_eval(input()); right = literal_eval(input())
    a, b = SparseVector(size, left), SparseVector(size, right)
    print(len(a)); print(a @ b); print(a == b)

if __name__ == "__main__": solve()'''
VECTOR_SOLUTION = '''from ast import literal_eval

class SparseVector:
    def __init__(self, size, entries):
        self.size = size
        self.entries = {int(index): value for index, value in entries.items() if value != 0}
    def __len__(self): return self.size
    def __add__(self, other):
        if self.size != other.size: raise ValueError("different sizes")
        result = dict(self.entries)
        for index, value in other.entries.items(): result[index] = result.get(index, 0) + value
        return SparseVector(self.size, result)
    def __matmul__(self, other):
        if self.size != other.size: raise ValueError("different sizes")
        if len(self.entries) > len(other.entries): self, other = other, self
        return sum(value * other.entries.get(index, 0) for index, value in self.entries.items())
    def __eq__(self, other):
        return isinstance(other, SparseVector) and self.size == other.size and self.entries == other.entries

def solve():
    size = int(input()); left = literal_eval(input()); right = literal_eval(input())
    a, b = SparseVector(size, left), SparseVector(size, right)
    print(len(a)); print(a @ b); print(a == b)

if __name__ == "__main__": solve()'''
def vector_harness(expected_entries):
    return f'''from ast import literal_eval
lines = sys.stdin.read().splitlines()
size = int(lines[0]); a = submission_class(size, literal_eval(lines[1])); b = submission_class(size, literal_eval(lines[2]))
if a + b != submission_class(size, literal_eval({expected_entries!r})): raise AssertionError("incorrect vector sum")
print(len(a)); print(a @ b); print(a == b)'''
add(396, "Sparse vector operators", ["classes", "operator-overloading", "hashing"],
    "Implement SparseVector(size, entries), where entries is a dictionary from valid index to integer and zero entries are ignored. Support len(vector), vector + other, vector @ other for a dot product, and equality. Addition and dot product raise ValueError for different sizes. CLI input is: line 1 size, then one Python dictionary literal on each of lines 2 and 3.",
    ["1 <= size <= 1,000,000,000 and each vector has at most 250 stored entries", "Every supplied index is between 0 and size - 1; stored values are signed 32-bit integers", "The complete CLI input is at most 12,000 characters and its output is at most 22,000 characters"],
    ["Store only nonzero entries.", "For a dot product, iterate one stored dictionary and look up the other.", "Construct a new vector for addition so zero sums disappear."], "O(k + m) addition, O(min(k,m)) expected dot product, and O(k + m) space",
    VECTOR_STARTER, VECTOR_SOLUTION,
    [("5\n{0: 2, 3: 4}\n{0: 3, 2: 7}\n", "5\n6\nFalse", vector_harness("{0: 5, 2: 7, 3: 4}")),
     ("3\n{1: 0}\n{}\n", "3\n0\nTrue", vector_harness("{}")),
     ("4\n{1: -2, 2: 5}\n{1: 2, 3: 1}\n", "4\n-4\nFalse", vector_harness("{2: 5, 3: 1}")),
     ("2\n{0: 9}\n{0: 9}\n", "2\n81\nTrue", vector_harness("{0: 18}")),
     ("10\n{9: 3}\n{8: 4}\n", "10\n0\nFalse", vector_harness("{8: 4, 9: 3}")),
     ("1\n{0: -1}\n{0: 1}\n", "1\n-1\nFalse", vector_harness("{}"))],
    "Only index zero overlaps, so the dot product is two times three.", {"name": "SparseVector", "methods": ["__init__", "__len__", "__add__", "__matmul__", "__eq__"]})

POLY_STARTER = '''class Polynomial:
    def __init__(self, coefficients):
        pass
    def __add__(self, other):
        pass
    def __mul__(self, other):
        pass
    def __call__(self, x):
        pass
    def __repr__(self):
        pass

def solve():
    a = Polynomial(list(map(int, input().split()))); b = Polynomial(list(map(int, input().split()))); x = int(input())
    print(repr(a + b)); print(repr(a * b)); print(a(x))

if __name__ == "__main__": solve()'''
POLY_SOLUTION = '''class Polynomial:
    def __init__(self, coefficients):
        self.coefficients = list(coefficients) or [0]
        while len(self.coefficients) > 1 and self.coefficients[-1] == 0: self.coefficients.pop()
    def __add__(self, other):
        length = max(len(self.coefficients), len(other.coefficients))
        return Polynomial([(self.coefficients[i] if i < len(self.coefficients) else 0) + (other.coefficients[i] if i < len(other.coefficients) else 0) for i in range(length)])
    def __mul__(self, other):
        result = [0] * (len(self.coefficients) + len(other.coefficients) - 1)
        for i, left in enumerate(self.coefficients):
            for j, right in enumerate(other.coefficients): result[i + j] += left * right
        return Polynomial(result)
    def __call__(self, x):
        total = 0
        for coefficient in reversed(self.coefficients): total = total * x + coefficient
        return total
    def __repr__(self):
        if self.coefficients == [0]: return "0"
        terms = []
        for power in range(len(self.coefficients) - 1, -1, -1):
            coefficient = self.coefficients[power]
            if coefficient == 0: continue
            magnitude = abs(coefficient)
            body = str(magnitude) if power == 0 else ("x" if power == 1 else f"x^{power}")
            if power and magnitude != 1: body = f"{magnitude}*{body}"
            sign = "-" if coefficient < 0 else "+"
            terms.append((sign, body))
        first_sign, first_body = terms[0]
        return ("-" if first_sign == "-" else "") + first_body + "".join(f" {sign} {body}" for sign, body in terms[1:])

def solve():
    a = Polynomial(list(map(int, input().split()))); b = Polynomial(list(map(int, input().split()))); x = int(input())
    print(repr(a + b)); print(repr(a * b)); print(a(x))

if __name__ == "__main__": solve()'''
POLY_HARNESS = '''lines = sys.stdin.read().splitlines()
a = submission_class(list(map(int, lines[0].split()))); b = submission_class(list(map(int, lines[1].split()))); x = int(lines[2])
print(repr(a + b)); print(repr(a * b)); print(a(x))'''
add(397, "Polynomial operator class", ["classes", "operator-overloading", "algebra"],
    "Implement Polynomial(coefficients) with coefficients in low-to-high power order. Remove unnecessary trailing zero coefficients. Support addition, multiplication, calling the polynomial at x, and repr in canonical descending form such as 2*x^2 - x + 3. CLI input is: coefficient lists for two polynomials on lines 1 and 2, then x on line 3.",
    ["Each input list has 1 through 300 coefficients with absolute value at most 100", "The evaluation input x satisfies -3 <= x <= 3", "The complete CLI input is at most 12,000 characters and its output is at most 22,000 characters"],
    ["Trim zeroes only from the high-power end.", "Use nested loops for coefficient multiplication.", "Horner's method evaluates from highest power down."], "O(nm) multiplication, O(n+m) addition, and O(n+m) space",
    POLY_STARTER, POLY_SOLUTION,
    [("3 2\n1 -1\n2\n", "x + 4\n-2*x^2 - x + 3\n7", POLY_HARNESS),
     ("0 0\n0\n5\n", "0\n0\n0", POLY_HARNESS),
     ("1\n1\n3\n", "2\n1\n1", POLY_HARNESS),
     ("0 1\n0 1\n2\n", "2*x\nx^2\n2", POLY_HARNESS),
     ("-3 0 1\n3\n-1\n", "x^2\n3*x^2 - 9\n-2", POLY_HARNESS),
     ("2 -1 0\n-2 1\n4\n", "0\n-x^2 + 4*x - 4\n-2", POLY_HARNESS)],
    "(3 + 2x) plus (1 - x) is 4 + x, and the first polynomial has value seven at two.", {"name": "Polynomial", "methods": ["__init__", "__add__", "__mul__", "__call__", "__repr__"]})

STORE_STARTER = '''class VersionedStore:
    def __init__(self):
        pass
    def set(self, key, value, timestamp):
        pass
    def get(self, key, timestamp):
        pass

def solve():
    store = VersionedStore()
    for _ in range(int(input())):
        p = input().split()
        if p[0] == "set": store.set(p[1], p[2], int(p[3]))
        else: print(store.get(p[1], int(p[2])))

if __name__ == "__main__": solve()'''
STORE_SOLUTION = '''from bisect import bisect_right

class VersionedStore:
    def __init__(self): self.values = {}
    def set(self, key, value, timestamp):
        self.values.setdefault(key, []).append((timestamp, value))
    def get(self, key, timestamp):
        versions = self.values.get(key, [])
        index = bisect_right(versions, (timestamp, chr(0x10ffff))) - 1
        return versions[index][1] if index >= 0 else ""

def solve():
    store = VersionedStore()
    for _ in range(int(input())):
        p = input().split()
        if p[0] == "set": store.set(p[1], p[2], int(p[3]))
        else: print(store.get(p[1], int(p[2])))

if __name__ == "__main__": solve()'''
STORE_HARNESS = '''store = submission_class()
lines = sys.stdin.read().splitlines()
for line in lines[1:]:
    p = line.split()
    if p[0] == "set": store.set(p[1], p[2], int(p[3]))
    else: print(store.get(p[1], int(p[2])))'''
add(398, "Versioned key-value store", ["classes", "binary-search", "hashing"],
    "Implement VersionedStore(). set(key, value, timestamp) records a value; calls for each key have strictly increasing timestamps. get(key, timestamp) returns the value with the greatest timestamp no later than the request, or an empty string if none exists. CLI input is: line 1 command count q, then q lines of set KEY VALUE TIMESTAMP or get KEY TIMESTAMP.",
    ["There are at most 800 operations, including at most 500 get commands", "Keys and values are lowercase words of at most 20 characters; timestamps are nonnegative integers", "For a key, set timestamps are strictly increasing", "The complete CLI input is at most 12,000 characters and its output is at most 22,000 characters"],
    ["Map each key to its ordered versions.", "Binary search finds the final timestamp not above the query.", "A missing key and a too-early query both return an empty string."], "O(1) amortized set, O(log k) get for k versions of that key, and O(operations) space",
    STORE_STARTER, STORE_SOLUTION,
    [("4\nset cat small 2\nget cat 1\nget cat 2\nget cat 9\n", "\nsmall\nsmall", STORE_HARNESS),
     ("5\nset a red 1\nset a blue 4\nget a 3\nget a 4\nget b 5\n", "red\nblue", STORE_HARNESS),
     ("3\nset x one 0\nget x 0\nget x 10\n", "one\none", STORE_HARNESS),
     ("5\nset a x 2\nset b y 3\nget b 2\nget a 2\nget b 3\n", "\nx\ny", STORE_HARNESS),
     ("4\nset x old 1\nset x new 2\nget x 1\nget x 2\n", "old\nnew", STORE_HARNESS),
     ("1\nget absent 0\n", "", STORE_HARNESS)],
    "Before timestamp two there is no cat value; at two and later it is small.", {"name": "VersionedStore", "methods": ["__init__", "set", "get"]})

GRAPH_STARTER = '''class DependencyGraph:
    def __init__(self):
        pass
    def add_task(self, task):
        pass
    def add_dependency(self, task, prerequisite):
        pass
    def order(self):
        pass

def solve():
    graph = DependencyGraph()
    for _ in range(int(input())):
        p = input().split()
        if p[0] == "task": graph.add_task(p[1])
        elif p[0] == "depends": graph.add_dependency(p[1], p[2])
    try: print(" ".join(graph.order()))
    except ValueError: print("CYCLE")

if __name__ == "__main__": solve()'''
GRAPH_SOLUTION = '''import heapq

class DependencyGraph:
    def __init__(self): self.edges = {}
    def add_task(self, task): self.edges.setdefault(task, set())
    def add_dependency(self, task, prerequisite):
        self.add_task(task); self.add_task(prerequisite); self.edges[prerequisite].add(task)
    def order(self):
        indegree = {task: 0 for task in self.edges}
        for next_tasks in self.edges.values():
            for task in next_tasks: indegree[task] += 1
        ready = [task for task, count in indegree.items() if count == 0]; heapq.heapify(ready); result = []
        while ready:
            task = heapq.heappop(ready); result.append(task)
            for next_task in self.edges[task]:
                indegree[next_task] -= 1
                if indegree[next_task] == 0: heapq.heappush(ready, next_task)
        if len(result) != len(self.edges): raise ValueError("cycle")
        return result

def solve():
    graph = DependencyGraph()
    for _ in range(int(input())):
        p = input().split()
        if p[0] == "task": graph.add_task(p[1])
        elif p[0] == "depends": graph.add_dependency(p[1], p[2])
    try: print(" ".join(graph.order()))
    except ValueError: print("CYCLE")

if __name__ == "__main__": solve()'''
GRAPH_HARNESS = '''graph = submission_class()
for line in sys.stdin.read().splitlines()[1:]:
    p = line.split()
    if p[0] == "task": graph.add_task(p[1])
    elif p[0] == "depends": graph.add_dependency(p[1], p[2])
try: print(" ".join(graph.order()))
except ValueError: print("CYCLE")'''
add(399, "Dependency graph class", ["classes", "graphs", "topological-sort"],
    "Implement DependencyGraph(). add_task(task) declares a task, add_dependency(task, prerequisite) adds the prerequisite relation and declares either missing task, and order() returns the lexicographically smallest valid task order. order() raises ValueError when a cycle exists. CLI input is: line 1 command count q, then q lines of task NAME or depends TASK PREREQUISITE; print the final order or CYCLE.",
    ["There are at most 800 task and dependency commands", "Task names are distinct lowercase words of at most 20 characters", "The complete CLI input is at most 12,000 characters and its output is at most 22,000 characters"],
    ["Store an edge from prerequisite to task.", "Count incoming prerequisites.", "A min-heap chooses the lexicographically smallest available task."], "O((V + E) log V) time and O(V + E) space",
    GRAPH_STARTER, GRAPH_SOLUTION,
    [("4\ntask bake\ntask shop\ndepends bake shop\ntask clean\n", "clean shop bake", GRAPH_HARNESS),
     ("3\ndepends test build\ndepends deploy test\ntask docs\n", "build docs test deploy", GRAPH_HARNESS),
     ("2\ndepends a b\ndepends b a\n", "CYCLE", GRAPH_HARNESS),
     ("3\ntask c\ntask a\ntask b\n", "a b c", GRAPH_HARNESS),
     ("3\ndepends c a\ndepends c b\ntask d\n", "a b c d", GRAPH_HARNESS),
     ("1\ndepends solo solo\n", "CYCLE", GRAPH_HARNESS)],
    "Clean and shop are initially available, so clean comes first alphabetically.", {"name": "DependencyGraph", "methods": ["__init__", "add_task", "add_dependency", "order"]})

SHEET_STARTER = '''class MiniSpreadsheet:
    def __init__(self):
        pass
    def set_value(self, cell, value):
        pass
    def set_formula(self, cell, expression):
        pass
    def evaluate(self, cell):
        pass

def solve():
    sheet = MiniSpreadsheet()
    for _ in range(int(input())):
        p = input().split(maxsplit=2)
        if p[0] == "value": sheet.set_value(p[1], int(p[2]))
        elif p[0] == "formula": sheet.set_formula(p[1], p[2])
        else:
            try: print(sheet.evaluate(p[1]))
            except ValueError: print("CYCLE")

if __name__ == "__main__": solve()'''
SHEET_SOLUTION = '''class MiniSpreadsheet:
    def __init__(self): self.cells = {}; self.cache = {}
    def set_value(self, cell, value): self.cells[cell] = value; self.cache.clear()
    def set_formula(self, cell, expression): self.cells[cell] = expression; self.cache.clear()
    def evaluate(self, cell):
        def parts(expression):
            return [part.strip() for part in expression.split("+")]
        visiting = set(); stack = [(cell, False)]
        while stack:
            name, ready = stack.pop()
            if name in self.cache: continue
            item = self.cells.get(name, 0)
            if isinstance(item, int):
                self.cache[name] = item; continue
            terms = parts(item)
            if ready:
                self.cache[name] = sum(int(term) if term.lstrip("-").isdigit() else self.cache[term] for term in terms)
                visiting.remove(name); continue
            if name in visiting: raise ValueError("cycle")
            visiting.add(name); stack.append((name, True))
            for term in reversed(terms):
                if not term.lstrip("-").isdigit() and term not in self.cache:
                    if term in visiting: raise ValueError("cycle")
                    stack.append((term, False))
        return self.cache[cell]

def solve():
    sheet = MiniSpreadsheet()
    for _ in range(int(input())):
        p = input().split(maxsplit=2)
        if p[0] == "value": sheet.set_value(p[1], int(p[2]))
        elif p[0] == "formula": sheet.set_formula(p[1], p[2])
        else:
            try: print(sheet.evaluate(p[1]))
            except ValueError: print("CYCLE")

if __name__ == "__main__": solve()'''
SHEET_HARNESS = '''sheet = submission_class()
for line in sys.stdin.read().splitlines()[1:]:
    p = line.split(maxsplit=2)
    if p[0] == "value": sheet.set_value(p[1], int(p[2]))
    elif p[0] == "formula": sheet.set_formula(p[1], p[2])
    else:
        try: print(sheet.evaluate(p[1]))
        except ValueError: print("CYCLE")'''
add(400, "Mini spreadsheet class", ["classes", "graphs", "memoization", "parsing"],
    "Implement MiniSpreadsheet(). set_value(cell, integer) stores a number, set_formula(cell, expression) stores a plus-separated expression of integer literals and cell references, and evaluate(cell) returns its value. Missing cells equal zero. Raise ValueError for a dependency cycle. CLI input is: line 1 command count q, then q lines of value CELL INTEGER, formula CELL EXPRESSION, or get CELL.",
    ["There are at most 500 commands and 1,000 formula tokens", "Cell names are uppercase letters followed by digits", "Expressions contain only integer literals, cell names, spaces, and +; every evaluated value fits in a signed 64-bit integer", "The complete CLI input is at most 12,000 characters and its output is at most 22,000 characters"],
    ["Clear cached values whenever a cell changes.", "Evaluate referenced cells with an explicit stack.", "Keep a visiting set to detect a cycle."], "O(reachable formula tokens) per uncached evaluation and O(cells + formula tokens) space",
    SHEET_STARTER, SHEET_SOLUTION,
    [("5\nvalue A1 2\nvalue B1 3\nformula C1 A1 + B1 + 4\nget C1\nget D1\n", "9\n0", SHEET_HARNESS),
     ("4\nvalue A1 1\nformula B1 A1 + 2\nvalue A1 5\nget B1\n", "7", SHEET_HARNESS),
     ("3\nformula A1 B1 + 1\nformula B1 A1 + 1\nget A1\n", "CYCLE", SHEET_HARNESS),
     ("4\nformula C1 5 + 6\nformula D1 C1 + 1\nget D1\nget C1\n", "12\n11", SHEET_HARNESS),
     ("3\nvalue A1 -2\nformula B1 A1 + 10\nget B1\n", "8", SHEET_HARNESS),
     ("3\nformula A1 Z9 + 2\nget A1\nget Z9\n", "2\n0", SHEET_HARNESS)],
    "C1 adds A1, B1, and the literal four; an unstored cell evaluates to zero.", {"name": "MiniSpreadsheet", "methods": ["__init__", "set_value", "set_formula", "evaluate"]})


PYTHON_CURATED_394_400 = ITEMS
