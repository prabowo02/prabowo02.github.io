---
title: "Notes on Fast Fourier Transform"
slug: fft
description: null
date: 2020-12-17T17:55:15+08:00
type: posts
summary: A summary of what FFT can do.
mathjax: false

---

This is not a tutorial. It's just an overview for those who already (hopefully) understood FFT.
(Actually, more of a personal note to myself)

### So what is FFT?

DFT but fast

### What DFT does?

Converts a polynomial into point value forms where the points sampled are principal $n$-th root of unity.

### Can you inverse the transformation?

Yes, by doing the exact same thing as DFT but the sampled points are inverted too, then divide the final result by $n$.

### How to do DFT?

Evaluate each sample point in $O(N)$, and you end up in $O(N^2)$ transformation.

### Can you do better?

Yes, that's when FFT comes in.

### How to FFT?

The most commonly used algorithm is Cooley-Tukey algorithm, and the DFT size is usually taken in the form of $2^k$. It is basically a Divide and Conquer algorithm, by separating the odd and even terms, and does FFT recursively. By doing some reordering using bit reversal, you can actually does an iterative version of it. Final complexity is $O(N \log N)$ without any additional space.
Details on FFT can be found in this [Codeforces blog](https://codeforces.com/blog/entry/43499).

### How does FFT help to solve problems?

The main idea is sum-convolution (can also be viewed as polynomial multiplication). That is, given two sequences $a$ and $b$, for each pair of $i$, $j$, $a_i \times b_j$ is "contributed" to $c_{i + j}$, where $c$ is the convolution.
The way to do that is: $c = IFFT(FFT(a) * FFT(b))$, where $\*$ is point-wise multiplication.

Note that by default DFT is a cyclic convolution, i.e. $a_i b_j$ is actually contributed to $c_{(i + j) \bmod n}$ (in other words, the multiplication is in modulo $(x^n - 1)$). Therefore, to avoid "overflow", you pad the polynoms with $0$s until the polynom size is of size $2^k ≥ |a| + |b|$.

[An example problem](https://open.kattis.com/problems/aplusb) on how FFT helps. For this problem, you create a polynom where the coefficient of $x^i$ is the number of elements in a that are equal to $i$. After that, you square the polynomial, then start processing from there.

Sometimes FFT is closely related to string "matching" too. In this case, usually each alphabet is associated with a polynom where coefficient $x^i$ equals to $1$ if $s_i$ is equal to the associated alphabet, or $0$ otherwise. Here is [an example](https://codeforces.com/problemset/problem/528/D).

Another time, a DP problem can be optimized using FFT too. This can be noticed when the transition is $O(N)$ and looks like a convolution. In the case of DP, often we mention the polynomial as (Ordinary) Generating Function. The coefficients of the OGF will be of the interest when arriving at the final answer.

Talking about generating functions, there is also something called Exponential Generating Function. In EGF, the coefficient of $x^i$ is $\frac{\text{actual value}}{i!}$. And when you multiply, the contributed value is $\binom{i + j}{i} a_i b_j$.

### What are some popular generating functions?

- $(1 + x)^n$. OGF for binomial coefficients $(\binom{n}{0}, \binom{n}{1}, \dots, \binom{n}{n})$.
- $\frac{1}{1 - x}$. OGF for $(1, 1, \dots)$. This is handy if you want to get the "prefix sum" of a GF by simply divides it by $(1 - x)$.
- $\frac{1}{(1 - x)^k}$. OGF for $(\kern-.5em(\genfrac{}{}{0pt}{}{n}{k})\kern-.5em) = \binom{n + k - 1}{k - 1}$. Used for counting multisets.
- $\frac{x^k}{(1 - x)^{k + 1}}$. OGF for $\binom{n}{k}$. The "column" of binomial cofficients.
- $y = xy + xy^2 + 1 \implies y = \frac{1}{1 - x - x^2}$. OGF for Fibonacci number.
- $y = 1 + xy^2 \implies y = \frac{2}{1 + \sqrt{1 - 4x}}$. OGF for Catalan number.
- $\exp(x)$. EGF for $(1, 1, \dots)$.
- $\exp(\exp(x) - 1)$. EGF for Bell numbers. It can be used to count number of set partitions.
- $\prod_{i=0}^{n-1}(x + i)$. OGF for Stirling number first kind.
- $\exp(-x) \sum_{i=0}^n \frac{i^n x^i}{i!}$. OGF for Stirling number second kind, also known as Touchard polynomial.
- $\frac{(-\log(1 - x))^k}{k!}$. EGF for "column" Stirling number first kind. Note that $-\log(1 - x) = \sum \frac{x^i}{i}$.
- $\frac{(\exp(x) - 1)^k}{k!}$. EGF for "column" Stirling number second kind.
- $y \exp(y) = x$. Lambert W function. Also EGF for number of rooted enumerated trees. Can be computed using Lagrange–Bürmann formula.

### Why are there divisions and exponent?

These are operations on formal power series. The idea is, if you want to compute $Q$ that satisfies $f(Q) = 0$, for some polynom $Q$ and function $f$, we can use the Newton's method $Q_{n+1} = Q_n - \frac{f(P)}{f'(P)}$.

For example, computing $Q = \frac{1}{P} \implies Q^{-1} - P = 0 \implies f(Q) = Q^{-1} - P$ \
$Q := Q - \frac{Q^{-1} - P}{-Q^{-2}} = Q + (Q - PQ) = 2Q - PQ^2$

Another example, computing $Q = \sqrt{P} \implies Q^2 - P = 0 \implies f(Q) = Q^2 - P$ \
$Q := Q - \frac{Q^2 - P}{2Q} = \frac{1}{2}(Q + \frac{P}{Q})$

In every iteration of the Newton's method, the precision is doubled, i.e. the degree of $Q$ is improved from $n$ to $2n + 1$, and initially $Q$ is only a constant.

And here are several operations along with their tricks:

- Additions and subtractions are obvious.
- Multiplication done by FFT.
- Differentiation and integral are straightforward.
- $\frac{1}{P}$, $\sqrt{P}$, $\exp(P)$ can be done using Newton's method.
- $\log(P) = \int \frac{P'}{P}$
- $P(x)^a = \exp(a \log(P(x)))$
- $\arctan(P) = \int \frac{1}{1 + P^2}$
- Generally, inverse trigonometric function can be computed from [their derivatives](https://en.wikipedia.org/wiki/Inverse_trigonometric_functions#Derivatives_of_inverse_trigonometric_functions).
- $P^{-1}(x)$ i.e. the inverse function, can be done using Lagrange–Bürmann formula

### What about modulo?

You can find the details of division, modulo, multipoint evaluation, and interpolation in [adamant's lecture note](https://drive.google.com/file/d/1B9BIfATnI_qL6rYiE5hY9bh20SMVmHZ7/view).

### Do the points must be roots of unity?

You can actually compute for $\\{{z^i\\}}\_{i=0}^{n-1}$, for any complex number $z$. This is called Chirp Z-transform and can be done using Bluestein's algorithm. The main idea is to write $ij = \binom{i + j}{2} - \binom{i}{2} - \binom{j}{2}$. \
Hence, $\sum(a_i z^{ik}) = \sum \left(a_i z^{-\binom{i}{2}} z^{\binom{i + k}{2}} \right) z^{-\binom{k}{2}}$, which is exactly a convolution and can be computed using FFT. [Example problem](https://codeforces.com/problemset/problem/1054/H).

### Can we compute any size DFT quickly?

Yes, by using CZT, and $z$ such that $z$ is primitive $n$-th root of unity where $n$ is the DFT size. One example problem that use DFT any size can be found on [Codeforces](https://codeforces.com/contest/901/problem/E).

### Must the polynomial be monic? 

Multidimentional DFT can be done by performing DFT on each dimension one by one. An example problem can be found [here](https://codeforces.com/gym/102441/problem/E). In this problem, <span style="color:white">you will need both sum-convolution for one variable, and xor-convolution for the other in a single polynomial</span> (spoiler in white text).

### Xor-convolution?

Xor convolution means that $a_i b_j$ is contributed to $c_{i \oplus j}$. It is basically the standard DFT but multidimensional, and each dimension is DFT of size $2$. This is working because xor is basically addition in vector space $\bmod 2$.

### Can we have other bitwise convolutions?

In XOR, you tranform $(u, v)$ to $(u + v, u - v)$. \
In AND, you tranform $(u, v)$ to $(u + v, v)$. After performing AND-tranform, you actually ends up with sum of supermasks. \
In OR, you tranform $(u, v)$ to $(u, u + v)$. After performing OR-tranform, you actually ends up with sum of submasks. \
In NAND, you perform AND, then do the bit inverting (i.e. swap coefficients of bit 0 and bit 1).

An example problem that uses various binary gates can be found on [Codeforces](https://codeforces.com/contest/1033/problem/F)

### Must DFT be operated in complex?

DFT works over an arbitrary ring, as long as you are using the principal $n$-th root of unity as the sampled points. Primitive $n$-th root is also principal $n$-th root. Since primitive roots are roots of the $n$-th cyclotomic polynomial, by ensuring your points satisfy $\Phi_n(x) = 0$, then DFT should work. [An example problem](https://codeforces.com/problemset/problem/1103/E).

### Can we compute the product of multiple polynomials?

Suppose that the sum of degrees of the given polynomials is $N$, then we can do either of the following:

- Use priority queue, and compute the multiplication of every two polynomials with the lowest degrees.
- Use Divide and Conquer, then split the polynomials to sum of degrees approximately N/2, then recurse
- Divide and Conquer, then split half of the polynomials, regardless of the degrees

All of these run in $O(N \log^2 N)$. [This problem](https://codeforces.com/problemset/problem/1257/G) require this technique.
