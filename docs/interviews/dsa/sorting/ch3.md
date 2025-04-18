# Mergesort

* Biggest Advantage is guaranted runtime : $O(N \log{N})$ (Independent of Input)
* Requires Additional Space : $O(N)$ (disadvantage)
* Guaranted Runtime can become liability. Some linear sorts can take take advantage of array properties.
* Stable (NOTE: Quicksort & Heapsort are not)
* Choice for Sorting Linked List
* Proper Example of Divide & Conquer

## Two-Way Merging

````c++
// two-way merging: given two ordered files (a, b), merge them into one (c)
template <class Item>
void mergeAB(Item c[], Item a[], int N, Item b[], int M){
    for(int i = 0, j = 0, k = 0; k < (M+N); k++){
        if(i == N){ c[k] = b[j++]; continue;}
        if(j == M){ c[k] = a[i++]; continue;}
        c[k] = (a[i] < b[j]) ? a[i++] : b[j++];
    }
}
````

## Inplace Merge

* Stable

````c++
// merge without sentinels, copy second array aux in reverse back to back with the first (putting aux in bitonic order)
template <class Item>
void merge(Item a[], int l, int m, int r){
    int i , j;
    static Item aux[maxN];
    for(i = m+1; i > l; i--) aux[i-1] = a[i-1];
    for(j = m; j < r ; j++) aux[r+m-j] = a[j+1];
    for(int k = l; k <= r ; k++)
				if(aux[j] < aux[i]) 
          a[k] = aux[j--]; 
  			else a[k] = aux[i++];
}
````

````c++
// top-down merge sort
template <class Item>
void mergesort(Item a[],int l , int r)
{
    if(r <= l ) return;
    int m = (r+l)/2 ;
    mergesort(a,l,m);
    mergesort(a,m+1,r);
    merge(a,l,m,r);
}
````

````c++
// bottom-up merge sort
template <class Item>
void mergesortBU(Item [a],int l, int r){
    for(int m = l; m <= r-l ; m = m+m )
        for(int i = l; i <= r-m; i += m+m)
            merge(a, i, i+m-1, min(i+m+m-1, r));
}
````

* NOTE: MergeSort can be improved by adding additional check to sort smaller partition using *insertion sort*

## Linked List Merge Sort

````c++
// merge
link merge(link a, link b ){
    node dummy(0); link head = &dummy, c= head;
    while((a!=0) && (b!=0))
        if(a->item < b->item)
        {c->next = a; c= a; a = a->next;}
    	else
        {c->next = b ;c= b ; b= b->next;}
    c->next = (a==0) ? b :a;
    return head->next;
}
// bottom-up
link mergesort(link t){
    QUEUE<link> Q(max);
    if(t == 0 || t->next == 0) return t;
    for(link u = 0 ; t != 0 ; t = u)
    {u = t->next ; t->next = 0; Q.put(t);}
    t = Q.get();
    while(!Q.empty())
    {Q.put(t); t = merge(Q.get(),Q.get());}
    return t;
}

// top-down
link mergesort(link c){
    if( c==0 || c->next == 0) return c;
    //splits link pointed by c into two lists a, b
    //then sorting two halves recursively
    //and finally merging them
    link a = c, b = c->next;
    while((b!=0) && (b->next!= 0))
    { c = c->next; b = b->next->next;}
    b = c->next; c->next = 0;
    return merge(mergesort(a),mergesort(b));
}
````

