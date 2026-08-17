"""Beginner-first Python practice extension 201--288.

Every drill uses plain stdin/stdout, states its input lines explicitly, and
keeps its reference solution deliberately readable for new programmers.
"""
from __future__ import annotations

STARTER = "import sys\n\ndef solve() -> None:\n    pass\n\nif __name__ == '__main__':\n    solve()\n"
ITEMS = []


def add(num, title, topics, description, constraints, hints, complexity, body, cases, explanation):
    records = [{"input": source, "expected_output": result} for source, result in cases]
    ITEMS.append({"id": f"python-curated-{num:03d}", "language": "python", "title": title,
        "difficulty": "Easy", "topics": topics, "practice_frequency": "Common",
        "description": description, "constraints": constraints, "hints": hints,
        "expected_complexity": complexity, "starter_code": STARTER,
        "solution": "import sys\n" + body.strip() + "\n\nif __name__ == '__main__':\n    solve()\n",
        "examples": [{"input": records[0]["input"], "output": records[0]["expected_output"], "explanation": explanation}],
        "public_tests": records[:2], "hidden_tests": records[2:]})


# Numbers and direct conditionals.
add(201,"Add two integers",["math","input-output"],"Line 1 contains two integers a and b. Print their sum.",["-1,000,000 <= a,b <= 1,000,000"],["Read both values with input().split().","Convert them with int.","Use +."],"O(1) time and O(1) space","""def solve():
    a,b=map(int,input().split()); print(a+b)""",[("2 3\n","5"),("-4 10\n","6"),("0 0\n","0"),("999999 1\n","1000000")],"Two plus three is five.")
add(202,"Subtract two integers",["math","input-output"],"Line 1 contains integers a and b. Print a minus b.",["-1,000,000 <= a,b <= 1,000,000"],["Keep the input order.","Convert both values to int.","Use the - operator."],"O(1) time and O(1) space","""def solve():
    a,b=map(int,input().split()); print(a-b)""",[("9 4\n","5"),("3 8\n","-5"),("0 -7\n","7"),("-2 -2\n","0")],"Subtracting four from nine leaves five.")
add(203,"Multiply two integers",["math","input-output"],"Line 1 contains two integers. Print their product.",["Each integer is between -100,000 and 100,000"],["Read both numbers from line 1.","Convert them to int.","Use * for multiplication."],"O(1) time and O(1) space","""def solve():
    a,b=map(int,input().split()); print(a*b)""",[("6 7\n","42"),("-3 5\n","-15"),("0 99\n","0"),("-4 -8\n","32")],"Six times seven is forty-two.")
add(204,"Integer quotient",["math","division"],"Line 1 contains integers a and b, where b is not zero. Print the quotient from floor division a // b.",["-1,000,000 <= a <= 1,000,000", "-1,000 <= b <= 1,000 and b != 0"],["Use // rather than /.","Floor division rounds down for negative values.","Do not print a decimal."],"O(1) time and O(1) space","""def solve():
    a,b=map(int,input().split()); print(a//b)""",[("17 5\n","3"),("-7 3\n","-3"),("8 -2\n","-4"),("0 9\n","0")],"Seventeen floor-divided by five is three.")
add(205,"Integer remainder",["math","division"],"Line 1 contains integers a and b, where b is not zero. Print a modulo b.",["-1,000,000 <= a <= 1,000,000", "-1,000 <= b <= 1,000 and b != 0"],["Use the % operator.","The divisor is the second number.","Python pairs % with //."],"O(1) time and O(1) space","""def solve():
    a,b=map(int,input().split()); print(a%b)""",[("17 5\n","2"),("-7 3\n","2"),("8 -2\n","0"),("0 9\n","0")],"The remainder after seventeen divided by five is two.")
add(206,"Absolute value",["math","conditionals"],"Line 1 contains an integer n. Print its distance from zero.",["-1,000,000 <= n <= 1,000,000"],["A distance is never negative.","Python provides abs.","Print the returned value."],"O(1) time and O(1) space","""def solve():
    print(abs(int(input())))""",[("-12\n","12"),("5\n","5"),("0\n","0"),("-1\n","1")],"Negative twelve is twelve units from zero.")
add(207,"Larger of two",["conditionals","math"],"Line 1 contains two integers. Print the larger integer; if equal, print that value.",["-1,000,000 <= both integers <= 1,000,000"],["Compare the two values.","max gives the larger value.","Equal values need no special output."],"O(1) time and O(1) space","""def solve():
    a,b=map(int,input().split()); print(max(a,b))""",[("4 9\n","9"),("7 7\n","7"),("-2 -8\n","-2"),("0 -1\n","0")],"Nine is larger than four.")
add(208,"Smallest of three",["conditionals","math"],"Line 1 contains three integers. Print the smallest one.",["-1,000,000 <= each integer <= 1,000,000"],["Read all three values.","min finds the smallest.","Negative values can be smallest."],"O(1) time and O(1) space","""def solve():
    print(min(map(int,input().split())))""",[("4 -2 9\n","-2"),("3 3 3\n","3"),("0 8 1\n","0"),("-1 -7 -4\n","-7")],"Negative two is the smallest value.")
add(209,"Is even",["conditionals","math"],"Line 1 contains an integer n. Print YES if n is even, otherwise print NO.",["-1,000,000 <= n <= 1,000,000"],["Even numbers have remainder zero when divided by two.","Use n % 2.","Print exactly YES or NO."],"O(1) time and O(1) space","""def solve():
    n=int(input()); print('YES' if n%2==0 else 'NO')""",[("8\n","YES"),("-3\n","NO"),("0\n","YES"),("11\n","NO")],"Eight divides by two with no remainder.")
add(210,"Celsius to Fahrenheit",["math","formatting"],"Line 1 contains an integer temperature in Celsius. Print Fahrenheit as an integer using F = C * 9 // 5 + 32. Inputs are chosen so this formula is exact.",["-100 <= C <= 100", "C is a multiple of 5"],["Start with Celsius times nine.","Divide by five, then add 32.","The result is an integer."],"O(1) time and O(1) space","""def solve():
    c=int(input()); print(c*9//5+32)""",[("0\n","32"),("100\n","212"),("-40\n","-40"),("25\n","77")],"Zero Celsius is thirty-two Fahrenheit.")

# Counting and numeric loops.
add(211,"Sum from one to n",["loops","math"],"Line 1 contains positive integer n. Print 1 + 2 + ... + n.",["1 <= n <= 1,000,000"],["This is an arithmetic series.","Use n * (n + 1) // 2.","No loop is required."],"O(1) time and O(1) space","""def solve():
    n=int(input()); print(n*(n+1)//2)""",[("5\n","15"),("1\n","1"),("100\n","5050"),("7\n","28")],"One through five add to fifteen.")
add(212,"Count down to zero",["loops","output"],"Line 1 contains nonnegative integer n. Print n down to 0, one integer per line.",["0 <= n <= 5,000"],["range can count backwards.","Include -1 as the stopping point.","Print each number on its own line."],"O(n) time and O(1) auxiliary space","""def solve():
    n=int(input())
    for x in range(n,-1,-1): print(x)""",[("3\n","3\n2\n1\n0"),("0\n","0"),("1\n","1\n0"),("5\n","5\n4\n3\n2\n1\n0")],"Start at three and step down to zero.")
add(213,"Sum of even numbers",["loops","math"],"Line 1 contains positive integer n. Print the sum of all even integers from 1 through n.",["1 <= n <= 1,000,000"],["The evens are 2, 4, 6, ...","There are n // 2 of them.","Their sum is k * (k + 1)."],"O(1) time and O(1) space","""def solve():
    k=int(input())//2; print(k*(k+1))""",[("8\n","20"),("1\n","0"),("5\n","6"),("100\n","2550")],"Two plus four plus six plus eight is twenty.")
add(214,"Multiplication table",["loops","output"],"Line 1 contains integer n. Print n times 1 through n times 10, one result per line.",["-1,000 <= n <= 1,000"],["Loop from 1 through 10.","Multiply n by the loop number.","Print only the result on each line."],"O(1) time and O(1) auxiliary space","""def solve():
    n=int(input())
    for i in range(1,11): print(n*i)""",[("3\n","3\n6\n9\n12\n15\n18\n21\n24\n27\n30"),("0\n","0\n0\n0\n0\n0\n0\n0\n0\n0\n0"),("-1\n","-1\n-2\n-3\n-4\n-5\n-6\n-7\n-8\n-9\n-10"),("2\n","2\n4\n6\n8\n10\n12\n14\n16\n18\n20")],"The first ten multiples of three are printed.")
add(215,"Factorial",["loops","math"],"Line 1 contains integer n. Print n factorial, the product from 1 through n. By definition, 0! is 1.",["0 <= n <= 12"],["Begin the product at one.","Multiply each value from 2 through n.","Zero needs no multiplication."],"O(n) time and O(1) auxiliary space","""def solve():
    n=int(input()); answer=1
    for x in range(2,n+1): answer*=x
    print(answer)""",[("5\n","120"),("0\n","1"),("1\n","1"),("8\n","40320")],"Five factorial is 1 * 2 * 3 * 4 * 5.")
add(216,"Digit count",["loops","strings"],"Line 1 contains a nonnegative integer n. Print how many decimal digits it has. Zero has one digit.",["0 <= n <= 10^18"],["Reading as text keeps every digit.","len gives the number of characters.","There is no sign character in the input."],"O(d) time and O(d) input space, where d is the digit count","""def solve():
    print(len(input().strip()))""",[("507\n","3"),("0\n","1"),("1000000000000000000\n","19"),("42\n","2")],"507 has three digits.")
add(217,"Sum of digits",["loops","strings"],"Line 1 contains a nonnegative integer n. Print the sum of its decimal digits.",["0 <= n <= 10^18"],["Read the number as a string.","Convert each character to int.","Add the converted digits."],"O(d) time and O(d) input space","""def solve():
    print(sum(map(int,input().strip())))""",[("507\n","12"),("0\n","0"),("999\n","27"),("1002\n","3")],"Five plus zero plus seven is twelve.")
add(218,"Reverse digits",["strings","loops"],"Line 1 contains a nonnegative integer n with no leading zero unless n is 0. Print its digits in reverse order.",["0 <= n <= 10^18"],["Read the input as text.","String slicing [::-1] reverses text.","Do not convert the reversed result back to int."],"O(d) time and O(d) space","""def solve():
    print(input().strip()[::-1])""",[("1205\n","5021"),("0\n","0"),("7\n","7"),("100\n","001")],"The digits of 1205 backwards are 5021.")
add(219,"Count positive values",["lists","loops"],"Line 1 contains n. Line 2 contains n space-separated integers. Print how many are greater than zero.",["1 <= n <= 100,000", "Each value is between -1,000,000 and 1,000,000"],["Line 1 tells you how many values are on line 2.","Check value > 0 for each number.","Zero is not positive."],"O(n) time and O(n) input space","""def solve():
    n=int(input()); values=list(map(int,input().split())); print(sum(x>0 for x in values))""",[("5\n-2 0 4 8 -1\n","2"),("1\n0\n","0"),("4\n1 2 3 4\n","4"),("3\n-1 -2 -3\n","0")],"Only four and eight are positive.")
add(220,"Product of a list",["lists","loops"],"Line 1 contains n. Line 2 contains n space-separated integers. Print their product.",["1 <= n <= 20", "Each value is between -10 and 10"],["Start the answer at one.","Multiply every value on line 2.","A zero makes the final product zero."],"O(n) time and O(n) input space","""def solve():
    n=int(input()); answer=1
    for x in map(int,input().split()): answer*=x
    print(answer)""",[("3\n2 3 4\n","24"),("1\n-5\n","-5"),("4\n1 0 9 2\n","0"),("3\n-2 -3 4\n","24")],"Two times three times four is twenty-four.")

# Text fundamentals.
add(221,"Text length",["strings"],"Line 1 contains a string, possibly with spaces. Print its number of characters, including spaces.",["0 <= line length <= 10,000"],["Use rstrip only to remove the input newline.","Spaces are characters.","len counts them too."],"O(n) time and O(n) input space","""def solve():
    print(len(input().rstrip('\\n')))""",[("hello world\n","11"),("\n","0"),("a b\n","3"),("  hi\n","4")],"The space in hello world is counted.")
