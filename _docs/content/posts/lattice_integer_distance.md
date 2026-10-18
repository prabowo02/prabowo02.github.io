---
title: "Counting Lattice Points at a Distance $r$"
slug: lattice-integer-distance
description: null
date: 2026-10-18T20:59:08+08:00
type: posts
summary: Count the number of lattice points $(x, y) \in \mathbb{Z}^2$ such that  $x^2 + y^2 = r$.
---

## 1. 2D Grid

You want to find the number of lattice points $(x, y) \in \mathbb{Z}^2$ such that  $x^2 + y^2 = r$. Equivalently, we are counting how many [Gaussian integers](https://en.wikipedia.org/wiki/Gaussian_integer) with norm $\sqrt{r}$ there are.

First, factorise $r$ and group the primes according to their modulo $4$:


$$r = 2^a \prod_{p_i \equiv 1 \pmod 4} p_i^{e_i} \prod_{q_j \equiv 3 \pmod 4} q_j^{f_j}.$$

If **any** $f_j$ is odd, then the count is $0$. Otherwise, the count is:

$$4 \prod (e_i + 1)$$

## 2. Triangular Grid

You want to count the number of triangular lattice with a fixed distance $d$, i.e. you want to count $(x, y) \in \mathbb{Z}^2$ such that $x^2 - xy + y^2 = r$. Equivalently, we are counting how many [Eisenstein integers](https://en.wikipedia.org/wiki/Eisenstein_integer) with norm $\sqrt{r}$ there are.

First, factorize $r$ and group the prime factors according to their modulo 3:
$$r = 3^a \prod_{p_i \equiv 1 \pmod 3} p_i^{e_i} \prod_{q_j \equiv 2 \pmod 3} q_j^{f_j}.$$

If **any** $f_j$ is odd, then the count is $0$. Otherwise, the count is:
$$6 \prod (e_i + 1)$$

## 3. 3D Sphere


You want to find the number of lattice points $(x, y, z) \in \mathbb{Z}^3$ such that $x^2 + y^2 + z^2 = r^2$. Note that we require the distance to be also an **integer**, so the R.H.S. is $r^2$ **not** $r$.
The conditions for non-integers are a little tricky, but for integers they are highly simplified.

First, factorise $r$ and group the primes according to their modulo $4$:

$$r = 2^a \prod_{p_i \equiv 1 \pmod 4} p_i^{e_i} \prod_{q_j \equiv 3 \pmod 4} q_j^{f_j}.$$

Then, the count is:

$$6 \prod_{p_i \equiv 1 \pmod 4} p_i^{e_i} \prod_{q_j \equiv 3 \pmod 4} \left( 1 + (q_j + 1)\frac{q_j^{f_j} - 1}{q_j - 1} \right)$$
