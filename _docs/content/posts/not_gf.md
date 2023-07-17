---
title: "How to incorrectly use Generating Function"
slug: not-gf
description: null
date: 2023-07-17T21:22:18+08:00
type: posts
summary: Generating functions can be used to *cheese* numerous counting problems without too much thinking. Here, I will show the **not** proper way to use generating function to solve such problems.
---

Generating functions can be used to *cheese* numerous counting problems without too much thinking.
Here, I will show the **not** proper way to use generating function to solve such problems.

A few people may find the generating function approach for some of these problems is more "intuitive", as the combinatorial approach is a bit out of the blue.


## [Codeforces 1549 E -- The Three Little Pigs](https://codeforces.com/contest/1549/problem/E)

> Given $N$, then given $Q$ queries, each gives you an integer $K$ and asks you to compute $\sum_{i=0}^N \binom{3i}{K}$
> - $N \le 1\\,000\\,000$

### Proper solution

Let $\text{dp}\_0(K)$, $\text{dp}\_1(K)$, and $\text{dp}\_2(K)$ be the sum $\sum_{i=0}^N \binom{3i}{K}$, $\sum_{i=0}^N \binom{3i + 1}{K}$, and $\sum_{i=0}^N \binom{3i + 2}{K}$ respectively.

We can see that:

* $\text{dp}\_0(K) + \text{dp}\_1(K) + \text{dp}\_2(K) = \sum_{i=0}^{3N+2} \binom{i}{K} = \binom{3N + 3}{K + 1}$ using the Hockey-stick identity;
* $\text{dp}\_1(K) = \text{dp}\_0(K) + \text{dp}\_0(K - 1)$ using the Pascal's rule; and
* $\text{dp}\_2(K) = \text{dp}\_1(K) + \text{dp}\_1(K - 1)$ using the Pascal's rule.

With three equations and three unknowns, the values of all DP can then be inferred.

### Generating function approach

Suppose we are able to evaluate $\sum_{i=0}^N (1 + x)^{3i}$, then for each query, the answer is the $K$-th coefficient of that generating function.

To evaluate that polynomial,

$$
\begin{align\*}
\sum_{i=0}^N (1 + x)^{3i} &= \frac{1 - (1 + x)^{3N + 3}}{1 - (1 + x)^3} \\\\
&= \frac{\sum_{i=1}^{3N + 3} \left(\binom{3N + 3}{i} x^i\right)}{-3x -3x^2 - x^3}
\end{align\*}
$$

The binomial coefficients from the numerator can be easily computed, then perform a standard long division to get the final G.F. in $\mathcal{O}(N)$.


## [AtCoder Regular Contest 110 D -- Binomial Coefficient is Fun](https://atcoder.jp/contests/arc110/tasks/arc110_d)

> Given a sequence $A$ of $N$ integers, compute the sum $\prod_{i=1}^N \binom{B_i}{A_i}$ over all sequences $B$ of $N$ non-negative integers whose sum is at most $M$.
> - $1 \le N \le 2000$
> - $1 \le M \le 10^9$
> - $0 \le A_i \le 2000$

### Proper solution

Suppose you have $\sum A_i + N$ bars and $M - \sum A_i$ stars.
The stars and bars before the $a_1$-th bar correspond to $\binom{B_1}{A_1}$; the stars and bars strictly between the $a_1$-th and $a_1 + a_2$-th bars correspond to $\binom{B_2}{A_2}$; and so on; and the stars after the $\sum A_i$-th bar are those that does not make the $B$ sum up to $M$.

The number of ways to arrange those stars and bars is then $\binom{M + N}{\sum A_i + N}$.

### Generating function approach

Recall that $[x^n] \frac{x^k}{(1 - x)^{k + 1}} = \binom{n}{k}$.

That means the sum of products from the description such that $B$ has a sum of exactly $m$ is the $m$-th coefficient of:

$$\prod_{i = 1}^N \frac{x^{A_i}}{(1 - x)^{A_i + 1}} = \frac{x^{\sum A_i}}{(1 - x)^{\sum A_i + N}}$$

