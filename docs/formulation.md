# Mathematical formulation

## 1. Problem instance

An instance is a pair $(P, B)$, where

$$P = \{(w_i, h_i)\}_{i=1}^{n}, \qquad B = [0, W] \times [0, H]$$

$P$ is a **multiset** of parts, each given by its width and height.
It is a multiset rather than a set because repeated parts carry
information: the reference instance contains $(125, 48.5)$ twice.

The board is modelled as the rectangle $[0, W] \times [0, H]$ rather
than the pair $(W, H)$. This fixes the origin at the lower-left
corner and orients both axes, which every inequality in the sections
below depends on.

### Reference instance

| $i$ | $w_i$ | $h_i$ |
|-----|-------|-------|
| 1, 2 | 125 | 48.5 |
| 3 | 68 | 43 |
| 4 | 67.5 | 43 |
| 5 | 57 | 43 |
| 6 | 50 | 43 |
| 7, 8 | 48.5 | 40 |

with $W = 244$, $H = 122$, all in centimetres.

## 2. Exact integer scaling

### 2.1 Why coordinates must be exact

The search decides where a part goes by testing whether two
coordinates coincide, for instance whether one part starts exactly
where another ends:

$$x_i + w_i = x_j$$

If such a test is wrong even once, a valid position is discarded and
the search may report *infeasible* for an instance that is in fact
feasible. The proof of optimality would then be worthless.

Floating-point arithmetic cannot guarantee these tests. A `float`
represents only rationals of the form

$$\frac{p}{2^k}, \qquad p, k \in \mathbb{Z}$$

so a value is stored exactly **iff** its denominator in lowest terms
is a power of two. $48.5 = \tfrac{97}{2}$ qualifies; $33.3 =
\tfrac{333}{10}$ does not, because $10 = 2 \cdot 5$ carries a factor
of $5$. Stored approximately, it accumulates error: three such parts
stacked give $99.89999\ldots$ instead of $99.9$, and the equality
test above fails.

### 2.2 The scaling

All part dimensions are rationals, since any measurement written with
finitely many decimals is one. A finite set of rationals always
admits a common denominator, so the instance can be rewritten in
integers.

Let $\mathcal{D} = \{w_i, h_i\}_{i=1}^{n} \cup \{W, H\}$ be the set
of all dimensions, and let $\lambda$ be the least common multiple of
their denominators in lowest terms. The scaled instance is

$$\tilde{w}_i = \lambda w_i, \quad \tilde{h}_i = \lambda h_i,
\quad \tilde{W} = \lambda W, \quad \tilde{H} = \lambda H$$

which is by construction free of decimals.

### 2.3 Why this changes nothing

Multiplying every length by the same factor is a change of units, not
a change of problem — the same figure measured in half-centimetres
instead of centimetres. Distances, and therefore which parts overlap
and which fit, are unaffected.

Formally, the map $s(x) = \lambda x$ sends any feasible layout of
$(P, B)$ to a feasible layout of $(\tilde{P}, \tilde{B})$, and
$s^{-1}(x) = x / \lambda$ sends it back. The correspondence is
one-to-one in both directions, so

$$(P, B) \text{ is feasible} \iff (\tilde{P}, \tilde{B})
\text{ is feasible}$$

No solution is gained and none is lost. The solver may therefore work
entirely in $\mathbb{Z}$ and divide by $\lambda$ only when reporting
results.

### 2.4 Why not exact rational arithmetic throughout

Python's `Fraction` is exact for every rational, so it would also be
correct. It is avoided for speed: each operation requires finding a
common denominator and reducing by a `gcd`, which is orders of
magnitude slower than integer arithmetic. The search performs
millions of coordinate comparisons, so `Fraction` is used exactly
once — to read the decimals without error and compute $\lambda$ —
after which everything is integer.

### 2.5 Reference instance

$\mathcal{D}$ contains $48.5$ and $67.5$, of denominator $2$; all
other values are integers. Hence $\lambda = 2$ and the board becomes
$488 \times 244$ in half-centimetres.

Note that for this particular instance every denominator is already a
power of two, so `float` would happen to be exact. The scaling is not
a fix for these numbers but a guarantee that correctness does not
depend on which numbers are supplied.

## 3. Geometry

A layout assigns to each part $i$ a position and an orientation. The
position is the coordinate of its lower-left corner,

$$(x_i, y_i) \in \mathbb{Z}^2$$

and the orientation is a binary variable

$$r_i \in \{0, 1\}$$

where $r_i = 1$ means the part is rotated by $90°$. Only these two
orientations matter: a rectangle rotated by $180°$ occupies exactly
the same region, so the four possible right-angle rotations collapse
into two distinct footprints.

The **effective dimensions** of part $i$ are therefore

$$w'_i = (1 - r_i)\, w_i + r_i\, h_i, \qquad
  h'_i = (1 - r_i)\, h_i + r_i\, w_i$$

This is a linear way of writing a swap. For $r_i = 0$ it gives
$(w'_i, h'_i) = (w_i, h_i)$; for $r_i = 1$ it gives $(h_i, w_i)$.
Writing it linearly rather than as a conditional matters because
these expressions must appear inside linear constraints later on.

### 3.1 Containment

Part $i$ lies inside the board iff

$$0 \le x_i, \qquad x_i + w'_i \le W$$
$$0 \le y_i, \qquad y_i + h'_i \le H$$

Since $(x_i, y_i)$ is the lower-left corner, the part occupies
$[x_i,\, x_i + w'_i] \times [y_i,\, y_i + h'_i]$, and containment is
simply the requirement that this rectangle be a subset of
$[0, W] \times [0, H]$.

These are four independent linear inequalities per part, so
containment on its own is easy: it defines a convex region of
feasible positions. All the difficulty of the problem comes from the
next condition.

### 3.2 Non-overlap

No two parts may share area. Both are rectangles with sides parallel
to the axes, and for such rectangles there is a simple criterion:
they are disjoint exactly when a straight line can be drawn between
them, either vertical or horizontal.

A vertical line exists when one part ends, horizontally, before the
other begins. A horizontal line exists when one ends vertically
before the other begins. That gives four cases, one per side, and at
least one of them must hold:

$$x_i + w'_i \le x_j \quad \lor \quad x_j + w'_j \le x_i
  \quad \lor \quad y_i + h'_i \le y_j \quad \lor \quad y_j + h'_j \le y_i$$

for every pair $i < j$ placed on the same board. The symbol $\lor$ is
inclusive disjunction: at least one must hold, and more than one may.

Each of the four is a single linear inequality, and each describes
infinitely many layouts rather than one. The first, for instance,
constrains only the horizontal axis — part $i$ must end before part
$j$ starts — and says nothing about height, so every vertical
placement remains available. A part sitting above and to the left of
another satisfies two of the four at once, which is permitted.

The inequalities are non-strict, so parts sharing an edge count as
disjoint: they touch along a line, which has zero area.

Compare this with containment, where four inequalities were joined by
**and** and all had to hold. Here they are joined by **or**, and a
choice appears: which of the four to satisfy. The choice cannot be
resolved locally — whether it was the right one depends on where
every other part ends up, and is only known once all parts are
placed. Section 5 takes up the consequences.