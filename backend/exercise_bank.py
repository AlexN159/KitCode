"""A local, dependency-free bank of Python stdin/stdout interview drills.

The catalogue deliberately stores the complete exercise payload used by the UI.
The runner is intentionally small: it executes a submitted script in an isolated
temporary directory, compares normalized stdout, and never exposes hidden cases
through ``get_catalog``.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import os
import signal
import subprocess
import sys
import tempfile
import threading
import time
from typing import Callable, Iterable


class _SubmissionProcess:
    """A short-lived subprocess contained with platform-native primitives.

    Windows Job Objects are important here: terminating only the parent Python
    process leaves any child it spawned running.  KILL_ON_JOB_CLOSE applies to
    the complete descendant tree.  Other platforms use a new session and kill
    its process group as the stdlib-only fallback.
    """

    _MEMORY_CAP_BYTES = 256 * 1024 * 1024

    def __init__(self, command: list[str], **kwargs: object) -> None:
        self._job_handle = None
        self._job_assigned = False
        self._windows = os.name == "nt"
        if self._windows:
            kwargs["creationflags"] = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        else:
            kwargs["start_new_session"] = True
        self.process = subprocess.Popen(command, **kwargs)  # type: ignore[arg-type]
        if self._windows:
            self._job_handle = self._create_windows_job()
            if self._job_handle is not None:
                self._job_assigned = self._assign_windows_job(self.process.pid, self._job_handle)

    @classmethod
    def _create_windows_job(cls):
        """Create a kill-on-close Job Object with a conservative memory cap."""
        try:
            import ctypes
            from ctypes import wintypes

            class _IO_COUNTERS(ctypes.Structure):
                _fields_ = [(name, ctypes.c_ulonglong) for name in (
                    "ReadOperationCount", "WriteOperationCount", "OtherOperationCount",
                    "ReadTransferCount", "WriteTransferCount", "OtherTransferCount",
                )]

            class _BASIC_LIMIT(ctypes.Structure):
                _fields_ = [
                    ("PerProcessUserTimeLimit", ctypes.c_longlong), ("PerJobUserTimeLimit", ctypes.c_longlong),
                    ("LimitFlags", wintypes.DWORD), ("MinimumWorkingSetSize", ctypes.c_size_t),
                    ("MaximumWorkingSetSize", ctypes.c_size_t), ("ActiveProcessLimit", wintypes.DWORD),
                    ("Affinity", ctypes.c_size_t), ("PriorityClass", wintypes.DWORD), ("SchedulingClass", wintypes.DWORD),
                ]

            class _EXTENDED_LIMIT(ctypes.Structure):
                _fields_ = [("BasicLimitInformation", _BASIC_LIMIT), ("IoInfo", _IO_COUNTERS),
                           ("ProcessMemoryLimit", ctypes.c_size_t), ("JobMemoryLimit", ctypes.c_size_t),
                           ("PeakProcessMemoryUsed", ctypes.c_size_t), ("PeakJobMemoryUsed", ctypes.c_size_t)]

            kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            kernel32.CreateJobObjectW.argtypes = (ctypes.c_void_p, wintypes.LPCWSTR)
            kernel32.CreateJobObjectW.restype = wintypes.HANDLE
            handle = kernel32.CreateJobObjectW(None, None)
            if not handle:
                return None
            info = _EXTENDED_LIMIT()
            # JOB_OBJECT_LIMIT_PROCESS_MEMORY | JOB_OBJECT_LIMIT_JOB_MEMORY |
            # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
            info.BasicLimitInformation.LimitFlags = 0x100 | 0x200 | 0x2000
            info.ProcessMemoryLimit = cls._MEMORY_CAP_BYTES
            info.JobMemoryLimit = cls._MEMORY_CAP_BYTES
            kernel32.SetInformationJobObject.argtypes = (wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD)
            kernel32.SetInformationJobObject.restype = wintypes.BOOL
            if not kernel32.SetInformationJobObject(handle, 9, ctypes.byref(info), ctypes.sizeof(info)):
                kernel32.CloseHandle(handle)
                return None
            return handle
        except Exception:
            return None

    @staticmethod
    def _assign_windows_job(pid: int, job_handle: object) -> bool:
        try:
            import ctypes
            from ctypes import wintypes
            kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            kernel32.OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
            kernel32.OpenProcess.restype = wintypes.HANDLE
            kernel32.AssignProcessToJobObject.argtypes = (wintypes.HANDLE, wintypes.HANDLE)
            kernel32.AssignProcessToJobObject.restype = wintypes.BOOL
            kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
            # PROCESS_TERMINATE | PROCESS_SET_QUOTA
            process = kernel32.OpenProcess(0x0001 | 0x0100, False, pid)
            if process:
                assigned = bool(kernel32.AssignProcessToJobObject(job_handle, process))
                kernel32.CloseHandle(process)
                return assigned
        except Exception:
            # Timeout/process-group cleanup below remains available if assigning
            # a Job Object is unavailable in this host configuration.
            pass
        return False

    def terminate_tree(self) -> None:
        try:
            if self._windows:
                if self._job_handle is not None and self._job_assigned:
                    import ctypes
                    ctypes.WinDLL("kernel32", use_last_error=True).TerminateJobObject(self._job_handle, 1)
                elif self.process.poll() is None:
                    self.process.kill()
            else:
                if self.process.poll() is None:
                    os.killpg(self.process.pid, signal.SIGKILL)
        except (OSError, ProcessLookupError):
            pass

    def close(self) -> None:
        self.terminate_tree()
        try:
            self.process.wait(timeout=1)
        except subprocess.TimeoutExpired:
            self.terminate_tree()
            self.process.wait(timeout=1)
        if self._job_handle is not None:
            try:
                import ctypes
                kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
                # Explicit termination closes the small assignment race and is
                # also clearer than relying solely on KILL_ON_JOB_CLOSE.
                if self._job_assigned:
                    kernel32.TerminateJobObject(self._job_handle, 1)
                kernel32.CloseHandle(self._job_handle)
            except Exception:
                pass
            self._job_handle = None


_CAPTURE_LIMIT_BYTES = 64 * 1024


def _read_capped_stream(stream, limit: int, target: bytearray, state: dict[str, bool]) -> None:
    """Drain a pipe completely while retaining only a bounded prefix."""
    try:
        while True:
            chunk = stream.read(8192)
            if not chunk:
                return
            available = limit - len(target)
            if available > 0:
                target.extend(chunk[:available])
            if len(chunk) > available:
                state["truncated"] = True
    finally:
        stream.close()


def _run_capped(submission: _SubmissionProcess, input_text: str, timeout_seconds: float) -> tuple[str, str, int, bool, bool]:
    """Run a submission without ever accumulating unbounded output in memory.

    Returns stdout, stderr, return code, whether output was capped, and timeout
    state.  Reading both streams concurrently prevents a child blocking on one
    full OS pipe while the other is being consumed.
    """
    process = submission.process
    assert process.stdin is not None and process.stdout is not None and process.stderr is not None
    stdout, stderr = bytearray(), bytearray()
    output_state = {"truncated": False}
    readers = [
        threading.Thread(target=_read_capped_stream, args=(process.stdout, _CAPTURE_LIMIT_BYTES, stdout, output_state), daemon=True),
        threading.Thread(target=_read_capped_stream, args=(process.stderr, _CAPTURE_LIMIT_BYTES, stderr, output_state), daemon=True),
    ]
    for reader in readers:
        reader.start()
    try:
        process.stdin.write(input_text.encode("utf-8"))
    except BrokenPipeError:
        pass
    finally:
        process.stdin.close()
    timed_out = False
    try:
        process.wait(timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        timed_out = True
        submission.terminate_tree()
        process.wait(timeout=1)
    for reader in readers:
        reader.join(timeout=1)
    return (stdout.decode("utf-8", errors="replace"), stderr.decode("utf-8", errors="replace"),
            process.returncode if process.returncode is not None else -1, output_state["truncated"], timed_out)


def _norm(value: str) -> str:
    """Compare output forgiving only terminal whitespace, like most judges."""
    return "\n".join(line.rstrip() for line in value.replace("\r\n", "\n").strip().split("\n"))


STARTER = '''import sys


def solve() -> None:
    # Read from standard input and print the answer.
    pass


if __name__ == "__main__":
    solve()
'''


def _example(inp: str, output: str, explanation: str = "") -> dict:
    result = {"input": inp, "output": output}
    if explanation:
        result["explanation"] = explanation
    return result


def _exercise(
    *, key: str, title: str, difficulty: str, topics: list[str], description: str,
    constraints: list[str], cases: list[tuple[str, str]], solution: str,
    hints: list[str], complexity: str, frequency: str = "Common",
) -> dict:
    public = [{"input": a, "expected_output": b} for a, b in cases[:2]]
    hidden = [{"input": a, "expected_output": b} for a, b in cases[2:]]
    return {
        "id": key, "title": title, "difficulty": difficulty, "topics": topics,
        "interview_frequency": frequency, "description": description,
        "constraints": constraints, "examples": [_example(*cases[0])],
        "starter_code": STARTER, "hints": hints[:3], "solution": solution,
        "expected_complexity": complexity, "public_tests": public,
        "hidden_tests": hidden,
    }


def _int_solution(expression: str) -> str:
    return f'''import sys


def solve() -> None:
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        return
    n = data[0]
    print({expression})


if __name__ == "__main__":
    solve()
'''


def _single_int_bank() -> list[dict]:
    # title, expression over n, description, constraints, cases, difficulty, topics
    rows = [
        ("Parity Label", "'even' if n % 2 == 0 else 'odd'", "Read one integer. Print `even` when it is divisible by 2; otherwise print `odd`.", ["-10^9 <= n <= 10^9"], [(8,"even"),(-3,"odd"),(0,"even")], "Easy", ["math", "conditionals"]),
        ("Absolute Difference from Zero", "abs(n)", "Read one integer and print its distance from zero.", ["-10^12 <= n <= 10^12"], [(-42,"42"),(0,"0"),(91,"91")], "Easy", ["math"]),
        ("Sign Classifier", "'positive' if n > 0 else ('negative' if n < 0 else 'zero')", "Print `positive`, `negative`, or `zero` for the supplied integer.", ["-10^9 <= n <= 10^9"], [(7,"positive"),(-1,"negative"),(0,"zero")], "Easy", ["conditionals"]),
        ("Square a Number", "n * n", "Read an integer and print its square.", ["|n| <= 10^6"], [(12,"144"),(-5,"25"),(0,"0")], "Easy", ["math"]),
        ("Cube a Number", "n * n * n", "Read an integer and print its cube.", ["|n| <= 10^5"], [(4,"64"),(-3,"-27"),(0,"0")], "Easy", ["math"]),
        ("Next Multiple of Five", "((n + 4) // 5) * 5", "Print the smallest multiple of 5 that is at least n.", ["-10^9 <= n <= 10^9"], [(12,"15"),(15,"15"),(-8,"-5")], "Easy", ["math", "rounding"]),
        ("Inclusive Sum to N", "n * (n + 1) // 2", "Given a non-negative integer n, print 1 + 2 + ... + n.", ["0 <= n <= 10^9"], [(5,"15"),(1,"1"),(0,"0")], "Easy", ["math", "formula"]),
        ("Triangular Check", "'yes' if int((8*n+1)**0.5) ** 2 == 8*n+1 else 'no'", "Print `yes` if n is a triangular number (including 0), else `no`.", ["0 <= n <= 10^12"], [(15,"yes"),(14,"no"),(0,"yes")], "Medium", ["math", "binary-search"]),
        ("Digit Count", "len(str(abs(n)))", "Print how many decimal digits an integer has. Zero has one digit.", ["|n| <= 10^18"], [(-904,"3"),(0,"1"),(123456,"6")], "Easy", ["strings", "math"]),
        ("Last Digit", "abs(n) % 10", "Print the last decimal digit of an integer, ignoring a leading minus sign.", ["|n| <= 10^18"], [(-129,"9"),(40,"0"),(7,"7")], "Easy", ["math"]),
        ("Celsius to Fahrenheit", "n * 9 // 5 + 32", "Input is a Celsius temperature divisible by 5. Print the equivalent Fahrenheit temperature.", ["-1000 <= n <= 1000", "n is divisible by 5"], [(0,"32"),(25,"77"),(-40,"-40")], "Easy", ["math"]),
        ("Leap Year", "'yes' if n % 400 == 0 or (n % 4 == 0 and n % 100 != 0) else 'no'", "Print `yes` when a Gregorian calendar year is a leap year; otherwise `no`.", ["1 <= n <= 9999"], [(2024,"yes"),(1900,"no"),(2000,"yes")], "Easy", ["conditionals", "math"]),
    ]
    output: list[dict] = []
    for i, (title, expr, desc, cons, vals, diff, topics) in enumerate(rows, 1):
        cases = [(f"{n}\n", ans) for n, ans in vals]
        output.append(_exercise(key=f"number-{i:03}", title=title, difficulty=diff, topics=topics,
            description=desc, constraints=cons, cases=cases, solution=_int_solution(expr),
            hints=["Read the integer with `int(input())`.", "Write down the mathematical rule before coding.", "Print exactly the requested value."], complexity="O(1) time, O(1) space"))
    return output


def _list_problem(key: str, title: str, difficulty: str, topics: list[str], description: str,
                  constraints: list[str], cases: list[tuple[str, str]], body: str, hints: list[str], complexity: str) -> dict:
    solution = f'''import sys


def solve() -> None:
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    nums = list(map(int, tokens[1:1+n]))
{body}


if __name__ == "__main__":
    solve()
'''
    return _exercise(key=key, title=title, difficulty=difficulty, topics=topics,
        description=description, constraints=constraints, cases=cases, solution=solution,
        hints=hints, complexity=complexity)


def _array_bank() -> list[dict]:
    specs = [
        ("Array Sum", "Easy", ["arrays", "iteration"], "Print the sum of n integers.", [("5\n2 -1 3 0 4\n", "8"),("0\n\n", "0"),("3\n-5 -6 -7\n", "-18")], "    print(sum(nums))", "O(n) time, O(1) extra space"),
        ("Array Maximum", "Easy", ["arrays"], "Print the largest of n integers.", [("4\n-2 9 3 1\n", "9"),("1\n-7\n", "-7"),("5\n0 0 0 0 0\n", "0")], "    print(max(nums))", "O(n) time, O(1) extra space"),
        ("Array Minimum", "Easy", ["arrays"], "Print the smallest of n integers.", [("4\n-2 9 3 1\n", "-2"),("1\n8\n", "8"),("3\n0 -4 2\n", "-4")], "    print(min(nums))", "O(n) time, O(1) extra space"),
        ("Count Positive Values", "Easy", ["arrays", "iteration"], "Count values strictly greater than zero.", [("5\n-1 0 2 9 -4\n", "2"),("3\n0 0 0\n", "0"),("4\n1 2 3 4\n", "4")], "    print(sum(x > 0 for x in nums))", "O(n) time, O(1) extra space"),
        ("Count Even Values", "Easy", ["arrays", "iteration"], "Count integers divisible by two.", [("5\n1 2 3 4 8\n", "3"),("0\n\n", "0"),("3\n-2 -1 0\n", "2")], "    print(sum(x % 2 == 0 for x in nums))", "O(n) time, O(1) extra space"),
        ("Reverse Numbers", "Easy", ["arrays", "two-pointers"], "Print the n integers in reverse order, separated by one space.", [("4\n1 2 3 4\n", "4 3 2 1"),("1\n8\n", "8"),("0\n\n", "")], "    print(*reversed(nums))", "O(n) time, O(n) output space"),
        ("Adjacent Difference Sum", "Easy", ["arrays", "iteration"], "Print the sum of absolute differences between every adjacent pair.", [("4\n1 7 3 5\n", "12"),("1\n8\n", "0"),("3\n-2 -2 4\n", "6")], "    print(sum(abs(nums[i] - nums[i-1]) for i in range(1, n)))", "O(n) time, O(1) extra space"),
        ("Running Totals", "Easy", ["arrays", "prefix-sum"], "Print cumulative sums after each number.", [("4\n3 -1 2 5\n", "3 2 4 9"),("1\n7\n", "7"),("0\n\n", "")], "    total = 0\n    answer = []\n    for x in nums:\n        total += x\n        answer.append(total)\n    print(*answer)", "O(n) time, O(n) output space"),
        ("Second Distinct Largest", "Medium", ["arrays", "selection"], "Print the second-largest distinct value, or `NONE` if fewer than two distinct values exist.", [("5\n4 1 4 3 2\n", "3"),("3\n7 7 7\n", "NONE"),("2\n-1 -2\n", "-2")], "    values = sorted(set(nums), reverse=True)\n    print(values[1] if len(values) > 1 else 'NONE')", "O(n log n) time, O(n) space"),
        ("First Peak Index", "Medium", ["arrays", "iteration"], "Return the first index i whose value is greater than both neighbors. Endpoints are not peaks. Print -1 when none exists.", [("5\n1 3 2 4 4\n", "1"),("3\n1 2 3\n", "-1"),("5\n0 2 1 2 0\n", "1")], "    answer = -1\n    for i in range(1, n - 1):\n        if nums[i] > nums[i-1] and nums[i] > nums[i+1]:\n            answer = i\n            break\n    print(answer)", "O(n) time, O(1) extra space"),
        ("Move Zeros to End", "Easy", ["arrays", "two-pointers"], "Keep non-zero values in their original order, then append all zeros.", [("6\n0 1 0 3 12 0\n", "1 3 12 0 0 0"),("3\n0 0 0\n", "0 0 0"),("3\n1 2 3\n", "1 2 3")], "    answer = [x for x in nums if x != 0]\n    answer += [0] * (n - len(answer))\n    print(*answer)", "O(n) time, O(n) space"),
        ("Sorted Unique", "Easy", ["arrays", "hashing"], "Print distinct input values in ascending order.", [("6\n3 1 3 2 1 2\n", "1 2 3"),("1\n5\n", "5"),("0\n\n", "")], "    print(*sorted(set(nums)))", "O(n log n) time, O(n) space"),
        ("Frequency of Target", "Easy", ["arrays", "counting"], "Input gives n, then n integers, then target t. Print how many values equal t.", [("5\n1 2 2 3 2\n2\n", "3"),("0\n\n7\n", "0"),("3\n-1 0 -1\n-1\n", "2")], "    target = int(tokens[1+n])\n    print(nums.count(target))", "O(n) time, O(1) extra space"),
    ]
    out=[]
    for i, (title,diff,topics,desc,cases,body,complexity) in enumerate(specs,1):
        cons=["0 <= n <= 200,000", "Values fit in a signed 32-bit integer"]
        out.append(_list_problem(f"array-{i:03}", title,diff,topics,desc,cons,cases,body,
            ["Parse n before the list.", "Consider the empty-list boundary case.", "Avoid printing Python list brackets."],complexity))
    return out


def _text_problem(key: str, title: str, difficulty: str, description: str, cases: list[tuple[str,str]], body: str, topics: list[str], complexity: str) -> dict:
    solution=f'''import sys


def solve() -> None:
    text = sys.stdin.readline().rstrip("\\n")
{body}


if __name__ == "__main__":
    solve()
'''
    return _exercise(key=key,title=title,difficulty=difficulty,topics=topics,description=description,
      constraints=["Input text contains printable ASCII characters", "Length is at most 200,000"],cases=cases,solution=solution,
      hints=["Keep the newline out of the value.", "Think about the result for an empty string.", "Use a linear scan when possible."],complexity=complexity)


def _string_bank() -> list[dict]:
    specs=[
      ("Reverse Text","Easy","Print the input line in reverse character order.",[("hello\n","olleh"),("\n",""),("race car\n","rac ecar")],"    print(text[::-1])",["strings"],"O(n) time, O(n) space"),
      ("Vowel Count","Easy","Count English vowels (a, e, i, o, u), ignoring case.",[("Alphabet\n","3"),("rhythm\n","0"),("AEIOU\n","5")],"    print(sum(ch.lower() in 'aeiou' for ch in text))",["strings","counting"],"O(n) time, O(1) space"),
      ("Palindrome Ignoring Spaces","Easy","Print `yes` if text reads the same backward after removing spaces and ignoring case; otherwise print `no`.",[("Never odd or even\n","yes"),("python\n","no"),("\n","yes")],"    compact = ''.join(ch.lower() for ch in text if ch != ' ')\n    print('yes' if compact == compact[::-1] else 'no')",["strings","two-pointers"],"O(n) time, O(n) space"),
      ("First Unique Character","Medium","Print the first character that occurs exactly once, or `NONE` if every character repeats.",[("swiss\n","w"),("aabb\n","NONE"),("alphabet\n","l")],"    from collections import Counter\n    counts = Counter(text)\n    print(next((ch for ch in text if counts[ch] == 1), 'NONE'))",["strings","hashing"],"O(n) time, O(n) space"),
      ("Run Length Encode","Medium","Replace each consecutive run by its character followed by its count. For example, `aaabb` becomes `a3b2`.",[("aaabbc\n","a3b2c1"),("\n",""),("xxxx\n","x4")],"    if not text:\n        print()\n        return\n    parts = []\n    start = 0\n    for i in range(1, len(text) + 1):\n        if i == len(text) or text[i] != text[start]:\n            parts.append(text[start] + str(i - start))\n            start = i\n    print(''.join(parts))",["strings","two-pointers"],"O(n) time, O(n) space"),
      ("Balanced Brackets","Medium","Input contains only parentheses, square brackets, and braces. Print `yes` when brackets are correctly nested and closed; otherwise `no`.",[("{[()]}\n","yes"),("([)]\n","no"),("\n","yes")],"    pairs = {')': '(', ']': '[', '}': '{'}\n    stack = []\n    for ch in text:\n        if ch in '([{':\n            stack.append(ch)\n        elif not stack or stack.pop() != pairs[ch]:\n            print('no')\n            return\n    print('yes' if not stack else 'no')",["strings","stack"],"O(n) time, O(n) space"),
      ("Longest Word Length","Easy","Words are separated by one or more spaces. Print the length of the longest word, or 0 for a blank line.",[("write clear code\n","5"),("\n","0"),("a bb ccc\n","3")],"    print(max((len(word) for word in text.split()), default=0))",["strings"],"O(n) time, O(n) temporary space"),
      ("Title Case Words","Easy","Capitalize the first letter of each space-separated word and lowercase the rest.",[("hELLO woRLD\n","Hello World"),("one\n","One"),("\n","")],"    print(' '.join(word[:1].upper() + word[1:].lower() for word in text.split()))",["strings"],"O(n) time, O(n) space"),
      ("Anagram Signature","Easy","Read two lines. Print `yes` if they are anagrams after ignoring spaces and letter case; otherwise `no`.",[("listen\nsilent\n","yes"),("rail safety\nfairy tales\n","yes"),("cat\ndog\n","no")],"    other = sys.stdin.readline().rstrip('\\n')\n    normalize = lambda s: sorted(ch.lower() for ch in s if ch != ' ')\n    print('yes' if normalize(text) == normalize(other) else 'no')",["strings","sorting"],"O(n log n) time, O(n) space"),
      ("Character Histogram","Medium","Print each distinct character and its count in first-appearance order as `character:count`, separated by spaces.",[("banana\n","b:1 a:3 n:2"),("\n",""),("aab\n","a:2 b:1")],"    from collections import Counter\n    counts = Counter(text)\n    seen = set()\n    result = []\n    for ch in text:\n        if ch not in seen:\n            seen.add(ch)\n            result.append(f'{ch}:{counts[ch]}')\n    print(' '.join(result))",["strings","hashing"],"O(n) time, O(n) space"),
    ]
    return [_text_problem(f"string-{i:03}",a,b,c,d,e,f,g) for i,(a,b,c,d,e,f,g) in enumerate(specs,1)]


def _parametric_bank() -> list[dict]:
    """Exercises whose cases and solutions are individually specified below.

    This section covers the interview patterns that deserve their own problem,
    rather than disguising the same task under different nouns.
    """
    records = [
      ("two-sum-indices","Pair With Target","Easy",["arrays","hashing"],"Read n, n integers, then target. Print the first pair of zero-based indices `i j` with i < j whose values sum to target. Print `NONE` if absent.",[("4\n2 7 11 15\n9\n","0 1"),("3\n1 2 3\n7\n","NONE"),("4\n3 3 4 5\n6\n","0 1")],'''    target = int(tokens[n + 1])
    seen = {}
    for j, value in enumerate(nums):
        if target - value in seen:
            print(seen[target - value], j)
            return
        if value not in seen:
            seen[value] = j
    print('NONE')''',"O(n) time, O(n) space"),
      ("contains-duplicate","Contains Duplicate","Easy",["arrays","hashing"],"Print `yes` if any value appears at least twice; otherwise print `no`.",[("4\n1 2 3 1\n","yes"),("3\n1 2 3\n","no"),("0\n\n","no")],'''    print('yes' if len(set(nums)) != n else 'no')''',"O(n) time, O(n) space"),
      ("majority-value","Majority Value","Easy",["arrays","voting"],"A majority value occurs more than n/2 times, if one exists. Print it, or `NONE`.",[("5\n2 2 1 2 3\n","2"),("4\n1 2 1 2\n","NONE"),("1\n-1\n","-1")],'''    candidate = None
    count = 0
    for value in nums:
        if count == 0:
            candidate = value
        count += 1 if value == candidate else -1
    print(candidate if candidate is not None and nums.count(candidate) > n // 2 else 'NONE')''',"O(n) time, O(1) extra space"),
      ("valid-parentheses","Bracket Validator","Easy",["stack","strings"],"Read one bracket-only line and print `yes` when every opener is closed in the right order, else `no`.",[("([]{})\n","yes"),("(]\n","no"),("\n","yes")],'''    pairs = {')': '(', ']': '[', '}': '{'}
    stack = []
    for ch in sys.stdin.readline().strip():
        if ch in '([{': stack.append(ch)
        elif not stack or stack.pop() != pairs[ch]:
            print('no'); return
    print('yes' if not stack else 'no')''',"O(n) time, O(n) space"),
      ("binary-search","Binary Search Position","Easy",["arrays","binary-search"],"The n integers are sorted in nondecreasing order. Then a target is given. Print its first index, or -1.",[("5\n1 2 2 2 9\n2\n","1"),("3\n1 4 8\n3\n","-1"),("0\n\n5\n","-1")],'''    target = int(tokens[n + 1])
    lo, hi, answer = 0, n - 1, -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] >= target:
            if nums[mid] == target: answer = mid
            hi = mid - 1
        else: lo = mid + 1
    print(answer)''',"O(log n) time, O(1) space"),
      ("range-sum-query","Range Sum Query","Easy",["prefix-sum","arrays"],"Read n, the list, then inclusive indices l and r. Print the sum from l through r.",[("5\n2 4 1 3 5\n1 3\n","8"),("1\n7\n0 0\n","7"),("4\n-1 2 -3 4\n0 2\n","-2")],'''    left, right = map(int, tokens[n + 1:n + 3])
    prefix = [0]
    for value in nums: prefix.append(prefix[-1] + value)
    print(prefix[right + 1] - prefix[left])''',"O(n) preprocessing, O(1) query"),
      ("product-except-self","Product Except Self","Medium",["arrays","prefix-sum"],"Print for each position the product of every other integer. Do not use division.",[("4\n1 2 3 4\n","24 12 8 6"),("3\n0 2 3\n","6 0 0"),("1\n9\n","1")],'''    answer = [1] * n
    prefix = 1
    for i, value in enumerate(nums):
        answer[i] = prefix; prefix *= value
    suffix = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= suffix; suffix *= nums[i]
    print(*answer)''',"O(n) time, O(n) output space"),
      ("max-subarray","Maximum Contiguous Sum","Medium",["arrays","dynamic-programming"],"Print the largest sum of a non-empty contiguous subarray.",[("9\n-2 1 -3 4 -1 2 1 -5 4\n","6"),("3\n-4 -2 -7\n","-2"),("1\n5\n","5")],'''    best = current = nums[0]
    for value in nums[1:]:
        current = max(value, current + value)
        best = max(best, current)
    print(best)''',"O(n) time, O(1) space"),
      ("longest-consecutive","Longest Consecutive Run","Medium",["arrays","hashing"],"Print the length of the longest set of consecutive integer values, regardless of their input order.",[("6\n100 4 200 1 3 2\n","4"),("0\n\n","0"),("5\n1 2 0 1 3\n","4")],'''    values = set(nums)
    best = 0
    for value in values:
        if value - 1 not in values:
            length = 1
            while value + length in values: length += 1
            best = max(best, length)
    print(best)''',"O(n) expected time, O(n) space"),
      ("rotate-array","Rotate Right","Medium",["arrays","modulo"],"Read n, n integers, then k. Rotate the list right by k positions and print it.",[("5\n1 2 3 4 5\n2\n","4 5 1 2 3"),("3\n1 2 3\n3\n","1 2 3"),("0\n\n9\n","")],'''    k = int(tokens[n + 1]) if len(tokens) > n + 1 else 0
    if n: k %= n
    print(*(nums[-k:] + nums[:-k] if k else nums))''',"O(n) time, O(n) space"),
      ("merge-intervals","Merge Intervals","Medium",["intervals","sorting"],"Read n, then n lines of inclusive start/end pairs. Merge overlapping or touching intervals. Print one `start end` pair per line.",[("3\n1 3\n2 6\n8 10\n","1 6\n8 10"),("2\n1 2\n3 4\n","1 4"),("0\n","")],'''    values = list(map(int, tokens[1:]))
    intervals = sorted(zip(values[::2], values[1::2]))
    merged = []
    for start, end in intervals:
        if not merged or start > merged[-1][1] + 1: merged.append([start, end])
        else: merged[-1][1] = max(merged[-1][1], end)
    print(*(' '.join(map(str, pair)) for pair in merged), sep='\\n')''',"O(n log n) time, O(n) space"),
      ("daily-temperatures","Next Warmer Wait","Medium",["stack","arrays"],"For each temperature, print how many days until a strictly warmer value, or 0 if none exists.",[("8\n73 74 75 71 69 72 76 73\n","1 1 4 2 1 1 0 0"),("3\n80 79 78\n","0 0 0"),("1\n60\n","0")],'''    answer = [0] * n
    stack = []
    for i, value in enumerate(nums):
        while stack and nums[stack[-1]] < value:
            j = stack.pop(); answer[j] = i - j
        stack.append(i)
    print(*answer)''',"O(n) time, O(n) space"),
      ("min-stack-operations","Minimum Stack","Medium",["stack","simulation"],"Read q followed by q operations: `push x`, `pop`, or `min`. For every `min`, print the current minimum. It is guaranteed that pop/min are valid.",[("6\npush 3\npush 1\nmin\npop\nmin\npop\n","1\n3"),("4\npush -2\nmin\npush -3\nmin\n","-2\n-3"),("1\npush 8\n","")],'''    lines = sys.stdin.read().splitlines()
    stack, minimums, result = [], [], []
    for line in lines[1:]:
        parts = line.split()
        if not parts:
            continue
        if parts[0] == 'push':
            value = int(parts[1]); stack.append(value)
            minimums.append(value if not minimums else min(value, minimums[-1]))
        elif parts[0] == 'pop': stack.pop(); minimums.pop()
        else: result.append(str(minimums[-1]))
    print('\\n'.join(result))''',"O(1) per operation, O(q) space"),
    ]
    out=[]
    for key,title,diff,topics,description,cases,body,complexity in records:
        # Some records intentionally have custom line formats, so their solutions
        # use a token reader but remain valid for all listed cases.
        solution=f'''import sys


def solve() -> None:
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    nums = list(map(int, tokens[1:1+n]))
{body}


if __name__ == "__main__":
    solve()
'''
        out.append(_exercise(key=key,title=title,difficulty=diff,topics=topics,description=description,
            constraints=["Input sizes can reach 200,000 unless the operation count is stated", "All numbers fit in signed 32-bit integers"],cases=cases,solution=solution,
            hints=["Start by writing out the input shape.", "Name the invariant your loop maintains.", "Check empty and duplicate cases."],complexity=complexity,frequency="Very common"))
    return out


def _generated_drills() -> list[dict]:
    """Focused variants for practicing input/output fluency and core patterns.

    Each variant has a distinct operation and test oracle; these are not copies
    with renamed variables.
    """
    operations: list[tuple[str,str,str,Callable[[list[int]], str],str,str,list[str]]] = [
      ("Sum of Squares", "Print the sum of squares of all values.", "sum(x * x for x in nums)", lambda a: str(sum(x*x for x in a)), "Easy", "O(n) time, O(1) space", ["arrays", "math"]),
      ("Sum of Absolute Values", "Print the sum of the absolute values.", "sum(abs(x) for x in nums)", lambda a: str(sum(abs(x) for x in a)), "Easy", "O(n) time, O(1) space", ["arrays", "math"]),
      ("Count Negative Values", "Count values strictly below zero.", "sum(x < 0 for x in nums)", lambda a: str(sum(x < 0 for x in a)), "Easy", "O(n) time, O(1) space", ["arrays", "iteration"]),
      ("Average Floor", "Print the floor of the arithmetic mean. The list is non-empty.", "sum(nums) // n", lambda a: str(sum(a)//len(a)), "Easy", "O(n) time, O(1) space", ["arrays", "math"]),
      ("Range Width", "Print maximum minus minimum. Empty input has width 0.", "max(nums) - min(nums) if nums else 0", lambda a: str(max(a)-min(a) if a else 0), "Easy", "O(n) time, O(1) space", ["arrays"]),
      ("Strictly Increasing", "Print `yes` if every value is greater than the previous value; otherwise `no`.", "'yes' if all(nums[i] > nums[i-1] for i in range(1, n)) else 'no'", lambda a: 'yes' if all(a[i]>a[i-1] for i in range(1,len(a))) else 'no', "Easy", "O(n) time, O(1) space", ["arrays"]),
      ("Strictly Decreasing", "Print `yes` if every value is lower than the previous value; otherwise `no`.", "'yes' if all(nums[i] < nums[i-1] for i in range(1, n)) else 'no'", lambda a: 'yes' if all(a[i]<a[i-1] for i in range(1,len(a))) else 'no', "Easy", "O(n) time, O(1) space", ["arrays"]),
      ("Alternating Parity", "Print `yes` if adjacent values always have different parity.", "'yes' if all((nums[i] - nums[i-1]) % 2 for i in range(1, n)) else 'no'", lambda a: 'yes' if all((a[i]-a[i-1])%2 for i in range(1,len(a))) else 'no', "Easy", "O(n) time, O(1) space", ["arrays", "math"]),
      ("Odd Index Sum", "Print the sum of values at zero-based odd indices.", "sum(nums[1::2])", lambda a: str(sum(a[1::2])), "Easy", "O(n) time, O(1) space", ["arrays"]),
      ("Even Index Maximum", "Print the largest value at zero-based even indices, or `NONE` for an empty list.", "max(nums[::2]) if nums else 'NONE'", lambda a: str(max(a[::2]) if a else 'NONE'), "Easy", "O(n) time, O(1) space", ["arrays"]),
      ("First Negative Index", "Print the index of the first negative value, or -1.", "next((i for i, x in enumerate(nums) if x < 0), -1)", lambda a: str(next((i for i,x in enumerate(a) if x<0),-1)), "Easy", "O(n) time, O(1) space", ["arrays"]),
      ("Last Positive Index", "Print the index of the last positive value, or -1.", "next((i for i in range(n-1, -1, -1) if nums[i] > 0), -1)", lambda a: str(next((i for i in range(len(a)-1,-1,-1) if a[i]>0),-1)), "Easy", "O(n) time, O(1) space", ["arrays"]),
      ("Distinct Count", "Print how many distinct values are present.", "len(set(nums))", lambda a: str(len(set(a))), "Easy", "O(n) time, O(n) space", ["arrays", "hashing"]),
      ("Duplicate Excess", "Print how many entries remain after keeping only one copy of each value.", "n - len(set(nums))", lambda a: str(len(a)-len(set(a))), "Easy", "O(n) time, O(n) space", ["arrays", "hashing"]),
      ("Smallest Absolute Value", "Print the value with smallest absolute value; resolve ties by the smaller numeric value. Print `NONE` for empty input.", "min(nums, key=lambda x: (abs(x), x)) if nums else 'NONE'", lambda a: str(min(a,key=lambda x:(abs(x),x)) if a else 'NONE'), "Easy", "O(n) time, O(1) space", ["arrays", "math"]),
      ("Sorted Squares", "Square every value, sort the results, and print them.", "print(*sorted(x*x for x in nums)); return", lambda a: ' '.join(map(str,sorted(x*x for x in a))), "Easy", "O(n log n) time, O(n) space", ["arrays", "sorting"]),
      ("Median of Sorted List", "The list is sorted and non-empty with odd length. Print its middle value.", "nums[n // 2]", lambda a: str(a[len(a)//2]), "Easy", "O(1) time, O(1) space", ["arrays"]),
      ("Pairwise Minimum Sum", "Pair the first with last, second with second-last, and so on. Print the sum of the smaller values in every pair. n is even.", "sum(min(nums[i], nums[n-1-i]) for i in range(n // 2))", lambda a: str(sum(min(a[i],a[-1-i]) for i in range(len(a)//2))), "Medium", "O(n) time, O(1) space", ["arrays", "two-pointers"]),
      ("Local Valley Count", "Count non-endpoint values lower than both neighbours.", "sum(nums[i] < nums[i-1] and nums[i] < nums[i+1] for i in range(1, n-1))", lambda a: str(sum(a[i]<a[i-1] and a[i]<a[i+1] for i in range(1,len(a)-1))), "Easy", "O(n) time, O(1) space", ["arrays"]),
      ("Prefix Threshold Index", "Read n, n non-negative numbers, then a target. Print the first index where running sum reaches target, or -1.", "target = int(tokens[n+1])\n    total = 0\n    for i, x in enumerate(nums):\n        total += x\n        if total >= target: print(i); return\n    print(-1); return", lambda a: '', "Medium", "O(n) time, O(1) space", ["arrays", "prefix-sum"]),
    ]
    samples=[[2,-1,3,0],[0,0,0],[5],[-4,-1,2,7],[1,2,3,4,5]]
    out=[]
    for index,(title,desc,expr,oracle,diff,complexity,topics) in enumerate(operations,1):
        if title == "Prefix Threshold Index":
            case_data=[("4\n2 1 3 2\n5\n","2"),("3\n1 1 1\n5\n","-1"),("1\n5\n1\n","0")]
        else:
            case_data=[]
            for values in samples[:3]:
                if title == "Median of Sorted List": values=[1,4,9]
                if title == "Pairwise Minimum Sum": values=[1,5,2,4]
                case_data.append((str(len(values))+"\n"+" ".join(map(str,values))+"\n",oracle(values)))
        body = "    print(" + expr + ")" if not expr.startswith("print(") and "\n" not in expr else "    " + expr
        out.append(_list_problem(f"drill-{index:03}",title,diff,topics,desc,["0 <= n <= 200,000"],case_data,body,
            ["Write one small pass over the list.", "Use a named accumulator if the operation is not a direct built-in.", "Test the empty-list rule."],complexity))
    return out


def _scalar_drills() -> list[dict]:
    """Small but real full-script exercises for building fluent fundamentals."""
    rows = [
      ("Double Number", "n * 2", "Double the supplied integer.", [(6,"12"),(-4,"-8"),(0,"0")], "Easy", ["math"]),
      ("Triple Number", "n * 3", "Triple the supplied integer.", [(6,"18"),(-4,"-12"),(0,"0")], "Easy", ["math"]),
      ("Predecessor", "n - 1", "Print the integer immediately before n.", [(6,"5"),(-4,"-5"),(0,"-1")], "Easy", ["math"]),
      ("Successor", "n + 1", "Print the integer immediately after n.", [(6,"7"),(-4,"-3"),(0,"1")], "Easy", ["math"]),
      ("Remainder by Seven", "n % 7", "Print the non-negative remainder when n is divided by 7.", [(15,"1"),(-1,"6"),(0,"0")], "Easy", ["math"]),
      ("Divisible by Three", "'yes' if n % 3 == 0 else 'no'", "Print `yes` if n is divisible by 3, else `no`.", [(15,"yes"),(14,"no"),(0,"yes")], "Easy", ["math", "conditionals"]),
      ("Multiple of Ten", "'yes' if n % 10 == 0 else 'no'", "Print `yes` if n is divisible by 10, else `no`.", [(50,"yes"),(-1,"no"),(0,"yes")], "Easy", ["math", "conditionals"]),
      ("Clamp to Zero", "max(0, n)", "Print n when it is positive; otherwise print zero.", [(8,"8"),(-2,"0"),(0,"0")], "Easy", ["conditionals"]),
      ("Clamp to One Hundred", "min(100, max(0, n))", "Restrict n to the inclusive range 0 through 100.", [(45,"45"),(-2,"0"),(120,"100")], "Easy", ["conditionals"]),
      ("Nearest Lower Dozen", "n // 12 * 12", "Print the greatest multiple of 12 no greater than n.", [(29,"24"),(24,"24"),(-1,"-12")], "Easy", ["math"]),
      ("Is Power of Two", "'yes' if n > 0 and n & (n - 1) == 0 else 'no'", "Print `yes` exactly when n is a positive power of two.", [(16,"yes"),(18,"no"),(1,"yes")], "Medium", ["bit-manipulation", "math"]),
      ("Population Count", "bin(abs(n)).count('1')", "Print the number of 1 bits in the binary form of |n|.", [(13,"3"),(-8,"1"),(0,"0")], "Easy", ["bit-manipulation"]),
      ("Binary Representation", "bin(n)[2:] if n >= 0 else '-' + bin(-n)[2:]", "Print n in base 2 without a prefix.", [(10,"1010"),(-3,"-11"),(0,"0")], "Easy", ["bit-manipulation"]),
      ("Hex Representation", "hex(n)[2:].upper() if n >= 0 else '-' + hex(-n)[2:].upper()", "Print n in uppercase base 16 without a prefix.", [(26,"1A"),(-15,"-F"),(0,"0")], "Easy", ["math"]),
      ("Digit Sum", "sum(map(int, str(abs(n))))", "Print the sum of the decimal digits of n.", [(502,"7"),(-99,"18"),(0,"0")], "Easy", ["math", "strings"]),
      ("Digit Product", "__import__('functools').reduce(lambda a, b: a * b, map(int, str(abs(n))), 1)", "Print the product of the decimal digits of n. Zero has product 0.", [(502,"0"),(-39,"27"),(7,"7")], "Medium", ["math", "strings"]),
      ("Reverse Digits", "int(('-' if n < 0 else '') + str(abs(n))[::-1])", "Reverse the decimal digits, preserving a leading minus sign if present.", [(120,"21"),(-340,"-43"),(0,"0")], "Easy", ["math", "strings"]),
      ("Numeric Palindrome", "'yes' if str(abs(n)) == str(abs(n))[::-1] else 'no'", "Print `yes` when the digits of |n| form a palindrome.", [(1221,"yes"),(-120,"no"),(0,"yes")], "Easy", ["math", "strings"]),
      ("Digital Root", "0 if n == 0 else 1 + (abs(n) - 1) % 9", "Repeatedly sum decimal digits until one digit remains, and print that digit.", [(9875,"2"),(-18,"9"),(0,"0")], "Medium", ["math"]),
      ("Factorial", "__import__('math').factorial(n)", "Print n factorial.", [(5,"120"),(0,"1"),(8,"40320")], "Easy", ["math", "recursion"]),
      ("Fibonacci Number", "(lambda f: f(n))(lambda k: (lambda a,b: a)(*(__import__('functools').reduce(lambda p,_:(p[1],p[0]+p[1]), range(k), (0,1)))))", "Print the nth Fibonacci number where F(0)=0 and F(1)=1.", [(0,"0"),(7,"13"),(10,"55")], "Medium", ["dynamic-programming"]),
      ("Count Multiples up to N", "n // 4", "For non-negative n, count positive multiples of 4 no larger than n.", [(10,"2"),(4,"1"),(0,"0")], "Easy", ["math"]),
      ("Sum of Multiples of Three", "3 * (n // 3) * (n // 3 + 1) // 2", "For non-negative n, print the sum of positive multiples of 3 up to n.", [(10,"18"),(3,"3"),(0,"0")], "Medium", ["math", "formula"]),
      ("Sum of Odd Numbers", "(n * n)", "For non-negative n, print 1 + 3 + ... + (2n-1).", [(4,"16"),(1,"1"),(0,"0")], "Easy", ["math", "formula"]),
      ("Perfect Square Check", "'yes' if __import__('math').isqrt(n) ** 2 == n else 'no'", "For non-negative n, print `yes` if it is a perfect square.", [(49,"yes"),(50,"no"),(0,"yes")], "Easy", ["math"]),
      ("Integer Square Root", "__import__('math').isqrt(n)", "For non-negative n, print the greatest integer whose square is at most n.", [(20,"4"),(49,"7"),(0,"0")], "Easy", ["math", "binary-search"]),
      ("Prime Check", "'yes' if n >= 2 and all(n % d for d in range(2, __import__('math').isqrt(n) + 1)) else 'no'", "Print `yes` if n is prime, otherwise `no`.", [(29,"yes"),(1,"no"),(100,"no")], "Medium", ["math"]),
      ("Count Divisors", "sum(n % d == 0 for d in range(1, __import__('math').isqrt(n)+1)) * 2 - (__import__('math').isqrt(n) ** 2 == n)", "For positive n, print its number of positive divisors.", [(12,"6"),(1,"1"),(49,"3")], "Medium", ["math"]),
      ("Largest Proper Divisor", "1 if n > 1 else 0", "For positive n, print its largest proper divisor; print 0 when n is 1.", [(12,"6"),(1,"0"),(17,"1")], "Easy", ["math"]),
      ("Weeks and Days", "f'{n // 7} {n % 7}'", "Given a non-negative day count, print complete weeks then leftover days.", [(15,"2 1"),(7,"1 0"),(0,"0 0")], "Easy", ["math"]),
      ("Minutes to Hours", "f'{n // 60} {n % 60}'", "Given non-negative minutes, print complete hours then leftover minutes.", [(125,"2 5"),(60,"1 0"),(0,"0 0")], "Easy", ["math"]),
      ("Seconds to Clock", "f'{n // 3600} {(n % 3600) // 60} {n % 60}'", "Given non-negative seconds, print hours, minutes, seconds separated by spaces.", [(3661,"1 1 1"),(59,"0 0 59"),(0,"0 0 0")], "Easy", ["math"]),
      ("Quadrant from Signs", "'I' if n > 0 else ('II' if n == 0 else 'III')", "Print I for a positive number, II for zero, and III for a negative number.", [(2,"I"),(0,"II"),(-2,"III")], "Easy", ["conditionals"]),
      ("Letter Grade", "'A' if n >= 90 else ('B' if n >= 80 else ('C' if n >= 70 else ('D' if n >= 60 else 'F')))", "Given a score from 0 to 100, print A/B/C/D/F using 90/80/70/60 cutoffs.", [(91,"A"),(72,"C"),(59,"F")], "Easy", ["conditionals"]),
      ("Divisibility Labels", "'both' if n % 6 == 0 else ('two' if n % 2 == 0 else ('three' if n % 3 == 0 else 'neither'))", "Print `both`, `two`, `three`, or `neither` depending on divisibility by 2 and 3.", [(6,"both"),(4,"two"),(9,"three")], "Easy", ["conditionals"]),
      ("Taxicab Distance", "abs(n - 10) + 5", "A point lies at (n, 0). Print its Manhattan distance to fixed point (10, -5).", [(10,"5"),(0,"15"),(-5,"20")], "Easy", ["math"]),
      ("Double Until Threshold", "next(k for k in range(100) if n * (2 ** k) >= 100)", "For positive n no greater than 100, print how many doublings are needed to reach at least 100.", [(25,"2"),(100,"0"),(1,"7")], "Medium", ["math", "iteration"]),
      ("Collatz Next", "n // 2 if n % 2 == 0 else 3 * n + 1", "Print the next value in the Collatz rule.", [(6,"3"),(5,"16"),(1,"4")], "Easy", ["conditionals", "math"]),
      ("Distance to Nearest Multiple", "min(n % 10, 10 - n % 10)", "Print the smallest distance from n to a multiple of 10.", [(17,"3"),(20,"0"),(-1,"1")], "Easy", ["math"]),
      ("Base Seven Digit Count", "len(__import__('numpy').base_repr(abs(n), base=7))", "Print how many digits |n| uses in base 7.", [(49,"3"),(0,"1"),(6,"1")], "Medium", ["math"]),
      ("Odd Factorial Double", "__import__('math').factorial(2*n+1)", "Given non-negative n, print (2n+1)!.", [(1,"6"),(0,"1"),(3,"5040")], "Medium", ["math"]),
      ("Choose Two", "n * (n - 1) // 2", "Given non-negative n, print the number of ways to choose two items.", [(5,"10"),(1,"0"),(0,"0")], "Easy", ["math", "combinatorics"]),
      ("Chessboard Color", "'dark' if (n // 8 + n % 8) % 2 == 0 else 'light'", "Squares are numbered 0 to 63 row by row. Print `dark` or `light` for its checkerboard color.", [(0,"dark"),(1,"light"),(9,"dark")], "Easy", ["math"]),
      ("Day of Week Offset", "['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][n % 7]", "Day 0 is Mon. Given a possibly negative offset, print the resulting three-letter day.", [(0,"Mon"),(6,"Sun"),(-1,"Sun")], "Easy", ["modulo"]),
    ]
    out=[]
    for i,(title,expr,desc,values,diff,topics) in enumerate(rows,1):
        # Avoid optional third-party packages in learner solutions.
        if title == "Base Seven Digit Count":
            solution='''import sys\n\n\ndef solve() -> None:\n    n = abs(int(sys.stdin.read()))\n    count = 1\n    while n >= 7:\n        n //= 7\n        count += 1\n    print(count)\n\n\nif __name__ == "__main__":\n    solve()\n'''
        elif title == "Fibonacci Number":
            solution='''import sys\n\n\ndef solve() -> None:\n    n = int(sys.stdin.read())\n    a, b = 0, 1\n    for _ in range(n):\n        a, b = b, a + b\n    print(a)\n\n\nif __name__ == "__main__":\n    solve()\n'''
        elif title == "Largest Proper Divisor":
            solution='''import sys\nfrom math import isqrt\n\n\ndef solve() -> None:\n    n = int(sys.stdin.read())\n    if n == 1:\n        print(0)\n        return\n    for divisor in range(2, isqrt(n) + 1):\n        if n % divisor == 0:\n            print(n // divisor)\n            return\n    print(1)\n\n\nif __name__ == "__main__":\n    solve()\n'''
        else:
            solution=_int_solution(expr)
        complexity = "O(1) time, O(1) space" if diff == "Easy" else "See solution for the intended bound"
        constraints = ["-10^9 <= n <= 10^9 unless factorial is requested", "Use Python integer arithmetic"]
        if title in {"Factorial", "Odd Factorial Double"}: constraints = ["0 <= n <= 12", "Use Python integer arithmetic"]
        if title == "Fibonacci Number": constraints = ["0 <= n <= 90", "Use Python integer arithmetic"]
        if title == "Largest Proper Divisor":
            constraints = ["1 <= n <= 10^12", "Use a square-root divisor search"]
            complexity = "O(sqrt(n)) time, O(1) space"
        if title == "Base Seven Digit Count": constraints = ["|n| <= 10^18", "Zero uses one digit"]
        out.append(_exercise(key=f"fundamental-{i:03}",title=title,difficulty=diff,topics=topics,description=desc,
            constraints=constraints,cases=[(str(n)+"\n",answer) for n,answer in values],solution=solution,
            hints=["Parse a single integer.", "Use integer division (`//`) when the result must stay integral.", "Test the boundary examples carefully."],complexity=complexity))
    return out


def _hard_bank() -> list[dict]:
    """Multi-step problems used when learners are ready to narrate trade-offs."""
    raw = [
      ("hard-001", "Shortest Path in a Grid", ["graphs", "breadth-first-search"],
       "Read rows and columns, then a grid of `.` open cells and `#` walls. Starting at the top-left, print the fewest moves to the bottom-right, or -1 if unreachable. Start and end are always open.",
       [("3 3\n...\n.#.\n...\n", "4"), ("2 2\n.#\n#.\n", "-1"), ("1 1\n.\n", "0")],
'''    from collections import deque
    rows, cols = map(int, sys.stdin.readline().split())
    grid = [sys.stdin.readline().strip() for _ in range(rows)]
    queue = deque([(0, 0, 0)])
    seen = {(0, 0)}
    while queue:
        r, c, distance = queue.popleft()
        if (r, c) == (rows - 1, cols - 1):
            print(distance); return
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '.' and (nr, nc) not in seen:
                seen.add((nr, nc)); queue.append((nr, nc, distance + 1))
    print(-1)''', "O(rows × cols) time and space"),
      ("hard-002", "Minimum Coin Count", ["dynamic-programming"],
       "Read m, m positive coin values, then target. Print the fewest coins that make exactly target, or -1 when impossible. Each coin may be used repeatedly.",
       [("3\n1 3 4\n6\n", "2"), ("2\n2 4\n7\n", "-1"), ("3\n2 5 10\n0\n", "0")],
'''    m = int(sys.stdin.readline())
    coins = list(map(int, sys.stdin.readline().split()))
    target = int(sys.stdin.readline())
    best = [target + 1] * (target + 1)
    best[0] = 0
    for amount in range(1, target + 1):
        best[amount] = min((best[amount - coin] + 1 for coin in coins if coin <= amount), default=target + 1)
    print(best[target] if best[target] <= target else -1)''', "O(m × target) time, O(target) space"),
      ("hard-003", "Edit Distance", ["dynamic-programming", "strings"],
       "Read two lowercase words on separate lines. Print the minimum insertions, deletions, and replacements needed to change the first into the second.",
       [("kitten\nsitting\n", "3"), ("\nabc\n", "3"), ("same\nsame\n", "0")],
'''    first = sys.stdin.readline().rstrip('\\n')
    second = sys.stdin.readline().rstrip('\\n')
    previous = list(range(len(second) + 1))
    for i, left in enumerate(first, 1):
        current = [i]
        for j, right in enumerate(second, 1):
            current.append(previous[j - 1] if left == right else 1 + min(previous[j], current[-1], previous[j - 1]))
        previous = current
    print(previous[-1])''', "O(a × b) time, O(b) space"),
      ("hard-004", "Course Ordering", ["graphs", "topological-sort"],
       "Read n and m, then m prerequisite pairs `a b`, meaning a must happen before b. Print one valid ordering separated by spaces, or `CYCLE` when no ordering exists. When several nodes are ready, choose the smaller index first.",
       [("4 3\n0 1\n0 2\n1 3\n", "0 1 2 3"), ("2 2\n0 1\n1 0\n", "CYCLE"), ("3 0\n", "0 1 2")],
'''    import heapq
    n, m = map(int, sys.stdin.readline().split())
    graph = [[] for _ in range(n)]
    incoming = [0] * n
    for _ in range(m):
        a, b = map(int, sys.stdin.readline().split())
        graph[a].append(b); incoming[b] += 1
    ready = [i for i in range(n) if incoming[i] == 0]
    heapq.heapify(ready)
    order = []
    while ready:
        node = heapq.heappop(ready); order.append(node)
        for neighbor in graph[node]:
            incoming[neighbor] -= 1
            if incoming[neighbor] == 0: heapq.heappush(ready, neighbor)
    print(*order) if len(order) == n else print('CYCLE')''', "O((n + m) log n) time, O(n + m) space"),
      ("hard-005", "Largest Rectangle", ["stack", "arrays"],
       "Read n followed by n non-negative bar heights. Print the area of the largest rectangle that can be formed from consecutive bars.",
       [("6\n2 1 5 6 2 3\n", "10"), ("2\n2 4\n", "4"), ("0\n\n", "0")],
'''    n = int(sys.stdin.readline())
    heights = list(map(int, sys.stdin.readline().split())) if n else []
    stack = []
    best = 0
    for i, height in enumerate(heights + [0]):
        while stack and heights[stack[-1]] > height:
            top = stack.pop()
            left = stack[-1] + 1 if stack else 0
            best = max(best, heights[top] * (i - left))
        stack.append(i)
    print(best)''', "O(n) time, O(n) space"),
      ("hard-006", "Longest Increasing Subsequence", ["dynamic-programming", "binary-search"],
       "Read n and n integers. Print the length of a strictly increasing subsequence; elements need not be adjacent.",
       [("8\n10 9 2 5 3 7 101 18\n", "4"), ("4\n4 3 2 1\n", "1"), ("0\n\n", "0")],
'''    from bisect import bisect_left
    n = int(sys.stdin.readline())
    values = list(map(int, sys.stdin.readline().split())) if n else []
    tails = []
    for value in values:
        place = bisect_left(tails, value)
        if place == len(tails): tails.append(value)
        else: tails[place] = value
    print(len(tails))''', "O(n log n) time, O(n) space"),
      ("hard-007", "Count Island Components", ["graphs", "depth-first-search"],
       "Read rows and columns, then a grid of `1` land and `0` water. Land cells connected up/down/left/right form one island. Print the island count.",
       [("3 4\n1100\n1001\n0011\n", "2"), ("2 2\n00\n00\n", "0"), ("1 3\n111\n", "1")],
'''    rows, cols = map(int, sys.stdin.readline().split())
    grid = [list(sys.stdin.readline().strip()) for _ in range(rows)]
    islands = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != '1': continue
            islands += 1
            stack = [(r, c)]
            grid[r][c] = '0'
            while stack:
                x, y = stack.pop()
                for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == '1':
                        grid[nx][ny] = '0'; stack.append((nx, ny))
    print(islands)''', "O(rows × cols) time and space"),
      ("hard-008", "Trapped Rainwater", ["arrays", "two-pointers"],
       "Read n and n non-negative heights. Print how many unit squares of water are trapped after rain.",
       [("12\n0 1 0 2 1 0 1 3 2 1 2 1\n", "6"), ("3\n1 2 3\n", "0"), ("4\n3 0 0 3\n", "6")],
'''    n = int(sys.stdin.readline())
    heights = list(map(int, sys.stdin.readline().split())) if n else []
    left, right = 0, n - 1
    left_high = right_high = water = 0
    while left < right:
        if heights[left] <= heights[right]:
            left_high = max(left_high, heights[left])
            water += left_high - heights[left]
            left += 1
        else:
            right_high = max(right_high, heights[right])
            water += right_high - heights[right]
            right -= 1
    print(water)''', "O(n) time, O(1) space"),
    ]
    out=[]
    for key,title,topics,desc,cases,body,complexity in raw:
        solution="import sys\n\n\ndef solve() -> None:\n" + body + "\n\n\nif __name__ == \"__main__\":\n    solve()\n"
        out.append(_exercise(key=key,title=title,difficulty="Hard",topics=topics,description=desc,
           constraints=["Dimensions and counts can be up to 200,000 where applicable", "Use an algorithm appropriate for the stated complexity"],cases=cases,solution=solution,
           hints=["State the subproblem or traversal invariant out loud.", "Choose a data structure that makes the repeated operation cheap.", "Verify the smallest and disconnected cases."],complexity=complexity,frequency="Very common"))
    return out


def _advanced_bank() -> list[dict]:
    """Interview-pattern drills with deliberately different input contracts."""
    rows = [
      ("advanced-001", "Longest Unique Window", "Medium", ["sliding-window", "strings", "hashing"],
       "Read one line and print the length of its longest substring with no repeated character.",
       [("abcabcbb\n", "3"), ("bbbbb\n", "1"), ("\n", "0")],
'''    text = sys.stdin.readline().rstrip('\\n')
    last, left, best = {}, 0, 0
    for right, char in enumerate(text):
        if char in last and last[char] >= left: left = last[char] + 1
        last[char] = right; best = max(best, right - left + 1)
    print(best)''', "O(n) time, O(min(n, alphabet)) space"),
      ("advanced-002", "Smallest Covering Window", "Hard", ["sliding-window", "strings", "hashing"],
       "Read source and required characters on separate lines. Print the shortest substring of source containing every character in required with matching multiplicity, or `NONE`.",
       [("ADOBECODEBANC\nABC\n", "BANC"), ("a\naa\n", "NONE"), ("aa\naa\n", "aa")],
'''    from collections import Counter
    source = sys.stdin.readline().rstrip('\\n')
    required = sys.stdin.readline().rstrip('\\n')
    if not required: print(); return
    need = Counter(required); have = Counter(); formed = 0; left = 0; best = None
    for right, char in enumerate(source):
        have[char] += 1
        if char in need and have[char] == need[char]: formed += 1
        while formed == len(need):
            if best is None or right - left + 1 < best[0]: best = (right - left + 1, left, right)
            removed = source[left]; have[removed] -= 1
            if removed in need and have[removed] < need[removed]: formed -= 1
            left += 1
    print(source[best[1]:best[2]+1] if best else 'NONE')''', "O(n + m) time, O(alphabet) space"),
      ("advanced-003", "Reverse Serialized List", "Medium", ["linked-list", "serialization"],
       "Read a space-separated list of integers on one line. Treat it as a singly linked list, reverse it, and print the serialized values. A blank line represents an empty list.",
       [("1 2 3\n", "3 2 1"), ("7\n", "7"), ("\n", "")],
'''    values = sys.stdin.readline().split()
    previous = None
    for value in values:
        previous = (value, previous)
    answer = []
    while previous is not None:
        value, previous = previous; answer.append(value)
    print(*answer)''', "O(n) time, O(n) serialized-node space"),
      ("advanced-004", "Remove Nth List Node", "Medium", ["linked-list", "two-pointers", "serialization"],
       "Read a space-separated non-empty list, then n on the next line. Remove the nth node from the end and print the remaining serialized values. n is valid.",
       [("1 2 3 4 5\n2\n", "1 2 3 5"), ("1\n1\n", ""), ("4 5\n2\n", "5")],
'''    values = sys.stdin.readline().split()
    nth = int(sys.stdin.readline())
    del values[len(values) - nth]
    print(*values)''', "O(n) time, O(n) serialization space"),
      ("advanced-005", "Tree Level Order", "Medium", ["binary-tree", "breadth-first-search", "serialization"],
       "Read a complete positional-array tree serialization using integers and `null` (children of index i are 2i+1 and 2i+2). Print values level by level, with levels separated by ` | `. Empty tree prints an empty line.",
       [("3 9 20 null null 15 7\n", "3 | 9 20 | 15 7"), ("1\n", "1"), ("null\n", "")],
'''    from collections import deque
    values = sys.stdin.readline().split()
    if not values or values[0] == 'null': print(); return
    queue = deque([0]); levels = []
    while queue:
        level = []
        for _ in range(len(queue)):
            index = queue.popleft(); level.append(values[index])
            for child in (2 * index + 1, 2 * index + 2):
                if child < len(values) and values[child] != 'null': queue.append(child)
        levels.append(' '.join(level))
    print(' | '.join(levels))''', "O(n) time, O(n) space"),
      ("advanced-006", "Validate Binary Search Tree", "Medium", ["binary-tree", "binary-search-tree", "depth-first-search"],
       "Read a complete positional-array tree serialization with `null` (children of index i are 2i+1 and 2i+2). Print `yes` if it is a strict binary search tree, otherwise `no`.",
       [("2 1 3\n", "yes"), ("5 1 4 null null 3 6\n", "no"), ("null\n", "yes")],
'''    values = sys.stdin.readline().split()
    def valid(index, low, high):
        if index >= len(values) or values[index] == 'null': return True
        value = int(values[index])
        return low < value < high and valid(2*index+1, low, value) and valid(2*index+2, value, high)
    print('yes' if valid(0, float('-inf'), float('inf')) else 'no')''', "O(n) time, O(height) recursion space"),
      ("advanced-007", "Kth Largest Value", "Medium", ["heaps", "arrays"],
       "Read n, n integers, then k. Print the kth largest value counting duplicates.",
       [("6\n3 2 1 5 6 4\n2\n", "5"), ("3\n3 3 2\n2\n", "3"), ("1\n-1\n1\n", "-1")],
'''    import heapq
    n = int(sys.stdin.readline())
    values = list(map(int, sys.stdin.readline().split()))
    k = int(sys.stdin.readline())
    print(heapq.nlargest(k, values)[-1])''', "O(n log k) time, O(k) space"),
      ("advanced-008", "Merge K Sorted Streams", "Hard", ["heaps", "sorting"],
       "Read k. Each of the next k lines begins with its count followed by that many sorted integers. Merge all streams and print one sorted sequence.",
       [("3\n3 1 4 7\n2 2 5\n3 0 3 8\n", "0 1 2 3 4 5 7 8"), ("1\n0\n", ""), ("2\n1 -1\n1 0\n", "-1 0")],
'''    import heapq
    k = int(sys.stdin.readline())
    streams = []
    for _ in range(k):
        parts = list(map(int, sys.stdin.readline().split()))
        streams.append(parts[1:])
    heap = [(stream[0], i, 0) for i, stream in enumerate(streams) if stream]
    heapq.heapify(heap); answer = []
    while heap:
        value, stream_id, index = heapq.heappop(heap); answer.append(value)
        if index + 1 < len(streams[stream_id]): heapq.heappush(heap, (streams[stream_id][index+1], stream_id, index+1))
    print(*answer)''', "O(n log k) time, O(k) space"),
      ("advanced-009", "Non-Overlapping Meetings", "Medium", ["greedy", "intervals", "sorting"],
       "Read n, then n start/end pairs. Print the maximum number of mutually non-overlapping meetings; a meeting ending at t may be followed by one starting at t.",
       [("3\n0 30\n5 10\n15 20\n", "2"), ("3\n1 2\n2 3\n3 4\n", "3"), ("0\n", "0")],
'''    n = int(sys.stdin.readline())
    meetings = [tuple(map(int, sys.stdin.readline().split())) for _ in range(n)]
    count = 0; end = float('-inf')
    for start, finish in sorted(meetings, key=lambda pair: pair[1]):
        if start >= end: count += 1; end = finish
    print(count)''', "O(n log n) time, O(n) space"),
      ("advanced-010", "Minimum Platforms", "Hard", ["greedy", "heaps", "intervals"],
       "Read n, then n arrival/departure pairs. A platform is needed for each train present; an arrival at the exact departure time can reuse that platform. Print the minimum platforms.",
       [("3\n900 910\n940 1200\n950 1120\n", "2"), ("2\n1 2\n2 3\n", "1"), ("0\n", "0")],
'''    import heapq
    n = int(sys.stdin.readline())
    trains = sorted(tuple(map(int, sys.stdin.readline().split())) for _ in range(n))
    departures = []; best = 0
    for arrival, departure in trains:
        while departures and departures[0] <= arrival: heapq.heappop(departures)
        heapq.heappush(departures, departure); best = max(best, len(departures))
    print(best)''', "O(n log n) time, O(n) space"),
      ("advanced-011", "Dynamic Connectivity", "Hard", ["union-find", "graphs"],
       "Read n and q, then q commands: `union a b` joins vertices, and `same a b` asks whether they are connected. Print one `yes`/`no` line per query.",
       [("5 5\nunion 0 1\nsame 0 1\nsame 1 2\nunion 1 2\nsame 0 2\n", "yes\nno\nyes"), ("2 1\nsame 0 1\n", "no"), ("3 2\nunion 1 2\nsame 1 2\n", "yes")],
'''    n, q = map(int, sys.stdin.readline().split())
    parent = list(range(n)); size = [1] * n
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    answer = []
    for _ in range(q):
        command, a, b = sys.stdin.readline().split(); a = int(a); b = int(b)
        left, right = find(a), find(b)
        if command == 'union':
            if left != right:
                if size[left] < size[right]: left, right = right, left
                parent[right] = left; size[left] += size[right]
        else: answer.append('yes' if left == right else 'no')
    print('\\n'.join(answer))''', "O(q α(n)) time, O(n) space"),
      ("advanced-012", "Generate Parentheses", "Medium", ["backtracking", "strings"],
       "Read n and print every well-formed parenthesis string with n pairs in lexicographic construction order (open branch before close), one per line.",
       [("2\n", "(())\n()()"), ("1\n", "()"), ("0\n", "")],
'''    n = int(sys.stdin.readline())
    answer = []
    def build(text, opened, closed):
        if len(text) == 2 * n: answer.append(text); return
        if opened < n: build(text + '(', opened + 1, closed)
        if closed < opened: build(text + ')', opened, closed + 1)
    build('', 0, 0)
    print('\\n'.join(answer))''', "O(Cn × n) time, O(n) recursion space excluding output"),
      ("advanced-013", "Word Search Grid", "Hard", ["backtracking", "matrix", "depth-first-search"],
       "Read rows, columns, a grid of uppercase letters, then a target word. Print `yes` if the word can be traced through orthogonally adjacent cells without reusing a cell.",
       [("3 4\nABCE\nSFCS\nADEE\nABCCED\n", "yes"), ("3 4\nABCE\nSFCS\nADEE\nABCB\n", "no"), ("1 1\nA\nA\n", "yes")],
'''    rows, cols = map(int, sys.stdin.readline().split())
    grid = [list(sys.stdin.readline().strip()) for _ in range(rows)]
    word = sys.stdin.readline().strip()
    def search(r, c, index):
        if index == len(word): return True
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] != word[index]: return False
        saved = grid[r][c]; grid[r][c] = '#'
        found = any(search(r+dr, c+dc, index+1) for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)))
        grid[r][c] = saved
        return found
    print('yes' if any(search(r, c, 0) for r in range(rows) for c in range(cols)) else 'no')''', "O(rows × cols × 4^L) time, O(L) space"),
      ("advanced-014", "Prefix Directory", "Medium", ["trie", "strings"],
       "Read n words, then q prefixes. For every prefix, print the count of inserted words beginning with it.",
       [("3\napp\napple\napt\n3\nap\napp\nb\n", "3\n2\n0"), ("1\na\n1\na\n", "1"), ("0\n2\na\n\n", "0\n0")],
'''    n = int(sys.stdin.readline())
    root = {'count': 0}
    for _ in range(n):
        node = root
        root['count'] += 1
        for char in sys.stdin.readline().strip():
            node = node.setdefault(char, {'count': 0}); node['count'] += 1
    q = int(sys.stdin.readline()); answer = []
    for _ in range(q):
        node = root
        for char in sys.stdin.readline().strip():
            if char not in node: node = None; break
            node = node[char]
        answer.append(str(node['count'] if node else 0))
    print('\\n'.join(answer))''', "O(total input characters) time and space"),
      ("advanced-015", "Three Value Sum", "Medium", ["two-pointers", "arrays", "sorting"],
       "Read n, n integers, then target. Print `yes` if three distinct indices sum to target; otherwise `no`.",
       [("5\n-1 0 1 2 -1\n0\n", "yes"), ("3\n1 2 4\n10\n", "no"), ("3\n0 0 0\n0\n", "yes")],
'''    n = int(sys.stdin.readline())
    values = sorted(map(int, sys.stdin.readline().split()))
    target = int(sys.stdin.readline())
    for i in range(n - 2):
        left, right = i + 1, n - 1
        while left < right:
            total = values[i] + values[left] + values[right]
            if total == target: print('yes'); return
            if total < target: left += 1
            else: right -= 1
    print('no')''', "O(n²) time, O(n) space for sorting"),
      ("advanced-016", "Spiral Matrix", "Medium", ["matrix", "simulation"],
       "Read rows and columns followed by the matrix. Print values in clockwise spiral order.",
       [("3 3\n1 2 3\n4 5 6\n7 8 9\n", "1 2 3 6 9 8 7 4 5"), ("1 4\n1 2 3 4\n", "1 2 3 4"), ("2 1\n1\n2\n", "1 2")],
'''    rows, cols = map(int, sys.stdin.readline().split())
    matrix = [list(map(int, sys.stdin.readline().split())) for _ in range(rows)]
    top, bottom, left, right = 0, rows - 1, 0, cols - 1; answer = []
    while top <= bottom and left <= right:
        answer.extend(matrix[top][left:right+1]); top += 1
        for r in range(top, bottom + 1): answer.append(matrix[r][right])
        right -= 1
        if top <= bottom: answer.extend(reversed(matrix[bottom][left:right+1])); bottom -= 1
        if left <= right:
            for r in range(bottom, top - 1, -1): answer.append(matrix[r][left])
            left += 1
    print(*answer)''', "O(rows × cols) time, O(1) auxiliary space"),
      ("advanced-017", "Matrix Zeroes", "Medium", ["matrix", "hashing"],
       "Read rows and columns followed by an integer matrix. If any cell is zero, set its whole row and column to zero. Print the resulting rows.",
       [("3 3\n1 1 1\n1 0 1\n1 1 1\n", "1 0 1\n0 0 0\n1 0 1"), ("1 2\n0 3\n", "0 0"), ("2 2\n1 2\n3 4\n", "1 2\n3 4")],
'''    rows, cols = map(int, sys.stdin.readline().split())
    matrix = [list(map(int, sys.stdin.readline().split())) for _ in range(rows)]
    zero_rows = {r for r in range(rows) for c in range(cols) if matrix[r][c] == 0}
    zero_cols = {c for r in range(rows) for c in range(cols) if matrix[r][c] == 0}
    for r in range(rows):
        for c in range(cols):
            if r in zero_rows or c in zero_cols: matrix[r][c] = 0
    print(*(' '.join(map(str, row)) for row in matrix), sep='\\n')''', "O(rows × cols) time, O(rows + cols) space"),
      ("advanced-018", "Median of Two Sorted Arrays", "Hard", ["binary-search", "arrays"],
       "Read sizes n and m, then two sorted integer lines. Print the median; if it is a half integer, print it with `.5`.",
       [("2 1\n1 3\n2\n", "2"), ("2 2\n1 2\n3 4\n", "2.5"), ("0 1\n\n5\n", "5")],
'''    n, m = map(int, sys.stdin.readline().split())
    first_line = sys.stdin.readline().split()
    second_line = sys.stdin.readline().split()
    first = list(map(int, first_line)) if n else []
    second = list(map(int, second_line)) if m else []
    if len(first) > len(second): first, second = second, first
    total = len(first) + len(second); half = total // 2; low, high = 0, len(first)
    while True:
        cut_a = (low + high) // 2; cut_b = half - cut_a
        left_a = first[cut_a-1] if cut_a else float('-inf'); right_a = first[cut_a] if cut_a < len(first) else float('inf')
        left_b = second[cut_b-1] if cut_b else float('-inf'); right_b = second[cut_b] if cut_b < len(second) else float('inf')
        if left_a <= right_b and left_b <= right_a:
            if total % 2: answer = min(right_a, right_b)
            else: answer = (max(left_a, left_b) + min(right_a, right_b)) / 2
            print(int(answer) if answer == int(answer) else answer); return
        if left_a > right_b: high = cut_a - 1
        else: low = cut_a + 1''', "O(log min(n, m)) time, O(1) space"),
      ("advanced-019", "N Queens Count", "Hard", ["backtracking", "graphs"],
       "Read n and print the number of ways to place n queens on an n × n board so none attack each other.",
       [("4\n", "2"), ("1\n", "1"), ("3\n", "0")],
'''    n = int(sys.stdin.readline())
    columns, diagonals_a, diagonals_b = set(), set(), set()
    def place(row):
        if row == n: return 1
        total = 0
        for col in range(n):
            if col in columns or row-col in diagonals_a or row+col in diagonals_b: continue
            columns.add(col); diagonals_a.add(row-col); diagonals_b.add(row+col)
            total += place(row+1)
            columns.remove(col); diagonals_a.remove(row-col); diagonals_b.remove(row+col)
        return total
    print(place(0))''', "O(n!) time, O(n) space"),
      ("advanced-020", "Cheapest Network", "Hard", ["union-find", "graphs", "greedy"],
       "Read n and m, then weighted undirected edges `a b cost`. Print the total cost of a minimum spanning tree, or `IMPOSSIBLE` when the graph is disconnected.",
       [("4 5\n0 1 1\n1 2 2\n2 3 3\n0 3 10\n0 2 4\n", "6"), ("3 1\n0 1 5\n", "IMPOSSIBLE"), ("1 0\n", "0")],
'''    n, m = map(int, sys.stdin.readline().split())
    parent = list(range(n)); size = [1] * n
    def find(x):
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    cost = used = 0
    edges = sorted((tuple(map(int, sys.stdin.readline().split())) for _ in range(m)), key=lambda edge: edge[2])
    for a, b, weight in edges:
        a, b = find(a), find(b)
        if a == b: continue
        if size[a] < size[b]: a, b = b, a
        parent[b] = a; size[a] += size[b]; cost += weight; used += 1
    print(cost if used == n - 1 else 'IMPOSSIBLE')''', "O(m log m) time, O(n) space"),
    ]
    items=[]
    for key,title,difficulty,topics,description,cases,body,complexity in rows:
        solution="import sys\n\n\ndef solve() -> None:\n" + body + "\n\n\nif __name__ == \"__main__\":\n    solve()\n"
        items.append(_exercise(key=key,title=title,difficulty=difficulty,topics=topics,description=description,
            constraints=["Use the stated input format exactly", "Input sizes are chosen to require the target pattern"],cases=cases,solution=solution,
            hints=["Restate the invariant before writing the loop.", "Choose data structures that make the repeated operation cheap.", "Check empty, singleton, and duplicate boundaries."],complexity=complexity,frequency="Very common"))
    return items


EXERCISES: dict[str, dict] = {}
for _item in (_single_int_bank() + _array_bank() + _string_bank() + _parametric_bank() + _generated_drills() + _scalar_drills() + _hard_bank() + _advanced_bank()):
    if _item["id"] in EXERCISES:
        raise RuntimeError(f"duplicate exercise id: {_item['id']}")
    EXERCISES[_item["id"]] = _item

# Two operation-driven problems have deliberately non-array input shapes.  Keep
# their canonical scripts explicit rather than forcing them through the common
# n-and-list template used by most catalogue entries.
EXERCISES["valid-parentheses"]["solution"] = '''import sys


def solve() -> None:
    pairs = {')': '(', ']': '[', '}': '{'}
    stack = []
    for ch in sys.stdin.readline().strip():
        if ch in '([{':
            stack.append(ch)
        elif not stack or stack.pop() != pairs[ch]:
            print('no')
            return
    print('yes' if not stack else 'no')


if __name__ == "__main__":
    solve()
'''
EXERCISES["min-stack-operations"]["solution"] = '''import sys


def solve() -> None:
    lines = sys.stdin.read().splitlines()
    stack, minimums, result = [], [], []
    for line in lines[1:]:
        parts = line.split()
        if not parts:
            continue
        if parts[0] == 'push':
            value = int(parts[1])
            stack.append(value)
            minimums.append(value if not minimums else min(value, minimums[-1]))
        elif parts[0] == 'pop':
            stack.pop()
            minimums.pop()
        else:
            result.append(str(minimums[-1]))
    print('\\n'.join(result))


if __name__ == "__main__":
    solve()
'''

# The advanced set has deeper hidden coverage so it remains useful for practice
# rather than rewarding a solution tailored to the two displayed examples.
_ADVANCED_EXTRA_HIDDEN: dict[str, list[tuple[str, str]]] = {
    "advanced-001": [("pwwkew\n", "3"), ("abba\n", "2")],
    "advanced-002": [("aaflslflsldkalskaaa\naaa\n", "aaa"), ("abc\n\n", "")],
    "advanced-003": [("-1 0 1\n", "1 0 -1"), ("8 8\n", "8 8")],
    "advanced-004": [("1 2\n1\n", "1"), ("9 8 7\n3\n", "8 7")],
    "advanced-005": [("1 null 2 null null 3\n", "1 | 2 | 3"), ("1 2 3 4 5 null 7\n", "1 | 2 3 | 4 5 7")],
    "advanced-006": [("2 2 2\n", "no"), ("10 5 15 null null 12 20\n", "yes")],
    "advanced-007": [("5\n5 1 5 2 4\n3\n", "4"), ("4\n-5 -2 -3 -1\n4\n", "-5")],
    "advanced-008": [("2\n2 1 1\n2 1 1\n", "1 1 1 1"), ("3\n1 2\n0\n1 1\n", "1 2")],
    "advanced-009": [("4\n1 4\n2 3\n3 5\n5 6\n", "3"), ("1\n-2 -1\n", "1")],
    "advanced-010": [("3\n1 10\n2 3\n4 5\n", "2"), ("3\n1 4\n1 4\n1 4\n", "3")],
    "advanced-011": [("4 4\nunion 0 1\nunion 2 3\nsame 0 3\nsame 2 3\n", "no\nyes"), ("1 1\nsame 0 0\n", "yes")],
    "advanced-012": [("3\n", "((()))\n(()())\n(())()\n()(())\n()()()"), ("0\n", "")],
    "advanced-013": [("2 2\nAB\nCD\nACDB\n", "yes"), ("1 3\nAAA\nAAAA\n", "no")],
    "advanced-014": [("4\nto\ntop\ntoy\ntea\n3\nt\nto\ntea\n", "4\n3\n1"), ("2\na\nab\n2\nabc\nz\n", "0\n0")],
    "advanced-015": [("4\n1 1 1 1\n3\n", "yes"), ("2\n1 2\n3\n", "no")],
    "advanced-016": [("2 3\n1 2 3\n4 5 6\n", "1 2 3 6 5 4"), ("1 1\n9\n", "9")],
    "advanced-017": [("2 3\n0 1 2\n3 4 5\n", "0 0 0\n0 4 5"), ("2 2\n0 1\n2 3\n", "0 0\n0 3")],
    "advanced-018": [("1 1\n-2\n-1\n", "-1.5"), ("3 2\n1 2 6\n3 4\n", "3")],
    "advanced-019": [("0\n", "1"), ("5\n", "10")],
    "advanced-020": [("3 3\n0 1 10\n1 2 1\n0 2 2\n", "3"), ("2 1\n0 1 -4\n", "-4")],
}
for _advanced_id, _cases in _ADVANCED_EXTRA_HIDDEN.items():
    EXERCISES[_advanced_id]["hidden_tests"].extend(
        {"input": _input, "expected_output": _output} for _input, _output in _cases
    )


def _add_input_framing_coverage() -> None:
    """Give every drill a minimum hidden-test depth without dynamic oracles.

    Full-script exercises frequently fail in interviews because a solution only
    reads a convenient first line or makes brittle EOF assumptions.  These
    deterministic hidden variants retain the same semantic payload while
    varying harmless trailing blank-record framing.  Unlike executing stored
    solutions during import, their expected output is an already-authored,
    auditable oracle.  Medium and Hard drills receive a fourth hidden framing
    check in addition to their algorithm-specific cases.
    """
    for exercise in EXERCISES.values():
        existing_inputs = {case["input"] for case in exercise["public_tests"] + exercise["hidden_tests"]}
        target = 4 if exercise["difficulty"] in {"Medium", "Hard"} else 3
        source_cases = exercise["hidden_tests"] + exercise["public_tests"]
        source_index = 0
        framing_depth = 1
        while len(exercise["hidden_tests"]) < target:
            source = source_cases[source_index % len(source_cases)]
            candidate = source["input"] + ("\n" * framing_depth)
            while candidate in existing_inputs:
                framing_depth += 1
                candidate = source["input"] + ("\n" * framing_depth)
            exercise["hidden_tests"].append({"input": candidate, "expected_output": source["expected_output"]})
            existing_inputs.add(candidate)
            source_index += 1
            framing_depth += 1


_add_input_framing_coverage()

# Keep user-visible complexity notation portable across terminals and web fonts.
for _exercise_record in EXERCISES.values():
    _exercise_record["expected_complexity"] = (_exercise_record["expected_complexity"]
        .replace("×", "*").replace("²", "^2").replace("α", "alpha"))

# The exponential backtracking exercises need practical bounds, not a generic
# large-input boilerplate constraint.
EXERCISES["advanced-013"]["constraints"] = ["1 <= rows, cols <= 6", "1 <= word length <= 15"]
EXERCISES["advanced-019"]["constraints"] = ["0 <= n <= 11", "Count fits in a Python integer"]
for _hard_id in ("hard-001", "hard-007"):
    EXERCISES[_hard_id]["constraints"] = ["1 <= rows, cols <= 500", "Grid input contains only the documented symbols"]
EXERCISES["hard-002"]["constraints"] = ["1 <= m <= 100", "0 <= target <= 20,000"]
EXERCISES["hard-003"]["constraints"] = ["0 <= word lengths <= 2,000", "Words are ASCII text"]
EXERCISES["hard-004"]["constraints"] = ["0 <= n, m <= 200,000", "Vertices are numbered 0 through n-1"]
EXERCISES["hard-005"]["constraints"] = ["0 <= n <= 200,000", "Heights are non-negative integers"]
EXERCISES["hard-006"]["constraints"] = ["0 <= n <= 200,000", "Values fit in signed 32-bit integers"]
EXERCISES["hard-008"]["constraints"] = ["0 <= n <= 200,000", "Heights are non-negative integers"]
EXERCISES["valid-parentheses"]["constraints"] = ["0 <= input length <= 200,000", "Input contains only (), [], and {} brackets"]
EXERCISES["min-stack-operations"]["constraints"] = ["0 <= q <= 200,000", "Every pop/min operation is valid at the time it appears"]
EXERCISES["range-sum-query"]["constraints"] = ["1 <= n <= 200,000", "0 <= l <= r < n"]
EXERCISES["merge-intervals"]["constraints"] = ["0 <= n <= 200,000", "Each interval satisfies start <= end"]

# Correct the two generated drills whose original sample selector happened to
# choose the same list repeatedly.  These are different semantic boundaries,
# not merely alternate whitespace around the same input.
EXERCISES["drill-017"]["public_tests"] = [
    {"input": "3\n1 4 9\n", "expected_output": "4"},
    {"input": "5\n-5 -1 0 3 8\n", "expected_output": "0"},
]
EXERCISES["drill-017"]["hidden_tests"] = [
    {"input": "1\n42\n", "expected_output": "42"},
    {"input": "3\n-8 -2 -1\n", "expected_output": "-2"},
    {"input": "5\n1 1 1 1 1\n", "expected_output": "1"},
    {"input": "7\n-9 -3 0 2 4 8 10\n", "expected_output": "2"},
]
EXERCISES["drill-018"]["public_tests"] = [
    {"input": "4\n1 5 2 4\n", "expected_output": "3"},
    {"input": "4\n8 1 9 2\n", "expected_output": "3"},
]
EXERCISES["drill-018"]["hidden_tests"] = [
    {"input": "2\n7 7\n", "expected_output": "7"},
    {"input": "6\n-5 4 2 -3 8 1\n", "expected_output": "-4"},
    {"input": "4\n0 0 0 0\n", "expected_output": "0"},
    {"input": "8\n1 8 2 7 3 6 4 5\n", "expected_output": "10"},
]
EXERCISES["advanced-012"]["hidden_tests"] = [
    {"input": "0\n", "expected_output": ""},
    {"input": "3\n", "expected_output": "((()))\n(()())\n(())()\n()(())\n()()()"},
    {"input": "4\n", "expected_output": "(((())))\n((()()))\n((())())\n((()))()\n(()(()))\n(()()())\n(()())()\n(())(())\n(())()()\n()((()))\n()(()())\n()(())()\n()()(())\n()()()()"},
    {"input": "1\n\n", "expected_output": "()"},
]
_FUNDAMENTAL_COMPLEXITIES = {
    "fundamental-011": "O(1) time, O(1) space",
    "fundamental-016": "O(d) time, O(d) digit space",
    "fundamental-019": "O(1) time, O(1) space",
    "fundamental-021": "O(n) time, O(1) space",
    "fundamental-023": "O(1) time, O(1) space",
    "fundamental-027": "O(sqrt(n)) time, O(1) space",
    "fundamental-028": "O(sqrt(n)) time, O(1) space",
    "fundamental-037": "O(log(100/n)) time, O(1) space",
    "fundamental-040": "O(log_7(|n|)) time, O(1) space",
    "fundamental-041": "O(n) time, O(n) result space",
}
for _fundamental_id, _complexity in _FUNDAMENTAL_COMPLEXITIES.items():
    EXERCISES[_fundamental_id]["expected_complexity"] = _complexity
_ADVANCED_CONSTRAINTS = {
    "advanced-001": ["0 <= text length <= 200,000", "Input uses printable ASCII characters"],
    "advanced-002": ["0 <= source length <= 200,000", "1 <= required length <= 200,000"],
    "advanced-003": ["0 <= list length <= 200,000", "Values fit in signed 32-bit integers"],
    "advanced-004": ["1 <= list length <= 200,000", "1 <= n <= list length"],
    "advanced-005": ["0 <= serialized slots <= 200,000", "Use complete positional-array null placeholders"],
    "advanced-006": ["0 <= serialized slots <= 200,000", "Node values fit in signed 32-bit integers"],
    "advanced-007": ["1 <= n <= 200,000", "1 <= k <= n"],
    "advanced-008": ["0 <= k <= 20,000", "Total stream values <= 200,000"],
    "advanced-009": ["0 <= n <= 200,000", "Each meeting has start <= end"],
    "advanced-010": ["0 <= n <= 200,000", "Each train has arrival <= departure"],
    "advanced-011": ["1 <= n, q <= 200,000", "Vertices are numbered 0 through n-1"],
    "advanced-012": ["0 <= n <= 8", "Output order is open branch before close branch"],
    "advanced-014": ["0 <= word and prefix lengths <= 100", "n + q <= 200,000"],
    "advanced-015": ["0 <= n <= 5,000", "Values fit in signed 32-bit integers"],
    "advanced-016": ["1 <= rows * columns <= 200,000", "Matrix values fit in signed 32-bit integers"],
    "advanced-017": ["1 <= rows * columns <= 200,000", "Matrix values fit in signed 32-bit integers"],
    "advanced-018": ["1 <= n + m <= 200,000", "Both input arrays are sorted nondecreasing"],
    "advanced-020": ["1 <= n <= 200,000", "0 <= m <= 300,000; vertices are 0 through n-1"],
}
for _advanced_id, _constraints in _ADVANCED_CONSTRAINTS.items():
    EXERCISES[_advanced_id]["constraints"] = _constraints

# Python is explicit too, allowing callers to filter a single uniform
# catalogue without relying on an implicit fallback.  The separate module keeps
# Java/SQL content auditable and avoids making this already substantial file
# harder to maintain.
for _python_exercise in EXERCISES.values():
    _python_exercise.setdefault("language", "python")

from backend.multilang_bank import MULTILANG_EXERCISES
from backend.java_interview_bank import JAVA_INTERVIEW_EXERCISES
from backend.python_curated_141_160 import PYTHON_CURATED_141_160
from backend.python_curated_161_180 import PYTHON_CURATED_161_180
from backend.python_curated_181_200 import PYTHON_CURATED_181_200
from backend.java_curriculum_part1 import JAVA_CURRICULUM_PART1
from backend.java_curriculum_part2 import JAVA_CURRICULUM_PART2
from backend.java_curriculum_part3 import JAVA_CURRICULUM_PART3
from backend.java_curriculum_part4 import JAVA_CURRICULUM_PART4
from backend.java_curriculum_part5 import JAVA_CURRICULUM_PART5
from backend.sql_curriculum_part1 import SQL_CURRICULUM_PART1
from backend.sql_curriculum_part2 import SQL_CURRICULUM_PART2

for _multilang_exercise in MULTILANG_EXERCISES:
    if _multilang_exercise["id"] in EXERCISES:
        raise RuntimeError(f"duplicate exercise id: {_multilang_exercise['id']}")
    EXERCISES[_multilang_exercise["id"]] = _multilang_exercise

for _java_interview_exercise in JAVA_INTERVIEW_EXERCISES:
    if _java_interview_exercise["id"] in EXERCISES:
        raise RuntimeError(f"duplicate exercise id: {_java_interview_exercise['id']}")
    EXERCISES[_java_interview_exercise["id"]] = _java_interview_exercise

for _curated_exercise in (
    *PYTHON_CURATED_141_160,
    *PYTHON_CURATED_161_180,
    *PYTHON_CURATED_181_200,
    *JAVA_CURRICULUM_PART1,
    *JAVA_CURRICULUM_PART2,
    *JAVA_CURRICULUM_PART3,
    *JAVA_CURRICULUM_PART4,
    *JAVA_CURRICULUM_PART5,
    *SQL_CURRICULUM_PART1,
    *SQL_CURRICULUM_PART2,
):
    if _curated_exercise["id"] in EXERCISES:
        raise RuntimeError(f"duplicate exercise id: {_curated_exercise['id']}")
    EXERCISES[_curated_exercise["id"]] = _curated_exercise


def _public_view(exercise: dict, include_hidden: bool = False) -> dict:
    # SQL fixtures are test data just like private cases.  They must never
    # appear in the exercise-detail response, or the answer can be tailored to
    # a fixed dataset rather than written as a general query.
    data = {key: value for key, value in exercise.items() if key not in {"hidden_tests", "sql_setup", "setup_sql"}}
    if "public_tests" in data:
        data["public_tests"] = [
            {key: value for key, value in test.items() if key not in {"setup_sql", "sql_setup"}}
            for test in data["public_tests"]
        ]
    if include_hidden:
        data["hidden_tests"] = exercise["hidden_tests"]
    return data


def get_catalog() -> list[dict]:
    """Return lightweight metadata, deliberately excluding all test input."""
    return [{key: item[key] for key in ("id", "title", "language", "difficulty", "topics", "interview_frequency", "expected_complexity")}
            for item in EXERCISES.values()]


def get_exercise(exercise_id: str) -> dict | None:
    exercise = EXERCISES.get(exercise_id)
    return _public_view(exercise) if exercise else None


def validate_submission(exercise_id: str, code: str, timeout_seconds: float = 2.0) -> dict:
    """Run public and hidden cases, returning safe result metadata for the UI.

    This is a convenience runner for a trusted local learner, not a hardened
    multi-tenant sandbox. The server should impose its own process/container
    limits before exposing it beyond localhost.
    """
    exercise = EXERCISES.get(exercise_id)
    if not exercise:
        return {"status": "not_found", "message": "Unknown exercise id.", "passed": 0, "total": 0, "results": []}
    if not isinstance(code, str) or not code.strip():
        return {"status": "invalid", "message": "Submit a non-empty Python script.", "passed": 0, "total": 0, "results": []}
    tests = [("public", item) for item in exercise["public_tests"]] + [("hidden", item) for item in exercise["hidden_tests"]]
    results=[]
    started=time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="python-interview-") as directory:
        program=Path(directory) / "solution.py"
        program.write_text(code, encoding="utf-8")
        for number,(visibility,test) in enumerate(tests,1):
            try:
                safe_environment = {
                    name: os.environ[name]
                    for name in ("SYSTEMROOT", "WINDIR", "COMSPEC", "PATH", "PATHEXT", "TEMP", "TMP")
                    if name in os.environ
                }
                safe_environment.update({"PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0"})
                submission = _SubmissionProcess([sys.executable, "-I", str(program)], stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=directory, env=safe_environment)
                try:
                    stdout, stderr, return_code, output_truncated, timed_out = _run_capped(submission, test["input"], timeout_seconds)
                    if timed_out:
                        results.append({"number":number,"visibility":visibility,"passed":False,
                            "input":test["input"] if visibility == "public" else None,
                            "error":f"Timed out after {timeout_seconds:g} seconds."})
                        continue
                    if output_truncated:
                        results.append({"number":number,"visibility":visibility,"passed":False,
                            "input":test["input"] if visibility == "public" else None,
                            "error":f"Output exceeded the {_CAPTURE_LIMIT_BYTES // 1024} KiB safety limit."})
                        continue
                except subprocess.TimeoutExpired:
                    results.append({"number":number,"visibility":visibility,"passed":False,
                        "input":test["input"] if visibility == "public" else None,
                        "error":f"Timed out after {timeout_seconds:g} seconds."})
                    continue
                finally:
                    # On Windows this closes KILL_ON_JOB_CLOSE, taking any
                    # surviving descendants with it even after a normal exit.
                    submission.close()
                actual=_norm(stdout)
                expected=_norm(test["expected_output"])
                passed=return_code == 0 and actual == expected
                result={"number":number,"visibility":visibility,"passed":passed,"input":test["input"] if visibility == "public" else None}
                if visibility == "public":
                    result.update({"expected_output":test["expected_output"],"actual_output":stdout})
                if return_code:
                    result["error"] = ((stderr or "Program exited with an error.")[-2000:]
                        if visibility == "public" else "Program exited with an error on a private test.")
                results.append(result)
            except Exception as exc:
                results.append({"number": number, "visibility": visibility, "passed": False,
                    "input": test["input"] if visibility == "public" else None,
                    "error": (f"Runner error: {type(exc).__name__}: {exc}" if visibility == "public"
                              else "Private test could not be completed.")})
    passed=sum(result["passed"] for result in results)
    return {"status":"passed" if passed == len(results) else "failed", "passed":passed, "total":len(results),
        "duration_ms":round((time.perf_counter()-started)*1000,1), "results":results,
        "message":"All checks passed." if passed == len(results) else "Some checks did not pass."}


def catalog_summary() -> dict:
    """Useful for health endpoints and tests."""
    counts={level:0 for level in ("Easy","Medium","Hard")}
    for exercise in EXERCISES.values(): counts[exercise["difficulty"]]=counts.get(exercise["difficulty"],0)+1
    return {"total":len(EXERCISES), "by_difficulty":counts, "topics":sorted({topic for item in EXERCISES.values() for topic in item["topics"]})}
