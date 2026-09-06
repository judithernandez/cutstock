"""Geometric predicates.

See docs/formulation.md, section 3.
A placed part is described by (x, y, w, h): (x, y) is its lower-left
corner and (w, h) its effective dimensions after rotation.
"""


def fits_in_board(x, y, w, h, W, H):
    """Containment: the part lies inside [0, W] x [0, H]."""
    return 0 <= x and 0 <= y and x + w <= W and y + h <= H