add(222,"First character",["strings"],"Line 1 contains a nonempty string. Print its first character.",["1 <= line length <= 10,000"],["Strings use zero-based indexes.","The first index is 0.","Do not strip spaces; a space can be first."],"O(1) time and O(n) input space","""def solve():
    print(input().rstrip('\\n')[0])""",[("python\n","p"),("Z\n","Z"),(" hello\n"," "),("42\n","4")],"Index zero of python is p.")
add(223,"Last character",["strings"],"Line 1 contains a nonempty string. Print its last character.",["1 <= line length <= 10,000"],["Remove only the final newline.","Index -1 means the last character.","A trailing space before Enter is part of the string."],"O(1) time and O(n) input space","""def solve():
    print(input().rstrip('\\n')[-1])""",[("python\n","n"),("Z\n","Z"),("hello world\n","d"),("abc123\n","3")],"Index -1 of python is n.")
add(224,"Uppercase text",["strings"],"Line 1 contains a string. Print the same string with letters changed to uppercase.",["0 <= line length <= 10,000"],["Read the whole line.","Use the string method upper().","Digits and punctuation stay unchanged."],"O(n) time and O(n) space","""def solve():
    print(input().rstrip('\\n').upper())""",[("Hello, world!\n","HELLO, WORLD!"),("abc123\n","ABC123"),("\n",""),("MiXeD\n","MIXED")],"upper changes each letter to its capital form.")
add(225,"Lowercase text",["strings"],"Line 1 contains a string. Print the same string with letters changed to lowercase.",["0 <= line length <= 10,000"],["Read the whole line.","Use lower().","Numbers stay as they are."],"O(n) time and O(n) space","""def solve():
    print(input().rstrip('\\n').lower())""",[("Hello, WORLD!\n","hello, world!"),("ABC123\n","abc123"),("\n",""),("MiXeD\n","mixed")],"lower changes each letter to its small form.")
add(226,"Count vowels",["strings","loops"],"Line 1 contains a string. Print the number of English vowels a, e, i, o, u, counting both uppercase and lowercase.",["0 <= line length <= 10,000"],["Convert the text to lowercase.","Check whether each character is in aeiou.","y is not a vowel for this drill."],"O(n) time and O(n) space","""def solve():
    print(sum(c in 'aeiou' for c in input().rstrip('\\n').lower()))""",[("Beautiful\n","5"),("rhythm\n","0"),("AEIOU\n","5"),("a e i\n","3")],"Beautiful contains five vowels.")
add(227,"Reverse text",["strings"],"Line 1 contains a string. Print the characters in reverse order.",["0 <= line length <= 10,000"],["Keep spaces as characters.","Use [::-1] to reverse a string.","Remove only the newline first."],"O(n) time and O(n) space","""def solve():
    print(input().rstrip('\\n')[::-1])""",[("stressed\n","desserts"),("a b\n","b a"),("\n",""),("Python\n","nohtyP")],"stressed backwards spells desserts.")
add(228,"Palindrome text",["strings","conditionals"],"Line 1 contains a string with no leading or trailing spaces. Print YES if it reads the same backwards, otherwise print NO. Case matters.",["0 <= line length <= 10,000"],["Make a reversed copy.","Compare it to the original.","An empty string is a palindrome."],"O(n) time and O(n) space","""def solve():
    s=input().rstrip('\\n'); print('YES' if s==s[::-1] else 'NO')""",[("level\n","YES"),("Python\n","NO"),("\n","YES"),("Aa\n","NO")],"level has the same letters in reverse.")
add(229,"Count one character",["strings"],"Line 1 contains a string. Line 2 contains one character. Print how many times that character appears in line 1. Matching is case-sensitive.",["0 <= text length <= 10,000", "Line 2 contains exactly one character"],["Read the text first.","The next input line is the target character.","str.count counts non-overlapping single characters."],"O(n) time and O(n) input space","""def solve():
    text=input().rstrip('\\n'); target=input().rstrip('\\n'); print(text.count(target))""",[("banana\na\n","3"),("Hello\nl\n","2"),("Hello\nL\n","0"),("\nx\n","0")],"banana contains three lowercase a characters.")
add(230,"Word count",["strings","lists"],"Line 1 contains a string. Words are maximal groups of non-space characters. Print the number of words.",["0 <= line length <= 10,000"],["split() without an argument handles repeated spaces.","It also ignores leading and trailing spaces.","Count the resulting words."],"O(n) time and O(n) space","""def solve():
    print(len(input().split()))""",[("one two three\n","3"),("   hello   world  \n","2"),("\n","0"),("single\n","1")],"There are three space-separated words.")

# Lists and ordering.
add(231,"List sum",["lists","loops"],"Line 1 contains n. Line 2 contains n space-separated integers. Print their sum.",["1 <= n <= 100,000", "Each integer is between -1,000,000 and 1,000,000"],["Read n from line 1.","Read the values from line 2.","sum adds a list of numbers."],"O(n) time and O(n) input space","""def solve():
    n=int(input()); print(sum(map(int,input().split())))""",[("4\n1 2 3 4\n","10"),("3\n-2 5 -1\n","2"),("1\n0\n","0"),("5\n1 1 1 1 1\n","5")],"One plus two plus three plus four is ten.")
add(232,"List maximum",["lists","conditionals"],"Line 1 contains n. Line 2 contains n space-separated integers. Print the largest value.",["1 <= n <= 100,000", "Each integer is between -1,000,000 and 1,000,000"],["All values are on line 2.","max finds the largest.","The list is never empty."],"O(n) time and O(n) input space","""def solve():
    n=int(input()); print(max(map(int,input().split())))""",[("4\n1 9 3 2\n","9"),("3\n-5 -2 -8\n","-2"),("1\n7\n","7"),("4\n0 0 0 0\n","0")],"Nine is the largest entry.")
add(233,"List minimum",["lists","conditionals"],"Line 1 contains n. Line 2 contains n space-separated integers. Print the smallest value.",["1 <= n <= 100,000", "Each integer is between -1,000,000 and 1,000,000"],["All values are on line 2.","min finds the smallest.","The list is never empty."],"O(n) time and O(n) input space","""def solve():
    n=int(input()); print(min(map(int,input().split())))""",[("4\n1 9 3 2\n","1"),("3\n-5 -2 -8\n","-8"),("1\n7\n","7"),("4\n0 0 0 0\n","0")],"One is the smallest entry.")
add(234,"Count even list values",["lists","loops"],"Line 1 contains n. Line 2 contains n integers. Print how many values are even.",["1 <= n <= 100,000", "Each integer is between -1,000,000 and 1,000,000"],["Use x % 2 == 0.","Zero is even.","Count every matching value."],"O(n) time and O(n) input space","""def solve():
    n=int(input()); print(sum(x%2==0 for x in map(int,input().split())))""",[("5\n1 2 3 4 5\n","2"),("3\n-2 0 7\n","2"),("1\n9\n","0"),("4\n8 6 4 2\n","4")],"Only two and four are even.")
add(235,"First and last list values",["lists","indexing"],"Line 1 contains n. Line 2 contains n space-separated integers. Print the first and last values, separated by one space.",["1 <= n <= 100,000"],["Store line 2 in a list.","The first item has index 0.","The last item has index -1."],"O(n) time and O(n) space","""def solve():
    n=int(input()); a=input().split(); print(a[0],a[-1])""",[("4\n1 2 3 4\n","1 4"),("1\n7\n","7 7"),("3\n-1 0 2\n","-1 2"),("2\n5 5\n","5 5")],"The first value is one and the last is four.")
add(236,"Reverse a list",["lists","loops"],"Line 1 contains n. Line 2 contains n space-separated integers. Print them in reverse order, separated by spaces.",["1 <= n <= 100,000"],["Read line 2 with split().","Use [::-1] on the list.","print with * separates values by spaces."],"O(n) time and O(n) space","""def solve():
    n=int(input()); a=input().split(); print(*a[::-1])""",[("4\n1 2 3 4\n","4 3 2 1"),("1\n7\n","7"),("3\n-1 0 2\n","2 0 -1"),("2\n5 5\n","5 5")],"The list is read from right to left.")
add(237,"Sort integers",["lists","sorting"],"Line 1 contains n. Line 2 contains n space-separated integers. Print them in ascending order, separated by spaces.",["1 <= n <= 100,000", "Each integer is between -1,000,000 and 1,000,000"],["Convert the values to integers.","sorted returns ascending order by default.","Unpack the list into print."],"O(n log n) time and O(n) space","""def solve():
    n=int(input()); print(*sorted(map(int,input().split())))""",[("4\n3 1 4 2\n","1 2 3 4"),("3\n-1 -3 0\n","-3 -1 0"),("1\n9\n","9"),("4\n2 2 1 2\n","1 2 2 2")],"Sorting puts one before two, three, and four.")
add(238,"Second largest distinct",["lists","conditionals"],"Line 1 contains n. Line 2 contains n space-separated integers. At least two distinct values occur. Print the second-largest distinct value.",["2 <= n <= 100,000", "At least two different values are present"],["A set removes duplicates.","Sort the distinct values.","Index -2 is the second from the end."],"O(n log n) time and O(n) space","""def solve():
    n=int(input()); print(sorted(set(map(int,input().split())))[-2])""",[("4\n1 9 3 2\n","3"),("4\n5 5 4 4\n","4"),("3\n-1 -2 -3\n","-2"),("2\n0 1\n","0")],"After nine, three is the next distinct largest value.")
add(239,"Positive list sum",["lists","loops"],"Line 1 contains n. Line 2 contains n integers. Print the sum of only the positive values.",["1 <= n <= 100,000", "Each integer is between -1,000,000 and 1,000,000"],["Test each number with x > 0.","Ignore zero and negatives.","Add the matching values."],"O(n) time and O(n) input space","""def solve():
    n=int(input()); print(sum(x for x in map(int,input().split()) if x>0))""",[("5\n-2 0 4 8 -1\n","12"),("3\n-1 -2 -3\n","0"),("1\n7\n","7"),("4\n1 2 3 4\n","10")],"Four and eight are the positive values.")
add(240,"List average quotient",["lists","math"],"Line 1 contains n. Line 2 contains n integers whose sum is divisible by n. Print their integer average.",["1 <= n <= 100,000", "The sum of line 2 is divisible by n"],["Add the values first.","Divide by n using //.","The constraint makes the average exact."],"O(n) time and O(n) input space","""def solve():
    n=int(input()); print(sum(map(int,input().split()))//n)""",[("4\n2 4 6 8\n","5"),("3\n-3 0 3\n","0"),("1\n7\n","7"),("2\n10 20\n","15")],"The average of two, four, six, and eight is five.")

# Everyday decisions.
add(241,"Classify a number sign",["conditionals"],"Line 1 contains integer n. Print POSITIVE, NEGATIVE, or ZERO.",["-1,000,000 <= n <= 1,000,000"],["Test n > 0 first.","Then test n < 0.","The remaining case is zero."],"O(1) time and O(1) space","""def solve():
    n=int(input()); print('POSITIVE' if n>0 else 'NEGATIVE' if n<0 else 'ZERO')""",[("7\n","POSITIVE"),("-1\n","NEGATIVE"),("0\n","ZERO"),("999\n","POSITIVE")],"Seven is greater than zero.")
add(242,"Leap year",["conditionals","math"],"Line 1 contains a year. Print YES if it is a Gregorian leap year, otherwise NO. A leap year is divisible by 400, or divisible by 4 but not by 100.",["1 <= year <= 9999"],["Check divisibility with %.","Years divisible by 400 are leap years.","Century years otherwise need divisibility by four and not 100."],"O(1) time and O(1) space","""def solve():
    y=int(input()); print('YES' if y%400==0 or y%4==0 and y%100 else 'NO')""",[("2024\n","YES"),("1900\n","NO"),("2000\n","YES"),("2023\n","NO")],"2024 is divisible by four and not by one hundred.")
add(243,"Multiple check",["conditionals","math"],"Line 1 contains integers a and b, where b is not zero. Print YES if a is a multiple of b, otherwise NO.",["-1,000,000 <= a <= 1,000,000", "-1,000 <= b <= 1,000 and b != 0"],["A multiple has remainder zero.","Test a % b == 0.","Zero is a multiple of every nonzero b."],"O(1) time and O(1) space","""def solve():
    a,b=map(int,input().split()); print('YES' if a%b==0 else 'NO')""",[("12 3\n","YES"),("10 4\n","NO"),("0 7\n","YES"),("-9 3\n","YES")],"Twelve divided by three has no remainder.")
