# String Matching

## Library Solution

Modern programming languages provide library solutions for basic string matching. These solutions are highly optimized and can be used directly for simple problems

### C++

C++ offers several built-in functions in the `<string>` library for string matching:

* `find()`: Returns the index of the first occurrence of a substring.
* `substr()`: Extracts a portion of the string.

```c++
string text = "hello world";
string pattern = "world";
size_t pos = text.find(pattern);
if (pos != string::npos) {
    cout << "Pattern found at index " << pos << endl;
} else {
    cout << "Pattern not found" << endl;
}
```

### Python

Python simplifies string matching with built-in methods:

* `find()`: Returns the index of the first occurrence of a substring or -1 if not found.
* `in` **operator**: Checks for substring presence.

````c++
text = "hello world"
pattern = "world"
if pattern in text:
    print(f"Pattern found at index {text.find(pattern)}")
else:
    print("Pattern not found")
````

## String Hashing

String hashing is a preprocessing technique that converts a string into a numeric value (hash). This value allows efficient comparisons of substrings.

Algorithm

* Choose a **base** (e.g., 31) and a **modulus** (e.g., $10^9+7$).

* Compute the hash of the string using the formula:

  $$H[i] = (H[i-1] \cdot \text{base} + \text{char}[i]) \mod \text{modulus}$$

* Use **prefix hashes** to compute substring hashes efficiently.

````c++
vector<long long> compute_hash(string s, int base, int mod) {
    vector<long long> hash(s.size() + 1, 0);
    long long power = 1;
    for (int i = 0; i < s.size(); i++) {
        hash[i + 1] = (hash[i] * base + (s[i] - 'a' + 1)) % mod;
        power = (power * base) % mod;
    }
    return hash;
}
````

## Rabin-Karp

[Best Explanation of Rabin Karp](https://www.youtube.com/watch?v=4qEZned9qWM)

The Rabin-Karp algorithm uses hashing to find all occurrences of a pattern in a text.

Algorithm

* Precompute the hash of the pattern and the initial substring of the text of the same length.
* Slide over the text:
    * If the hashes match, verify the strings.
    * Recompute the hash for the next substring in O(1)
* Complexity: O(N + M) on average.
* Things to consider while implementation
    * Always verify with string comparison after hash match
    * Consider double hashing for critical applications
    * Birthday Paradox - The **Birthday Paradox** refers to the counterintuitive probability result that in a group of just 23 people, there is about a 50% chance that at least two people share the same birthday. Shows the vulnerability of hash functions to collisions, leading to the "birthday attack" where finding two inputs that hash to the same output is easier than expected.


````c++
bool rabin_karp(string text, string pattern) {
    int n = text.size(), m = pattern.size();
    if (m > n) return false;  // Pattern longer than text

    int base = 31;
    int mod = 1000000007;
    long long pattern_hash = 0, text_hash = 0, power = 1;

    // Precompute power = base^(m-1) % mod
    for (int i = 0; i < m - 1; i++) {
        power = (power * base) % mod;
    }

    // Compute initial hashes for pattern and first window of text
    for (int i = 0; i < m; i++) {
        pattern_hash = (pattern_hash * base + (pattern[i] - 'a' + 1)) % mod;
        text_hash = (text_hash * base + (text[i] - 'a' + 1)) % mod;
    }

    for (int i = 0; i <= n - m; i++) {
        // Check hash match and then verify substring to avoid false positives
        if (pattern_hash == text_hash && text.substr(i, m) == pattern) {
            return true;
        }

        // Compute hash for next window (if any)
        if (i < n - m) {
            text_hash = (text_hash - ((text[i] - 'a' + 1) * power) % mod + mod) % mod;  // Remove leading char
            text_hash = (text_hash * base + (text[i + m] - 'a' + 1)) % mod;            // Add trailing char
        }
    }
    return false;
}

````

## Z-Function

The Z-function computes an array where Z[i] is the length of the longest substring starting from i that matches the prefix of the string.

Applications

* Pattern Matching (Exact Match) : concatenate P and T : `P + '$' + T`, compute Z-function for such string. If $Z[i] \geq \text{length of } P$ , the pattern occurs starting at $i - (\text{length of } P + 1$) 
* Finding Periods in Strings
* Counting Unique Substrings
* String Compression

Algorithm

* Initialize Z[0] = 0 .
* Maintain a window [L, R] that matches the prefix.
* For each i :
    * If $i \leq R$, use previously computed values.
    * Otherwise, compute Z[i] directly
* Complexity: O(N)

````c++
vector<int> compute_z(string s) {
    int n = s.size();
    vector<int> z(n, 0);
    int l = 0, r = 0;

    for (int i = 1; i < n; i++) {
        if (i <= r) z[i] = min(r - i + 1, z[i - l]);
        while (i + z[i] < n && s[z[i]] == s[i + z[i]]) z[i]++;
        if (i + z[i] - 1 > r) {
            l = i;
            r = i + z[i] - 1;
        }
    }
    return z;
}
````

## Prefix Function (KMP) Algorithm

Very Good Explanation : [Link](https://www.youtube.com/watch?v=M9azY7YyMqI&list=PL3edoBgC7ScV9WPytQ2dtso21YrTuUSBd)

The Knuth-Morris-Pratt (KMP) algorithm avoids redundant comparisons by precomputing a prefix function(lps).

Algorithm

* Compute the prefix function:
    *  $\text{pi}[i]$ is the length of the longest prefix that is also a suffix for the substring ending at i .
* Use $\text{pi}[]$ to skip unnecessary comparisons
* Complexity: O(N + M).

````c++
vector<int> compute_prefix_function(string pattern) {
    int m = pattern.size();
    vector<int> pi(m, 0);

    for (int i = 1, j = 0; i < m; i++) {
        while (j > 0 && pattern[i] != pattern[j]) j = pi[j - 1];
        if (pattern[i] == pattern[j]) j++;
        pi[i] = j;
    }
    return pi;
}
````

````c++
// using above function to perform KMP Search
int strStr(string haystack, string needle) {
    int n = needle.size();
    if (n == 0) return 0;

    vector<int> lps = compute_prefix_function(needle);

    // Perform the KMP search
    int i = 0; 
    j = 0; 
    while (i < haystack.size()) {
        if (haystack[i] == needle[j]) {
            i++;
            j++;
        }
        if (j == n) {
            return i - n; // Pattern found at index (i - n)
        }
        if (i < haystack.size() && haystack[i] != needle[j]) {
            if (j > 0) {
                j = lps[j - 1];
            } else {
                i++;
            }
        }
    }

    return -1; // Pattern not found
}
````

