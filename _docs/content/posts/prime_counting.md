---
title: "On Prime Counting in Sublinear Time"
slug: prime-counting
description: null
date: 2019-12-22T14:00:39+08:00
type: posts
summary: We are to count how many prime numbers are there up to $N$ ($N \leq 10^{11}$). Let $\pi(N)$ be the number of primes up to $N$, and $f(n, p)$ be the number of integers $x$, for $2 \leq x \leq N$, such that it contains no prime factor $< p$. If $p$ is not prime, then $f(n, p) = f(n, p-1)$. Otherwise $$f(n, p) = f(n, p-1) - \left(f\Big(\big\lfloor\frac{n}{p} \big\rfloor, p-1\Big) - \pi(p-1)\right)$$ Our goal is to compute $\pi(N) = f(N, \sqrt N)$.
draft: false
mathjax: true

---


We are to count how many prime numbers are there up to $N$ ($N \leq 10^{11}$).

## Computation

Let $\pi(N)$ be the number of primes up to $N$, and $f(n, p)$ be the number of integers $x$, for $2 \leq x \leq N$, such that it contains no prime factor $< p$.

If $p$ is not prime, then $f(n, p) = f(n, p-1)$. Otherwise:

\begin{align}
f(n, p) = f(n, p-1) - \left(f\Big(\big\lfloor\frac{n}{p} \big\rfloor, p-1\Big) - \pi(p-1)\right)
\tag{1}
\end{align}

The value $f(\lfloor\frac{n}{p} \rfloor, p-1) - \pi(p-1)$ gives the number of integer $\leq N$ that has $p$ as its prime factor but no prime factor $< p$. In other words, it is subtracting $|\\{pk | 1 \leq k \leq n/p, \forall_{\text{prime }q  < p} q \nmid k \\}|$ from $f(n, p-1)$.

Our goal is to compute $\pi(N) = f(N, \sqrt N)$.

### Implementation

The idea is similar to the standard prime sieving: eliminate all numbers that is multiple of $2, 3, 5, \ldots, \sqrt N$.

1. Denote `dp[n]` as an array to store the number of primes up to $n$, and initiate the array `dp[n]` $= f(n, 1) = n-1$ for all unique values of $\lfloor \frac{N}{i} \rfloor$ (there are $O(\sqrt N) $such values).
2. For every prime $p$ in the range $[2, N]$, update `dp[n] -= dp[n/p] - dp[p-1]`, for all unique values of $n = \lfloor \frac{N}{i} \rfloor$ and $n \geq p^2$.
    - This is because when iterating prime $p$, all values of `dp[n]` is storing $f(n, p-1)$. In particular, for $n < p^2$, it is already storing the number of primes up to `n`.
    - Therefore, the operation `dp[n] -= dp[n/p] - dp[p-1]` is actually performing the equation from $(1)$.
    - By the end of this iteration, `dp[n]` will store $f(n, p)$.
3. Return `dp[N]` as our answer.

### Pseudo Code

```cpp
int primeCounting(int N) {
  Ni = sort_descending(unique([N/i for i in [1 .. N]]))
  for (n: Ni) {
    dp[n] = n-1
  }

  for (p = 2; p*p <= N; ++p) {
    if (dp[p] == dp[p-1]) continue; // p is not a prime
    for (n: Ni) {
      if (n < i*i) break;
      dp[n] -= dp[n/p] - dp[p];
    }
  }

  return dp[N];
}
```

### Complexity

It can be seen that the transition operation of $(1)$ is $O(1)$. Therefore, we just need to compute the space of $f(n, p)$.

There are two cases:

#### Case 1: $n \leq \sqrt N$

All values of $n \leq \sqrt N$ exists in the set $\\{ \lfloor \frac{N}{i} \rfloor \\}$, and for each $n$, only $p^2 \leq n$ will be considered.


Therefore the overall time complexity for this case:

$$ \sum_{i=1}^{\sqrt N} \sqrt i = O\left( \int_1^{\sqrt N} \sqrt x \\, dx \right) = O(N^{3/4})$$

#### Case 2: $n > \sqrt N$

The values of $n$ in this case is $\frac{N}{1}, \frac{N}{2}, \ldots, \frac{N}{\sqrt N}$. Since every $n$ needs to consider all $p^2 \leq n$, the time complexity for this case is:

$$ \sum_{i=1}^{\sqrt N} \sqrt{\frac{N}{i}} = O\left(\sqrt N \int_1^{\sqrt N} \frac{1}{\sqrt x} \\, dx \right) = O(N^{3/4})$$

#### Total Complexity

Since the complexity for both cases are the same, the total complexity is $O(N^{3/4})$

## Remarks

### Speeding Up Computation

It seems that we can speed up the computation by precomputing the first few prime numbers using the standard sieve of eratosthenes. Precompute the first $f(n, p)$ for $n \leq N^{2/3}$, then for the rest of the $n$, use the same iteration as above. This should run in a little more than $O(N^{2/3})$.

### Other Usages

With a few tweaks, we can compute the following with the same method:

- Sum of prime up to $n$.
- Sum of prime of the form $4k + 1$ up to $n$.
- Totient summatory function up to $n$.

Looks like it is also possible to further generalize this method using the Dirichlet Hyperbola method.

## References

- [The Meissel-Lehmer algorithm](https://en.wikipedia.org/wiki/Prime-counting_function#The_Meissel%E2%80%93Lehmer_algorithm)
- [Efficient Totient Summatory Function](https://math.stackexchange.com/questions/316376/how-to-calculate-these-totient-summation-sums-efficiently)
- [Sum of primes smaller than a big number](https://math.stackexchange.com/questions/1378286/find-the-sum-of-all-primes-smaller-than-a-big-number)
- [Dirichlet Hyperbola Method](https://en.wikipedia.org/wiki/Dirichlet_hyperbola_method)