add(244,"Largest of three",["conditionals","math"],"Line 1 contains three integers. Print the largest value.",["-1,000,000 <= each value <= 1,000,000"],["Read all values.","max works for more than two values.","Equal maximum values are fine."],"O(1) time and O(1) space","""def solve():
    print(max(map(int,input().split())))""",[("4 9 2\n","9"),("-1 -2 -3\n","-1"),("5 5 1\n","5"),("0 0 0\n","0")],"Nine is the largest of the three values.")
add(245,"Triangle validity",["conditionals","math"],"Line 1 contains three positive side lengths. Print YES if they can form a non-degenerate triangle, otherwise NO.",["1 <= each side <= 1,000,000"],["Sort the three sides.","The two shorter sides must add to more than the longest.","Equality is not a triangle here."],"O(1) time and O(1) space","""def solve():
    a,b,c=sorted(map(int,input().split())); print('YES' if a+b>c else 'NO')""",[("3 4 5\n","YES"),("1 2 3\n","NO"),("2 2 3\n","YES"),("5 1 1\n","NO")],"Three plus four is greater than five.")
add(246,"Pass mark",["conditionals"],"Line 1 contains a whole-number score from 0 through 100. Print PASS for scores at least 50, otherwise FAIL.",["0 <= score <= 100"],["Compare the score to 50.","At least includes exactly 50.","Print the requested uppercase word."],"O(1) time and O(1) space","""def solve():
    print('PASS' if int(input())>=50 else 'FAIL')""",[("50\n","PASS"),("49\n","FAIL"),("100\n","PASS"),("0\n","FAIL")],"Fifty reaches the pass mark.")
add(247,"Letter grade",["conditionals"],"Line 1 contains a score from 0 through 100. Print A for 90+, B for 80-89, C for 70-79, D for 60-69, otherwise F.",["0 <= score <= 100"],["Check the largest threshold first.","Use descending if/elif conditions.","A score of 90 is A."],"O(1) time and O(1) space","""def solve():
    s=int(input()); print('A' if s>=90 else 'B' if s>=80 else 'C' if s>=70 else 'D' if s>=60 else 'F')""",[("91\n","A"),("80\n","B"),("69\n","D"),("70\n","C")],"A score of 91 is in the A range.")
add(248,"Days in a month",["conditionals"],"Line 1 contains month number m from 1 through 12. Print its number of days in a non-leap year.",["1 <= m <= 12"],["February has 28 days here.","April, June, September, and November have 30.","The rest have 31."],"O(1) time and O(1) space","""def solve():
    m=int(input()); print(28 if m==2 else 30 if m in (4,6,9,11) else 31)""",[("2\n","28"),("4\n","30"),("1\n","31"),("11\n","30")],"February has 28 days in a non-leap year.")
add(249,"Quadrant",["conditionals","coordinates"],"Line 1 contains integers x and y, neither both zero. Print Q1, Q2, Q3, Q4, X_AXIS, or Y_AXIS for the point's location.",["-1,000,000 <= x,y <= 1,000,000", "x and y are not both zero"],["Check axes before quadrants.","Positive x and y is Q1.","Follow signs clockwise for the other quadrants."],"O(1) time and O(1) space","""def solve():
    x,y=map(int,input().split())
    if y==0: print('X_AXIS')
    elif x==0: print('Y_AXIS')
    elif x>0 and y>0: print('Q1')
    elif x<0 and y>0: print('Q2')
    elif x<0: print('Q3')
    else: print('Q4')""",[("2 3\n","Q1"),("-2 3\n","Q2"),("0 -4\n","Y_AXIS"),("5 0\n","X_AXIS")],"Positive x and positive y is quadrant one.")
add(250,"Ticket price band",["conditionals"],"Line 1 contains age from 0 through 120. Print CHILD for under 13, TEEN for 13 through 17, ADULT for 18 through 64, otherwise SENIOR.",["0 <= age <= 120"],["Check the smallest upper bounds in order.","Age 13 starts TEEN.","Age 65 starts SENIOR."],"O(1) time and O(1) space","""def solve():
    a=int(input()); print('CHILD' if a<13 else 'TEEN' if a<18 else 'ADULT' if a<65 else 'SENIOR')""",[("12\n","CHILD"),("13\n","TEEN"),("18\n","ADULT"),("65\n","SENIOR")],"Twelve is below thirteen, so it is CHILD.")

# More text/list transformations.
add(251,"Unique character count",["strings","sets"],"Line 1 contains a string. Print how many different characters it contains. Spaces and case count as distinct characters.",["0 <= line length <= 10,000"],["A set keeps one copy of each value.","Do not lower-case the input.","len of the set is the count."],"O(n) time and O(n) space","""def solve():
    print(len(set(input().rstrip('\\n'))))""",[("banana\n","3"),("Aa\n","2"),("\n","0"),("a a\n","2")],"banana uses b, a, and n.")
add(252,"Count a word",["strings","lists"],"Line 1 contains a sentence of words separated by spaces. Line 2 contains one target word. Print how many sentence words exactly equal the target.",["Sentence length <= 10,000", "The target contains no spaces"],["split turns the sentence into words.","Compare whole words, not substrings.","Matching is case-sensitive."],"O(n) time and O(n) space","""def solve():
    words=input().split(); target=input().strip(); print(words.count(target))""",[("red blue red green\nred\n","2"),("one one one\ntwo\n","0"),("Hi hi Hi\nHi\n","2"),("\nx\n","0")],"The word red occurs twice.")
add(253,"Join words with hyphens",["strings","lists"],"Line 1 contains n. The next n lines each contain one word with no spaces. Print the words joined by hyphens.",["1 <= n <= 500", "Each word length <= 20"],["Read exactly n lines after line 1.","Store each word.","'-'.join combines them."],"O(total character count) time and space","""def solve():
    n=int(input()); print('-'.join(input().strip() for _ in range(n)))""",[("3\nred\ngreen\nblue\n","red-green-blue"),("1\nhello\n","hello"),("2\na\nb\n","a-b"),("4\n1\n2\n3\n4\n","1-2-3-4")],"The three words are separated by hyphens.")
add(254,"Remove spaces",["strings"],"Line 1 contains a string. Print it with every ordinary space removed; all other characters stay in order.",["0 <= line length <= 10,000"],["Read the complete line.","replace can change a space into an empty string.","Do not remove other whitespace characters."],"O(n) time and O(n) space","""def solve():
    print(input().rstrip('\\n').replace(' ',''))""",[("a b c\n","abc"),(" no spaces\n","nospaces"),("\n",""),("  a  \n","a")],"All three spaces are removed.")
add(255,"Replace commas",["strings"],"Line 1 contains a string. Print it with every comma replaced by a semicolon.",["0 <= line length <= 10,000"],["Use replace.","The first argument is a comma.","The second argument is a semicolon."],"O(n) time and O(n) space","""def solve():
    print(input().rstrip('\\n').replace(',',';'))""",[("a,b,c\n","a;b;c"),("hello\n","hello"),(",,\n",";;"),("one, two\n","one; two")],"Each comma becomes a semicolon.")
add(256,"Middle character",["strings","indexing"],"Line 1 contains a string with odd length. Print its middle character.",["1 <= odd line length <= 10,000"],["The middle index is len(s) // 2.","Odd length means there is exactly one middle character.","Remove only the newline."],"O(1) time and O(n) input space","""def solve():
    s=input().rstrip('\\n'); print(s[len(s)//2])""",[("abcde\n","c"),("x\n","x"),("hello\n","l"),("12345\n","3")],"The middle of abcde is c.")
add(257,"Starts with prefix",["strings","conditionals"],"Line 1 contains text. Line 2 contains a prefix. Print YES if text starts with prefix, otherwise NO. The prefix may be empty.",["Each line length <= 10,000"],["Python strings have startswith.","An empty prefix matches every text.","Matching is case-sensitive."],"O(prefix length) time and O(n) input space","""def solve():
    text=input().rstrip('\\n'); prefix=input().rstrip('\\n'); print('YES' if text.startswith(prefix) else 'NO')""",[("python\npy\n","YES"),("python\nthon\n","NO"),("abc\n\n","YES"),("Hello\nhe\n","NO")],"python begins with py.")
add(258,"Ends with suffix",["strings","conditionals"],"Line 1 contains text. Line 2 contains a suffix. Print YES if text ends with suffix, otherwise NO. The suffix may be empty.",["Each line length <= 10,000"],["Python strings have endswith.","An empty suffix matches every text.","Matching is case-sensitive."],"O(suffix length) time and O(n) input space","""def solve():
    text=input().rstrip('\\n'); suffix=input().rstrip('\\n'); print('YES' if text.endswith(suffix) else 'NO')""",[("python\non\n","YES"),("python\npy\n","NO"),("abc\n\n","YES"),("Hello\nLO\n","NO")],"python ends with on.")
add(259,"Find first character index",["strings","search"],"Line 1 contains text. Line 2 contains one character. Print its first zero-based index in text, or -1 if absent.",["Text length <= 10,000", "Line 2 contains exactly one character"],["str.find returns the first index.","It returns -1 when there is no match.","Indexes start at zero."],"O(n) time and O(n) input space","""def solve():
    print(input().rstrip('\\n').find(input().rstrip('\\n')))""",[("banana\nn\n","2"),("hello\nx\n","-1"),("abc\na\n","0"),("\nx\n","-1")],"The first n in banana is at index two.")
add(260,"Count distinct numbers",["lists","sets"],"Line 1 contains n. Line 2 contains n space-separated integers. Print how many distinct values occur.",["1 <= n <= 100,000"],["Convert the values to integers.","A set removes repeated values.","Its length is the answer."],"O(n) time and O(n) space","""def solve():
    n=int(input()); print(len(set(map(int,input().split()))))""",[("5\n1 2 1 3 2\n","3"),("1\n7\n","1"),("4\n0 0 0 0\n","1"),("3\n-1 0 1\n","3")],"The distinct values are one, two, and three.")

# Readable algorithmic mini-problems.
add(261,"Count values above a limit",["lists","loops"],"Line 1 contains n and limit k. Line 2 contains n integers. Print how many values are strictly greater than k.",["1 <= n <= 100,000", "All values and k fit signed 32-bit integers"],["Read n and k from line 1.","Compare every line-2 value with k.","Equal values do not count."],"O(n) time and O(n) input space","""def solve():
    n,k=map(int,input().split()); print(sum(x>k for x in map(int,input().split())))""",[("5 3\n1 4 3 5 2\n","2"),("3 0\n-1 0 1\n","1"),("1 7\n7\n","0"),("4 -2\n-1 -3 0 5\n","3")],"Only four and five are above three.")
add(262,"Running total",["lists","loops"],"Line 1 contains n. Line 2 contains n integers. Print the running totals after each value, separated by spaces.",["1 <= n <= 50,000"],["Start a total at zero.","Add one value at a time.","Save each new total before printing."],"O(n) time and O(n) space","""def solve():
    n=int(input()); total=0; out=[]
    for x in map(int,input().split()): total+=x; out.append(total)
    print(*out)""",[("4\n1 2 3 4\n","1 3 6 10"),("3\n-1 5 -2\n","-1 4 2"),("1\n7\n","7"),("4\n0 0 0 0\n","0 0 0 0")],"After each number, the total has grown.")
add(263,"Adjacent difference sum",["lists","loops","math"],"Line 1 contains n. Line 2 contains n integers. Print the sum of absolute differences between adjacent values. A one-value list has answer 0.",["1 <= n <= 100,000"],["Compare each value to the next one.","Use abs for a nonnegative difference.","There are n - 1 adjacent pairs."],"O(n) time and O(n) space","""def solve():
    n=int(input()); a=list(map(int,input().split())); print(sum(abs(a[i]-a[i-1]) for i in range(1,n)))""",[("4\n1 4 2 5\n","8"),("1\n7\n","0"),("3\n-1 -1 -1\n","0"),("3\n0 10 0\n","20")],"The differences are three, two, and three.")
