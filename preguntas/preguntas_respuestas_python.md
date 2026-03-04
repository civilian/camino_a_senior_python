# Python Interview Questions and Answers (2025)

He recopilado las **preguntas** y sus **respuestas principales** en formato Markdown para que puedas usarlas como banco de estudio. El contenido está en inglés tal y como aparece en la fuente (resumido a la parte de Q&A, sin navegación ni texto irrelevante).

---

## Basic Python Interview Questions for Freshers

### Q1. What is the difference between list and tuples in Python?

**Answer:**

- **Lists**
  - Mutable (can be edited after creation).
  - Slower than tuples.
  - Syntax: `list_1 = [10, "Chelsea", 20]`
- **Tuples**
  - Immutable (cannot be edited after creation).
  - Faster than lists.
  - Syntax: `tup_1 = (10, "Chelsea", 20)`

---

### Q2. What are the key features of Python?

**Answer:**

- **Interpreted** language (no compilation step required).
- **Dynamically typed** (no need to declare variable types).
- Supports **object-oriented programming** (classes, inheritance, composition).
- **Functions and classes are first-class objects**.
- **Fast to write, slower to run** (but can use C extensions like NumPy for speed).
- Widely used in **web apps, automation, scientific computing, big data**, etc.

---

### Q3. What type of language is Python? Programming or scripting?

**Answer:**

Python is a **general-purpose programming language** that is also excellent for **scripting**. It is commonly used in both roles.

---

### Q4. Python is an interpreted language. Explain.

**Answer:**

An **interpreted language** executes code line by line at runtime, without producing a separate machine-code binary ahead of time. Python source is compiled to bytecode and then executed by the Python virtual machine at runtime.

---

### Q5. What is PEP 8?

**Answer:**

**PEP 8** (Python Enhancement Proposal 8) is the **style guide for Python code**. It defines conventions for:

- Naming (functions, variables, classes).
- Indentation, whitespace, line length.
- Imports, comments, and more.

Its goal is to maximize code readability and consistency.

---

### Q6. What are the benefits of using Python?

**Answer:**

1. **Easy to use and learn** – clear, high-level syntax.
2. **Interpreted** – executes line by line, easier debugging.
3. **Dynamically typed** – no explicit type declarations.
4. **Free and open-source** – strong community and ecosystem.
5. **Extensive standard library and third-party packages** (PyPI).
6. **Portable** – runs on many platforms without changes.
7. **Rich built-in data structures** (lists, dicts, sets).
8. **More functionality with less code** – very productive.

---

### Q7. What are Python namespaces?

**Answer:**

A **namespace** is a mapping from names to objects (like a dictionary). It ensures that names are unique and won’t conflict.

Types of namespaces:

1. **Built-in namespace** – names provided by Python (e.g., `len`, `print`).
2. **Global namespace** – names defined at the module level.
3. **Enclosing namespaces** – names in enclosing functions.
4. **Local namespace** – names inside a specific function.

---

### Q8. What are decorators in Python?

**Answer:**

**Decorators** are a way to modify or enhance functions or methods **without changing their code**. A decorator is a callable that takes a function and returns a new function.

Basic pattern:

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        # do something before
        result = func(*args, **kwargs)
        # do something after
        return result
    return wrapper

@my_decorator
def my_function():
    ...
