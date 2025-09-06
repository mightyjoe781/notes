# Two Pointer

* Useful for handling sorted data or searching for pairs, triplets, or subarrays that meet specific conditions
* The core idea is to use two indices that move through the data structure at different speeds or in different directions to narrow the search space.

| Problem Type                        | Description                                                  | Movement Strategy                          |
| ----------------------------------- | ------------------------------------------------------------ | ------------------------------------------ |
| Pair with target sum                | Find two elements summing to a target value in a sorted array | Move left/right pointers inward            |
| Remove duplicates from sorted array | Remove duplicates in-place and return new length             | Slow and fast pointer moving forward       |
| Partition array                     | Rearrange elements based on a pivot                          | Left and right pointers moving inward      |
| Check palindrome                    | Check if a string is palindrome                              | Left and right pointers moving inward      |
| Triplets with zero sum              | Find all unique triplets that sum to zero                    | Fix one pointer, use two pointers for rest |

## Framework to Solve Problems

- Determine if the two-pointer technique applies.

    - Is the array or string sorted? Can it be sorted without violating constraints?
    - Are pairs, triplets, or subarrays required?
    - Can two loops be replaced by two pointers? NOTE: Extra Information by sorted constraint allows us to skip every pair check.

- Initialize the pointers
    - Usually, `l = 0` and `r = n-1` for pairs
    - For windows, `l` and `r` start at `0`

- Pointer moving conditions
    - If `sum` or `constraint` is more, move `r` to reduce it
    - If `sum` or `constraint` is less, move `l` to reduce it
    - For partitioning problems, swap elements and move pointers accordingly

- Stop Conditions : When pointers cross or meet, terminate

## Examples

* Remove Duplicates from Sorted Array In-Place

````c++
int removeDuplicates(vector<int>& nums) {
    if (nums.empty()) return 0;
    int slow = 0;
    for (int fast = 1; fast < nums.size(); fast++) {
        if (nums[fast] != nums[slow]) {
            slow++;
            nums[slow] = nums[fast];
        }
    }
    return slow + 1;
}
````

* Partition Array Around a Pivot

````c++
void partitionArray(vector<int>& nums, int pivot, int n) {
    int l = 0, r = n - 1;
    while (l <= r) {
        if (nums[l] < pivot) {
            l++;
        } else {
            swap(nums[l], nums[r]);
            r--;
        }
    }
}
````

## Problems

* [2 Sum with sorted Input](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/description/)
* [3 Sum](https://leetcode.com/problems/3sum/description/) : we can sort without violating constraint
* [(125) Valid Palindrome](https://leetcode.com/problems/valid-palindrome/)
