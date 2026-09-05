"""Problem instance: parts and board.

Symbols follow docs/formulation.md:
    P  multiset of parts, each (w_i, h_i)
    B  board rectangle [0, W] x [0, H], given as (W, H)
All dimensions in centimetres.
"""

P = [(125, 48.5)] * 2 + [(68, 43), (67.5, 43), (57, 43), (50, 43)] \
  + [(48.5, 40)] * 2
B = (244, 122)