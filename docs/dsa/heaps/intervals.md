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

https://leetcode.com/problems/interval-list-intersections/

## Greedy Interval Decisions

### Minimum Number of Arrows to Burst Balloons

### Maximum Number of Events That Can Be Attended

## Meeting Rooms/ Concurrency

Meeting Rooms
https://leetcode.com/problems/meeting-rooms/
Meeting Rooms II
https://leetcode.com/problems/meeting-rooms-ii/
Car Pooling
https://leetcode.com/problems/car-pooling/

## Sweep Line/Timeline

Maximum Population Year
https://leetcode.com/problems/maximum-population-year/
Number of Flowers in Full Bloom
https://leetcode.com/problems/number-of-flowers-in-full-bloom/
Employee Free Time
https://leetcode.com/problems/employee-free-time/

## Scheduling with Constraints

## Interval DP/Range DP

[Interval DP](../dp/mcm.md)

Problems :

- Burst Balloons
- Minimum Cost to Cut a Stick
- Strange Printer

## Dynamic Calendar/Interval Sets

My Calendar I
https://leetcode.com/problems/my-calendar-i/
My Calendar II
https://leetcode.com/problems/my-calendar-ii/
My Calendar III
https://leetcode.com/problems/my-calendar-iii/


## Range Impact / Prefix-Sum Intervals

Corporate Flight Bookings
https://leetcode.com/problems/corporate-flight-bookings/
Count Number of Nice Subarrays
https://leetcode.com/problems/count-number-of-nice-subarrays/
