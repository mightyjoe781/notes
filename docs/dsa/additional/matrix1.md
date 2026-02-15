# Matrix Problems

## Matrix Traversal

- SSince travel is possible from any (i, j) position in four/eight directions, use a direction vector to solve the problem of traversing the matrix efficiently.

### DFS

````c++
vector<vector<int>> dirs = {{1, 0}, {0, 1}, {-1, 0}, {0, -1}};

void dfs(vector<vector<int>>& grid, int i, int j, vector<vector<int>>& vis) {
  vis[i][j] = true;
  for(auto dir: dirs) {
    int x = i + dir[0];
    int y = j + dir[1];
    
    if(x < 0 || y < 0 || x >= grid.size() || y >= grid[0].size())
      	continue;
    if(vis[x][y])
      	continue;
    dfs(grid, x, y, vis);
  }
}
````

### BFS

````c++
vector<vector<int>> dirs = {{1, 0}, {0, 1}, {-1, 0}, {0, -1}};
queue<pair<int, int>> q;
q.push({sr, sc});

while(!q.empty()) {
  auto const &[i, j] = q.front(); q.pop();
	vis[i][j] = true;
  for(auto dir: dirs) {
    int x = i + dir[0];
    int y = j + dir[1];
    
    if(x < 0 || y < 0 || x >= grid.size() || y >= grid[0].size())
      	continue;
    if(vis[x][y])
      	continue;
    q.push({x, y});
  }
}
````

### Spiral

````c++
vector<int> spiralOrder(vector<vector<int>>& matrix) {
    if(matrix.empty()) return {};
    int m = matrix.size(), n = matrix[0].size();
    int top = 0, bottom = m - 1;
    int left = 0, right = n - 1;
    vector<int> result;

    while (top <= bottom && left <= right) {
        // Traverse from left to right
        for (int j = left; j <= right; j++) {
            result.push_back(matrix[top][j]);
        }
        top++;

        // Traverse downwards
        for (int i = top; i <= bottom; i++) {
            result.push_back(matrix[i][right]);
        }
        right--;

        if (top <= bottom) {
            // Traverse from right to left
            for (int j = right; j >= left; j--) {
                result.push_back(matrix[bottom][j]);
            }
            bottom--;
        }

        if (left <= right) {
            // Traverse upwards
            for (int i = bottom; i >= top; i--) {
                result.push_back(matrix[i][left]);
            }
            left++;
        }
    }
    return result;
}
````

A more elegant python solution is to rotate array and consume first row.

````python
def spirallyTraverse(self, matrix):
    result = []
    while matrix:
        result += matrix.pop(0)
        matrix = list(zip(*matrix))[::-1]
    return resul
````

### Zig-Zag

- Pretty Intuitive Traversal

## Matrix Rotation & Transformation

- **Rotation by 90 degrees (clockwise)**
    - For an $n \times n$ matrix \(M\), the element at position $(i, j)$ moves to $(j, n-1-i)$
    - Common approach:
        - **Transpose** the matrix: swap `M[i][j]` with `M[j][i]`
        - **Reverse each row**.
- Rotation by 90 degrees (counter clockwise)
    - Transpose the Matrix
    - Reverse each columns
    - or do the reverse each row, then transpose
- General Transformations
    - Translation
    - Scaling 
    - Rotation by angle $\theta$

## Prefix 2D Sum


````c++
int m = matrix.size();
int n = matrix[0].size();
vector<vector<int>> prefix(m, vector<int>(n, 0));

for (int i = 0; i < m; i++) {
    for (int j = 0; j < n; j++) {
        int top = (i > 0) ? prefix[i-1][j] : 0;
        int left = (j > 0) ? prefix[i][j-1] : 0;
        int diag = (i > 0 && j > 0) ? prefix[i-1][j-1] : 0;
        prefix[i][j] = matrix[i][j] + top + left - diag;
    }
}
````

### Querying Submatrix Sum

````python
      (r1, c1)
         +---------------+
         |               |
         |     SUM       |
         |               |
         +---------------+
                         (r2, c2)
          
          
total = P[r2][c2]
if r1 > 0: total -= P[r1-1][c2]
if c1 > 0: total -= P[r2][c1-1]
if r1 > 0 and c1 > 0: total += P[r1-1][c1-1]
````

### Application

- Image Processing
- Histogram or Heatmap Analysis
- DP Optimization on 2D Grids

## Binary Search in Sorted Matrix

- Naive Method is to put all numbers in a vector then sort and search.

````python
def searchMatrix(matrix, target):
    if not matrix or not matrix[0]:
        return False

    n, m = len(matrix), len(matrix[0])
    low, high = 0, n * m - 1

    while low <= high:
        mid = (low + high) // 2
        row, col = divmod(mid, m)
        mid_val = matrix[row][col]

        if mid_val == target:
            return True
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1

    return False
````

## Pathfinding in Grids

### Dijkstra

````python
import heapq

