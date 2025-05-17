# Binary Search

Binary search is a powerful algorithm for locating an element or solving optimization problems within a search space where the data meets specific criteria. The following is a concise summary and framework for applying binary search effectively:

Key Concepts

1. **Search Space:** 
   * A set of elements, such as indices, numbers, or a conceptual range, that can be ordered or partitioned. Examples include sorted arrays, monotonic functions, and intervals.

2. **Predicate (p(x))**: 
   * A boolean function (true/false) applied to items in the search space.
   * The predicate determines the behavior of the elements:
     * `F*T*`: false, false, false, true, true (transition from F to T).
     * `T*F*`: true, true, true, false, false (transition from T to F).
3. Applicability of Binary Search:
   * Binary Search is applicable if:
     * The search space is monotonic w.r.t. the predicate.
     * For `F*T*`: All F precede T.
     * For `T*F*`: All T precede F.
4. Goals of Binary Search:
   * Find the last F or the first T in `F*T*`.
   * Find the last T or the first F in `T*F*`.

## Framework to Solve Binary Search Problem

1. **Define the Search Space:**
   * Decide whether it is a range ([lo, hi]) or a collection (like an array).

2. **Define the Predicate (p(x)):**
   * Write a condition that transitions at a key point.

Example: For a sorted array and a target x, use p(x) = (arr[mid] >= target) for ``F*T*`.

3. **Decide the Goal:**
   * Find **first T**, **last F**, **last T**, or **first F** based on the problem.

4. **Write Binary Search:**
   * Use the appropriate loop (while(lo < hi) or while(lo <= hi)) and mid-point calculation:
     * low_mid: mid = lo + (hi - lo) / 2 (default).
     * high_mid: mid = lo + (hi - lo + 1) / 2 (if focusing on higher mid).

## Pseudo Codes

### For `F*T*` (Find Last F/First T)

````c++
int lastF(int lo, int hi) {
    while (lo < hi) {
        int mid = lo + (hi - lo + 1) / 2;  // Use high_mid
        if (p(mid))
            hi = mid - 1;  // Move left
        else
            lo = mid;      // Move right
    }
    return (!p(lo)) ? lo : -1;  // Check and return
}
````

````c++
int firstT(int lo, int hi) {
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;  // Use low_mid
        if (p(mid))
            hi = mid;      // Move left
        else
            lo = mid + 1;  // Move right
    }
    return (p(lo)) ? lo : -1;  // Check and return
}
````

### For `T*F*` (Find Last T/First F)

````c++
int lastT(int lo, int hi) {
    while (lo < hi) {
        int mid = lo + (hi - lo + 1) / 2;  // Use high_mid
        if (p(mid))
            lo = mid;      // Move right
        else
            hi = mid - 1;  // Move left
    }
    return (p(lo)) ? lo : -1;  // Check and return
}
````

````c++
int firstF(int lo, int hi) {
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;  // Use low_mid
        if (p(mid))
            lo = mid + 1;  // Move right
        else
            hi = mid;      // Move left
    }
    return (!p(lo)) ? lo : -1;  // Check and return
}
````

### **Tips to Remember**

1. **Predicate**: Design it to divide the search space into `F*T*` or `T*F*`.

2. **Mid Calculation**:
   * **low_mid**: lo + (hi - lo) / 2 (default for most cases).
   * **high_mid**: lo + (hi - lo + 1) / 2 (if skipping mid element is required).

3. **Focus**: Adjust lo or hi based on whether you move left or right.

4. **Post-Loop Check**: Always verify the result before returning to avoid off-by-one errors.

Binary Search simplifies problems when you clearly define the search space and the predicate.

### Further Study

[Divide & Conquer](../paradigm/dnc.md)