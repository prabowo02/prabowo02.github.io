---
title: "Project Euler #100"
slug: project-euler-100
description: null
date: 2020-07-10T00:24:26+08:00
type: posts
summary: Given $P$, $Q$, and $M$, find smallest $n$ such that $\frac{b(b-1)}{n(n-1)} = \frac{P}{Q}$, where $b$ and $n$ are positive integers and $n > M$.

---

This post will give the analysis to [Project Euler #100](https://www.hackerrank.com/contests/projecteuler/challenges/euler100/problem) from hackerrank, which is an extended version from the [original](https://projecteuler.net/problem=100).

## Problem

Given $P$, $Q$, and $M$, find smallest $n$ such that $\frac{b(b-1)}{n(n-1)} = \frac{P}{Q}$, where $b$ and $n$ are positive integers and $n > M$.

Constraints:
- $2 ≤ M ≤ 10^{15}$.
- $0 < P < Q ≤ 10^7$.

## Solution

To simplify matters, we assume $P$ and $Q$ are coprime. If they are not, simply divide both of them with their gcd.
The equation $\frac{b(b-1)}{n(n-1)} = \frac{P}{Q}$ can be rewritten as $Q(b(b-1)) = P(n(n-1)) \Rightarrow Q(2b-1)^2 - P(2n-1)^2 = Q - P$ by completing the square.

Let $Q = qr^2$ where $r$ is the largest divisor of $Q$ such that $r^2 | Q$. Therefore $q$ is squarefree.
Multiplying both sides of the equation with $q$, we obtain:

$$(qr(2b-1))^2 - Pq(2n-1)^2 = q(Q-P)$$

Notice that this is actually the generalized Pell equation $x^2 - Dy^2 = N$, with $D = Pq$ and $N = q(Q-P)$.
Some readers may notice that multiplying both sides with $Q$ instead of $q$ will make the equation looks easier, but the reason to that may have to wait until the next few parts of the solution.

There are two cases when solving the Pell equation $x^2 - Dy^2 = N$:
- $D$ is a square.
- $D$ is not a square.

### $D$ is a square

If $D$ is a square, that means $Pq$ is a square, or equivalently $PQ$ is also a square.
Let $d = \sqrt{PQ}$, $x = Q(2b-1)$, $y = (2n-1)$, then we can rewrite the equation $x^2 - PQy^2 = Q(Q-P)$ as:

$(x - dy)(x + dy) = Q(Q-P)$

Factoring $Q(Q-P)$ into $a \times b$ where $a$ and $b$ are integers, we solve these two simultaneous linear equations:

$$x - dy = a$$
$$x + dy = b$$

After solving these two equations for all $a$ and $b$, we obtain all solutions to $x$ and $y$. Hence, $b$ and $n$ can also be determined.

### $D$ is not a square

If $D$ is not a square, apply the LMM algorithm ([Solving the generalized Pell equation by John P. Robertson](http://www.jpr2718.org/pell.pdf) page 16). The first part of the algorithm is to find all $z$ such that $z^2 = D \pmod {|m|}$ where $m = \frac{N}{f^2}$ and $f^2 | N$. Finding such $z$ may be hard in general, but there are a few special property on this specific equation:

- It can be seen that $q$ and $Q-P$ are coprime. Therefore we can split the congruence into two congruences and merge them later using CRT (Chinese Remainder Theorem).
- $f^2$ only divides $Q-P$ because $q$ is squarefree. Therefore we do not need to consider the divisors of $q$ when considering the equation $x^2 = Pq \mod q$.

#### Solving $x^2 = Pq \mod q$

It is obvious that $Pq = 0 \mod q$ because $q | Pq$. The congruence became $x^2 = 0 mod q$. Since q is squarefree, there is only one solution to $x$, which is $0$ (how convenient). This is the reason why we are not using the equation $x^2 - PQ = Q(Q-P)$, because solving $x^2 = 0 \mod Q$ may yield tens or hundreds of solutions.

#### Solving $x^2 = Pq \mod (Q-P)$

First, rewrite the congruence:

$ \ \ \ \ \ \ \  x^2 = Pq \pmod{Q-P}$ \
$\Longrightarrow x^2 = Pq + q(Q-P) \pmod{Q-P}$ \
$\Longrightarrow x^2 = Qq \pmod {Q-P}$ \
$\Longrightarrow x^2 = (qr)^2 \pmod{Q-P}$ 

This also works when the modulo is $\frac{Q-P}{f^2}$, we will obtain the same congruence $x^2 = (qr)^2 \pmod{\frac{Q-P}{f^2}}$.

Since we already know one solution to $x$ (which is $qr$), then the other solutions can be determined quite easily.

To solve $x^2 = a^2 \pmod m$, factor $m$ into its prime factors $p_1^{k_1} \times p_2^{k_2} \times \ldots \times p_n^{k_n}$.
Then solve $x^2 = a^2 \pmod{p^k}$ for each prime factor $p$ of $m$. Lastly, merge them using CRT.
Since $qr$ and $Q-P$ are coprime, we assume that $a$ and $m$ are coprime too.

##### Solving $x^2 = a^2 \pmod {2^k}$

Three cases:
- $k = 1$: Only one solution to $x$, namely $x = 1$.
- $k = 2$: Two solutions, namely $x = 1$ and $x = 3$.
- $k > 2$: Four solutions, $x = a \pmod {2^k}$, $x = -a \pmod {2^k}$ $x = a + 2^{k-1} \pmod {2^k}$, $x = -a + 2^{k-1} \pmod {2^k}$.

Proves are left to the readers.

##### Solving $x^2 = a^2 \pmod {p^k}$ where $p$ odd primes.

Only two solutions exist: $x = a \pmod {p^k}$ and $x = -a \pmod {p^k}$.

At this point, we already have a way to obtain all $z$ quickly. 
Apply PQa with $P_0 = z$, $Q_0 = \frac{N}{f^2}$, $D = D$ until we find the first $(f \times G_i)^2 - (f \times Q_i)^2 = N$ (refer to the paper above for more explanations)

We also have to find sufficiently many solutions to $x^2 - Dy^2 = 1$ to generate the solutions from the fundamentals above.
With these, the solution to the original equation can be found.
