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