# Expression Evaluation & Parsing

### Expression Types

* Infix : `a + b * c`
* Postfix (RPN): `a b c * +`
* Prefix: `+ a * b c`

### Stack - Based Evaluation

* Convert Infix into Postfix using Stack (Shunting Yard Algorithm)
* Evaluate Postfix using stack:
    * If operand - `push`
    * If operator `pop two operands, evaluate, push result`

### Problems

* Evaluate Reverse Polish Notation (150)
* Infix to Postfix Convertor
* Basic Caculator
* Expression Parsing 
