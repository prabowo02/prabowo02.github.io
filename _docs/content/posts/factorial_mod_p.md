---
title: "Factorial mod prime"
slug: factorial-mod-p
description: null
date: 2020-11-02T18:00:15+08:00
type: posts
summary: We are to compute $n! \bmod p$ in $O(\sqrt{p} \log p)$.
mathjax: true

---


We are to compute $n! \bmod p$ in $O(\sqrt{p} \log p)$.

## Basic Idea

If we define the polynomial $f(x) := \prod_{i=1}^n (x + i)$, then we can write $n! = f(0)$.

Let $v := \lfloor \sqrt n \rfloor$ and $g(x) := \prod_{i=1}^v (x+i)$, then

$$ n! = \left( \prod_{i=0}^{v-1} g(vi) \right) \prod_{i=v^2 + 1}^n i $$

The latter part of the product can be computed in $O(\sqrt p)$. We will try to find a fast way to compute
$g(0), g(v), \dots, g(v(v-1))$.

## Method

### 1. $O(\sqrt p (\log p)^2)$

Using FFT multipoint evaluation, we can compute $g(0), \dots, g(v(v+1))$ simultaneously. However, this algorithm uses a lot of polynomial division, which has heavy constant factor, and the speed will not be much faster than $O(p)$.

### 2. $O(\sqrt p \log p)$

$g(x)$ has roots $-1, -2, \dots, -v$ which is an arithmetic progression, and we want to evaluate $g(x)$ at $0, v, \dots, v(v-1)$ which is also an arithmetic progression. In this case, we will make use of Lagrange Interpolation.

Next, for a fixed $d$, we define $g_d(x) := \prod_{i=1}^d (x+i)$. Suppose we are able to compute $g_d(0), g_d(v), \dots, g_d(dv)$, then we can compute $g_{2d}(0), g_{2d}(v), \dots, g_{2d}(2dv)$ in $O(d \log d)$. If we are able to achieve this, then we can achieve the desired complexity.

Notice that $g_{2d}(x) = g_d(x) \cdot g_d(x + d)$. Let $G_d(i) := (g_d(i), g_d(v+i), \dots, g_d(dv + i))$, then from $G_d(0)$, we want to interpolate $G_d(d), G_d(dv), G_d(dv + d)$. This can be achieved using Lagrange Interpolation and FFT (NTT) in $O(d \log d)$ as described below.

Let there be a polynomial $h(x)$ and the values $h(0), h(1), \dots, h(d)$ are known, then the value $h(m + k)$ can be computed using Lagrange Interpolation (assuming $m + k - j$ has an inverse):

$$
\begin{align\*}
h(m + k) &= \sum_{i = 0}^d h(i) \prod_{j=0, i \neq j}^d \frac{m+k-j}{i-j} \\\\\\
         &= \left(\prod_{j=0}^d (m + k - j) \right) \left( \sum_{i=0}^d \frac{h(i)}{i! (d-i)! (-1)^{d-i}} \cdot \frac{1}{m + k - 1} \right)
\end{align\*}
$$

Notice that the right parenthesis is actually a convolution, so $h(m), h(m+1), \dots, h(m+d)$ can be computed in $O(d \log d)$. To interpolate $G_d(a)$ from $G_d(0)$, it is enough to substitute $m := av^{-1}$.

From the above, $n! \bmod p$ can be computed in $O(\sqrt p \log p)$.