```

---

### Q9. What are dict and list comprehensions?

**Answer:**

- **List comprehension** – concise way to create lists:

```python
x = [i for i in range(5)]      # [0, 1, 2, 3, 4]
```

- **Dictionary comprehension** – concise way to create dicts:

```python
x = {i: i + 2 for i in range(5)}  # {0: 2, 1: 3, 2: 4, 3: 5, 4: 6}
```

They are more readable and often faster than manual loops.

---

### Q10. What are the common built-in data types in Python?

**Answer:**

- **Numbers** – `int`, `float`, `complex`
- **String** – `str`
- **Sequence types** – `list`, `tuple`, `range`
- **Mapping** – `dict`
- **Set types** – `set`, `frozenset`
- **Boolean** – `bool`
- **Binary types** – `bytes`, `bytearray`, `memoryview`

---

### Q11. What is the difference between `.py` and `.pyc` files?

**Answer:**

- `.py` files – **source code**.
- `.pyc` files – **compiled bytecode** (created by the interpreter when importing modules to speed up loading).

`.pyc` files are generated automatically and used internally by Python.

---

### Q12. What is slicing in Python?

**Answer:**

**Slicing** extracts parts of sequences (strings, lists, tuples) using:

```python
sequence[start:end:step]
```

- `start` – starting index (inclusive).
- `end` – ending index (exclusive).
- `step` – stride; can be negative.

Example:

```python
lst = [1, 2, 3, 4, 5, 6, 7, 8]
lst[1:5]      # [2, 3, 4, 5]
lst[::-1]     # [8, 7, 6, 5, 4, 3, 2, 1]
```

---

### Q13. What are keywords in Python?

**Answer:**

**Keywords** are reserved words with special meaning (cannot be used as identifiers). Examples:

`and, or, not, if, elif, else, for, while, break, as, def, lambda, pass, return, True, False, try, with, assert, class, continue, del, except, finally, from, global, import, in, is, None, nonlocal, raise, yield`

---

### Q14. What are literals in Python and what different types exist?

**Answer:**

**Literals** represent fixed values in code:

- **String literals** – `"Hello"`, `'World'`, `"""multi-line"""`.
- **Character literal** – single character string, e.g. `'a'`.
- **Numeric literals** – integers, floats, complex, e.g. `10`, `7.9`, `3+4j`.
- **Boolean literals** – `True`, `False`.
- **Collection literals**:
  - Lists: `[1, 2, 3]`
  - Tuples: `(1, 2, 3)`
  - Dicts: `{1: "apple"}`
  - Sets: `{"A", "B"}`
- **Special literal** – `None` (represents null).

---

### Q15. What are the new features added in Python 3.9?

**Answer (high level):**

- Dict **merge (`|`) and update (`|=`)** operators.
- New string methods: `removeprefix`, `removesuffix`.
- Type hinting improvements for standard collections.
- New parser based on PEG.
- New modules like `zoneinfo`, `graphlib`.
- Various optimizations and deprecations.

---

### Q16. How is memory managed in Python?

**Answer:**

- Python manages memory in a **private heap space**.
- A built-in **memory manager** handles allocation.
- Python has an automatic **garbage collector** to reclaim unused memory (based on reference counting + cyclic GC).

---

### Q17. What is a namespace in Python?

**Answer:**

A **namespace** is a mapping (like a dict) from names to objects, used to avoid name clashes. Examples: built-in, global, local namespaces.

---

### Q18. What is `PYTHONPATH`?

**Answer:**

`PYTHONPATH` is an **environment variable** that specifies additional directories where the interpreter should look for modules when importing.

---

### Q19. What are Python modules? Name some commonly used built-in modules.

**Answer:**

A **module** is a `.py` file containing Python code (functions, classes, variables).

Common built-in modules:

- `os`, `sys`, `math`, `random`, `datetime`, `json`, etc.

---

### Q20. What are local variables and global variables in Python?

**Answer:**

- **Global variables** – declared at the top-level of a module; accessible throughout the file (and modules importing it, if referenced properly).
- **Local variables** – declared inside a function; accessible only within that function.

Example:

```python
a = 2  # global

def add():
    b = 3  # local
    c = a + b
    print(c)  # 5
