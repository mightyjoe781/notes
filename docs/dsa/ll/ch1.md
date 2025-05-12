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

### Traversal

````c++
for(link t = x; t != 0; t = t->next)
  	cout << t->item << endl;
````

### Reversal

* Maintain a pointer `r` to the portion of the list already processed , and a pointer `y` to the portion of the list not yet seen.
* Then save a pointer to the node following `y` in `t`, change `y`’s link to point to `r`, and then move `r` to `y` and `y` to `t`,

````c++
link reverse(link x) {
  link t, y = x, r = 0;
  while(y != 0) {
    t = y->next; y->next = r; r = y; y = t;
  }
  return r;
}
````

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

## Problems

* Merge Two Sorted List (21)
* Remove Nth Node from End (19)
* Remove Linked List Element (203)
* Intersection of Two Linked List (160)
* Josephus Problem (Linked List Variant)
