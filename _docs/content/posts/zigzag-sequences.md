---
title: "On counting the number of zigzag sequences"
slug: zigzag-sequences
description: null
date: 2022-07-10T18:30:00+08:00
type: posts
summary: We will describe on how to find the number of zigzag sequences $a_1 \lt a_2 \gt \ldots$ in $O(N \log N)$.
draft: false
---

I feel like these are classical, but it's hard to find a good discussion about them, so here we go.

We will discuss two things here:

* find the number of zigzag permutations, and
* find the number of zigzag sequences.

## Counting Zigzag permutations

Given $N \le 200\\;000$, find the number of permutations that satisfy $p_1 \lt p_2 \gt p_3 \lt p_4 \gt \ldots p_N$.

You may stop here if you are interested to solve the problem by yourself first.

### Terminologies

First, let us clear up the terminology we are going to use.

A *permutation* of length $N$ is a sequence of length $N$ where $1, 2, \ldots, N$ each appears exactly once.
In this article, whenever I omit the "of length $N$", the permutation always has length $N$ by default.

A *zigzag permutation* is a permutation $p$, such that $p_1 \lt p_2 \gt p_3 \lt p_4 \gt \ldots p_n$.
More formally, the relation $p_i \lt p_{i+1}$ is satisfied when $i$ is odd, and $p_i \gt p_{i+1}$ when $i$ is even.

We define similarly a *zagzig permutation* as a permutation $p$, such that $p_1 \gt p_2 \lt p_3 \gt p_4 \gt \ldots p_n$.
This is the same as zigzag permutation, as they both have alternating relations, but this one starts with $\gt$.

We will also collectively refer both *zigzag* and *zagzig* permutations as *alternating permutations*

### Catalan-like DP

Before getting to the calculation, we first note that there exists a bijection between zigzag permutations and zagzig permutations.
This is easy to show: for a zigzag permutation $p$, we map $p_i$ to $N - p_i + 1$.

Moreover, for $N \ge 2$ the set of zigzag permutations are mutually exclusive from the set of zagzig permutations.
This means that, if we know the cardinality of a set of alternating permutations (of length $N \ge 2$), then the cardinality of the zigzag permutations is exactly half of it.

Let $a_n$ be the number of zigzag permutations of length $n$.
That is, the number of alternating permutations is $2a_n$ for $n \ge 2$.

The key to compute $a_n$ is we consider every position of its largest element $n$, then we "attach" a reversed zigzag permutation to the left, then attach another zigzag permutation to the right of the largest element. Note that this will give you all the alternating permutations instead of the zigzag permutations alone. The elements that are to the left of the largest can be chosen from any of the remaining $n - 1$ elements.

To sum up:

$$2a_n = \sum_{k=0}^{n-1} \binom{n - 1}{k} a_k a_{n-1-k}$$

or to make it prettier:

$$2a_{n+1} = \sum_{k=0}^{n} \binom{n}{k} a_k a_{n-k}$$

for $n \ge 1$ with the base case $a_0 = a_1 = 1$.

This can be easily computed using DP in $O(N^2)$.

### Faster Computation

Let $A(x)$ be the exponential generating function of the sequence $(a)_n$. That is, 

$$A(x) = \sum_{k=0}^\infty \frac{a_k}{k!} x^k$$

Then,

$$2A(x) = \int A(x)^2 dx + x + 2$$

The purpose of the integration is to "shift" the EGF by one, and the $x + 2$ part is to make the base case of $[x^0]$ and $[x^1]$ be both $2$ (recall that we are computing $2A(x)$, not a single $A(x)$).

Let's solve the integration formula. We derive both sides:

$$2 \frac{\mathrm{d}}{\mathrm{d}x} A(x) = A(x)^2 + 1$$

Since I have nothing better to do, I will derive this ordinary differential equation in more details.
We divide both sides by $A(x)^2 + 1$ then integrate both sides.

$$\int \frac{2}{A(x)^2 + 1} \mathrm{d}A(x) = \int dx$$

Use the trigonometry substituion $A(x) = \tan(t)$ and we obtain:

$$\int \frac{2}{\tan(t)^2 + 1} \sec(t)^2 dt = x + C$$

Note the trigonometry identity $\tan(t)^2 + 1 = \sec(t)^2$, then:

$$2\arctan(A(x)) = x + C$$

We note that when $x = 0$, $A(0) = 1$, hence:

$$A(x) = \tan\left(\frac{x}{2} + \frac{\pi}{4}\right)$$

Use the tangent half-angle formula, and we finally obtain:

$$A(x) = \sec(x) + \tan(x) = \frac{1 + \sin(x)}{\cos(x)}$$

and this can be easily calculated in $O(N \log N)$ using FFT.

Apparently, the resulting generating function is also known as André's theorem.

## Counting Zigzag Sequences

Given $N \le 200\\;000$ and $M \le 10^9$, find the number of sequences of positive integers such that $a_i \le M$ and $a_1 \lt a_2 \gt a_3 \lt a_4 \gt \ldots a_N$.

To solve this problem, we must first forget everything from the previous section as they prove to be useless for this problem.

The key idea here is inclusion-exclusion, and we have to solve by cases.

### N is even

We will apply inclusion-exclusion on the "$\gt$" part.
What this means is we keep all the "$\lt$" signs, ignore some of the "$\gt$" conditions, and replace all the other "$\gt$" with "$\le$".
For every such replacement, count the number of the inequalities, then multiply by $(-1)^{\text{\\# of ≤}}$, then sum for all of the possible replacements.

The sum is not straightforward to come. Instead, for one possible replacement, we will consider a *chain* as the maximal subsegment such that $a_{2i+1} \lt a_{2i+2} \le a_{2i+3} \lt \ldots \le a_{2j}$. That is, the chain is a maximal consecutive subsequence such that it contains either "$\lt$" or "$\le$". Notice that such a chain always has an even length.

The number of sequences $b$ of length $2n$ (an even number) such that $b_1 \lt b_2 \le b_3 \lt \ldots \le b_{2n}$ can be easily found out as $\binom{M + n - 1}{2n}$.

Now, we just have to "glue" up all these chains to form a sequence of length $N$.

So we obtain this DP formula:

$$dp(n) = \sum_{k=1}^n (-1)^{k-1} \binom{M+k-1}{2k} dp(n-k)$$

and our answer is $dp(\frac{N}{2})$ which can be solved in $O(N^2)$.

To speed it up, define $P(x)$ as the generating function:

$$P(x) = \sum_{k=1}^\infty (-1)^{k-1} \binom{M+k-1}{2k} x^{2k}$$.

then we simply need to find:

$$[x^N](1 + P(x) + P(x)^2 + \ldots) = [x^N]\frac{1}{1 - P(x)}$$

using FFT in $O(N \log N)$.

### N is odd

We continue from the result of the even case. What we need to do now is to add a single odd chain at the end.

So we define the generating function of the odd chain:

$$Q(x) = \sum_{k=0}^\infty (-1)^k \binom{M+k}{2k+1} x^{2k+1}$$

Then we can simply find

$$[x^N] \frac{Q(x)}{1 - P(x)}$$

with FFT in $O(N \log N)$.

### Combining both cases

Since both GFs are "independent", we can simply find:

$$[x^N] \frac{1 + Q(x)}{1 - P(x)}$$

without the need for a parity check of $N$.
