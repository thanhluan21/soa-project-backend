# services/users/manage.py

from flask.cli import FlaskGroup
from project import create_app, db
import os
import math

import pytest
import sys
from project.api.models import User, Exercise, Score


# deug env
# import sys

# print(app.config, file=sys.stderr)

app = create_app()
cli = FlaskGroup(app)


@cli.command("recreate_db")
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    """Seeds the database."""
    db.session.add(
        User(
            username="longns",
            email="longmentor@cloudmentorpro.com",
            password="verysecure",
        )
    )
    db.session.add(
        User(
            username="admnin1",
            email="admin1@a.c",
            password="123456",
            admin=True,
        )
    )

    # Exercise 1
    db.session.add(
        Exercise(
            title="Sum of Two Integers",
            body=(
                '# Define a function called sum that takes two integers as\n'
                '# arguments and returns their sum.\n'
                'def sum(a, b):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=0,
            test_cases=["sum(2, 3)", "sum(4, 5)", "sum(-1, 1)"],
            solutions=["5", "9", "0"],
        )
    )

    # Exercise 2
    db.session.add(
        Exercise(
            title="Reverse a String",
            body=(
                '# Define a function called reverse that takes a string as\n'
                '# an argument and returns the string in reversed order.\n'
                'def reverse(s):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=0,
            test_cases=['reverse("racecar")', 'reverse("hello")', 'reverse("")'],
            solutions=["racecar", "olleh", ""],
        )
    )

    # Exercise 3
    db.session.add(
        Exercise(
            title="Factorial of a Number",
            body=(
                '# Define a function called factorial that takes a non-negative integer\n'
                '# as an argument and returns its factorial.\n'
                'def factorial(n):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=1,
            test_cases=["factorial(5)", "factorial(0)", "factorial(1)"],
            solutions=["120", "1", "1"],
        )
    )

    # Exercise 4
    db.session.add(
        Exercise(
            title="Check Palindrome",
            body=(
                '# Define a function called is_palindrome that takes a string and\n'
                '# returns True if it is a palindrome, False otherwise.\n'
                'def is_palindrome(s):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=0,
            test_cases=['is_palindrome("racecar")', 'is_palindrome("hello")', 'is_palindrome("a")'],
            solutions=["True", "False", "True"],
        )
    )

    # Exercise 5
    db.session.add(
        Exercise(
            title="Maximum in List",
            body=(
                '# Define a function called max_in_list that takes a list of numbers\n'
                '# and returns the maximum value.\n'
                'def max_in_list(lst):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=0,
            test_cases=["max_in_list([1, 3, 2])", "max_in_list([-5, -1, -10])", "max_in_list([0])"],
            solutions=["3", "-1", "0"],
        )
    )

    # Exercise 6
    db.session.add(
        Exercise(
            title="Fibonacci Sequence",
            body=(
                '# Define a function called fibonacci that takes an integer n and\n'
                '# returns the nth Fibonacci number (0-indexed).\n'
                'def fibonacci(n):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=1,
            test_cases=["fibonacci(0)", "fibonacci(1)", "fibonacci(5)"],
            solutions=["0", "1", "5"],
        )
    )

    # Exercise 7
    db.session.add(
        Exercise(
            title="Count Vowels",
            body=(
                '# Define a function called count_vowels that takes a string and\n'
                '# returns the number of vowels (a, e, i, o, u).\n'
                'def count_vowels(s):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=0,
            test_cases=['count_vowels("hello")', 'count_vowels("python")', 'count_vowels("")'],
            solutions=["2", "1", "0"],
        )
    )

    # Exercise 8
    db.session.add(
        Exercise(
            title="Prime Number Check",
            body=(
                '# Define a function called is_prime that takes an integer and\n'
                '# returns True if it is prime, False otherwise.\n'
                'def is_prime(n):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=1,
            test_cases=["is_prime(7)", "is_prime(4)", "is_prime(1)"],
            solutions=["True", "False", "False"],
        )
    )

    # Exercise 9
    db.session.add(
        Exercise(
            title="List Sum",
            body=(
                '# Define a function called list_sum that takes a list of numbers\n'
                '# and returns their sum.\n'
                'def list_sum(lst):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=0,
            test_cases=["list_sum([1, 2, 3])", "list_sum([])", "list_sum([-1, 1])"],
            solutions=["6", "0", "0"],
        )
    )

    # Exercise 10
    db.session.add(
        Exercise(
            title="Remove Duplicates",
            body=(
                '# Define a function called remove_duplicates that takes a list\n'
                '# and returns a list with duplicates removed.\n'
                'def remove_duplicates(lst):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=1,
            test_cases=["remove_duplicates([1, 2, 2, 3])", "remove_duplicates([])", "remove_duplicates([4, 4])"],
            solutions=["[1, 2, 3]", "[]", "[4]"],
        )
    )

    # Exercise 11
    db.session.add(
        Exercise(
            title="String Capitalize",
            body=(
                '# Define a function called capitalize_words that takes a string\n'
                '# and returns the string with each word capitalized.\n'
                'def capitalize_words(s):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=0,
            test_cases=['capitalize_words("hello world")', 'capitalize_words("python")', 'capitalize_words("")'],
            solutions=["Hello World", "Python", ""],
        )
    )

    # Exercise 12
    db.session.add(
        Exercise(
            title="GCD of Two Numbers",
            body=(
                '# Define a function called gcd that takes two integers and\n'
                '# returns their greatest common divisor.\n'
                'def gcd(a, b):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=1,
            test_cases=["gcd(48, 18)", "gcd(7, 5)", "gcd(0, 0)"],
            solutions=["6", "1", "0"],
        )
    )

    # Exercise 13
    db.session.add(
        Exercise(
            title="List Reverse",
            body=(
                '# Define a function called reverse_list that takes a list and\n'
                '# returns it in reversed order.\n'
                'def reverse_list(lst):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=0,
            test_cases=["reverse_list([1, 2, 3])", "reverse_list([])", "reverse_list([5])"],
            solutions=["[3, 2, 1]", "[]", "[5]"],
        )
    )

    # Exercise 14
    db.session.add(
        Exercise(
            title="Binary Search",
            body=(
                '# Define a function called binary_search that takes a sorted list\n'
                '# and a target, returns index if found, -1 otherwise.\n'
                'def binary_search(lst, target):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=2,
            test_cases=["binary_search([1, 3, 5, 7], 5)", "binary_search([1, 2, 3], 4)", "binary_search([], 1)"],
            solutions=["2", "-1", "-1"],
        )
    )

    # Exercise 15
    db.session.add(
        Exercise(
            title="Count Occurrences",
            body=(
                '# Define a function called count_occurrences that takes a list and an element,\n'
                '# returns how many times the element appears.\n'
                'def count_occurrences(lst, elem):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=0,
            test_cases=["count_occurrences([1, 2, 2, 3], 2)", "count_occurrences([], 5)", "count_occurrences([4], 4)"],
            solutions=["2", "0", "1"],
        )
    )

    # Exercise 16
    db.session.add(
        Exercise(
            title="Merge Two Lists",
            body=(
                '# Define a function called merge_lists that takes two lists and\n'
                '# returns a single merged list.\n'
                'def merge_lists(lst1, lst2):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=0,
            test_cases=["merge_lists([1, 2], [3, 4])", "merge_lists([], [5])", "merge_lists([6], [])"],
            solutions=["[1, 2, 3, 4]", "[5]", "[6]"],
        )
    )

    # Exercise 17
    db.session.add(
        Exercise(
            title="Power Function",
            body=(
                '# Define a function called power that takes base and exponent,\n'
                '# returns base raised to exponent.\n'
                'def power(base, exp):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=1,
            test_cases=["power(2, 3)", "power(5, 0)", "power(3, 1)"],
            solutions=["8", "1", "3"],
        )
    )

    # Exercise 18
    db.session.add(
        Exercise(
            title="Sort List",
            body=(
                '# Define a function called sort_list that takes a list of numbers\n'
                '# and returns it sorted in ascending order.\n'
                'def sort_list(lst):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=1,
            test_cases=["sort_list([3, 1, 2])", "sort_list([])", "sort_list([5, 5])"],
            solutions=["[1, 2, 3]", "[]", "[5, 5]"],
        )
    )

    # Exercise 19
    db.session.add(
        Exercise(
            title="Check Even",
            body=(
                '# Define a function called is_even that takes an integer and\n'
                '# returns True if even, False otherwise.\n'
                'def is_even(n):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=0,
            test_cases=["is_even(4)", "is_even(5)", "is_even(0)"],
            solutions=["True", "False", "True"],
        )
    )

    # Exercise 20
    db.session.add(
        Exercise(
            title="Longest Word",
            body=(
                '# Define a function called longest_word that takes a string of words\n'
                '# and returns the longest word.\n'
                'def longest_word(s):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=1,
            test_cases=['longest_word("hello world python")', 'longest_word("a b c")', 'longest_word("")'],
            solutions=["python", "a", ""],
        )
    )

    # Exercise 21
    db.session.add(
        Exercise(
            title="Square Root",
            body=(
                '# Define a function called square_root that takes a number and\n'
                '# returns its integer square root (floor).\n'
                'def square_root(n):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=1,
            test_cases=["square_root(9)", "square_root(10)", "square_root(0)"],
            solutions=["3", "3", "0"],
        )
    )

    # Exercise 22
    db.session.add(
        Exercise(
            title="Unique Elements",
            body=(
                '# Define a function called unique_elements that takes two lists and\n'
                '# returns unique elements from both.\n'
                'def unique_elements(lst1, lst2):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=1,
            test_cases=["unique_elements([1, 2], [2, 3])", "unique_elements([], [])", "unique_elements([4], [4])"],
            solutions=["[1, 2, 3]", "[]", "[4]"],
        )
    )

    # Exercise 23
    db.session.add(
        Exercise(
            title="Average of List",
            body=(
                '# Define a function called average that takes a list of numbers\n'
                '# and returns their average (float).\n'
                'def average(lst):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=0,
            test_cases=["average([1, 2, 3])", "average([5])", "average([])"],
            solutions=["2.0", "5.0", "0.0"],
        )
    )

    # Exercise 24
    db.session.add(
        Exercise(
            title="Anagram Check",
            body=(
                '# Define a function called is_anagram that takes two strings and\n'
                '# returns True if they are anagrams.\n'
                'def is_anagram(s1, s2):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=1,
            test_cases=['is_anagram("listen", "silent")', 'is_anagram("hello", "world")', 'is_anagram("a", "a")'],
            solutions=["True", "False", "True"],
        )
    )

    # Exercise 25
    db.session.add(
        Exercise(
            title="Multiply Strings",
            body=(
                '# Define a function called multiply_strings that takes a string and an integer n,\n'
                '# returns the string repeated n times.\n'
                'def multiply_strings(s, n):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=0,
            test_cases=['multiply_strings("ab", 3)', 'multiply_strings("", 5)', 'multiply_strings("c", 0)'],
            solutions=["ababab", "", ""],
        )
    )

    # Exercise 26
    db.session.add(
        Exercise(
            title="Matrix Transpose",
            body=(
                '# Define a function called transpose that takes a 2D list (matrix)\n'
                '# and returns its transpose.\n'
                'def transpose(matrix):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=2,
            test_cases=["transpose([[1,2],[3,4]])", "transpose([[5]])", "transpose([])"],
            solutions=["[[1, 3], [2, 4]]", "[[5]]", "[]"],
        )
    )

    # Exercise 27
    db.session.add(
        Exercise(
            title="Leap Year Check",
            body=(
                '# Define a function called is_leap_year that takes a year and\n'
                '# returns True if it is a leap year.\n'
                'def is_leap_year(year):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=1,
            test_cases=["is_leap_year(2000)", "is_leap_year(1900)", "is_leap_year(2024)"],
            solutions=["True", "False", "True"],
        )
    )

    # Exercise 28
    db.session.add(
        Exercise(
            title="Dictionary Merge",
            body=(
                '# Define a function called merge_dicts that takes two dictionaries\n'
                '# and returns a merged dictionary.\n'
                'def merge_dicts(d1, d2):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=1,
            test_cases=["merge_dicts({'a':1}, {'b':2})", "merge_dicts({}, {})", "merge_dicts({'c':3}, {'c':4})"],
            solutions=["{'a': 1, 'b': 2}", "{}", "{'c': 4}"],
        )
    )

    # Exercise 29
    db.session.add(
        Exercise(
            title="Fizz Buzz",
            body=(
                '# Define a function called fizz_buzz that takes an integer n and\n'
                '# returns "Fizz" if divisible by 3, "Buzz" by 5, "FizzBuzz" by both, else n.\n'
                'def fizz_buzz(n):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=0,
            test_cases=["fizz_buzz(15)", "fizz_buzz(3)", "fizz_buzz(5)", "fizz_buzz(4)"],
            solutions=["FizzBuzz", "Fizz", "Buzz", "4"],
        )
    )

    # Exercise 30
    db.session.add(
        Exercise(
            title="Roman to Integer",
            body=(
                '# Define a function called roman_to_int that takes a Roman numeral string\n'
                '# and returns its integer value.\n'
                'def roman_to_int(s):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=2,
            test_cases=['roman_to_int("III")', 'roman_to_int("IV")', 'roman_to_int("IX")'],
            solutions=["3", "4", "9"],
        )
    )

    # Exercise 31
    db.session.add(
        Exercise(
            title="Generate Primes",
            body=(
                '# Define a function called generate_primes that takes an integer n\n'
                '# and returns list of primes up to n.\n'
                'def generate_primes(n):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=2,
            test_cases=["generate_primes(10)", "generate_primes(2)", "generate_primes(1)"],
            solutions=["[2, 3, 5, 7]", "[2]", "[]"],
        )
    )

    # Exercise 32
    db.session.add(
        Exercise(
            title="Caesar Cipher",
            body=(
                '# Define a function called caesar_cipher that takes a string and shift,\n'
                '# returns the encrypted string.\n'
                'def caesar_cipher(s, shift):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=1,
            test_cases=['caesar_cipher("abc", 1)', 'caesar_cipher("xyz", 3)', 'caesar_cipher("", 5)'],
            solutions=["bcd", "abc", ""],
        )
    )

    # Exercise 33
    db.session.add(
        Exercise(
            title="List Flatten",
            body=(
                '# Define a function called flatten_list that takes a nested list\n'
                '# and returns a flat list.\n'
                'def flatten_list(lst):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=1,
            test_cases=["flatten_list([[1, 2], [3]])", "flatten_list([])", "flatten_list([[4]])"],
            solutions=["[1, 2, 3]", "[]", "[4]"],
        )
    )

    # Exercise 34
    db.session.add(
        Exercise(
            title="Permutations",
            body=(
                '# Define a function called permutations that takes a list\n'
                '# and returns all its permutations as list of lists.\n'
                'def permutations(lst):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=2,
            test_cases=["permutations([1, 2])", "permutations([])", "permutations([3])"],
            solutions=["[[1, 2], [2, 1]]", "[[]]", "[[3]]"],
        )
    )

    # Exercise 35
    db.session.add(
        Exercise(
            title="Temperature Conversion",
            body=(
                '# Define a function called celsius_to_fahrenheit that takes Celsius\n'
                '# and returns Fahrenheit.\n'
                'def celsius_to_fahrenheit(c):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=0,
            test_cases=["celsius_to_fahrenheit(0)", "celsius_to_fahrenheit(100)", "celsius_to_fahrenheit(-40)"],
            solutions=["32.0", "212.0", "-40.0"],
        )
    )

    # Exercise 36
    db.session.add(
        Exercise(
            title="Queue Implementation",
            body=(
                '# Define a class called Queue with methods enqueue, dequeue, is_empty.\n'
                '# For this exercise, implement enqueue and test it.\n'
                'class Queue:\n'
                '    def __init__(self):\n'
                '        self.queue = []\n'
                '    def enqueue(self, item):\n'
                '        # write your answer here\n'
                '        pass\n'
                '# Test will create instance and call methods'
            ),
            difficulty=1,
            test_cases=["q = Queue(); q.enqueue(1); q.enqueue(2); str(q.queue)", "q = Queue(); str(q.queue)"],
            solutions=["[1, 2]", "[]"],
        )
    )

    # Exercise 37
    db.session.add(
        Exercise(
            title="Stack Implementation",
            body=(
                '# Define a class called Stack with methods push, pop, is_empty.\n'
                '# For this exercise, implement push and test it.\n'
                'class Stack:\n'
                '    def __init__(self):\n'
                '        self.stack = []\n'
                '    def push(self, item):\n'
                '        # write your answer here\n'
                '        pass\n'
                '# Test will create instance and call methods'
            ),
            difficulty=1,
            test_cases=["s = Stack(); s.push(1); s.push(2); str(s.stack)", "s = Stack(); str(s.stack)"],
            solutions=["[1, 2]", "[]"],
        )
    )

    # Exercise 38
    db.session.add(
        Exercise(
            title="Linked List Node",
            body=(
                '# Define a class called Node for linked list with value and next.\n'
                'class Node:\n'
                '    def __init__(self, value):\n'
                '        self.value = value\n'
                '        self.next = None\n'
                '# Test will create nodes'
            ),
            difficulty=1,
            test_cases=["n = Node(5); n.value", "n = Node('a'); n.value"],
            solutions=["5", "a"],
        )
    )

    # Exercise 39
    db.session.add(
        Exercise(
            title="Binary Tree Height",
            body=(
                '# Define a function called tree_height that takes a binary tree root\n'
                '# and returns its height. Assume TreeNode class exists.\n'
                'def tree_height(root):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=2,
            test_cases=[],  # Skip complex setup for now
            solutions=[],
        )
    )

    # Exercise 40
    db.session.add(
        Exercise(
            title="Validate Email",
            body=(
                '# Define a function called is_valid_email that takes a string\n'
                '# and returns True if valid email format.\n'
                'def is_valid_email(email):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=1,
            test_cases=['is_valid_email("test@example.com")', 'is_valid_email("invalid")', 'is_valid_email("a@b.c")'],
            solutions=["True", "False", "True"],
        )
    )

    # Exercise 41
    db.session.add(
        Exercise(
            title="Random Number Generator",
            body=(
                '# Define a function called random_between that takes two integers\n'
                '# and returns a random integer between them inclusive. Import random.\n'
                'import random\n'
                'def random_between(a, b):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=0,
            test_cases=[],  # Random, hard to test deterministically
            solutions=[],
        )
    )

    # Exercise 42
    db.session.add(
        Exercise(
            title="JSON Parse",
            body=(
                '# Define a function called parse_json that takes a JSON string\n'
                '# and returns the parsed dict. Import json.\n'
                'import json\n'
                'def parse_json(s):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=1,
            test_cases=['parse_json(\'{"a":1}\')', 'parse_json(\'[]\')'],
            solutions=["{'a': 1}", "[]"],
        )
    )

    # Exercise 43
    db.session.add(
        Exercise(
            title="File Read",
            body=(
                '# Define a function called read_file that takes a filename\n'
                '# and returns its content as string. Assume file exists.\n'
                'def read_file(filename):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=1,
            test_cases=[],  # File system access not in test
            solutions=[],
        )
    )

    # Exercise 44
    db.session.add(
        Exercise(
            title="Date Difference",
            body=(
                '# Define a function called days_between that takes two dates as strings "YYYY-MM-DD"\n'
                '# and returns days between them. Import datetime.\n'
                'from datetime import datetime\n'
                'def days_between(d1, d2):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=1,
            test_cases=['days_between("2023-01-01", "2023-01-02")', 'days_between("2020-02-28", "2020-03-01")'],
            solutions=["1", "2"],
        )
    )

    # Exercise 45
    db.session.add(
        Exercise(
            title="Hex to Decimal",
            body=(
                '# Define a function called hex_to_dec that takes a hex string\n'
                '# and returns its decimal integer.\n'
                'def hex_to_dec(h):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=1,
            test_cases=["hex_to_dec('A')", "hex_to_dec('10')", "hex_to_dec('0')"],
            solutions=["10", "16", "0"],
        )
    )

    # Exercise 46
    db.session.add(
        Exercise(
            title="Binary to Decimal",
            body=(
                '# Define a function called bin_to_dec that takes a binary string\n'
                '# and returns its decimal integer.\n'
                'def bin_to_dec(b):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=1,
            test_cases=["bin_to_dec('101')", "bin_to_dec('0')", "bin_to_dec('1')"],
            solutions=["5", "0", "1"],
        )
    )

    # Exercise 47
    db.session.add(
        Exercise(
            title="Shuffle List",
            body=(
                '# Define a function called shuffle_list that takes a list\n'
                '# and returns a shuffled copy. Import random.\n'
                'import random\n'
                'def shuffle_list(lst):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=1,
            test_cases=[],  # Random
            solutions=[],
        )
    )

    # Exercise 48
    db.session.add(
        Exercise(
            title="Calculate Area Circle",
            body=(
                '# Define a function called circle_area that takes radius\n'
                '# and returns area (use math.pi). Import math.\n'
                'import math\n'
                'def circle_area(r):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=0,
            test_cases=["circle_area(1)", "circle_area(0)"],
            solutions=[str(math.pi), "0.0"],
        )
    )

    # Exercise 49
    db.session.add(
        Exercise(
            title="Find Median",
            body=(
                '# Define a function called find_median that takes a list of numbers\n'
                '# and returns the median.\n'
                'def find_median(lst):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=1,
            test_cases=["find_median([1, 2, 3])", "find_median([4, 5])", "find_median([])"],
            solutions=["2", "4.5", "None"],
        )
    )

    # Exercise 50
    db.session.add(
        Exercise(
            title="Hanoi Tower",
            body=(
                '# Define a function called tower_of_hanoi that solves for n disks.\n'
                '# Return number of moves.\n'
                'def tower_of_hanoi(n):\n'
                '    # write your answer here\n'
                '    pass'
            ),
            difficulty=2,
            test_cases=["tower_of_hanoi(1)", "tower_of_hanoi(3)", "tower_of_hanoi(0)"],
            solutions=["1", "7", "0"],
        )
    )

    # commit exercises and users first
    db.session.commit()

    # get exercises and users directly from database
    exercises = Exercise.query.all()
    users = User.query.all()

    # seed scores
    for user in users:
        for exercise in exercises:
            db.session.add(Score(user_id=user.id, exercise_id=exercise.id))

    db.session.commit()


@cli.command("run_tests")
def run_tests():
    """Chạy hết test case trong project/tests ."""
    # Chạy pytest với folder tests, thêm -v để verbose .
    sys.exit(
        pytest.main(["project/tests", "-v"])
    )  # Exit với code từ pytest, fail thì báo lỗi


if __name__ == "__main__":
    cli()