```

---

### Q21. Is Python case sensitive?

**Answer:**

Yes, Python is **case sensitive** (`Variable`, `variable`, and `VARIABLE` are three different identifiers).

---

### Q22. What is type conversion in Python?

**Answer:**

**Type conversion** converts one data type to another, e.g.:

- `int()`, `float()`, `str()`, `tuple()`, `list()`, `set()`, `dict()`, `complex()`, etc.

Example:

```python
int("10")      # 10
float("3.14")  # 3.14
str(123)       # "123"
```

---

### Q23. How to install Python on Windows and set path variable?

**Answer (summary):**

1. Download installer from `python.org`.
2. Run installer and (optionally) check **“Add Python to PATH”**.
3. If not added automatically:
   - Find install path (e.g. `C:\Python39\`).
   - Add it to **Environment Variables → PATH**.

---

### Q24. Is indentation required in Python?

**Answer:**

Yes. **Indentation is syntactically significant** and defines code blocks (e.g. inside `if`, `for`, `def`, etc.). Wrong indentation causes `IndentationError`.

---

### Q25. What is the difference between Python arrays and lists?

**Answer:**

- **Lists**
  - Can hold elements of **different types**.
  - Built-in, very flexible.
- **Arrays** (from `array` module)
  - Hold elements of **a single type** (e.g. all integers).
  - More memory-efficient for large homogeneous numeric data.

Example:

```python
import array as arr

my_array = arr.array('i', [1, 2, 3, 4])
my_list  = [1, "abc", 1.20]
```

---

### Q26. What are functions in Python?

**Answer:**

A **function** is a reusable block of code defined with `def` and executed only when called.

Example:

```python
def new_func():
    print("Hi, Welcome to Edureka")

new_func()
```

---

### Q27. What is `__init__`?

**Answer:**

`__init__` is the **constructor** method of a class. It is called automatically when a new instance is created and is typically used to initialize attributes.

Example:

```python
class Employee:
    def __init__(self, name, age, salary):
        self.name = name
        self.age = age
        self.salary = salary
```

---

### Q28. What is a lambda function?

**Answer:**

A **lambda** is an **anonymous function** defined with `lambda` keyword, having a single expression.

Example:

```python
add = lambda x, y: x + y
add(5, 6)  # 11
```

---

### Q29. What is `self` in Python?

**Answer:**

`self` refers to the **instance** of the class on which a method is being called. It is the first parameter of instance methods by convention (not a keyword).

---

### Q30. What is the use of `break`, `continue` and `pass` keywords in Python?

**Answer:**

- `break` – exit the nearest enclosing loop.
- `continue` – skip rest of current loop iteration and go to next iteration.
- `pass` – do nothing; used as a placeholder where syntactically some code is required.

---

### Q31. What does `[::-1]` do?

**Answer:**

`[::-1]` is a slice that returns the **reversed** sequence.

Example:

```python
lst = [1, 2, 3, 4, 5]
lst[::-1]  # [5, 4, 3, 2, 1]
```

---

### Q32. How can you randomize the items of a list in place in Python?

**Answer:**

Use `random.shuffle`:

```python
from random import shuffle

x = ['Keep', 'The', 'Blue', 'Flag', 'Flying', 'High']
shuffle(x)
```

---

### Q33. What are Python iterators?

**Answer:**

An **iterator** is an object that implements:

- `__iter__()` – returns the iterator object itself.
- `__next__()` – returns the next value or raises `StopIteration`.

They are used to iterate over containers like lists, tuples, etc.

---

### Q34. How can you generate random numbers in Python?

**Answer:**

Use the `random` module:

```python
import random

random.random()      # float in [0.0, 1.0)
random.randint(1, 10)  # int between 1 and 10 inclusive
```

There are many other helpers: `randrange`, `uniform`, etc.

---

### Q35. What is the difference between `range` and `xrange`?

**Answer (Python 2 context):**

- `range` returns a **list**.
- `xrange` returns an **xrange object** that generates values on demand (like a generator).

In **Python 3**, `range` behaves like old `xrange` and `xrange` no longer exists.

---

### Q36. How do you write comments in Python?

**Answer:**

- Single-line comments use `#`.
- Multi-line documentation is usually done with triple-quoted strings (`""" ... """`) as docstrings.