def dijkstra(grid, start, goal):
    n, m = len(grid), len(grid[0])
    dist = [[float('inf')] * m for _ in range(n)]
    dist[start[0]][start[1]] = 0
    pq = [(0, start[0], start[1])]  # (cost, x, y)
    
    dirs = [(-1,0), (1,0), (0,-1), (0,1)]

    while pq:
        cost, x, y = heapq.heappop(pq)
        if (x, y) == goal:
            return cost
        for dx, dy in dirs:
            nx, ny = x+dx, y+dy
            if 0<=nx<n and 0<=ny<m and grid[nx][ny] != -1:
                new_cost = cost + grid[nx][ny]
                if new_cost < dist[nx][ny]:
                    dist[nx][ny] = new_cost
                    heapq.heappush(pq, (new_cost, nx, ny))
    return -1
````

### A*

**Use When:** You want Dijkstra + **heuristics** (e.g., Euclidean or Manhattan distance)

**Guarantees:** Optimal + faster than Dijkstra (if heuristic is admissible)

````python
def manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def astar(grid, start, goal):
    n, m = len(grid), len(grid[0])
    open_set = [(0 + manhattan(*start, *goal), 0, start[0], start[1])]  # (f = g + h, g, x, y)
    g_score = [[float('inf')] * m for _ in range(n)]
    g_score[start[0]][start[1]] = 0
    
    dirs = [(-1,0), (1,0), (0,-1), (0,1)]

    while open_set:
        f, g, x, y = heapq.heappop(open_set)
        if (x, y) == goal:
            return g
        for dx, dy in dirs:
            nx, ny = x+dx, y+dy
            if 0<=nx<n and 0<=ny<m and grid[nx][ny] == 0:
                ng = g + 1
                if ng < g_score[nx][ny]:
                    g_score[nx][ny] = ng
                    f_score = ng + manhattan(nx, ny, *goal)
                    heapq.heappush(open_set, (f_score, ng, nx, ny))
    return -1
````

## Matrix Exponentiation

https://codeforces.com/blog/entry/67776

- Powerful technique that can be used compute the terms of linear recurrence relations efficiently.
- General Recurrence relation looks like : $f_n = \Sigma^{k}_{i=1} c_i * f_{n-i}$, where $c_i$ could be zero, implying no dependence on that term.
- Let’s consider simple case of $f_n = \Sigma^{k}_{i=n} c_k * f_{n-k}$
- Consider this matrix

$$
T = \begin{bmatrix}
    0 & 1 & 0 & 0 & \dots  \\
    0 & 0 & 1 & 0 & \dots \\
    \vdots & \vdots & \vdots & \vdots & \vdots \\
    c_{k} & c_{k-1} & c_{k-2} & \dots  & c_{1}
\end{bmatrix}
$$



- And the $k * 1$ column vector $F$

$$
F = \begin{bmatrix}
    f_0 \\
    f_1 \\
    f_2 \\
    \vdots \\
    f_{k-1}
\end{bmatrix}
$$

$$
C = T * F = \begin{bmatrix}
    f_1 \\
    f_2 \\
    f_3 \\
    \vdots \\
    f_{k}
\end{bmatrix}
$$

- Its straightforward to see first $k-1$ entries of $C = T * F$. The $k^{th}$ entry is just the calculation of recurrence relation using the past *k* values of the sequence.So, when we obtain $C=T*F$, the first entry gives $f_1$. It is easy to see that $f_n$ is the first entry of the vector: $C_n = T^n * F$(Here $T^n$ is the matrix multiplication of T with itself *n* times).
- Example Matrix for Finbonacci sequence

$$
T = \begin{bmatrix}
    0 & 1 \\
    1 & 1 \\
\end{bmatrix}
$$

- Main Crux of Problem is getting the $T$ matrix
- Problem: Let’s write T, F matrix for $f_n = 2 * f_{i-1} + 3 * f_{i-2} + 4 * f_{i-3}$
- Solution for $f_n = 2 * f_{i-1} + 3 * f_{i-2} + 5$

$$
C = T * F = \begin{bmatrix}
    0 & 1 & 0 \\
    3 & 2 & 5 \\
    0 & 0 & 1
\end{bmatrix} * \begin{bmatrix}
    f_0 \\
    f_1 \\
    1
\end{bmatrix}
$$

- $n^{th}$ term will still be first entry of $C = T^n * F$
- To calculate $T^n$, use the concept of binary exponentiation to calculate it in $O(\log(n))$

## Binary Exponentiation

- This requires two function, one to multiply matrices, and second to perform exponentiation

````python
def mat_mult(A, B, mod=None):
    n = len(A)
    res = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                res[i][j] += A[i][k] * B[k][j]
                if mod:
                    res[i][j] %= mod
    return res
  
def mat_pow(mat, power, mod=None):
    n = len(mat)
    result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]  # Identity matrix
    while power > 0:
        if power % 2 == 1:
            result = mat_mult(result, mat, mod)
        mat = mat_mult(mat, mat, mod)
        power //= 2
    return result

# finbonacci in O(log n)
def fib(n):
    if n == 0:
        return 0
    base = [
        [1, 1],
        [1, 0]
    ]
    res = mat_pow(base, n - 1)
    return res[0][0]
````