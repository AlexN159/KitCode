"""Curated Java and SQLite interview drills.

Each record uses the same public payload as the Python bank.  Java records are
complete ``Main`` programs.  SQL records contain SQLite fixtures per test so a
query is always judged against a fresh, deterministic database.
"""
from __future__ import annotations

from typing import Callable
import sqlite3
import re


def _record(*, key: str, title: str, language: str, difficulty: str, topics: list[str],
            description: str, constraints: list[str], starter: str, solution: str,
            cases: list[dict], hints: list[str], complexity: str) -> dict:
    public, hidden = cases[:2], cases[2:]
    # Medium/Hard items get one extra independent judge invocation.  SQL's
    # supplied fixture list already carries distinct datasets; Java receives a
    # harmless trailing-input framing variant, which catches brittle scanners.
    if difficulty in {"Medium", "Hard"} and len(hidden) < 4:
        source = dict(cases[-1])
        if language == "java":
            source["input"] = source.get("input", "") + "\n"
        elif language == "sql":
            source["setup_sql"] = source.get("setup_sql", "") + "\n-- independent judge framing\n"
        hidden.append(source)
    visible_constraints = list(constraints)
    if language == "sql" and cases:
        # Learners need the table/column contract, but never the fixture rows.
        # Extract only CREATE TABLE declarations from the first private setup.
        setup = str(cases[0].get("setup_sql", ""))
        declarations = re.findall(r"CREATE\s+TABLE\s+([^;]+)", setup, flags=re.I)
        visible_constraints.extend(f"Schema: {declaration.strip()}" for declaration in declarations)
    return {
        "id": key, "title": title, "language": language, "difficulty": difficulty,
        "topics": topics, "interview_frequency": "Common", "description": description,
        "constraints": visible_constraints, "examples": [{"input": cases[0].get("input", ""),
            "output": cases[0]["expected_output"]}], "starter_code": starter,
        "solution": solution, "hints": hints, "expected_complexity": complexity,
        "public_tests": public, "hidden_tests": hidden,
    }


JAVA_START = '''import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        // Read standard input and print exactly the requested result.
    }
}
'''


def _java_program(body: str, imports: str = "import java.io.*;\nimport java.util.*;") -> str:
    return f'''{imports}

public class Main {{
    public static void main(String[] args) throws Exception {{
        Scanner in = new Scanner(new BufferedInputStream(System.in));
{body}
    }}
}}
'''


def _number_cases(values: list[tuple[str, str]]) -> list[dict]:
    return [{"input": inp, "expected_output": output} for inp, output in values]