---

### Q37. What is pickling and unpickling?

**Answer:**

- **Pickling** – serializing Python objects to a byte stream using the `pickle` module.
- **Unpickling** – deserializing the byte stream back to Python objects.

Use only with **trusted data**, as unpickling arbitrary data can execute code.

---

### Q38. What are generators in Python?

**Answer:**

Generators are functions that use `yield` to produce a sequence of values lazily, returning an iterator.

Example:

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1
```

---

### Q39. How will you capitalize the first letter of a string?

**Answer:**

Use `str.capitalize()`:

```python
"edureka".capitalize()  # "Edureka"
```

---

### Q40. How will you convert a string to all lowercase?

**Answer:**

Use `str.lower()`:

```python
"ABCD".lower()  # "abcd"
```

---

### Q41. How to comment multiple lines in Python?

**Answer:**

Prefix each line with `#`, or in many editors select the lines and use a block-comment shortcut. Multi-line docstrings (`"""..."""`) can also serve as documentation but are not technically comments.

---

### Q42. What are docstrings in Python?

**Answer:**

**Docstrings** are string literals that appear as the first statement in a module, function, class, or method definition. They document what the object does and are accessible via `.__doc__` or `help()`.

Example:

```python
def add(a, b):
    """Return the sum of a and b."""
    return a + b
```

---

### Q43. What is the purpose of `is`, `not` and `in` operators?

**Answer:**

- `is` – identity test (`a is b` checks if both refer to the same object).
- `not` – logical negation (`not True` → `False`).
- `in` – membership test (`x in seq`).

---

### Q44. What is the usage of `help()` and `dir()` functions in Python?

**Answer:**

- `help(obj)` – shows the documentation/help for an object, module, function, etc.
- `dir(obj)` – lists attributes and methods of an object (or of the current scope if no argument).

---

### Q45. Whenever Python exits, why isn’t all the memory de-allocated?

**Answer:**

- Objects with **circular references** or referenced from global namespaces may not be immediately freed.
- Memory allocated by the **C runtime** (or extensions) may not be returned to the OS immediately.
- Python relies on its **garbage collector** and the underlying allocator behavior.

---

### Q46. What is a dictionary in Python?

**Answer:**

A **dictionary** is an unordered collection of key–value pairs.

Example:

```python
person = {"Country": "India", "Capital": "Delhi", "PM": "Modi"}
person["Country"]  # "India"
```

---

### Q47. How can the ternary operators be used in Python?

**Answer:**

Python uses a conditional expression:

```python
result = x if condition else y
```

Example:

```python
big = x if x > y else y
```

---

### Q48. What does `*args`, `**kwargs` mean and why use them?

**Answer:**

- `*args` – collects extra **positional** arguments into a tuple.
- `**kwargs` – collects extra **keyword** arguments into a dict.

They are used when:

- You don’t know beforehand how many arguments will be passed.
- You want to forward arguments to another function.

---

### Q49. What does `len()` do?

**Answer:**

Returns the **length** of an object (number of items in list, characters in string, etc.).

---

### Q50. Explain `split()`, `sub()`, `subn()` methods of `re` module.

**Answer:**

- `re.split(pattern, string)` – split string by regex pattern.
- `re.sub(pattern, repl, string)` – replace occurrences of pattern with `repl` (returns new string).
- `re.subn(pattern, repl, string)` – like `sub` but also returns the number of substitutions made.

---

### Q51. What are negative indexes and why are they used?

**Answer:**

Negative indices refer to positions **from the end** of the sequence:

- `-1` – last element.
- `-2` – second last, etc.

They are convenient when accessing or slicing relative to the end.

---

### Q52. What are Python packages?

**Answer:**

**Packages** are namespaces containing multiple modules, usually represented by a directory with `__init__.py` (or namespace packages in modern Python).

