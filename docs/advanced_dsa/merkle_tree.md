# Merkle Trees

Problem : You are given two systems, you are supposed to maintain them in sync.

![](assets/Pasted%20image%2020260217114724.png)

A naive approach is to check each and every file in that directory and compare with the files from the remote system.

But we could approach it in atleast a better way where we compute the hash of Local and Remote System and compare it before scanning all directories for deltas.

But it still poses a difficulty when there are lots of files, but change is minuscule, and it happens too often.

Rather than storing hash of entire directory, we can store hash of each directory and build a logical tree, where parent hash is hash of concatenation of children's hash.

Key Idea : *Instead of hashing the whole dataset as a piece, hash the pieces and combine their hashes to build a tree.*

Verifying a single part requires only $\log (n)$ hashes.

Examples : Assume following 

```
project/
├── src/
│   ├── api/
│   │   ├── api.ts
│   │   └── scrapper.ts
│   │
│   ├── app/
│   │   ├── app.ts
│   │   └── runner.ts
│   │
├── test/
│   ├── states.ts
│   └── test.ts
```

Building a Merkle Tree

![](assets/Pasted%20image%2020260217115849.png)

Let's see we made a change in `scrapper.ts` then tree will trigger rebuilding hash on following nodes (highlighted)

![](assets/Pasted%20image%2020260217115953.png)

*So effectively changing any file in the directory changes the root hash*

So our syncing algorithm can quickly check whether root hashes match, if not then recursively try to find leaves which triggered this change.

We could employ this same algorithm for tracking large files, let's say several GBs,  PBs.

![](assets/Pasted%20image%2020260217120343.png)

### Use-Cases

- BlockChain (Bitcoin/Ethereum) 
    - Block header stores Merkle root, and then transactions build on merkle root using Block Hashes
    - Light clients only download Block Header + Merkle Proof, not the entire blockchain
- Distributed Databases (Cassandra, DynamoDB)
    - Instead of comparing full database, they compare merkle roots and mismatching branches.
- Git objects form a Merkle DAG
    - file -> blob hash
    - folder -> tree hash
    - commit -> parent + tree hash
    - commit ID -> snapshot integrity
- BitTorrent/IPFS
    - Verify Chunks independently
    - Download order is irrelevant

### Relationship with LSM Trees

- LSM Tree Solves : *fast writes*
- Merkle Trees solves : *verifiable reads*

Modern systems often combine both of them

- Cassandra : LSM + Merkle Tree
- Bitcoin : Append Log + Merkle Verification
- Git : Object Store + Merkle DAG

### Variants

- Sparse Merkle Tree : used in blockchains ( Supports proof of absence )
- Merkle DAG : git & IPFS content addressing


## Python Implementation

*NOTE : This is not production ready code, actual implementation might be more complicated*

```python

import hashlib

def h(data: bytes):
    return hashlib.sha256(data).hexdigest()
    
def build_merkle(leaves):
    level = [h(x.encode()) for x in leaves]

    while len(level) > 1:
        next_level = []
        for i in range(0, len(level), 2):
            left = level[i]
            right = level[i+1] if i+1 < len(level) else left
            next_level.append(h((left+right).encode()))
        level = next_level

    return level[0]
    
def merkle_proof(leaves, index):
    level = [h(x.encode()) for x in leaves]
    proof = []

    while len(level) > 1:
        if index % 2 == 0:
            sibling = level[index+1] if index+1 < len(level) else level[index]
            proof.append(("right", sibling))
        else:
            sibling = level[index-1]
            proof.append(("left", sibling))

        index //= 2

        next_level = []
        for i in range(0, len(level), 2):
            left = level[i]
            right = level[i+1] if i+1 < len(level) else left
            next_level.append(h((left+right).encode()))
        level = next_level

    return proof
    
def verify_proof(leaf, proof, root):
    cur = h(leaf.encode())

    for direction, sibling in proof:
        if direction == "right":
            cur = h((cur + sibling).encode())
        else:
            cur = h((sibling + cur).encode())

    return cur == root

```

|**Operation**| **Cost** |
|---|---|
|Build| O(n)     |
|Verify| O(log n) |
|Proof size| O(log n) |
|Compare datasets| O(log n) 