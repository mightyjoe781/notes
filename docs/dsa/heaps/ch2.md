# Applications

## Real-time Top-K Elements

### Concept

* Maintain the top `K` largest or smallest elements from a stream or dataset in real-time
* Use a *min-heap* of size `K` to track top `K` largest elements (stream)

### Use Cases

* Streaming data analytics
* Real-time Leaderboards
* Online Recommendation System

### Complexity

* Each insertion/deletion operation takes $O(\log K)$
* Efficient for large data streams where $K << N$

### Kth Largest Element in an Array

Idea is simple, build a heap in python using negative numbers, and then return reverting the sign.

```python

import heapq
def findKthLargest(nums):
    
    pq = [-x for x in nums]
    heapq.heapify(pq) # NOTE: doesn't return anything, modifies array in-place

    ans = None
    
    while k:
        k -= 1
        ans = heapq.heappop(pq)

    return -ans

```

Could you do the same in a *stream* ?
### Top K Frequent Elements

Given an integer array `nums` and an integer `k`, return _the_ `k` _most frequent elements_. You may return the answer in **any order**.

```
Input: nums = [1,1,1,2,2,3], k = 2
Output: [1,2]
```

In python its straightforward to use Min-Heap and use `nlargest` to get last k elements or use `nsmallest` with Max Heap (use `negative` values to create one)

```python

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        f = Counter(nums)
        pq = [(v, key) for key, v in f.items()]
        heapq.heapify(pq)
        return [key for v, key in heapq.nlargest(k, pq)]
        
```

### Minimum Cost to Connect Ropes

Given an array, **arr[]** of rope lengths, connect all ropes into a single rope with the **minimum total cost**. The **cost** to connect two ropes is the **sum of their lengths**.

Since cost of connecting the ropes is directly dependent on the two pieces we pick, smaller they are, smaller it costs. So just always take 2 smallest items from heap and put their joined length back in the heap, keep doing this until left with 1 Rope

### Kth Largest Element in the Stream

Implement the `KthLargest` class:

- `KthLargest(int k, int[] nums)` Initializes the object with the integer `k` and the stream of test scores `nums`.
- `int add(int val)` Adds a new test score `val` to the stream and returns the element representing the `kth` largest element in the pool of test scores so far.

So here an obvious thought comes store all the numbers which would be impossible for stream (hint), Even if we store the numbers, putting one number in the heap and then getting `nlargest` will take atleast $O(n.k)$ for n queries and `k` the largest number

A better solution is to maintain heap of size `k`, since every number smaller than `kth` largest number never would be the answer we can drop it and return directly smallest number, and if its larger, put it in heap, run heap invariant (of )size k) and drop the largest number.


```python

import heapq
class KthLargest:

    def __init__(self, k: int, nums: List[int]):
        self.pq = heapq.nlargest(k, nums)
        self.size = k
        heapq.heapify(self.pq)
        
    def add(self, val: int) -> int:
        if len(self.pq) < self.size: # if heap is not k-heap, push elements
            heapq.heappush(self.pq, val)
        elif self.pq[0] < val:
            heapq.heappushpop(self.pq, val)
        return self.pq[0]

```


## Median Maintenance

* Maintain the median of a dynamic data stream efficiently
* Use two-heaps
    * A max-heap for the lower half of the numbers
    * A min-heap for the upper half of the numbers
* Balancing the heaps ensures
    * The max-heap size is equal to or one more than the min-heap size
    * Median is either the top of the max-heap (odd cnt) or average of tops of both heaps (even cnt)

Use Cases

* Real-time Statistics
* Running median in Sensor Data
* Financial Analytics

```python

import heapq

class MedianFinder:
    def __init__(self):
        self.left = []   # max-heap (store negatives)
        self.right = []  # min-heap

    def addNum(self, num: int) -> None:
        # Step 1: push to appropriate heap
        if not self.left or num <= -self.left[0]:
            heapq.heappush(self.left, -num)
        else:
            heapq.heappush(self.right, num)

        # Step 2: rebalance
        if len(self.left) > len(self.right) + 1:
            heapq.heappush(self.right, -heapq.heappop(self.left))
        elif len(self.right) > len(self.left) + 1:
            heapq.heappush(self.left, -heapq.heappop(self.right))

    def findMedian(self) -> float:
        if len(self.left) == len(self.right):
            return (-self.left[0] + self.right[0]) / 2
        elif len(self.left) > len(self.right):
            return -self.left[0]
        else:
            return self.right[0]

```


## Heap-based Sorting & Merging

### HeapSort

* Use a *max-heap* to sort an array in-place
* Steps
    * Build a *max-heap* from input array
    * Repeatedly extract the maximum element and place it at the end
    * Heapify the reduced heap
* Time Complexity: $O(n \log n)$
* Space Complexity: $O(1)$ (in-place)

### Sort K Sorted Array

**Problem Statement:** Given an array `arr[]` and a number k . The array is sorted in a way that every element is at max k distance away from it sorted position. It means if we completely sort the array, then the index of the element can go from i - k to i + k where i is index in the given array. Our task is to completely sort the array.

```
Input :  arr = [6, 5, 3, 2, 8, 10, 9], k = 3  
Output :  [2, 3, 5, 6, 8, 9, 10]  
Explanation :  The element 2 was at index 3, it moved to index 0. The element 3 was at index 2, it moved to index 1. The element 5 moved from index 1 to index 2. The element 6 moved from index 0 to index 3. The rest (8, 9, 10) were near their correct spots and shifted slightly.
```