---

### Q53. How can files be deleted in Python?

**Answer:**

Use `os.remove`:

```python
import os
os.remove("xyz.txt")
```

---

### Q54. What are the different types of variables in Python OOP?

**Answer:**

Typically:

- **Instance variables** – unique to each instance (`self.var`).
- **Class variables** – shared across all instances (`Class.var`).

(The article also lists Python’s built-in *data types* as “types of variables”.)

---

### Q55. What advantages do NumPy arrays offer over (nested) Python lists?

**Answer:**

- More **efficient** (compact, homogeneous storage).
- Support **vectorized operations** (element-wise arithmetic, etc.).
- Rich set of numerical routines (linear algebra, FFT, statistics).
- Often **much faster** than pure Python loops.

---

### Q56. How to add values to a Python array?

**Answer:**

Using the `array` module:

```python
import array as arr
a = arr.array('d', [1.1, 2.1, 3.1])

a.append(3.4)
a.extend([4.5, 6.3, 6.8])
a.insert(2, 3.8)
```

---

### Q57. How to remove values from a Python array?

**Answer:**

Use `pop` and `remove`:

```python
import array as arr
a = arr.array('d', [1.1, 2.2, 3.8, 3.1, 3.7, 1.2, 4.6])

a.pop()     # removes and returns last element
a.pop(3)    # removes and returns index 3
a.remove(1.1)  # removes first occurrence of value 1.1
```

---

### Q58. Does Python have OOP concepts?

**Answer:**

Yes. Python supports **object-oriented programming**: classes, objects, inheritance, polymorphism, encapsulation, etc. It can also be used in procedural and functional styles.

---

### Q59. What is the difference between deep and shallow copy?

**Answer:**

- **Shallow copy**
  - Copies the **outer container**, but not nested objects (shares references).
  - Changes in nested objects affect both copies.
- **Deep copy**
  - Copies the container **and all nested objects** recursively.
  - Changes in one copy do not affect the other.

Implemented via `copy.copy()` (shallow) and `copy.deepcopy()` (deep).

---

### Q60. How is multithreading achieved in Python?

**Answer:**

- Python has a `threading` module and `concurrent.futures.ThreadPoolExecutor`.
- But CPython has a **Global Interpreter Lock (GIL)**, so only one thread executes Python bytecode at a time.
- Threads are good for **I/O-bound** tasks; for **CPU-bound** tasks use **multiprocessing** or native-code extensions.

---

### Q61. What is the process of compilation and linking in Python?

**Answer:**

Python code is compiled to **bytecode** (`.pyc`) and executed by the interpreter. When extending Python with C/C++:

1. Write extension source file (e.g. `module.c`).
2. Add it to the build (e.g. `Modules/Setup.local`).
3. Rebuild Python or build an extension module.

---

### Q62. What are Python libraries? Name a few.

**Answer:**

Python libraries are collections of modules providing specific functionality, e.g.:

- **NumPy, Pandas, Matplotlib, SciPy, Scikit-learn, Requests, Flask, Django, TensorFlow**, etc.

---

### Q63. What is `split` used for?

**Answer:**

`str.split()` splits a string into a list using a delimiter (default: whitespace).

```python
"edureka python".split()  # ["edureka", "python"]
```

---

### Q64. What are immutable and mutable data types?

**Answer:**

- **Mutable** – can be changed in place (e.g. `list`, `dict`, `set`, `bytearray`).
- **Immutable** – cannot be changed in place (e.g. `str`, `tuple`, `int`, `float`, `bool`, `frozenset`).

---

### Q65. What is the use of `try` and `except` block in Python?

**Answer:**

Used for **exception handling**:

```python
try:
    # code that may raise
    ...
except SomeError:
    # handle error
    ...
else:
    # runs if no exception
    ...
finally:
    # always runs
    ...
```

---

### Q66. What is an ordered dictionary in Python?

