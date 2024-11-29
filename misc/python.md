# Python 

## Conventions

```python
class UpperCamelCase:
    self

def lowercase_with_underscore():
    """docstring"""
    pass
```

## Basics

Everything is an object

### Assignment



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
Oss: operator * syntax is before variable: *\*var* and not *var\**

Oss2: i can also unpack JSON: (dictionaries)
- *\*tuple*
- *\*\*dict*

## Flow Control

### if

elif and else are optional, there is no switch-case statement

```python
if cond:
    # something
elif :
    # something
else:
```

*in* keyword

```python
reply = input('Insert yes or no')
if reply in {'y', 'ye', 'yes'}:
    return True
if reply in {'n', 'no', 'nop', 'nope'}:
    return False
```

### for

Similar to *for each*, iterate on elements of any sequence, contrary to what C does (define iteration step and halt condition)

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

We also have *brake* and *continue* statements, the latter skip to next loop iteration. \
*break* can be paired with *else*: if no break after loop ended, else clause is executed.

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

*pop* vs *del*

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

*dir()* function prints which names a module defines. \
Without arguments it lists the name defined in the current session.

### Packages

Higher directory level for collection of modules. \
Use dot notation. \
There **must** be a *__init__.py* to make Python treat a directory as a package.