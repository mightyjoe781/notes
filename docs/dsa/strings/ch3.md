# Trie

A **Trie** (pronounced “try”) is a tree-like data structure used to store a dynamic set of strings. Each node in the Trie represents a single character, and strings are represented as paths from the root to a leaf node. It is mainly used for:

* Word search (exact match)

* Prefix search (words starting with a prefix)

Its commong use-cases are

* Auto-Complete
* Spell Checker
* Longest Prefix Matching

![Trie](./ch3.assets/1050.png)

````c++
class Trie {
public:
    Trie() { root = new TrieNode(); }

    // Insert a word into the Trie
    void insert(const string& word) {
        TrieNode* tmp = root;
        for (char c : word) {
            int i = c - 'a';
            if (tmp->next[i] == nullptr)
                tmp->next[i] = new TrieNode();
            tmp = tmp->next[i];
        }
        tmp->end = true;
    }

    // Check if a word exists in the Trie
    bool search(const string& word) {
        TrieNode* tmp = root;
        for (char c : word) {
            int i = c - 'a';
            if (tmp->next[i] == nullptr) return false;
            tmp = tmp->next[i];
        }
        return tmp->end;
    }

    // Check if any word starts with the given prefix
    bool startsWith(const string& prefix) {
        TrieNode* tmp = root;
        for (char c : prefix) {
            int i = c - 'a';
            if (tmp->next[i] == nullptr) return false;
            tmp = tmp->next[i];
        }
        return true;
    }

private:
    struct TrieNode {
        vector<TrieNode*> next;
        bool end;
        TrieNode() : next(26, nullptr), end(false) {}
    };

    TrieNode* root;
};
````

