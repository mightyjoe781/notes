# Sliding Window

All problems of sliding window have similar basic idea: *Slide a sub-array(window) in a linear fashion from left to right over original array of n elements*.

Types:

1. find the smallest sub-array size(smallest window length) so that sum of the sub-array is greater or equal to a certain constant S in O(n).
2. find the smallest sub-array size(smallest window length) os that elements inside the sub-array contains all integers in range [1..K].
3. find the maximum sum of a certain sub-arry with static size K.
4. find the minimum of each possible sub-array with static size K.

Solutions

1. we keep a window that keeps on growing, append the element on the back of window and add it to some running sum or keeps shrinking (remove from front) as long as some constraint is satisfied like running sum >= S
2. we maintain a window that keeps growing if some constraint is not satisfied like [1..K] elements are not present otherwise keep shrinking it. We keep the smallest window thorhout the process and report the answer. To keep track of whether range [1..K] is covered or not, we can use some frequency counting. Its important to keep updating frequency is window grows or shrinks
3. insert K integers in window and compute its sum, and then declare as current maximum. Then just slide window over to right by adding last element and removing element in front. Keep track of maxima while doing this
4. this is challenging especially if n is quite large. To get O(n) solution use deque to model the window. this time we maintain that the window is sorted in ascending order, that is front element of deque is minimum. However this changes ordering of elements in the array. To keep track of whether an element is in window or not, we need to remember index of each element too. See example below

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
// Type-4
void SlidingWindow(int A[], int n, int K) {
  // ii---or pair<int, int>---represents the pair (A[i], i)
  deque<ii> window; // we maintain ‘window’ to be sorted in ascending order
  
  for (int i = 0; i < n; i++) { // this is O(n)
    while (!window.empty() && window.back().first >= A[i])
    	window.pop_back(); // this to keep ‘window’ always sorted
    window.push_back(ii(A[i], i));
    
  // use the second field to see if this is part of the current window
  while (window.front().second <= i - K) // lazy deletion
  	window.pop_front();
  if (i + 1 >= K) // from the first window of length K onwards
  	printf("%d\n", window.front().first); // the answer for this window
} }
````

