# Interval Problems

This section is specifically dedicated for problems related to intervals.

There are two types of intervals,

- Inclusive : `[start, end]`
    - They overlap if, `next.start <= curr.end`
    - Example: meetings that include both start and end time.
- Exclusive:  `[start, end)`
    - They overlap if, `next.start < curr.end`
    - Common: in CS/Scheduling

## Understanding Intervals ~ Merge/Overlap Basics

- Compare current interval with previous
- sort by start time

### Merge Intervals

[Link](https://leetcode.com/problems/merge-intervals/)

Given an array of intervals where `intervals[i] = [starti, endi]`, merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.

```python

def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    res = []

    for start, end in intervals:
        if not res or res[-1][1] < start:
            res.append([start, end])
        else:
            res[-1][1] = max(res[-1][1], end)

    return res

```

### Insert Interval

[Link](https://leetcode.com/problems/insert-interval/)

You are given an array of non-overlapping intervals `intervals` where `intervals[i] = [starti, endi]` represent the start and the end of the `ith` interval and `intervals` is sorted in ascending order by `starti`. You are also given an interval `newInterval = [start, end]` that represents the start and end of another interval.

```
Input: intervals = [[1,3],[6,9]], newInterval = [2,5]
Output: [[1,5],[6,9]]

Input: intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]
Output: [[1,2],[3,10],[12,16]]
Explanation: Because the new interval [4,8] overlaps with [3,5],[6,7],[8,10].
```

**Note** that you don't need to modify `intervals` in-place. You can make a new array and return it.

### Interval List Intersection

[Problem Link](https://leetcode.com/problems/interval-list-intersections/)

You are given two lists of closed intervals, `firstList` and `secondList`, where `firstList[i] = [starti, endi]` and `secondList[j] = [startj, endj]`. Each list of intervals is pairwise **disjoint** and in **sorted order**.

Return _the intersection of these two interval lists_.

A **closed interval** `[a, b]` (with `a <= b`) denotes the set of real numbers `x` with `a <= x <= b`.

The **intersection** of two closed intervals is a set of real numbers that are either empty or represented as a closed interval. For example, the intersection of `[1, 3]` and `[2, 4]` is `[2, 3]`.

Hint : Its similar to merge phase of merge sort.

```python

def intervalIntersection(A, B):

    i, j = 0, 0
    res = []
    n, m = len(A), len(B)

    while i < n and j < m:

        if A[i][1] < B[j][0]:
            i += 1
        elif B[j][1] < A[i][0]:
            j += 1
        else:
            # intersects
            res.append([max(A[i][0],B[j][0]), min(A[i][1], B[j][1])])
            if B[j][1] > A[i][1]:
                i += 1
            else:
                j += 1

    return res

```

NOTE: Try to take union of the both intervals.

## Greedy Interval Decisions

- Sort by end time
- Greedily Choose Intervals

### Non Overlapping Intervals

*minimal removals*, earliest end wins

Given an array of intervals `intervals` where `intervals[i] = [starti, endi]`, return _the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping_.

**Note** that intervals which only touch at a point are **non-overlapping**. For example, `[1, 2]` and `[2, 3]` are non-overlapping.

Actually, the problem is the same as "Given a collection of intervals, find the maximum number of intervals that are non-overlapping." (the classic Greedy problem: Interval Scheduling).

And we can return the remaining intervals to be removed, Greedily collect non-overlapping intervals which end first to maximize the number of non-overlapping intervals, minimizing removals.


```python

def eraseOverlapIntervals(intervals):
    # greedily pick earliest ending interval
    intervals.sort(key = lambda x: x[1])

    cnt, end = 0, float('-inf')
    for s, e in intervals:
        if s >= end:
            end = e
        else:
            cnt += 1 # overlapping found
    
    return cnt

```

### Minimum Number of Arrows to Burst Balloons


There are some spherical balloons taped onto a flat wall that represents the XY-plane. The balloons are represented as a 2D integer array `points` where `points[i] = [xstart, xend]` denotes a balloon whose **horizontal diameter** stretches between `xstart` and `xend`. You do not know the exact y-coordinates of the balloons.

Arrows can be shot up **directly vertically** (in the positive y-direction) from different points along the x-axis. A balloon with `xstart` and `xend` is **burst** by an arrow shot at `x` if `xstart <= x <= xend`. There is **no limit** to the number of arrows that can be shot. A shot arrow keeps traveling up infinitely, bursting any balloons in its path.

Given the array `points`, return _the **minimum** number of arrows that must be shot to burst all balloons_.

This is exactly same as above problem, First arrow should be fired at the end of first interval, then we can burst all the intervals intersecting with the first interval, until we find interval completely disjoint from the current interval, adding a new arrow thereby.

```python

def findMinArrowShots(points):

    points.sort(key=lambda x: x[1])
    cnt, last = 0, float('-inf')

    for s, e in points:
        if s > last:
            cnt += 1
            last = e
    
    return cnt

```


### Maximum Number of Events That Can Be Attended

You are given an array of events where `events[i] = [startDayi, endDayi]`. Every event i starts at startDayi and ends at endDayi.

You can attend an event i at any day d where `startDayi <= d <= endDayi`. You can only attend one event at any time d.

Return the maximum number of events you can attend.

To attend the maximum events, the events should be as short as possible, i.e. they should end as fast as they can.

Solution :

Using Above Solution will not work, as events here spans the days and if we have event spanning two days, 1st day we can attend event-1 and 2nd day we can attend 2nd Event.

![](assets/Pasted%20image%2020260118190137.png)
Here its 3 days

For following example its 4

```

Input: events= [[1,2],[2,3],[3,4],[1,2]]
Output: 4

Day 1 : Attend 1st day of [1, 2]
Day 2 : Attend 2nd day of last [1, 2]
Day 3 : Attend 3rd day of [2, 3]
Day 4 : Attend 4th day of [3, 4]

```


Best Approach treat each day as interval, `[1, 2), [2, 3), .....`
Now try to find as many as intervals you can in the each day !

Since only one meeting can be attended per day, we apply a greedy strategy: if it's possible to attend both meetings i and j on day k, we should prioritize the one with the earlier end time, i.e., `min(endDayi​,endDayj​)`. This ensures we leave more room to accommodate other meetings later.

Let the current day be i. At each day, we perform the following steps:

- Add to the candidate queue (the min-heap) all meetings whose start day is less than or equal to i. At this point, the heap contains all meetings available to attend on day i or earlier.
- Remove from the heap all meetings whose end day is less than i, as they can no longer be attended.
- If the heap is not empty, we attend the meeting with the earliest end time (which is at the top of the heap), increment the count of attended meetings by 1, and remove it from the heap.

Finally, return the total number of meetings attended.

```python

def maxEvents(events):

    n = len(events)
    max_day = max(event[1] for event in events)
    events.sort()

    pq = []
    ans, j = 0, 0

    for i in range(1, max_day + 1):
        while j < n and events[j][0] <= i:
            # push all events that starts before i the day
            heapq.heappush(pq, events[j][1])
            j += 1
        
        # discard invalid meetings
        while pq and pq[0] < i:
            heapq.heappop(pq)
        
        # take the shortest event, 
        if pq:
            heapq.heappop(pq)
            ans += 1
    
    return ans

```


## Meeting Rooms/ Concurrency

### Meeting Rooms

[Meeting Rooms](https://neetcode.io/problems/meeting-schedule/question)

Given an array of meeting time interval objects consisting of start and end times `[[start_1,end_1],[start_2,end_2],...] (start_i < end_i)`, determine if a person could add all meetings to their schedule without any conflicts.

**Note:** (0,8),(8,10) is not considered a conflict at 8

So Basically you go over all intervals, and if any where any overlap return false.

```python

from itertools import pairwise
class Solution:
    def canAttendMeetings(self, intervals: List[Interval]) -> bool:
        
        # sorting issue on the platform
        intervals.sort(key=lambda x: (x.start, x.end))
        for m1, m2 in pairwise(intervals):
            if m1.end > m2.start:
                return False
        return True

```

### Meeting Rooms II

Problem Link : [Link](https://neetcode.io/problems/meeting-schedule-ii/question)

Given an array of meeting time interval objects consisting of start and end times `[[start_1,end_1],[start_2,end_2],...] (start_i < end_i)`, find the minimum number of days required to schedule all meetings without any conflicts.

**Note:** (0,8),(8,10) is not considered a conflict at 8.

This problem can be thought of as finding the maximum overlapping that we can encounter, over given intervals.

```python

class Solution:
    def minMeetingRooms(self, intervals: List[Interval]) -> int:
        meetings = []
        for interval in intervals:
            meetings.append((interval.start, +1))
            meetings.append((interval.end, -1))
        
        meetings.sort()

        days, curr = 0, 0
        for t, d in meetings:
            curr += d
            days = max(curr, days)

        return days

```

For Dynamic Query using a Min Heap is preferred

- each meeting needs a room from its start time to its end time
- if a meeting starts **after or at the same time** another meeting ends, they can share the **same room**
- otherwise, we need a **new room**

To efficiently track room availability, we use a **min heap**:

- the heap stores the **end times** of meetings currently occupying rooms
- the smallest end time is always at the top, representing the room that frees up the earliest

As we process meetings in order of start time:

- if the earliest-ending meeting finishes before the current one starts, we can reuse that room
- otherwise, we must allocate a new room

The maximum size the heap reaches is the number of rooms needed.


```python

import heapq

class Solution:
    def minMeetingRooms(self, intervals: List[Interval]) -> int:

        intervals.sort(key=lambda x: (x.start, x.end))

        pq = []

        for interval in intervals:
            if pq and pq[0] <= interval.start:
                # reuse the same room
                heapq.heappop(pq)
            heapq.heappush(pq, interval.end)
        
        return len(pq)

```


### Car Pooling

https://leetcode.com/problems/car-pooling/

There is a car with `capacity` empty seats. The vehicle only drives east (i.e., it cannot turn around and drive west).

You are given the integer `capacity` and an array `trips` where `trips[i] = [numPassengersi, fromi, toi]` indicates that the `ith` trip has `numPassengersi` passengers and the locations to pick them up and drop them off are `fromi` and `toi` respectively. The locations are given as the number of kilometers due east from the car's initial location.

Return `true` _if it is possible to pick up and drop off all passengers for all the given trips, or_ `false` _otherwise_.

Solution is to use sweep line and make sure to never exceed the number of seats, or simulate using heaps.

Following is Simulation Solution

```python
class Solution:
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        
        trips.sort(key=lambda x:x[1])
        heap = []
        curr = 0
        for trip in trips:
            passenger, start, end = trip

            #First check the heap whether we can drop off any passengers:
            while heap and heap[0][0] <= start: #(end, passengers)
                dropped = heappop(heap)[1]
                curr -= dropped
            
            # Take the passengers of current trip
            curr += passenger
            if curr > capacity:
                return False
            # Add the current trip to heap to drop them off
            heappush(heap, (end, passenger))

        return True

```

## Sweep Line/Timeline

### Maximum Population Year

Easy StraightForward Line Sweep Problem : https://leetcode.com/problems/maximum-population-year/

Keep track of year you find maximum in for returning as answer.

### Number of Flowers in Full Bloom

https://leetcode.com/problems/number-of-flowers-in-full-bloom/

So in this problem, we can run sweep line algorithm to find the flowers existing at a specific time.

We will first create a difference array and then create prefix sum on top of it to answer queries fast regarding active flowers on that day !

![](assets/Pasted%20image%2020260118202709.png)

Then we can just binary search on the position and return the flowers that person sees,
example for 11 days, he will see 2 flowers (from 9 days-13days)

```python

from collections import Counter
class Solution:
    def fullBloomFlowers(self, flowers: List[List[int]], people: List[int]) -> List[int]:


        diff = Counter()

        for s, e in flowers:
            diff[s] += 1
            diff[e+1] -= 1
        
        pos = []
        prefix = []

        curr = 0

        for t, d in sorted(diff.items()):
            pos.append(t)
            curr += d
            prefix.append(curr)
        
        ans = []
        for person in people:
            i = bisect_right(pos, person) - 1
            ans.append(prefix[i])
        
        return ans


```

Using Simulation

```python

import heapq
class Solution:
    def fullBloomFlowers(self, flowers: List[List[int]], people: List[int]) -> List[int]:

        n = len(flowers)
        flowers.sort()
        sorted_people = sorted(people)

        dic = {}
        pq = []

        i = 0

        for person in sorted_people:
            # put all active flowers before the person comes
            while i < n and flowers[i][0] <= person:
                heapq.heappush(pq, flowers[i][1]) # end time
                i += 1
            
            # remove all flowers that have died down before person comes
            while pq and pq[0] < person:
                heapq.heappop(pq)

            dic[person] = len(pq) # active flowers that day

        return [dic[x] for x in people]

```

### Employee Free Time

https://leetcode.com/problems/employee-free-time/

Write a function to find the common free time for all employees from a list called schedule. Each employee's schedule is represented by a list of non-overlapping intervals sorted by start times. The function should return a list of finite, non-zero length intervals where all employees are free, also sorted in order.

```
schedule = [[[2,4],[7,10]],[[1,5]],[[6,9]]]
output = [(5, 6)]
```

Create difference array and track start and end time using sweep line, but whenever sum dips to zero, everyone is free so it becomes start of your interval, and then if it rises to 1 then that would be end of free time, collect all intervals created such way.

Simulation after flattening, then similar to balloon problem as above, 

```python

class Solution:
    def employeeFreeTime(self, schedule: List[List[List[int]]]):
        booked_time = []
        for intervals in schedule:
            for interval in intervals:
                booked_time.append(interval)
        
        booked_time.sort()
        if not booked_time:
            return []

        latest = booked_time[0][1]
        free_time = []
        for i in range(1, len(booked_time)):
            if latest < booked_time[i][0]:
                free_time.append([latest, booked_time[i][0]])
            latest = max(latest, booked_time[i][1])
        return free_time

```

## Scheduling with Constraints

*Sort + greedy + sometimes heap*

### Task Scheduler

[Task Scheduler](https://leetcode.com/problems/task-scheduler/)

You are given an array of CPU `tasks`, each labeled with a letter from A to Z, and a number `n`. Each CPU interval can be idle or allow the completion of one task. Tasks can be completed in any order, but there's a constraint: there has to be a gap of **at least** `n` intervals between two tasks with the same label.

Return the **minimum** number of CPU intervals required to complete all tasks.

```
Input: tasks = ["A","A","A","B","B","B"], n = 2
Output: 8
Explanation: A possible sequence is: A -> B -> idle -> A -> B -> idle -> A -> B.
After completing task A, you must wait two intervals before doing A again. The same applies to task B. In the 3rd interval, neither A nor B can be done, so you idle. By the 4th interval, you can do A again as 2 intervals have passed.
```

Simulation : If we notice that way to follow constraints we might need to add few idle times to the tasks, and the total size would be (tasks + idle)

We need to pick tasks greedily, when we are not able to schedule any of the task, we should put the idle thereby minimizing wastage of time.

*Observation, Choosing the task with highest frequency decreases the idle time for scheduler and vice-versa, so we should choose highest frequency task first.*

```python

from collections import Counter
from heapq import heapify
class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:

        freq = Counter(tasks)

        pq = [ -v for v in freq.values() ]
        heapify(pq)

        time = 0

        while pq:

            # create a cycle of n + 1 tasks
            cycle = n + 1
            store = []
            task_count = 0

            # execute tasks in each cycle
            while cycle > 0 and pq:
                current_freq = -heappop(pq)
                # if current_freq == 1 then it shouldn't put 
                # task back, as it is consumed
                if current_freq > 1:
                    store.append(-(current_freq-1))
                task_count += 1
                cycle -= 1
            
            # restore updated frequencies to heap
            # helps avoid re-evaluating the frequencies in same cycle
            for x in store:
                heappush(pq, x)
            
            # add time for the completed cycles
            time += task_count if not pq else n + 1
        
        return time


```

### Job Scheduling

We have `n` jobs, where every job is scheduled to be done from `startTime[i]` to `endTime[i]`, obtaining a profit of `profit[i]`.

You're given the `startTime`, `endTime` and `profit` arrays, return the maximum profit you can take such that there are no two jobs in the subset with overlapping time range.

If you choose a job that ends at time `X` you will be able to start another job that starts at time `X`.

NOTE: For Unweighted Interval Scheduling, we can easily use greedy algorithm. First sort by finish time(ascending order) then decide whether to fit the next interval in or not based on its start time.

Before thinking about this weighted Interval Scheduling problem, let's take a look at Unweighted Interval Scheduling, which is problem 646. *Maximum Length of Pair Chain*

```python

def findLongestChain(self, pairs: List[List[int]]) -> int:

    # greedily sort by end times
    pairs.sort(key=lambda x: x[1])

    last = float('-inf')

    cnt = 0
    for s, e in pairs:
        if s > last:
            last = e
            cnt += 1
    
    return cnt

```

But Greedy algorithm can fail spectacularly if arbitrary weights are allowed. So that's when DP comes in. From my understanding, greedy is a specific kind of DP, and DP is a general greedy.

For this problem we can still first sort by finish time(ascending order) then use DP to decide whether it is profitable to put in the next interval based on its value. Here is the essence:

Define Job j starts at `sj`, finishes at `fj`, and has weight or value `vj`, and `p(j) = largest index i < j` such that job `i` is compatible with `j`. Then it should be like:

`DP[j] = max(vj + DP[p(j)], DP[j-1])`

For optimizing we can use binary search to locate p(j).

```python

from bisect import bisect_left
from functools import cache

class Solution:
    def jobScheduling(self, startTime: List[int], endTime: List[int], profit: List[int]) -> int:

        # sort by endTime
        jobs = sorted(zip(startTime, endTime, profit))
        starts = [job[0] for job in jobs]
        n = len(jobs)

        @cache
        def dp(i):
            if i == n:
                return 0

            # Option 1: skip this job
            skip = dp(i + 1)

            # Option 2: take this job
            _, end, p = jobs[i]
            j = bisect_left(starts, end) # find compatible job, using binary search
            take = p + dp(j)

            return max(skip, take)

        return dp(0)

```

## Interval DP/Range DP

[Interval DP](../dp/mcm.md), By choosing a split point.


Problems :

- Burst Balloons
- Minimum Cost to Cut a Stick
- Strange Printer

## Dynamic Calendar/Interval Sets

- BST/Tree Map
- Ordered Intervals

### My Calendar I

https://leetcode.com/problems/my-calendar-i/

You are implementing a program to use as your calendar. We can add a new event if adding the event will not cause a **double booking**.

A **double booking** happens when two events have some non-empty intersection (i.e., some moment is common to both events.).

The event can be represented as a pair of integers `startTime` and `endTime` that represents a booking on the half-open interval `[startTime, endTime)`, the range of real numbers `x` such that `startTime <= x < endTime`.

Implement the `MyCalendar` class:

- `MyCalendar()` Initializes the calendar object.
- `boolean book(int startTime, int endTime)` Returns `true` if the event can be added to the calendar successfully without causing a **double booking**. Otherwise, return `false` and do not add the event to the calendar.

So the problem says that we need fast insertions for the calendar, quickly checking double booking.

So a naive approach is that we just keep a sorted list of intervals, and try to put the interval without conflicts but it will affect the sorted property and we will need to sort it again. This indicates to a structure which allow us to maintain sorted property even when multiple insertions are done, which points to BST.

We can insert interval in $O(\log n)$ and the structure will maintain sorted property!

```python

class Node:
    def __init__(self, s, e):
        self.val = (s, e)
        self.right = None
        self.left = None
        
class MyCalendar:

    def __init__(self):
        self.root = None

    def book_helper(self, s, e, node):
        if s >= node.val[1]:
            # right subtree is correct insertion
            if node.right:
                return self.book_helper(s, e, node.right)
            else:
                node.right = Node(s, e)
                return True
        
        elif e <= node.val[0]:
            # left subtree
            if node.left:
                return self.book_helper(s, e, node.left)
            else:
                node.left = Node(s, e)
                return True

        else:
            # conflicting
            return False

        

    def book(self, start: int, end: int) -> bool:
        if not self.root:
            self.root = Node(start, end)
            return True
        return self.book_helper(start, end, self.root)

```



### My Calendar II

https://leetcode.com/problems/my-calendar-ii/

You are implementing a program to use as your calendar. We can add a new event if adding the event will not cause a **triple booking**.

A **triple booking** happens when three events have some non-empty intersection (i.e., some moment is common to all the three events.).

The event can be represented as a pair of integers `startTime` and `endTime` that represents a booking on the half-open interval `[startTime, endTime)`, the range of real numbers `x` such that `startTime <= x < endTime`.

Implement the `MyCalendarTwo` class:

- `MyCalendarTwo()` Initializes the calendar object.
- `boolean book(int startTime, int endTime)` Returns `true` if the event can be added to the calendar successfully without causing a **triple booking**. Otherwise, return `false` and do not add the event to the calendar.

Here we are allowed to have 2 bookings but not more than that.

The key problem is preventing a new booking from overlapping with two existing overlapping bookings, which would create a triple booking. For example, in the list `[[3, 10], [4, 8], [10, 15], [20, 25]]`, no triple booking occurs despite overlaps. However, adding `[5, 7]` would overlap with both `[[3, 10], [4, 8]]`, leading to a triple booking.

To handle this, we track double-overlapping bookings. When `book(start, end)` is called, we check if the new booking overlaps with any double-overlapped bookings. If it does, we return `false`; otherwise, we return `true`, add the booking, and update the double-overlapped list if necessary.

Checking for overlap between two bookings `(start1, end1)` and `(start2, end2)` is done by verifying if `max(start1, start2) < min(end1, end2)`. This condition excludes endpoint overlaps, as the intervals are half-open. If they overlap, the overlap interval is `(max(start1, start2), min(end1, end2))`, also half-open.

```python

class MyCalendarTwo:

    def __init__(self):
        self.overlaps = []
        self.calendar = []
        

    def book(self, start: int, end: int) -> bool:
        for i, j in self.overlaps:
            if start < j and end > i:
                return False
        
        for i, j in self.calendar:
            if start < j and end > i:
                self.overlaps.append((max(start, i), min(end, j)))
        
        self.calendar.append((start, end))
        return True

```

Another Approach is to use Line Sweep as previous technique is not flexible if bookings count changes.

This is quite similar to flowers in Bloom Problem shared above, we keep track of frequencies and update the bookingCount for each interval, and then prefixSum returns every query regarding the time.

```python

from sortedcontainers import SortedDict
class MyCalendarTwo:

    def __init__(self):
        self.booking_cnt = SortedDict()
        self.max_overbook_allowed = 2
        

    def book(self, start: int, end: int) -> bool:

        self.booking_cnt[start] = self.booking_cnt.get(start, 0) + 1
        self.booking_cnt[end] = self.booking_cnt.get(end, 0) - 1

        overlapped_booking = 0

        for cnt in self.booking_cnt.values():
            overlapped_booking += cnt

            if overlapped_booking > self.max_overbook_allowed:
                self.booking_cnt[start] -= 1
                self.booking_cnt[end] += 1

                if self.booking_cnt[start] == 0:
                    del self.booking_cnt[start]

                return False
        
        return True
                

```

![](assets/Pasted%20image%2020260119013825.png)

Here amortized insertion in sorted Dict is $O(\log n)$, so insertion of an element can take $O(n\log n)$ just to insert one element,

### My Calendar III

https://leetcode.com/problems/my-calendar-iii/

Quite similar problem, best we can do is $O(n \log n)$ with sortedList

```python

from sortedcontainers import SortedList
class MyCalendarThree:

    def __init__(self):
        self.bookings = SortedList()
        

    def book(self, s: int, e: int) -> int:
        
        # O(log n)
        self.bookings.add([s, +1])
        self.bookings.add([e, -1])

        curr = 0
        res = float('-inf')
        for t, d in self.bookings:
            curr += d
            res = max(res, curr)

        return res

```


## Range Impact / Prefix-Sum Intervals

*Convert Interval -> Prefix Sum*

### Range Addition

Assume you have an array of length **_n_** initialized with all **0**'s and are given **_k_** update operations.

Each operation is represented as a triplet: **[startIndex, endIndex, inc]** which increments each element of subarray **A[startIndex ... endIndex]** (startIndex and endIndex inclusive) with **inc**.

Return the modified array after all **_k_** operations were executed.

```python

Input: length = 5, updates = [[1,3,2],[2,4,3],[0,2,-2]]
Output: [-2,0,3,5,3]

```

Generally We don't wanna apply the operation immediately, we defer and keep applying the changes as boundaries like interval sweeping and then apply it when we want to return the answer.

```python
from collections import defaultdict
def main(updates, n):
    # create map for this
    mp = defaultdict(int)

    for s, e, inc in updates:
        mp[s] += inc
        mp[e + 1] -= inc

    # on sorted keys
    res = []
    curr = 0
    for k in sorted(mp.keys()):
        curr += mp[k]
        res.append(curr)
    return res


```


### Corporate Flight Bookings : 

Exactly Same Problem as Above : https://leetcode.com/problems/corporate-flight-bookings/


### Count Number of Nice Subarrays

https://leetcode.com/problems/count-number-of-nice-subarrays/

Use Prefix Sum make sure that this `curr_sum - k` value exists already in the map and we can add that to count of our count