We know each element is `k` distance away from its correct place, That means the smallest element of the array exists in first k+1 entries.

Put first `k+1` entries on heap, and take smallest, then slide the window or add another element to heap, again take smallest element, keep doing till your stack is empty.


```python

import heapq
def sortNearlySortedArray(nums, k):
    n = len(nums)
    pq = nums[:min(k+1,n)] # copy first k + 1 elements
    
    heapq.heapify(pq)
    
    res = []
    
    for i in range(k+1, n):
        res.append(heapq.heappop(pq))
        heapq.heappush(pq, arr[i])
    
    while pq:
        res.append(heapq.heappop(pq))
        
    return res

```

Here complexity would be : $O(n \log k)$, We insert k times at max in the heap, for each number, 
### Merge K Sorted Lists/Array

[Video Explanation](https://www.youtube.com/watch?v=xS9Qix5RDA8&list=PL3edoBgC7ScV9WPytQ2dtso21YrTuUSBd&index=21)

You are given an array of `k` linked-lists `lists`, each linked-list is sorted in ascending order.
_Merge all the linked-lists into one sorted linked-list and return it._


```
Input: lists = [[1,4,5],[1,3,4],[2,6]]
Output: [1,1,2,3,4,4,5,6]
Explanation: The linked-lists are:
[
  1->4->5,
  1->3->4,
  2->6
]
merging them into one sorted linked list:
1->1->2->3->4->4->5->6
```


* Use a *min-heap* to efficiently merge K sorted list
* Steps
    * Insert the first element of each list into the min-heap
    * Extract the smallest element from the heap and add it to the merged output.
    * Insert the next element from the extracted element’s list into the heap.
    * Repeat until all elements are processed.
* Time Complexity: $O(N \log K)$

```python

import heapq
class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    
        ListNode.__eq__ = lambda self, other: self.val == other.val
        ListNode.__lt__ = lambda self, other: self.val < other.val

        pq = []

        head = tail = ListNode(0)

        for lst in lists:
            if lst:
                heapq.heappush(pq, (lst.val, lst))

        while pq:
            node = heapq.heappop(pq)[1]
            tail.next = node
            tail = tail.next

            if node.next:
                heapq.heappush(pq, (node.next.val, node.next))
        
        return head.next

```

To merge lists which are already sorted in $O(n \log k)$ time, we can use python in-built.

```python
import heapq

# Two sorted lists
list1 = [1, 4, 7]
list2 = [2, 5, 8]
list3 = [3, 6, 9]

# Merging the sorted lists
merged_list = list(heapq.merge(list1, list2, list3))
print(merged_list)

```

### Hand of Straight/Divide array in sets of k-consecutive numbers

Alice has some number of cards and she wants to rearrange the cards into groups so that each group is of size groupSize, and consists of groupSize consecutive cards.

Given an integer array hand where `hand[i]` is the value written on the `ith` card and an integer groupSize, return true if she can rearrange the cards, or false otherwise.

```
Input: hand = [1,2,3,6,2,3,4,7,8], groupSize = 3
Output: true
Explanation: Alice's hand can be rearranged as [1,2,3],[2,3,4],[6,7,8]

```

We can store frequency of each card in a map, then we can put all (frequency, number) pairs in heap, and pick the number with lowest frequency and then try to find consecutive numbers within that groupSize of elements.

```python

class Solution:
    def isNStraightHand(self, hand: List[int], groupSize: int) -> bool:
        
        n = len(hand)

        if n % groupSize != 0:
            return False

        f = Counter(hand)

        pq = list(f.keys())
        heapify(pq)

        while pq:
            curr = pq[0] # get smallest card

            for i in range(groupSize):
                # card exhausted before forming sequence
                if f[curr + i] == 0:
                    return False
                f[curr+i] -= 1

                if f[curr + i] == 0:
                    if curr + i != heappop(pq):
                        return False
            
        return True

```



### Meeting Rooms II (Minimum Number of Meeting Rooms)

(253) : NOTE Solved in Interval sections

### Use Cases

* External Sorting
* Merging logs or streams
* Database Query Language

## Misc. Problems on Heap

### Design Twitter

[Design Twitter](https://leetcode.com/problems/design-twitter/description)

So Problem Requires us to quickly return the feed of the people he follows ordered by time and only 10 most recent.

So If we see the analyze the problem correctly, we need to fetch all people a person is following along with posts done by them.

So we can represent follower-followee relationship using graph (Used Set because of fast insert and delete criteria), and while maintaining a tweets map for each user.


```python

class Twitter:

    def __init__(self):
        # convert to max-heap
        self.timer = itertools.count(step=-1)
        self.tweets = collections.defaultdict(collections.deque)
        self.followees = collections.defaultdict(set)
        

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.tweets[userId].appendleft((next(self.timer), tweetId))

    def getNewsFeed(self, userId: int) -> List[int]:
        # aggregate tweets from followee and myself, notice its a set union
        tweets = heapq.merge(*(self.tweets[u] for u in self.followees[userId] | {userId}))
        return [t for _, t in itertools.islice(tweets, 10)]

    def follow(self, followerId: int, followeeId: int) -> None:
        self.followees[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.followees[followerId].discard(followeeId)


```