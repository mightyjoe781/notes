# Misc. Problems

## DP on Squares


### Maximal Rectangle

Problem Link 85 - [Link](https://leetcode.com/problems/maximal-rectangle/description/)

**2D DP (state compression) + Max–Min Greedy (Monotonic Stack)**

NOTE: This requires understanding of Monotonic Stack and Count maximal rectangle in Histogram Problem.

So we could say something like this for each column `j`

`height[j] = number of consecutive '1's ending at current row`

Final Answer would be Max over all rows.

NOTE: Histogram resets for the column if there is a 0 present in between.


```python
def maximalRectangle(self, matrix):
    if not matrix:
        return 0

    n, m = len(matrix), len(matrix[0])
    heights = [0] * m
    ans = 0


    # building the histogram
    for i in range(n):
        for j in range(m):
            if matrix[i][j] == '1':
                heights[j] += 1
            else:
                heights[j] = 0
        # find the maximal area in histogram
        ans = max(ans, self.largestRectangleArea(heights))

    return ans

def largestRectangleArea(self, heights):
    stack = []
    max_area = 0
    heights.append(0)

    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h: # monotonic stack
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)

    heights.pop()
    return max_area
```


### Count Square Submatrices with All Ones

Problem Link 1277 - [Link](https://leetcode.com/problems/count-square-submatrices-with-all-ones/description/)

**DP with local state + “propagation”**

Answer of this question would be `1x1, 2x2, 3x3` etc submatrices, and so on. Each cell of `1` would be a valid matrix of size `1x1`

For a valid `2x2` square ending at `(i, j)` following condition must be met

- The cell at `(i, j)` must be 1
- The cells above, left, and diagonally must also be `1`

![](assets/Pasted%20image%2020260107195526.png)

Similarly for `3x3` square it would be :

![](assets/Pasted%20image%2020260107195618.png)

So we construct bigger squares based on valid smaller squares.

```python
def countSquares(matrix):
    n, m = len(matrix), len(matrix[0])

    @cache
    def solve(i, j):
        if i < 0 or j < 0:
            return 0
        if matrix[i][j] == 0:
            return 0

        return 1 + min(
            solve(i-1, j),
            solve(i, j-1),
            solve(i-1, j-1)
        )

    # we are supposed count all valid such submatrices
    ans = 0
    for i in range(n):
        for j in range(m):
            ans += solve(i, j)

    return ans
```