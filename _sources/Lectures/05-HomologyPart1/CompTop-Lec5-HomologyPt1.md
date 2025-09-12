# Slide transcript

I am working on finding ways to increase accessibility of the beamer slides provided. The following is an automatically generated transcript from [the pdf of the slides](./CompTop-Lec5-HomologyPt1.pdf) but is still not perfect. I would be happy to hear feedback on how this transcript can be improved for additional usefulness.

# Lecture 5 - Here Comes the Homology

## Goals

Goals for today:

- Ch 2.4: Cycles and Boundaries
# Linear Algebra Review & Homology

**Definition:**
A field $(k,+,\cdot)$ is a set $k$ with two operations $+$ and $\cdot$
such that for any $a,b,c \in k$:

- Closure:

- Commutativity:

  - 
  - 

- Associativity:

  - 
  - 

- Identity:

  - 
  - 
- Inverses:

  - 
  - 

- Distributivity:

**Examples:**
## Vector space
**Definition:**
A vector space over a field $k$ is a set $V$ with vector addition and
scalar multiplication such that

- Associative $+$:

- Commutative $+$:

- Identity

  - 
  - 

- Inverses:

  - 
- Scalar vs. field mult:

- Distributivity:

  - 
  - 

**Examples:**

## Basis

**Definition:**
A basis for a vector space $V$ is a collection of vectors
$\{b_\alpha\}_{\alpha \in A}$ such that

- they are linearly independent and,

- they span $V$.

## Goal

Build a vector space from a simplicial complex!
## $p$-Chains

Let $K$ be a simplicial complex and fix a dimension $p$.
A $p$-chain is a finite formal sum of $p$-simplices in $K$, written
$$\alpha = \sum a_i \sigma_i

$$

![image](../Figures/SimplexExamples_WithTet-web.png)
## Addition of chains

$p$-chains are added component-wise: if $\alpha = \sum a_i \sigma_i$ and
$\beta = \sum b_i \sigma_i$, then
$\alpha + \beta =$
## Chain group

The collection of $p$-chains with addition is called the
$p^\text{th}$-chain group (vector space), $C_p(K)$.

**Some checks**

- Associative $+$:

- Commutative $+$:

- Zero element

- Inverses:
## Linear Transformations

A linear transformation between two vector spaces $V$ and $W$ is a map
$T:V\to W$ such that the following hold:

- 
- 

Matrix representation:
## Boundary maps[^1]

$$\begin{matrix}
\partial _p: & C_p(K) & \to & C_{p-1}(K)\
& \sigma = [v_0,\cdots,v_p] & \mapsto & \sum_{j=0}^p[v_0,\cdots,\widehat{v_j}, \cdots v_p]
\end{matrix}

$$
## Checking linearity

$$\partial_p(\alpha + \beta) = \partial_p(\alpha) + \partial_p(\beta); \hspace{.5in} \alpha = \sum a_i \sigma_i,\qquad  \beta = \sum b_i, \sigma_i

$$

## Homework

::: minipage
![image](../Figures/SimplexExamples_WithTet-web.png)
::: minipage
- $\partial_1([a,e]) =$

- $\partial_1([a,e] + [b,e]) =$

- $\partial_1([a,e] + [c,e] + [c,d] + [a,d]) =$

- $\partial_2([a,c,e] + [a,c,d]) =$

[^1]: Warning: We are assuming $\mathbb{Z}_2$ coefficients from now on!
