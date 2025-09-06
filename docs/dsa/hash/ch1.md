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



### Problems

* Top K frequent Elements
* Sort Characters by Frequency
* First Unique Character