**Answer:**

`collections.OrderedDict` preserves **insertion order** when iterating. Since Python 3.7+, the built-in `dict` also preserves insertion order, but `OrderedDict` still offers some extra methods.

---

### Q67. What is the difference between `return` and `yield` keywords?

**Answer:**

- `return` – exits the function **and returns a value**, after which the function cannot resume.
- `yield` – turns a function into a **generator**; it produces a value and suspends execution, which can later resume where it left off.

---

### Q68. What’s the difference between a `set()` and a `frozenset()`?

**Answer:**

- `set` – **mutable**; you can add/remove elements.
- `frozenset` – **immutable** version of a set; hashable and can be used as dict keys or elements of other sets.

---

### Q69. What are the ways to swap the values of two elements?

**Answer:**

Pythonic way:

```python
a, b = b, a
```

---

### Q70. How to import modules in Python?

**Answer:**

```python
import array           # import full module
import array as arr    # import with alias
from array import *    # import everything (not recommended)
from array import array  # import specific name
```

---

## OOP Python Interview Questions

### Q71. Explain inheritance in Python with an example.

**Answer:**

**Inheritance** lets a class (child) derive attributes and methods from another class (parent).

Types:

- Single, multilevel, hierarchical, multiple inheritance.

Example:

```python
class Animal:
    def speak(self):
        print("Some sound")

class Dog(Animal):  # Dog inherits from Animal
    def speak(self):
        print("Bark")
```

---

### Q72. How are classes created in Python?

**Answer:**

Using the `class` keyword:

```python
class Employee:
    def __init__(self, name):
        self.name = name

e1 = Employee("abc")
print(e1.name)
```

---

### Q73. What is monkey patching in Python?

**Answer:**

**Monkey patching** means dynamically modifying a class or module **at runtime**.

Example:

```python
import m

def monkey_f(self):
    print("monkey_f()")

m.MyClass.f = monkey_f
obj = m.MyClass()
obj.f()  # prints monkey_f()
```

---

### Q74. Does Python support multiple inheritance?

**Answer:**

Yes. A class can inherit from **multiple base classes**:

```python
class C(A, B):
    ...
```

---

### Q75. What is polymorphism in Python?

**Answer:**

**Polymorphism** allows objects of different classes to be treated through a common interface (same method name, different implementations).

Example: multiple classes implementing a `speak()` method; code can call `obj.speak()` without caring about the class.

---

### Q76. Define encapsulation in Python.

**Answer:**

**Encapsulation** bundles data (attributes) and methods that operate on that data within a class. In Python, leading underscores (e.g. `_attr`, `__attr`) signal “protected” / “private” usage by convention.

---

### Q77. How do you do data abstraction in Python?

**Answer:**

Using **abstract base classes (ABCs)** and **interfaces** (`abc` module), hiding internal implementation and exposing only necessary methods.

---

### Q78. Does Python make use of access specifiers?

**Answer:**

Python has no strict access modifiers like `public`/`private`; it uses **naming conventions**:

- `_name` – “protected” (internal use).
- `__name` – name-mangled to discourage external access.

---

### Q79. How to create an empty class in Python?

**Answer:**

Use `pass`:

```python
class A:
    pass

obj = A()
obj.name = "xyz"
```

---

### Q80. What does `object()` do?

**Answer:**

`object` is the **base class** for all new-style classes. `object()` returns a new, featureless object instance.

---

## Pandas / Data-related (high level)

The article also includes questions on **Pandas, NumPy, web scraping, data analysis, and code snippets** (Q81–Q127), plus multiple-choice questions (Q128–Q137). For brevity, I have focused this file on the **core language + OOP Q&A**.

If quieres, puedo generar otro archivo separado solo con:

- **Pandas / NumPy / Data Analysis** preguntas (Q81–Q127).
- **MCQ** preguntas con la respuesta correcta marcada (Q128–Q137).

