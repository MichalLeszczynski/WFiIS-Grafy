#!/usr/bin/env python3
from spacja.functions import *


def test_is_valid_graph_sequence():
    cases = [
        ([4, 3, 3, 2, 2, 1, 1], True),
        ([4, 3, 3, 2, 2, 1], False),
        ([6, 6, 6, 4, 4, 2, 2], False),
    ]
    for seq, val in cases:
        assert is_valid_graph_sequence(seq) == val