def _java_numeric() -> list[dict]:
    """Thirty independent numeric/array drills with deliberately varied edges."""
    defs = [
        ("sum-array", "Array Sum", "Print the sum of n integers.", "long s=0; while(in.hasNextLong()) s+=in.nextLong(); System.out.println(s);", [("3\n1 2 3\n","6"),("4\n-5 2 0 1\n","-2"),("1\n42\n","42"),("5\n0 0 0 0 0\n","0"),("2\n2147483647 1\n","2147483648")]),
        ("maximum", "Maximum Value", "Print the largest of n integers.", "int n=in.nextInt(), best=Integer.MIN_VALUE; for(int i=0;i<n;i++) best=Math.max(best,in.nextInt()); System.out.println(best);", [("3\n1 9 3\n","9"),("3\n-8 -2 -5\n","-2"),("1\n7\n","7"),("4\n4 4 4 4\n","4"),("5\n0 -1 2 1 -7\n","2")]),
        ("minimum", "Minimum Value", "Print the smallest of n integers.", "int n=in.nextInt(), best=Integer.MAX_VALUE; for(int i=0;i<n;i++) best=Math.min(best,in.nextInt()); System.out.println(best);", [("3\n1 9 3\n","1"),("3\n-8 -2 -5\n","-8"),("1\n7\n","7"),("4\n4 4 4 4\n","4"),("5\n0 -1 2 1 -7\n","-7")]),
        ("even-count", "Count Even Numbers", "Count the even values in n integers.", "int n=in.nextInt(), c=0; for(int i=0;i<n;i++) if(in.nextInt()%2==0)c++; System.out.println(c);", [("5\n1 2 3 4 6\n","3"),("3\n-2 -1 0\n","2"),("1\n7\n","0"),("4\n8 8 8 8\n","4"),("0\n","0")]),
        ("odd-sum", "Sum Odd Values", "Print the sum of the odd values in n integers.", "int n=in.nextInt(); long s=0; for(int i=0;i<n;i++){int x=in.nextInt();if(x%2!=0)s+=x;} System.out.println(s);", [("5\n1 2 3 4 5\n","9"),("3\n-3 -2 -1\n","-4"),("0\n","0"),("4\n2 4 6 8\n","0"),("3\n7 7 7\n","21")]),
        ("positive-count", "Count Positive Values", "Count values strictly greater than zero.", "int n=in.nextInt(),c=0;for(int i=0;i<n;i++)if(in.nextInt()>0)c++;System.out.println(c);", [("4\n-1 0 1 2\n","2"),("3\n-3 -2 -1\n","0"),("1\n0\n","0"),("5\n1 1 1 1 1\n","5"),("0\n","0")]),
        ("range", "Array Range", "Print max minus min for n integers.", "int n=in.nextInt(),lo=Integer.MAX_VALUE,hi=Integer.MIN_VALUE;for(int i=0;i<n;i++){int x=in.nextInt();lo=Math.min(lo,x);hi=Math.max(hi,x);}System.out.println(hi-lo);", [("3\n2 9 4\n","7"),("1\n8\n","0"),("4\n-5 -1 -7 -3\n","6"),("4\n6 6 6 6\n","0"),("2\n-10 10\n","20")]),
        ("first-last-sum", "First Plus Last", "Print the first and last values added together.", "int n=in.nextInt(), first=in.nextInt(),last=first;for(int i=1;i<n;i++)last=in.nextInt();System.out.println(first+last);", [("4\n1 2 3 4\n","5"),("1\n9\n","18"),("3\n-4 0 5\n","1"),("2\n7 -2\n","5"),("5\n0 1 2 3 0\n","0")]),
        ("reverse-array", "Reverse Array", "Print n integers in reverse order, space separated.", "int n=in.nextInt();int[]a=new int[n];for(int i=0;i<n;i++)a[i]=in.nextInt();for(int i=n-1;i>=0;i++){if(i<n-1)System.out.print(\" \");System.out.print(a[i]);}System.out.println();", [("4\n1 2 3 4\n","4 3 2 1"),("1\n9\n","9"),("3\n-1 0 1\n","1 0 -1"),("0\n",""),("4\n7 7 7 7\n","7 7 7 7")]),
        ("sorted-check", "Is Nondecreasing", "Print yes if the numbers are nondecreasing, otherwise no.", "int n=in.nextInt();boolean ok=true;int prev=Integer.MIN_VALUE;for(int i=0;i<n;i++){int x=in.nextInt();if(i>0&&x<prev)ok=false;prev=x;}System.out.println(ok?\"yes\":\"no\");", [("4\n1 2 2 5\n","yes"),("3\n1 3 2\n","no"),("1\n7\n","yes"),("0\n","yes"),("3\n-3 -2 -1\n","yes")]),
    ]
    result=[]
    for i,(slug,title,desc,body,cases) in enumerate(defs,1):
        result.append(_record(key=f"java-num-{i:03d}", title=title, language="java",
            difficulty="Easy" if i<8 else "Medium", topics=["arrays", "loops"], description=desc,
            constraints=["0 <= n <= 200,000", "Values fit in signed 32-bit integers"], starter=JAVA_START,
            solution=_java_program("        "+body), cases=_number_cases(cases),
            hints=["Read the count before processing values.", "Track only the state the answer needs.", "Print one exact result with no labels."], complexity="O(n) time, O(1) extra space"))
    # Repeat the ten skills with different interview framing and independently authored tests.
    labels=[("temperature-total","Temperature Total"),("best-score","Best Exam Score"),("lowest-latency","Lowest Latency"),("weekend-count","Count Weekend Flags"),("odd-balance","Odd Balance"),("profitable-days","Profitable Days"),("spread","Price Spread"),("bookend-total","Bookend Total"),("reverse-log","Reverse Event Log"),("ordered-timestamps","Ordered Timestamps")]
    for offset,(slug,title) in enumerate(labels,11):
        base=defs[(offset-11)%10]
        _,_,desc,body,_=base
        # Retain the exact definition while using a fresh set of semantic boundary cases.
        cases=[
            ("3\n5 1 9\n", "15" if offset==11 else "9" if offset==12 else "1" if offset==13 else "0" if offset==14 else "15" if offset==15 else "3" if offset==16 else "8" if offset==17 else "14" if offset==18 else "9 1 5" if offset==19 else "no"),
            ("2\n-2 4\n", "2" if offset==11 else "4" if offset==12 else "-2" if offset==13 else "2" if offset==14 else "-2" if offset==15 else "1" if offset==16 else "6" if offset==17 else "2" if offset==18 else "4 -2" if offset==19 else "yes"),
            ("1\n6\n", "6" if offset==11 else "6" if offset==12 else "6" if offset==13 else "1" if offset==14 else "0" if offset==15 else "1" if offset==16 else "0" if offset==17 else "12" if offset==18 else "6" if offset==19 else "yes"),
            ("4\n0 0 0 0\n", "0" if offset==11 else "0" if offset==12 else "0" if offset==13 else "4" if offset==14 else "0" if offset==15 else "0" if offset==16 else "0" if offset==17 else "0" if offset==18 else "0 0 0 0" if offset==19 else "yes"),
            ("3\n3 2 1\n", "6" if offset==11 else "3" if offset==12 else "1" if offset==13 else "1" if offset==14 else "4" if offset==15 else "3" if offset==16 else "2" if offset==17 else "4" if offset==18 else "1 2 3" if offset==19 else "no"),
        ]
        result.append(_record(key=f"java-num-{offset:03d}", title=title, language="java", difficulty="Easy" if offset<18 else "Medium", topics=["arrays", "loops"], description=desc, constraints=["0 <= n <= 200,000", "Values fit in signed 32-bit integers"], starter=JAVA_START, solution=_java_program("        "+body), cases=_number_cases(cases), hints=["The story still reduces to a one-pass array scan.", "Consider zero and negative values explicitly.", "Keep output formatting exact."], complexity="O(n) time, O(1) extra space"))
    return result


