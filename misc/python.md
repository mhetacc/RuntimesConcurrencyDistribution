*Information repository: all there is to know (for this project at least) on Python. First section is about language in general (conventions, types, etc) while second section is about specific Python modules (like ui or rpcs modules)*

---

# Python Language 

## Conventions

### Naming Conventions

```python
# Comments should start capitalized unless 
# keyword (i will not follow this)

class UpperCamelCase:
    self

# They actually use lowerCamelCase 
# but say it should be avoided
def lowercase_with_underscore():
    """docstring"""
    pass

# same for variables
def _private_fun()
def __very_private_fun()


some_variable = 'Correct'
SomeOtherVariable = 'Correct'
someOtherOtherVariable = 'Wrong'
CONSTANT = 'Correct'


# Line break before binary operator
income = (gross_wages
          + taxable_interest
          + (dividends - qualified_dividends)
          - ira_deduction
          - student_loan_interest)

# import on separate lines
import os
import sys
``` 

### Programming Conventions

Comparison to singletons (like `None`) should always be done with 
- `is`
- `is not`

```python
if __name__ == "__main__":
    print("Hello, World!")
```

Why the above? It's boilerplate code that protects users from accidentally invokin the script ([source](https://stackoverflow.com/questions/419163/what-does-if-name-main-do)).

## Basics

Everything is an object, and therefore has a *class* (also called its *type*). \
It is stored as `object.__class__`

### Assignment

Simple assignment is **always by-reference** and **creates always a new copy** of the referenced object (unless used to "share" references between pointing variables).

```shell
>>> rgb = ["Red", "Green", "Blue"]
>>> rgba = rgb
>>> id(rgb) == id(rgba)  # they reference the same object
True

>>> a = 1
>>> b = a
>>> b is a  # they reference the same object
True
```

Multi line assignment

```python
a, b = 0, 1 
# is equal to
a=1 
b=0

# and also (i don't like it)
a, b = b, a+b 
```

Expression assignment \[Python 3.8]: assign and evaluate (`if true`). \
To be precise:

- assigns value
- returns it

```python
# read chunk and check whether it is empty or not
while chunk := file.read(9000):
    process(chunk)

# could get same result with
chunk = file.read(9000)
while chunk:
    process(chunk)
    chunk = file.read(9000)

# or with do while if we had one
```

### Logical Operations

**Connectives**  

```python
# boolean operators
x and y  
x or y
not x

# bitwise operators
# works only with integers
x & b  # AND
x | b  # OR
x ^ b  # XOR
```

I can do chaining

```python
# following expressions are equivalent
x < y <= z
(x < y) and (y <= z)
```

**Comparisons** 

- By value:
  - `<`
  - `<=`
  - `!=`
  - etc
- By reference (ie pointed object):
  - `is`
  - `is not`
- By class / container:
  - `in`
  - `not in`


### Division

```shell
>>> 8 / 5  # division always returns floating-point
1.6
```

```shell
>>> 8 // 5  # floor division discards fractional
1 
```

### Powers

```shell
>>> pow(5,2)
25
>>> 5 ** 2  # operator ** to calculate powers
25
```

Warning: with operator `**` expressions are evaluated from right to left, so a leftmost `-` will change result sign

```shell
>>> -2**4
-16
>>> pow(-2,4)
16
>>> (-2)**4
16
```

### Strings

