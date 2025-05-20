# Matrix Problems

## Matrix Traversal

- SSince travel is possible from any (i, j) position in eight directions, use a direction vector to solve the problem of traversing the matrix efficiently.

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



## Sliding Window on 2D Grids