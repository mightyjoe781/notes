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

Application

* AST Analysis by Compilers to detect recursive & errornous constructs
* Game Development, cycle detection to avoid resource hogging
* Routing Loops

### Problems

* Palindrome Linked List (234)
* Linked List Cycle Detection (141)
* Find Cycle Entry Point (142)

#### Problem : Find Cycle Entry Point

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

### Problems

* Linked List Palindrome (Recursive Solution)
* Swap Nodes in Pair (24)
* Reverse Node in `k-Groups` (25)

## Cycle Detection & List Manipulation

* Advanced operation involving cycles or structural changes

### Problems

* Reorder List (143) : Combine Cycle Detection with Reversal 
* Flatten a Multilevel DLL (430)
* Partition List (86)
* Odd Even Linked List (328)