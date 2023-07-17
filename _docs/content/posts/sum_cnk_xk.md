---
title: "Sum of $C(N, i) \\times i^K$"
slug: sum-cnk-xk
description: null
date: 2021-06-01T23:08:09+08:00
type: posts
summary: Given $N \le 10^9$, $K \le 10^5$, find $$\sum_{i=0}^N \binom{N}{i} i^K$$ 
---


Have you ever felt the need to compute:

$$\sum_{i=0}^N \binom{N}{i} i^K $$

where $N \le 10^9$ and $K \le 10^5$? Well you are in luck, because I'm about to show you how.

Consider the binomial expansion:

$$f_0(x) := (1 + x)^N = \sum_{i=0}^N \binom{N}{i} x^i$$

If you differentiate then multiply by $x$, you will get:

$$f_1(x) := x \frac{\mathrm{d}}{\mathrm{d}x}(1 + x)^N = \sum_{i=0}^N \binom{N}{i}\cdot i \cdot x^i$$

Then repeatedly differentiate and multiply by $x$ (i.e. $f_k(x) = x \frac{\mathrm{d}}{\mathrm{d}x} f_{k - 1}(x)$), then you will end up with:

$$f_K(x) = \sum_{i=0}^N \binom{N}{i} i^K x^i$$

Evaluate $f_K(1)$ then you will get the answer to the original question.

The value of $f_K$ is actually:

$$f_K(x) = \sum_{i=0}^K S(K, i) \cdot (N)\_i \cdot (1 + x)^{N-i}$$

where $S$ is the Stirling number of the second kind and $(N)\_i$ is the falling factorial $N(N - 1) \ldots (N - i + 1)$.
The formula can be easily shown using induction following the property $S(N, K) = K \cdot S(N - 1, K) + S(N - 1, K - 1)$.

The computation of $(N)\_i$ for all $0 \le i \le K$ can be easily computed in $O(K)$, and the computation of $S(K, i)$ can be done using FFT ([Touchard Polynomial](https://en.wikipedia.org/wiki/Touchard_polynomials)) in $O(K \log K)$.

In case you need something more general:

$$\sum_{i=0}^N \binom{N}{i} \cdot i^K \cdot A^i \cdot B^{N - i} = \sum_{i=0}^K S(K, i) \cdot (N)\_i \cdot A^i \cdot (A + B)^{N - i}$$

which can actually be obtained by starting the initial equation from $(Ax + B)^N$.

You can now solve [Codeforces edu round problem Cards](https://codeforces.com/problemset/problem/1278/F) for $K \le 10^5$.

## Moment Generating Function

Another way (and perhaps more elegant way) to arrive at that equation is to use the moment generating function. Let

$$M_X(t) = \mathrm{E}(\exp(tX)) = \sum_{i=0}^\infty \frac{t^i \mathrm{E}(X^i)}{i!}$$

Now, if you differentiate $M_X(t)$ for $k$ times, and substitute $t = 0$, you will end up with $\mathrm{E}(X^k)$.

So if you start from $(A \exp(x) + B)^N$, then you differentiate $K$ times, you will obtain:

$$\frac{\mathrm{d}^K}{\mathrm{d}x^K} (A \exp(x) + B)^N = \sum_{i = 0}^K S(K, i) \cdot (N)\_i \cdot A^i \cdot (A \exp(x) + B)^{N - i} \cdot \exp(ix)$$

Again, the formula above can be easily shown (roughly shown below) using induction following the recursion property of the Stirling second kind.

Substituting $x = 0$, then you will arrive at the same equation.

### Some kind of proof

We will prove that equation from the moment generating function section.

Let $f(i) = (N)\_i \cdot A^i \cdot (A \exp(x) + B)^{N - i} \cdot \exp(ix)$, which in particular $f(0) = (A \exp(x) + B)^N$.

Then,

$$\frac{\mathrm{d}f(i)}{\mathrm{d}x} = (N)\_{i + 1} \cdot A^{i + 1} (A \exp(x) + B)^{N - i - 1} \exp((i+1)x) + i \cdot (N)\_i \cdot A^i \cdot (A \exp(x) + B)^{N - i} \cdot \exp(ix)$$

Substitute them back using $f$:

$$\frac{\mathrm{d}f(i)}{\mathrm{d}x} = f(i + 1) + i \cdot f(i)$$

Now write:

$$\frac{\mathrm{d}^k}{\mathrm{d}x^k} (A \exp(x) + B)^N = \sum_{i = 0}^k c_{k, i} \cdot f(i)$$

Differentiate it once, then you will get:

$$\frac{\mathrm{d}^{k+1}}{\mathrm{d}x^{k+1}} (A \exp(x) + B)^N = \sum_{i = 0}^{k+1} (c_{k, i - 1} + i \cdot c_{k, i}) \cdot f(i)$$

And notice that $c_{k + 1, i} = c_{k, i - 1} + i \cdot c_{k, i}$ is actually the same recurrence as the Stirling number of the second kind, which roughly end the proof.