add(264,"Is list nondecreasing",["lists","conditionals"],"Line 1 contains n. Line 2 contains n integers. Print YES if every value is at least the value before it, otherwise NO.",["1 <= n <= 100,000"],["Compare neighbouring pairs.","Equal neighbours are allowed.","any decreasing pair means NO."],"O(n) time and O(n) space","""def solve():
    n=int(input()); a=list(map(int,input().split())); print('YES' if all(a[i-1]<=a[i] for i in range(1,n)) else 'NO')""",[("4\n1 2 2 5\n","YES"),("3\n1 3 2\n","NO"),("1\n7\n","YES"),("3\n-3 -2 -1\n","YES")],"Each value is at least the value before it.")
add(265,"Swap first and last",["lists","indexing"],"Line 1 contains n. Line 2 contains n integers. Swap the first and last values, then print the list. If n is 1, it stays unchanged.",["1 <= n <= 1,200", "Each integer is between -1,000,000 and 1,000,000"],["Store the list.","Python can swap with a[0], a[-1] = a[-1], a[0].","Print the changed list."],"O(n) time and O(n) space","""def solve():
    n=int(input()); a=input().split(); a[0],a[-1]=a[-1],a[0]; print(*a)""",[("4\n1 2 3 4\n","4 2 3 1"),("1\n7\n","7"),("2\n-1 5\n","5 -1"),("3\n0 0 1\n","1 0 0")],"Only the outside values exchange places.")
add(266,"Rotate list left once",["lists","indexing"],"Line 1 contains n. Line 2 contains n integers. Move the first value to the end and print the result.",["1 <= n <= 100,000"],["Take the slice after the first value.","Then append the first value.","A one-value list is unchanged."],"O(n) time and O(n) space","""def solve():
    n=int(input()); a=input().split(); print(*(a[1:]+a[:1]))""",[("4\n1 2 3 4\n","2 3 4 1"),("1\n7\n","7"),("2\n-1 5\n","5 -1"),("3\n0 0 1\n","0 1 0")],"One moves from the front to the end.")
add(267,"Find list value",["lists","search"],"Line 1 contains n. Line 2 contains n integers. Line 3 contains target t. Print the first zero-based index of t, or -1 if absent.",["1 <= n <= 100,000"],["Read the target from line 3.","list.index finds the first match.","Check membership first to avoid an error."],"O(n) time and O(n) space","""def solve():
    n=int(input()); a=list(map(int,input().split())); t=int(input()); print(a.index(t) if t in a else -1)""",[("4\n5 2 5 1\n5\n","0"),("3\n1 2 3\n4\n","-1"),("1\n7\n7\n","0"),("4\n0 0 2 0\n2\n","2")],"The first five is at zero-based index zero.")
add(268,"Count list target",["lists","search"],"Line 1 contains n. Line 2 contains n integers. Line 3 contains target t. Print how many times t occurs.",["1 <= n <= 100,000"],["Read the target after the list.","list.count counts matching entries.","An absent target gives zero."],"O(n) time and O(n) space","""def solve():
    n=int(input()); a=list(map(int,input().split())); print(a.count(int(input())))""",[("4\n5 2 5 1\n5\n","2"),("3\n1 2 3\n4\n","0"),("1\n7\n7\n","1"),("4\n0 0 2 0\n0\n","3")],"Five appears twice.")
add(269,"Range width",["lists","math"],"Line 1 contains n. Line 2 contains n integers. Print largest value minus smallest value.",["1 <= n <= 100,000"],["Find max and min.","Subtract min from max.","Equal values give zero."],"O(n) time and O(n) space","""def solve():
    n=int(input()); a=list(map(int,input().split())); print(max(a)-min(a))""",[("4\n1 9 3 2\n","8"),("3\n-5 -2 -8\n","6"),("1\n7\n","0"),("3\n0 0 0\n","0")],"Nine minus one is eight.")
add(270,"Largest absolute list value",["lists","math"],"Line 1 contains n. Line 2 contains n integers. Print the value whose absolute value is largest. If tied, print the smaller actual value.",["1 <= n <= 100,000"],["Compare using abs.","A tuple key can include abs(value) and -value.","The tie rule prefers -5 over 5."],"O(n) time and O(n) space","""def solve():
    n=int(input()); print(max(map(int,input().split()),key=lambda x:(abs(x),-x)))""",[("4\n1 -9 3 2\n","-9"),("3\n5 -5 2\n","-5"),("1\n0\n","0"),("3\n-2 7 -6\n","7")],"Negative nine has the greatest absolute value.")

# Small simulations and number theory.
add(271,"Count multiples in a range",["loops","math"],"Line 1 contains positive integers n and k. Print how many integers from 1 through n are multiples of k.",["1 <= n,k <= 1,000,000"],["Every kth number is a multiple.","Use floor division n // k.","No iteration is needed."],"O(1) time and O(1) space","""def solve():
    n,k=map(int,input().split()); print(n//k)""",[("10 3\n","3"),("5 1\n","5"),("4 9\n","0"),("100 10\n","10")],"Three, six, and nine are multiples of three up to ten.")
add(272,"Greatest common divisor",["math","loops"],"Line 1 contains two positive integers a and b. Print their greatest common divisor.",["1 <= a,b <= 10^12"],["Use the Euclidean algorithm.","Repeatedly replace a,b with b,a%b.","When b is zero, a is the answer."],"O(log(min(a,b))) time and O(1) space","""def solve():
    a,b=map(int,input().split())
    while b: a,b=b,a%b
    print(a)""",[("12 18\n","6"),("7 13\n","1"),("100 25\n","25"),("42 56\n","14")],"Six divides both twelve and eighteen.")
add(273,"Least common multiple",["math","loops"],"Line 1 contains two positive integers a and b. Print their least common multiple.",["1 <= a,b <= 1,000,000"],["Find the gcd first.","lcm is a * b // gcd.","Divide before or after multiplication safely at this bound."],"O(log(min(a,b))) time and O(1) space","""def solve():
    a,b=map(int,input().split()); x,y=a,b
    while y: x,y=y,x%y
    print(a//x*b)""",[("12 18\n","36"),("7 13\n","91"),("4 6\n","12"),("1 9\n","9")],"Thirty-six is the first shared multiple of twelve and eighteen.")
add(274,"Prime check",["math","loops"],"Line 1 contains positive integer n. Print YES if n is prime, otherwise NO.",["1 <= n <= 1,000,000"],["One is not prime.","Try divisors from two upward.","You only need to test while divisor squared is at most n."],"O(sqrt(n)) time and O(1) space","""def solve():
    n=int(input()); d=2
    while d*d<=n:
        if n%d==0: print('NO'); return
        d+=1
    print('YES' if n>1 else 'NO')""",[("2\n","YES"),("1\n","NO"),("49\n","NO"),("97\n","YES")],"Two has exactly two positive divisors.")
add(275,"Next multiple",["math","division"],"Line 1 contains integers n and k, where k is positive. Print the smallest multiple of k that is at least n.",["0 <= n <= 1,000,000", "1 <= k <= 1,000,000"],["Use ceiling division.","(n + k - 1) // k rounds up.","Multiply that count by k."],"O(1) time and O(1) space","""def solve():
    n,k=map(int,input().split()); print((n+k-1)//k*k)""",[("12 5\n","15"),("10 5\n","10"),("0 7\n","0"),("1 3\n","3")],"Fifteen is the next multiple of five after twelve.")
add(276,"Seconds to clock time",["math","formatting"],"Line 1 contains nonnegative seconds s less than 86,400. Print whole hours, minutes, and seconds as H M S separated by spaces.",["0 <= s < 86,400"],["There are 3600 seconds in an hour.","Use divmod twice.","Print the three whole-number parts."],"O(1) time and O(1) space","""def solve():
    s=int(input()); h,s=divmod(s,3600); m,s=divmod(s,60); print(h,m,s)""",[("3661\n","1 1 1"),("0\n","0 0 0"),("59\n","0 0 59"),("86399\n","23 59 59")],"3661 seconds is one hour, one minute, one second.")
add(277,"Rectangle area and perimeter",["math"],"Line 1 contains positive integer width w and height h. Print area then perimeter, separated by one space.",["1 <= w,h <= 1,000,000"],["Area is width times height.","Perimeter is twice width plus height.","Print area first."],"O(1) time and O(1) space","""def solve():
    w,h=map(int,input().split()); print(w*h,2*(w+h))""",[("3 4\n","12 14"),("1 1\n","1 4"),("10 2\n","20 24"),("5 7\n","35 24")],"A three by four rectangle has area twelve and perimeter fourteen.")
add(278,"Count decimal zeros",["strings","loops"],"Line 1 contains a nonnegative integer n with no leading zeros unless n is zero. Print the number of zero digits it contains.",["0 <= n <= 10^18"],["Read the number as text.","Use count('0').","The number zero itself contains one zero digit."],"O(d) time and O(d) input space","""def solve():
    print(input().strip().count('0'))""",[("10020\n","3"),("0\n","1"),("123\n","0"),("9090\n","2")],"10020 has three zero digits.")
add(279,"Binary digit count",["math","strings"],"Line 1 contains nonnegative integer n. Print how many binary digits are in its base-two representation. Zero has one binary digit.",["0 <= n <= 10^18"],["bin(n) produces text beginning with 0b.","Remove those first two characters.","Count what remains."],"O(log n) time and O(log n) space","""def solve():
    print(len(bin(int(input())))-2)""",[("8\n","4"),("0\n","1"),("1\n","1"),("15\n","4")],"Eight is 1000 in binary, which has four digits.")
add(280,"Power of two check",["math","bitwise"],"Line 1 contains nonnegative integer n. Print YES if n is a power of two, otherwise NO. One is a power of two; zero is not.",["0 <= n <= 2^60"],["Powers of two have one set bit.","For positive n, n & (n - 1) is zero exactly then.","Check positivity too."],"O(1) time and O(1) space","""def solve():
    n=int(input()); print('YES' if n>0 and n&(n-1)==0 else 'NO')""",[("8\n","YES"),("0\n","NO"),("1\n","YES"),("12\n","NO")],"Eight is two cubed.")

# Final everyday-data drills.
add(281,"Count lowercase letters",["strings","loops"],"Line 1 contains a string. Print how many characters are lowercase English letters a through z.",["0 <= line length <= 10,000"],["isalpha alone would include non-English letters.","Use 'a' <= c <= 'z'.","Uppercase letters do not count."],"O(n) time and O(n) input space","""def solve():
    print(sum('a'<=c<='z' for c in input().rstrip('\\n')))""",[("Hello, world!\n","9"),("ABC123\n","0"),("aZz\n","2"),("\n","0")],"The lowercase letters are ello and world.")
add(282,"Count uppercase letters",["strings","loops"],"Line 1 contains a string. Print how many characters are uppercase English letters A through Z.",["0 <= line length <= 10,000"],["Use 'A' <= c <= 'Z'.","Lowercase letters do not count.","Check every character."],"O(n) time and O(n) input space","""def solve():
    print(sum('A'<=c<='Z' for c in input().rstrip('\\n')))""",[("Hello, WORLD!\n","6"),("abc123\n","0"),("aZz\n","1"),("\n","0")],"H and WORLD make six uppercase letters.")
add(283,"Count digits in text",["strings","loops"],"Line 1 contains a string. Print how many characters are decimal digits 0 through 9.",["0 <= line length <= 10,000"],["Use '0' <= c <= '9'.","Count every matching character.","Letters and spaces do not count."],"O(n) time and O(n) input space","""def solve():
    print(sum('0'<=c<='9' for c in input().rstrip('\\n')))""",[("room 101\n","3"),("abc\n","0"),("0a2b4\n","3"),("\n","0")],"101 contributes three digit characters.")
add(284,"Sum squares",["lists","math"],"Line 1 contains n. Line 2 contains n integers. Print the sum of their squares.",["1 <= n <= 100,000", "Each integer is between -10,000 and 10,000"],["Square each x with x*x.","Then add the squares.","Negative values become positive when squared."],"O(n) time and O(n) input space","""def solve():
    n=int(input()); print(sum(x*x for x in map(int,input().split())))""",[("3\n1 2 3\n","14"),("2\n-2 3\n","13"),("1\n0\n","0"),("4\n1 -1 1 -1\n","4")],"One squared plus two squared plus three squared is fourteen.")
