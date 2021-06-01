---
title: "Sum of $C(N, i) \\times i^K$"
slug: sum-cnk-xk
description: null
date: 2021-06-01T23:08:09+08:00
type: posts
summary: Given $N \le 10^9$, $K \le 10^5$, find $$\sum_{i=0}^N \binom{N}{i} i^K$$ 
---


Have you ever been doing your grocery then suddenly felt the need to compute:

$$\sum_{i=0}^N \binom{N}{i} i^K $$

where $N \le 10^9$ and $K \le 10^5$? Well you are in luck, because I'm about to show you how.

Consider the binomial expansion:

$$f_0(x) := (1 + x)^N = \sum_{i=0}^N \binom{N}{i} x^i$$

If you differentiate then multiply by $x$, you will get:

$$f_1(x) := x \frac{d}{dx}(1 + x)^N = \sum_{i=0}^N \binom{N}{i}\cdot i \cdot x^i$$

Then repeatedly differentiate and multiply by $x$ (i.e. $f_k(x) = x \frac{d}{dx} f_{k - 1}(x)$), then you will end up with:

$$f_K(x) = \sum_{i=0}^N \binom{N}{i} i^K x^i$$

Evaluate $f_K(1)$ then you will get the answer to the original question.

The value of $f_K$ is actually:

$$f_K(x) = \sum_{i=0}^K S(K, i) \cdot \binom{N}{i} \cdot i! \cdot 2^{N-i} \cdot x^i$$

where $S$ is the Stirling number of the second kind.
The formula can be easily shown using induction following the property $S(N, K) = K \cdot S(N - 1, K) + S(N - 1, K - 1)$.

The computation of $\binom{N}{i} i!$ for all $0 \le i \le K$ can be easily computed in $O(K)$, and the computation of $S(K, i)$ can be done using FFT ([Touchard Polynomial](https://en.wikipedia.org/wiki/Touchard_polynomials)) in $O(K \log K)$.

In case you need something more general:

$$\sum_{i=0}^N \binom{N}{i} \cdot i^K \cdot A^i \cdot B^{N - i} = \sum_{i=0}^K S(K, i) \cdot \binom{N}{i} \cdot i! \cdot A^i \cdot (1 + B)^{N - i}$$

which can actually be obtained by starting the initial equation from $(B + x)^N$ and substitute $x = A$.

You can now solve [this problem](https://codeforces.com/problemset/problem/1278/F) for $K \le 10^5$.