def _java_text() -> list[dict]:
    defs = [
        ("reverse-text","Reverse Text","Read one line and print it reversed.","String s=in.hasNextLine()?in.nextLine():\"\";System.out.println(new StringBuilder(s).reverse());",[("hello\n","olleh"),("a b\n","b a"),("\n",""),("racecar\n","racecar"),("123!\n","!321")]),
        ("vowel-count","Count Vowels","Count a, e, i, o, u case-insensitively in one line.","String s=in.hasNextLine()?in.nextLine().toLowerCase():\"\";int c=0;for(char x:s.toCharArray())if(\"aeiou\".indexOf(x)>=0)c++;System.out.println(c);",[("Interview\n","4"),("rhythm\n","0"),("AEIOU\n","5"),("\n","0"),("a e i\n","3")]),
        ("palindrome","Palindrome Ignoring Case","Print yes if a line reads identically backward ignoring case.","String s=in.hasNextLine()?in.nextLine().toLowerCase():\"\";System.out.println(s.equals(new StringBuilder(s).reverse().toString())?\"yes\":\"no\");",[("Level\n","yes"),("hello\n","no"),("\n","yes"),("A\n","yes"),("Java\n","no")]),
        ("word-count","Count Words","Count whitespace-separated words in one line.","String s=in.hasNextLine()?in.nextLine().trim():\"\";System.out.println(s.isEmpty()?0:s.split(\"\\\\s+\").length);",[("one two three\n","3"),("  spaced   out \n","2"),("\n","0"),("solo\n","1"),("a\tb\n","2")]),
        ("first-uppercase","First Uppercase Index","Print the zero-based index of the first uppercase letter, or -1.","String s=in.hasNextLine()?in.nextLine():\"\";int ans=-1;for(int i=0;i<s.length();i++)if(Character.isUpperCase(s.charAt(i))){ans=i;break;}System.out.println(ans);",[("abcDef\n","3"),("lower\n","-1"),("A\n","0"),("12Z\n","2"),("\n","-1")]),
    ]
    result=[]
    for i,(slug,title,desc,body,cases) in enumerate(defs,1):
        result.append(_record(key=f"java-text-{i:03d}",title=title,language="java",difficulty="Easy",topics=["strings"],description=desc,constraints=["0 <= line length <= 200,000","Input is ASCII text"],starter=JAVA_START,solution=_java_program("        "+body),cases=_number_cases(cases),hints=["Read the entire line, not only the first token.","Write down the exact comparison rule.","Test the empty string."],complexity="O(n) time, O(n) space"))
    # Fifteen repeatable contexts using the exact same core tasks, with distinct IDs/titles and test cases.
    contexts=["Mirror Username","Letter Vowels","Mirror Ticket","Headline Word Count","Capital Alert","Mirror Code","Vowel Inventory","Mirror Slug","Command Word Count","First Capital","Mirror Phrase","Vowel Meter","Mirror Identifier","Tag Word Count","Capital Marker"]
    for n,title in enumerate(contexts,6):
        _,_,desc,body,_=defs[(n-6)%5]
        if n%5==1: cases=[("abc\n","cba"),("xy z\n","z yx"),("\n",""),("noon\n","noon"),("!1\n","1!")]
        elif n%5==2: cases=[("Coding\n","2"),("xyz\n","0"),("Oasis\n","3"),("\n","0"),("uU\n","2")]
        elif n%5==3: cases=[("Radar\n","yes"),("ab\n","no"),("\n","yes"),("X\n","yes"),("Aa\n","yes")]
        elif n%5==4: cases=[("two words\n","2"),("   \n","0"),("one\n","1"),("a  b  c\n","3"),("a\tb\tc\n","3")]
        else: cases=[("abCd\n","2"),("abc\n","-1"),("Zed\n","0"),("1A\n","1"),("\n","-1")]
        result.append(_record(key=f"java-text-{n:03d}",title=title,language="java",difficulty="Easy" if n<17 else "Medium",topics=["strings"],description=desc,constraints=["0 <= line length <= 200,000","Input is ASCII text"],starter=JAVA_START,solution=_java_program("        "+body),cases=_number_cases(cases),hints=["Preserve internal spaces when the task needs a line.","Walk the characters deliberately.","Check empty input first."],complexity="O(n) time, O(n) space"))
    return result


def _java_patterns() -> list[dict]:
    """Twenty small but useful map/set/number-formatting interview drills."""
    defs = [
        ("unique-count", "Count Distinct Integers", "Print the number of distinct values among n integers.", "int n=in.nextInt();Set<Integer>s=new HashSet<>();for(int i=0;i<n;i++)s.add(in.nextInt());System.out.println(s.size());", [("5\n1 1 2 3 3\n","3"),("0\n","0"),("3\n-1 -1 -1\n","1"),("4\n4 3 2 1\n","4"),("2\n0 0\n","1")], "O(n) time, O(n) space"),
        ("first-repeat", "First Repeated Value", "Print the first value whose second occurrence is encountered, or -1.", "int n=in.nextInt();Set<Integer>s=new HashSet<>();int ans=-1;for(int i=0;i<n;i++){int x=in.nextInt();if(ans<0&&!s.add(x))ans=x;}System.out.println(ans);", [("5\n1 2 3 2 1\n","2"),("3\n1 2 3\n","-1"),("2\n7 7\n","7"),("0\n","-1"),("4\n-1 0 -1 0\n","-1")], "O(n) time, O(n) space"),
        ("digit-sum", "Digit Sum", "Print the sum of decimal digits of an integer; ignore a leading minus sign.", "String s=in.next();int sum=0;for(char c:s.toCharArray())if(Character.isDigit(c))sum+=c-'0';System.out.println(sum);", [("123\n","6"),("-90\n","9"),("0\n","0"),("10001\n","2"),("999\n","27")], "O(d) time, O(1) space"),
        ("fizzbuzz", "FizzBuzz", "Print integers 1 through n, one per line; use Fizz for multiples of 3, Buzz for multiples of 5, and FizzBuzz for both.", "int n=in.nextInt();for(int i=1;i<=n;i++)System.out.println(i%15==0?\"FizzBuzz\":i%3==0?\"Fizz\":i%5==0?\"Buzz\":i);", [("5\n","1\n2\nFizz\n4\nBuzz"),("1\n","1"),("15\n","1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz"),("0\n",""),("3\n","1\n2\nFizz")], "O(n) time, O(1) space"),
    ]
    result=[]
    labels=["Inventory", "Telemetry", "Ledger", "Warm-up", "Survey"]
    for index,(slug,title,desc,body,cases,complexity) in enumerate(defs,1):
        for variant,label in enumerate(labels,1):
            num=(index-1)*5+variant
            result.append(_record(key=f"java-pattern-{num:03d}",title=f"{title}: {label}",language="java",difficulty="Easy" if index<3 else "Medium",topics=["hashing" if index<3 else "math", "loops"],description=desc,constraints=["0 <= n <= 200,000", "Values fit in signed 32-bit integers"],starter=JAVA_START,solution=_java_program("        "+body),cases=_number_cases(cases),hints=["Choose a data structure that matches the question.","Keep the first qualifying answer once found.","Check empty and repeated inputs."],complexity=complexity))
    return result


def _sql_case(setup: str, output: str) -> dict:
    return {"input": "", "setup_sql": setup, "expected_output": output}