add(285,"Count changes",["lists","loops"],"Line 1 contains n. Line 2 contains n integers. Print the number of times a value differs from the value immediately before it.",["1 <= n <= 100,000"],["The first value cannot be a change.","Compare each index i with i-1.","Count unequal adjacent pairs."],"O(n) time and O(n) space","""def solve():
    n=int(input()); a=list(map(int,input().split())); print(sum(a[i]!=a[i-1] for i in range(1,n)))""",[("5\n1 1 2 2 3\n","2"),("1\n7\n","0"),("4\n1 2 3 4\n","3"),("3\n0 0 0\n","0")],"The list changes from one to two and two to three.")
add(286,"Pairwise smaller value",["lists","conditionals"],"Line 1 contains n. Line 2 contains n integers a. Line 3 contains n integers b. Print min(a[i], b[i]) for each position, separated by spaces.",["1 <= n <= 100,000"],["Read both lists after n.","Zip pairs from the same position.","Take min for each pair."],"O(n) time and O(n) space","""def solve():
    n=int(input()); a=list(map(int,input().split())); b=list(map(int,input().split())); print(*[min(x,y) for x,y in zip(a,b)])""",[("3\n1 5 3\n2 4 3\n","1 4 3"),("1\n7\n2\n","2"),("3\n-1 0 8\n-2 1 7\n","-2 0 7"),("2\n0 0\n0 1\n","0 0")],"At each position, choose the smaller number.")
add(287,"Zip list sums",["lists","loops"],"Line 1 contains n. Line 2 contains n integers a. Line 3 contains n integers b. Print a[i] + b[i] for each position, separated by spaces.",["1 <= n <= 100,000"],["Read both lists after n.","Zip matching positions.","Add each pair."],"O(n) time and O(n) space","""def solve():
    n=int(input()); a=list(map(int,input().split())); b=list(map(int,input().split())); print(*[x+y for x,y in zip(a,b)])""",[("3\n1 5 3\n2 4 3\n","3 9 6"),("1\n7\n2\n","9"),("3\n-1 0 8\n-2 1 7\n","-3 1 15"),("2\n0 0\n0 1\n","0 1")],"Add the two values at each matching position.")
add(288,"Check all values positive",["lists","conditionals"],"Line 1 contains n. Line 2 contains n integers. Print YES if every value is greater than zero, otherwise NO.",["1 <= n <= 100,000"],["Use all on a condition for each value.","Zero is not positive.","One failing value means NO."],"O(n) time and O(n) input space","""def solve():
    n=int(input()); print('YES' if all(x>0 for x in map(int,input().split())) else 'NO')""",[("3\n1 2 3\n","YES"),("3\n1 0 3\n","NO"),("1\n-1\n","NO"),("2\n5 6\n","YES")],"Every value in the first list is above zero.")

def revise(num, title, topics, description, constraints, hints, complexity, body, cases, explanation):
    """Replace an early draft with a semantically distinct beginner drill."""
    records = [{"input": source, "expected_output": result} for source, result in cases]
    ITEMS[num - 201].update({"title": title, "topics": topics, "description": description,
        "constraints": constraints, "hints": hints, "expected_complexity": complexity,
        "solution": "import sys\n" + body.strip() + "\n\nif __name__ == '__main__':\n    solve()\n",
        "examples": [{"input": records[0]["input"], "output": records[0]["expected_output"], "explanation": explanation}],
        "public_tests": records[:2], "hidden_tests": records[2:]})


# These replacements intentionally avoid contracts already taught in the core bank.
revise(206,"Distance between two values",["math"],"Line 1 contains integers a and b. Print the nonnegative distance between them.",["-1,000,000 <= a,b <= 1,000,000"],["Subtract one value from the other.","Use abs to make the distance nonnegative.","The input order does not change the answer."],"O(1) time and O(1) space","""def solve():
    a,b=map(int,input().split()); print(abs(a-b))""",[("3 10\n","7"),("-4 5\n","9"),("7 7\n","0"),("0 -2\n","2")],"The distance from three to ten is seven.")
revise(210,"Minutes to seconds",["math"],"Line 1 contains a nonnegative whole number of minutes. Print the equivalent number of seconds.",["0 <= minutes <= 1,000,000"],["There are 60 seconds in one minute.","Multiply minutes by 60.","Zero minutes gives zero seconds."],"O(1) time and O(1) space","""def solve():
    print(int(input())*60)""",[("2\n","120"),("0\n","0"),("15\n","900"),("1\n","60")],"Two minutes contain 120 seconds.")
revise(211,"Square sum to n",["math","loops"],"Line 1 contains positive integer n. Print 1 squared plus 2 squared through n squared.",["1 <= n <= 1,000,000"],["There is a formula for this series.","Use n*(n+1)*(2*n+1)//6.","The integer division is exact."],"O(1) time and O(1) space","""def solve():
    n=int(input()); print(n*(n+1)*(2*n+1)//6)""",[("3\n","14"),("1\n","1"),("5\n","55"),("10\n","385")],"One plus four plus nine is fourteen.")
revise(215,"Hundreds digit",["math","division"],"Line 1 contains a three-digit positive integer n. Print its hundreds digit.",["100 <= n <= 999"],["The hundreds digit is at the left.","Floor-divide by 100.","The result is one digit."],"O(1) time and O(1) space","""def solve():
    print(int(input())//100)""",[("507\n","5"),("100\n","1"),("999\n","9"),("320\n","3")],"507 has five hundreds.")
revise(216,"First decimal digit",["strings"],"Line 1 contains a nonnegative integer with no leading zeros unless it is zero. Print its first decimal digit.",["0 <= n <= 10^18"],["Read the number as text.","The first character has index zero.","Zero is itself its first digit."],"O(1) time and O(d) input space","""def solve():
    print(input().strip()[0])""",[("507\n","5"),("0\n","0"),("999\n","9"),("42\n","4")],"The first digit of 507 is five.")
revise(217,"Count even digits",["strings","loops"],"Line 1 contains a nonnegative integer n. Print how many of its decimal digits are even.",["0 <= n <= 10^18"],["Read the number as a string.","Convert each character to an integer.","Zero is an even digit."],"O(d) time and O(d) input space","""def solve():
    print(sum(int(c)%2==0 for c in input().strip()))""",[("5072\n","2"),("0\n","1"),("135\n","0"),("2468\n","4")],"Zero and two are even digits in 5072.")
revise(218,"Last two digits",["math","division"],"Line 1 contains nonnegative integer n. Print its last two decimal digits as a number, so a leading zero is not printed.",["0 <= n <= 10^18"],["Remainder by 100 keeps the last two digits.","The answer is a number, not padded text.","For 7, the answer is 7."],"O(1) time and O(1) space","""def solve():
    print(int(input())%100)""",[("1205\n","5"),("0\n","0"),("987\n","87"),("42\n","42")],"1205 ends with 05, printed as five.")
revise(219,"Count zero list values",["lists","loops"],"You receive n numbers: n is on line 1 and the numbers are on line 2. Return the number of entries equal to zero.",["1 <= n <= 100,000"],["Read the values from line 2.","Check x == 0.","Count every matching value."],"O(n) time and O(n) input space","""def solve():
    n=int(input()); print(sum(x==0 for x in map(int,input().split())))""",[("5\n-2 0 4 0 -1\n","2"),("1\n0\n","1"),("4\n1 2 3 4\n","0"),("3\n0 0 0\n","3")],"Two values in the first list are zero.")
revise(220,"List product parity",["lists","math"],"Line 1 contains n. Line 2 contains n integers. Print EVEN if their product is even, otherwise print ODD.",["1 <= n <= 100,000"],["A product is even when any factor is even.","You do not need to multiply large values.","If all values are odd, the product is odd."],"O(n) time and O(n) input space","""def solve():
    n=int(input()); print('EVEN' if any(x%2==0 for x in map(int,input().split())) else 'ODD')""",[("3\n2 3 5\n","EVEN"),("3\n1 3 5\n","ODD"),("1\n0\n","EVEN"),("2\n-1 -7\n","ODD")],"The factor two makes the product even.")
revise(226,"Count consonants",["strings","loops"],"Line 1 contains letters and spaces only. Print how many English letters are consonants, ignoring case.",["0 <= line length <= 10,000"],["Make the text lowercase.","A consonant is a letter not in aeiou.","Spaces do not count."],"O(n) time and O(n) space","""def solve():
    s=input().rstrip('\\n').lower(); print(sum('a'<=c<='z' and c not in 'aeiou' for c in s))""",[("Beautiful\n","4"),("AEIOU\n","0"),("b c d\n","3"),("\n","0")],"Beautiful has four consonants.")
revise(227,"All text lowercase",["strings","conditionals"],"Line 1 contains a nonempty string of English letters. Print YES if every letter is lowercase, otherwise NO.",["1 <= line length <= 10,000"],["Compare the text with text.lower().","Uppercase letters change under lower().","The input contains letters only."],"O(n) time and O(n) space","""def solve():
    s=input().strip(); print('YES' if s==s.lower() else 'NO')""",[("python\n","YES"),("Python\n","NO"),("abcXYZ\n","NO"),("z\n","YES")],"python already uses only lowercase letters.")
revise(231,"Sum of negative values",["lists","loops"],"Line 1 contains n. Line 2 contains n integers. Print the sum of only the negative values.",["1 <= n <= 100,000"],["Test every value with x < 0.","Ignore zero and positives.","The answer can be zero."],"O(n) time and O(n) input space","""def solve():
    n=int(input()); print(sum(x for x in map(int,input().split()) if x<0))""",[("4\n-2 5 -1 0\n","-3"),("3\n1 2 3\n","0"),("1\n-7\n","-7"),("3\n-1 -2 -3\n","-6")],"Negative two plus negative one is negative three.")
revise(232,"Largest even list value",["lists","conditionals"],"Line 1 contains n. Line 2 contains n integers and includes at least one even value. Print the largest even value.",["1 <= n <= 100,000"],["Keep only values with remainder zero by two.","Then find their maximum.","The constraint guarantees a result."],"O(n) time and O(n) space","""def solve():
    n=int(input()); print(max(x for x in map(int,input().split()) if x%2==0))""",[("4\n1 8 3 6\n","8"),("3\n-2 -8 5\n","-2"),("1\n0\n","0"),("4\n2 2 1 2\n","2")],"Eight is the largest even value.")
revise(233,"Smallest odd list value",["lists","conditionals"],"Line 1 contains n. Line 2 contains n integers and includes at least one odd value. Print the smallest odd value.",["1 <= n <= 100,000"],["Keep only odd values.","Odd values have nonzero remainder by two.","Then find their minimum."],"O(n) time and O(n) space","""def solve():
    n=int(input()); print(min(x for x in map(int,input().split()) if x%2))""",[("4\n1 8 3 6\n","1"),("3\n-2 -7 5\n","-7"),("1\n9\n","9"),("4\n2 2 1 3\n","1")],"One is the smallest odd value.")
revise(234,"Count odd list values",["lists","loops"],"Given a sequence length on line 1 and its values on line 2, report the number of odd entries.",["1 <= n <= 100,000"],["Odd values have nonzero remainder by two.","Negative odd values count too.","Zero is even."],"O(n) time and O(n) input space","""def solve():
    n=int(input()); print(sum(x%2!=0 for x in map(int,input().split())))""",[("5\n1 2 3 4 5\n","3"),("3\n-2 0 7\n","1"),("1\n8\n","0"),("4\n1 3 5 7\n","4")],"One, three, and five are odd.")
revise(235,"Middle list value",["lists","indexing"],"An odd-sized sequence is supplied as its length on line 1 followed by the values on line 2. Output the central entry.",["1 <= n <= 100,000", "n is odd"],["The middle index is n // 2.","Indexes start at zero.","Odd n gives one middle position."],"O(n) time and O(n) space","""def solve():
    n=int(input()); a=input().split(); print(a[n//2])""",[("5\n1 2 3 4 5\n","3"),("1\n7\n","7"),("3\n-1 0 2\n","0"),("3\n9 8 7\n","8")],"Index two is the middle of five values.")
