---
title: "Project Euler #242"
description: This post
slug: project-euler-242
description: null
date: 2019-11-29T12:15:14+08:00
type: posts
summary: This post will give the analysis to Project Euler 242 from hackerrank, which is an extended version from the original Project Euler. Given 5 integers $m$, $r$, $n$, $k$, and $M$, count the number of k-subsets of $\\{1, 2, \ldots, n\\}$ such that the sum of the subset is $r \pmod m$. This is actually an extended version of IMO 1995 P6 (having $m = p$, $n = 2p$, $k = p$, $r = 0$). A discussion to this problem can be found in AOPS.
draft: false

---

This post will give the analysis to [Project Euler #242](https://www.hackerrank.com/contests/projecteuler/challenges/euler242/problem) from hackerrank, which is an extended version from the [original](https://projecteuler.net/problem=242).

### Problem Statement

Given 5 integers $m$, $r$, $n$, $k$, and $M$, count the number of k-subsets of $\\{1, 2, \ldots, n\\}$ such that the sum of the subset is $r \pmod m$. Let the answer be $S$, output $S \times m$ modulo $M$. 

#### Constraints

- $2 \leq m \leq 10^{11}$
- $0 \leq r \leq m$ 
- $1 \leq k \leq n \leq 10^{18}$
- For each positive divisor $d$ of $m$: $n \mod d \leq k \mod d$
- $2 \leq M \leq 2^{62}$
- The largest prime factor of $M$ is less than $10^5$

### Solution

This is actually an extended version of [IMO 1995 P6](https://www.imo-official.org/year_info.aspx?year=1995) (having $m = p$, $n = 2p$, $k = p$, $r = 0$). A discussion to this problem can be found in [AOPS](https://artofproblemsolving.com/community/c6h15112p107230).

Back to the original problem, consider the generating function $(1 + xy)(1 + xy^2) \ldots (1 + xy^n)$. Our answer will be the sum of coefficients of $x^k y^r, x^k y^{r+m}, x^k y^{r+2m}, \ldots$.

To get this sum, we use the [Series Multisection](https://en.wikipedia.org/wiki/Series_multisection) formula on the y coefficients, then our generating function become:

$$\frac{1}{m} \sum_{l=0}^{m-1} \left( \omega^{-lr} \prod_{i=1}^n (1 + x\omega^{li}) \right)$$

where $\omega$ is the primitive $m$-th root of unity. Since the final answer will be multiplied by $m$, the $\frac{1}{m}$ will be ignored for the rest of this post. Now our goal is to find the coefficient of $x^k$ from that equation.

Using the [Cauchy Binomial Theorem](http://mathworld.wolfram.com/CauchyBinomialTheorem.html), we convert our equation above to:

$$\sum_{l=0}^{m-1} \left( \omega^{-lr} \sum_{i=0}^n x^i \omega^{li(i+1)/2} {n \brack i}\_{\omega^l} \right)$$

Since we only care with the $x^k$ coefficient, then the answer to our original problem is the evaluation of:

$$ \sum_{i=0}^{m-1} \left( (\omega^{i})^{k(k+1)/2 - r} {n \brack k}\_{\omega^i} \right) $$

We will compute the sum for each primitive of $\omega^i$ separately. Denote $\omega_d$ as the primitive $d$-th root of unity. Also note the [q-Lucas theorem](https://www.math.upenn.edu/~peal/polynomials/q-analogues.htm#prelimQanaloguesQLucas): ${n \brack k}\_{\omega_d} = {\lfloor n/d \rfloor \choose \lfloor k/d \rfloor } {n \mod d \brack k \mod d}\_{\omega_d}$. \
Since $n \mod d \leq k \mod d$, the value of ${n \mod d \brack k \mod d} = 1$ if $n \equiv k \pmod d$, $0$ otherwise. \
With these in mind, we rewrite our equation to:

$$ \sum_{d|m} \left( \sum_{(d, i) = 1}^d (\omega_d^i)^{k(k+1)/2 - r}  {n \choose k}[n \equiv k \pmod d] \right) $$

where $[]$ is the [Iverson bracket](https://en.wikipedia.org/wiki/Iverson_bracket). Recall that the sum of $k$-th power of the $d$-th root of unity is $\frac{\mu(d / \gcd(k, d)) \varphi(d)}{\varphi(d / \gcd(k, d))}$, where $\mu$ is the [Möbius function](https://en.wikipedia.org/wiki/M%C3%B6bius_function) and $\varphi$ is the [Euler's Totient function](https://en.wikipedia.org/wiki/Euler%27s_totient_function). \
Therefore, our final answer is:

$$ \sum_{d|m} \left( \frac{\mu\left(\frac{d}{\gcd(k(k+1)/2 - r, d)}\right) \varphi(d)}{\varphi\left(\frac{d}{\gcd(k(k+1)/2 - r, d)}\right)} {n \choose k}[n \equiv k \pmod d] \right) $$

And now, for the computational part. Compute the final sum for every prime factor of $M$, then combine the answers using [Chinese Remainder Theorem](https://en.wikipedia.org/wiki/Chinese_remainder_theorem). The computation of binomial theorem modulo $p^e$ can be computed in $O(e(p + e + \log n))$, which is described in this [post](/posts/binomial-mod-pe). \
The computation of the divisors of $m$ and all its mobius and euler totient values can be computed in $O(\sqrt m)$

Therefore, the overall complexity is $O(\sqrt m + \log M \log n)$.
