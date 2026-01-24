# Techniques

## Monotonic Stack

*A monotonic stack is a stack that maintains elements in increasing or decreasing order*

Applications

* Next Greater Element
* Largest Rectangle in Histogram
* Stock Span Problem
* Daily Temperature

### Next Greater Element

NOTE: Here we keep putting items in decreasing order in stack, if any item is greater than item on top of stack, we pop until we are able to place that item, in doing so we find that each element that was popped will have a right next greater element which is same as the one we have are trying to put in the stack.

NOTE: Notice we are storing indices in the stack

NOTE: Here its a monotonically decreasing stack,

````python
# Next Greater Element
nums = [2, 1, 2, 4, 3]
stack = []
res = [-1] * len(nums)
for i, v in enumerate(nums):
    while stack and nums[stack[-1]] < v:
        idx = stack.pop()
        res[idx] = v
    stack.append(i)
````

### Previous Smaller Element

NOTE: This is monotonically increasing stack

```python

nums = [4, 5, 2, 10, 8]
stack = []
res = [-1] * len(nums)

for i, v in enumerate(nums):
    while stack and nums[stack[-1]] >= v:
        stack.pop()
    res[i] = nums[stack[-1]] if stack else -1
    stack.append(i)

```

### Stock Span Problem

The stock span problem is a financial problem where we have a series of daily price quotes for a stock and we need to calculate the span of stock price for all days.  
You are given an array **arr[]** representing daily stock prices, the stock span for the **i-th** day is the number of consecutive days up to day i (including day i itself) for which the price of the stock is **less than or equal** to the price on day **i**. Return the span of stock prices for each day in the given sequence.

Hint : For day i, you only care about the **nearest previous day with a higher price**. Monotonically decreasing stack can answer this problem fast.

```python

def calculateSpan(prices):
    n = len(prices)
    span = [0] * n
    stack = []  # stores indices

    for i in range(n):
        while stack and prices[stack[-1]] <= prices[i]:
            stack.pop()

        if not stack:
            span[i] = i + 1
        else:
            span[i] = i - stack[-1] # j-i ~ 

        stack.append(i)

    return span

```
### Maximal Area in Histogram

This can be solved using the above concept on monotonically decreasing stack.


```python

def largestRectangleArea(self, heights: List[int]) -> int:
    stack = []
    max_area = 0
    heights.append(0)  # sentinel

    for i in range(len(heights)):
        while stack and heights[stack[-1]] > heights[i]:
            h = heights[stack.pop()]
            w = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, h * w)
        stack.append(i)

    heights.pop()
    return max_area

```
### Trapping Rainwater

![](assets/Pasted%20image%2020260111174414.png)

For computing the trapped water we need

- a left boundary,
- a right boundary
- a bottom

Water is trapped between two taller bars, not just next greater.

```python

# left boundary = stk[-1]
# right boundary = curr_idx i
# bottom = mid


def trap(self, height: List[int]) -> int:
    stack = []
    water = 0

    for i, h in enumerate(height):
        # resolve trapped water
        while stack and height[stack[-1]] < h:
            mid = stack.pop()  # bottom

            if not stack:
                break  # no left boundary

            left = stack[-1]
            width = i - left - 1
            bounded_height = min(height[left], h) - height[mid]
            water += width * bounded_height

        stack.append(i)

    return water

```

NOTE: In trapping rain water, water is calculated at the moment a bar is popped from a decreasing stack.

### Asteroid Collision

Here there are following scenarios possible. NOTE: In this problem sign decides the direction,

- Left destroyed Right : `[3, -1]`
- Right destroyed left : `[1, -3]`
- Both destroyed : `[2, -2]`
- No collision : `[2, 3]`

This question can be analyzed linearly with some condition check on neighbors,

- If left destroyed right asteroid, then no more to destroy, break
- If both destroyed, no more to destroy, break
- If right destroyed, left then there is a chance that it may destroy more on the left,  thus pop out left from stack, repeat and check again,
- If stack becomes empty all right asteroids destroyed all left asteroids, append right to stack

```python

def asteroidCollision(asteroids):
    stk = []
    for v in asteroids:
        # collision possible only when:
        # stack top moves right and current asteroid moves left
        while stk and stk[-1] > 0 and v < 0:
            # stack asteroid is smaller -> it explodes
            if stk[-1] + v < 0:
                stk.pop()
            # stack asteroid is larger -> current asteroid explodes
            elif stk[-1] + v > 0:
                break
            # equal size -> both explode
            else:
                stk.pop()
                break
        # executed only if current asteroid was NOT destroyed
        else:
            stk.append(v)

    return stk

```

