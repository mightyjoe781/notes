# Divide & Conquer

- Divide the original problem into sub-problems-(usually half)
- Find (sub)-solutions for each of these sub-problems-which are now easier
- If needed combine the sub solutions to get a complete solution for the main problem.

***Divide and Conquer to find the maximum***

* function divides array into two halves and then finds the maximum

````c++
Item max(Item a[],int l, int r){
    if (l==r) return a[l];
    item m = (l+r)/2;
    Item u = max(a,l,m);
    Item v = max(a,m+1,r);
    if(u>v) return u; else return v;
}
````

* *Property* - A recursive function that divides a problem of size N into two independent (non empty) parts that it solves recursively calls itself less than N times.
* If parts are one of size k and one size `N-k`

$$
T_N = T_k + T_{N-k} + 1, for N \ge 1 \text{ with } T_1 = 0
$$

* Solution : $T_N = N - 1$ is immediate by induction

***Towers of Hanoi***

given 3 pegs and N disks that fit onto the pegs.  Disks differ in  size and are initially arranged on one of the pegs, in order from  largest(disk N) at the bottom to smallest (disk1) at the top.

The task is to move the stack of disks to the right one position(peg), while obeying the following rules

1. only one disk mat be shifted at a time
2. no disk may be placed on top of smaller one

*The recursive divide-and-conquer algorithm for the towers of Hanoi problem produces a solution that has $2^{N^{-1}}$ moves.*

* $T_N = 2 T_{N-1} + 1, for N \ge \text{ with } T_1 = 1$

***Solution to the towers of Hanoi problem***

````c++
void hanoi(int N,int d){
    if(N==0) return;
    hanoi(N-1,-d);
    shift(N,d);
    hanoi(N-1,-d);
}
````

there is a  correspondence with n-bit numbers is a simple algorithm  for the task. We can move the pile one peg to right by iterating the  following two steps until done:

1. Move the small disk to right if n is odd (left if n is even)
2. Make the only legal move not involving the small disk.

## Uncommon Usages of Binary Search

### The Ordinary Usage

- canonical usage is searching a item in static sorted array.
- complexity is $O(\log n)$
- pre-requisite for performing a binary search can also be found in other uncommon data structures like-root-to-leaf path of a tree (not necessarily binary nor complete ) that satisfies *min heap property* .

### Binary Search on Uncommon Data Structures

### Bisection Method

* also known as binary search on answer space

| Problem Name                                | Problem Number | Description                                                  |
| ------------------------------------------- | -------------- | ------------------------------------------------------------ |
| **Capacity To Ship Packages Within D Days** | 1011           | Binary search on the ship capacity range to find the minimum capacity to ship all packages within D days. |
| **Koko Eating Bananas**                     | 875            | Binary search on the eating speed to find the minimum speed to finish piles within H hours. |
| **Split Array Largest Sum**                 | 410            | Binary search on the largest sum allowed to split the array into m subarrays. |
| **Minimum Time to Complete Trips**          | 2187           | Binary search on time to find the minimum time to complete all trips given multiple buses. |

* All these problems rely on a simple concept. Consider a solution space from 0 to 100000. Usually, a solution exists at some point X within this range, such that every number greater than X is also a solution. Finding X becomes a problem solvable using binary search.

````c++
# gas station problem
#define EPS 1e-9

bool can(double f){	//simulation portion
    //return true if jeep reaches to its goal 
    //return false otherwise
}
//inside int main
// Binary Search the answer, then simulate
double lo =0.0, hi=1000.0, mid =0.0 ans =0.0;
while(fabs(hi-lo)>EBS){
    mid = (lo+hi)/2.0;
    if(can(mid)) { ans = mid ; hi = mid;}
    else 			lo=mid;
}
 printf("%.31f\n",ans);
````

