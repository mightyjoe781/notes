### Introduction

- Arithmetic in Python

    - Power : `a**b`

- Division in python :

    - Integer Division : `a//b`
    - Float Division : `a/b`

- Conditionals in Python

- Loop in Python

- given `n` : print `123..n` (don’t use strings)

  ```python
  for i in xrange(10):
  	print i,		# this (due to comma) prints numbers in a single line separated by space
  	
  # there is a print function from __future__ module
  print(*values, sep=' ', end='\n', file=sys.stdout) # *values means array is unpacked : val1, val2, val3..
  
  # solution 
  	print(*range(1,n+1), sep='')
  ```

### Basic Data Types

- List : `[element1, element2, element3, element4, ...]`
- 