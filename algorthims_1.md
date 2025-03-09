# Algorithms Learning Notes

## Basic Knowledge

### What is an Algorithm?

**Definition:** An algorithm is a step-by-step procedure designed to solve a specific computational problem.

Studying algorithms involves analyzing their **performance** (how fast they run) and **resource usage** (like memory). Performance analysis is crucial because:

- It transforms previously infeasible algorithms into practical ones.
- It provides a universal language to discuss program behavior independently from specific programming languages.

### Running Time

Running time measures algorithm efficiency. It depends primarily on two factors:

- **Nature of Input:** Certain inputs allow algorithms to run faster.
- **Input Size (n):** Larger input sizes typically result in increased running times.

We parameterize performance based on input size, usually considering it as `n → ∞`. Often, we focus on upper bounds, guaranteeing that performance won't exceed certain limits.

### Types of Algorithm Analysis

When analyzing algorithm performance, we consider three scenarios:

- **Worst Case:** The maximum running time over all possible inputs. Usually emphasized due to its safety guarantees.

- **Average Case:** The expected running time averaged over all possible inputs, assuming a specific statistical distribution.

- **Best Case:** The minimum running time, usually of theoretical interest, as it rarely occurs in practice.

### Key Idea in Algorithm Analysis

Two important principles:

- **Ignore Machine-Dependent Constants:** Focus on algorithmic structure rather than specific hardware.
- **Growth Rate:** Prioritize understanding how running time grows with increasing input sizes (as n approaches infinity).

### Asymptotic Notation

To simplify analysis, we use special notations that describe algorithm complexity by ignoring less significant terms and constants:

- **Θ (Theta) notation:** Describes asymptotic tight bound.

For example:

\[ 3n^3 + 90n^2 - n + 6064 = \Theta(n^3) \]

Lower-order terms and constants become negligible as input size grows.

---

## Problem One: Sorting Algorithms

### 1. Insertion Sort

**Idea:** Think about sorting playing cards. Each new card is inserted into the correct position relative to already sorted cards.

**Pseudocode:**

```
InsertionSort(A, n)
for j = 2 to n:
    key = A[j]
    i = j - 1
    while i > 0 and A[i] > key:
        A[i + 1] = A[i]
        i = i - 1
    A[i + 1] = key
```

**C++ Implementation:**

``` c++
void insertionSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 1; i < n; i++) {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
}
```

**Complexity Analysis:**

- **Worst-case (reverse-sorted input):** \(\Theta(n^2)\)
- **Average-case:** \(\Theta(n^2)\)
- **Best-case (already sorted):** \(\Theta(n)\)

### 2. Merge Sort

**Idea:** Divide-and-conquer approach. Recursively splits array into halves, sorts each half, and merges them.

**Pseudocode:**

```
  
MergeSort(A, left, right)
if left < right:
    mid = (left + right) / 2
    MergeSort(A, left, mid)
    MergeSort(A, mid + 1, right)
    Merge(A, left, mid, right)
```

**C++ Implementation:**

```cpp
#include <iostream>
#include <vector>
using namespace std;

void merge(vector<int>& arr, int left, int mid, int right) {
    vector<int> temp(right - left + 1);
    int i = left, j = mid + 1, k = 0;

    while (i <= mid && j <= right) {
        if (arr[i] <= arr[j]) temp[k++] = arr[i++];
        else temp[k++] = arr[j++];
    }

    while (i <= mid) temp[k++] = arr[i++];
    while (j <= right) temp[k++] = arr[j++];

    for (int m = 0; m < k; m++) arr[left + m] = temp[m];
}

void mergeSort(vector<int>& arr, int left, int right) {
    if (left >= right) return;

    int mid = left + (right - left) / 2;
    mergeSort(arr, left, mid);
    mergeSort(arr, mid + 1, right);
    merge(arr, left, mid, right);
}
```

**Complexity Analysis:**

- **Worst-case, Average-case, Best-case:** \(\Theta(n \log n)\)

---

By thoroughly understanding and practicing these basic algorithms, you'll build a solid foundation for more advanced algorithm studies!
