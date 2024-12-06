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

## Basics

Everything is an object, and therefore has a *class* (also called its *type*). \
It is stored as `object.__class__`

### Assignment

Simple assignment is **always by-reference**

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

There are some ways other than scope to access parent stuff

```python
class super(type, object_or_type=None):
    # stuff

# returns a proxy object to access parent class of type
```

Or I could call explicitly `ParentClass.parent_function()` 

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

## Tkinter 



