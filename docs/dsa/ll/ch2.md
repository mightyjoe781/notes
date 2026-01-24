# Linked List Techniques

## Fast & Slow Pointer Techniques

* Optimize traversal using two pointers moving at different speeds.
* Detects cycles, Start of Cycle, mid of list
* Finds Nth Node from End
* Palindrome Checks

````c++
ListNode* middleNode(ListNode* head) {
    ListNode *slow = head, *fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
    }
    return slow;
}
````

````c++
// suppose a struct node exists. and link is just typedef on *node
link isCycle(link head){
    link slow = head , fast = head;
    while(!fast && !fast->next && slow!=fast){
        slow = slow -> next;
        fast = fast -> next -> next;
    }
    // the moment loop ends we hit the point at which both meet
    if(!fast || !fast->next) return nullptr;
    return slow;
}
// above function returns null if there is no cycle else it return the point where the cycle exists.
````

An Approach in Python which is quite faster than above ^ using EAFP (Easier to Ask for Forgiveness than Permission) patter in python, as compared to LBYL (Look before you leap) in languages like C.

In a multi-threaded environment, the LBYL approach can risk introducing a [race condition](https://docs.python.org/3/glossary.html#term-race-condition) between “the looking” and “the leaping”

```python

def hasCycle(head):
    try:
        slow = head
        fast = head.next

        while slow is not fast:
            slow = slow.next
            fast = fast.next.next
        
        return True
    except:
        return False
        
```


Application

* AST Analysis by Compilers to detect recursive & errornous constructs
* Game Development, cycle detection to avoid resource hogging
* Routing Loops

#### Problems

* Palindrome Linked List (234)
* Linked List Cycle Detection (141)
* Find Cycle Entry Point (142)

### Problem : Find Cycle Entry Point

![](assets/Pasted%20image%2020250906110100.png)

Imagine `n` represents the distance between starting point and the point where the loop starts, `m` represents the distance of the loop.

Assuming we are running turtle-hare algorithm, diamond represents the point where turtle meets here, `k` represents the distance from starting of loop to the diamond point.

Since hare runs at twice speed as turtle, then we can say, distance travelled by turtle (`i`) for $p1$

$$
i = n + m . p1 + k
$$
distance travelled by hare (`2i`), for some integer $p2$

$$
2i = n + m. p2 + k
$$

Simplifying above relationships, where I represents some integer
$$
n + k = m.(p2-p1) = m. (I) 
$$

Alternately : `n+k` wraps around circle. or diamond point is `n` distance away from head of the list. (towards the direction of iteration)

```c++
link diamond = isCycle(head) // find diamond point using hare-tortoise algorithm
link hptr = head; // good practice to not change given head
while(diamond!=hptr){
    diamond = diamond->next;
    head = head->next;
}
```

Full Solution in Python

```python

def detectCycle(head: Optional[ListNode]) -> Optional[ListNode]:
    if not head or not head.next:
        return None

    slow = head
    fast = head

    # Phase 1: detect cycle
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            break
    else:
        # no cycle
        return None

    # Phase 2: find entry point
    p = head
    while p is not slow:
        p = p.next
        slow = slow.next

```

### Palindrome Linked List

Given the `head` of a singly linked list, return true if it is a *palindrome* or false otherwise.

Approaches

- Clone the list and reverse the the clone, then compare node by node.
- put till half nodes in the stack and then pop stk and compare it
- Optimal Approach : Reverse half of the list and then compare both parts

```python

def isPalindrome(self, head: Optional[ListNode]) -> bool:
    rev = None
    slow = fast = head

    while fast and fast.next:
        fast = fast.next.next
        rev, rev.next, slow = slow, rev, slow.next # reverse and forward s

    if fast:
        slow = slow.next
    
    # check palindrome
    while rev and rev.val == slow.val:
        rev = rev.next
        slow = slow.next
    
    return not rev

```

### Find Nth Node from End of List & Remove it

Given the head of a linked list, remove the nth node from the end of the list and return its head.

Approach :

- Find the length of entire list, then calculate the `nth` node from the length, traverse to it and delete it,
- One Pass solution : using `fast pointer` to reach `nth node` from start, then start slow pointer

![](assets/Pasted%20image%2020260124142422.png)


```python

def removeNthFromEnd(head, n):

    fast = slow = head

    for _ in range(n):
        fast = fast.next

    if not fast:
        return head.next
    
    while fast.next:
        fast = fast.next
        slow = slow.next
    # slow points to node before the node to be deleted!
    slow.next = slow.next.next
    return head

```


Recursive Solution for counting the `nth` from end, and removes the node as well

```python

def removeNthFromEnd(head, n):
    def remove(head):
        if not head:
            return 0, head
        i, head.next = remove(head.next)
        return i+1, (head, head.next)[i+1 == n]
    return remove(head)[1]

```


## Recursive Linked List Problems

* these problems usually involve backtracking, divide & Conquer

````c++
ListNode* reverseList(ListNode* head) {
    if (!head || !head->next) return head;
    ListNode* newHead = reverseList(head->next);
    head->next->next = head;
    head->next = nullptr;
    return newHead;
}
````

#### Problems

* Linked List Palindrome (Recursive Solution)
* Swap Nodes in Pair (24)
* Reverse Node in `k-Groups` (25)

### Reverse node in k-Groups

```python

def reverseKGroup(head, k):

    # check if we need to reverse the group
    curr = head
    for _ in range(k):
        if not curr:
            return head
        curr = curr.next

    # reverse the group 
    prev = None
    curr = head
    for _ in range(k):
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt


    head.next = self.reverseKGroup(curr, k)
    return prev

```


## Cycle Detection & List Manipulation

* Advanced operation involving cycles or structural changes

#### Problems

* Reorder List (143) : Combine Cycle Detection with Reversal 
* Flatten a Multilevel DLL (430)
* Partition List (86)
* Odd Even Linked List (328)


### Odd Even Linked List

Given the `head` of a singly linked list, group all the nodes with odd indices together followed by the nodes with even indices, and return _the reordered list_.

The **first** node is considered **odd**, and the **second** node is **even**, and so on.

```
Input: head = [1,2,3,4,5]
Output: [1,3,5,2,4]
```


```python

def oddEvenList(head):

    if not head:
        return None

    odd, even = head, head.next
    # keep a copy of even head, to connect to odd tail
    evenHead = even

    while even and even.next:
        odd.next = even.next
        odd = odd.next   # forward odd
        even.next = odd.next
        even = even.next # forward even
    
    odd.next = evenHead
    return head

```

### Find the Intersection of Two Lists

![](assets/Pasted%20image%2020260124145040.png)

Solution below uses the concept, if two lists are placed one after another for example, `(l1, l2)` and `(l2, l1)`, so both pointer will travel same distance let's say `(n + m)`

And eventually both pointer will meet if cycle exists, 


```python

def getIntersectionNode(headA, headB):

    p, q = headA, headB

    while p != q:
        p = p.next
        q = q.next

        if p == q:
            return p

        if not p:
            p = headB
        
        if not q:
            q = headA

    return p

```

### Add 1 to a number represented as LL

```python

## Recursive Approach

def add_one(node):
    # Base case: when reaching beyond last node, return carry = 1
    if not node:
        return 1
    # Recurse to the end
    carry = add_one(node.next)  
    total = node.data + carry
    node.data = total % 10
    # Return new carry
    return total // 10  

```

### Add 2 Numbers in LL

Following is an iterative Solution to the problem

```python

def addTwoNumbers(l1, l2):

    dummyHead = ListNode(0)
    curr = dummyHead
    carry = 0
    while l1 != None or l2 != None or carry != 0:
        l1Val = l1.val if l1 else 0
        l2Val = l2.val if l2 else 0

        columnSum = l1Val + l2Val + carry
        carry = columnSum // 10

        newNode = ListNode(columnSum % 10)
        curr.next = newNode
        curr = newNode

        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
        
    return dummyHead.next

```


### Rotate a Linked List

Rotate the list by k elements,

```python

def rotateRight(head, k):
    # edge cases
    if not head or not head.next:
        return head

    # reduce rotations
    p = head
    n = 0
    while p:
        p = p.next
        n += 1
    
    k = k%n
    if k == 0:
        return head

    # n-th node from end problem
    fast = head
    for _ in range(k):
        fast = fast.next
    
    slow = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next

    # relink the ll
    newHead = slow.next
    slow.next = None
    fast.next = head 

    return newHead

```

### Flatten a Linked List

```python


class Solution:
    def merge(self, list1, list2):
        dummyNode = ListNode(-1)
        res = dummyNode

        # Merge the lists based on data values
        while list1 is not None and list2 is not None:
            if list1.val < list2.val:
                res.child = list1
                res = list1
                list1 = list1.child
            else:
                res.child = list2
                res = list2
                list2 = list2.child
            res.next = None

        # Connect the remaining elements if any
        if list1:
            res.child = list1
        else:
            res.child = list2

        # Break the last node's link to prevent cycles
        if dummyNode.child:
            dummyNode.child.next = None

        return dummyNode.child

    # Function to flatten a linked list with child pointers 
    def flattenLinkedList(self, head):
        # If head is null or there is no next node
        if head is None or head.next is None:
            return head # Return head

        mergedHead = self.flattenLinkedList(head.next)
        head = self.merge(head, mergedHead)
        return head

```

Alternatively traverse the list and collect the numbers and then recreate a new list.

### Remove Duplicates from a DLL

```python

def removeDuplicates(head):
    # If the list is empty, return None
    if not head:
        return None

    current = head

    while current and current.next:
        nextDistinct = current.next

        while nextDistinct and nextDistinct.data == current.data:
            nextDistinct = nextDistinct.next

        # Connect current node to the next distinct node
        current.next = nextDistinct
        if nextDistinct:
            nextDistinct.prev = current

        current = current.next

    return self.head

```

### Clone Linked List with Next, Random Pointer

A linked list of length `n` is given such that each node contains an additional random pointer, which could point to any node in the list, or `null`.

```python

def copyRandomList(head):
    if not head:
        return None
    old_to_new = {}
    
    curr = head
    while curr:
        old_to_new[curr] = Node(curr.val)
        curr = curr.next
    
    curr = head
    while curr:
        old_to_new[curr].next = old_to_new.get(curr.next)
        old_to_new[curr].random = old_to_new.get(curr.random)
        curr = curr.next
        
    return old_to_new[head]

```

### Sort Linked List

Given the `head` of a linked list, return _the list after sorting it in **ascending order**_.

A quick and dirty way is to collect values in $O(n)$ time, and then sort in $O(n\log n)$ and recreate again a new list using $O(n)$ time complexity.

TODO: Merge Sort