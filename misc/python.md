# Python 

## Basics

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
def fun():
    """docstring"""
    # make it habit to use it

fun() # calling the function
```