revise(236,"Every other list value",["lists","indexing"],"Line 1 contains n. Line 2 contains n integers. Print values at zero-based indexes 0, 2, 4, and so on, separated by spaces.",["1 <= n <= 1,200", "Each integer is between -1,000,000 and 1,000,000"],["Python slices can step by two.","Start at index zero.","Print the selected values in original order."],"O(n) time and O(n) space","""def solve():
    n=int(input()); print(*input().split()[::2])""",[("5\n1 2 3 4 5\n","1 3 5"),("1\n7\n","7"),("4\n-1 0 2 9\n","-1 2"),("2\n5 5\n","5")],"Indexes zero, two, and four hold one, three, and five.")
revise(237,"Sort by absolute value",["lists","sorting"],"Line 1 contains n. Line 2 contains n integers. Print them ordered by increasing absolute value; ties use the smaller actual value first.",["1 <= n <= 1,200", "Each integer is between -1,000,000 and 1,000,000"],["Use sorted with a key.","The key should include abs(x).","Add x as the tie-breaker."],"O(n log n) time and O(n) space","""def solve():
    n=int(input()); print(*sorted(map(int,input().split()),key=lambda x:(abs(x),x)))""",[("4\n3 -1 2 -2\n","-1 -2 2 3"),("3\n5 -5 0\n","0 -5 5"),("1\n7\n","7"),("4\n-3 -2 -1 0\n","0 -1 -2 -3")],"Negative two comes before positive two when absolute values tie.")
revise(238,"Second smallest distinct",["lists","sorting"],"Line 1 contains n. Line 2 contains n integers. At least two distinct values occur. Print the second-smallest distinct value.",["2 <= n <= 100,000", "At least two different values are present"],["A set removes duplicates.","Sort the distinct values.","Index one is the second-smallest."],"O(n log n) time and O(n) space","""def solve():
    n=int(input()); print(sorted(set(map(int,input().split())))[1])""",[("4\n1 9 3 2\n","2"),("4\n5 5 4 4\n","5"),("3\n-1 -2 -3\n","-2"),("2\n0 1\n","1")],"After one, two is the next distinct smallest value.")
revise(240,"First half list sum",["lists","loops"],"Line 1 contains even integer n. Line 2 contains n integers. Print the sum of the first n // 2 values.",["2 <= n <= 100,000", "n is even"],["The first half ends before index n//2.","Slice the list with [:n//2].","Then sum that slice."],"O(n) time and O(n) space","""def solve():
    n=int(input()); a=list(map(int,input().split())); print(sum(a[:n//2]))""",[("4\n2 4 6 8\n","6"),("2\n-3 3\n","-3"),("6\n1 2 3 4 5 6\n","6"),("2\n7 9\n","7")],"The first half contains two and four.")
revise(241,"Compare two integers",["conditionals"],"Line 1 contains integers a and b. Print LESS if a < b, EQUAL if a == b, otherwise GREATER.",["-1,000,000 <= a,b <= 1,000,000"],["Compare a and b.","Check less-than first.","The remaining possibilities are equal or greater."],"O(1) time and O(1) space","""def solve():
    a,b=map(int,input().split()); print('LESS' if a<b else 'EQUAL' if a==b else 'GREATER')""",[("3 7\n","LESS"),("5 5\n","EQUAL"),("9 -1\n","GREATER"),("-2 0\n","LESS")],"Three is less than seven.")
revise(242,"Century number",["math","division"],"Line 1 contains a positive year. Print its century number: years 1 through 100 are century 1, 101 through 200 are century 2, and so on.",["1 <= year <= 9999"],["Years exactly divisible by 100 stay in that century.","Use (year - 1) // 100 + 1.","Subtract one before floor division."],"O(1) time and O(1) space","""def solve():
    print((int(input())-1)//100+1)""",[("2024\n","21"),("1900\n","19"),("2000\n","20"),("1\n","1")],"2024 is in the twenty-first century.")
revise(247,"Points needed to pass",["conditionals","math"],"Line 1 contains a score from 0 through 100. A passing score is 50. Print how many more points are needed to pass, or 0 if already passing.",["0 <= score <= 100"],["Compare the score with 50.","Scores at least 50 need zero points.","Otherwise subtract score from 50."],"O(1) time and O(1) space","""def solve():
    print(max(0,50-int(input())))""",[("91\n","0"),("49\n","1"),("0\n","50"),("50\n","0")],"A score of 49 needs one more point.")
revise(249,"Closer coordinate axis",["conditionals","coordinates"],"Line 1 contains integers x and y. Print X if the point is closer to the x-axis, Y if closer to the y-axis, or TIE if equally close.",["-1,000,000 <= x,y <= 1,000,000"],["Distance to the x-axis is abs(y).","Distance to the y-axis is abs(x).","Compare those two distances."],"O(1) time and O(1) space","""def solve():
    x,y=map(int,input().split()); print('X' if abs(y)<abs(x) else 'Y' if abs(x)<abs(y) else 'TIE')""",[("2 3\n","Y"),("-2 3\n","Y"),("0 -4\n","Y"),("5 5\n","TIE")],"The point (2, 3) is two units from the y-axis and three from the x-axis.")
revise(260,"Count repeated values",["lists","sets"],"Line 1 contains n. Line 2 contains n integers. Print how many distinct values occur at least twice.",["1 <= n <= 100,000"],["Count each value's frequency.","Only values with frequency at least two count.","Count each repeated value once."],"O(n) time and O(n) space","""def solve():
    from collections import Counter
    n=int(input()); print(sum(v>=2 for v in Counter(map(int,input().split())).values()))""",[("5\n1 2 1 3 2\n","2"),("1\n7\n","0"),("4\n0 0 0 0\n","1"),("3\n-1 0 1\n","0")],"One and two each occur at least twice.")
revise(261,"First value above a limit",["lists","search"],"Line 1 contains n and limit k. Line 2 contains n integers. Print the first zero-based index holding a value greater than k, or -1 if none does.",["1 <= n <= 100,000"],["Scan from left to right.","Stop at the first x > k.","If the scan ends, print -1."],"O(n) time and O(n) space","""def solve():
    n,k=map(int,input().split()); a=list(map(int,input().split())); print(next((i for i,x in enumerate(a) if x>k),-1))""",[("5 3\n1 4 3 5 2\n","1"),("3 0\n-1 0 1\n","2"),("1 7\n7\n","-1"),("4 -2\n-1 -3 0 5\n","0")],"Four at index one is the first value above three.")
revise(262,"Prefix maximums",["lists","loops"],"The first line gives a sequence length and the next line gives its integers. For every position, output the greatest entry encountered from the start through that position, separated by spaces.",["1 <= n <= 1,200", "Each integer is between -1,000,000 and 1,000,000"],["Keep a current maximum.","Update it with each new value.","Append the current maximum after every step."],"O(n) time and O(n) space","""def solve():
    n=int(input()); best=None; out=[]
    for x in map(int,input().split()): best=x if best is None else max(best,x); out.append(best)
    print(*out)""",[("4\n1 3 2 4\n","1 3 3 4"),("3\n-1 -5 -2\n","-1 -1 -1"),("1\n7\n","7"),("4\n0 0 0 0\n","0 0 0 0")],"After two, the largest value seen is still three.")
revise(263,"Adjacent equal pair count",["lists","loops"],"Line 1 contains n. Line 2 contains n integers. Print how many adjacent pairs have equal values. A one-value list has answer 0.",["1 <= n <= 100,000"],["Compare each value to the one before it.","Count pairs where they are equal.","Overlapping pairs count separately."],"O(n) time and O(n) space","""def solve():
    n=int(input()); a=list(map(int,input().split())); print(sum(a[i]==a[i-1] for i in range(1,n)))""",[("5\n1 1 2 2 2\n","3"),("1\n7\n","0"),("4\n1 2 3 4\n","0"),("3\n0 0 0\n","2")],"There is one equal pair of ones and two equal pairs of twos.")
revise(264,"Is list constant",["lists","conditionals"],"Line 1 contains n. Line 2 contains n integers. Print YES if all values are equal, otherwise NO.",["1 <= n <= 100,000"],["Compare every value with the first one.","A one-value list is constant.","One different value means NO."],"O(n) time and O(n) space","""def solve():
    n=int(input()); a=input().split(); print('YES' if all(x==a[0] for x in a) else 'NO')""",[("4\n1 1 1 1\n","YES"),("3\n1 1 2\n","NO"),("1\n7\n","YES"),("3\n0 0 0\n","YES")],"Every value in the first list is one.")
revise(266,"Swap list halves",["lists","slicing"],"Line 1 contains even integer n. Line 2 contains n integers. Print the second half followed by the first half.",["2 <= n <= 1,200", "n is even", "Each integer is between -1,000,000 and 1,000,000"],["Find the halfway index n//2.","Slice the second half and first half.","Join the slices in that order."],"O(n) time and O(n) space","""def solve():
    n=int(input()); a=input().split(); m=n//2; print(*(a[m:]+a[:m]))""",[("4\n1 2 3 4\n","3 4 1 2"),("2\n7 8\n","8 7"),("6\n-1 0 2 3 4 5\n","3 4 5 -1 0 2"),("2\n0 0\n","0 0")],"The second half, three and four, moves in front.")
revise(268,"Last list target index",["lists","search"],"Line 1 contains n. Line 2 contains n integers. Line 3 contains target t. Print the last zero-based index of t, or -1 if absent.",["1 <= n <= 100,000"],["Search the list from the end.","A reversed loop visits the last occurrence first.","Print -1 if no item matches."],"O(n) time and O(n) space","""def solve():
    n=int(input()); a=list(map(int,input().split())); t=int(input()); print(next((i for i in range(n-1,-1,-1) if a[i]==t),-1))""",[("4\n5 2 5 1\n5\n","2"),("3\n1 2 3\n4\n","-1"),("1\n7\n7\n","0"),("4\n0 0 2 0\n0\n","3")],"The last five is at index two.")
revise(269,"Middle range sum",["lists","loops"],"Line 1 contains n at least 3. Line 2 contains n integers. Print the sum after removing the first and last values.",["3 <= n <= 100,000"],["The middle values are slice [1:-1].","The endpoints are not included.","Sum the remaining slice."],"O(n) time and O(n) space","""def solve():
    n=int(input()); a=list(map(int,input().split())); print(sum(a[1:-1]))""",[("4\n1 9 3 2\n","12"),("3\n-5 -2 -8\n","-2"),("3\n7 0 7\n","0"),("5\n1 2 3 4 5\n","9")],"Only nine and three remain after the endpoints are removed.")
revise(271,"Sum multiples of k",["loops","math"],"Line 1 contains positive integers n and k. Print the sum of multiples of k from 1 through n.",["1 <= n,k <= 1,000,000"],["There are n//k multiples.","Their sum is k times 1+2+...+count.","Use the arithmetic-series formula."],"O(1) time and O(1) space","""def solve():
    n,k=map(int,input().split()); c=n//k; print(k*c*(c+1)//2)""",[("10 3\n","18"),("5 1\n","15"),("4 9\n","0"),("100 10\n","550")],"Three plus six plus nine is eighteen.")
revise(274,"Smallest divisor above one",["math","loops"],"Line 1 contains composite integer n. Print its smallest divisor greater than one.",["4 <= n <= 1,000,000", "n is composite"],["Try divisors from two upward.","The first divisor found is the smallest.","The composite constraint guarantees one exists."],"O(sqrt(n)) time and O(1) space","""def solve():
    n=int(input()); d=2
    while n%d: d+=1
    print(d)""",[("12\n","2"),("49\n","7"),("91\n","7"),("25\n","5")],"Two is the smallest divisor of twelve above one.")
revise(276,"Clock time to seconds",["math","formatting"],"Line 1 contains whole hours h, minutes m, and seconds s for one day. Print the total number of seconds.",["0 <= h <= 23", "0 <= m,s <= 59"],["Hours contribute 3600 seconds each.","Minutes contribute 60 seconds each.","Add all three contributions."],"O(1) time and O(1) space","""def solve():
    h,m,s=map(int,input().split()); print(h*3600+m*60+s)""",[("1 1 1\n","3661"),("0 0 0\n","0"),("0 0 59\n","59"),("23 59 59\n","86399")],"One hour, one minute, and one second is 3661 seconds.")