### Sum of Subarray Ranges

Problem Link 2104 - [Link](https://leetcode.com/problems/sum-of-subarray-ranges/description/)

You are given an integer array `nums`. The range of a subarray of `nums` is the difference between the largest and smallest element in the subarray.

Most trivial approach to this problem is $O(n^2)$ where we track `minValue` and `maxValue` for every window.

There is a $O(n)$ of solution for this using Monotonic Stack.

Definition of this problem

$$
\Sigma_k \text{ range}_k = \Sigma_k (\text{ maxVal}_k - \text{ minVal}_k) = \Sigma_k \text{ maxVal}_k - \Sigma_k \text{ minVal}_k
$$

Above equation implies if we are able to find `maxVal` of each subarray and `minVal` for each subarray separately then we can still solve the problem.

Now instead of thinking about the *maxValue* or *minValue*, focus on the value at hand. So for each number we should find number of subarray having `nums[i]` as its minimum value as `minTime[i]`

Then formally : 

$$
\Sigma_k \text{ minVal}_k = \Sigma_{i=1}^{n} \text{ minTime[i]} . \text {nums[i]}
$$

So problem reduces to finding `minTime` for each element.

`minTime[i]` depends on

- The number of consecutive elements larger than or equal to `nums[i]` on its left side.
- The number of consecutive elements larger than or equal to `nums[i]` on its right side.

$$
\begin{align}
minTime[i] &= (right - i).(i - left) \\
range_i &= minTime[i]. nums[i]
\end{align}
$$


![](assets/Pasted%20image%2020260111205640.png)

To calculate `minTime[i]` for every index, we can use a stack to maintain a *monotonically increasing sequence* during iteration over `nums`

- left = element on `nums[i]`'s left in stack
- right = element we are using to pop `nums[i]` from the stack


```python

def subArrayRanges(nums):
    n, answer = len(nums), 0 
    stack = []
    
    # Find the sum of all the minimum.
    for right in range(n + 1):
        while stack and (right == n or nums[stack[-1]] >= nums[right]):
            mid = stack.pop()
            left = -1 if not stack else stack[-1]
            answer -= nums[mid] * (mid - left) * (right - mid)
        stack.append(right)

    # Find the sum of all the maximum.
    stack.clear()
    for right in range(n + 1):
        while stack and (right == n or nums[stack[-1]] <= nums[right]):
            mid = stack.pop()
            left = -1 if not stack else stack[-1]
            answer += nums[mid] * (mid - left) * (right - mid)
        stack.append(right)
    
    return answer

```

### Remove K Digits

Problem Link - 402 - [Link](https://leetcode.com/problems/remove-k-digits/description/)

Given string num representing a non-negative integer `num`, and an integer `k`, return _the smallest possible integer after removing_ `k` _digits from_ `num`.

A dp solution to this problem somewhere along this line,

```python

def removeKdigits(self, num: str, k: int) -> str:
    n = len(num)

    @cache
    def solve(i, k, curr):

        if k == 0:
            if curr == "":
                return 0
            return int(curr)

        if i == n:
            return float('inf')
        
        return min(
            solve(i+1, k, curr),
            solve(i, k-1, curr[:i] + curr[i+1:])
        )
    
    return str(solve(0, k, num))

```

But above might not pass under the constraint when number is way too big.
Clearly we can see for each character we will have choice of choosing it and not choosing it, we get $2^{n}$ ~ over a million states and we cache them,

Correct way to approach is greedy + stack. As the smallest number would be the number that *increases*, so we can maintain that constraint using monotonically increasing stack.

```python


def removeKdigits(self, num: str, k: int) -> str:
    stack = []

    for d in num:
        while stack and k > 0 and stack[-1] > d:
            stack.pop()
            k -= 1
        stack.append(d)

    # remove remaining digits from the end
    stack = stack[:len(stack) - k]

    # remove leading zeros
    res = "".join(stack).lstrip('0')

    return res if res else "0"


```

### Sum of Subarray Minimums

This is just a smaller version of above question Sum of Subarray Ranges, just use the above code.