Python strings are [immutable](https://docs.python.org/3.12/glossary.html#term-immutable).

Python doesn't have a `char` type, uses instead string objects with length `1`

```python
"this is the same"
'as this'

# escapes
"you need to escape \" but don't for ' "  
# and vice-versa for ' 
```

Out of range strings handled gracefully when **slicing**

```shell
>>> word[4:42]
'on'
>>>word[42:]
''
```

All slice operations return a new list containing the requested elements (ie slice returns a shallow copy)

To append strings the most efficient way is to call `str.join()`

### Unpacking

```python
# packing a tuple
fruits = ("apple", "banana")

# unpacking a tuple
(red, yellow) = fruits

print(red)    # apple
print(yellow) # banana

# operator * matches until end 
*x = fruits
print(x) # ['apple', 'banana']

# operator * matches until reasonable 
vector = (1,2,3,4)
(x, *y, z) = vector

print(y) # [2, 3]
```
Oss: operator * syntax is before variable: `*var` 

Oss2: i can also unpack dictionaries
- `*tuple`
- `**dict`

Often used in positional and by-keyword arguments in functions:
```python
def fun(*posvar, **kwargs)
```

### Performance Evaluation

```python
import time
s = time.perf_counter()
asyncio.run(main())
elapsed = time.perf_counter() - s
print(f"{__file__} executed in {elapsed:0.2f} seconds.")
```

## Flow Control

### if

`elif` and `else` are optional, there is no switch-case statement

```python
if cond:
    # something
elif :
    # something
else:
```

`in` keyword

```python
reply = input('Insert yes or no')
if reply in {'y', 'ye', 'yes'}:
    return True
if reply in {'n', 'no', 'nop', 'nope'}:
    return False
```

### for

Similar to `for each`, iterate on elements of any sequence, contrary to what C does (define iteration step and halt condition)

```python
for w in words:
    print (w)
```

You can also do crazy things like this

```python
# Create a sample collection
users = {'Hans': 'active', 'Éléonore': 'inactive', '景太郎': 'active'}

active_users = {}
for user, status in users.items():
    if status == 'active':
        active_users[user] = status

# basically you can use a sort-of zip() implicitly in the for loop
for key, value in collection.items():
    if key:
        # use value
```

We also have `brake` and `continue` statements, the latter skip to next loop iteration. \
`break` can be paired with `else`: if no break after loop ended, else clause is executed.

### sum

Sum function takes iterable

```python
sum(range(4))  # 0 + 1 + 2 + 3
```
### Functions

```python
def fun(var1, var2='default'):
    """docstring""" # make it habit to use it

fun(0) # calling the function

# I can call also by keyword
fun(0,0) # positional arguments
fun(var1=0, 0) # keyword and positional arguments

# if we need to divide clearly pos/key arguments 
# eg to prevent ambiguity
def foo(name, /, **kwargs)
    return 'name' in kwargs
``` 

Warning: default value is evaluated only once, so aggregators could work strangely

```python
def f(a, L=[]):
    L.append(a)
    return L

print(f(1))
print(f(2))
print(f(3))
```

Will print

```shell
>>>[1]
>>>[1, 2]
>>>[1, 2, 3]
```

## Data Structures 

### List

Can be used as array, stack, queue, everything

```python
# list comprehension 
from math import pi
[str(round(pi, i)) for i in range(1, 6)]

# ['3.1', '3.14', '3.142', '3.1416', '3.14159']
# i don't like this
```

But thankfully there exists built-in functions instead of complex flow statements

```python
[[row[i] for row in matrix] for i in range(4)]

# this produces
# [[1, 5, 9], [2, 6, 10], [3, 7, 11], [4, 8, 12]]

# and is equivalent to
transposed = []
for i in range(4):
    transposed_row = []
    for row in matrix:
        transposed_row.append(row[i])
    transposed.append(transposed_row)

# or we can use zip
list(zip(*matrix))

# which produces
# [(1, 5, 9), (2, 6, 10), (3, 7, 11), (4, 8, 12)]
```

`zip(*iterables, strict=False)` \
Iterates over several iterables in parallel, producing tuples with an item from each one.\
By default it stops once shortest iterable is exhausted.\
With `strict=True` an `ValueError` exception is raised if one iterable is exhausted before the others.

```python
list(zip(range(3), ['fee', 'fi', 'fo', 'fum']))

# [(0, 'fee'), (1, 'fi'), (2, 'fo')]
```

`pop` vs `del`

```python
vec = [1, 2]
vec.pop()  # return value
del vec[0] # delete by index

# delete by slices
vec = [1, 2, 3, 4]
del vec[1:3]

# [1]
```

### Set

Unordered collection without duplicates

```python
set1 = {1,2,3}
empty_set = set()
```

## Modules

*file.py* is a module

I can import a module into other modules (or in the interpreter cmd)

```shell
>>> from my_class import method1
>>> method1(0,0)

# some output
```

### dir()

`dir()` function prints which names a module defines. \
Without arguments it lists the name defined in the current session.

### Packages

Higher directory level for collection of modules. \
Use dot notation. \
There **must** be a *\__init__.py* to make Python treat a directory as a package.

## Input and Output

The standard output file is `sys.stdout`

### Formatting 

By prefixing either `f` or `F` i can insert variables directly into strings by using curled brackets

```python
var1 = 0
var2 = 1
f'Variables are {var1} and {var2}'
```

Expressions inside brackets can be further formatted

```python
# minimum number of characters
# useful to line up columns
f'{name:10} ==> {phone:10d}'

# auto to-string
f'{var!s}'

# using dict 
table = {
    'first' : 1352,
    'second' : 8462,
    'third' : 7401
}

print('{first:d}, {second:d}, {third:d}'.format(**table))
# 1352, 8462, 7401
```

### To String

Function `str()` translates any object in a somewhat human readable string

```python
var1 = 'something'
str(var1)
```

### Reading and Writing Files

`open()` returns a *file object* 

```python
mode = 'w'  # r for reading
            # a for appending

f = open('filename', mode, encoding="utf-8")
```

Closing the file can be done in two main ways

```python
# BETTER: using with keyword automatically closes the file 
with open('file') as f:
    read_data = f.read()

f.closed # True

# otherwise call close function
# can make stuff mis-behave 
f = open('file')
read_data = f.read()
f.close()
```

A *very* nice way to read is to loop each line

```python
for line in f:
    print(line, end='')
```

To write the syntax is similar: `f.write('Some line\n')`

## Errors and Exceptions

`except` can have an optional `else` clause that gets executed if `try` does **not** raises an exception

```python
for arg in sys.argv[1:]:
    try:
        f = open(arg, 'r')
    except OSError:
        print('cannot open', arg)
    else:
        print(arg, 'has', len(f.readlines()), 'lines')
        f.close()
```

I can also force `raise` specified exceptions

```python
raise NameError('HiThere')
```

### Multiple Unrelated Exceptions

[8.9](https://docs.python.org/3.12/tutorial/errors.html#raising-and-handling-multiple-unrelated-exceptions): sometimes several exceptions occurs, this is often the case in concurrency frameworks. \
[ExceptionGroup](https://docs.python.org/3.12/library/exceptions.html#ExceptionGroup) wraps a list of exception instances so that they can be raised together.

## Classes

- [...] nothing in Python makes it possible to enforce data hiding, it is all based upon convention.
  
- By default class members are *public* and all member functions are *virtual*.

- [...] *aliases* behave like pointers in some respects. For example, passing an object is cheap since only a pointer is passed. 

- [...] all operations that introduce new names use the local scope: in particular, `import` statements bind the module name in the local scope.

- Assignments do not copy data, they just bind names to objects. The same is true for deletions: `del x` just removes binding of `x` from the local scope. 

- **everything is a pointer**

```python
class MyClass:
    class_variable = 'I am shared by all instances'

    # Oss: self is not a keyword
    # it is the pointer to the object itself
    # must be made explicit 
    def __init__(self, name):
        self.instanceName = name 
```

### Cosa Stampa - Scope

```python
def scope_test():
    def do_local():
        spam = "local spam"

    def do_nonlocal():
        nonlocal spam
        spam = "nonlocal spam"

    def do_global():
        global spam
        spam = "global spam"

    spam = "test spam"

    do_local()
    print("After local assignment:", spam) # test spam

    do_nonlocal()
    print("After nonlocal assignment:", spam) # nonlocal spam

    do_global()
    print("After global assignment:", spam) # nonlocal spam   <--- OSS
                                            # more-local scope takes precedence 

scope_test()
print("In global scope:", spam) # global spam
```

Scope Modifiers:
- None: default local scope
- `nonlocal`: local of father (i.e. closest outside scope)
- `global`: holds for entire current code block

**Nearer** scope always has **precedence**: 
local > non local > global

### Constructor

```python
class Class:
    def __init__(self, data):
        self.data = data
```

**Warning**: instance variables are named and created only inside `__init__`

```python
class Dog:
    genus = 'Canis' # class variable
                    # shared by all instances

    def __init__(self, name):
        self.name = name # unique to each instance
```

This could lead to very bad very fast


```python
class Container:
    elements = []  # SHARED by all containers

    def __init__(self, id):
        self.id = id
    
    def push(self, element):
        self.elements.append(element)
```

There are some other ways besides scope to access parent's stuff

```python
# returns a proxy object to access parent class of type
super().parent_method()

# or call explicitly name of parent
ParentClass.parent_method()

```

### Methods

[...] the special thing about methods is that the instance object is passed as the first argument of the function

```python
# the two following lines are equivalent
x.f()
MyClass.f(x) 

# we call f() of class MyClass on object x
```

Often, the first argument of a method is called `self`. This is nothing more than a convention: the name `self` has absolutely no special meaning to Python

### Private Variables

They don't exists, but by convention `_variable` should be treated as such.

Any identifier in the form `__var` is textually replaced by `_className_var` to help privacy of variables.

### Iterators

We can manually reproduce `for` loop behavior with `iter()` and `next()` functions

```python
string = 'abc'

for w in string:
    print(w)
# abc

# or we can explicitly do it
iterator = iter(string)
next(iterator) # a
next(iterator) # b
next(iterator) # c
next(iterator) # StopIteration exception
```

Therefore, we can add iterator behavior to our custom classes 

```python
class Reverse:
    """Iterator for looping over a sequence backwards."""
    def __init__(self, data):
        self.data = data
        self.index = len(data)

    # implement iterator function
    def __iter__(self):
        return self

    # implement next function
    # returns and decrement index
    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.data[self.index]
```

We can then use `Reverse` with a `for` directly

```python
rev_string = Reverse('suck')

for char in rev_string:
    print(char)

# the opposite of suck which
# as we all know is kcus 
```

### Generators

All this above mentioned stuff with `__iter__()` and `__next__()` can be done automagically with `yield` statement. \
It is a sort of `return` but it resumes where it left off each time `next()` is called on it.

```python
def reverse(data):
    for index in range(len(data)-1, -1, -1):
        yield data[index] # returns data and resumes from index next time
```

## Virtual Environments and Packages

### venv 

Virtual Environment: self-contained directory tree that contains a Python installation for a particular version of Python, plus a number of additional packages.

### pip

Display all installed packages

`python -m pip list`

Display information about a specific package

`python -m pip show package_name`

Upgrade all packages

`python -m pip install --upgrade`

## Miscellaneous 

### Explicit Line Joining

Backslash allows to break line without logical break

```python
if 1900 < year < 2100 and 1 <= month <= 12 \
   and 1 <= day <= 31 and 0 <= hour < 24 \
   and 0 <= minute < 60 and 0 <= second < 60:   
        return 1
```

### Operators

```
+       -       *       **      /       //      %      @
<<      >>      &       |       ^       ~       :=
<       >       <=      >=      ==      !=
```

### Delimiters

```
(       )       [       ]       {       }
,       :       !       .       ;       @       =
->      +=      -=      *=      /=      //=     %=
@=      &=      |=      ^=      >>=     <<=     **=
```

## Vulnerabilities Avoidance 

### Top avoidance mechanisms in Python

1. Use type annotations
2. if a function has to update `global` object clearly states `global` variables 
3. Always use named exceptions
4. Most operations on non-integers can go bad
5. Protect all data shared between threads with locks
6. Avoid mixing concurrency models
7. Avoid external termination of concurrent entities

### Scope

`global` should be avoided, it is generally a bad programming practice.

`global` keyword is only needed when modifying (i.e., assign) a variable:

```python
var = 1

def fun():
    global var
    var = 2

fun()
print(var) # 2
```

If `global` not specified assignment is local:

```python
var = 1

def fun():
    var = 2

fun()
print(var) # 1
```

Using **wildcards** in `import` statement make only the last one stick:

```python
from moduleA import * # ignored
from moduleB import *
```

Local names are defined statically by looking for assignment, if only reference is found then the variable its assumed to be global:

```python
a = 1

def fun():
    print(a) # local
    a = 2

def fun():
    print(a) # global
```

### Type Hints

Allow a sort-of static typing and allow static type check with third party tools

```python
def function(var1, var2):
    return 0

# prefer to do this instead
def function(var1: int, var2: float) -> int:
    return 0


#ie
def function(variable: VarType) -> ReturnType:
    pass
```

### Strings

Simple strings are memory-optimized, if this is needed for non simple ones use `intern()` i.e., for the same string use same memory space:

```python
str = intern('non simple string')
```

### Inheritance

If a class have operation-handling methods ensure that `Py_NotImplemented` and `TypeError` exceptions are handled.

Forbid altering `__class__` attribute of instances.


### Mutable and Immutable Objects

`a = a + 1` always creates a new object (with both mutables and immutables)

Do not assign mutable objects as default values: they are created only at function definition:

```python
def fun (y=[]):
    y.append(1)

fun()
fun()
fun()
print(y) # [1, 1, 1]
```

Immutables can be modified if declared as global:

```python
def mutate(var):
    global var
    var = var * 2

var = 1 
mutate(var)
print var() # 2
```

Copies should be created when passing mutables to a function if we don't want them to be modified.

### Iteration

Modify a list inside a loop updates its own iterator:

```python
vec = [1]

for num in vec:
    if num == 1:
        vec += 2
    if num == 2: # iterator has updated already
        vec += 3

print(vec) # [1,2,3]
```

To prevent this is better to iterate on a copy of the list:

```python
vec = [1]
for num in vec[:]:
    #do stuff
```

In general don't use `for` a la C, as in do not update iterator inside:

```python
for i in range(1,5):
    print(i)
    i = 10
# out: 1, 2, 3, 4
```

Loop will always end in the "normal" way: `i<n`

### Concurrency

§5.1.7: "[...] **multithreading** can still be useful in situations where the CPU becomes idle such as in I/O-bound applications" but its important to handle thread exceptions, and make sure each thread is only started once.

A `daemon` thread never terminates until the program ends

If a child thread has already started, attempting to start it again will result in an exception. Can lead to deadlock.

`ThreadPoolExecutor` can be used to allocate a predetermined number of available threads. Can be helped with `concurrent.futures` module. 
It should be destroyed not relying only on Python's own garbage collector (pool's finalizers may not be called).\
Same story for `multiprocess.pool`: call explicitly `close()` or `terminate()` or use a context manager.

Create and destroy threads has a significant overhead.

Threads should be waited to terminate (they terminate themselves) using `join()`.

If a `process` contains a `pipe` and multiple `threads` try to access it, there is a risk of data corruption.

## Parallelism

Threading vs Multiprocessing

https://medium.com/@me.mdhamim/a-comprehensive-guide-to-python-threading-advanced-concepts-and-best-practices-9f3aea6f0a63

- Utilize threading to send concurrent HTTP requests and maximize the use of available network bandwidth.
- A CPU-intensive task, such as image processing or numerical computation, needs to [...] leverage multiprocessing to run tasks concurrently in separate processes.

While Python’s Global Interpreter Lock (GIL) limits true parallelism for CPU-bound tasks in CPython, threading remains effective for I/O-bound and asynchronous operations.


https://stackoverflow.com/questions/3044580/multiprocessing-vs-threading-python

Threads run in the same memory, allowing sharing of memory, while processes are isolated.

- Multiprocessing:
  - Pros
    - multi-core speed up
    - no memory sharing so no race condition
    - good for CPU-bound applications
  - Cons
    - IPC communication model a bit more complicated
    - larger memory footprint
- Threading:
  - Pros
    - lightweight
    - easy to access state due to memory sharing
    - good for I/O bound applications
  - Cons
    - CPython ie GIL
    - race conditions more likely
    - code harder to understand 

### Concurrency and Parallelism
https://www.youtube.com/watch?v=0kXaLh8Fz3k&t=630s

We can utilize `multiprocessing` and `asyncio` at the same time since they are quite complemental with each other. We need to create a new async loop for each process.

```python
async def run_loop(work_queue, result_queue):
    while True:
        # actual work here

# we need to bootstrap-it otherwise it wont work
def bootstrap (work_queue, result_queue):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_loop(work_queue, result_queue))

def main():
    process = multiprocessing.Process(
        target=bootstrap,
        args=(work_queue, result_queue)
    )

process.start()  # actually starts the process
```

With https://github.com/omnilib/aiomultiprocess we can use the multiprocessXasync stuff without having to do it ourself:

```python
from aiomultiprocess import Pool

async def fetch_url(url):
    return await aiohttp.request('GET', url)

async def fetch_all(urls):
    # same syntax of multiprocess.Pool
    async with Pool() as pool:
        results = await pool.map(fetch_url, urls)
```

# Python Modules

## Logging (debug)
`logging` module: https://docs.python.org/3/library/logging.html

Standard module to logs stuff

Logging is performed by calling methods on instances of the `Logger` class 

### Basics

Oss: `__name__` as in "the name of the logger file we want to create eg `my_logger`

```python
import logging

logging.basicConfig(**kwargs) # a dict of attribute passed by keyword 
# e.g. filename : 'name'
#      filemode : 'w'

logger = logging.getLogger(__name__)

logger.debug('Debug message')
logger.info('Info message')
logger.warning('Warning message')
logger.error('Error message')
```

Some basic config could be

```python
logging.basicConfig(filename='myLog.log')
# this should append all logs in file myLog

logging.basicConfig(filename='myLog.log', filemode='w')
# while this should re-write it every time

logging.basicConfig(format='%(asctime)s %(message)s')
# this would append datetime at the start of every logged string
```

To embed variables and such

```python
logging.warning('%s and %s', var1, var2)
# var1 and var2
```

Log events gets passed around in a `LogRecord` instance 

Root logger is top-hierarchhy of loggers, is used by core function (eg `debug()` or `error()`)

```python
logger = logging.getLogger(__name__)

# root logger
# name is 'root' in output
```

### Ideal Structure 
- RuntimesConcurrency
  - misc
  - logs
    - script1
      - datetime_s1.log
      - datetime_s1.log
      - datetime_s1.log
    - script2
      - datetime_s2.log
  - some other folder

### Handlers

Handlers send log records to appropriate destination

Should not use `Handler` directly, instead use as interface for child custom handlers, like the following useful `Handlers`:

- `FileHandler`: send messages to disk files
- `RotatingFileHandler`: to disk files, support max log sizes and file rotation
- `StreamHandler`: send to stream (file-like objects)

**FileHandler:**

```python
class logging.FileHandler(filename, mode='a', encoding=None, delay=False, errors=None)

# specified file is opened and used for logging
# by default, file grows indefinitely
# Path object are accepted in filename argument
```

So as far as i can tell, to get what I want, i need:

- [datetime](https://docs.python.org/3/library/datetime.html#datetime.datetime.today)
- [Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path)
- [FileHandler](https://docs.python.org/3/library/logging.handlers.html#logging.FileHandler) 

```python
from pathlib import Path
import logging

# basic config is skipped since all is done with specific thingies 

filename = 'script1'

# create logger
logger = logging.getLogger(__name__)

log_path = Path(f'../logs/{datetime.now()}.{filename}')

# create log file handler
filehandle = logging.FileHandler(log_path, encoding = 'utf-8')

logger.addHandler(filehandle)
```

### Configuration

Three ways to configure logging:
- explicitly in Python code
- create config file and use `fileConfig()`
- create config dictionary and use `dictConfig()`

```python
logging.config.fileConfig('logging.conf')
```

Warning: `fileConfig()` has default parameter which will cause any pre-existing non-root loggers to be disabled, unless explicitly named in the Configuration

```python
fileConfig(disable_existing_loggers = True) # can call it False
```

## Queues and Logs (data) 

### list
https://docs.python.org/3.12/library/stdtypes.html#list

Standard Library module to make lists (standard is good). Is a mutable sequence type (and we need it to mute).

### queue
https://docs.python.org/3.12/library/collections.html#collections.deque

 Deques support thread-safe, memory efficient appends and pops from either side of the deque with approximately the same O(1) performance in either direction.

### deque 
https://docs.python.org/3.12/library/queue.html#module-queue

The queue module implements multi-producer, multi-consumer queues. It is especially useful in threaded programming when information must be exchanged safely between multiple threads.

## xmlrpc 

To do remote procedure calls Python provides a core library module called ``xmlrpc``. 

### Start a localhost server

```shell
python -m http.server port
```

If you want it in a specific directory

```shell
cd /my_dir
python -m http.server 8080
```

### ServerProxy 

A `ServerProxy` instance is an *object* that manages communication with a remote XML-RPC server.

```python
import xmlrpc.client

proxyobject = xmlrpc.client.ServerProxy(
    uri,                # target, usually server URL 
    *defaultOK,         # some values that are ok to leave as is
    allow_none = True,  # translates None in XML, otherwise TypeError exception is raised
    headers = (),       # Py 3.8 and above, allows HTTP headers to be included
)
```

Lets see an example client-side

```python
import xmlrpc.client

with xmlrpc.client.ServerProxy(
    'http://localhost:8080/',   # target, server URL and port
    allow_none = True,          # translates XML
    ) as proxyobject            # automatically closes resource when not in use anymore

# use RPC i.e. make a request to the server to return
# a value as if it was a local function, parameters and all
print(proxyobject.function_name(42))

# prints 'The number is 42'
```

On the server-side

```python
from xmlrpc.server import SimpleXMLRPCServer

def server_function(n):
    return f'The number is {n}'

# create server on localhost, port 8000
server = SimpleXMLRPCServer (('localhost', 8000))

# register the function in the server 
# and gives it a callable name
# as usual it is good practice to use with
server.register_function(server_function, 'function_name')  # (name, callable name) tuple
                                                            # maybe better if they are the same idk
server.serve_forever()  # idk
```

### Fault Objects

A `Fault` object encapsulates an XML-RPC fault tag, it has:

- `faultCode`: `int` indicates fault type
- `faultString`: contains diagnostic message

It is needed in cases of type problems and such, so we *should* be safe since all we intend to pass around are strings or dictionaries.

### ProtocolError 

A `ProtocolError` object is like *"404 not found"*, i.e. problems in the underlying transport layer. \
It has the following attributes:

- `url`: who triggered the error
- `errcode`: error type
- `errmsg`: diagnostic string
- `headers`: HTTP requests that triggered the error

They are propagated automatically by the server, and handled by the client

```python
import xmlrpc.client

# server that does not respond to XMLRPC requests
proxy = xmlrpc.client.ServerProxy("http://google.com/")

# protocol errors are exceptions
try:
    proxy.some_method()                         # some.method() didnt work
except: xmlrpc.client.ProtocolError as error:   # so a error has been caught
    print(f'Error URL: {error.url}')
    print(f'Error code: {error.errocode}')
    print(f'Error message: {error.errmsg}')
```

### SimpleXMLRPCServer

A `SimpleXMLRPCServer` object provides a means to create a basic sand alone XML-RPC server. 

```python
# Constructor

xmlrpc.server.SimpleXMLRPCServer(
    addr,  # ('url', port)
    requestHandler=SimpleXMLRPCRequestHandler,
    **kwargs,
)
```

Method `register_function` expose functions that can respond to XML-RPC requests

```python
server.register_function(
    fun_name,
    "function",     # if not provided function.__name__ 
                    # will be used instead
                    # in this case it will be fun_name
)
```

Method `register_instance` expose an object to call its methods.

PROBLEM: can the server forward messages to the clients? Only time will tell, some sparse ideas:

- server create a response to a non-existent request
- use explicit modules like tpc (is it still an rpc a that point?)

### Mixed Approach

Since `xmlrpc.server` only exposes functions to be called by a `xmlrpc.client`, which in turns can only call exposed functions, a Raft node cannot be either. But it can be both i.e. 

```python
# server without exposed functions
with SimpleXMLRPCServer (('localhost', 8080)) as server:

    # client inside server
    with xmlrpc.client.ServerProxy('http://localhost:8080', allow_none=True) as proxy:
        print(proxy.test_foo(42))


    server.serve_forever()
```

Oss: if `serve_forever()` use client inside `service_actions()` or set `Timeout = None`.

Advantages of this approach:
- `xmlrpc` does everything by itself:
  - establish server
  - expose functionality 
  - handle common tcp errors
- no need to use `socket.socket()` directly
- `xmlrpc` is a standard library module hence great compatibility
- actually uses rpcs since I didn't made the module
- mixed server/client means that nodes are real servers
  - coherent to Raft specifications
  - future expandability: they can be enhanced to expose whatever  
  - long lived

### socketserver.TCPServer

`SimpleXMLRPCServer` extends class `socketserver.TCPServer` hence can use its functionalities.\
It is synchronous: each request must be completed before the next can be started (should be fine for Raft specs)

#### serve_forever(poll_interval=0.5)

Handle requests until explicit `shutdown()` (not necessary if used `with`). Poll for shutdown every *poll_interval* seconds. 

Ignores `timeout` attribute hence server does not shuts down automatically.

Loops on `service_actions()`

#### service_actions()

> added in version 3.3
Called in the `serve_forever()` loop, can be overridden.

#### shutdown()

Stops `serve_forever()` loop and wait until it is done.

If `serve_forever()` is running in the same thread it will deadlock.

#### timeout

Measured in seconds, can be set to `None`

## asyncio

Library to write concurrent code, it provides high level APIs to:

- run Python coroutines concurrently and have full control over them
- perform network I/O and IPC
- control subprocesses
- distribute tasks via queues
- synchronize concurrent code

Additionally provides low level APIs to:

- create and manage event loops
- implement efficient protocols using transports
- bridge callback-based libraries

**Oss:** synchronous code **should not call** asynchronous code: it would become synchronous instead (but its fine vice-versa).

**Oss:** `await` pauses enclosing coroutine(s) and yields control back to the event loop so that it can let other "ready" coroutines run. Every coroutine should be awaited, i.e. an asynchronous function should always be called with `await` keyword.

https://stackoverflow.com/questions/55647753/call-async-function-from-sync-function-while-the-synchronous-function-continues\
Credit: [user4815162342](https://stackoverflow.com/users/1600898/user4815162342) (top 350 user)\
*Concurrency doesn't always mean a new thread **if** you use coroutines (async def) for all your code. But your requirement is to have a sync function executed concurrently with async code, and that will certainly require multiple threads or fibers* [...]
*new_event_loop only allocates an event loop. To actually run async code in it, you must use run_until_complete or run_forever, which blocks the current thread - so you need an additional thread to run sync code concurrently with async code. It will never work without threads.*

Credit: [Mikhail Gerasimov](https://stackoverflow.com/users/1113207/mikhail-gerasimov)\
*asyncio can't run arbitrary code "in background" without using threads. As user4815162342 noted, in asyncio you run event loop that blocks main thread and manages execution of coroutines.*\
*If you want to use asyncio and take advantage of using it, you should rewrite all your functions that uses coroutines to be coroutines either up to main function - entry point of your program. This main coroutine is usually passed to run_until_complete.*

https://realpython.com/async-io-python/
Simply putting async before every function is a bad idea if all of the functions use blocking calls. [...]\
Threading also (tends) to scale less elegantly than async IO, because threads are a system resource with a finite availability. Creating thousands of threads will fail on many machines, and I don’t recommend trying it in the first place. Creating thousands of async IO tasks is completely feasible.

Async IO shines when you have multiple IO-bound tasks where the tasks would otherwise be dominated by blocking IO-bound wait time, such as:

- **Network IO, whether your program is the server or the client side**
- Serverless designs, such as a peer-to-peer, multi-user network like a group chatroom
- Read/write operations where you want to mimic a “fire-and-forget” style but worry less about holding a lock on whatever you’re reading and writing to

**Oss:** not sure it can be used with `xmlrpc`. It should not work with `sockets`.



### Concurrent Tasks

`TaskGroup()` may be useful to register ACKs of heartbeat

```python
async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(some_coroutine(...))
        task2 = tg.create_task(another_coroutine(...))
    print(f"Both tasks have completed now: {task1.result()}, {task2.result()}")
```

~~We also have `gather(*awaitables)` that runs all passed awaitables concurrently, then returns an aggregate list of returned values.~~ 
<span style="color:red">*deprecated since 3.10*</span>.

### Looping Task

<span style="color:red">*Deprecated since 3.10:* warning is emitted if *loop* is not specified and there is no running event loop.</span>

Task Objects can be used to run coroutines in event loops (not thread-safe).

```python
class asyncio.Task(coroutine, *, loop=None, name=None, context=None, eager_start=False)
```

Exposes some nice function: 

- `add_done_callback(callback, *, context=None)`
- `result()`: if Task is done, result wrapped in coroutine and returned
- `done()`: `True` if Task is done
- `cancel(msg=None)`

### Wait

`asyncio.sleep(t)` allow to have a non-blocking delay function.

`asyncio.timeout(t)` limits the amount of awaitable time of another async task. Its probably better to use the form

```python
asyncio.wait_for(awaitable, timeout)
```

### Streams

High level async/await primitives for networking. Can be used with bot TCP and HTTP.\
Since we use `xmlrpc` all of this should be lower level. 

```python
async def tcp_echo_client(message):
    # creates TCP connection
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888)

    # sends message to server
    print(f'Send: {message!r}')
    writer.write(message.encode())
    await writer.drain()

    # wait on server response
    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    # close connection
    print('Close the connection')
    writer.close()
    await writer.wait_closed()


asyncio.run(tcp_echo_client('Hello World'))
```

### Synchronization Primitives

Non-thread-safe sync stuff for asyncio.

- `Lock`: mutex lock
- `Event`: awaitable flag
- `Condition`: event with extra steps
- Semaphores and barriers

### Event Loop

```python
loop = asyncio.get_running_loop()

# run until stop()
loop.run_forever()

# stop event loop
loop.stop()

# True if running
loop.is_running()

# callback to be called at next loop iteration
# returns asyncio.Handle object
handle = loop.call_soon(callback, *args)

# cancel callback
handle.cancel()

# True if cancelled callback
handle.cancelled()

# absolute timestamp of scheduled callback
handle.when()
```

### Future 

<span style="color:red">*Deprecated since 3.10*: warning is emitted if loop is not specified and there is no running event loop</span>.

```python
# awaitable object
future = asyncio.Future(*, loop=None)

# mark as done and set result=result
future.set_result(result)

# add callback to be run once future is done
future.add_done_callback(callback, *)

# return True if is done
future.done()
```

### Timers

Contributors:
- https://github.com/zhebrak/raftos/blob/c51e14433e06046db0cf3cb83429b07aed01861f/raftos/timer.py#L4
- https://stackoverflow.com/questions/45419723/python-timer-with-asyncio-coroutine
- 

*Question: "What is the correct way to set a non-blocking timer, that will call a callback function after some number of seconds? Being able to cancel the timer would be a bonus but is not a requirement."*

Creating `Tasks` using `ensure_future` is a common way to start non-blocking jobs. There is also the option to `cancel` a task.

```python
class Timer:
    def __init__(self, timeout, callback, args=None, kwargs=None):
        self._timeout = timeout
        self._callback = callback
        self._task = asyncio.ensure_future(self._wait_and_call())
        self._args = args if args is not None else []
        self._kwargs = kwargs if kwargs is not None else {}

    async def _wait_and_call(self):
        """Wait timeout seconds, then call callback(*args)"""
        await asyncio.sleep(self._timeout)
        await self._callback(*self._args, **self._kwargs)

    def cancel(self):
        self._task.cancel()
```

Then the callback function should be a coroutine:

```python
async def callback():
    print('echo!')
```

How to make it work then:

```python
async def main():
    timer = Timer(2, callback)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
try:
    loop.run_until_complete(main())
finally:
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()
```

The above implementation has one caveat: calling `cancel()` cancels both:

- the timer
- the callback: if `cancel()` called **after** `timeout` but actual job still in progress

Alternative approach uses `loop.call_later`:

```python
loop = asyncio.get_event_loop()
timer = loop.call_later(5, lambda: asyncio.ensure_future(job()))

# cancel timer but not job() if already started
timer.cancel()
```

What could `job()` be:

- `heartbeat()`
- `start_election()`

Here follows a different `Timer` implementation that uses `call_later()` instead:

```python
class Timer:
    """Scheduling periodic callbacks using handler"""
    def __init__(self, timeout, callback, args=None, kwargs=None):
        self._timeout = timeout
        self._callback = callback
        self._args = args if args is not None else []
        self._kwargs = kwargs if kwargs is not None else {}
        self._loop = asyncio.get_event_loop()
        # self._handler gets created on start() only


    def _get_timeout(self):
        return self._timeout() if callable(self._timeout) else self._timeout

    def _run(self):
        """Fire callback then restarts timer"""
        self._callback(*self._args, **self._kwargs)
        self._handler = self._loop.call_later(self._get_timeout(), self._run)



    def start(self):
        self._handler = self._loop.call_later(self._get_timeout(), self._run)

    def stop(self):
        self._handler.cancel()

    def reset(self):
        self.stop()
        self.start()
```

Then on the callback it is used as:

```python
class State:
    def to_follower(self):
        self._change_state(Follower)
        self.set_leader(None)
        if asyncio.iscoroutinefunction(config.on_follower):
            asyncio.ensure_future(config.on_follower())
        else:
            config.on_follower()

###################

class Leader:
    def heartbeat(self):
        self.request_id += 1
        self.response_map[self.request_id] = set()
        asyncio.ensure_future(self.append_entries(), loop=self.loop)

####################

class Configuration:
    def default_settings():
        return{
            'on_follower`: lambda:None
        }

```

### Custom Awaitable

To create an awaitable class i just need to implement `__await__` method:

```python
class MyAwaitable:
    def __await__(self):
        yield       # pause until
        return 42
```

Using `yield` should makes us remember that coroutines are basically glorified generators.

## threading

This project will need thread-based parallelism for two main reasons:

- Game loop and Raft's node-loop must be alive at the same time (both `while True`)
- Raft nodes needs a timer, and `time.sleep(t)` is a less than ideal solution since its a blocking one

Due to CPython implementation, specifically [global interpreter lock](https://docs.python.org/3/glossary.html#term-global-interpreter-lock), we cannot use parallelism to computational speed-up (only one thread can run at the time) but we can still manage to have non-locking properties.

Some useful methods:

- `get_native_id()`: returns kernel-assigned thread ID
- `enumerate()`: returns list of all thread objects currently active
- `is_alive()`: checks if thread is alive

### Thread Objects

A `Thread` represents an activity that is run and controlled in its own thread, and the activity can be specified in two ways:

1. pass a callable object to the constructor
2. subclass and override `run()` method

No other method (except constructor) should ever be overridden.\
Once created, a thread object's activity must be started with `start()`, which invokes `run()`. Each thread has a `name` attribute.

```python
threading.Thread(
    group=None,
    target=None,    # callable object
    name=None,      # by default construct "Thread-N"
    args=(),
    kwargs={},
     *,
    daemon=None
)
```

#### Pass function to a Thread

```python
# enclose server in a callable function
def handle_server():
    with SimpleXMLRPCServer(('localhost', 8080), allow_none=True) as server:
        def just_return(value):
            return value
        
        server.register_function(just_return)
        server.serve_forever()


# pass all server stuff to a separate thread
threading.Thread(target=handle_server).start()
```

### Timer

```python
threading.Timer(
    time,        # expire time in seconds
    callback,    # name of function to call once expired
    *args,       # callback's arguments
    **kwargs     # callback's kwarguments
)
```

Timer does **not** loop: it jus starts a timer in a separate thread.

```python
# create a simple timer with callback
import threading

# after time t callback will be called
timer = threading.Timer(t, callback)
timer.start()
```

Timer code is like this:

```python
# not complete code, just what is needed
class Timer(Thread):

    def __init__(self, countdown, callback):
        Thread.__init__(self)
        self.interval = countdown
        self.function = callback
        # uses event class to wait, set and check a flag
        self.finished = Event()     


    def run(self):
        # wait the amount of specified time with
        # Event() (basically flag with locks)

        # returns internal flag on exit, which is 
        # False if timeout is given and operation times out
        self.finished.wait(self.interval)


        # flag false if wait times out
        if not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
        self.finished.set()
```

### Resource Sharing

https://www.geeksforgeeks.org/python-communicating-between-threads-set-1/
Perhaps the safest way to send data from one thread to another is to use a Queue from the queue library. To do this, create a Queue instance that is shared by the threads. Threads then use put() or get() operations to add or remove items from the queue.

https://www.reddit.com/r/learnpython/comments/1at6fnv/easiest_method_to_communicate_between_threads/
Queues are great for that. 

https://medium.com/@me.mdhamim/a-comprehensive-guide-to-python-threading-advanced-concepts-and-best-practices-9f3aea6f0a63
The use of a queue ensures that the communication is thread-safe.


#### queue

The [queue](https://docs.python.org/3/library/queue.html#module-queue) module implements multi-producer, multi-consumer queues. It is especially useful in threaded programming when information must be exchanged safely between multiple threads. The Queue class in this module implements all the required locking semantics.

## multiprocessing

Oss: there is no analogue to `threading.Timer`.

In `multiprocessing` processes are spawned using a `Process` object, which follows the API of `threading.Thread`:

```python
def handle(data):
    print(f'Something and {data}')

process = multiprocessing.Process(target=f, args=('something else',))
thread = threading.Thread(target=f, args=('something else',))

process.start() # print `Something and something else`
thread.start()  # print `Something and something else`

# close both process and thread 
# can be bypassed with `with` keyword
process.join()
thread.join()
```

I can make a process daemonic. It will be destroyed once parent process dies and i cannot spawn child processes. 

```python
process.daemon = True
process.start()
```

There are three starting methods:

- `spawn`: slowest, starts fresh Python interpreter. Available on all systems, default on Windows and MacOS 
- `fork`: clone parent process, problematic to safely forking a multithreaded process. Available and default on POSIX except macOS 
- `forkserver`: safest and quite efficient. Available only POSIX with support of file descriptor passing over Unix pipes (like Linux).

Better to let the system decides since forcing one could prevent compatibility or performance speed up.

### Message Passing

When using multiple processes it is generally advised to use message passing instead of synchronization primitives.

- `Pipe()` for connection between two processes
- `Queue()` if multiple producers and consumers are needed

Two communication channels are supported: queues and pipes. The latter can be accessed both ways.\
Moreover, `multiprocessing` contains all the synchronization primitives from `threading`.

#### Pipes

`Pipe()` returns two end of a pipe. Each end (each connection object) has `send()` and `recv()` methods to, respectively, read and write on the pipe. 

No risk of data corruption if two processes (eg Pygame and Raft) use different ends of the pipe at the same time.

- `send()` serializes the object
- `recv()` re-creates the object

```python
multiprocessing.Pipe([duplex])
```

Returns a pair: (`connection1`, `connection2`).\ 
If `duplex` is `False`, then `c1` can only receive while `c2` can only send.

#### Queues

Near clone of `queue.Queue`, it is both thread and process safe.

### State Sharing

#### Shared Memory

While not advised, some way to provide actual shared memory are given: data can be stored in `Value` or `Array`.

```python
from multiprocessing import Process, Value, Array

num = Value('d', 0.0) # double precision float 

process = Process(target=handle, args=(num))
process.start()  # num is then a shared data
```

#### Managers

We can also use a more complex structure with `Manager()` objects, that supports the creation of shared `threading.Event` or `threading.Lock`. 

### Synchronization Primitives

We have a clone of `Event`

```python
m_event = multiprocessing.Event()
t_event = threading.Event()

m_event.is_set()
t_event.is_set()
# so on and so forth
```

## Tkinter 

Oss: old naming style: *window*, new naming style: *widget*.

Version: 8.6.14

- Uses a classic widget object model, in a parent-child structure (kinda like html or Dart)
- Widgets are not automatically added to the UI, a *geometry manager* like `grid` is needed to control their placement
- Every UI update (user input, refreshes, etc) can happen only if an *event loop* like `mainloop` is running 

Every time we create a widget we must specify its parent

```python
# new widget will be placed inside parent widget
newwidget = ttk.Widget (parent, **kwargs)
```

```python
# standard Tkinter import practice
from tkinter import *
from tkinter import ttk

root = Tk() # main window   
            # likely not a UI element
frm = ttk.Frame(root, padding=10) # fit inside window
                                  # matches new-tk style while main window does not
frm.grid() # relative grid layout 

# label widgets that holds a static text string
ttk.Label(frm, text="Hello World!").grid(column=0, row=0)

# button widget, destroy() on_pressed()
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)

# puts element on display
# responds to user input
root.mainloop() 
```
Options controls things like color and border width of a widget. We have three ways to set them

```python
# set widget object options

# at creation time using **kwargs
button = Button(self, foreground="red", background="blue")

# at creation time using dict-like
button["foreground"] = "red"
button["background"] = "blue"

# using config() method after object creation 
button.config(foreground="red", background="blue")
```

Tk add some custom optional data types, like:

- color eg `"#RGB"`
- distance eg `35m` means 35mm
- geometry eg `button["geometry"] = "200x100"` usually in pixels
- images eg subclasses of `tkinter.Image` like `PhotoImage` for pngs or gifs. 

The usual way to display in image is using `PhotoImage` and `Label`

```python
label = ttk.Label(parent)
image = PhotoImage(file='img.gif')
label['image'] = image

# i guess we could compact it to
lpic = ttk.Label(parent, image=PhotoImage(file='img.gif'))
```


### Introspection

Introspection as reference documentation

```python
button = ttk.Button()
print(button.configure().keys()) # dict with all object's config options 
                                 # keys() gets just the names of each option

# finds specific class config options
print(
    set(button.configure().keys()) 
    - set(frame.configure().keys())
)

# similarly to get all object's methods 
print(dir(button)) # will gets me over 200 methods
print(
    set(dir(button))
    - set(dir(frame))
)
```

`configure()` will produce something like the following

```shell
>>> button.configure()
{'cursor': ('cursor', 'cursor', 'Cursor', '', ''), 'style': ('style', 'style', 'Style', '', ''), 
'default': ('default', 'default', 'Default', <index object at 0x00DFFD10>, <index object at 0x00DFFD10>), 
'text': ('text', 'text', 'Text', '', 'goodbye'), 'image': ('image', 'image', 'Image', '', ''), 
'class': ('class', '', '', '', ''), 'padding': ('padding', 'padding', 'Pad', '', ''), 
'width': ('width', 'width', 'Width', '', ''), 
'state': ('state', 'state', 'State', <index object at 0x0167FA20>, <index object at 0x0167FA20>), 
'command': ('command', 'command' , 'Command', '', 'buttonpressed'), 
'textvariable': ('textvariable', 'textVariable', 'Variable', '', ''), 
'compound': ('compound', 'compound', 'Compound', <index object at 0x0167FA08>, <index object at 0x0167FA08>), 
'underline': ('underline', 'underline', 'Underline', -1, -1), 
'takefocus': ('takefocus', 'takeFocus', 'TakeFocus', '', 'ttk::takefocus')}
```

Which should be treated as

```python
# most useful are first (name), last (current value) and fourth (default value) 
{
    'key' : ('option name',*args,'default value', 'current value')
}

# button.configure() output
{'cursor': ('cursor', 'cursor', 'Cursor', '', ''), 'style': ('style', 'style', 'Style', '', ''), 
'default': ('default', 'default', 'Default', <index object at 0x00DFFD10>, <index object at 0x00DFFD10>),}
```

Using `winfo` we can get information on the widget

```python
# uses each widget winfo_children() to traverse widgets hierarchy
def print_hierarchy(w, depth=0):
    print('  '*depth + w.winfo_class() + ' w=' + str(w.winfo_width()) + ' h=' + str(w.winfo_height()) + ' x=' + str(w.winfo_x()) + ' y=' + str(w.winfo_y()))
    for i in w.winfo_children():
        print_hierarchy(i, depth+1)
```

Some of the most useful methods are:

- `winfo_class`: widget type
- `winfo_children`: list of children widgets
- `winfo_parent`
- `winfo_toplevel`
- `winfo_width`

### Threading model

Python and Tcl/Tk have different threading models, which `tkinter` tries to bridge. \
Each thread has a separate Tcl interpreter instance associated to it.\
Each Tk object created by `tkinter` contains a Tcl interpreter.

Since `Tk.mainloop()` is single threaded, event handler could block other events from being processed. To avoid this, any long running computations should not run in an event handler, but either broken int smaller pieces using timers, or run in another thread entirely.\
*i.e GUI runs in the same thread as all application code including event handlers.*

### Event Handling 

Simple callbacks are used eg when pressing a button. Most of he time I want my callback to call some other procedure.

```python
def dostuff():
    # fun body


# this button calls the function 
ttk.Button(parent, text="Press Me", command=dostuff)
```

To produce an action after an input, or for events that don't have a widget specific command callback associated to them (eg `button:command`) we can `bind` them together

```python
# calls function() after <Return> key is pressed
# in modern computer it is Enter key
root.bind("<Return>", function)


# or we can make a label respond to different mouse commands
l =ttk.Label(root, text="Starting...")
l.grid()
l.bind('<Enter>', lambda e: l.configure(text='Moved mouse inside'))
l.bind('<Leave>', lambda e: l.configure(text='Moved mouse outside'))
# left (main) click
l.bind('<ButtonPress-1>', lambda e: l.configure(text='Clicked left mouse button'))
# right click
l.bind('<ButtonPress3>', lambda e: l.configure(text='Clicked right mouse button'))
# left (main) double click
l.bind('<Double-1>', lambda e: l.configure(text='Double clicked'))
l.bind('<B3-Motion>', lambda e: l.configure(text='right button drag to %d,%d' % (e.x, e.y)))

# WHY LAMBDA?
# in this specific example the callbacks used are so trivial that creating a "real" function is unnecessary 
```

Some common bindings follow, to see all best to look at `bind` command reference:

- `<Activate>`: window has become active
- `<KeyPress>`
- `<Motion>`: mouse has been moved
- `<Enter>`: mouse pointer has entered widget

Coupled variables provide a similar functionality to hooks: variable's change produces an update in the widget.\
Such variables must be subclassed from `tkinter.Variable`.

There are many subclasses already defined, like `StringVar`, `IntVar`, `DoubleVar` and `BooleanVar`. \
To read current value use `get()`, to change it use `set()`. Following this protocol ensures widget always tracks variable's value.

When using these variables Tk will *automatically* update view any time they are changed.

```python
class App (tk.Frame):
    def __init__(self):
        self.hook = tk.StringVar()
        self.hook.set("Default value")


# i guess that if an outsider calls hook.set() the UI will update accordingly
```

### Geometry Managers

Tkinter uses geometry managers to place object in the applicaiton. If something is not managed by one it is not shown.

There are three geometry managers:

- pack()
- grid()
- place()

### pack()

Just place element one after the other vertically. If i want to make widgets as wide as the parent i can use `fill=X` option.
Following code produces this result: ![](https://python-course.eu/images/tkinter/packing2.png)

```python
from tkinter import *

root = Tk()
window = tk.Label(root, text="Red Sun", bg="red", fg="white")
window.pack(fill=tk.X)
window = tk.Label(root, text="Green Grass", bg="green", fg="black")
window.pack(fill=tk.X)
window = tk.Label(root, text="Blue Sky", bg="blue", fg="white")
window.pack(fill=tk.X)

tk.mainloop()
```

### place()

Allows to explicitly set the position and size of a widget, either in absolute terms or relative to another widget.

```python
# should create something like this
# we can potentially put canvases in there
#[ header ]  
#[--------]
#[--------]
#[--------]
#[ footer ]

header.place(x=0, y=0, width=1000, height=100)
mainwindow.place(x=0, y=100, width=1000, height=100)
footer.place(x=0, y=1100, width=1000, height=100)
```

#### grid()

To access single (or multiple) grid children i can use `grid_slaves()`

```python
for cell in content.grid_slaves(row=3):
    print(cell)

singlecell = content.grid_slaves(3,3) 
print(singlecell)
```

And i can configure options after gridding with `.grid_configure(**options)`. \
If i want to delete elements (de-grid them) i can use :

- `forget(*elem)`: takes off the screen a list of one or more widget, does not destroy the widgets
- `remove(*elem)`: same but grid options will be remembered

### Canvas

Must be placed inside a geometry manager but it allows great flexibility.

- [official tutorials](https://tkdocs.com/tutorial/)
- [official docs](https://tcl.tk/man)
- [better docs](https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/)

Opposite approach: extremely manual but because of this it is easier to do things in a specific way (ie doesn't need as many workarounds).

Canvas coordinates starts from top left corner and increase going down and right, like a matrix (row, col) would

```python
canvas = Canvas(parent, width=1, height=1)

# [(0,0)]  [ ]  [(1,0)]
# [ ]  [(.5, .5)] [ ]
# [(0,1)]  [ ]  [(1,1)]
```

Canvas basics

```python
# create canvas
canvas = Canvas(parent, width=500, height=400, background='gray75')

# line
canvas.create_line(10, 10, 200, 50, 90, 150, 50, 80)
# it goes through a series of points
id = canvas.create_line(x0, y0, x1, y1, ..., xn, yn, **options) 

# rectangle
canvas.create_rectangle(10, 10, 200, 50, fill='red', outline='blue')

# arbitrary shape
canvas.create_polygon(10, 10, 200, 50, 90, 150, 50, 80, 120, 55, fill='red', outline='blue')

# image
myimg = PhotoImage(file='pretty.png')
canvas.create_image(
    10, 10,        # coordinates
    image=myimg,   #  
    anchor='nw'    # where to put top left of img
    )

# text
canvas.create_text(100, 100, text='A wonderful story', anchor='nw', font='TkMenuFont', fill='red')

# widget
# must be put inside a window
button = ttk.Button(canvas, text='Implode!')
canvas.create_window(10, 10, anchor='nw', window=button)
```

To act on items we have options:

- `delete`: delete item
- `coords`: change size and position
- `move`: offset position

Items are drawn upon each other in what is called the **stacking order**: basically levels. We can change them by using:

- `raise()` (or `lift`)
- `lower()`

Any time i can use `id` to modify specific widget, i can use a `tag` to modify **multiple** widgets that share that specific `tag`.

```python
# use in construction
c = canvas.create_line(10, 10, 20, 20, tags=('gridline','verticalline'))

# add later 
c.addtag('tag1','tag2', 'tag3')

# delete
c.dtag(1, 'tag1') # credo

# find
c.find_withtag('tag') # accepts also an item
```

We have a custom `bind` command specific for canvases that works with group of elements that shares the same `tag`

```python
# specifies canvas number
# works exactly like normal bind
canvas.tag_bing(id, '<1>', ...)
```

#### Scrolling

In many applications you want a canvas larger than the window (eg a game map). I can attach horizontal and vertical scrollbars to the canvas in the usual way via `xview()` and `yview()`.

I therefore specify two sizes:

- `width` and `height` specify window size
- `scrollregion` config option coordinates (left, top, right, bottom) specify canvas size 

Then since `bind` does not now that a scroll has occurred: if i scroll down 50 pixel, and i tap at (0,-50), it will be registered as (0,0). To offset axis-zero we use `canvasx()` and `canvasy()`.

```python
# scroll bars
h = ttk.Scrollbar(root, orient=HORIZONTAL)
v = ttk.Scrollbar(root, orient=VERTICAL)

# makes canvas scrollable 
canvas = Canvas(root, scrollregion=(0, 0, 1000, 1000), yscrollcommand=v.set, xscrollcommand=h.set)
h['command'] = canvas.xview
v['command'] = canvas.yview

def xy(event)
    # may be incorrect
    # update x,y positions
    lastx = canvas.canvasx(event.x)
    lasty = canvas.canvasy(event.y)

# which is^ used by
canvas.bind("<Button-1>", xy)
```

#### Code Examples

Create a canvas

```python
from tkinter import *
from tkinter import ttk

# implant in a grid to make it auto big??
# min size 0, weight means rate of growth
root = Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

canvas = Canvas(root)
canvas.grid(column=0, row=0, sticky=(N, W, E, S))

root.mainloop()
```

Implant canvas in a grid

```python
canvas.grid(column=0, row=0, sticky=(N,W,E,S))
h.grid(column=0, row=1, sticky=(W,E))
v.grid(column=1, row=0, sticky=(N,S))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
```

Use tags to set color 

```python
def setColor(newcolor):
   global color
   color = newcolor
   canvas.dtag('all', 'paletteSelected')
   canvas.itemconfigure('palette', outline='white')
   canvas.addtag('paletteSelected', 'withtag', 'palette%s' % color)
   canvas.itemconfigure('paletteSelected', outline='#999999')

id = canvas.create_rectangle((10, 10, 30, 30), fill="red", tags=('palette', 'palettered'))
id = canvas.create_rectangle((10, 35, 30, 55), fill="blue", tags=('palette', 'paletteblue'))
id = canvas.create_rectangle((10, 60, 30, 80), fill="black", tags=('palette', 'paletteblack', 'paletteSelected'))

setColor('black')
canvas.itemconfigure('palette', width=5)
```

Bind event

```python
def doneStroke(event):
    canvas.itemconfigure('currentline', width=1)        

canvas.bind("<B1-ButtonRelease>", doneStroke)
```

## Pygame

Blit function is paramount to pygame, what is important to note is that blitted objects' *levels* follows program *scope*

```python
# draw source surface (object) on the destination surface or coordinates
DISPLAY.blit(source, dest)
DISPLAY.blit(source, (x,y))

# regarding scope: obj2 is drawn upon obj1
DISPLAY.blit(obj1, (10,10))
DISPLAY.blit(obj2, (10,10)) # hides obj1
```
 
Typical game loop structure. The strict separation between game's logic and rendering routines is deliberate: prevents a whole plethora of bugs related to objects updating and rendering concurrently.

```python
import pygame

# start engine
pygame.init()

# creates main screen
screen = pygame.display.set_mode((1280,720))

# starts clock
clock = pygame.time.Clock()


# everything runs inside infinite loop
while True:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    # Do logical updates here.
    # ...

    screen.fill("purple")  # Fill the display with a solid color

    # Render the graphics here.
    # ...


    # we want to limit display refresh speed
    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)         # wait until next frame (at 60 FPS)
```

Uses RGB color system

```python
pygame.Color(0, 0, 0)         # Black
pygame.Color(255, 255, 255)   # White
pygame.Color(128, 128, 128)   # Grey
pygame.Color(255, 0, 0)       # Red
```

Rect can be used to do almost everything, like enemies, players, or cities in Raftian

```python
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")

        # define sprite borders 
        # ie creates rect of the size of image and binds it
        self.rect = self.image.get_rect()

        # define starting position on the screen
        # with a bit of randomization
        self.rect.center=(random.randint(40,SCREEN_WIDTH-40),0) 
 

      def move(self):
        self.rect.move_ip(0,10)
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)
 
      def draw(self, surface):
        # draw image on rect
        surface.blit(self.image, self.rect) 
```

I can group `Sprite` objects (or just do a `list` of `Rect`s)

```python
# we can probably do this with rect 

# sprite group with all enemies
enemies = pygame.sprite.Group()
enemies.add(enemy)

# sprit group with all sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)


# then i can iterate through all of them for collision detection
if pygame.sprite.spritecollideany(player, enemies):
    DISPLAY.fill(RED)
    for entity in all_sprites:
        entity.kill()
    

    time.sleep(2)
    pygame.quit()
    raise SystemExit
```

Fonts: for text that does not need to change we can render it outside of game loop. 

```python
# create font
font = pygame.font.SysFont("Verdana", 60)

# create actual graphics for a text
text = font.render("Some Text", True, COLOR)

# draw it on some coordinates
DISPLAY.blit(text, (x,y))
```

Background image should be loaded outside game loop but `blit()` inside of it, since it must be redrawn as other entities move

```python
background = pygame.image.load("background.png")
...
...

while True: 
    ...
    # draw first so it stays on bottom layer
    DISPLAY.blit(background, (0,0))
    
    ...
    ...
``` 

### Font and Text

Two main classes:

- `pygame.font.Font()`: takes font format file `.ttf`
- `pygame.font.SysFont()`: need font name, uses standard fonts

```python
# custom
font = pygame.font.Font("arial.ttf", 20)

# system fonts
font = pygame.font.SysFont("Helvetica", 20)

# default
font = pygame.font.Font(None, size)
```

Then i create the actual text by rendering it

```python
text = font.render(
    "Displayed Text",  #
    True,              # anti-aliasing
    (0,0,0)            # text color
)
```

And then i draw it on the screen

```python
screen.blit(text, (x,y))
```

### Events 

Pygame comes with its own set of predefined events such as `K_LEFT` or `K_RIGHT`. These events are detected in the game loop.

Pygame has a total of 32 event slots, of which the first 23 are predefined. We can use the remaining ones 

```python
# create user event whith id=24
CUSTOM_EVENT = pygame.USEREVENT + 0
```

I can also broadcast my events using timers

```python
# uses milliseconds
pygame.time.set_timer(CUSTOM_EVENT, 3000)
```