# Expression Evaluation & Parsing

### Expression Types

* Infix : `a + b * c`
* Postfix (Reverse Polish Notation): `a b c * +`
* Prefix (Polish Notation): `+ a * b c`

## Stack - Based Evaluation

* Convert Infix into Postfix using Stack (Shunting Yard Algorithm)
* Evaluate Postfix using stack:
    * If operand - `push`
    * If operator `pop two operands, evaluate, push result`

### Infix to Postfix (Shunting Yard Algorithm)

**Problem Statement:** Given an infix expression, Your task is to convert the given infix expression to a postfix expression.

Stack maintains the operator precedence invariant.

```python

def infix_to_postfix(expr):
    prec = {'+':1, '-':1, '*':2, '/':2, '^':3}
    stack = []
    res = []

    for ch in expr:
        # operand, put to output
        if ch.isalnum():
            res.append(ch)

        # opening bracket
        elif ch == '(':
            stack.append(ch)

        # closing bracket
        elif ch == ')':
            while stack and stack[-1] != '(':
                res.append(stack.pop())
            stack.pop()  # remove '('

        # operator
        else:
            # precendence invairant !
            while (stack and stack[-1] != '(' and
                   prec[stack[-1]] >= prec[ch]):
                res.append(stack.pop())
            stack.append(ch)

    # pop remaining operators
    while stack:
        res.append(stack.pop())

    return ''.join(res)

```

### Evaluating Postfix Operations (RPN)

```python

def eval_postfix(expr):
    stack = []

    for ch in expr.split():
        # operand
        if ch.isdigit():
            stack.append(int(ch))
        else:
            b = stack.pop()
            a = stack.pop()

            if ch == '+':
                stack.append(a + b)
            elif ch == '-':
                stack.append(a - b)
            elif ch == '*':
                stack.append(a * b)
            elif ch == '/':
                stack.append(a // b)  # integer division

    return stack[0]

```

### Infix to Prefix

Simple Algorithm

- Reverse the Given Infix Expression
- Convert to RPN
- Reverse the Result

```
Infix:   (A+B)*C
Reverse: C*(B+A)
Postfix: C B A + *
Prefix:  * + A B C
```

### Postfix to Infix

```python

def postfix_to_infix(expr):
    stack = []
    for ch in expr:
        if ch.isalnum():
            stack.append(ch)
        else:
            b = stack.pop()
            a = stack.pop()
            stack.append(f"({a}{ch}{b})")
    return stack[0]

```

### Prefix to Infix

^ Same as Above, Just scan from `reversed(expr)`
### Postfix to Prefix

```python
# scan to right
def prefix_to_postfix(expr):
    stack = []
    for ch in expr:
        if ch.isalnum():
            stack.append(ch)
        else:
            a = stack.pop()
            b = stack.pop()
            stack.append(a + b + ch)
    return stack[0]

```

### Prefix to Postfix

Same as above ^, but scan from `reversed(expr)`


| Conversion       | Direction | Trick              |
| ---------------- | --------- | ------------------ |
| Infix → Postfix  | L → R     | stack + precedence |
| Infix → Prefix   | Reverse   | reverse + postfix  |
| Postfix → Infix  | L → R     | pop 2 operands     |
| Prefix → Infix   | R → L     | pop 2 operands     |
| Prefix → Postfix | R → L     | stack              |
| Postfix → Prefix | L → R     | stack              |