And to get the sum for all coefficients of $x^m$ with $m \le M$, we can get the "prefix-sum" of the above G.F. (by multiplying it with $(1 - x)^{-1}$, and simply get the $M$-th coefficient. In short,

$$[x^M] \frac{x^{\sum A_i}}{(1 - x)^{\sum A_i + N + 1}}$$

which conveniently equals to $\binom{M + N}{\sum A_i + N}$.


## [IOI 2022 Circuit](https://ioinformatics.org/files/ioi2022problem4.pdf)

> Given a rooted tree of $N$ nodes, its leaves has initial state of $0$ or $1$. You can assign an integer parameter $p$ for each internal node (and $p$ is at most the number of its children), then its state will be $1$ if at least $p$ of its children have state $1$. Given $Q$ updates which toggle the state of the leaf nodes from $L$ to $R$, find the number of ways to assign those parameters such that the root node has a state of $1$.

### Proper solution

The assignment of a parameter to a node can be reinterpreted as an operator that takes a value from one of its children.
Hence, for each leaf with state $1$, we count how many ways are there to have its value reaching the root, which equals the product of all internal nodes', excluding the nodes that are in the path between the leaf to the root, number of children.

### Generating function approach

Denote $\text{dp}\_0(v)$ and $\text{dp}\_1(v)$ as the number of ways to assign parameters for all subtree of $v$ such that the state of $v$ is $0$ and $1$ respectively.

Suppose $v_1, \ldots, v_c$ is the children of $v$, then the number of ways such that exactly $k$ children of $v$ has state of $1$ is the $k$-th coefficient of:

$$\prod_{i=1}^c (\text{dp}\_0(v_i) + x \text{dp}\_1(v_i))$$

That means the number of ways to get state $1$ if we assign parameter $p$ to node $v$, is the sum of $k$-th ($k \ge p$) coefficient of the above G.F..
Summing for all possible $p$, we can see that we actually need the value $k$ times the $k$-th coefficient.
So we can transform the generating function by doing its derivative:

$$
\begin{align\*}
 &x \frac{\mathrm{d}}{\mathrm{d}x} \prod_{i=1}^c (\text{dp}\_0(v_i) + x \text{dp}\_1(v_i)) \\\\
=&x \frac{\mathrm{d}}{\mathrm{d}x} \exp \log \prod_{i=1}^c (\text{dp}\_0(v_i) + x \text{dp}\_1(v_i)) \\\\
=&x \frac{\mathrm{d}}{\mathrm{d}x} \exp \sum_{i=1}^c \log (\text{dp}\_0(v_i) + x \text{dp}\_1(v_i)) \\\\
=&\sum_{i=1}^c \frac{x \text{dp}\_1(v_i)}{(\text{dp}\_0(v_i) + x \text{dp}\_1(v_i))} \exp \sum_{i=1}^c \log (\text{dp}\_0(v_i) + x \text{dp}\_1(v_i)) \\\\
=&\sum_{i=1}^c \frac{x \text{dp}\_1(v_i)}{(\text{dp}\_0(v_i) + x \text{dp}\_1(v_i))} \prod_{i=1}^c(\text{dp}\_0(v_i) + x \text{dp}\_1(v_i)) \\\\
\end{align\*}
$$

And because we only need the sum of all those coefficients, we substitute $x = 1$, then obtain the final formula of the DP as:

$$\text{dp}\_1(v) = \sum_{i=1}^c \frac{\text{dp}\_1(v_i)}{(\text{dp}\_0(v_i) + \text{dp}\_1(v_i))} \prod_{i=1}^c(\text{dp}\_0(v_i) + \text{dp}\_1(v_i))$$

Now see that $\text{dp}\_0(v) + \text{dp}\_1(v)$ is equal to $\prod_{u \in \text{subtree}(v)} \deg(u)$ (where $\deg(u)$ is the number of children of $u$, except when $u$ is a leaf which we set to be $1$ for convenience) because we can assign any parameter to the nodes in the subtree of $v$ without any restriction to the end state of $v$. We denote this value as $p(v)$ which can be precomputed and stays constant throughout the whole update.

Rewrite our DP formula:

$$
\begin{align\*}
 \text{dp}\_1(v) &= \sum_{i=1}^c \frac{\text{dp}\_1(v_i)}{p(v_i)} \prod_{i=1}^c p(v_i) \\\\
&= \sum_{i=1}^c \left(\frac{p(v)}{\deg(v) p(v_i)} \text{dp}\_1(v_i)\right)
\end{align\*}
$$

Now, here comes the "Competitive Programming" part. Imagine you recurse the above formula up to the leaves.
Then, suppose $[u_0, u_1, \ldots, u_k]$ is the path from the root node $u_0$ to a leaf node $u_k$, compute $\prod_{i=1}^k \frac{p(u_{i-1})}{\deg(u_{i-1}) p(u_i)}$, and assign this value to the leaf node $u_k$. If the source gate $u_k$ is $1$, then the assigned value will contribute to the sum of the final answer. Otherwise, its contribution is $0$.
