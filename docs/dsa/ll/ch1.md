# Linked List

### Key Concepts

* Types of Linked List
    * Singly Linked List
    * Doubly Linked List
    * Circular Linked List
* Advantages over arrays
    * Dynamic Size
    * Efficient Insertion/Deletion
* Disadvantages
    * No Random Access
    * Extra Memory for Pointers

## Implementation

```c++
// compact implementation
struct Node { Item item; Node *next;}
typedef Node *link;

// usage
link x = new Node; // or Node *x = new Node;
```

```c++
// constructor implementation
struct Node{
    Item item , Node *next;
    Node( Item x; Node *t){
        item = x ; next = t;
    };
}
typedef Node *link;

// usage
link t = new Node(x, t);	// or Node *x = new Node(x, t);
```


```python

class Node:
    def __init__(self, x, next=None):
        self.x = x
        self.next = next
        
t = Node(x, tc)        

```

## Basic Operation

### Access

````c++
// dereferencing the link
(*x).item // of type item
(*x).next	// of type link

// short-hand in cpp
x->item
x->next
````

### Deletion

````c++
// using temporary variable
t = x->next; x->next = t->next; // NOTE: Java GC can collect it later, but in C++ it needs to deleted.

// more simpler
x->next = x->next->next;
````

### Insertion

````c++
// inserting node t into the list at position following node x
t->next = x->next; x->next = t;
````

```python
# u ---> x --> y ---> z
# u ---> x ---> t ---> y ---> z
t.next = x.next
x.next = t
```

### Traversal

````c++
for(link t = x; t != 0; t = t->next)
  	cout << t->item << endl;
````

```python
p = x
while p:
    print(p.item)
    p = p.next 

```

### Reversal

* Maintain a pointer `r` to the portion of the list already processed , and a pointer `y` to the portion of the list not yet seen.
* Then save a pointer to the node following `y` in `t`, change `y`’s link to point to `r`, and then move `r` to `y` and `y` to `t`,

````c++
link reverse(link x) {
  link t, y = x, r = 0;
  while(y != 0) {
    t = y->next; y->next = r;  // temporarily save in t
    r = y;       // move r forward
    y = t;       // move y forward
  }
  return r;
}
````


```python

# reversing using recursion
def reverseList(head):

    if not head or not head.next:
        return head
    
    res = reverseList(head.next)

    head.next.next = head
    head.next = None

    return res

```

## Doubly Linked List

* Its not asked very commonly, but its better understand it.

````c++
// constructor implementation
struct Node{
    Item item , Node *next, Node *prev;
    Node( Item x; Node *t, Node *p){
        item = x ; next = t; prev = p;
    };
}
typedef Node *link;

// deletion for node t
t->next->prev = t->prev;
t->prev->next = t->next;

// insertion, requires updating four nodes
// insert t after x
t->next = x->next;
x->next->prev = t;
x->next = t;
t->prev = x;
````


```python

class Node:
    def __init__(self, data, next=None, prev=None):
        self.data = data
        self.next = next
        self.prev = prev

class DLL:
    def __init__(self):
        self.head = Node(None, None, None)
        self.tail = Node(None, None, None)
        # fix the pointing directions
        self.head.next = self.tail
        self.tail.prev = self.head
        
    def appendleft(self, node: Node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
    
    def append(self, node):
        node.prev = self.tail.prev
        node.next = self.tail
        self.tail.prev.next = node
        self.tail.prev = node
        
    def remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
        
    def pop(self) -> Node:
        if self.tail.prev == self.head:
            # nothing to pop
            return None
        node = self.tail.prev
        self.remove(node)
        return node

```

## Problems

* Merge Two Sorted List (21)
* Remove Nth Node from End (19)
* Remove Linked List Element (203)
* Intersection of Two Linked List (160)
* Josephus Problem (Linked List Variant)

### Josephus Problem

Generally Josephus Problem can be solved using following recursion.

Keeping a list and simulating the josephus criteria will not be optimal, it will take $O(n.k)$ time. Instead of asking who survived ?, ask following : If I already know the survivor among n−1 people,

how does adding **one more person** change the answer?

Recursively Build solution from base cases.

$$

\begin{align}
 J (1, k) &= 0 \\
 J (n, k) &= (J(n-1, k) + k) \% n
\end{align}

$$

Iteratively 

```python

def josephus(n, k):
    
    res = 0
    for i in range(2, n+1):
        res = (res + k) % i
    
    return res + 1

```

Now initially we had the issue in deleting the node, which was expensive, but using linked list we can reduce complexity to $O(n)$

