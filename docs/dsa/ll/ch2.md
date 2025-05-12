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

Application

* AST Analysis by Compilers to detect recursive & errornous constructs
* Game Development, cycle detection to avoid resource hogging
* Networking Routing Loops

### Problems

* Palindrome Linked List (234)
* Linked List Cycle Detection (141)
* Find Cycle Entry Point (142)

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