revise(280,"Odd binary one count",["math","bitwise"],"Line 1 contains nonnegative integer n. Print YES if its binary representation has an odd number of 1 bits, otherwise NO.",["0 <= n <= 2^60"],["Convert with bin or repeatedly inspect bits.","Count the 1 characters.","Test whether that count is odd."],"O(log n) time and O(log n) space","""def solve():
    print('YES' if bin(int(input())).count('1')%2 else 'NO')""",[("8\n","YES"),("0\n","NO"),("3\n","NO"),("7\n","YES")],"Eight is 1000, containing one 1 bit.")
revise(209,"Opposite signs",["conditionals","math"],"Line 1 contains two nonzero integers a and b. Print YES exactly when one is positive and the other is negative, otherwise print NO.",["-1,000,000 <= a,b <= 1,000,000", "a and b are nonzero"],["Numbers have opposite signs when their product is negative.","You can compare one number with zero at a time.","Print exactly YES or NO."],"O(1) time and O(1) space","""def solve():
    a,b=map(int,input().split()); print('YES' if a*b<0 else 'NO')""",[("3 -7\n","YES"),("-2 -5\n","NO"),("1 9\n","NO"),("-1 4\n","YES")],"Three and negative seven have opposite signs.")
revise(275,"Ceiling group count",["math","division"],"Line 1 contains a nonnegative item count n and positive capacity k. Print the minimum number of groups needed when each group holds at most k items.",["0 <= n <= 1,000,000", "1 <= k <= 1,000,000"],["A partially filled final group still counts.","Add k minus one before floor division.","Zero items need zero groups."],"O(1) time and O(1) space","""def solve():
    n,k=map(int,input().split()); print((n+k-1)//k)""",[("10 3\n","4"),("0 5\n","0"),("9 3\n","3"),("1 100\n","1")],"Ten items need four groups of capacity three.")
revise(284,"Sum list cubes",["lists","math"],"A count appears on the first line and the matching integer sequence on the next. Cube each entry and report the total.",["1 <= n <= 100,000", "Each integer is between -10,000 and 10,000"],["Cube x with x*x*x.","Add every cube.","Negative cubes remain negative."],"O(n) time and O(n) input space","""def solve():
    n=int(input()); print(sum(x*x*x for x in map(int,input().split())))""",[("3\n1 2 3\n","36"),("2\n-2 3\n","19"),("1\n0\n","0"),("4\n1 -1 1 -1\n","0")],"One cubed plus two cubed plus three cubed is 36.")


def revise_class(num, title, topics, description, constraints, hints, complexity, starter, solution, cases, explanation, required_class):
    """Replace a script drill with a beginner class contract and private judge harnesses."""
    records = [{"input": source, "expected_output": result, "harness": harness}
               for source, result, harness in cases]
    # Keep Run useful for learners: they get the same small stdin driver as the
    # reference, while the class members above it remain theirs to implement.
    driver = solution[solution.index("\ndef solve()") :]
    ITEMS[num - 201].update({"title": title, "topics": topics, "description": description,
        "constraints": constraints, "hints": hints, "expected_complexity": complexity,
        "starter_code": starter.strip() + "\n" + driver.strip() + "\n", "solution": solution.strip() + "\n",
        "examples": [{"input": records[0]["input"], "output": records[0]["expected_output"], "explanation": explanation}],
        "public_tests": records[:2], "hidden_tests": records[2:],
        "submission_mode": "python_class", "required_class": required_class})


# Beginner object-oriented drills.  The CLI demo makes each reference runnable as
# a normal script; the private harnesses are what assess learner class submissions.
revise_class(281, "Rectangle class", ["classes", "math"],
    "Create Rectangle(width, height). Its area() method returns width times height and perimeter() returns twice the sum of width and height. The CLI demo reads width and height from line 1 and prints area then perimeter.",
    ["width and height are positive integers no greater than 1,000,000", "The complete CLI input is at most 12,000 characters", "The complete CLI output is at most 22,000 characters"],
    ["Store width and height on self in __init__.", "area uses multiplication.", "perimeter is 2 * (width + height)."], "O(1) time and O(1) space",
    """class Rectangle:
    def __init__(self, width, height):
        pass

    def area(self):
        pass

    def perimeter(self):
        pass""",
    """class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

def solve():
    width, height = map(int, input().split())
    rectangle = Rectangle(width, height)
    print(rectangle.area(), rectangle.perimeter())

if __name__ == '__main__':
    solve()""",
    [("3 4\n", "12 14", "width, height = map(int, sys.stdin.read().split())\nr = submission_class(width, height)\nprint(r.area(), r.perimeter())"),
     ("1 9\n", "9 20", "width, height = map(int, sys.stdin.read().split())\nr = submission_class(width, height)\nprint(r.area(), r.perimeter())"),
     ("10 2\n", "20 24", "width, height = map(int, sys.stdin.read().split())\nr = submission_class(width, height)\nprint(r.area(), r.perimeter())"),
     ("7 7\n", "49 28", "width, height = map(int, sys.stdin.read().split())\nr = submission_class(width, height)\nprint(r.area(), r.perimeter())")],
    "A three by four rectangle has area twelve and perimeter fourteen.", {"name": "Rectangle", "methods": ["__init__", "area", "perimeter"]})

revise_class(282, "Step counter class", ["classes", "state"],
    "Create StepCounter(initial). add(steps) increases its total, reset() changes it to zero, and value() returns the current total. CLI input is: line 1 initial, line 2 command count q, then q lines of add STEPS, reset, or value.",
    ["initial and added steps are integers from 0 through 1,000,000", "There are at most 500 commands", "The complete CLI input is at most 12,000 characters", "The complete CLI output is at most 22,000 characters"],
    ["Keep the changing total in an instance attribute.", "add changes that attribute.", "reset does not need an argument."], "O(1) per command and O(1) space",
    """class StepCounter:
    def __init__(self, initial):
        pass

    def add(self, steps):
        pass

    def reset(self):
        pass

    def value(self):
        pass""",
    """class StepCounter:
    def __init__(self, initial):
        self.total = initial

    def add(self, steps):
        self.total += steps

    def reset(self):
        self.total = 0

    def value(self):
        return self.total

def solve():
    initial = int(input())
    counter = StepCounter(initial)
    for _ in range(int(input())):
        parts = input().split()
        if parts[0] == 'add': counter.add(int(parts[1]))
        elif parts[0] == 'reset': counter.reset()
        else: print(counter.value())

if __name__ == '__main__':
    solve()""",
    [("5\n3\nadd 4\nvalue\nvalue\n", "9\n9", "lines = sys.stdin.read().splitlines()\nc = submission_class(int(lines[0]))\nfor line in lines[2:]:\n    parts = line.split()\n    if parts[0] == 'add': c.add(int(parts[1]))\n    elif parts[0] == 'reset': c.reset()\n    else: print(c.value())"),
     ("0\n4\nadd 3\nreset\nadd 2\nvalue\n", "2", "lines = sys.stdin.read().splitlines()\nc = submission_class(int(lines[0]))\nfor line in lines[2:]:\n    parts = line.split()\n    if parts[0] == 'add': c.add(int(parts[1]))\n    elif parts[0] == 'reset': c.reset()\n    else: print(c.value())"),
     ("10\n2\nreset\nvalue\n", "0", "lines = sys.stdin.read().splitlines()\nc = submission_class(int(lines[0]))\nfor line in lines[2:]:\n    parts = line.split()\n    if parts[0] == 'add': c.add(int(parts[1]))\n    elif parts[0] == 'reset': c.reset()\n    else: print(c.value())"),
     ("1\n3\nadd 1\nadd 8\nvalue\n", "10", "lines = sys.stdin.read().splitlines()\nc = submission_class(int(lines[0]))\nfor line in lines[2:]:\n    parts = line.split()\n    if parts[0] == 'add': c.add(int(parts[1]))\n    elif parts[0] == 'reset': c.reset()\n    else: print(c.value())")],
    "Starting at five and adding four gives nine.", {"name": "StepCounter", "methods": ["__init__", "add", "reset", "value"]})

revise_class(283, "Todo list class", ["classes", "lists", "state"],
    "Create TodoList(). add(task) adds an unfinished task, complete(task) marks its first matching unfinished task complete, and pending() returns unfinished tasks in their added order. CLI input is: line 1 command count q, then q lines of add TASK, complete TASK, or pending.",
    ["Task names contain 1 through 20 lowercase letters", "There are at most 60 commands", "The complete CLI input is at most 12,000 characters", "The complete CLI output is at most 22,000 characters"],
    ["A list can store tasks in order.", "Keep completed information for each task.", "pending returns only unfinished task names."], "O(n) for complete or pending and O(n) space",
    """class TodoList:
    def __init__(self):
        pass

    def add(self, task):
        pass

    def complete(self, task):
        pass

    def pending(self):
        pass""",
    """class TodoList:
    def __init__(self):
        self.tasks = []

    def add(self, task):
        self.tasks.append([task, False])

    def complete(self, task):
        for item in self.tasks:
            if item[0] == task and not item[1]:
                item[1] = True
                break

    def pending(self):
        return [task for task, finished in self.tasks if not finished]

def solve():
    todo = TodoList()
    for _ in range(int(input())):
        parts = input().split()
        if parts[0] == 'add': todo.add(parts[1])
        elif parts[0] == 'complete': todo.complete(parts[1])
        else: print(' '.join(todo.pending()))

if __name__ == '__main__':
    solve()""",
    [("4\nadd homework\nadd dishes\ncomplete homework\npending\n", "dishes", "lines = sys.stdin.read().splitlines()\nt = submission_class()\nfor line in lines[1:]:\n    parts = line.split()\n    if parts[0] == 'add': t.add(parts[1])\n    elif parts[0] == 'complete': t.complete(parts[1])\n    else: print(' '.join(t.pending()))"),
     ("3\nadd read\nadd code\npending\n", "read code", "lines = sys.stdin.read().splitlines()\nt = submission_class()\nfor line in lines[1:]:\n    parts = line.split()\n    if parts[0] == 'add': t.add(parts[1])\n    elif parts[0] == 'complete': t.complete(parts[1])\n    else: print(' '.join(t.pending()))"),
     ("4\nadd walk\ncomplete walk\npending\npending\n", "\n", "lines = sys.stdin.read().splitlines()\nt = submission_class()\nfor line in lines[1:]:\n    parts = line.split()\n    if parts[0] == 'add': t.add(parts[1])\n    elif parts[0] == 'complete': t.complete(parts[1])\n    else: print(' '.join(t.pending()))"),
     ("5\nadd email\nadd email\ncomplete email\npending\ncomplete email\n", "email", "lines = sys.stdin.read().splitlines()\nt = submission_class()\nfor line in lines[1:]:\n    parts = line.split()\n    if parts[0] == 'add': t.add(parts[1])\n    elif parts[0] == 'complete': t.complete(parts[1])\n    else: print(' '.join(t.pending()))")],
    "After homework is completed, dishes is the only pending task.", {"name": "TodoList", "methods": ["__init__", "add", "complete", "pending"]})

revise_class(284, "Temperature class", ["classes", "math"],
    "Create Temperature(celsius). Temperature.from_fahrenheit(fahrenheit) is a class method that makes a Temperature, and celsius() returns its Celsius value. The CLI demo reads one Fahrenheit value on line 1 and prints Celsius.",
    ["Fahrenheit inputs are chosen so the Celsius result is an integer", "-1,000 <= Fahrenheit <= 1,000", "The complete CLI input is at most 12,000 characters", "The complete CLI output is at most 22,000 characters"],
    ["A class method receives cls instead of self.", "Convert with (F - 32) * 5 // 9.", "Use cls(...) to construct the result."], "O(1) time and O(1) space",
    """class Temperature:
    def __init__(self, celsius):
        pass

    @classmethod
    def from_fahrenheit(cls, fahrenheit):
        pass

    def celsius(self):
        pass""",
    """class Temperature:
    def __init__(self, celsius):
        self.value = celsius

    @classmethod
    def from_fahrenheit(cls, fahrenheit):
        return cls((fahrenheit - 32) * 5 // 9)

    def celsius(self):
        return self.value

def solve():
    print(Temperature.from_fahrenheit(int(input())).celsius())

if __name__ == '__main__':
    solve()""",
    [("212\n", "100", "fahrenheit = int(sys.stdin.read())\nprint(submission_class.from_fahrenheit(fahrenheit).celsius())"),
     ("32\n", "0", "fahrenheit = int(sys.stdin.read())\nprint(submission_class.from_fahrenheit(fahrenheit).celsius())"),
     ("-40\n", "-40", "fahrenheit = int(sys.stdin.read())\nprint(submission_class.from_fahrenheit(fahrenheit).celsius())"),
     ("77\n", "25", "fahrenheit = int(sys.stdin.read())\nprint(submission_class.from_fahrenheit(fahrenheit).celsius())")],
    "212 Fahrenheit is 100 Celsius.", {"name": "Temperature", "methods": ["__init__", "from_fahrenheit", "celsius"]})

