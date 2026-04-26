# Hash Maps & Frequency Counting

To count element frequencies effectively, hash map (dictionary) are used by storing elements as keys and counts as values.

* Updates/Insertion/Lookup : Avg Time $O(1)$ 

* Hash Maps are already implemented in modern programming languages
    * C++ : `map` or `unordered_map` or `set` or `unordered_set`
    * Python: `dict` , `OrderedDict`

* Use cases
    * Anagram Detection
    * First Unique Character in String
    * Find all elements appearing >= n/3 times

* NOTE: More on Hashing will be discussed in Searching/Sorting Portions

### Collision Handling

| **Method**          | **Technique**              | **Use Case**             |
| ------------------- | -------------------------- | ------------------------ |
| **Chaining**        | Linked List in Each Bucket | High collision scenarios |
| **Open Addressing** | Linear/Quadratic Probing   | Memory optimization      |
| **Double Hashing**  | Secondary Hash Functions   | Reduced clustering       |

### Hash Functions

* Properties of a Good Hash Function
    * Prime number modulus reduces collisions
    * Cryptographic hashes (SHA) for security
    * Simple mod/bitmask for speed

## Usage

### Python

````python
# Creating a dictionary
employee = {"name": "Alice", "age": 30, "role": "Engineer"}

print(employee["name"])  # Output: Alice

# Adding or updating values
employee["department"] = "IT"
employee["age"] = 31

# Checking for a key
if "salary" in employee:
    print(employee["salary"])
else:
    print("No salary info")

# Iterating over keys and values
for key, value in employee.items():
    print(f"{key}: {value}")
    
# safe access
print(employee.get("email", "Not available"))  # Output: Not available
````

### STL

````c++
int main() {
    unordered_map<int, string> hashmap;

    // Inserting key-value pairs
    hashmap.insert({1, "Value 1"});
    hashmap[2] = "Value 2";
    hashmap[3] = "Value 3";

    // Accessing values
    cout << "Key 2: " << hashmap[2] << endl;

    // Checking if a key exists
    if (hashmap.find(4) != hashmap.end()) {
        cout << "Key 4 found!" << endl;
    } else {
        cout << "Key 4 not found!" << endl;
    }

    // Removing a key-value pair
    hashmap.erase(2);

    // Iterating over key-value pairs
    for (const auto& pair : hashmap) {
        cout << "Key: " << pair.first << ", Value: " << pair.second << endl;
    }
    return 0;
}
````



## Core Interview Patterns

### Pattern 1 - Complement Lookup (Two Sum)

The most fundamental hashmap pattern. Instead of checking all pairs O(n²), store what you've *seen* and look up what you *need*.

```python
def twoSum(nums, target):
    seen = {}  # value -> index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
```

**Generalisation:** any problem asking "does X + Y = target?" can use this. Also works for "does X - Y = k?" by storing differences.

Related problems: 4Sum, Subarray Sum Equals K (use prefix sums as keys).

### Pattern 2 - Group by Key (Anagrams / Bucketing)

When items that look different should be treated as equivalent, hash them to the same key.

```python
from collections import defaultdict

def groupAnagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))   # canonical form
        groups[key].append(s)
    return list(groups.values())
```

**Key insight:** the canonical form (sorted string, character count tuple, etc.) is the hash key. Everything that maps to the same key belongs in the same bucket.

Related problems: Group Shifted Strings, Find Duplicate File in System.

### Pattern 3 - Frequency Map + Sliding Window

Combine a hashmap tracking counts with a sliding window to answer "longest/shortest subarray with property P".

```python
def lengthOfLongestSubstring(s):
    freq = {}
    left = res = 0
    for right, ch in enumerate(s):
        freq[ch] = freq.get(ch, 0) + 1
        while freq[ch] > 1:          # window constraint violated
            freq[s[left]] -= 1
            left += 1
        res = max(res, right - left + 1)
    return res
```

**Template:** expand right → if constraint violated, shrink left → update answer.

Related problems: Minimum Window Substring, Longest Substring with At Most K Distinct Characters, Fruit Into Baskets.

### Pattern 4 - Prefix Sum + Hashmap (Subarray with Target Sum)

Store prefix sums as you go. `prefix[j] - prefix[i] = target` means subarray `[i+1..j]` sums to target.

```python
from collections import defaultdict

def subarraySum(nums, k):
    count = defaultdict(int)
    count[0] = 1   # empty prefix
    prefix = res = 0
    for num in nums:
        prefix += num
        res += count[prefix - k]
        count[prefix] += 1
    return res
```

Related problems: Contiguous Array (equal 0s and 1s), Subarray Sum Divisible by K.

### Problems

* Top K frequent Elements
* Sort Characters by Frequency
* First Unique Character
* Two Sum
* Group Anagrams
* Longest Substring Without Repeating Characters
* Subarray Sum Equals K
