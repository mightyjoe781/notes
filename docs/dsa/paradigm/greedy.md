# Greedy Algorithms & Strategies

* an algorithm that make the locally optimal choice at each step with the  hope of eventually reaching the globally optimal solution.

* a problem to be solved using greedy must exhibit these two property

    * It has optimal sub structures
    * It has the greedy property (difficult to prove in time -critical environment)

* **Coin Change**

    * Problem Statement:

    Given a target amount $( V )$ cents and a list of $( n ) $ coin denominations, represented as coinValue[i] (in cents) for coin types $ i \in [0..n-1] $, determine the minimum number of coins required to represent the amount \( V \). Assume an unlimited supply of coins of each type.

    Example: For \( n = 4 \) and coinValue = {25, 10, 5, 1} cents, to represent \( V = 42 \) cents, apply the greedy algorithm by selecting the largest coin denomination not exceeding the remaining amount: \( 42 - 25 = 17 \), \( 17 - 10 = 7 \), \( 7 - 5 = 2 \), \( 2 - 1 = 1 \), \( 1 - 1 = 0 \). This requires a total of 5 coins and is optimal.

    - The Problem has two properties

        - Optimal sub-structures

      These are

            - To represent 17 cents we use 10+5+1+1
            - To represent 7 cents we use 5+1+1

        - Greedy property- Given every amount V,we can greedily subtract the  largest coin denomination which is not greater than this amount V. It  can be proven that using any other strategies will not lead to an  optimal solution, at least for this set of coin denominations.

    - However **this greedy doesn’t always work** for all sets of coin denominations e.g.  cents. To make 6 cents with this set will fail optimal solution.

- **UVa - 11292 Dragon of Loowater (Sort the input first)**
    - This is a bipartite matching problem but still can be solved.
    - we match(pair) certain knights to dragon heads in maximal fashion. However, this problem can be solved greedily
    - Each dragon head must be chopped by a knight with the shortest height  that is at least as tall as the diameter’s of the dragon’s head.
    - However input is arbitrary order. Sorting Cost : $O(n \log n + m \log m)$, then to get answer $O(min(n, m))$

````c++
gold = d = k = 0; // array dragon and knight sorted in non decreasing order
while(d<n && k<m){
    while(dragon[d]> knight[k] && k<m) k++; //find required knight
    if(k==m) break;		//no knight can kill this dragon head,doomed
    gold+= knight[k]; // the king pays this amount of gold
    d++;k++;	//next dragon head and knight please
}

if(d==n) printf("%d\n",gold);		//all dragon heads arer chopped
else printf("Loowater is doomed!\n");
````

* Other classical Examples
    * Kruskal’s (and Prim’s) algorithm for the minimum spanning tree (MST)
    * Dijkstra’s (SSSP)
    * Huffman Code
    * Fractional Knapsacks
    * Job Scheduling Problem
* More on [Greedy](https://algo.minetest.in/CP3_Book/3_Problem_Solving_Paradigms/#greedy)

## Problems

* **Station Balance(Load Balancing)- UVa 410**
* **Watering Grass- UVa 10382**-(**Interval Covering**)