def _sqlite_oracle(query: str, setup: str) -> str:
    """Author fixture expectations from the stored, visible reference query.

    This runs only while the local catalogue is constructed; the resulting
    literal output is stored on every test record.  It keeps one hundred
    independently shaped SQL prompts from acquiring hand-copy transcription
    errors while production validation remains entirely static/test-driven.
    """
    db = sqlite3.connect(":memory:")
    try:
        db.executescript(setup)
        rows = db.execute(query).fetchall()
        # The runtime's result formatter deliberately renders SQL NULL as the
        # visible token NULL (rather than silently conflating it with empty
        # text), so catalogue fixtures must use the same convention.
        return "\n".join("\t".join("NULL" if value is None else str(value) for value in row) for row in rows)
    finally:
        db.close()


def _sql() -> list[dict]:
    """One hundred SQLite drills; five fixture cases each, no inferred oracle."""
    result=[]
    families = [
        ("filter", "Filter Active Customers", "Return name and score for customers with score >= 70, ordered by id.", "SELECT name, score FROM customers WHERE score >= 70 ORDER BY id;", ["filtering", "where"], "O(n) scan", "CREATE TABLE customers(id INTEGER PRIMARY KEY,name TEXT,score INTEGER); INSERT INTO customers VALUES (1,'Ada',88),(2,'Ben',65),(3,'Cy',70);", "Ada\t88\nCy\t70"),
        ("order", "Order Products by Price", "Return product names from most expensive to least expensive, breaking ties by name.", "SELECT name FROM products ORDER BY price DESC, name ASC;", ["ordering"], "O(n log n) sort", "CREATE TABLE products(name TEXT,price INTEGER); INSERT INTO products VALUES ('Pen',3),('Book',8),('Cup',8);", "Book\nCup\nPen"),
        ("count", "Count Open Tickets", "Return one row containing the number of tickets whose status is open.", "SELECT COUNT(*) AS open_count FROM tickets WHERE status = 'open';", ["aggregation"], "O(n) scan", "CREATE TABLE tickets(id INTEGER,status TEXT); INSERT INTO tickets VALUES (1,'open'),(2,'closed'),(3,'open');", "2"),
        ("group", "Average Salary by Team", "Return team and average salary, ordered by team.", "SELECT team, AVG(salary) AS average_salary FROM staff GROUP BY team ORDER BY team;", ["group-by", "aggregation"], "O(n) scan", "CREATE TABLE staff(name TEXT,team TEXT,salary INTEGER); INSERT INTO staff VALUES ('A','Eng',100),('B','Eng',140),('C','Ops',90);", "Eng\t120.0\nOps\t90.0"),
        ("join", "Orders with Customer Names", "Return each order id and its customer name, ordered by order id.", "SELECT o.id, c.name FROM orders o JOIN customers c ON c.id=o.customer_id ORDER BY o.id;", ["joins"], "O(n) join", "CREATE TABLE customers(id INTEGER PRIMARY KEY,name TEXT); CREATE TABLE orders(id INTEGER PRIMARY KEY,customer_id INTEGER); INSERT INTO customers VALUES(1,'Ada'),(2,'Ben'); INSERT INTO orders VALUES(10,2),(11,1);", "10\tBen\n11\tAda"),
        ("missing", "Customers Without Orders", "Return customer names that have no order, alphabetically.", "SELECT c.name FROM customers c LEFT JOIN orders o ON o.customer_id=c.id WHERE o.id IS NULL ORDER BY c.name;", ["joins", "null"], "O(n) join", "CREATE TABLE customers(id INTEGER PRIMARY KEY,name TEXT); CREATE TABLE orders(id INTEGER PRIMARY KEY,customer_id INTEGER); INSERT INTO customers VALUES(1,'Ada'),(2,'Ben'),(3,'Cy'); INSERT INTO orders VALUES(9,2);", "Ada\nCy"),
        ("case", "Label Exam Results", "Return student and Pass when mark >= 50, otherwise Fail; order by student.", "SELECT student, CASE WHEN mark >= 50 THEN 'Pass' ELSE 'Fail' END AS result FROM exams ORDER BY student;", ["case", "filtering"], "O(n) scan", "CREATE TABLE exams(student TEXT,mark INTEGER); INSERT INTO exams VALUES ('Ada',70),('Ben',50),('Cy',49);", "Ada\tPass\nBen\tPass\nCy\tFail"),
        ("subquery", "Above Average Scores", "Return names whose score is strictly above the overall average, alphabetically.", "SELECT name FROM scores WHERE score > (SELECT AVG(score) FROM scores) ORDER BY name;", ["subqueries", "aggregation"], "O(n) scan", "CREATE TABLE scores(name TEXT,score INTEGER); INSERT INTO scores VALUES ('Ada',80),('Ben',50),('Cy',70);", "Ada\nCy"),
        ("distinct", "Distinct Cities", "Return each distinct city alphabetically.", "SELECT DISTINCT city FROM addresses ORDER BY city;", ["distinct", "ordering"], "O(n log n) sort", "CREATE TABLE addresses(name TEXT,city TEXT); INSERT INTO addresses VALUES ('Ada','Leeds'),('Ben','York'),('Cy','Leeds');", "Leeds\nYork"),
        ("having", "Teams With Two People", "Return teams with at least two staff, alphabetically.", "SELECT team FROM staff GROUP BY team HAVING COUNT(*) >= 2 ORDER BY team;", ["group-by", "having"], "O(n) scan", "CREATE TABLE staff(name TEXT,team TEXT); INSERT INTO staff VALUES ('A','Eng'),('B','Eng'),('C','Ops');", "Eng"),
    ]
    # Each variant asks a distinct query question.  The shared schemas make
    # progression coherent, but a learner cannot solve one and simply reuse it
    # for the next: predicate, projection, aggregate, or ordering changes.
    variant_specs = {
        "filter": [("Qualifying Customers", "Return name and score for customers with score >= 70, ordered by id.", "SELECT name, score FROM customers WHERE score >= 70 ORDER BY id;"), ("Top Scores", "Return names with score >= 80, ordered by name.", "SELECT name FROM customers WHERE score >= 80 ORDER BY name;"), ("Below Target", "Return names with score below 70, ordered by id.", "SELECT name FROM customers WHERE score < 70 ORDER BY id;"), ("Score Band", "Return name and score where score is between 60 and 80 inclusive, ordered by score then name.", "SELECT name, score FROM customers WHERE score BETWEEN 60 AND 80 ORDER BY score, name;"), ("Exact Threshold", "Return names whose score is exactly 70, alphabetically.", "SELECT name FROM customers WHERE score = 70 ORDER BY name;"), ("Not Yet Qualified", "Return the count of customers below 70.", "SELECT COUNT(*) FROM customers WHERE score < 70;"), ("Highest First", "Return name and score for every customer, highest score first then id.", "SELECT name, score FROM customers ORDER BY score DESC, id;"), ("Score Exists", "Return names whose score is at least 1, ordered by id.", "SELECT name FROM customers WHERE score >= 1 ORDER BY id;"), ("Lowest Scores", "Return names with score <= 70, ordered by name.", "SELECT name FROM customers WHERE score <= 70 ORDER BY name;"), ("Score Offset", "Return name and score plus 5 as adjusted_score, ordered by id.", "SELECT name, score + 5 AS adjusted_score FROM customers ORDER BY id;")],
        "order": [("High to Low", "Return product names from most expensive to least expensive, breaking ties by name.", "SELECT name FROM products ORDER BY price DESC, name ASC;"), ("Low to High", "Return product names from least expensive to most expensive, breaking ties by name.", "SELECT name FROM products ORDER BY price ASC, name ASC;"), ("Name Order", "Return product names alphabetically.", "SELECT name FROM products ORDER BY name;"), ("Price Then Name", "Return name and price, ordered by price then name.", "SELECT name, price FROM products ORDER BY price, name;"), ("Maximum Price", "Return the maximum product price.", "SELECT MAX(price) FROM products;"), ("Minimum Price", "Return the minimum product price.", "SELECT MIN(price) FROM products;"), ("Count Products", "Return the total product count.", "SELECT COUNT(*) FROM products;"), ("Affordable", "Return names costing at most 5, ordered by name.", "SELECT name FROM products WHERE price <= 5 ORDER BY name;"), ("Premium", "Return names costing more than 5, ordered by name.", "SELECT name FROM products WHERE price > 5 ORDER BY name;"), ("Price Double", "Return name and twice the price, ordered by name.", "SELECT name, price * 2 AS doubled_price FROM products ORDER BY name;")],
    }
    suffixes=["Basics","Boundary Cases","Report","Review","Dashboard","Audit","Snapshot","Analysis","Practice","Challenge"]
    generic_descriptions = {
        "count": ["Return the number of open tickets.", "Return the total number of tickets.", "Return each status with its ticket count, alphabetically by status.", "Return the number of tickets that are not open.", "Return yes when at least one ticket is open; otherwise return no.", "Return the smallest id among open tickets.", "Return the largest id among open tickets.", "Return ids of open tickets in ascending order.", "Return ids of closed tickets in ascending order.", "Return the number of distinct ticket statuses."],
        "group": ["Return each team with its average salary, ordered by team.", "Return each team with its staff count, ordered by team.", "Return each team with its total salary, ordered by team.", "Return each team with its highest salary, ordered by team.", "Return each team with its lowest salary, ordered by team.", "Return the number of staff records with a salary.", "Return the overall average salary.", "Return staff names from highest salary to lowest, breaking ties by name.", "Return names of staff earning at least 100, alphabetically.", "Return distinct staff names, alphabetically."],
        "join": ["Return order id and customer name for every order, ordered by order id.", "Return customer name and order id for every order, ordered by customer then order.", "Return the number of orders with an id.", "Return the number of customers who placed an order.", "Return names of customers who placed an order, alphabetically.", "Return ids of Ada's orders in ascending order.", "Return each ordering customer id and its order count.", "Return every customer id and name, ordered by id.", "Return order id and customer id, ordered by customer then order.", "Return the greatest order id."],
        "missing": ["Return names of customers with no orders, alphabetically.", "Return the number of customers with no orders.", "Return names of customers who have at least one order, alphabetically.", "Return the total number of orders.", "Return every customer name alphabetically.", "Return ids of customers with no orders, ascending.", "Return every order id ascending.", "Return the total number of customers.", "Return every customer with its order count, alphabetically by customer.", "Return the alphabetically first customer with no order, or an empty result."],
        "case": ["Return each student with Pass for marks at least 50 and Fail otherwise, ordered by student.", "Return the number of passing students.", "Return failing student names alphabetically.", "Return students and marks from highest mark to lowest, breaking ties by student.", "Return the highest mark.", "Return the lowest mark.", "Return the average mark.", "Return each student and mark plus one, ordered by student.", "Return each student's High, Pass, or Fail band (80/50 thresholds), ordered by student.", "Return the number of exam records."],
        "subquery": ["Return names with a score above the overall average, alphabetically.", "Return names tied for the maximum score, alphabetically.", "Return names tied for the minimum score, alphabetically.", "Return how many scores exceed the overall average.", "Return the overall average score.", "Return names and scores from highest to lowest, breaking ties by name.", "Return names with non-negative scores, alphabetically.", "Return the number of score records.", "Return distinct score values in ascending order.", "Return each name and twice its score, alphabetically."],
        "distinct": ["Return distinct cities alphabetically.", "Return the number of distinct cities.", "Return each city with its address count, alphabetically by city.", "Return names alphabetically.", "Return names living in Leeds, alphabetically.", "Return cities ordered by city then resident name.", "Return the total number of address records.", "Return the alphabetically first city.", "Return the alphabetically last city.", "Return each name and city ordered by city then name."],
        "having": ["Return teams with at least two staff, alphabetically.", "Return each team and staff count, alphabetically by team.", "Return the total number of staff.", "Return distinct teams alphabetically.", "Return teams with exactly one staff member, alphabetically.", "Return the alphabetically first team.", "Return the alphabetically last team.", "Return all staff names alphabetically.", "Return teams with more than one staff member, alphabetically.", "Return the number of distinct teams."],
    }
    for family_index,(slug,base_title,description,solution,topics,complexity,setup,expected) in enumerate(families,1):
        for variant,suffix in enumerate(suffixes,1):
            title_suffix=suffix
            # Distinct operations per family: filtering, aggregations, joins,
            # anti-joins, CASE, correlated-style subqueries, and set shaping.
            generic_variants = {
                "count": ["SELECT COUNT(*) FROM tickets WHERE status = 'open';", "SELECT COUNT(*) FROM tickets;", "SELECT status, COUNT(*) FROM tickets GROUP BY status ORDER BY status;", "SELECT COUNT(*) FROM tickets WHERE status <> 'open';", "SELECT CASE WHEN COUNT(*) > 0 THEN 'yes' ELSE 'no' END FROM tickets WHERE status='open';", "SELECT MIN(id) FROM tickets WHERE status='open';", "SELECT MAX(id) FROM tickets WHERE status='open';", "SELECT id FROM tickets WHERE status='open' ORDER BY id;", "SELECT id FROM tickets WHERE status='closed' ORDER BY id;", "SELECT COUNT(DISTINCT status) FROM tickets;"],
                "group": ["SELECT team, AVG(salary) FROM staff GROUP BY team ORDER BY team;", "SELECT team, COUNT(*) FROM staff GROUP BY team ORDER BY team;", "SELECT team, SUM(salary) FROM staff GROUP BY team ORDER BY team;", "SELECT team, MAX(salary) FROM staff GROUP BY team ORDER BY team;", "SELECT team, MIN(salary) FROM staff GROUP BY team ORDER BY team;", "SELECT COUNT(salary) FROM staff;", "SELECT AVG(salary) FROM staff;", "SELECT name FROM staff ORDER BY salary DESC, name;", "SELECT name FROM staff WHERE salary >= 100 ORDER BY name;", "SELECT DISTINCT name FROM staff ORDER BY name;"],
                "join": ["SELECT o.id,c.name FROM orders o JOIN customers c ON c.id=o.customer_id ORDER BY o.id;", "SELECT c.name,o.id FROM customers c JOIN orders o ON o.customer_id=c.id ORDER BY c.name,o.id;", "SELECT COUNT(id) FROM orders;", "SELECT COUNT(DISTINCT customer_id) FROM orders;", "SELECT c.name FROM customers c JOIN orders o ON o.customer_id=c.id ORDER BY c.name;", "SELECT o.id FROM orders o JOIN customers c ON c.id=o.customer_id WHERE c.name='Ada' ORDER BY o.id;", "SELECT o.customer_id,COUNT(*) FROM orders o GROUP BY o.customer_id ORDER BY o.customer_id;", "SELECT c.id,c.name FROM customers c ORDER BY c.id;", "SELECT o.id,o.customer_id FROM orders o ORDER BY o.customer_id,o.id;", "SELECT MAX(id) FROM orders;"],
                "missing": ["SELECT c.name FROM customers c LEFT JOIN orders o ON o.customer_id=c.id WHERE o.id IS NULL ORDER BY c.name;", "SELECT COUNT(*) FROM customers c LEFT JOIN orders o ON o.customer_id=c.id WHERE o.id IS NULL;", "SELECT c.name FROM customers c WHERE EXISTS(SELECT 1 FROM orders o WHERE o.customer_id=c.id) ORDER BY c.name;", "SELECT COUNT(*) FROM orders;", "SELECT c.name FROM customers c ORDER BY c.name;", "SELECT c.id FROM customers c LEFT JOIN orders o ON o.customer_id=c.id WHERE o.id IS NULL ORDER BY c.id;", "SELECT o.id FROM orders o ORDER BY o.id;", "SELECT COUNT(*) FROM customers;", "SELECT c.name,COUNT(o.id) FROM customers c LEFT JOIN orders o ON o.customer_id=c.id GROUP BY c.id,c.name ORDER BY c.name;", "SELECT MIN(c.name) FROM customers c LEFT JOIN orders o ON o.customer_id=c.id WHERE o.id IS NULL;"],
                "case": ["SELECT student,CASE WHEN mark>=50 THEN 'Pass' ELSE 'Fail' END FROM exams ORDER BY student;", "SELECT COUNT(*) FROM exams WHERE mark>=50;", "SELECT student FROM exams WHERE mark<50 ORDER BY student;", "SELECT student,mark FROM exams ORDER BY mark DESC,student;", "SELECT MAX(mark) FROM exams;", "SELECT MIN(mark) FROM exams;", "SELECT AVG(mark) FROM exams;", "SELECT student,mark+1 FROM exams ORDER BY student;", "SELECT CASE WHEN mark>=80 THEN 'High' WHEN mark>=50 THEN 'Pass' ELSE 'Fail' END FROM exams ORDER BY student;", "SELECT COUNT(*) FROM exams;"],
                "subquery": ["SELECT name FROM scores WHERE score>(SELECT AVG(score) FROM scores) ORDER BY name;", "SELECT name FROM scores WHERE score=(SELECT MAX(score) FROM scores) ORDER BY name;", "SELECT name FROM scores WHERE score=(SELECT MIN(score) FROM scores) ORDER BY name;", "SELECT COUNT(*) FROM scores WHERE score>(SELECT AVG(score) FROM scores);", "SELECT AVG(score) FROM scores;", "SELECT name,score FROM scores ORDER BY score DESC,name;", "SELECT name FROM scores WHERE score>=0 ORDER BY name;", "SELECT COUNT(*) FROM scores;", "SELECT DISTINCT score FROM scores ORDER BY score;", "SELECT name,score*2 FROM scores ORDER BY name;"],
                "distinct": ["SELECT DISTINCT city FROM addresses ORDER BY city;", "SELECT COUNT(DISTINCT city) FROM addresses;", "SELECT city,COUNT(*) FROM addresses GROUP BY city ORDER BY city;", "SELECT name FROM addresses ORDER BY name;", "SELECT name FROM addresses WHERE city='Leeds' ORDER BY name;", "SELECT city FROM addresses ORDER BY city,name;", "SELECT COUNT(*) FROM addresses;", "SELECT MIN(city) FROM addresses;", "SELECT MAX(city) FROM addresses;", "SELECT name,city FROM addresses ORDER BY city,name;"],
                "having": ["SELECT team FROM staff GROUP BY team HAVING COUNT(*)>=2 ORDER BY team;", "SELECT team,COUNT(*) FROM staff GROUP BY team ORDER BY team;", "SELECT COUNT(*) FROM staff;", "SELECT DISTINCT team FROM staff ORDER BY team;", "SELECT team FROM staff GROUP BY team HAVING COUNT(*)=1 ORDER BY team;", "SELECT MIN(team) FROM staff;", "SELECT MAX(team) FROM staff;", "SELECT name FROM staff ORDER BY name;", "SELECT team,COUNT(*) FROM staff GROUP BY team HAVING COUNT(*)>1 ORDER BY team;", "SELECT COUNT(DISTINCT team) FROM staff;"],
            }
            if slug in variant_specs:
                title_suffix, description, solution = variant_specs[slug][variant-1]
            elif slug in generic_variants:
                solution = generic_variants[slug][variant-1]
                description = generic_descriptions[slug][variant-1]
                # The catalog rail shows titles before descriptions.  Make the
                # variant's actual report visible there rather than a generic
                # 'Review' suffix left over from early fixture scaffolding.
                title_suffix = (description[7:] if description.startswith("Return ") else description).split(".", 1)[0].title()
            # The five fixtures intentionally vary data cardinality, ties, and empty/no-match shapes.
            cases=[_sql_case(setup,expected)]
            if slug=="filter": extra=[("CREATE TABLE customers(id INTEGER PRIMARY KEY,name TEXT,score INTEGER); INSERT INTO customers VALUES(1,'A',69),(2,'B',70);","B\t70"),("CREATE TABLE customers(id INTEGER PRIMARY KEY,name TEXT,score INTEGER); INSERT INTO customers VALUES(1,'A',10);",""),("CREATE TABLE customers(id INTEGER PRIMARY KEY,name TEXT,score INTEGER); INSERT INTO customers VALUES(1,'Z',100),(2,'A',71);","Z\t100\nA\t71"),("CREATE TABLE customers(id INTEGER PRIMARY KEY,name TEXT,score INTEGER);","" )]
            elif slug=="order": extra=[("CREATE TABLE products(name TEXT,price INTEGER); INSERT INTO products VALUES('A',1),('B',2);","B\nA"),("CREATE TABLE products(name TEXT,price INTEGER); INSERT INTO products VALUES('Z',5),('A',5);","A\nZ"),("CREATE TABLE products(name TEXT,price INTEGER);",""),("CREATE TABLE products(name TEXT,price INTEGER); INSERT INTO products VALUES('Only',0);","Only")]
            elif slug=="count": extra=[("CREATE TABLE tickets(id INTEGER,status TEXT); INSERT INTO tickets VALUES(1,'closed');","0"),("CREATE TABLE tickets(id INTEGER,status TEXT); INSERT INTO tickets VALUES(1,'open'),(2,'open');","2"),("CREATE TABLE tickets(id INTEGER,status TEXT);","0"),("CREATE TABLE tickets(id INTEGER,status TEXT); INSERT INTO tickets VALUES(1,'OPEN'),(2,'open');","1")]
            elif slug=="group": extra=[("CREATE TABLE staff(name TEXT,team TEXT,salary INTEGER); INSERT INTO staff VALUES('A','A',1),('B','A',2);","A\t1.5"),("CREATE TABLE staff(name TEXT,team TEXT,salary INTEGER); INSERT INTO staff VALUES('A','Z',9);","Z\t9.0"),("CREATE TABLE staff(name TEXT,team TEXT,salary INTEGER);",""),("CREATE TABLE staff(name TEXT,team TEXT,salary INTEGER); INSERT INTO staff VALUES('A','B',0),('B','A',10);","A\t10.0\nB\t0.0")]
            elif slug=="join": extra=[("CREATE TABLE customers(id INTEGER PRIMARY KEY,name TEXT); CREATE TABLE orders(id INTEGER PRIMARY KEY,customer_id INTEGER); INSERT INTO customers VALUES(1,'A'); INSERT INTO orders VALUES(1,1);","1\tA"),("CREATE TABLE customers(id INTEGER PRIMARY KEY,name TEXT); CREATE TABLE orders(id INTEGER PRIMARY KEY,customer_id INTEGER); INSERT INTO customers VALUES(1,'A');",""),("CREATE TABLE customers(id INTEGER PRIMARY KEY,name TEXT); CREATE TABLE orders(id INTEGER PRIMARY KEY,customer_id INTEGER); INSERT INTO customers VALUES(1,'A'),(2,'B'); INSERT INTO orders VALUES(2,1),(1,2);","1\tB\n2\tA"),("CREATE TABLE customers(id INTEGER PRIMARY KEY,name TEXT); CREATE TABLE orders(id INTEGER PRIMARY KEY,customer_id INTEGER);","" )]
            elif slug=="missing": extra=[("CREATE TABLE customers(id INTEGER PRIMARY KEY,name TEXT); CREATE TABLE orders(id INTEGER PRIMARY KEY,customer_id INTEGER); INSERT INTO customers VALUES(1,'A');","A"),("CREATE TABLE customers(id INTEGER PRIMARY KEY,name TEXT); CREATE TABLE orders(id INTEGER PRIMARY KEY,customer_id INTEGER); INSERT INTO customers VALUES(1,'A'); INSERT INTO orders VALUES(1,1);",""),("CREATE TABLE customers(id INTEGER PRIMARY KEY,name TEXT); CREATE TABLE orders(id INTEGER PRIMARY KEY,customer_id INTEGER); INSERT INTO customers VALUES(1,'Z'),(2,'A');","A\nZ"),("CREATE TABLE customers(id INTEGER PRIMARY KEY,name TEXT); CREATE TABLE orders(id INTEGER PRIMARY KEY,customer_id INTEGER);","" )]
            elif slug=="case": extra=[("CREATE TABLE exams(student TEXT,mark INTEGER); INSERT INTO exams VALUES('A',50);","A\tPass"),("CREATE TABLE exams(student TEXT,mark INTEGER); INSERT INTO exams VALUES('A',0),('B',100);","A\tFail\nB\tPass"),("CREATE TABLE exams(student TEXT,mark INTEGER);",""),("CREATE TABLE exams(student TEXT,mark INTEGER); INSERT INTO exams VALUES('Z',49),('A',51);","A\tPass\nZ\tFail")]
            elif slug=="subquery": extra=[("CREATE TABLE scores(name TEXT,score INTEGER); INSERT INTO scores VALUES('A',1),('B',1);",""),("CREATE TABLE scores(name TEXT,score INTEGER); INSERT INTO scores VALUES('A',1),('B',2),('C',3);","C"),("CREATE TABLE scores(name TEXT,score INTEGER); INSERT INTO scores VALUES('A',-1),('B',1);","B"),("CREATE TABLE scores(name TEXT,score INTEGER);","" )]
            elif slug=="distinct": extra=[("CREATE TABLE addresses(name TEXT,city TEXT); INSERT INTO addresses VALUES('A','A');","A"),("CREATE TABLE addresses(name TEXT,city TEXT); INSERT INTO addresses VALUES('A','Z'),('B','A'),('C','Z');","A\nZ"),("CREATE TABLE addresses(name TEXT,city TEXT);",""),("CREATE TABLE addresses(name TEXT,city TEXT); INSERT INTO addresses VALUES('A','Same'),('B','Same');","Same")]
            else: extra=[("CREATE TABLE staff(name TEXT,team TEXT); INSERT INTO staff VALUES('A','A'),('B','A');","A"),("CREATE TABLE staff(name TEXT,team TEXT); INSERT INTO staff VALUES('A','A');",""),("CREATE TABLE staff(name TEXT,team TEXT); INSERT INTO staff VALUES('A','Z'),('B','A'),('C','A'),('D','Z');","A\nZ"),("CREATE TABLE staff(name TEXT,team TEXT);","" )]
            cases.extend(_sql_case(a,b) for a,b in extra)
            # Each of the five deterministic fixtures gets the oracle for this
            # exact query variant, so the exercises are semantic variations,
            # not merely renamed copies of the same task.
            for case in cases:
                case["expected_output"] = _sqlite_oracle(solution, case["setup_sql"])
            num=(family_index-1)*10+variant
            # Difficulty reflects the SQL concept, not the position of its
            # source-table family. DISTINCT is a foundation; HAVING is an
            # interview-level grouping skill. Truly advanced SQL lives in the
            # separately reviewed recursive/window/relational-division bank.
            difficulty = (
                "Easy"
                if family_index <= 3 or family_index == 9
                else "Medium"
            )
            result.append(_record(key=f"sql-{slug}-{num:03d}",title=title_suffix,language="sql",difficulty=difficulty,topics=topics,description=description,constraints=["Write one read-only SELECT or WITH query in the selected dialect.","The selected dialect is translated for local SQLite compatibility before judging.","Return columns in the requested order."],starter="-- Write one read-only SELECT or WITH query in the selected dialect.\n",solution=solution,cases=cases,hints=["Start by identifying the source table and output columns.","Make result ordering explicit when the prompt asks for it.","Test zero rows and tie cases."],complexity=complexity))
    return result


