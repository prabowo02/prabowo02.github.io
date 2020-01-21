---
title: "Binomial Modulo Prime Power"
slug: binomial-mod-pe
description: null
date: 2019-12-04T16:03:30+08:00
type: posts
summary: Our goal is to solve ${n \choose m} \pmod {p^e}$, ($n, m, p^e < 10^{300}$, $p$ prime number). After precomputation, the number of operation to compute ${n \choose m} \pmod{p^e}$ is $O(e \log n)$. Define $(n!)\_p$ as the product of all positive integers $i \not\equiv 0 \pmod p$ for all $1 \leq i \leq n$. We are to to compute $(n!)\_p \pmod{p^e}$.
draft: false.

---


This is an attempt to translate [min_25's article](https://min-25.hatenablog.com/entry/2017/11/01/185400) with the help of Google Translate, and with a bit of modification.

Our goal is to solve ${n \choose m} \pmod{p^e}$, ($n, m, p^e < 10^{300}$, $p$: prime number).

The method differ from Andrew Granville's Binomial Coefficients modulo prime powers ([BinCoeff.pdf](https://web.archive.org/web/20170202003812/http://www.dms.umontreal.ca/~andrew/PDF/BinCoeff.pdf)). \
After precomputation, the number of operation to compute ${n \choose m} \pmod{p^e}$ is reduced from $O\left(e^2\left(\frac{\log n}{\log p} + \min(\log n, \log p)\right)\right)$ to $O(e \log n)$.

For the rest of the article, denote ${n \brack m}$ as [Stirling number of the first kind](https://en.wikipedia.org/wiki/Stirling_numbers_of_the_first_kind).

### Computation Method

Define $(n!)\_p$ as the product of all positive integers $i \not\equiv 0 \pmod p$ for all $1 \leq i \leq n$. Our goal is to compute $(n!)\_p \pmod {p^e}$.

Let $n = up + v$ where $u, v$ non-negative integers and $0 \leq v < p$.

For simplicity, we assume that $e < p$,

$$
\begin{align\*}
((up+v)!)\_p &= \left( \prod_{i=0}^{u-1} \prod_{j=1}^{p-1} (ip+j) \right) \cdot \prod_{j=1}^v (up + j) \\\\\\
&\equiv \left(\prod_{i=0}^{u-1} \left( \sum_{k=0}^{e-1} (ip)^k {p \brack {k+1}}\right)\right) \cdot \left(\sum_{k=0}^{e-1}(up)^k {{v+1} \brack {k+1}}\right) \pmod {p^e} \\\\\\
&= {p \brack 1}^u \left(\prod_{i=0}^{u-1}\left( 1 + \sum_{k=1}^{e-1} \frac{{p \brack {k+1}}}{{p \brack 1}}(ip)^k \right) \right) \cdot \left( \sum_{k=0}^{e-1} (up)^k {{v+1} \brack {k+1}} \right) \\\\\\
&= {p \brack 1}^u f_{p,e}(u) \left( \sum_{k=0}^{e-1} (up)^k {{v+1} \brack {k+1}} \right)
\end{align\*}
$$

It can be shown that $f_{p, e}$ is a polynomial of degree $(2e - 2)$ (proven below). By calculating the value of $f_{p, e}(0), \ldots, f_{p, e}(2e-2)$, the value of $f_{p, e}(u)$ can be computed in $O(e \log n)$ using [Lagrange interpolation](https://en.wikipedia.org/wiki/Lagrange_polynomial) (in $O(e)$ if you precompute the modular inverses).

#### Implementation and Time Complexity

First, compute the [$p$-adic valuation](https://en.wikipedia.org/wiki/P-adic_order) of ${n \choose m}$. If it is not less than $e$, then the modulo is 0. Otherwise, we factor out all the $p$ factors in $n!, m!, (n-m)!$ then we compute the factorials, and multiply with the $p$ factors at the end of the ${n \choose m}$ computation below.

After the 0 case handling, we do the steps as follow:

1. ${n \brack m} (1 \leq n \leq p, 1 \leq m \leq \min(p, e))$ is precomputed in $O(p \cdot \min(p, e))$
2. $f_{p, e}(0), \ldots, f_{p, e}(2e-2)$ for interpolation are precomputed in $O(e \cdot \min(p, e) + e \log p)$
3. Computation of $n!$ without the factor $p$ can be done by $\sum_{k=0}^\infty \left(\left\lfloor\frac{n}{p^k}\right\rfloor\_p\right)!$ in $O(e \log n)$

In total, there are around $O(pe + e^2 + e \log n)$ time complexity to compute ${n \choose m}$

#### Proof that $f_{p, e}$ is a polynomial

For any $e, p$ $(e \geq 1, p \geq 2)$, let $a_k$ be a rational number that exists under modulo $p$. Let,

$$ g(x, u) := \prod_{i=0}^{u-1} \left( 1 + \sum_{k=1}^{e-1} a_k (xi)^k \right) $$

Let $b_k$ be some other rational number satisfying:

$$
\begin{align\*}
\log(g(x, u)) &= \sum_{i=0}^{u-1} \log\left( 1 + \sum_{k=1}^{e-1} a_k(xi)^k \right) \\\\\\
 &= \sum_{i=0}^{u-1} \sum_{k=0}^\infty b_k x^k i^k \\\\\\
 &= \sum_{k=1}^\infty b_k x^k s_k(u)
\end{align\*}
$$

where $s_k(x) = \sum_{i=0}^x i^k$ is a polynomial of degree $k+1$. Continuing from above,

$$
\begin{align\*}
g(x, u) &= \exp\left( \sum_{k=1}^\infty b_k x^k s_k(u) \right) \\\\\\
&= 1 + \sum_{k=1}^\infty t_k(u) x^k
\end{align\*}
$$

where $t_k(u)$ is a polynomial of degree $2k$, because the highest polynomial degree obtained at $x^k$ is from $(b_1 x s_1(u))^k$. The coefficients of $t_k(u)$ are also rational number which exists under modulo $p$.

Substituting $x = p$ gives us the polynomial of $f_{p, e}(u)$:

$$ g(p, u) \equiv 1 + \sum_{k=1}^{e-1} t_k(u) \cdot p^k \pmod{p^e} $$

Therefore, $f_{p, e}(x)$ is a polynomial of degree $(2e - 2)$.


### Remark

- If $p$ is prime, ${p \brack i}$ $(2 \leq i < p)$ is divisible by $p$.
- If $p \geq 5$, ${p \brack 2}$ is divisible by $p^2$

Using these properties, looks like it is possible to further reduce the degree of $f_{p, e}(x)$.

### Source Codes

- min_25's implementation using [Python](https://gist.github.com/min-25/a5496354e10064a581d6b0c52c727a26).
- My implementation using [C++](https://github.com/prabowo02/CP/blob/master/binomial_mod_pe.cpp) (but it is not using big integer, only `__int128`, so it can only support for $n$ up to $10^{18}$).
