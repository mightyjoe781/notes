## Graph Search

### DFS



```c++
const UNVISITED = -1;
const VISITED = 1;

vector<int> dfs_num;				// initially all set to unvisited

void dfs(int u) {
  dfs_num[u] = VISITED;
  for(auto v:adj[u]) {
    if(dfs_num[v] == UNVISITED)
       dfs(v);
  } }

```

### BFS

````c++
// inside int main() -- no recursion
  vi d(V,INF); d[s] = 0;					// distance from source s to s is 0
  queue<int> q; q.push(s);

  while(!q.empty()) {
    int u = q.front(); q.pop();
    for(auto v:adj[u]) {
      if(d[v] == INF) {
        d[v] = d[u] + 1;
        q.push(v);
 } } }
````

