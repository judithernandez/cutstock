from fractions import Fraction
from math import lcm

"""Problem instance: parts and board.

Symbols follow docs/formulation.md:
    P  multiset of parts, each (w_i, h_i)
    B  board rectangle [0, W] x [0, H], given as (W, H)
All dimensions in centimetres.
"""

P = [(125, 48.5)] * 2 + [(68, 43), (67.5, 43), (57, 43), (50, 43)] \
  + [(48.5, 40)] * 2
B = (244, 122)

def scale(P, B):
    """Map every dimension to an integer multiple of 1/lambda.

    See docs/formulation.md, section 2.
    Returns (P_s, B_s, lam): the scaled instance and the factor used.
    """
    D = [v for p in P for v in p] + list(B)
    lam = lcm(*[Fraction(str(v)).denominator for v in D])
    to_int = lambda t: tuple(int(Fraction(str(v)) * lam) for v in t)
    return [to_int(p) for p in P], to_int(B), lam


if __name__ == "__main__":
    D = [v for p in P for v in p] + list(B)
    P_s, B_s, lam = scale(P, B)

    print(f"P = {P}" )
    print(f"B = {B}")
    print(f"D = {D}")
    print(f"lam = {lam}")
    print(f"B_s = {B_s}")
    print(f"P_s = {P_s}")