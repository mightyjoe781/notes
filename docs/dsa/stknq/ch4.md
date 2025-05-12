# Techniques

## Monotonic Stack

*A monotonic stack is a stack that maintains elements in increasing or decreasing order*

Applications

* Next Greater Element
* Largest Rectangle in Histogram
* Stock Span Problem

### Next Greater Element

````python
# Next Greater Element
nums = [2, 1, 2, 4, 3]
stack = []
res = [-1] * len(nums)
for i in range(len(nums)):
    while stack and nums[i] > nums[stack[-1]]:
        idx = stack.pop()
        res[idx] = nums[i]
    stack.append(i)
````

## Sliding Window Maximum

Given an array nums and window of size k, return the max of each sliding window

Applications

* Real-time data analysis
* Maximum in Streaming Data
* Temperature Monitoring, Sensor logs

````python
from collections import deque
def maxSlidingWindow(nums, k):
    dq, res = deque(), []
    for i in range(len(nums)):
        if dq and dq[0] <= i - k:
            dq.popleft()
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            res.append(nums[dq[0]])
    return res
````

