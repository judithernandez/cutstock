"""Normalized search over supported layouts.

See docs/formulation.md, section 4.
A placed part is a tuple (x, y, w, h).
"""


def candidates(placed):
    """Candidate positions for the next part.

    Returns the pairs in X(S) x Y(S), where X(S) holds 0 and the
    right edge of every placed part, and Y(S) holds 0 and the top
    edge of every placed part.
    """
    xs = sorted({0} | {x + w for x, y, w, h in placed})
    ys = sorted({0} | {y + h for x, y, w, h in placed})
    return [(x, y) for y in ys for x in xs]