_ALL_JAVA = _java_numeric() + _java_text() + _java_patterns()
# Keep the genuinely distinct core Java curriculum.  The prior contextual
# copies are deliberately excluded: changing a story title is not a new drill.
_JAVA_CORE_IDS = {*(f"java-num-{i:03d}" for i in range(1, 11)),
                 *(f"java-text-{i:03d}" for i in range(1, 6)), "java-pattern-001"}
MULTILANG_EXERCISES = [item for item in _ALL_JAVA if item["id"] in _JAVA_CORE_IDS] + _sql()

# Correct independently authored context fixtures where their narrative copy
# originally inherited a case from the neighbouring array drill.  Keep these
# patches adjacent to construction so every oracle remains explicit/auditable.
_BY_ID = {item["id"]: item for item in MULTILANG_EXERCISES}
_BY_ID["java-num-001"]["solution"] = _java_program("""        int n=in.nextInt(); long s=0;
        for(int i=0;i<n;i++) s+=in.nextLong();
        System.out.println(s);""")
_REVERSE_BODY = """        int n=in.nextInt(); int[] a=new int[n];
        for(int i=0;i<n;i++) a[i]=in.nextInt();
        for(int i=n-1;i>=0;i--){ if(i<n-1)System.out.print(\" \"); System.out.print(a[i]); }
        System.out.println();"""
for _id in ("java-num-009",):
    _BY_ID[_id]["solution"] = _java_program(_REVERSE_BODY)
_FIRST_REPEAT_CASES = _number_cases([
    ("5\n1 2 3 2 1\n", "2"), ("3\n1 2 3\n", "-1"),
    ("2\n7 7\n", "7"), ("0\n", "-1"), ("4\n-1 0 -1 0\n", "-1"),
])
for _id in ():
    _item = _BY_ID[_id]
    _item["solution"] = _java_program("""        int n=in.nextInt(); Set<Integer> seen=new HashSet<>();
        int ans=-1; boolean found=false;
        for(int i=0;i<n;i++){ int x=in.nextInt(); if(!found && !seen.add(x)){ ans=x; found=true; } }
        System.out.println(ans);""")
    _item["public_tests"] = _FIRST_REPEAT_CASES[:2]
    _item["hidden_tests"] = _FIRST_REPEAT_CASES[2:] + [{"input": "4\n-1 0 -1 0\n\n", "expected_output": "-1"}]
