# Sqrt Decomposition

* Divides the array into blocks of size roughly $\sqrt{n}$.
* Each block stores the minimum value of that block.
* Lazy array stores pending updates for each block.

Range Updates

* If the update range is within a single block, apply updates directly to elements and rebuild that block
* If the update range spans multiple blocks:
  * Update partial blocks at the edges directly.
  * For full blocks in between, store lazy updates and update block minimum directly.

Range Minimum Query

* If query range is within a single block, check elements directly.
* Otherwise, check partial blocks at edges and use stored block minimum or lazy values for full blocks in between.
* Using ⁠``INT_MAX` as sentinel for "no update" can cause problems if ⁠`INT_MAX` is a valid value.

````c++
#include <bits/stdc++.h>
using namespace std;

class SqrtDecomposition {
private:
    int n, blockSize, numBlocks;
    vector<int> A;          // original array
    vector<int> blocks;     // stores minimum of each block
    vector<int> lazy;       // lazy updates for each block

    void applyLazy(int block) {
        if (lazy[block] != INT_MAX) {
            int start = block * blockSize;
            int end = min(n, start + blockSize);
            for (int i = start; i < end; i++) {
                A[i] = lazy[block];
            }
            blocks[block] = lazy[block];
            lazy[block] = INT_MAX;
        }
    }

    void rebuildBlock(int block) {
        int start = block * blockSize;
        int end = min(n, start + blockSize);
        int mn = INT_MAX;
        for (int i = start; i < end; i++) {
            mn = min(mn, A[i]);
        }
        blocks[block] = mn;
    }

public:
    SqrtDecomposition(const vector<int> &initialA) {
        A = initialA;
        n = (int)A.size();
        blockSize = (int)sqrt(n);
        numBlocks = (n + blockSize - 1) / blockSize;
        blocks.assign(numBlocks, INT_MAX);
        lazy.assign(numBlocks, INT_MAX);

        for (int i = 0; i < numBlocks; i++) {
            rebuildBlock(i);
        }
    }

    // Range update: set all elements in [l, r] to val
    void rangeUpdate(int l, int r, int val) {
        int startBlock = l / blockSize;
        int endBlock = r / blockSize;

        if (startBlock == endBlock) {
            applyLazy(startBlock);
            for (int i = l; i <= r; i++) {
                A[i] = val;
            }
            rebuildBlock(startBlock);
        } else {
            // Partial first block
            applyLazy(startBlock);
            int startBlockEnd = (startBlock + 1) * blockSize - 1;
            for (int i = l; i <= startBlockEnd; i++) {
                A[i] = val;
            }
            rebuildBlock(startBlock);

            // Full blocks in between
            for (int b = startBlock + 1; b < endBlock; b++) {
                lazy[b] = val;
                blocks[b] = val;
            }

            // Partial last block
            applyLazy(endBlock);
            int endBlockStart = endBlock * blockSize;
            for (int i = endBlockStart; i <= r; i++) {
                A[i] = val;
            }
            rebuildBlock(endBlock);
        }
    }

    // Range minimum query [l, r]
    int rangeMinQuery(int l, int r) {
        int startBlock = l / blockSize;
        int endBlock = r / blockSize;
        int mn = INT_MAX;

        if (startBlock == endBlock) {
            applyLazy(startBlock);
            for (int i = l; i <= r; i++) {
                mn = min(mn, A[i]);
            }
        } else {
            // Partial first block
            applyLazy(startBlock);
            int startBlockEnd = (startBlock + 1) * blockSize - 1;
            for (int i = l; i <= startBlockEnd; i++) {
                mn = min(mn, A[i]);
            }

            // Full blocks in between
            for (int b = startBlock + 1; b < endBlock; b++) {
                if (lazy[b] != INT_MAX) {
                    mn = min(mn, lazy[b]);
                } else {
                    mn = min(mn, blocks[b]);
                }
            }

            // Partial last block
            applyLazy(endBlock);
            int endBlockStart = endBlock * blockSize;
            for (int i = endBlockStart; i <= r; i++) {
                mn = min(mn, A[i]);
            }
        }
        return mn;
    }
};
````

