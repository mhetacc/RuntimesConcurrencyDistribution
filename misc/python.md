# Python Language 

## Conventions

```python
class UpperCamelCase:
    self

def lowercase_with_underscore():
    """docstring"""
    pass
```

## Basics

Everything is an object, and therefore has a *class* (also called its *type*). \
It is stored as `object.__class__`

### Assignment

Multi line assignment

```python
a, b = 0, 1 
# is equal to
a=1 
b=0

# and also (i dont like it)
a, b = b, a+b 
```

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
>>> 
```

### Strings

Python strings are ![immutable](https://docs.python.org/3.12/glossary.html#term-immutable).

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

### Lists

Simple assignment in Python never copies data

```shell
>>> rgb = ["Red", "Green", "Blue"]
>>> rgba = rgb
>>> id(rgb) == id(rgba)  # they reference the same object
True
```

On the other hand all slice operations return a new list containing the requested elements (ie slice returns a shallow copy)

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
Oss: operator * syntax is before variable: `*var` and not `var*`

Oss2: i can also unpack JSON: (dictionaries)
- `*tuple`
- `**dict`

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
    """docstring"""
    # make it habit to use it

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
# i dont like this
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
>>>from my_class import method1
>>>method1(0,0)

# some output
```

### dir()

`dir()` function prints which names a module defines. \
Without arguments it lists the name defined in the current session.

### Packages

Higher directory level for collection of modules. \
Use dot notation. \
There **must** be a *__init__.py* to make Python treat a directory as a package.

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
# using with keyword automatically closes the file
# PREFERRED 
with open('file') as f:
    read_data = f.read()

f.closed # True

# otherwise call close function
f = open('file')
read_data = f.read()
f.close()
```

Using `close()` could make `f.write()` behave incorrectly.

A **very nice** way to read is to loop each line

```python
for line in f:
    print(line, end='')
```

Writing requires only to call `f.write('Some line\n')`

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

[...] nothing in Python makes it possible to enforce data hiding, it is all based upon convention.

By default class memebers are *public* and all member functions are *virtual*.

[...] *aliases* behave like pointers in some respects. For example, passing an object is cheap since only a pointer is passed. 

[...] all operations that introduce new names use the local scope: in particular, `import` statements bind the module name in the local scope.

Assignments do not copy data, they just bind names to objects. The same is true for deletions: `del x` just removes binding of `x` from the local scope. \
**i.e. everything is a pointer :)**

```python
class MyClass:
    class_variable = 'I am shared by all instances'

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

**Nearer** scope always has **precedence**: \
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
                    # shared by all istances
    def __init__(self, name):
        self.name = name # unique to each istance
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

### Methods

[...] the special thing about methods is that the instance object is passed as the first argument of the function

```python
# the two following lines are equivalent
x.f()

MyClass.f(x) 

# we call f() of class MyClass on object x
```

Often, the first argument of a method is called `self`. This is nothing more than a convention: the name `self` has absolutely no special meaning to Python

### Inheritance

[...] For C++ programmers: all methods in Python are effectively `virtual`

```python
class ChildClass(ParentClass):
    # class body
```

If i want to call a parent class method explicitly

```python
ParentClass.methodName(self, arguments)
```

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

# Specific Tools

## Logging (debug)
`logging` module: https://docs.python.org/3/library/logging.html

Standard module to logs stuff

Loggin is performed by calling methods on instances of the `Logger` class 

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
# this should appen all logs in file myLog

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

Should not use `Handler ` directly, instead use as interface for child custom handlers 

Useful `Handlers`:
- `FileHandler` send messages to disk files
- `RotatingFileHandler` to disk files, support max log sizes and file rotation
- `StreamHandler` send to stream (file-like objects)

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
fileConfig(disable_existing_loggers = True)

# can call it False
```


## Queues and Logs (data) 

### list

Standard built-in Python module to make lists. 

### queue
https://docs.python.org/3.12/library/collections.html#collections.deque

 Deques support thread-safe, memory efficient appends and pops from either side of the deque with approximately the same O(1) performance in either direction.

### deque 
https://docs.python.org/3.12/library/queue.html#module-queue

The queue module implements multi-producer, multi-consumer queues. It is especially useful in threaded programming when information must be exchanged safely between multiple threads.

# PEP 8 - Format Conventions