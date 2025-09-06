# Sliding Window

All sliding window problems share a basic concept: slide a sub-array (window) linearly from left to right over the original array of \(n\) elements.

## Common Problem Types

1. **find the smallest sub-array size**(smallest window length) such that sum of the sub-array is greater or equal to a certain constant S in O(n).
2. **find the smallest sub-array size**(smallest window length) such that elements inside the sub-array contains all integers in range [1..K].
3. **find the maximum sum** of a certain sub-arry with static size K.
4. **Find the minimum element** in every sub-array of size \(K\) — a classic problem solved efficiently using a deque.

## Solutions

- **Variable Size Window with Sum Constraint**
    - Maintain a window that **grows** by adding elements at the back (right pointer) and **shrinks** by removing elements from the front (left pointer) as long as the running sum meets or exceeds the target \(S\).
    - Continuously update the smallest window length satisfying the condition like `running sum >= S`

- **Variable Size Window with Frequency Constraints**
    - Expand the window until it contains **all required elements** (e.g., all integers in \([1..K]\)).
    - Use a frequency map to track counts of elements inside the window.
    - Shrink the window from the left while maintaining the constraint to find the minimal window.

- **Fixed Size Window for Maximum Sum**
    - Initialize the window with the first \(K\) elements and compute their sum.
    - Slide the window forward by removing the element at the front and adding the next element at the back.
    - Keep track of the maximum sum encountered.

- **Fixed Size Window for Minimum Element (Using Deque)**
    - Use a **deque** to maintain elements in ascending order within the current window.
    - For each new element:
    - Pop elements from the back of the deque while they are larger than the current element to maintain sorting.
    - Add the current element along with its index.
    - Remove elements from the front if they fall outside the current window.
    - The front of the deque always contains the minimum element for the current window.

- this is challenging especially if n is quite large. To get O(n) solution use deque to model the window. this time we maintain that the window is sorted in ascending order, that is front element of deque is minimum. However this changes ordering of elements in the array. To keep track of whether an element is in window or not, we need to remember index of each element too. See example below

````c++
// Type-1
// finding windows with sum == target
int subarraySum(vector<int>& nums, int k) {
    int res = 0, sum = 0;
  	// growing window
    for(int l = 0, r = 0; r < nums.size(); r++) {
        sum += nums[r];
      	// shrinking window
        while(sum > k && l < nums.size()) {
            sum-=nums[l];
            l++;
        }
      	// assess the condition to answer
        if(sum == k)
            res++;
    }
    return res;
}
````

````c++
// Type-4: Minimum in every subarray of size K using deque
void SlidingWindow(int A[], int n, int K) {
    // pair<int,int> represents (value, index)
    deque<pair<int, int>> window;  // maintain ascending order in window
    
    for (int i = 0; i < n; i++) {
        // Remove elements larger than current from the back
        while (!window.empty() && window.back().first >= A[i])
            window.pop_back();
        
        window.push_back({A[i], i});
        
        // Remove elements out of current window from front
        while (window.front().second <= i - K)
            window.pop_front();
        
        // Output minimum for windows starting from index K-1
        if (i + 1 >= K)
            printf("%d\\n", window.front().first);
    }
}
````

## Problems

* [209. Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/)
* [239. Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/)
* [76. Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/)