revise_class(285, "Wallet class", ["classes", "state", "conditionals"],
    "Create Wallet(initial). deposit(amount) adds money, withdraw(amount) returns True and removes money when enough is available, otherwise returns False without changing the balance, and balance() returns the current amount. CLI input is: line 1 initial amount, line 2 command count q, then q lines of deposit AMOUNT, withdraw AMOUNT, or balance.",
    ["All amounts are whole numbers from 0 through 1,000,000", "There are at most 500 commands", "The complete CLI input is at most 12,000 characters", "The complete CLI output is at most 22,000 characters"],
    ["Store the current amount on self.", "Check funds before subtracting.", "A failed withdrawal must leave the balance unchanged."], "O(1) per command and O(1) space",
    """class Wallet:
    def __init__(self, initial):
        pass

    def deposit(self, amount):
        pass

    def withdraw(self, amount):
        pass

    def balance(self):
        pass""",
    """class Wallet:
    def __init__(self, initial):
        self.money = initial

    def deposit(self, amount):
        self.money += amount

    def withdraw(self, amount):
        if amount > self.money:
            return False
        self.money -= amount
        return True

    def balance(self):
        return self.money

def solve():
    wallet = Wallet(int(input()))
    for _ in range(int(input())):
        parts = input().split()
        if parts[0] == 'deposit': wallet.deposit(int(parts[1]))
        elif parts[0] == 'withdraw': print(wallet.withdraw(int(parts[1])))
        else: print(wallet.balance())

if __name__ == '__main__':
    solve()""",
    [("10\n3\nwithdraw 4\ndeposit 7\nbalance\n", "True\n13", "lines = sys.stdin.read().splitlines()\nw = submission_class(int(lines[0]))\nfor line in lines[2:]:\n    parts = line.split()\n    if parts[0] == 'deposit': w.deposit(int(parts[1]))\n    elif parts[0] == 'withdraw': print(w.withdraw(int(parts[1])))\n    else: print(w.balance())"),
     ("5\n2\nwithdraw 8\nbalance\n", "False\n5", "lines = sys.stdin.read().splitlines()\nw = submission_class(int(lines[0]))\nfor line in lines[2:]:\n    parts = line.split()\n    if parts[0] == 'deposit': w.deposit(int(parts[1]))\n    elif parts[0] == 'withdraw': print(w.withdraw(int(parts[1])))\n    else: print(w.balance())"),
     ("0\n3\ndeposit 2\nwithdraw 2\nbalance\n", "True\n0", "lines = sys.stdin.read().splitlines()\nw = submission_class(int(lines[0]))\nfor line in lines[2:]:\n    parts = line.split()\n    if parts[0] == 'deposit': w.deposit(int(parts[1]))\n    elif parts[0] == 'withdraw': print(w.withdraw(int(parts[1])))\n    else: print(w.balance())"),
     ("20\n2\nwithdraw 20\nbalance\n", "True\n0", "lines = sys.stdin.read().splitlines()\nw = submission_class(int(lines[0]))\nfor line in lines[2:]:\n    parts = line.split()\n    if parts[0] == 'deposit': w.deposit(int(parts[1]))\n    elif parts[0] == 'withdraw': print(w.withdraw(int(parts[1])))\n    else: print(w.balance())")],
    "Withdrawing four succeeds, then depositing seven leaves thirteen.", {"name": "Wallet", "methods": ["__init__", "deposit", "withdraw", "balance"]})

revise_class(286, "Grade book class", ["classes", "lists", "math"],
    "Create GradeBook(). add(score) stores a score, average() returns the integer average of all stored scores, and highest() returns the largest score. CLI input is: line 1 command count q, then q lines of add SCORE, average, or highest; value commands occur only after a score was added.",
    ["Scores are integers from 0 through 100", "There are at most 1,000 commands", "average and highest are called only after add", "The complete CLI input is at most 12,000 characters", "The complete CLI output is at most 22,000 characters"],
    ["Keep scores in a list.", "append adds one score.", "Use // for the requested integer average."], "O(n) for average or highest and O(n) space",
    """class GradeBook:
    def __init__(self):
        pass

    def add(self, score):
        pass

    def average(self):
        pass

    def highest(self):
        pass""",
    """class GradeBook:
    def __init__(self):
        self.scores = []

    def add(self, score):
        self.scores.append(score)

    def average(self):
        return sum(self.scores) // len(self.scores)

    def highest(self):
        return max(self.scores)

def solve():
    book = GradeBook()
    for _ in range(int(input())):
        parts = input().split()
        if parts[0] == 'add': book.add(int(parts[1]))
        elif parts[0] == 'average': print(book.average())
        else: print(book.highest())

if __name__ == '__main__':
    solve()""",
    [("4\nadd 80\nadd 90\naverage\nhighest\n", "85\n90", "lines = sys.stdin.read().splitlines()\nb = submission_class()\nfor line in lines[1:]:\n    parts = line.split()\n    if parts[0] == 'add': b.add(int(parts[1]))\n    elif parts[0] == 'average': print(b.average())\n    else: print(b.highest())"),
     ("3\nadd 70\nadd 71\naverage\n", "70", "lines = sys.stdin.read().splitlines()\nb = submission_class()\nfor line in lines[1:]:\n    parts = line.split()\n    if parts[0] == 'add': b.add(int(parts[1]))\n    elif parts[0] == 'average': print(b.average())\n    else: print(b.highest())"),
     ("2\nadd 100\nhighest\n", "100", "lines = sys.stdin.read().splitlines()\nb = submission_class()\nfor line in lines[1:]:\n    parts = line.split()\n    if parts[0] == 'add': b.add(int(parts[1]))\n    elif parts[0] == 'average': print(b.average())\n    else: print(b.highest())"),
     ("5\nadd 30\nadd 60\nadd 90\naverage\nhighest\n", "60\n90", "lines = sys.stdin.read().splitlines()\nb = submission_class()\nfor line in lines[1:]:\n    parts = line.split()\n    if parts[0] == 'add': b.add(int(parts[1]))\n    elif parts[0] == 'average': print(b.average())\n    else: print(b.highest())")],
    "The average of eighty and ninety is eighty-five, and ninety is highest.", {"name": "GradeBook", "methods": ["__init__", "add", "average", "highest"]})

revise_class(287, "Pet class", ["classes", "state"],
    "Create Pet(name). It starts with hunger 5 and happiness 5. feed() lowers hunger by one but never below zero, play() raises happiness by one but never above ten, and status() returns the name, hunger, and happiness separated by spaces. CLI input is: line 1 name, line 2 command count q, then q lines of feed, play, or status.",
    ["The name contains 1 through 20 lowercase letters", "There are at most 500 commands", "The complete CLI input is at most 12,000 characters", "The complete CLI output is at most 22,000 characters"],
    ["Store the three pieces of state on self.", "Use max to stop hunger below zero.", "Use min to stop happiness above ten."], "O(1) per command and O(1) space",
    """class Pet:
    def __init__(self, name):
        pass

    def feed(self):
        pass

    def play(self):
        pass

    def status(self):
        pass""",
    """class Pet:
    def __init__(self, name):
        self.name = name
        self.hunger = 5
        self.happiness = 5

    def feed(self):
        self.hunger = max(0, self.hunger - 1)

    def play(self):
        self.happiness = min(10, self.happiness + 1)

    def status(self):
        return f'{self.name} {self.hunger} {self.happiness}'

def solve():
    pet = Pet(input().strip())
    for _ in range(int(input())):
        command = input().strip()
        if command == 'feed': pet.feed()
        elif command == 'play': pet.play()
        else: print(pet.status())

if __name__ == '__main__':
    solve()""",
    [("milo\n3\nfeed\nplay\nstatus\n", "milo 4 6", "lines = sys.stdin.read().splitlines()\np = submission_class(lines[0])\nfor command in lines[2:]:\n    if command == 'feed': p.feed()\n    elif command == 'play': p.play()\n    else: print(p.status())"),
     ("ava\n2\nfeed\nstatus\n", "ava 4 5", "lines = sys.stdin.read().splitlines()\np = submission_class(lines[0])\nfor command in lines[2:]:\n    if command == 'feed': p.feed()\n    elif command == 'play': p.play()\n    else: print(p.status())"),
     ("fox\n7\nfeed\nfeed\nfeed\nfeed\nfeed\nfeed\nstatus\n", "fox 0 5", "lines = sys.stdin.read().splitlines()\np = submission_class(lines[0])\nfor command in lines[2:]:\n    if command == 'feed': p.feed()\n    elif command == 'play': p.play()\n    else: print(p.status())"),
     ("leo\n7\nplay\nplay\nplay\nplay\nplay\nplay\nstatus\n", "leo 5 10", "lines = sys.stdin.read().splitlines()\np = submission_class(lines[0])\nfor command in lines[2:]:\n    if command == 'feed': p.feed()\n    elif command == 'play': p.play()\n    else: print(p.status())")],
    "Feeding Milo lowers hunger to four and playing raises happiness to six.", {"name": "Pet", "methods": ["__init__", "feed", "play", "status"]})

revise_class(288, "Countdown class", ["classes", "state", "conditionals"],
    "Create Countdown(initial). tick() lowers the remaining value by one but never below zero, remaining() returns that value, and done() returns True exactly when it is zero. CLI input is: line 1 initial value, line 2 command count q, then q lines of tick, remaining, or done.",
    ["initial is a nonnegative integer no greater than 1,000,000", "There are at most 1,000 commands", "The complete CLI input is at most 12,000 characters", "The complete CLI output is at most 22,000 characters"],
    ["Store the remaining value on self.", "Use max when ticking.", "done can compare remaining with zero."], "O(1) per command and O(1) space",
    """class Countdown:
    def __init__(self, initial):
        pass

    def tick(self):
        pass

    def remaining(self):
        pass

    def done(self):
        pass""",
    """class Countdown:
    def __init__(self, initial):
        self.value = initial

    def tick(self):
        self.value = max(0, self.value - 1)

    def remaining(self):
        return self.value

    def done(self):
        return self.value == 0

def solve():
    countdown = Countdown(int(input()))
    for _ in range(int(input())):
        command = input().strip()
        if command == 'tick': countdown.tick()
        elif command == 'remaining': print(countdown.remaining())
        else: print(countdown.done())

if __name__ == '__main__':
    solve()""",
    [("3\n3\ntick\nremaining\ndone\n", "2\nFalse", "lines = sys.stdin.read().splitlines()\nc = submission_class(int(lines[0]))\nfor command in lines[2:]:\n    if command == 'tick': c.tick()\n    elif command == 'remaining': print(c.remaining())\n    else: print(c.done())"),
     ("1\n3\ntick\ndone\nremaining\n", "True\n0", "lines = sys.stdin.read().splitlines()\nc = submission_class(int(lines[0]))\nfor command in lines[2:]:\n    if command == 'tick': c.tick()\n    elif command == 'remaining': print(c.remaining())\n    else: print(c.done())"),
     ("0\n2\ndone\ntick\n", "True", "lines = sys.stdin.read().splitlines()\nc = submission_class(int(lines[0]))\nfor command in lines[2:]:\n    if command == 'tick': c.tick()\n    elif command == 'remaining': print(c.remaining())\n    else: print(c.done())"),
     ("2\n4\ntick\ntick\ntick\nremaining\n", "0", "lines = sys.stdin.read().splitlines()\nc = submission_class(int(lines[0]))\nfor command in lines[2:]:\n    if command == 'tick': c.tick()\n    elif command == 'remaining': print(c.remaining())\n    else: print(c.done())")],
    "After one tick from three, two remain and the countdown is not done.", {"name": "Countdown", "methods": ["__init__", "tick", "remaining", "done"]})

PYTHON_CURATED_201_288 = ITEMS
