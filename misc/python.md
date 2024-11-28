# Python 

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

