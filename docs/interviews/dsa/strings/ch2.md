# String Matching

## Library Solution

Modern programming languages provide library solutions for basic string matching. These solutions are highly optimized and can be used directly for simple problems

### C++

C++ offers several built-in functions in the <string> library for string matching:

* `find()`: Returns the index of the first occurrence of a substring.
* `substr()`: Extracts a portion of the string.

````c++
string text = "hello world";
string pattern = "world";
size_t pos = text.find(pattern);
if (pos != string::npos) {
    cout << "Pattern found at index " << pos << endl;
} else {
    cout << "Pattern not found" << endl;
}
````

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

The Rabin-Karp algorithm uses hashing to find all occurrences of a pattern in a text.

Algorithm

* Precompute the hash of the pattern and the initial substring of the text of the same length.
* Slide over the text:
  * If the hashes match, verify the strings.
  * Recompute the hash for the next substring in O(1)
* Complexity: O(N + M) on average.

````c++
bool rabin_karp(string text, string pattern) {
    int n = text.size(), m = pattern.size();
    int base = 31, mod = 1e9 + 7;
    long long pattern_hash = 0, text_hash = 0, power = 1;

    for (int i = 0; i < m; i++) {
        pattern_hash = (pattern_hash * base + (pattern[i] - 'a' + 1)) % mod;
        text_hash = (text_hash * base + (text[i] - 'a' + 1)) % mod;
        if (i > 0) power = (power * base) % mod;
    }

    for (int i = 0; i <= n - m; i++) {
        if (pattern_hash == text_hash && text.substr(i, m) == pattern)
            return true;
        if (i < n - m) {
            text_hash = (text_hash - (text[i] - 'a' + 1) * power) % mod;
            text_hash = (text_hash * base + (text[i + m] - 'a' + 1)) % mod;
            if (text_hash < 0) text_hash += mod;
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



## Suffix Array

A suffix array is a sorted array of all suffixes of a string.

Algorithm

* Sort suffixes of the string using:
  * Radix Sort or precomputed ranks.
* Store starting indices of sorted suffixes.
* Complexity: $O(N \log N)$ .

````c++
vector<int> build_suffix_array(string s) {
    int n = s.size();
    vector<int> suffix_array(n), rank(n), temp(n);

    for (int i = 0; i < n; i++) suffix_array[i] = i, rank[i] = s[i];

    for (int k = 1; k < n; k *= 2) {
        auto compare = [&](int i, int j) {
            if (rank[i] != rank[j]) return rank[i] < rank[j];
            int ri = (i + k < n) ? rank[i + k] : -1;
            int rj = (j + k < n) ? rank[j + k] : -1;
            return ri < rj;
        };
        sort(suffix_array.begin(), suffix_array.end(), compare);

        temp[suffix_array[0]] = 0;
        for (int i = 1; i < n; i++) {
            temp[suffix_array[i]] = temp[suffix_array[i - 1]] + compare(suffix_array[i - 1], suffix_array[i]);
        }
        rank = temp;
    }
    return suffix_array;
}
````

