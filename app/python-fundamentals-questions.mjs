/** Static Python-fundamentals multiple-choice interview bank. */
export const pythonFundamentalsQuestions = [
  {
    "id": "python-fundamentals-001",
    "title": "What is the Global Interpreter Lock (GIL) in CPython",
    "topic": "runtime",
    "difficulty": "Intermediate",
    "question": "What is the Global Interpreter Lock (GIL) in CPython?",
    "options": [
      "In a GIL-enabled build, a lock that lets only one thread execute Python bytecode at a time",
      "A lock that prevents imports from running concurrently",
      "A garbage-collection lock used only for cyclic objects",
      "A database lock built into the standard library"
    ],
    "correctIndex": 0,
    "explanation": "In GIL-enabled CPython builds, it serializes Python bytecode execution within a process; free-threaded CPython builds are also available."
  },
  {
    "id": "python-fundamentals-002",
    "title": "Which built-in type is immutable",
    "topic": "types",
    "difficulty": "Easy",
    "question": "Which built-in type is immutable?",
    "options": [
      "list",
      "dict",
      "set",
      "tuple"
    ],
    "correctIndex": 3,
    "explanation": "A tuple cannot have elements added, removed, or replaced after creation, although an element may itself reference a mutable object."
  },
  {
    "id": "python-fundamentals-003",
    "title": "Which expression creates an empty set",
    "topic": "collections",
    "difficulty": "Easy",
    "question": "Which expression creates an empty set?",
    "options": [
      "{}",
      "set()",
      "[]",
      "()"
    ],
    "correctIndex": 1,
    "explanation": "{} creates an empty dictionary; set() creates an empty set."
  },
  {
    "id": "python-fundamentals-004",
    "title": "What does // do for integers in Python",
    "topic": "operators",
    "difficulty": "Easy",
    "question": "What does // do for integers in Python?",
    "options": [
      "Floating-point division",
      "Floor division",
      "Remainder division",
      "Bitwise division"
    ],
    "correctIndex": 1,
    "explanation": "// rounds the quotient down toward negative infinity."
  },
  {
    "id": "python-fundamentals-005",
    "title": "What does 5 // -2 evaluate to",
    "topic": "operators",
    "difficulty": "Intermediate",
    "question": "What does 5 // -2 evaluate to?",
    "options": [
      "-2",
      "-2.5",
      "-3",
      "2"
    ],
    "correctIndex": 2,
    "explanation": "Floor division rounds -2.5 down to -3."
  },
  {
    "id": "python-fundamentals-006",
    "title": "Which statement about == and is is correct",
    "topic": "objects",
    "difficulty": "Easy",
    "question": "Which statement about == and is is correct?",
    "options": [
      "Both always compare object identity",
      "== compares values while is compares identity",
      "is compares values while == compares identity",
      "They differ only for strings"
    ],
    "correctIndex": 1,
    "explanation": "Use == for equality and is, commonly with None, for object identity."
  },
  {
    "id": "python-fundamentals-007",
    "title": "What is the preferred test for a missing optional value",
    "topic": "objects",
    "difficulty": "Easy",
    "question": "What is the preferred test for a missing optional value?",
    "options": [
      "value == None",
      "value is None",
      "not value",
      "type(value) is None"
    ],
    "correctIndex": 1,
    "explanation": "None is a singleton, so identity comparison is the idiomatic test."
  },
  {
    "id": "python-fundamentals-008",
    "title": "What is the result of bool([])",
    "topic": "truthiness",
    "difficulty": "Easy",
    "question": "What is the result of bool([])?",
    "options": [
      "True",
      "False",
      "None",
      "It raises TypeError"
    ],
    "correctIndex": 1,
    "explanation": "Empty containers are falsy."
  },
  {
    "id": "python-fundamentals-009",
    "title": "What does list(range(2, 8, 2)) produce",
    "topic": "control-flow",
    "difficulty": "Easy",
    "question": "What does list(range(2, 8, 2)) produce?",
    "options": [
      "[2, 4, 6, 8]",
      "[2, 4, 6]",
      "[2, 3, 4, 5, 6, 7]",
      "[4, 6, 8]"
    ],
    "correctIndex": 1,
    "explanation": "range stops before its end value."
  },
  {
    "id": "python-fundamentals-010",
    "title": "What does the slice text[::-1] do",
    "topic": "strings",
    "difficulty": "Easy",
    "question": "What does the slice text[::-1] do?",
    "options": [
      "Removes the final character",
      "Returns every other character",
      "Returns the text reversed",
      "Raises ValueError"
    ],
    "correctIndex": 2,
    "explanation": "A step of -1 visits the sequence from end to start."
  },
  {
    "id": "python-fundamentals-011",
    "title": "Which collection preserves insertion order and maps keys to values",
    "topic": "collections",
    "difficulty": "Easy",
    "question": "Which collection preserves insertion order and maps keys to values?",
    "options": [
      "set",
      "dict",
      "tuple",
      "frozenset"
    ],
    "correctIndex": 1,
    "explanation": "Modern Python dictionaries retain insertion order and provide key-value lookup."
  },
  {
    "id": "python-fundamentals-012",
    "title": "What happens when you access a dictionary using a key that is absent with d[key]",
    "topic": "collections",
    "difficulty": "Easy",
    "question": "What happens when you access a dictionary using a key that is absent with d[key]?",
    "options": [
      "It returns None",
      "It inserts the key with None",
      "It raises KeyError",
      "It raises IndexError"
    ],
    "correctIndex": 2,
    "explanation": "Use get() when a fallback is appropriate."
  },
  {
    "id": "python-fundamentals-013",
    "title": "What does d.get('missing', 0) return when 'missing' is not a key",
    "topic": "collections",
    "difficulty": "Easy",
    "question": "What does d.get('missing', 0) return when 'missing' is not a key?",
    "options": [
      "None",
      "0",
      "KeyError",
      "The string 'missing'"
    ],
    "correctIndex": 1,
    "explanation": "dict.get returns its supplied default for an absent key."
  },
  {
    "id": "python-fundamentals-014",
    "title": "Which type can be a dictionary key",
    "topic": "hashing",
    "difficulty": "Intermediate",
    "question": "Which type can be a dictionary key?",
    "options": [
      "list",
      "set",
      "dict",
      "tuple containing only hashable values"
    ],
    "correctIndex": 3,
    "explanation": "Dictionary keys must be hashable; a tuple is hashable when every value it contains is hashable."
  },
  {
    "id": "python-fundamentals-015",
    "title": "Why can't a list be used as a dictionary key",
    "topic": "hashing",
    "difficulty": "Intermediate",
    "question": "Why can't a list be used as a dictionary key?",
    "options": [
      "Lists are too large",
      "Lists are mutable and therefore unhashable",
      "Lists have no equality operation",
      "Lists are ordered"
    ],
    "correctIndex": 1,
    "explanation": "Changing a key's hash would break hash-table lookup."
  },
  {
    "id": "python-fundamentals-016",
    "title": "What does a set primarily guarantee",
    "topic": "collections",
    "difficulty": "Easy",
    "question": "What does a set primarily guarantee?",
    "options": [
      "Sorted values",
      "Unique hashable elements",
      "Index-based access",
      "Key-value pairs"
    ],
    "correctIndex": 1,
    "explanation": "Sets eliminate duplicate hashable values; their iteration order should not be used as sorted order."
  },
  {
    "id": "python-fundamentals-017",
    "title": "What does enumerate(names, start=1) provide in a loop",
    "topic": "iteration",
    "difficulty": "Easy",
    "question": "What does enumerate(names, start=1) provide in a loop?",
    "options": [
      "Sorted names",
      "A one-based index and each name",
      "Only the length of names",
      "A copy of names"
    ],
    "correctIndex": 1,
    "explanation": "enumerate yields index-value pairs, beginning at the requested start."
  },
  {
    "id": "python-fundamentals-018",
    "title": "What does zip(a, b) do when a and b have different lengths",
    "topic": "iteration",
    "difficulty": "Easy",
    "question": "What does zip(a, b) do when a and b have different lengths?",
    "options": [
      "Raises ValueError",
      "Pads the shorter iterable with None",
      "Stops at the shorter iterable",
      "Repeats the last value"
    ],
    "correctIndex": 2,
    "explanation": "Normal zip stops when the shortest input is exhausted."
  },
  {
    "id": "python-fundamentals-019",
    "title": "What is a list comprehension",
    "topic": "syntax",
    "difficulty": "Easy",
    "question": "What is a list comprehension?",
    "options": [
      "A compact expression for constructing a list",
      "A list method that sorts in place",
      "A way to make tuples immutable",
      "A special exception type"
    ],
    "correctIndex": 0,
    "explanation": "For example, [x * x for x in values] builds a new list."
  },
  {
    "id": "python-fundamentals-020",
    "title": "Which expression lazily produces squares from values",
    "topic": "generators",
    "difficulty": "Intermediate",
    "question": "Which expression lazily produces squares from values?",
    "options": [
      "[x * x for x in values]",
      "{x * x for x in values}",
      "(x * x for x in values)",
      "dict(x * x for x in values)"
    ],
    "correctIndex": 2,
    "explanation": "Parentheses create a generator expression here."
  },
  {
    "id": "python-fundamentals-021",
    "title": "What does yield do in a function",
    "topic": "generators",
    "difficulty": "Intermediate",
    "question": "What does yield do in a function?",
    "options": [
      "Immediately exits the program",
      "Makes the function return a generator when called",
      "Creates a class method",
      "Suppresses exceptions"
    ],
    "correctIndex": 1,
    "explanation": "A yielding function pauses and resumes as its generator is iterated."
  },
  {
    "id": "python-fundamentals-022",
    "title": "An iterator must provide which method to produce its next item",
    "topic": "iteration",
    "difficulty": "Intermediate",
    "question": "An iterator must provide which method to produce its next item?",
    "options": [
      "__next__",
      "__getitem__",
      "__call__",
      "__yield__"
    ],
    "correctIndex": 0,
    "explanation": "next(iterator) invokes __next__; exhaustion raises StopIteration."
  },
  {
    "id": "python-fundamentals-023",
    "title": "What is an iterable",
    "topic": "iteration",
    "difficulty": "Intermediate",
    "question": "What is an iterable?",
    "options": [
      "Only a list",
      "An object that can provide an iterator",
      "An object that must be mutable",
      "A function with yield"
    ],
    "correctIndex": 1,
    "explanation": "iter(obj) succeeds for iterables, including many containers and generators."
  },
  {
    "id": "python-fundamentals-024",
    "title": "What does pass do",
    "topic": "control-flow",
    "difficulty": "Easy",
    "question": "What does pass do?",
    "options": [
      "Skips to the next loop iteration",
      "Ends a function",
      "Acts as a no-operation placeholder",
      "Raises StopIteration"
    ],
    "correctIndex": 2,
    "explanation": "pass is syntactically useful where a statement is required but no action is needed."
  },
  {
    "id": "python-fundamentals-025",
    "title": "What does continue do inside a loop",
    "topic": "control-flow",
    "difficulty": "Easy",
    "question": "What does continue do inside a loop?",
    "options": [
      "Exits the loop entirely",
      "Skips the rest of the current iteration",
      "Restarts the function",
      "Runs the loop's else block"
    ],
    "correctIndex": 1,
    "explanation": "Control moves to the loop's next iteration."
  },
  {
    "id": "python-fundamentals-026",
    "title": "When does a loop else block run",
    "topic": "control-flow",
    "difficulty": "Intermediate",
    "question": "When does a loop else block run?",
    "options": [
      "After every iteration",
      "Only if the loop completed normally without break",
      "Only if the loop body raises",
      "Never for for loops"
    ],
    "correctIndex": 1,
    "explanation": "A loop else block runs after normal exhaustion or a false condition; it is skipped by break and by an exception or return that leaves the loop."
  },
  {
    "id": "python-fundamentals-027",
    "title": "What is the usual purpose of finally in try/except/finally",
    "topic": "exceptions",
    "difficulty": "Easy",
    "question": "What is the usual purpose of finally in try/except/finally?",
    "options": [
      "It runs only when no exception occurs",
      "It runs cleanup whether or not an exception occurs",
      "It retries the try block",
      "It converts all exceptions to None"
    ],
    "correctIndex": 1,
    "explanation": "finally is used for cleanup such as closing a resource."
  },
  {
    "id": "python-fundamentals-028",
    "title": "Which exception is raised by 1 / 0",
    "topic": "exceptions",
    "difficulty": "Easy",
    "question": "Which exception is raised by 1 / 0?",
    "options": [
      "ValueError",
      "TypeError",
      "ZeroDivisionError",
      "ArithmeticError only"
    ],
    "correctIndex": 2,
    "explanation": "Division by numeric zero raises ZeroDivisionError."
  },
  {
    "id": "python-fundamentals-029",
    "title": "What is the best way to ensure an opened file is closed",
    "topic": "files",
    "difficulty": "Easy",
    "question": "What is the best way to ensure an opened file is closed?",
    "options": [
      "Use a with statement",
      "Call gc.collect()",
      "Put open() in a list",
      "Use assert"
    ],
    "correctIndex": 0,
    "explanation": "A context manager closes the file when the with block exits."
  },
  {
    "id": "python-fundamentals-030",
    "title": "What is a context manager",
    "topic": "files",
    "difficulty": "Intermediate",
    "question": "What is a context manager?",
    "options": [
      "A type of dictionary",
      "An object that manages setup and cleanup around a with block",
      "A module import cache",
      "A recursive function"
    ],
    "correctIndex": 1,
    "explanation": "Context managers implement the context-management protocol, often through __enter__ and __exit__."
  },
  {
    "id": "python-fundamentals-031",
    "title": "What does the default argument in def f(items=[]) risk",
    "topic": "functions",
    "difficulty": "Intermediate",
    "question": "What does the default argument in def f(items=[]) risk?",
    "options": [
      "A SyntaxError",
      "A new list on every call",
      "Sharing one mutable list across calls",
      "Making items immutable"
    ],
    "correctIndex": 2,
    "explanation": "Default expressions are evaluated once when the function is defined."
  },
  {
    "id": "python-fundamentals-032",
    "title": "What is the standard safe pattern for an optional list argument",
    "topic": "functions",
    "difficulty": "Intermediate",
    "question": "What is the standard safe pattern for an optional list argument?",
    "options": [
      "def f(items=[]):",
      "def f(items=None): then create [] when items is None",
      "def f(items=set()):",
      "def f(items=tuple()): then append"
    ],
    "correctIndex": 1,
    "explanation": "None avoids sharing a mutable default between calls."
  },
  {
    "id": "python-fundamentals-033",
    "title": "What do *args collect in a function definition",
    "topic": "functions",
    "difficulty": "Easy",
    "question": "What do *args collect in a function definition?",
    "options": [
      "Extra positional arguments as a tuple",
      "Extra keyword arguments as a dict",
      "Only required arguments",
      "All local variables"
    ],
    "correctIndex": 0,
    "explanation": "*args collects remaining positional inputs into a tuple."
  },
  {
    "id": "python-fundamentals-034",
    "title": "What do **kwargs collect in a function definition",
    "topic": "functions",
    "difficulty": "Easy",
    "question": "What do **kwargs collect in a function definition?",
    "options": [
      "Extra positional arguments as a list",
      "Extra keyword arguments as a dictionary",
      "All exception data",
      "Only default values"
    ],
    "correctIndex": 1,
    "explanation": "**kwargs collects unbound keyword arguments in a dict."
  },
  {
    "id": "python-fundamentals-035",
    "title": "Python argument passing is best described as what",
    "topic": "functions",
    "difficulty": "Intermediate",
    "question": "Python argument passing is best described as what?",
    "options": [
      "Pass by value",
      "Pass by reference",
      "Pass by object reference",
      "Copy on write"
    ],
    "correctIndex": 2,
    "explanation": "Names are bound to object references; mutation and rebinding have different effects."
  },
  {
    "id": "python-fundamentals-036",
    "title": "What is LEGB in Python name lookup",
    "topic": "scope",
    "difficulty": "Intermediate",
    "question": "What is LEGB in Python name lookup?",
    "options": [
      "Local, Enclosing, Global, Built-in",
      "List, Entry, Generator, Boolean",
      "Local, External, General, Base",
      "Lambda, Eval, Global, Block"
    ],
    "correctIndex": 0,
    "explanation": "Python resolves unqualified names through those scopes in order."
  },
  {
    "id": "python-fundamentals-037",
    "title": "When should nonlocal be used",
    "topic": "scope",
    "difficulty": "Intermediate",
    "question": "When should nonlocal be used?",
    "options": [
      "To modify a name in an enclosing function scope",
      "To import a module",
      "To modify any global name",
      "To make a variable immutable"
    ],
    "correctIndex": 0,
    "explanation": "nonlocal rebinds a name from the nearest enclosing function scope."
  },
  {
    "id": "python-fundamentals-038",
    "title": "What does global x declare inside a function",
    "topic": "scope",
    "difficulty": "Intermediate",
    "question": "What does global x declare inside a function?",
    "options": [
      "x is immutable",
      "Assignments to x target the module-level name",
      "x is thread-local",
      "x is visible only in the function"
    ],
    "correctIndex": 1,
    "explanation": "global changes assignment binding to the module namespace."
  },
  {
    "id": "python-fundamentals-039",
    "title": "What is a closure",
    "topic": "scope",
    "difficulty": "Intermediate",
    "question": "What is a closure?",
    "options": [
      "A function that retains access to enclosing-scope values",
      "A function with no parameters",
      "A class destructor",
      "A closed file object"
    ],
    "correctIndex": 0,
    "explanation": "Inner functions can capture names from their enclosing scopes."
  },
  {
    "id": "python-fundamentals-040",
    "title": "What is a lambda expression intended for",
    "topic": "functions",
    "difficulty": "Easy",
    "question": "What is a lambda expression intended for?",
    "options": [
      "A concise anonymous function expression",
      "Defining a multi-statement function body",
      "Creating a generator only",
      "Declaring a class"
    ],
    "correctIndex": 0,
    "explanation": "A lambda body is a single expression."
  },
  {
    "id": "python-fundamentals-041",
    "title": "What does a decorator do",
    "topic": "functions",
    "difficulty": "Intermediate",
    "question": "What does a decorator do?",
    "options": [
      "Changes a function or class by wrapping or transforming it",
      "Only documents a function",
      "Deletes function arguments",
      "Makes a function asynchronous"
    ],
    "correctIndex": 0,
    "explanation": "The @ syntax applies a callable to the decorated object."
  },
  {
    "id": "python-fundamentals-042",
    "title": "What is the main difference between a shallow and deep copy",
    "topic": "objects",
    "difficulty": "Intermediate",
    "question": "What is the main difference between a shallow and deep copy?",
    "options": [
      "A shallow copy duplicates nested objects too",
      "A deep copy normally copies nested objects recursively",
      "Deep copies are always immutable",
      "They are identical for every object"
    ],
    "correctIndex": 1,
    "explanation": "A shallow copy shares nested object references, while copy.deepcopy normally copies them recursively and preserves shared references through memoization."
  },
  {
    "id": "python-fundamentals-043",
    "title": "What does list_a = list_b do",
    "topic": "objects",
    "difficulty": "Easy",
    "question": "What does list_a = list_b do?",
    "options": [
      "Creates a shallow copy",
      "Creates a deep copy",
      "Binds list_a to the same list object",
      "Converts list_b into a tuple"
    ],
    "correctIndex": 2,
    "explanation": "Assignment binds another name; it does not copy the list."
  },
  {
    "id": "python-fundamentals-044",
    "title": "What is the result of [1, 2] + [3]",
    "topic": "collections",
    "difficulty": "Easy",
    "question": "What is the result of [1, 2] + [3]?",
    "options": [
      "[1, 2, 3]",
      "[4, 5]",
      "[1, 2, [3]]",
      "TypeError"
    ],
    "correctIndex": 0,
    "explanation": "+ concatenates lists into a new list."
  },
  {
    "id": "python-fundamentals-045",
    "title": "What is the result of [0] * 3",
    "topic": "collections",
    "difficulty": "Easy",
    "question": "What is the result of [0] * 3?",
    "options": [
      "[0, 0, 0]",
      "[3]",
      "[[0], [0], [0]]",
      "TypeError"
    ],
    "correctIndex": 0,
    "explanation": "List multiplication repeats the list's element references."
  },
  {
    "id": "python-fundamentals-046",
    "title": "Why can rows = [[0] * 3] * 2 be surprising",
    "topic": "objects",
    "difficulty": "Intermediate",
    "question": "Why can rows = [[0] * 3] * 2 be surprising?",
    "options": [
      "It creates tuples",
      "Both rows reference the same inner list",
      "It sorts the rows",
      "It cannot be indexed"
    ],
    "correctIndex": 1,
    "explanation": "The outer multiplication repeats a reference to one inner list."
  },
  {
    "id": "python-fundamentals-047",
    "title": "Which operation mutates a list in place",
    "topic": "collections",
    "difficulty": "Easy",
    "question": "Which operation mutates a list in place?",
    "options": [
      "sorted(items)",
      "items + [value]",
      "items.append(value)",
      "items[:]"
    ],
    "correctIndex": 2,
    "explanation": "append changes the existing list and returns None."
  },
  {
    "id": "python-fundamentals-048",
    "title": "What is the difference between sorted(items) and items.sort()",
    "topic": "collections",
    "difficulty": "Easy",
    "question": "What is the difference between sorted(items) and items.sort()?",
    "options": [
      "They always return the same new list",
      "sorted returns a new list; sort mutates a list and returns None",
      "sort works on every iterable and sorted does not",
      "sorted mutates tuples"
    ],
    "correctIndex": 1,
    "explanation": "sorted accepts any iterable; list.sort is an in-place list method."
  },
  {
    "id": "python-fundamentals-049",
    "title": "What does the key parameter to sorted commonly specify",
    "topic": "collections",
    "difficulty": "Intermediate",
    "question": "What does the key parameter to sorted commonly specify?",
    "options": [
      "A comparison result to mutate",
      "A function that produces each item's sort key",
      "The dictionary key to delete",
      "A type annotation"
    ],
    "correctIndex": 1,
    "explanation": "For example, key=len sorts strings by length."
  },
  {
    "id": "python-fundamentals-050",
    "title": "What does reversed(sequence) return",
    "topic": "iteration",
    "difficulty": "Easy",
    "question": "What does reversed(sequence) return?",
    "options": [
      "Always a new reversed list",
      "An iterator that yields items in reverse order",
      "The original sequence changed in place",
      "A set of reversed items"
    ],
    "correctIndex": 1,
    "explanation": "Wrap it in list() if a materialized list is needed."
  },
  {
    "id": "python-fundamentals-051",
    "title": "Which string method removes leading and trailing whitespace",
    "topic": "strings",
    "difficulty": "Easy",
    "question": "Which string method removes leading and trailing whitespace?",
    "options": [
      "trim()",
      "strip()",
      "clean()",
      "split()"
    ],
    "correctIndex": 1,
    "explanation": "str.strip removes leading and trailing whitespace by default."
  },
  {
    "id": "python-fundamentals-052",
    "title": "What does 'a,b,c'.split(',') return",
    "topic": "strings",
    "difficulty": "Easy",
    "question": "What does 'a,b,c'.split(',') return?",
    "options": [
      "['a', 'b', 'c']",
      "('a', 'b', 'c')",
      "'abc'",
      "A generator"
    ],
    "correctIndex": 0,
    "explanation": "split returns a list of substrings."
  },
  {
    "id": "python-fundamentals-053",
    "title": "What is an f-string used for",
    "topic": "strings",
    "difficulty": "Easy",
    "question": "What is an f-string used for?",
    "options": [
      "Binary file reading",
      "String formatting with embedded expressions",
      "Function annotation only",
      "Creating frozensets"
    ],
    "correctIndex": 1,
    "explanation": "An f-prefix allows expressions inside braces, such as f'{name}'."
  },
  {
    "id": "python-fundamentals-054",
    "title": "What does the r prefix on a string literal do",
    "topic": "strings",
    "difficulty": "Easy",
    "question": "What does the r prefix on a string literal do?",
    "options": [
      "Reverses the string",
      "Creates a raw string where backslashes are not normally treated as escapes",
      "Makes the string read-only",
      "Rounds numeric text"
    ],
    "correctIndex": 1,
    "explanation": "Raw strings are useful for many regular-expression and path literals."
  },
  {
    "id": "python-fundamentals-055",
    "title": "Which module is most appropriate for regular expressions",
    "topic": "standard-library",
    "difficulty": "Easy",
    "question": "Which module is most appropriate for regular expressions?",
    "options": [
      "rx",
      "regex",
      "re",
      "match"
    ],
    "correctIndex": 2,
    "explanation": "The standard library regular-expression module is re."
  },
  {
    "id": "python-fundamentals-056",
    "title": "What is a class in Python",
    "topic": "oop",
    "difficulty": "Easy",
    "question": "What is a class in Python?",
    "options": [
      "A blueprint for creating objects",
      "An instance variable",
      "A built-in exception",
      "A package manager"
    ],
    "correctIndex": 0,
    "explanation": "Classes define behavior and shared structure for instances."
  },
  {
    "id": "python-fundamentals-057",
    "title": "What does self conventionally refer to in an instance method",
    "topic": "oop",
    "difficulty": "Easy",
    "question": "What does self conventionally refer to in an instance method?",
    "options": [
      "The class object",
      "The current instance",
      "The module",
      "The superclass only"
    ],
    "correctIndex": 1,
    "explanation": "Python passes the instance as the first argument to an instance method."
  },
  {
    "id": "python-fundamentals-058",
    "title": "Which method commonly initializes a new instance",
    "topic": "oop",
    "difficulty": "Easy",
    "question": "Which method commonly initializes a new instance?",
    "options": [
      "__new__ only",
      "__init__",
      "__start__",
      "__create__"
    ],
    "correctIndex": 1,
    "explanation": "__init__ initializes an instance after it is created."
  },
  {
    "id": "python-fundamentals-059",
    "title": "What is a class attribute",
    "topic": "oop",
    "difficulty": "Intermediate",
    "question": "What is a class attribute?",
    "options": [
      "An attribute stored on the class and shared unless shadowed",
      "An attribute available only in __init__",
      "An attribute each instance must copy",
      "A private module variable"
    ],
    "correctIndex": 0,
    "explanation": "Instances can read class attributes, but assigning through an instance can shadow one."
  },
  {
    "id": "python-fundamentals-060",
    "title": "What does @classmethod make the first parameter receive",
    "topic": "oop",
    "difficulty": "Intermediate",
    "question": "What does @classmethod make the first parameter receive?",
    "options": [
      "The current instance",
      "The class",
      "The module",
      "The parent instance"
    ],
    "correctIndex": 1,
    "explanation": "A class method receives cls and is often used for alternate constructors."
  },
  {
    "id": "python-fundamentals-061",
    "title": "What is @staticmethod useful for",
    "topic": "oop",
    "difficulty": "Intermediate",
    "question": "What is @staticmethod useful for?",
    "options": [
      "A method needing instance state",
      "A utility placed on a class that needs neither instance nor class state",
      "Making all attributes immutable",
      "Creating a singleton"
    ],
    "correctIndex": 1,
    "explanation": "Static methods receive no automatic self or cls argument."
  },
  {
    "id": "python-fundamentals-062",
    "title": "What does @property let callers use",
    "topic": "oop",
    "difficulty": "Intermediate",
    "question": "What does @property let callers use?",
    "options": [
      "A method through attribute-style access",
      "A private attribute from another module",
      "A class as a dictionary",
      "A generator as a list"
    ],
    "correctIndex": 0,
    "explanation": "Properties expose computed or validated values with obj.name syntax."
  },
  {
    "id": "python-fundamentals-063",
    "title": "What is inheritance",
    "topic": "oop",
    "difficulty": "Easy",
    "question": "What is inheritance?",
    "options": [
      "A subclass reusing and extending a base class",
      "Copying a dictionary",
      "A way to import modules",
      "A file permission model"
    ],
    "correctIndex": 0,
    "explanation": "Inheritance expresses an is-a relationship and supports behavior reuse."
  },
  {
    "id": "python-fundamentals-064",
    "title": "Why is super() commonly used in an overriding method",
    "topic": "oop",
    "difficulty": "Intermediate",
    "question": "Why is super() commonly used in an overriding method?",
    "options": [
      "To call the appropriate parent implementation",
      "To make the method static",
      "To remove inheritance",
      "To catch every exception"
    ],
    "correctIndex": 0,
    "explanation": "super helps cooperative inheritance follow method resolution order."
  },
  {
    "id": "python-fundamentals-065",
    "title": "What is polymorphism in Python",
    "topic": "oop",
    "difficulty": "Intermediate",
    "question": "What is polymorphism in Python?",
    "options": [
      "Different objects responding to the same operation through a common interface",
      "Only multiple inheritance",
      "Changing an object's id",
      "Converting all values to strings"
    ],
    "correctIndex": 0,
    "explanation": "Python often relies on duck typing: behavior matters more than exact type."
  },
  {
    "id": "python-fundamentals-066",
    "title": "What does __repr__ aim to provide",
    "topic": "oop",
    "difficulty": "Intermediate",
    "question": "What does __repr__ aim to provide?",
    "options": [
      "A developer-oriented representation of an object",
      "A guaranteed JSON encoding",
      "An object's hash",
      "A destructor"
    ],
    "correctIndex": 0,
    "explanation": "repr is intended to be unambiguous and useful for debugging."
  },
  {
    "id": "python-fundamentals-067",
    "title": "What does __str__ aim to provide",
    "topic": "oop",
    "difficulty": "Intermediate",
    "question": "What does __str__ aim to provide?",
    "options": [
      "A user-friendly string representation",
      "An integer conversion",
      "A method-resolution order",
      "A class constructor"
    ],
    "correctIndex": 0,
    "explanation": "str(obj) calls __str__ when defined."
  },
  {
    "id": "python-fundamentals-068",
    "title": "What happens if a class overrides __eq__ but does not define __hash__",
    "topic": "hashing",
    "difficulty": "Advanced",
    "question": "What happens if a class overrides __eq__ but does not define __hash__?",
    "options": [
      "Instances are automatically sortable",
      "Instances become unhashable by default",
      "Equality is ignored",
      "They become immutable"
    ],
    "correctIndex": 1,
    "explanation": "Python sets __hash__ to None in this case to preserve the rule that equal hashable objects need equal hashes."
  },
  {
    "id": "python-fundamentals-069",
    "title": "What does dataclasses.dataclass primarily reduce",
    "topic": "standard-library",
    "difficulty": "Intermediate",
    "question": "What does dataclasses.dataclass primarily reduce?",
    "options": [
      "Network latency",
      "Boilerplate for data-holding classes",
      "The need for all imports",
      "Thread scheduling"
    ],
    "correctIndex": 1,
    "explanation": "It can generate methods such as __init__, __repr__, and __eq__ from fields."
  },
  {
    "id": "python-fundamentals-070",
    "title": "What is the default visibility of an attribute named _value",
    "topic": "oop",
    "difficulty": "Easy",
    "question": "What is the default visibility of an attribute named _value?",
    "options": [
      "Truly private and inaccessible",
      "A convention that it is internal",
      "Public only to subclasses",
      "Read-only"
    ],
    "correctIndex": 1,
    "explanation": "One leading underscore is a convention, not enforced access control."
  },
  {
    "id": "python-fundamentals-071",
    "title": "What does a name such as __value inside a class trigger",
    "topic": "oop",
    "difficulty": "Intermediate",
    "question": "What does a name such as __value inside a class trigger?",
    "options": [
      "Automatic deletion",
      "Name mangling",
      "A syntax error",
      "A static method"
    ],
    "correctIndex": 1,
    "explanation": "Double-leading underscores mangle the name to reduce accidental subclass clashes."
  },
  {
    "id": "python-fundamentals-072",
    "title": "What does import module do",
    "topic": "modules",
    "difficulty": "Easy",
    "question": "What does import module do?",
    "options": [
      "Imports a module object under the name module",
      "Imports every name directly into local scope",
      "Runs no module code",
      "Creates a package"
    ],
    "correctIndex": 0,
    "explanation": "Access exported names as module.name unless a different import form is used."
  },
  {
    "id": "python-fundamentals-073",
    "title": "What does if __name__ == '__main__': guard",
    "topic": "modules",
    "difficulty": "Easy",
    "question": "What does if __name__ == '__main__': guard?",
    "options": [
      "Code intended to run when the file is executed as the main program",
      "Only test functions",
      "Code that must run on every import",
      "A module's package name"
    ],
    "correctIndex": 0,
    "explanation": "Imported modules receive their module name rather than __main__."
  },
  {
    "id": "python-fundamentals-074",
    "title": "What is a Python virtual environment for",
    "topic": "packaging",
    "difficulty": "Easy",
    "question": "What is a Python virtual environment for?",
    "options": [
      "Speeding up loops",
      "Isolating a project's Python interpreter and packages",
      "Replacing unit tests",
      "Encrypting source files"
    ],
    "correctIndex": 1,
    "explanation": "Virtual environments avoid mixing project dependencies."
  },
  {
    "id": "python-fundamentals-075",
    "title": "Which standard-library module is commonly used to parse JSON",
    "topic": "standard-library",
    "difficulty": "Easy",
    "question": "Which standard-library module is commonly used to parse JSON?",
    "options": [
      "json",
      "yaml",
      "pickle",
      "csv"
    ],
    "correctIndex": 0,
    "explanation": "json.loads parses text and json.dumps serializes Python data."
  },
  {
    "id": "python-fundamentals-076",
    "title": "Why should pickle be avoided for untrusted data",
    "topic": "security",
    "difficulty": "Intermediate",
    "question": "Why should pickle be avoided for untrusted data?",
    "options": [
      "It can execute arbitrary code while unpickling",
      "It cannot serialize lists",
      "It uses too little memory",
      "It only works on Windows"
    ],
    "correctIndex": 0,
    "explanation": "Unpickling untrusted bytes is a code-execution security risk."
  },
  {
    "id": "python-fundamentals-077",
    "title": "What does the csv module help with",
    "topic": "standard-library",
    "difficulty": "Easy",
    "question": "What does the csv module help with?",
    "options": [
      "Parsing and writing comma-separated tabular data",
      "Compiling Python code",
      "Managing threads",
      "Encrypting files"
    ],
    "correctIndex": 0,
    "explanation": "csv provides reader, writer, DictReader, and DictWriter utilities."
  },
  {
    "id": "python-fundamentals-078",
    "title": "What is the usual time complexity of average dictionary lookup",
    "topic": "complexity",
    "difficulty": "Intermediate",
    "question": "What is the usual time complexity of average dictionary lookup?",
    "options": [
      "O(1)",
      "O(log n)",
      "O(n)",
      "O(n log n)"
    ],
    "correctIndex": 0,
    "explanation": "Hash-table lookup is expected constant time, though pathological cases exist."
  },
  {
    "id": "python-fundamentals-079",
    "title": "What is the usual time complexity of list.append",
    "topic": "complexity",
    "difficulty": "Intermediate",
    "question": "What is the usual time complexity of list.append?",
    "options": [
      "O(1) amortized",
      "O(n) always",
      "O(log n)",
      "O(n squared)"
    ],
    "correctIndex": 0,
    "explanation": "Lists occasionally resize, but appends are amortized constant time."
  },
  {
    "id": "python-fundamentals-080",
    "title": "Which collection is best for efficiently removing from both ends",
    "topic": "standard-library",
    "difficulty": "Intermediate",
    "question": "Which collection is best for efficiently removing from both ends?",
    "options": [
      "list",
      "tuple",
      "collections.deque",
      "frozenset"
    ],
    "correctIndex": 2,
    "explanation": "deque supports O(1) appends and pops at both ends."
  },
  {
    "id": "python-fundamentals-081",
    "title": "What does collections.Counter provide",
    "topic": "standard-library",
    "difficulty": "Easy",
    "question": "What does collections.Counter provide?",
    "options": [
      "A mapping of elements to their counts",
      "A sorted set",
      "A thread lock",
      "A file iterator"
    ],
    "correctIndex": 0,
    "explanation": "Counter is a dictionary subclass for tallying hashable objects."
  },
  {
    "id": "python-fundamentals-082",
    "title": "What is a common use of collections.defaultdict",
    "topic": "standard-library",
    "difficulty": "Intermediate",
    "question": "What is a common use of collections.defaultdict?",
    "options": [
      "Avoid handling missing keys manually by supplying a default factory",
      "Create immutable dictionaries",
      "Sort dictionaries in place",
      "Make keys case-insensitive"
    ],
    "correctIndex": 0,
    "explanation": "For example, defaultdict(list) creates an empty list for a new key."
  },
  {
    "id": "python-fundamentals-083",
    "title": "What does functools.lru_cache do",
    "topic": "standard-library",
    "difficulty": "Intermediate",
    "question": "What does functools.lru_cache do?",
    "options": [
      "Caches recent function calls by arguments",
      "Creates a thread pool",
      "Converts a function into a list",
      "Locks a file"
    ],
    "correctIndex": 0,
    "explanation": "It memoizes results for hashable arguments, often speeding repeated pure computations."
  },
  {
    "id": "python-fundamentals-084",
    "title": "Which statement about threads and the CPython GIL is accurate",
    "topic": "concurrency",
    "difficulty": "Advanced",
    "question": "Which statement about threads and the CPython GIL is accurate?",
    "options": [
      "Threads never overlap any work",
      "Threads can help I/O-bound tasks, but CPU-bound Python bytecode does not run in parallel under one GIL",
      "Threads make CPU-bound Python bytecode always use all cores",
      "The GIL applies only to asyncio"
    ],
    "correctIndex": 1,
    "explanation": "I/O operations may release the GIL, while CPU parallelism commonly uses processes or native code."
  },
  {
    "id": "python-fundamentals-085",
    "title": "What is asyncio primarily designed for",
    "topic": "concurrency",
    "difficulty": "Intermediate",
    "question": "What is asyncio primarily designed for?",
    "options": [
      "Cooperative concurrency for many I/O-bound operations",
      "Automatic CPU parallelism for ordinary functions",
      "Replacing all threads in every program",
      "Compiling Python to C"
    ],
    "correctIndex": 0,
    "explanation": "An event loop switches between tasks at await points."
  },
  {
    "id": "python-fundamentals-086",
    "title": "What does await require",
    "topic": "concurrency",
    "difficulty": "Intermediate",
    "question": "What does await require?",
    "options": [
      "A regular list",
      "An awaitable, normally inside an async function",
      "A global variable",
      "A classmethod"
    ],
    "correctIndex": 1,
    "explanation": "await suspends a coroutine until its awaitable completes."
  },
  {
    "id": "python-fundamentals-087",
    "title": "What does the threading.Lock context manager help prevent",
    "topic": "concurrency",
    "difficulty": "Intermediate",
    "question": "What does the threading.Lock context manager help prevent?",
    "options": [
      "Race conditions around a critical section",
      "All exceptions",
      "Garbage collection",
      "Dictionary key collisions"
    ],
    "correctIndex": 0,
    "explanation": "with lock: ensures only one holder enters the guarded code at a time."
  },
  {
    "id": "python-fundamentals-088",
    "title": "What is a race condition",
    "topic": "concurrency",
    "difficulty": "Intermediate",
    "question": "What is a race condition?",
    "options": [
      "A deterministic ordering of tasks",
      "A bug where results depend on unpredictable operation timing",
      "An invalid import",
      "A slow for loop"
    ],
    "correctIndex": 1,
    "explanation": "Unsynchronized shared-state access can produce race conditions."
  },
  {
    "id": "python-fundamentals-089",
    "title": "What does id(obj) represent during an object's lifetime",
    "topic": "objects",
    "difficulty": "Intermediate",
    "question": "What does id(obj) represent during an object's lifetime?",
    "options": [
      "Its value equality",
      "Its identity as an integer unique among live objects",
      "Its hash value always",
      "Its class name"
    ],
    "correctIndex": 1,
    "explanation": "In CPython it is typically related to the memory address, but code should treat it as identity only."
  },
  {
    "id": "python-fundamentals-090",
    "title": "Which group contains only immutable built-in scalar types",
    "topic": "types",
    "difficulty": "Easy",
    "question": "Which group contains only immutable built-in scalar types?",
    "options": [
      "int, float, bool, str",
      "list, dict, set, bytearray",
      "list, tuple, dict, set",
      "dict, frozenset, list, bytearray"
    ],
    "correctIndex": 0,
    "explanation": "Those scalar values cannot be modified in place; rebinding a name creates or references another object."
  },
  {
    "id": "python-fundamentals-091",
    "title": "Is a tuple always hashable",
    "topic": "hashing",
    "difficulty": "Intermediate",
    "question": "Is a tuple always hashable?",
    "options": [
      "Yes",
      "No; it is hashable only when all contained values are hashable",
      "No tuple can be hashed",
      "Only empty tuples are hashable"
    ],
    "correctIndex": 1,
    "explanation": "A tuple containing a list is unhashable because the list is unhashable."
  },
  {
    "id": "python-fundamentals-092",
    "title": "What does all(values) return",
    "topic": "truthiness",
    "difficulty": "Intermediate",
    "question": "What does all(values) return?",
    "options": [
      "True if every item is truthy, or True for an empty iterable",
      "True if any item is truthy",
      "A list of truthy items",
      "False for every empty iterable"
    ],
    "correctIndex": 0,
    "explanation": "all uses vacuous truth for an empty iterable."
  },
  {
    "id": "python-fundamentals-093",
    "title": "What does any(values) return for an empty iterable",
    "topic": "truthiness",
    "difficulty": "Easy",
    "question": "What does any(values) return for an empty iterable?",
    "options": [
      "True",
      "False",
      "None",
      "It raises StopIteration"
    ],
    "correctIndex": 1,
    "explanation": "There is no truthy element in an empty iterable."
  },
  {
    "id": "python-fundamentals-094",
    "title": "What kind of error does int('three') raise",
    "topic": "exceptions",
    "difficulty": "Easy",
    "question": "What kind of error does int('three') raise?",
    "options": [
      "TypeError",
      "KeyError",
      "ValueError",
      "IndexError"
    ],
    "correctIndex": 2,
    "explanation": "The input is a string but not a valid integer literal."
  },
  {
    "id": "python-fundamentals-095",
    "title": "What kind of error does 'x' + 1 raise",
    "topic": "exceptions",
    "difficulty": "Easy",
    "question": "What kind of error does 'x' + 1 raise?",
    "options": [
      "ValueError",
      "TypeError",
      "NameError",
      "AttributeError"
    ],
    "correctIndex": 1,
    "explanation": "Python cannot concatenate a string and an integer."
  },
  {
    "id": "python-fundamentals-096",
    "title": "What kind of error does unknown_name raise when it has not been defined",
    "topic": "exceptions",
    "difficulty": "Easy",
    "question": "What kind of error does unknown_name raise when it has not been defined?",
    "options": [
      "NameError",
      "KeyError",
      "ImportError",
      "RuntimeError"
    ],
    "correctIndex": 0,
    "explanation": "NameError indicates that normal scope lookup could not find the name."
  },
  {
    "id": "python-fundamentals-097",
    "title": "What does isinstance(value, int) check",
    "topic": "types",
    "difficulty": "Easy",
    "question": "What does isinstance(value, int) check?",
    "options": [
      "Whether value is exactly the int class object",
      "Whether value is an instance of int or its subclasses",
      "Whether value can be converted to int",
      "Whether value has an integer hash"
    ],
    "correctIndex": 1,
    "explanation": "isinstance supports inheritance-aware type checks."
  },
  {
    "id": "python-fundamentals-098",
    "title": "What does type(value) is int check",
    "topic": "types",
    "difficulty": "Intermediate",
    "question": "What does type(value) is int check?",
    "options": [
      "Whether value is an int or subclass",
      "Whether value has exactly type int",
      "Whether value can be cast to int",
      "Whether value is truthy"
    ],
    "correctIndex": 1,
    "explanation": "Exact type identity excludes instances of int subclasses."
  },
  {
    "id": "python-fundamentals-099",
    "title": "What is PEP 8",
    "topic": "tooling",
    "difficulty": "Easy",
    "question": "What is PEP 8?",
    "options": [
      "Python's style-guide convention document",
      "The Python package installer",
      "A runtime optimizer",
      "A replacement for unit tests"
    ],
    "correctIndex": 0,
    "explanation": "PEP 8 describes widely used Python code-style conventions."
  },
  {
    "id": "python-fundamentals-100",
    "title": "What is the purpose of a unit test",
    "topic": "testing",
    "difficulty": "Easy",
    "question": "What is the purpose of a unit test?",
    "options": [
      "Check a small unit of behavior automatically",
      "Deploy an application",
      "Replace code review",
      "Measure network bandwidth"
    ],
    "correctIndex": 0,
    "explanation": "Unit tests provide fast, repeatable checks of focused behavior."
  }
];
