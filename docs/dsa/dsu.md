# DSU

## Union-Find (Simple)

````c++
class UnionFind {
private:
  vector<int> p;
public:
  UnionFind(int N) {
    p.assign(N, 0); 
    for (int i = 0; i < N; ++i) 
      p[i] = i;
  }

  int findSet(int i) { return (p[i] == i) ? i : (p[i] = findSet(p[i])); }
  bool unionSet(int i, int j) {
    int x = findSet(i), y = findSet(j);
    if(x == y) return false;
    p[x] = y;
    return true;
  }
};
````



## Union-Find (Fastest Implementation)

````c++
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;

class UnionFind {                                // OOP style
private:
  vi p, rank, setSize;                           // vi p is the key part
  int numSets;
public:
  UnionFind(int N) {
    p.assign(N, 0); for (int i = 0; i < N; ++i) p[i] = i;
    rank.assign(N, 0);                           // optional speedup
    setSize.assign(N, 1);                        // optional feature
    numSets = N;                                 // optional feature
  }

  int findSet(int i) { return (p[i] == i) ? i : (p[i] = findSet(p[i])); }
  bool isSameSet(int i, int j) { return findSet(i) == findSet(j); }

  int numDisjointSets() { return numSets; }      // optional
  int sizeOfSet(int i) { return setSize[findSet(i)]; } // optional

  bool unionSet(int i, int j) {
    if (isSameSet(i, j)) return false;           // i and j are in same set
    int x = findSet(i), y = findSet(j);          // find both rep items
    if (rank[x] > rank[y]) swap(x, y);           // keep x 'shorter' than y
    p[x] = y;                                    // set x under y
    if (rank[x] == rank[y]) ++rank[y];           // optional speedup
    setSize[y] += setSize[x];                    // combine set sizes at y
    --numSets;                                   // a union reduces numSets
    return true;
  }
};
````

## Applications

* Cycle Detection in Graphs
* Connected Components
* Applications in Network Connectivity

Implementation of Above Application can be found in Graph Section.