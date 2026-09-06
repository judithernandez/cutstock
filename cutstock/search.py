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

from cutstock.geometry import fits_in_board, overlaps


def search(parts, W, H):
    """Find a valid layout of all parts on one board, or None.

    See docs/formulation.md, section 5.1.
    parts: list of (w, h), already scaled to integers.
    Returns a list of placed parts (x, y, w, h), or None.
    """
    placed = []

    def place(i):
        # base case: no parts left to place
        if i == len(parts):
            return True
        
        # area pruning: docs/formulation.md, section 5.2
        free = W * H - sum(w * h for _, _, w, h in placed)
        if sum(w * h for w, h in parts[i:]) > free:
            return False

        w0, h0 = parts[i]

        for (x, y) in candidates(placed):
            for (w, h) in {(w0, h0), (h0, w0)}:

                # does it stay inside the board?
                if not fits_in_board(x,y,w,h,W,H):
                    continue

                # does it hit anything already placed?
                if any(overlaps((x,y,w,h),p) for p in placed):
                    continue

                placed.append((x,y,w,h))
                if place(i+1):
                    return True
                placed.pop()          # backtrack

        return False

    return placed if place(0) else None